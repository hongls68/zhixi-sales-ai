"""
智析销售AI - 管理员路由
"""
from datetime import datetime, timedelta
from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session
from sqlalchemy import func
from pydantic import BaseModel
from typing import Optional

from database import get_db
from models.user import User, AccessLog, OperationLog
from models.analysis import Analysis
from services.auth_service import decode_access_token

router = APIRouter(prefix="/api/admin", tags=["管理员"])


# ============ 辅助函数 ============

def get_admin_user(request: Request, db: Session) -> User:
    """获取管理员用户"""
    auth = request.headers.get("Authorization", "")
    if not auth.startswith("Bearer "):
        raise HTTPException(401, "未登录")

    payload = decode_access_token(auth[7:])
    if not payload:
        raise HTTPException(401, "Token无效")

    user = db.query(User).filter(User.id == int(payload.get("sub", 0))).first()
    if not user:
        raise HTTPException(401, "用户不存在")
    if user.role != "admin":
        raise HTTPException(403, "需要管理员权限")

    return user


# ============ 请求模型 ============

class UpdateUserRequest(BaseModel):
    nickname: Optional[str] = None
    role: Optional[str] = None
    is_active: Optional[bool] = None


# ============ 辅助：记录操作日志 ============

def log_operation(db: Session, admin: User, action: str, target_type: str, target_id: int, detail: str, ip: str = ""):
    """记录管理员操作"""
    log = OperationLog(
        admin_id=admin.id,
        admin_name=admin.nickname or admin.phone,
        action=action,
        target_type=target_type,
        target_id=target_id,
        detail=detail,
        ip_address=ip
    )
    db.add(log)
    db.commit()


# ============ 统计接口 ============

@router.get("/stats")
async def get_stats(request: Request, db: Session = Depends(get_db)):
    """获取统计数据"""
    admin = get_admin_user(request, db)

    today = datetime.utcnow().replace(hour=0, minute=0, second=0, microsecond=0)
    week_start = today - timedelta(days=today.weekday())

    # DAU - 今日活跃用户
    dau = db.query(func.count(func.distinct(AccessLog.user_id))).filter(
        AccessLog.created_at >= today
    ).scalar() or 0

    # WAU - 本周活跃用户
    wau = db.query(func.count(func.distinct(AccessLog.user_id))).filter(
        AccessLog.created_at >= week_start
    ).scalar() or 0

    # 总用户数
    total_users = db.query(func.count(User.id)).scalar() or 0

    # 今日新增用户
    today_users = db.query(func.count(User.id)).filter(
        User.created_at >= today
    ).scalar() or 0

    # 总分析次数
    total_analyses = db.query(func.count(Analysis.id)).scalar() or 0

    # 今日分析次数
    today_analyses = db.query(func.count(Analysis.id)).filter(
        Analysis.created_at >= today
    ).scalar() or 0

    # 7天用户增长趋势
    user_trend = []
    for i in range(6, -1, -1):
        day = today - timedelta(days=i)
        next_day = day + timedelta(days=1)
        count = db.query(func.count(User.id)).filter(
            User.created_at >= day,
            User.created_at < next_day
        ).scalar() or 0
        user_trend.append({"date": day.strftime("%m-%d"), "count": count})

    # 7天分析趋势
    analysis_trend = []
    for i in range(6, -1, -1):
        day = today - timedelta(days=i)
        next_day = day + timedelta(days=1)
        count = db.query(func.count(Analysis.id)).filter(
            Analysis.created_at >= day,
            Analysis.created_at < next_day
        ).scalar() or 0
        analysis_trend.append({"date": day.strftime("%m-%d"), "count": count})

    return {
        "dau": dau,
        "wau": wau,
        "total_users": total_users,
        "today_users": today_users,
        "total_analyses": total_analyses,
        "today_analyses": today_analyses,
        "user_trend": user_trend,
        "analysis_trend": analysis_trend
    }


# ============ 用户管理接口 ============

@router.get("/users")
async def get_users(
    request: Request,
    page: int = 1,
    page_size: int = 20,
    keyword: str = "",
    db: Session = Depends(get_db)
):
    """获取用户列表"""
    admin = get_admin_user(request, db)

    query = db.query(User)

    # 搜索
    if keyword:
        query = query.filter(
            User.phone.contains(keyword) |
            User.nickname.contains(keyword)
        )

    # 分页
    total = query.count()
    users = query.order_by(User.created_at.desc()).offset((page - 1) * page_size).limit(page_size).all()

    return {
        "list": [user.to_dict() for user in users],
        "total": total,
        "page": page,
        "page_size": page_size
    }


@router.get("/users/{user_id}")
async def get_user(user_id: int, request: Request, db: Session = Depends(get_db)):
    """获取用户详情"""
    admin = get_admin_user(request, db)

    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(404, "用户不存在")

    # 获取用户的分析数量
    analysis_count = db.query(func.count(Analysis.id)).filter(Analysis.user_id == user_id).scalar() or 0

    result = user.to_dict()
    result["analysis_count"] = analysis_count

    return result


@router.put("/users/{user_id}")
async def update_user(
    user_id: int,
    body: UpdateUserRequest,
    request: Request,
    db: Session = Depends(get_db)
):
    """更新用户"""
    admin = get_admin_user(request, db)

    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(404, "用户不存在")

    changes = []
    if body.nickname is not None and body.nickname != user.nickname:
        changes.append(f"昵称: {user.nickname} → {body.nickname}")
        user.nickname = body.nickname
    if body.role is not None and body.role != user.role:
        changes.append(f"角色: {user.role} → {body.role}")
        user.role = body.role
    if body.is_active is not None and body.is_active != user.is_active:
        changes.append(f"状态: {'启用' if user.is_active else '禁用'} → {'启用' if body.is_active else '禁用'}")
        user.is_active = body.is_active

    db.commit()
    db.refresh(user)

    # 记录操作日志
    if changes:
        log_operation(db, admin, "update_user", "user", user_id,
                      f"更新用户 {user.phone}: {'; '.join(changes)}",
                      request.client.host if request.client else "")

    return user.to_dict()


@router.put("/users/{user_id}/toggle-active")
async def toggle_user_active(user_id: int, request: Request, db: Session = Depends(get_db)):
    """切换用户启用/禁用状态"""
    admin = get_admin_user(request, db)

    if user_id == admin.id:
        raise HTTPException(400, "不能禁用自己")

    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(404, "用户不存在")

    user.is_active = not user.is_active
    db.commit()
    db.refresh(user)

    action = "enable_user" if user.is_active else "disable_user"
    detail = f"{'启用' if user.is_active else '禁用'}用户 {user.phone}"
    log_operation(db, admin, action, "user", user_id, detail,
                  request.client.host if request.client else "")

    return user.to_dict()


@router.delete("/users/{user_id}")
async def delete_user(user_id: int, request: Request, db: Session = Depends(get_db)):
    """删除用户"""
    admin = get_admin_user(request, db)

    # 不能删除自己
    if user_id == admin.id:
        raise HTTPException(400, "不能删除自己")

    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(404, "用户不存在")

    phone = user.phone

    # 删除用户的分析记录
    db.query(Analysis).filter(Analysis.user_id == user_id).delete()

    # 删除用户
    db.delete(user)
    db.commit()

    # 记录操作日志
    log_operation(db, admin, "delete_user", "user", user_id,
                  f"删除用户 {phone}",
                  request.client.host if request.client else "")

    return {"message": "删除成功"}


# ============ 分析记录管理 ============

@router.get("/analyses")
async def get_analyses(
    request: Request,
    page: int = 1,
    page_size: int = 20,
    keyword: str = "",
    db: Session = Depends(get_db)
):
    """获取分析记录列表"""
    admin = get_admin_user(request, db)

    query = db.query(Analysis)

    # 搜索
    if keyword:
        query = query.filter(
            Analysis.title.contains(keyword) |
            Analysis.content.contains(keyword)
        )

    # 分页
    total = query.count()
    analyses = query.order_by(Analysis.created_at.desc()).offset((page - 1) * page_size).limit(page_size).all()

    # 添加用户名
    result = []
    for analysis in analyses:
        user = db.query(User).filter(User.id == analysis.user_id).first()
        item = analysis.to_dict()
        item["user_phone"] = user.phone if user else "未知"
        item["user_nickname"] = user.nickname if user else "未知"
        result.append(item)

    return {
        "list": result,
        "total": total,
        "page": page,
        "page_size": page_size
    }


@router.delete("/analyses/{analysis_id}")
async def delete_analysis(analysis_id: int, request: Request, db: Session = Depends(get_db)):
    """删除分析记录"""
    admin = get_admin_user(request, db)

    analysis = db.query(Analysis).filter(Analysis.id == analysis_id).first()
    if not analysis:
        raise HTTPException(404, "分析记录不存在")

    title = analysis.title or f"分析#{analysis_id}"

    db.delete(analysis)
    db.commit()

    # 记录操作日志
    log_operation(db, admin, "delete_analysis", "analysis", analysis_id,
                  f"删除分析记录: {title}",
                  request.client.host if request.client else "")

    return {"message": "删除成功"}


# ============ 操作日志接口 ============

@router.get("/operation-logs")
async def get_operation_logs(
    request: Request,
    page: int = 1,
    page_size: int = 20,
    action: str = "",
    db: Session = Depends(get_db)
):
    """获取操作日志"""
    admin = get_admin_user(request, db)

    query = db.query(OperationLog)

    # 按操作类型筛选
    if action:
        query = query.filter(OperationLog.action == action)

    total = query.count()
    logs = query.order_by(OperationLog.created_at.desc()).offset((page - 1) * page_size).limit(page_size).all()

    return {
        "list": [log.to_dict() for log in logs],
        "total": total,
        "page": page,
        "page_size": page_size
    }
