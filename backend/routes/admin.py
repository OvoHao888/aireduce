from fastapi import APIRouter, Depends, HTTPException, status, Header
from pydantic import BaseModel
from sqlalchemy.orm import Session
from sqlalchemy import text
from database import get_db
from auth import create_access_token, verify_password
from jose import jwt, JWTError
import logging
import os
from typing import Optional

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/api/admin", tags=["admin"])

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM", "HS256")

# ==================== 登录请求模型 ====================
class LoginRequest(BaseModel):
    username: str
    password: str

class LoginResponse(BaseModel):
    token: str
    user: dict

# ==================== 从Header获取token并验证 ====================
def verify_admin_token(authorization: Optional[str] = Header(None)):
    """验证管理员token"""
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
    except JWTError as e:
        logger.error(f"Token验证失败: {e}")
        raise HTTPException(status_code=401, detail="无效的令牌", headers={"WWW-Authenticate": "Bearer"})

# ==================== 管理员登录 ====================
@router.post("/login", response_model=LoginResponse)
def admin_login(login_data: LoginRequest, db: Session = Depends(get_db)):
    """管理员登录"""
    # 先按用户名取记录，再用 bcrypt 校验密码。
    # 原实现把明文口令直接放进 SQL 做等值比较，等价于要求口令明文入库，
    # 一旦 init.sql / 数据库泄露即可直登后台。
    row = db.execute(
        text("SELECT id, username, nickname, password FROM admin_users WHERE username=:username AND status=1"),
        {"username": login_data.username}
    ).fetchone()

    result = row if (row and verify_password(login_data.password, row[3])) else None

    if result:
        token = create_access_token(data={"sub": result[1], "is_admin": True})
        logger.info(f"管理员登录成功: {result[1]}")
        return {
            "token": token,
            "user": {
                "username": result[1],
                "nickname": result[2],
                "id": result[0]
            }
        }
    
    logger.warning(f"管理员登录失败: {login_data.username}")
    raise HTTPException(status_code=401, detail="用户名或密码错误")

# ==================== 统计概览 ====================
@router.get("/stats")
def get_stats(db: Session = Depends(get_db), admin_payload: dict = Depends(verify_admin_token)):
    """获取统计概览"""
    # 总用户数
    total_users = db.execute(text("SELECT COUNT(*) FROM users")).fetchone()[0]
    # VIP用户数
    vip_users = db.execute(text("SELECT COUNT(*) FROM users WHERE expire_date IS NOT NULL AND expire_date > NOW()")).fetchone()[0]
    # 总卡密数
    total_cards = db.execute(text("SELECT COUNT(*) FROM token_cards")).fetchone()[0]
    # 已使用卡密
    used_cards = db.execute(text("SELECT COUNT(*) FROM token_cards WHERE status='used'")).fetchone()[0]
    # 总使用次数
    total_uses = db.execute(text("SELECT COALESCE(SUM(total_usage), 0) FROM users")).fetchone()[0]
    # 反馈数量
    total_feedbacks = db.execute(text("SELECT COUNT(*) FROM feedbacks")).fetchone()[0]
    
    return {
        "total_users": total_users,
        "vip_users": vip_users,
        "total_cards": total_cards,
        "used_cards": used_cards,
        "total_uses": total_uses,
        "total_feedbacks": total_feedbacks
    }