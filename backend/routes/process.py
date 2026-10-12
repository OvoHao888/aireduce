# -*- coding: utf-8 -*-
"""
文本处理路由
"""

from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from typing import List
import json
import logging

from database import get_db, SessionLocal
from models import User, UsageRecord
from auth import get_current_user, is_valid_member
from schemas import ProcessRequest, UsageRecordResponse, UsageRecordListResponse
from config import ai_settings

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/process", tags=["文本处理"])


@router.post("")
async def process_text(
    request: ProcessRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    文本处理接口（非流式）
    """
    try:
        if not is_valid_member(current_user):
            logger.warning(f"会员已过期: {current_user.email}")
            raise HTTPException(status_code=403, detail="会员已过期，请兑换卡密")
        
        if not request.text or len(request.text.strip()) < 10:
            raise HTTPException(status_code=400, detail="请输入至少10个字符的文本")
        
        if len(request.text.strip()) > 50000:
            raise HTTPException(status_code=400, detail="文本长度不能超过50000字符")
        
        if request.mode not in ["mode1", "mode2"]:
            raise HTTPException(status_code=400, detail="无效的处理模式")
        
        # 使用配置文件中的API配置（前端可不传）
        api_key = request.api_key or ai_settings.API_KEY
        base_url = request.base_url or ai_settings.BASE_URL
        model = request.model or ai_settings.DEFAULT_MODEL
        temperature = request.temperature if request.temperature is not None else ai_settings.DEFAULT_TEMPERATURE
        max_tokens = request.max_tokens if request.max_tokens is not None else ai_settings.DEFAULT_MAX_TOKENS
        
        logger.info(f"使用API配置: base_url={base_url}, model={model}")
        
        record = UsageRecord(
            user_id=current_user.id,
            mode=request.mode,
            input_text=request.text[:50000],
            status="processing"
        )
        
        db.add(record)
        db.commit()
        db.refresh(record)
        
        try:
            # 使用AI处理（非流式）
            import asyncio
            from processor import get_processor
            
            # 获取用户专属处理器（多用户隔离）
            processor = get_processor(current_user.id)
            
            async def collect_result():
                full_result = ""
                async for result in processor.process_text(
                    text=request.text,
                    mode=request.mode,
                    api_key=api_key,
                    base_url=base_url,
                    model=model,
                    temperature=temperature,
                    max_tokens=max_tokens
                ):
                    if result.get("status") == "success":
                        full_result = result.get("result", "")
                    elif result.get("status") == "error":
                        raise Exception(result.get("error", "处理失败"))
                return full_result
            
            output_text = await collect_result()
            
        except HTTPException:
            record.status = "failed"
            record.error_message = "文本处理失败"
            db.commit()
            raise
        except Exception as e:
            record.status = "failed"
            record.error_message = str(e)
            db.commit()
            logger.error(f"处理失败: {str(e)}")
            raise HTTPException(status_code=500, detail="文本处理失败")
        
        record.output_text = output_text
        record.status = "success"
        
        current_user.total_usage += 1
        
        db.commit()
        
        logger.info(f"用户 {current_user.email} 处理文本成功，模式: {request.mode}")
        
        return {
            "success": True,
            "message": "处理成功",
            "output_text": output_text,
            "record_id": record.id
        }
    except HTTPException:
        raise
    except SQLAlchemyError as e:
        db.rollback()
        logger.error(f"数据库错误 - 处理文本失败: {str(e)}")
        raise HTTPException(status_code=500, detail="数据库操作失败，请稍后重试")
    except Exception as e:
        db.rollback()
        logger.error(f"处理文本失败: {str(e)}")
        raise HTTPException(status_code=500, detail="处理失败，请稍后重试")


@router.post("/stream")
async def process_text_stream(
    request: ProcessRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    文本处理接口（流式输出）
    推荐使用此接口获得实时处理进度和结果
    """
    try:
        if not is_valid_member(current_user):
            logger.warning(f"会员已过期: {current_user.email}")
            raise HTTPException(status_code=403, detail="会员已过期，请兑换卡密")
        
        if not request.text or len(request.text.strip()) < 10:
            raise HTTPException(status_code=400, detail="请输入至少10个字符的文本")
        
        if len(request.text.strip()) > 50000:
            raise HTTPException(status_code=400, detail="文本长度不能超过50000字符")
        
        if request.mode not in ["mode1", "mode2"]:
            raise HTTPException(status_code=400, detail="无效的处理模式")
        
        # 使用配置文件中的API配置（前端可不传）
        api_key = request.api_key or ai_settings.API_KEY
        base_url = request.base_url or ai_settings.BASE_URL
        model = request.model or ai_settings.DEFAULT_MODEL
        temperature = request.temperature if request.temperature is not None else ai_settings.DEFAULT_TEMPERATURE
        max_tokens = request.max_tokens if request.max_tokens is not None else ai_settings.DEFAULT_MAX_TOKENS
        
        logger.info(f"使用API配置: base_url={base_url}, model={model}")
        
        record = UsageRecord(
            user_id=current_user.id,
            mode=request.mode,
            input_text=request.text[:50000],
            status="processing"
        )
        
        db.add(record)
        db.commit()
        db.refresh(record)
        
        # 在进入异步生成器前保存需要的数据
        user_id = current_user.id
        user_email = current_user.email
        record_id = record.id
        mode = request.mode
        
        async def generate():
            from processor import get_processor
            from database import SessionLocal
            
            # 获取用户专属处理器（多用户隔离）
            processor = get_processor(user_id)
            
            full_result = ""
            
            # 在生成器内创建新的数据库会话
            db_gen = SessionLocal()
            
            try:
                async for result in processor.process_text(
                    text=request.text,
                    mode=request.mode,
                    api_key=api_key,
                    base_url=base_url,
                    model=model,
                    temperature=temperature,
                    max_tokens=max_tokens
                ):
                    # 发送进度更新
                    yield f"data: {json.dumps(result, ensure_ascii=False)}\n\n"
                    
                    # 收集最终结果
                    if result.get("status") == "success":
                        full_result = result.get("result", "")
                    elif result.get("status") == "error":
                        # 更新记录为失败
                        try:
                            rec = db_gen.query(UsageRecord).filter(UsageRecord.id == record_id).first()
                            if rec:
                                rec.status = "failed"
                                rec.error_message = result.get("error", "处理失败")
                                db_gen.commit()
                        except:
                            db_gen.rollback()
                        return
                
                # 更新记录为成功
                try:
                    rec = db_gen.query(UsageRecord).filter(UsageRecord.id == record_id).first()
                    user = db_gen.query(User).filter(User.id == user_id).first()
                    if rec and user:
                        rec.output_text = full_result
                        rec.status = "success"
                        user.total_usage += 1
                        db_gen.commit()
                        logger.info(f"用户 {user_email} 处理文本成功（流式），模式: {mode}")
                except Exception as db_err:
                    logger.error(f"更新记录失败: {str(db_err)}")
                    db_gen.rollback()
                
            except Exception as e:
                logger.error(f"流式处理失败: {str(e)}")
                try:
                    rec = db_gen.query(UsageRecord).filter(UsageRecord.id == record_id).first()
                    if rec:
                        rec.status = "failed"
                        rec.error_message = str(e)
                        db_gen.commit()
                except:
                    db_gen.rollback()
                
                error_data = {
                    "status": "error",
                    "error": f"处理失败: {str(e)}",
                    "progress": 0
                }
                yield f"data: {json.dumps(error_data, ensure_ascii=False)}\n\n"
            finally:
                db_gen.close()
        
        return StreamingResponse(
            generate(),
            media_type="text/event-stream",
            headers={
                "Cache-Control": "no-cache",
                "Connection": "keep-alive",
                "X-Accel-Buffering": "no"
            }
        )
        
    except HTTPException:
        raise
    except SQLAlchemyError as e:
        db.rollback()
        logger.error(f"数据库错误 - 处理文本失败: {str(e)}")
        raise HTTPException(status_code=500, detail="数据库操作失败，请稍后重试")
    except Exception as e:
        db.rollback()
        logger.error(f"处理文本失败: {str(e)}")
        raise HTTPException(status_code=500, detail="处理失败，请稍后重试")


@router.get("/records", response_model=UsageRecordListResponse)
def get_records(
    page: int = 1,
    limit: int = 10,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    获取使用记录
    """
    try:
        offset = (page - 1) * limit
        
        records = db.query(UsageRecord).filter(
            UsageRecord.user_id == current_user.id
        ).order_by(
            UsageRecord.created_at.desc()
        ).offset(offset).limit(limit).all()
        
        total = db.query(UsageRecord).filter(
            UsageRecord.user_id == current_user.id
        ).count()
        
        return {
            "records": records,
            "total": total,
            "page": page,
            "limit": limit
        }
    except SQLAlchemyError as e:
        logger.error(f"数据库错误 - 获取记录失败: {str(e)}")
        raise HTTPException(status_code=500, detail="获取记录失败")


@router.get("/records/{record_id}", response_model=UsageRecordResponse)
def get_record(
    record_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    获取单条使用记录
    """
    record = db.query(UsageRecord).filter(
        UsageRecord.id == record_id,
        UsageRecord.user_id == current_user.id
    ).first()
    
    if not record:
        raise HTTPException(status_code=404, detail="记录不存在")
    
    return record


@router.delete("/records/{record_id}")
def delete_record(
    record_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    删除使用记录
    """
    record = db.query(UsageRecord).filter(
        UsageRecord.id == record_id,
        UsageRecord.user_id == current_user.id
    ).first()
    
    if not record:
        raise HTTPException(status_code=404, detail="记录不存在")
    
    try:
        db.delete(record)
        db.commit()
        return {"success": True, "message": "删除成功"}
    except SQLAlchemyError as e:
        db.rollback()
        logger.error(f"数据库错误 - 删除记录失败: {str(e)}")
        raise HTTPException(status_code=500, detail="删除记录失败")


@router.post("/clear-cache")
def clear_cache(
    current_user: User = Depends(get_current_user)
):
    """
    清除用户的历史缓存
    防止旧内容污染新内容
    """
    try:
        from processor import clear_user_cache
        
        success = clear_user_cache(current_user.id)
        
        if success:
            logger.info(f"用户 {current_user.email} 清除历史缓存成功")
            return {
                "success": True,
                "message": "历史缓存已清除"
            }
        else:
            logger.warning(f"用户 {current_user.email} 清除历史缓存失败（无缓存）")
            return {
                "success": True,
                "message": "无历史缓存需要清除"
            }
    except Exception as e:
        logger.error(f"清除历史缓存失败: {str(e)}")
        raise HTTPException(status_code=500, detail="清除缓存失败")
