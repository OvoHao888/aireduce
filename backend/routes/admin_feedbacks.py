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
router = APIRouter(prefix="/api/admin/feedbacks", tags=["admin-feedbacks"])

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM", "HS256")

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

@router.get("")
def get_feedbacks(page: int = 1, limit: int = 10, db: Session = Depends(get_db), admin_payload: dict = Depends(verify_admin_token)):
    offset = (page - 1) * limit
    feedbacks = db.execute(
        text("SELECT f.id, f.user_id, u.username, f.content, f.reply, f.created_at FROM feedbacks f LEFT JOIN users u ON f.user_id = u.id ORDER BY f.id DESC LIMIT :limit OFFSET :offset"),
        {"limit": limit, "offset": offset}
    ).fetchall()
    total = db.execute(text("SELECT COUNT(*) FROM feedbacks")).fetchone()[0]
    return {
        "items": [{
            "id": f[0], "user_id": f[1], "username": f[2], "content": f[3], "reply": f[4],
            "created_at": f[5].isoformat() if f[5] else None
        } for f in feedbacks],
        "total": total, "page": page, "limit": limit
    }

@router.put("/{feedback_id}")
def reply_feedback(feedback_id: int, reply_data: dict, db: Session = Depends(get_db), admin_payload: dict = Depends(verify_admin_token)):
    reply = reply_data.get("reply")
    if reply:
        db.execute(text("UPDATE feedbacks SET reply=:reply WHERE id=:id"), {"reply": reply, "id": feedback_id})
        db.commit()
    return {"message": "回复成功"}

@router.delete("/{feedback_id}")
def delete_feedback(feedback_id: int, db: Session = Depends(get_db), admin_payload: dict = Depends(verify_admin_token)):
    db.execute(text("DELETE FROM feedbacks WHERE id=:id"), {"id": feedback_id})
    db.commit()
    return {"message": "删除成功"}