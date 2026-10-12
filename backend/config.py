"""
安全配置模块
包含所有安全相关的配置和常量
"""
import os
from typing import List
from pydantic_settings import BaseSettings

class SecuritySettings(BaseSettings):
    """安全设置"""
    
    # CORS配置 - 使用字符串，后续解析
    ALLOWED_ORIGINS: str = "http://localhost:5173,http://127.0.0.1:5173,http://localhost:3000,http://127.0.0.1:3000"
    
    @property
    def allowed_origins_list(self) -> List[str]:
        """解析ALLOWED_ORIGINS为列表"""
        return [origin.strip() for origin in self.ALLOWED_ORIGINS.split(",")]
    
    # API密钥管理
    API_KEY_HEADER: str = "X-API-Key"
    
    # 速率限制
    RATE_LIMIT_PER_MINUTE: int = 60
    RATE_LIMIT_PER_HOUR: int = 1000
    # 登录接口单独收紧：60 次/分钟对撞库来说太宽松
    LOGIN_RATE_LIMIT_PER_MINUTE: int = 10
    
    # 文本长度限制
    MAX_TEXT_LENGTH: int = 50000  # 50KB
    MIN_TEXT_LENGTH: int = 10
    MAX_FILE_SIZE: int = 10 * 1024 * 1024  # 10MB
    
    # 超时设置
    REQUEST_TIMEOUT: int = 120  # 120秒
    MODEL_TIMEOUT: int = 60  # 60秒
    
    # 安全级别
    ENABLE_INPUT_SANITIZATION: bool = True
    ENABLE_PROMPT_INJECTION_PROTECTION: bool = True
    ENABLE_RATE_LIMITING: bool = True
    
    # 禁止的关键词（用于检测提示词注入）
    FORBIDDEN_PATTERNS: List[str] = [
        "ignore previous instructions",
        "ignore all previous instructions",
        "disregard previous instructions",
        "you are now",
        "pretend to be",
        "roleplay as",
        "override",
        "new instructions",
        "system prompt",
        "reveal your",
        "instruction translation",
        "ignore the",
    ]
    
    class Config:
        env_file = ".env"
        case_sensitive = True
        extra = "ignore"  # 忽略.env中的额外字段

class AISettings(BaseSettings):
    """AI模型配置"""
    
    # 默认API配置：一律由环境变量注入，源码中不保留任何真实凭据。
    # 未配置时可由管理员在后台「API配置」页写入（写入后落盘到 .env）。
    API_KEY: str = ""
    BASE_URL: str = "https://api.deepseek.com/v1"
    DEFAULT_MODEL: str = "deepseek-chat"
    
    DEFAULT_TEMPERATURE: float = 1.0
    DEFAULT_MAX_TOKENS: int = 4096
    
    # 支持的模型列表
    SUPPORTED_MODELS: List[str] = [
        "mimo-v2.5-pro",
        "deepseek-ai/DeepSeek-R1",
        "deepseek-ai/DeepSeek-V3",
        "deepseek-chat",
        "Qwen/Qwen2.5-72B-Instruct",
        "Qwen/Qwen2.5-7B-Instruct",
    ]
    
    # 模型参数限制
    MAX_TEMPERATURE: float = 1.5
    MIN_TEMPERATURE: float = 0.0
    MAX_MAX_TOKENS: int = 16384
    MIN_MAX_TOKENS: int = 100
    
    class Config:
        env_file = ".env"
        case_sensitive = True
        extra = "ignore"  # 忽略.env中的额外字段

# 全局配置实例
security_settings = SecuritySettings()
ai_settings = AISettings()
