from fastapi import APIRouter, Depends, HTTPException, Header
from pydantic import BaseModel
from sqlalchemy.orm import Session
from sqlalchemy import text
from database import get_db
from jose import jwt, JWTError
import logging
import os
from typing import Optional

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/api/admin/records", tags=["admin-records"])

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
def get_records(page: int = 1, limit: int = 10, db: Session = Depends(get_db), admin_payload: dict = Depends(verify_admin_token)):
    offset = (page - 1) * limit
    records = db.execute(
        text("SELECT r.id, r.user_id, u.username, r.mode, r.input_text, r.output_text, r.status, r.error_message, r.created_at FROM usage_records r LEFT JOIN users u ON r.user_id = u.id ORDER BY r.id DESC LIMIT :limit OFFSET :offset"),
        {"limit": limit, "offset": offset}
    ).fetchall()
    total = db.execute(text("SELECT COUNT(*) FROM usage_records")).fetchone()[0]
    return {
        "items": [{
            "id": r[0], "user_id": r[1], "username": r[2], "mode": r[3], "input_text": r[4][:100] + "..." if r[4] and len(r[4]) > 100 else r[4],
            "output_text": r[5], "status": r[6], "error_message": r[7], "created_at": r[8].isoformat() if r[8] else None
        } for r in records],
        "total": total, "page": page, "limit": limit
    }

@router.delete("/{record_id}")
def delete_record(record_id: int, db: Session = Depends(get_db), admin_payload: dict = Depends(verify_admin_token)):
    db.execute(text("DELETE FROM usage_records WHERE id=:id"), {"id": record_id})
    db.commit()
    return {"message": "删除成功"}