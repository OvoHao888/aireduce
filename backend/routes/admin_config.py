"""
管理员系统配置接口
包括API配置、系统参数等
"""
from fastapi import APIRouter, Depends, HTTPException, Header
from pydantic import BaseModel
from sqlalchemy.orm import Session
from database import get_db
from jose import jwt, JWTError
from config import ai_settings, SecuritySettings
import logging
import os
from typing import Optional

logger = logging.getLogger(__name__)


def _mask_key(key: str) -> str:
    """只回显尾部 4 位。完整密钥经接口回显会泄漏到浏览器、日志与前端缓存。"""
    if not key:
        return ""
    return "****" + key[-4:] if len(key) > 8 else "****"
router = APIRouter(prefix="/api/admin/config", tags=["admin-config"])

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM", "HS256")

# ==================== 验证管理员token ====================
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
    except JWTError:
        raise HTTPException(status_code=401, detail="无效的认证令牌", headers={"WWW-Authenticate": "Bearer"})


# ==================== 请求模型 ====================
class APIConfigRequest(BaseModel):
    api_key: str
    base_url: str
    model: str
    temperature: Optional[float] = 1.0
    max_tokens: Optional[int] = 4096

class APIConfigResponse(BaseModel):
    api_key: str
    base_url: str
    model: str
    temperature: float
    max_tokens: int


# ==================== 获取API配置 ====================
@router.get("/api", response_model=APIConfigResponse)
def get_api_config(admin_payload: dict = Depends(verify_admin_token)):
    """
    获取当前API配置
    """
    return {
        "api_key": _mask_key(ai_settings.API_KEY),
        "base_url": ai_settings.BASE_URL,
        "model": ai_settings.DEFAULT_MODEL,
        "temperature": ai_settings.DEFAULT_TEMPERATURE,
        "max_tokens": ai_settings.DEFAULT_MAX_TOKENS
    }


# ==================== 更新API配置 ====================
@router.post("/api")
def update_api_config(
    config: APIConfigRequest,
    admin_payload: dict = Depends(verify_admin_token)
):
    """
    更新API配置（写入.env文件）
    """
    try:
        # 读取现有.env文件
        env_path = os.path.join(os.path.dirname(__file__), "..", ".env")
        env_lines = []
        
        if os.path.exists(env_path):
            with open(env_path, "r", encoding="utf-8") as f:
                env_lines = f.readlines()
        
        # 需要更新的配置
        config_map = {
            "API_KEY": config.api_key,
            "BASE_URL": config.base_url,
            "DEFAULT_MODEL": config.model,
            "DEFAULT_TEMPERATURE": str(config.temperature),
            "DEFAULT_MAX_TOKENS": str(config.max_tokens)
        }
        
        # 更新或添加配置
        updated_keys = set()
        new_lines = []
        
        for line in env_lines:
            stripped = line.strip()
            if "=" in stripped and not stripped.startswith("#"):
                key = stripped.split("=")[0].strip()
                if key in config_map:
                    new_lines.append(f"{key}={config_map[key]}\n")
                    updated_keys.add(key)
                else:
                    new_lines.append(line)
            else:
                new_lines.append(line)
        
        # 添加未更新的配置
        for key, value in config_map.items():
            if key not in updated_keys:
                new_lines.append(f"{key}={value}\n")
        
        # 写入.env文件
        with open(env_path, "w", encoding="utf-8") as f:
            f.writelines(new_lines)
        
        logger.info(f"管理员 {admin_payload.get('sub')} 更新了API配置")
        
        return {
            "success": True,
            "message": "配置已保存，重启服务后生效",
            "config": {
                "api_key": _mask_key(config.api_key),
                "base_url": config.base_url,
                "model": config.model,
                "temperature": config.temperature,
                "max_tokens": config.max_tokens
            }
        }
        
    except Exception as e:
        logger.error(f"更新API配置失败: {str(e)}")
        raise HTTPException(status_code=500, detail=f"保存配置失败: {str(e)}")


# ==================== 测试API连接 ====================
@router.post("/api/test")
async def test_api_connection(
    config: APIConfigRequest,
    admin_payload: dict = Depends(verify_admin_token)
):
    """
    测试API连接是否正常
    """
    try:
        from openai import AsyncOpenAI
        
        client = AsyncOpenAI(
            api_key=config.api_key,
            base_url=config.base_url
        )
        
        # 发送简单测试请求
        response = await client.chat.completions.create(
            model=config.model,
            messages=[{"role": "user", "content": "你好"}],
            max_tokens=10
        )
        
        logger.info(f"API连接测试成功: {config.base_url}")
        
        return {
            "success": True,
            "message": "API连接正常",
            "model": config.model,
            "response": response.choices[0].message.content if response.choices else None
        }
        
    except Exception as e:
        logger.error(f"API连接测试失败: {str(e)}")
        return {
            "success": False,
            "message": f"连接失败: {str(e)}"
        }


# ==================== 获取支持的模型列表 ====================
@router.get("/models")
def get_supported_models(admin_payload: dict = Depends(verify_admin_token)):
    """
    获取支持的模型列表
    """
    return {
        "models": ai_settings.SUPPORTED_MODELS,
        "current": ai_settings.DEFAULT_MODEL
    }
