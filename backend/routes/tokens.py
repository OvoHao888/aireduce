from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from database import get_db
from models import User, TokenCard, TokenProduct
from schemas import CardExchange, CardExchangeResponse, ProductResponse
from typing import List
from auth import get_current_user, get_member_level
from datetime import datetime, timedelta
import logging

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/api/tokens", tags=["tokens"])

@router.get("/products", response_model=List[ProductResponse])
def get_products(db: Session = Depends(get_db)):
    try:
        # 只返回上架中的套餐：此前管理员在后台下架后，用户端仍能看到并可购买
        products = (
            db.query(TokenProduct)
            .filter(TokenProduct.is_active.is_(True))
            .order_by(TokenProduct.sort_order)
            .all()
        )
        return products
    except SQLAlchemyError as e:
        logger.error(f"数据库错误 - 获取产品列表失败: {str(e)}")
        raise HTTPException(status_code=500, detail="获取产品列表失败")
    except Exception as e:
        logger.error(f"获取产品列表失败: {str(e)}")
        raise HTTPException(status_code=500, detail="获取产品列表失败")

@router.post("/exchange", response_model=CardExchangeResponse)
def exchange_card(
    card_data: CardExchange,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    try:
        if not card_data.card_code or len(card_data.card_code) < 8 or len(card_data.card_code) > 20:
            raise HTTPException(status_code=400, detail="卡密格式不正确（长度应在8-20位之间）")
        
        # 对命中行加排他锁：并发兑换同一张卡时，后一个事务会阻塞到前一个提交后再读，
        # 从而看到 status='used' 并被拒绝。原实现"先查再改"没有任何锁或原子条件，
        # 两个请求可同时通过校验，同一张卡被重复兑换、会员时长翻倍。
        card = (
            db.query(TokenCard)
            .filter(TokenCard.card_code == card_data.card_code)
            .with_for_update()
            .first()
        )
        
        if not card:
            logger.warning(f"卡密不存在: {card_data.card_code}")
            raise HTTPException(status_code=400, detail="卡密不存在")
        
        if card.status == "used":
            logger.warning(f"卡密已被使用: {card_data.card_code}")
            raise HTTPException(status_code=400, detail="卡密已被使用")
        
        if card.status == "expired":
            logger.warning(f"卡密已过期: {card_data.card_code}")
            raise HTTPException(status_code=400, detail="卡密已过期")
        
        if card.card_expire_date < datetime.now():
            card.status = "expired"
            db.commit()
            logger.warning(f"卡密已过期: {card_data.card_code}")
            raise HTTPException(status_code=400, detail="卡密已过期")
        
        now = datetime.now()
        if current_user.expire_date and current_user.expire_date > now:
            new_expire_date = current_user.expire_date
        else:
            new_expire_date = now
        
        if card.duration_hours:
            new_expire_date += timedelta(hours=card.duration_hours)
        if card.duration_days:
            new_expire_date += timedelta(days=card.duration_days)
        
        card.status = "used"
        card.user_id = current_user.id
        card.used_at = now
        
        current_user.expire_date = new_expire_date
        
        db.commit()
        
        logger.info(f"用户 {current_user.email} 兑换卡密成功: {card_data.card_code}")
        
        return {
            "success": True,
            "message": "兑换成功",
            "token_type": card.token_type,
            "duration_days": card.duration_days,
            "duration_hours": card.duration_hours,
            "new_expire_date": new_expire_date
        }
    except HTTPException:
        raise
    except SQLAlchemyError as e:
        db.rollback()
        logger.error(f"数据库错误 - 兑换卡密失败: {str(e)}")
        raise HTTPException(status_code=500, detail="数据库操作失败，请稍后重试")
    except Exception as e:
        db.rollback()
        logger.error(f"兑换卡密失败: {str(e)}")
        raise HTTPException(status_code=500, detail="兑换失败，请稍后重试")

@router.get("/my-status")
def get_member_status(current_user: User = Depends(get_current_user)):
    try:
        now = datetime.now()
        is_member = current_user.expire_date is not None and current_user.expire_date > now
        remaining_days = None
        
        if is_member:
            remaining_days = max(0, (current_user.expire_date - now).days)
        
        return {
            "is_member": is_member,
            "expire_date": current_user.expire_date,
            "remaining_days": remaining_days,
            "member_level": get_member_level(current_user),
            "total_usage": current_user.total_usage
        }
    except Exception as e:
        logger.error(f"获取会员状态失败: {str(e)}")
        raise HTTPException(status_code=500, detail="获取会员状态失败")