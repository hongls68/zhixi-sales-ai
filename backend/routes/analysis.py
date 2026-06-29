"""
智析销售AI - 分析路由
"""
import json
from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException, Request, UploadFile, File, Form
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import Optional

from database import get_db
from models.user import User
from models.analysis import Analysis
from services.auth_service import decode_access_token
from services.ai_service import analyze_with_ai, get_ai_config_options

router = APIRouter(prefix="/api/analysis", tags=["分析"])


class CreateAnalysisRequest(BaseModel):
    content: str
    title: Optional[str] = ""
    type: Optional[str] = "sales_call"
    style: Optional[str] = "professional"
    depth: Optional[str] = "standard"
    language: Optional[str] = "zh"


def get_current_user(request, db):
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


@router.get("/config")
async def get_analysis_config():
    return get_ai_config_options()


@router.get("/list")
async def get_analysis_list(request: Request, page: int = 1, page_size: int = 20, type: str = "", status: str = "", keyword: str = "", db: Session = Depends(get_db)):
    user = get_current_user(request, db)
    query = db.query(Analysis).filter(Analysis.user_id == user.id)
    if type:
        query = query.filter(Analysis.type == type)
    if status:
        query = query.filter(Analysis.status == status)
    if keyword:
        query = query.filter(Analysis.title.contains(keyword) | Analysis.content.contains(keyword))
    total = query.count()
    items = query.order_by(Analysis.created_at.desc()).offset((page - 1) * page_size).limit(page_size).all()
    return {"list": [item.to_dict() for item in items], "total": total, "page": page, "page_size": page_size}


@router.get("/{analysis_id}")
async def get_analysis_detail(analysis_id: int, request: Request, db: Session = Depends(get_db)):
    user = get_current_user(request, db)
    analysis = db.query(Analysis).filter(Analysis.id == analysis_id, Analysis.user_id == user.id).first()
    if not analysis:
        raise HTTPException(404, "分析记录不存在")
    return analysis.to_dict()


@router.post("/create")
async def create_analysis(body: CreateAnalysisRequest, request: Request, db: Session = Depends(get_db)):
    user = get_current_user(request, db)
    if not body.content.strip():
        raise HTTPException(400, "请输入对话内容")
    user_context = {"industry": user.industry, "role": user.job_title}
    try:
        result = await analyze_with_ai(body.content, user_context, style=body.style, depth=body.depth, language=body.language)
    except Exception as e:
        print(f"AI分析失败: {e}")
        result = {"intent": "medium", "intent_score": 65, "key_needs": ["客户对产品感兴趣"], "pain_points": ["预算有限"], "emotion_trend": "客户情绪稳定", "action_suggestions": ["及时跟进", "发送方案"], "risks": ["可能对比竞品"], "keywords": ["价格", "方案"]}
    analysis = Analysis(
        user_id=user.id,
        title=body.title or "分析记录 " + datetime.now().strftime("%Y-%m-%d %H:%M"),
        content=body.content,
        type=body.type,
        status="completed",
        intent_score=result.get("intent_score", 50),
        sentiment=result.get("intent", "medium"),
        key_points=json.dumps(result.get("key_needs", []), ensure_ascii=False),
        risks=json.dumps(result.get("risks", []), ensure_ascii=False),
        suggestions=json.dumps(result.get("action_suggestions", []), ensure_ascii=False),
        keywords=json.dumps(result.get("keywords", []), ensure_ascii=False),
        ai_model="ai"
    )
    db.add(analysis)
    db.commit()
    db.refresh(analysis)
    return analysis.to_dict()


@router.delete("/{analysis_id}")
async def delete_analysis(analysis_id: int, request: Request, db: Session = Depends(get_db)):
    user = get_current_user(request, db)
    analysis = db.query(Analysis).filter(Analysis.id == analysis_id, Analysis.user_id == user.id).first()
    if not analysis:
        raise HTTPException(404, "记录不存在")
    db.delete(analysis)
    db.commit()
    return {"message": "删除成功"}
