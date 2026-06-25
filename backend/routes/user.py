"""
智析销售AI - 用户路由
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import Optional

from database import get_db
from models.user import User
from services.auth_service import decode_access_token

router = APIRouter(prefix="/api/user", tags=["用户"])


# ============ 请求模型 ============

class UpdateUserRequest(BaseModel):
    nickname: Optional[str] = None
    company: Optional[str] = None
    job_title: Optional[str] = None
    industry: Optional[str] = None


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

@router.get("/me")
async def get_user_info(request, db: Session = Depends(get_db)):
    """获取当前用户信息"""
    user = get_current_user(request, db)
    return user.to_dict()


@router.put("/update")
async def update_user_info(body: UpdateUserRequest, request, db: Session = Depends(get_db)):
    """更新用户信息"""
    user = get_current_user(request, db)

    if body.nickname is not None:
        user.nickname = body.nickname
    if body.company is not None:
        user.company = body.company
    if body.job_title is not None:
        user.job_title = body.job_title
    if body.industry is not None:
        user.industry = body.industry

    db.commit()
    db.refresh(user)

    return user.to_dict()


@router.get("/stats")
async def get_user_stats(request, db: Session = Depends(get_db)):
    """获取用户统计"""
    user = get_current_user(request, db)

    from models.analysis import Analysis
    from sqlalchemy import func
    from datetime import datetime, timedelta

    # 总分析次数
    total = db.query(func.count(Analysis.id)).filter(Analysis.user_id == user.id).scalar() or 0

    # 本月分析次数
    month_start = datetime.utcnow().replace(day=1, hour=0, minute=0, second=0, microsecond=0)
    month_count = db.query(func.count(Analysis.id)).filter(
        Analysis.user_id == user.id,
        Analysis.created_at >= month_start
    ).scalar() or 0

    # 平均评分
    avg_score = db.query(func.avg(Analysis.intent_score)).filter(
        Analysis.user_id == user.id,
        Analysis.status == "completed"
    ).scalar() or 0

    # 最近7天趋势
    trend = []
    for i in range(6, -1, -1):
        day = datetime.utcnow() - timedelta(days=i)
        day_start = day.replace(hour=0, minute=0, second=0, microsecond=0)
        day_end = day_start + timedelta(days=1)
        count = db.query(func.count(Analysis.id)).filter(
            Analysis.user_id == user.id,
            Analysis.created_at >= day_start,
            Analysis.created_at < day_end
        ).scalar() or 0
        trend.append({
            "date": day_start.strftime("%m-%d"),
            "count": count
        })

    return {
        "total_analyses": total,
        "month_analyses": month_count,
        "avg_score": round(avg_score, 1),
        "trend": trend
    }
