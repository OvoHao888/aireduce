from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from database import get_db
from models import User
from schemas import UserRegister, UserLogin, UserResponse, TokenResponse
from auth import verify_password, get_password_hash, create_access_token, get_current_user, get_member_level
from config import security_settings
from deps import rate_limit
from datetime import datetime
import logging

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/api/users", tags=["users"])

@router.post("/register", response_model=TokenResponse, status_code=status.HTTP_201_CREATED)
def register(user_data: UserRegister, db: Session = Depends(get_db)):
    try:
        existing_email = db.query(User).filter(User.email == user_data.email).first()
        if existing_email:
            raise HTTPException(status_code=400, detail="邮箱已被注册")
        
        existing_username = db.query(User).filter(User.username == user_data.username).first()
        if existing_username:
            raise HTTPException(status_code=400, detail="用户名已被使用")
        
        if len(user_data.password) < 6:
            raise HTTPException(status_code=400, detail="密码长度不能少于6位")
        
        if len(user_data.username) < 2 or len(user_data.username) > 50:
            raise HTTPException(status_code=400, detail="用户名长度应在2-50位之间")
        
        hashed_password = get_password_hash(user_data.password)
        user = User(
            username=user_data.username,
            email=user_data.email,
            password=hashed_password,
            expire_date=None,
            total_usage=0
        )
        
        db.add(user)
        db.commit()
        db.refresh(user)
        
        access_token = create_access_token(data={"sub": user.email})
        
        logger.info(f"新用户注册成功: {user.email}")
        
        return {
            "access_token": access_token,
            "token_type": "bearer",
            "user": {
                "id": user.id,
                "username": user.username,
                "email": user.email,
                "expire_date": user.expire_date,
                "total_usage": user.total_usage,
                "member_level": None
            }
        }
    except HTTPException:
        raise
    except SQLAlchemyError as e:
        db.rollback()
        logger.error(f"数据库错误 - 注册失败: {str(e)}")
        raise HTTPException(status_code=500, detail="数据库操作失败，请稍后重试")
    except Exception as e:
        db.rollback()
        logger.error(f"注册失败: {str(e)}")
        raise HTTPException(status_code=500, detail="注册失败，请稍后重试")

@router.post(
    "/login",
    response_model=TokenResponse,
    dependencies=[Depends(rate_limit("login", security_settings.LOGIN_RATE_LIMIT_PER_MINUTE))],
)
def login(user_data: UserLogin, db: Session = Depends(get_db)):
    try:
        if not user_data.email or not user_data.password:
            raise HTTPException(status_code=400, detail="邮箱和密码不能为空")
        
        user = db.query(User).filter(User.email == user_data.email).first()
        
        if not user:
            logger.warning(f"登录失败 - 用户不存在: {user_data.email}")
            raise HTTPException(status_code=401, detail="邮箱或密码错误")
        
        if not verify_password(user_data.password, user.password):
            logger.warning(f"登录失败 - 密码错误: {user_data.email}")
            raise HTTPException(status_code=401, detail="邮箱或密码错误")
        
        user.updated_at = datetime.now()
        db.commit()
        
        access_token = create_access_token(data={"sub": user.email})
        
        logger.info(f"用户登录成功: {user.email}")
        
        return {
            "access_token": access_token,
            "token_type": "bearer",
            "user": {
                "id": user.id,
                "username": user.username,
                "email": user.email,
                "expire_date": user.expire_date,
                "total_usage": user.total_usage,
                "member_level": get_member_level(user)
            }
        }
    except HTTPException:
        raise
    except SQLAlchemyError as e:
        db.rollback()
        logger.error(f"数据库错误 - 登录失败: {str(e)}")
        raise HTTPException(status_code=500, detail="数据库操作失败，请稍后重试")
    except Exception as e:
        db.rollback()
        logger.error(f"登录失败: {str(e)}")
        raise HTTPException(status_code=500, detail="登录失败，请稍后重试")

@router.get("/me", response_model=UserResponse)
def get_me(current_user: User = Depends(get_current_user)):
    try:
        return {
            "id": current_user.id,
            "username": current_user.username,
            "email": current_user.email,
            "expire_date": current_user.expire_date,
            "total_usage": current_user.total_usage,
            "member_level": get_member_level(current_user)
        }
    except Exception as e:
        logger.error(f"获取用户信息失败: {str(e)}")
        raise HTTPException(status_code=500, detail="获取用户信息失败")

class UpdateProfileRequest(BaseModel):
    username: str = None
    email: str = None

@router.put("/me")
def update_profile(
    request: UpdateProfileRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    try:
        username = request.username
        email = request.email
        if username is not None:
            if len(username) < 2 or len(username) > 50:
                raise HTTPException(status_code=400, detail="用户名长度应在2-50位之间")
            
            existing = db.query(User).filter(
                User.username == username,
                User.id != current_user.id
            ).first()
            if existing:
                raise HTTPException(status_code=400, detail="用户名已被使用")
            current_user.username = username
        
        if email is not None:
            existing = db.query(User).filter(
                User.email == email,
                User.id != current_user.id
            ).first()
            if existing:
                raise HTTPException(status_code=400, detail="邮箱已被注册")
            current_user.email = email
        
        db.commit()
        db.refresh(current_user)
        
        logger.info(f"用户资料更新成功: {current_user.email}")
        
        return {"message": "更新成功"}
    except HTTPException:
        raise
    except SQLAlchemyError as e:
        db.rollback()
        logger.error(f"数据库错误 - 更新资料失败: {str(e)}")
        raise HTTPException(status_code=500, detail="数据库操作失败，请稍后重试")
    except Exception as e:
        db.rollback()
        logger.error(f"更新资料失败: {str(e)}")
        raise HTTPException(status_code=500, detail="更新资料失败，请稍后重试")

class ChangePasswordRequest(BaseModel):
    old_password: str
    new_password: str

class DeleteAccountRequest(BaseModel):
    password: str

@router.put("/me/password")
def change_password(
    request: ChangePasswordRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    try:
        if not request.old_password or not request.new_password:
            raise HTTPException(status_code=400, detail="密码不能为空")
        
        if len(request.new_password) < 6:
            raise HTTPException(status_code=400, detail="新密码长度不能少于6位")
        
        if not verify_password(request.old_password, current_user.password):
            raise HTTPException(status_code=400, detail="原密码不正确")
        
        current_user.password = get_password_hash(request.new_password)
        db.commit()
        
        logger.info(f"用户密码修改成功: {current_user.email}")
        
        return {"message": "密码修改成功"}
    except HTTPException:
        raise
    except SQLAlchemyError as e:
        db.rollback()
        logger.error(f"数据库错误 - 修改密码失败: {str(e)}")
        raise HTTPException(status_code=500, detail="数据库操作失败，请稍后重试")
    except Exception as e:
        db.rollback()
        logger.error(f"修改密码失败: {str(e)}")
        raise HTTPException(status_code=500, detail="修改密码失败，请稍后重试")

@router.delete("/me")
def delete_account(
    request: DeleteAccountRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    try:
        if not request.password:
            raise HTTPException(status_code=400, detail="请输入密码确认删除")
        
        if not verify_password(request.password, current_user.password):
            raise HTTPException(status_code=400, detail="密码不正确")
        
        db.delete(current_user)
        db.commit()
        
        logger.info(f"用户删除账号: {current_user.email}")
        
        return {"message": "账号删除成功"}
    except HTTPException:
        raise
    except SQLAlchemyError as e:
        db.rollback()
        logger.error(f"数据库错误 - 删除账号失败: {str(e)}")
        raise HTTPException(status_code=500, detail="数据库操作失败，请稍后重试")
    except Exception as e:
        db.rollback()
        logger.error(f"删除账号失败: {str(e)}")
        raise HTTPException(status_code=500, detail="删除账号失败，请稍后重试")