from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from database import get_db
from models import User, Feedback
from schemas import FeedbackRequest, FeedbackResponse
from auth import get_current_user
import logging

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/api/feedbacks", tags=["feedbacks"])

@router.post("", response_model=FeedbackResponse, status_code=201)
def create_feedback(
    request: FeedbackRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    try:
        if not request.content or len(request.content.strip()) < 5:
            raise HTTPException(status_code=400, detail="反馈内容不能少于5个字符")
        
        if len(request.content) > 2000:
            raise HTTPException(status_code=400, detail="反馈内容不能超过2000个字符")
        
        if request.type not in ["suggestion", "bug", "complaint", "other"]:
            raise HTTPException(status_code=400, detail="无效的反馈类型")
        
        feedback = Feedback(
            user_id=current_user.id,
            content=request.content.strip(),
            contact=request.contact.strip() if request.contact else None,
            type=request.type,
            status="pending"
        )
        
        db.add(feedback)
        db.commit()
        db.refresh(feedback)
        
        logger.info(f"用户 {current_user.email} 提交反馈成功")
        
        return feedback
    except HTTPException:
        raise
    except SQLAlchemyError as e:
        db.rollback()
        logger.error(f"数据库错误 - 提交反馈失败: {str(e)}")
        raise HTTPException(status_code=500, detail="提交反馈失败")
    except Exception as e:
        db.rollback()
        logger.error(f"提交反馈失败: {str(e)}")
        raise HTTPException(status_code=500, detail="提交反馈失败")

from typing import List

@router.get("", response_model=List[FeedbackResponse])
def get_feedbacks(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    try:
        feedbacks = db.query(Feedback)\
            .filter(Feedback.user_id == current_user.id)\
            .order_by(Feedback.created_at.desc())\
            .all()
        
        return feedbacks
    except SQLAlchemyError as e:
        logger.error(f"数据库错误 - 获取反馈列表失败: {str(e)}")
        raise HTTPException(status_code=500, detail="获取反馈列表失败")
    except Exception as e:
        logger.error(f"获取反馈列表失败: {str(e)}")
        raise HTTPException(status_code=500, detail="获取反馈列表失败")

@router.get("/{feedback_id}", response_model=FeedbackResponse)
def get_feedback(
    feedback_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    try:
        if feedback_id < 1:
            raise HTTPException(status_code=400, detail="无效的反馈ID")
        
        feedback = db.query(Feedback).filter(
            Feedback.id == feedback_id,
            Feedback.user_id == current_user.id
        ).first()
        
        if not feedback:
            logger.warning(f"反馈不存在: {feedback_id}")
            raise HTTPException(status_code=404, detail="反馈不存在")
        
        return feedback
    except HTTPException:
        raise
    except SQLAlchemyError as e:
        logger.error(f"数据库错误 - 获取反馈详情失败: {str(e)}")
        raise HTTPException(status_code=500, detail="获取反馈详情失败")
    except Exception as e:
        logger.error(f"获取反馈详情失败: {str(e)}")
        raise HTTPException(status_code=500, detail="获取反馈详情失败")