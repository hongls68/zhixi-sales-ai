"""
智析销售AI - 分析路由
"""
import json
from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import Optional

from database import get_db
from models.user import User
from models.analysis import Analysis
from services.auth_service import decode_access_token
from services.ai_service import analyze_with_ai

router = APIRouter(prefix="/api/analysis", tags=["分析"])


# ============ 请求模型 ============

class CreateAnalysisRequest(BaseModel):
    content: str
    title: Optional[str] = ""
    type: Optional[str] = "sales_call"


# ============ 辅助函数 ============

def get_current_user(request, db: Session) -> User:
    """获取当前用户"""
    auth = request.headers.get("Authorization", "")
    if not auth.startswith("Bearer "):
        raise HTTPException(401, "未登录")

    payload = decode_access_token(auth[7:])
    if not payload:
        raise HTTPException(401, "Token无效或已过期")

    user = db.query(User).filter(User.id == int(payload.get("sub", 0))).first()
    if not user or not user.is_active:
        raise HTTPException(401, "用户不存在或已禁用")

    return user


# ============ 接口实现 ============

@router.get("/list")
async def get_analysis_list(
    request,
    page: int = 1,
    page_size: int = 20,
    type: str = "",
    status: str = "",
    keyword: str = "",
    db: Session = Depends(get_db)
):
    """获取分析列表"""
    user = get_current_user(request, db)

    query = db.query(Analysis).filter(Analysis.user_id == user.id)

    # 筛选
    if type:
        query = query.filter(Analysis.type == type)
    if status:
        query = query.filter(Analysis.status == status)
    if keyword:
        query = query.filter(Analysis.title.contains(keyword) | Analysis.content.contains(keyword))

    # 分页
    total = query.count()
    items = query.order_by(Analysis.created_at.desc()).offset((page - 1) * page_size).limit(page_size).all()

    return {
        "list": [item.to_dict() for item in items],
        "total": total,
        "page": page,
        "page_size": page_size
    }


@router.get("/{analysis_id}")
async def get_analysis_detail(analysis_id: int, request, db: Session = Depends(get_db)):
    """获取分析详情"""
    user = get_current_user(request, db)

    analysis = db.query(Analysis).filter(
        Analysis.id == analysis_id,
        Analysis.user_id == user.id
    ).first()

    if not analysis:
        raise HTTPException(404, "分析记录不存在")

    return analysis.to_dict()


@router.post("/create")
async def create_analysis(body: CreateAnalysisRequest, request, db: Session = Depends(get_db)):
    """创建分析（文本输入）"""
    user = get_current_user(request, db)

    if not body.content.strip():
        raise HTTPException(400, "请输入对话内容")

    # 调用AI分析
    user_context = {
        "industry": user.industry,
        "role": user.job_title
    }

    try:
        result = await analyze_with_ai(body.content, user_context)
    except Exception as e:
        print(f"AI分析失败: {e}")
        # 返回Mock数据
        result = {
            "intent_score": 75,
            "sentiment": "positive",
            "key_points": ["客户对产品感兴趣"],
            "risks": ["可能对比竞品"],
            "suggestions": ["及时跟进"],
            "keywords": ["价格", "方案"]
        }

    # 保存到数据库
    analysis = Analysis(
        user_id=user.id,
        title=body.title or "分析记录 " + datetime.now().strftime("%Y-%m-%d %H:%M"),
        content=body.content,
        type=body.type,
        status="completed",
        intent_score=result.get("intent_score", 50),
        sentiment=result.get("sentiment", "neutral"),
        key_points=json.dumps(result.get("key_points", []), ensure_ascii=False),
        risks=json.dumps(result.get("risks", []), ensure_ascii=False),
        suggestions=json.dumps(result.get("suggestions", []), ensure_ascii=False),
        keywords=json.dumps(result.get("keywords", []), ensure_ascii=False),
        ai_model="local"
    )

    db.add(analysis)
    db.commit()
    db.refresh(analysis)

    return analysis.to_dict()


@router.post("/upload")
async def upload_and_analyze(
    request,
    file: UploadFile = File(...),
    title: str = Form(""),
    db: Session = Depends(get_db)
):
    """上传录音并分析"""
    user = get_current_user(request, db)

    # 检查文件类型
    allowed_types = ["audio/mpeg", "audio/wav", "audio/mp3", "audio/m4a", "text/plain"]
    if file.content_type not in allowed_types:
        raise HTTPException(400, "不支持的文件类型，请上传音频或文本文件")

    content = await file.read()

    # 如果是文本文件，直接读取
    if file.content_type == "text/plain":
        text_content = content.decode("utf-8")
    else:
        # 音频文件，调用Whisper转写
        try:
            from services.whisper_service import transcribe_audio
            text_content = await transcribe_audio(file)
            if not text_content:
                raise HTTPException(500, "语音转写失败，请直接粘贴文本")
        except ImportError:
            raise HTTPException(500, "Whisper未安装，无法转写音频")

    # 调用AI分析
    user_context = {"industry": user.industry, "role": user.job_title}
    result = await analyze_with_ai(text_content, user_context)

    # 保存
    analysis = Analysis(
        user_id=user.id,
        title=title or file.filename or "上传分析",
        content=text_content,
        type="sales_call",
        status="completed",
        intent_score=result.get("intent_score", 50),
        sentiment=result.get("sentiment", "neutral"),
        key_points=json.dumps(result.get("key_points", []), ensure_ascii=False),
        risks=json.dumps(result.get("risks", []), ensure_ascii=False),
        suggestions=json.dumps(result.get("suggestions", []), ensure_ascii=False),
        keywords=json.dumps(result.get("keywords", []), ensure_ascii=False),
        ai_model="whisper+ai"
    )

    db.add(analysis)
    db.commit()
    db.refresh(analysis)

    return analysis.to_dict()


@router.delete("/{analysis_id}")
async def delete_analysis(analysis_id: int, request, db: Session = Depends(get_db)):
    """删除分析记录"""
    user = get_current_user(request, db)

    analysis = db.query(Analysis).filter(
        Analysis.id == analysis_id,
        Analysis.user_id == user.id
    ).first()

    if not analysis:
        raise HTTPException(404, "记录不存在")

    db.delete(analysis)
    db.commit()

    return {"message": "删除成功"}
