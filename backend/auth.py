from datetime import datetime, timedelta
from typing import Optional
from jose import JWTError, jwt
from jose.exceptions import ExpiredSignatureError
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from database import get_db
from models import User
from dotenv import load_dotenv
import os
import logging
import hashlib
import hmac
import bcrypt

logger = logging.getLogger(__name__)

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")

try:
    ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "10080"))  # 默认7天=7*24*60=10080分钟
except (ValueError, TypeError):
    ACCESS_TOKEN_EXPIRE_MINUTES = 10080  # 7天

if not SECRET_KEY:
    logger.error("SECRET_KEY 未在环境变量中配置")
    raise ValueError("SECRET_KEY 环境变量必须配置")

if not ALGORITHM:
    logger.warning("ALGORITHM 未配置，使用默认值 HS256")
    ALGORITHM = "HS256"

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/users/login")

# 密码哈希统一用 bcrypt：自带随机盐 + 可调成本因子。
# 原实现是单轮无盐 SHA-256 —— 同一密码永远得到同一个哈希，彩虹表/GPU 可秒破，
# 且没有盐意味着撞库后所有使用相同密码的账号会同时失守。
PASSWORD_MIN_LENGTH = 8
PASSWORD_MAX_LENGTH = 32
# bcrypt 算法本身只取前 72 字节，超出部分会被静默忽略（新版库直接抛错），
# 因此在入口按字节长度拦截，避免"密码后半段其实没参与校验"。
BCRYPT_MAX_BYTES = 72

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """校验密码：bcrypt 恒定时间比较；同时兼容历史无盐 SHA-256 哈希，便于平滑迁移。"""
    if not plain_password or not hashed_password:
        return False
    try:
        if hashed_password.startswith("$2"):
            return bcrypt.checkpw(
                plain_password.encode("utf-8"), hashed_password.encode("utf-8")
            )
        legacy = hashlib.sha256(plain_password.encode("utf-8")).hexdigest()
        return hmac.compare_digest(legacy, hashed_password)
    except Exception as e:
        logger.error(f"密码验证失败: {str(e)}")
        return False

def get_password_hash(password: str) -> str:
    try:
        if len(password) < PASSWORD_MIN_LENGTH:
            logger.warning(f"密码长度不足: {len(password)}")
            raise HTTPException(status_code=400, detail=f"密码长度不能少于{PASSWORD_MIN_LENGTH}位")
        if len(password) > PASSWORD_MAX_LENGTH:
            logger.warning(f"密码长度超过: {len(password)}")
            raise HTTPException(status_code=400, detail=f"密码长度不能超过{PASSWORD_MAX_LENGTH}位")
        if len(password.encode("utf-8")) > BCRYPT_MAX_BYTES:
            raise HTTPException(status_code=400, detail="密码过长，请使用较短的密码")
        return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"密码哈希失败: {str(e)}")
        raise HTTPException(status_code=500, detail="密码处理失败")

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    try:
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
        return encoded_jwt
    except JWTError as e:
        logger.error(f"JWT编码失败: {str(e)}")
        raise HTTPException(status_code=500, detail="令牌生成失败")
    except Exception as e:
        logger.error(f"创建访问令牌失败: {str(e)}")
        raise HTTPException(status_code=500, detail="令牌生成失败")

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)) -> User:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            logger.warning("JWT payload 中缺少用户邮箱")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="invalid_token",
                headers={"WWW-Authenticate": "Bearer"},
            )
    except ExpiredSignatureError:
        logger.warning("JWT令牌已过期")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="token_expired",
            headers={"WWW-Authenticate": "Bearer"},
        )
    except JWTError as e:
        logger.warning(f"JWT解析失败: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="invalid_token",
            headers={"WWW-Authenticate": "Bearer"},
        )
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"认证失败: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="invalid_token",
            headers={"WWW-Authenticate": "Bearer"},
        )

    try:
        user = db.query(User).filter(User.email == email).first()
        if user is None:
            logger.warning(f"用户不存在: {email}")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="invalid_token",
                headers={"WWW-Authenticate": "Bearer"},
            )
        return user
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"数据库查询失败: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="invalid_token",
            headers={"WWW-Authenticate": "Bearer"},
        )

def is_valid_member(user: User) -> bool:
    try:
        if user.expire_date is None:
            return False
        return user.expire_date > datetime.now()
    except Exception as e:
        logger.error(f"检查会员状态失败: {str(e)}")
        return False

def get_member_level(user: User) -> Optional[str]:
    try:
        if not is_valid_member(user):
            return None
        
        remaining_days = (user.expire_date - datetime.now()).days
        
        if remaining_days >= 365:
            return "vip3"
        elif remaining_days >= 180:
            return "vip2"
        elif remaining_days >= 30:
            return "vip1"
        else:
            return "member"
    except Exception as e:
        logger.error(f"获取会员等级失败: {str(e)}")
        return None