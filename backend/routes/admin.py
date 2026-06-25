"""
智析 AI - 管理员路由
"""
from datetime import datetime, timedelta
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func

import models
from database import get_db
from deps import require_admin

router = APIRouter(prefix="/api/admin", tags=["管理员"])


@router.get("/stats")
async def admin_stats(admin: models.User = Depends(require_admin), db: Session = Depends(get_db)):
    """管理后台统计数据"""
    today = datetime.utcnow().replace(hour=0, minute=0, second=0, microsecond=0)
    week_ago = today - timedelta(days=7)

    dau = db.query(func.count(func.distinct(models.AccessLog.user_id))).filter(
        models.AccessLog.action == "login", models.AccessLog.created_at >= today
    ).scalar() or 0

    wau = db.query(func.count(func.distinct(models.AccessLog.user_id))).filter(
        models.AccessLog.action == "login", models.AccessLog.created_at >= week_ago
    ).scalar() or 0

    total_users = db.query(func.count(models.User.id)).scalar() or 0
    today_users = db.query(func.count(models.User.id)).filter(models.User.created_at >= today).scalar() or 0
    total_reports = db.query(func.count(models.Report.id)).scalar() or 0
    today_reports = db.query(func.count(models.Report.id)).filter(models.Report.created_at >= today).scalar() or 0

    daily_regs = []
    for i in range(7):
        day = today - timedelta(days=6 - i)
        next_day = day + timedelta(days=1)
        count = db.query(func.count(models.User.id)).filter(
            models.User.created_at >= day, models.User.created_at < next_day
        ).scalar() or 0
        daily_regs.append({"date": day.strftime("%m-%d"), "count": count})

    daily_active = []
    for i in range(7):
        day = today - timedelta(days=6 - i)
        next_day = day + timedelta(days=1)
        count = db.query(func.count(func.distinct(models.AccessLog.user_id))).filter(
            models.AccessLog.action == "login",
            models.AccessLog.created_at >= day,
            models.AccessLog.created_at < next_day,
        ).scalar() or 0
        daily_active.append({"date": day.strftime("%m-%d"), "count": count})

    model_stats = db.query(models.Report.ai_model, func.count(models.Report.id)).group_by(models.Report.ai_model).all()
    model_usage = [{"model": m or "unknown", "count": c} for m, c in model_stats]

    return {
        "dau": dau, "wau": wau,
        "total_users": total_users, "today_users": today_users,
        "total_reports": total_reports, "today_reports": today_reports,
        "daily_regs": daily_regs, "daily_active": daily_active,
        "model_usage": model_usage,
    }


@router.get("/users")
async def admin_users(
    page: int = 1, search: str = "",
    admin: models.User = Depends(require_admin),
    db: Session = Depends(get_db),
):
    """用户列表（分页 + 搜索）"""
    query = db.query(models.User)
    if search:
        query = query.filter(models.User.username.contains(search) | models.User.email.contains(search))
    total = query.count()
    users = query.order_by(models.User.created_at.desc()).offset((page - 1) * 20).limit(20).all()
    return {
        "total": total, "page": page, "pages": (total + 19) // 20,
        "users": [
            {
                "id": u.id, "username": u.username, "email": u.email,
                "role": u.role, "is_active": u.is_active,
                "created_at": u.created_at.isoformat() if u.created_at else None,
                "last_login": u.last_login.isoformat() if u.last_login else None,
            }
            for u in users
        ],
    }


@router.put("/users/{user_id}")
async def admin_update_user(
    user_id: int, body: dict,
    admin: models.User = Depends(require_admin),
    db: Session = Depends(get_db),
):
    """更新用户信息"""
    target = db.query(models.User).filter(models.User.id == user_id).first()
    if not target:
        raise HTTPException(404, "用户不存在")
    if "role" in body:
        target.role = body["role"]
    if "is_active" in body:
        target.is_active = body["is_active"]
    db.commit()
    return {"status": "ok"}


@router.delete("/users/{user_id}")
async def admin_delete_user(
    user_id: int,
    admin: models.User = Depends(require_admin),
    db: Session = Depends(get_db),
):
    """删除用户"""
    target = db.query(models.User).filter(models.User.id == user_id).first()
    if not target:
        raise HTTPException(404, "用户不存在")
    if target.id == admin.id:
        raise HTTPException(400, "不能删除自己")
    db.delete(target)
    db.commit()
    return {"status": "ok"}


@router.get("/reports")
async def admin_reports(
    page: int = 1,
    admin: models.User = Depends(require_admin),
    db: Session = Depends(get_db),
):
    """报告列表"""
    total = db.query(models.Report).count()
    reports = db.query(models.Report).order_by(models.Report.created_at.desc()).offset((page - 1) * 20).limit(20).all()
    result = []
    for r in reports:
        u = db.query(models.User).filter(models.User.id == r.user_id).first()
        result.append({
            "id": r.id, "user_id": r.user_id,
            "username": u.username if u else "deleted",
            "content": r.content[:80], "style": r.style, "type": r.report_type,
            "model": r.ai_model, "created_at": r.created_at.isoformat(),
        })
    return {"total": total, "page": page, "pages": (total + 19) // 20, "reports": result}
