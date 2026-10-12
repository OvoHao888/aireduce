from fastapi import APIRouter, Depends, HTTPException, Header
from pydantic import BaseModel
from sqlalchemy.orm import Session
from sqlalchemy import text
from database import get_db
from jose import jwt, JWTError
from decimal import Decimal
import logging
import os
from typing import Optional

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/api/admin/products", tags=["admin-products"])

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
def get_products(page: int = 1, limit: int = 10, db: Session = Depends(get_db), admin_payload: dict = Depends(verify_admin_token)):
    offset = (page - 1) * limit
    products = db.execute(
        text("SELECT id, name, token_type, duration_hours, duration_days, price, original_price, description, is_active, sort_order FROM token_products ORDER BY sort_order, id LIMIT :limit OFFSET :offset"),
        {"limit": limit, "offset": offset}
    ).fetchall()
    total = db.execute(text("SELECT COUNT(*) FROM token_products")).fetchone()[0]

    def safe_iso(val):
        if val is None:
            return None
        if hasattr(val, 'isoformat'):
            return val.isoformat()
        return str(val)

    return {
        "items": [{
            "id": p[0], "name": p[1], "token_type": p[2], "duration_hours": p[3], "duration_days": p[4],
            "price": float(p[5]) if p[5] else None, "original_price": float(p[6]) if p[6] else None,
            "description": p[7], "is_active": p[8], "sort_order": p[9]
        } for p in products],
        "total": total, "page": page, "limit": limit
    }

@router.post("")
def create_product(product_data: dict, db: Session = Depends(get_db), admin_payload: dict = Depends(verify_admin_token)):
    name = product_data.get("name")
    token_type = product_data.get("token_type")
    duration_hours = product_data.get("duration_hours")
    duration_days = product_data.get("duration_days")
    price = product_data.get("price")
    original_price = product_data.get("original_price")
    description = product_data.get("description", "")
    is_active = product_data.get("is_active", True)
    sort_order = product_data.get("sort_order", 0)
    
    db.execute(text("INSERT INTO token_products (name, token_type, duration_hours, duration_days, price, original_price, description, is_active, sort_order) VALUES (:name, :token_type, :duration_hours, :duration_days, :price, :original_price, :description, :is_active, :sort_order)"),
        {"name": name, "token_type": token_type, "duration_hours": duration_hours, "duration_days": duration_days, "price": price, "original_price": original_price, "description": description, "is_active": is_active, "sort_order": sort_order})
    db.commit()
    logger.info(f"添加套餐: {name}")
    return {"message": "套餐添加成功"}

@router.put("/{product_id}")
def update_product(product_id: int, product_data: dict, db: Session = Depends(get_db), admin_payload: dict = Depends(verify_admin_token)):
    fields = []
    values = {}
    for key in ["name", "token_type", "duration_hours", "duration_days", "price", "original_price", "description", "is_active", "sort_order"]:
        if key in product_data:
            fields.append(f"{key}=:{key}")
            values[key] = product_data[key]
    
    values["id"] = product_id
    if fields:
        sql = f"UPDATE token_products SET {', '.join(fields)} WHERE id=:id"
        db.execute(text(sql), values)
        db.commit()
    return {"message": "更新成功"}

@router.delete("/{product_id}")
def delete_product(product_id: int, db: Session = Depends(get_db), admin_payload: dict = Depends(verify_admin_token)):
    db.execute(text("DELETE FROM token_products WHERE id=:id"), {"id": product_id})
    db.commit()
    return {"message": "删除成功"}