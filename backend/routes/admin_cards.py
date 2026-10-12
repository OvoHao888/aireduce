from fastapi import APIRouter, Depends, HTTPException, Header
from pydantic import BaseModel
from sqlalchemy.orm import Session
from sqlalchemy import text
from database import get_db
from jose import jwt, JWTError
from datetime import datetime, timedelta
import logging
import os
import random
import string
from typing import Optional

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/api/admin/cards", tags=["admin-cards"])

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
def get_cards(page: int = 1, limit: int = 10, db: Session = Depends(get_db), admin_payload: dict = Depends(verify_admin_token)):
    offset = (page - 1) * limit
    cards = db.execute(
        text("SELECT c.id, c.card_code, c.token_type, c.duration_hours, c.duration_days, c.status, c.user_id, u.username, c.used_at, c.card_expire_date, c.created_at FROM token_cards c LEFT JOIN users u ON c.user_id = u.id ORDER BY c.id DESC LIMIT :limit OFFSET :offset"),
        {"limit": limit, "offset": offset}
    ).fetchall()
    total = db.execute(text("SELECT COUNT(*) FROM token_cards")).fetchone()[0]
    
    def safe_iso(val):
        if val is None:
            return None
        if hasattr(val, 'isoformat'):
            return val.isoformat()
        return str(val)
    
    return {
        "items": [
            {
                "id": c[0], 
                "card_code": c[1], 
                "token_type": c[2], 
                "duration_hours": c[3], 
                "duration_days": c[4],
                "status": c[5], 
                "used_by": c[7] if c[7] else str(c[6]),
                "used_at": safe_iso(c[8]), 
                "expire_date": safe_iso(c[9]), 
                "created_at": safe_iso(c[10])
            } for c in cards
        ],
        "total": total, "page": page, "limit": limit
    }

@router.post("")
def create_card(card_data: dict, db: Session = Depends(get_db), admin_payload: dict = Depends(verify_admin_token)):
    token_type = card_data.get("token_type")
    quantity = card_data.get("quantity", 1)
    duration_days = card_data.get("duration_days")
    duration_hours = card_data.get("duration_hours")
    expire_days = card_data.get("expire_days", 30)
    
    product = db.execute(text("SELECT duration_days, duration_hours FROM token_products WHERE token_type=:token_type"), {"token_type": token_type}).fetchone()
    if product:
        duration_days = duration_days or product[0]
        duration_hours = duration_hours or product[1]
    
    cards = []
    for _ in range(quantity):
        code = ''.join(random.choices(string.ascii_letters + string.digits, k=16))
        expire_date = datetime.now() + timedelta(days=expire_days)
        db.execute(text("INSERT INTO token_cards (card_code, token_type, duration_days, duration_hours, card_expire_date, created_at) VALUES (:code, :token_type, :duration_days, :duration_hours, :expire_date, NOW())"),
            {"code": code, "token_type": token_type, "duration_days": duration_days, "duration_hours": duration_hours, "expire_date": expire_date})
        cards.append(code)
    db.commit()
    logger.info(f"生成{quantity}个卡密: {token_type}")
    return {"message": f"成功生成{quantity}个卡密", "cards": cards}

@router.get("/{card_id}")
def get_card(card_id: int, db: Session = Depends(get_db), admin_payload: dict = Depends(verify_admin_token)):
    card = db.execute(text("SELECT id, card_code, token_type, duration_hours, duration_days, status, user_id, used_at, card_expire_date, created_at FROM token_cards WHERE id=:id"), {"id": card_id}).fetchone()
    if not card:
        raise HTTPException(status_code=404, detail="卡密不存在")
    return {"id": card[0], "card_code": card[1], "token_type": card[2], "duration_hours": card[3], "duration_days": card[4], "status": card[5], "user_id": card[6]}

@router.put("/{card_id}")
def update_card(card_id: int, card_data: dict, db: Session = Depends(get_db), admin_payload: dict = Depends(verify_admin_token)):
    status = card_data.get("status")
    if status:
        db.execute(text("UPDATE token_cards SET status=:status WHERE id=:id"), {"status": status, "id": card_id})
        db.commit()
    return {"message": "更新成功"}

@router.delete("/{card_id}")
def delete_card(card_id: int, db: Session = Depends(get_db), admin_payload: dict = Depends(verify_admin_token)):
    db.execute(text("DELETE FROM token_cards WHERE id=:id"), {"id": card_id})
    db.commit()
    return {"message": "删除成功"}