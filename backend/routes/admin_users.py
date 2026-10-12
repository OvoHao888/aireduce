from fastapi import APIRouter, Depends, HTTPException, Header
from pydantic import BaseModel
from sqlalchemy.orm import Session
from sqlalchemy import text
from database import get_db
from jose import jwt, JWTError
from datetime import datetime
import logging
import os
from typing import Optional

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/api/admin/users", tags=["admin-users"])

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM", "HS256")

# ==================== 验证管理员token ====================
def verify_admin_token(authorization: Optional[str] = Header(None)):
    if not authorization:
        raise HTTPException(status_code=401, detail="未提供认证令牌", headers={"WWW-Authenticate": "Bearer"})
    if not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="无效的认证格式", headers={"WWW-Authenticate": "Bearer"})
    token = authorization.replace("Bearer ", "")
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        if not payload.get("is_admin"):
            raise HTTPException(status_code=403, detail="需要管理员权限")
        return payload
    except JWTError:
        raise HTTPException(status_code=401, detail="无效的令牌", headers={"WWW-Authenticate": "Bearer"})

# ==================== 获取用户列表 ====================
@router.get("")
def get_users(page: int = 1, limit: int = 10, db: Session = Depends(get_db), admin_payload: dict = Depends(verify_admin_token)):
    offset = (page - 1) * limit
    users = db.execute(
        text("SELECT id, username, email, expire_date, total_usage, created_at FROM users ORDER BY id DESC LIMIT :limit OFFSET :offset"),
        {"limit": limit, "offset": offset}
    ).fetchall()
    total = db.execute(text("SELECT COUNT(*) FROM users")).fetchone()[0]
    return {
        "items": [
            {
                "id": u[0], "username": u[1], "email": u[2],
                "expire_date": u[3].isoformat() if u[3] else None,
                "total_usage": u[4], "created_at": u[5].isoformat() if u[5] else None,
                "is_vip": str(u[3]) > str(datetime.now()) if u[3] else False
            }
            for u in users
        ],
        "total": total, "page": page, "limit": limit
    }

# ==================== 获取单个用户 ====================
@router.get("/{user_id}")
def get_user(user_id: int, db: Session = Depends(get_db), admin_payload: dict = Depends(verify_admin_token)):
    result = db.execute(
        text("SELECT id, username, email, expire_date, total_usage, created_at FROM users WHERE id=:id"),
        {"id": user_id}
    ).fetchone()
    if not result:
        raise HTTPException(status_code=404, detail="用户不存在")
    return {
        "id": result[0], "username": result[1], "email": result[2],
        "expire_date": result[3].isoformat() if result[3] else None,
        "total_usage": result[4], "created_at": result[5].isoformat() if result[5] else None
    }

# ==================== 更新用户信息 ====================
@router.put("/{user_id}")
def update_user(user_id: int, user_data: dict, db: Session = Depends(get_db), admin_payload: dict = Depends(verify_admin_token)):
    exists = db.execute(text("SELECT id FROM users WHERE id=:id"), {"id": user_id}).fetchone()
    if not exists:
        raise HTTPException(status_code=404, detail="用户不存在")
    
    fields = []
    values = {}
    if "expire_date" in user_data:
        fields.append("expire_date=:expire_date")
        values["expire_date"] = user_data["expire_date"]
    if "total_usage" in user_data:
        fields.append("total_usage=:total_usage")
        values["total_usage"] = user_data["total_usage"]
    
    values["id"] = user_id
    if fields:
        sql = f"UPDATE users SET {', '.join(fields)} WHERE id=:id"
        db.execute(text(sql), values)
        db.commit()
    
    logger.info(f"更新用户: {user_id}")
    return {"message": "更新成功"}

# ==================== 删除用户 ====================
@router.delete("/{user_id}")
def delete_user(user_id: int, db: Session = Depends(get_db), admin_payload: dict = Depends(verify_admin_token)):
    result = db.execute(text("DELETE FROM users WHERE id=:id"), {"id": user_id})
    db.commit()
    if result.rowcount == 0:
        raise HTTPException(status_code=404, detail="用户不存在")
    logger.info(f"删除用户: {user_id}")
    return {"message": "删除成功"}

# ==================== 更新会员状态 ====================
@router.put("/{user_id}/status")
def update_user_status(user_id: int, status_data: dict, db: Session = Depends(get_db), admin_payload: dict = Depends(verify_admin_token)):
    new_expire = status_data.get("expire_date")
    if new_expire:
        db.execute(text("UPDATE users SET expire_date=:expire_date WHERE id=:id"), {"expire_date": new_expire, "id": user_id})
    else:
        db.execute(text("UPDATE users SET expire_date=NULL WHERE id=:id"), {"id": user_id})
    db.commit()
    logger.info(f"更新用户状态: {user_id}")
    return {"message": "状态更新成功"}