"""
智析 AI - 周报生成 + 历史记录路由
"""
from fastapi import APIRouter, Request, HTTPException, Depends
from sqlalchemy.orm import Session
import httpx

from database import get_db
from models import User, Report, AccessLog
from services import decode_access_token

router = APIRouter(prefix="/api", tags=["report"])

# ============ AI 配置 ============
AI_CONFIGS = {
    "deepseek": {
        "base_url": "https://api.deepseek.com/v1",
        "model": "deepseek-chat",
        "api_key": "",
    },
    "openai": {
        "base_url": "https://api.openai.com/v1",
        "model": "gpt-3.5-turbo",
        "api_key": "",
    },
    "lmstudio": {
        "base_url": "http://localhost:1234/v1",
        "model": "qwen2.5-1.5b-instruct",
        "api_key": "***",
    },
}

# ============ Prompt 模板 ============
PROMPTS = {
    "zh": {
        "professional": "你是一位专业的销售分析专家。请根据以下销售对话/客户沟通记录，进行深度分析。\n\n分析要求：\n1. 识别客户需求和痛点\n2. 评估销售机会等级（高/中/低）\n3. 分析购买意向和决策阶段\n4. 提取关键异议和顾虑点\n5. 给出下一步跟进建议\n\n销售对话/沟通记录：\n{content}\n\n请直接输出分析报告。",
        "concise": "你是一位高效的销售分析助手。请简要分析以下对话记录。\n\n要点：客户需求、机会等级、关键异议、行动建议。\n\n对话记录：\n{content}",
        "detailed": "你是一位细致的分析专家。请从客户画像、需求挖掘、决策链、竞争态势、跟进计划等维度深度分析以下对话。\n\n对话记录：\n{content}",
        "creative": "你是一位有洞察力的销售顾问。请用生动的方式分析以下对话。\n\n对话记录：\n{content}",
    }
}

REPORT_TYPE_NAMES = {"zh": {"analysis": "销售分析", "followup": "跟进", "opportunity": "商机"}}


# ============ 认证辅助 ============
async def _get_current_user(request: Request, db: Session):
    auth = request.headers.get("Authorization", "")
    if not auth.startswith("Bearer "):
        return None
    payload = decode_access_token(auth[7:])
    if not payload:
        return None
    user = db.query(User).filter(User.id == int(payload.get("sub", 0))).first()
    return user if user and user.is_active else None


# ============ 周报生成 API ============
@router.post("/generate")
async def generate_report(request: Request, req: dict, db: Session = Depends(get_db)):
    user = await _get_current_user(request, db)
    if not user:
        raise HTTPException(401, "未登录")

    content = req.get("content", "")
    style = req.get("style", "professional")
    report_type = req.get("report_type", "weekly")
    language = req.get("language", "zh")
    ai_model = req.get("ai_model", "deepseek")
    custom_prompt = req.get("custom_prompt")

    lang_prompts = PROMPTS.get(language, PROMPTS["zh"])
    template = lang_prompts.get(style, lang_prompts["professional"])
    report_type_name = REPORT_TYPE_NAMES.get(language, REPORT_TYPE_NAMES["zh"]).get(report_type, "周报")

    if custom_prompt:
        prompt = custom_prompt.format(content=content, report_type=report_type_name)
    else:
        prompt = template.format(content=content, report_type=report_type_name)

    ai_config = AI_CONFIGS.get(ai_model, AI_CONFIGS["deepseek"])

    if not ai_config["api_key"]:
        report_text = _generate_mock_report(content, report_type_name)
    else:
        try:
            report_text = await _call_ai_api(prompt, ai_config)
        except Exception as e:
            raise HTTPException(500, f"AI 生成失败：{e}")

    report = Report(
        user_id=user.id,
        content=content,
        report=report_text,
        style=style,
        report_type=report_type,
        ai_model=ai_model,
    )
    db.add(report)
    db.add(AccessLog(user_id=user.id, action="generate"))
    db.commit()

    return {"report": report_text, "model": ai_model, "style": style}


# ============ 历史记录 API ============
@router.get("/history")
async def get_history(request: Request, db: Session = Depends(get_db)):
    user = await _get_current_user(request, db)
    if not user:
        raise HTTPException(401, "未登录")

    reports = (
        db.query(Report)
        .filter(Report.user_id == user.id)
        .order_by(Report.created_at.desc())
        .limit(50)
        .all()
    )
    return {
        "history": [
            {
                "id": r.id,
                "content": r.content[:100] + ("..." if len(r.content) > 100 else ""),
                "report": r.report,
                "style": r.style,
                "type": r.report_type,
                "model": r.ai_model,
                "created_at": r.created_at.isoformat(),
            }
            for r in reports
        ]
    }


@router.delete("/history/{item_id}")
async def delete_history(item_id: int, request: Request, db: Session = Depends(get_db)):
    user = await _get_current_user(request, db)
    if not user:
        raise HTTPException(401, "未登录")

    report = db.query(Report).filter(Report.id == item_id, Report.user_id == user.id).first()
    if not report:
        raise HTTPException(404, "记录不存在")
    db.delete(report)
    db.commit()
    return {"status": "ok"}


# ============ 工具函数 ============
async def _call_ai_api(prompt: str, model_config: dict) -> str:
    async with httpx.AsyncClient(timeout=60.0) as client:
        resp = await client.post(
            f"{model_config['base_url']}/chat/completions",
            headers={
                "Authorization": f"Bearer {model_config['api_key']}",
                "Content-Type": "application/json",
            },
            json={
                "model": model_config["model"],
                "messages": [
                    {"role": "system", "content": "你是一位专业的职场写作助手。"},
                    {"role": "user", "content": prompt},
                ],
                "temperature": 0.7,
                "max_tokens": 2000,
            },
        )
        if resp.status_code != 200:
            raise Exception(f"AI API 错误：{resp.text}")
        return resp.json()["choices"][0]["message"]["content"]


def _generate_mock_report(content: str, report_type_name: str) -> str:
    return f"""# {report_type_name}分析报告

## 一、客户需求分析
- 客户表达了明确的产品需求
- 关注点：性价比、售后服务、交付周期

## 二、销售机会评估
**机会等级：中高**
- 需求匹配度：85%
- 预算充足度：良好

## 三、客户异议及顾虑
- 对价格有一定顾虑
- 担心交付时间

## 四、下一步跟进建议
1. 3 天内发送详细报价方案
2. 1 周内安排产品演示
3. 跟进决策进度

---
*此分析由 智析 AI 生成*"""
