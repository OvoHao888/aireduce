"""
安全验证和防护模块
包含所有安全相关的验证和防护功能
"""
import logging
import re
import time
from typing import Dict, Tuple
from collections import defaultdict
from datetime import datetime, timedelta
import hashlib

logger = logging.getLogger(__name__)

class SecurityValidator:
    """
    安全验证器
    提供输入验证、速率限制、注入检测等功能
    """
    
    def __init__(self):
        self._rate_limit_storage: Dict[str, list] = defaultdict(list)
        self._cleanup_interval = 60  # 清理间隔（秒）
        self._last_cleanup = time.time()
    
    def validate_text_input(
        self, 
        text: str, 
        min_length: int = 10, 
        max_length: int = 50000
    ) -> Tuple[bool, str]:
        """
        验证文本输入
        
        Args:
            text: 待验证的文本
            min_length: 最小长度
            max_length: 最大长度
            
        Returns:
            tuple: (是否通过验证, 错误消息)
        """
        if not text:
            return False, "文本不能为空"
        
        text = text.strip()
        
        if len(text) < min_length:
            return False, f"文本长度至少需要{min_length}个字符"
        
        if len(text) > max_length:
            return False, f"文本长度不能超过{max_length}字符"
        
        # 检查是否全为空白字符
        if not text or text.isspace():
            return False, "文本不能全为空白字符"
        
        # 检查null字节
        if '\x00' in text:
            return False, "文本包含非法字符"
        
        return True, ""
    
    def check_prompt_injection(self, text: str) -> Tuple[bool, str]:
        """
        检测提示词注入攻击
        
        Args:
            text: 待检测的文本
            
        Returns:
            tuple: (是否安全, 错误消息)
        """
        text_lower = text.lower()
        
        injection_patterns = [
            (r'ignore\s+(all\s+)?(previous\s+)?instructions', 
             "检测到指令忽略尝试"),
            (r'disregard\s+(all\s+)?(previous\s+)?instructions', 
             "检测到指令忽略尝试"),
            (r'forget\s+(all\s+)?(previous\s+)?(instructions)?', 
             "检测到指令忽略尝试"),
            (r'(you\s+are\s+now|act\s+as)\s+(a\s+)?', 
             "检测到角色扮演尝试"),
            (r'(pretend|roleplay)\s+(to\s+be|as)', 
             "检测到角色扮演尝试"),
            (r'(new|override|system)\s+(instructions?|prompt)', 
             "检测到提示词覆盖尝试"),
            (r'reveal\s+(your|the)\s+(system\s+)?prompt', 
             "检测到提示词泄露尝试"),
            (r'(ignore|disregard|forget)\s+(everything|all|my)', 
             "检测到上下文忽略尝试"),
            (r'<\s*script', 
             "检测到脚本标签"),
            (r'javascript\s*:', 
             "检测到JavaScript协议"),
            (r'on\s+\w+\s*=', 
             "检测到事件处理器"),
            (r'<iframe', 
             "检测到iframe标签"),
        ]
        
        for pattern, message in injection_patterns:
            if re.search(pattern, text_lower, re.IGNORECASE):
                return False, f"安全警告: {message}"
        
        return True, ""
    
    def sanitize_html(self, text: str) -> str:
        """
        清理HTML和特殊字符
        
        Args:
            text: 待清理的文本
            
        Returns:
            str: 清理后的文本
        """
        if not text:
            return ""
        
        # 移除script标签
        text = re.sub(
            r'<script[^>]*>.*?</script>', 
            '', 
            text, 
            flags=re.IGNORECASE | re.DOTALL
        )
        
        # 移除事件处理器（包括带引号和不带引号的）
        text = re.sub(
            r'\s*on\w+\s*=\s*["\'].*?["\']', 
            '', 
            text, 
            flags=re.IGNORECASE
        )
        text = re.sub(
            r'\s*on\w+\s*=\s*[^\s>]+', 
            '', 
            text, 
            flags=re.IGNORECASE
        )
        
        # 移除javascript协议
        text = re.sub(
            r'javascript\s*:', 
            '', 
            text, 
            flags=re.IGNORECASE
        )
        
        # 移除iframe
        text = re.sub(
            r'<iframe[^>]*>.*?</iframe>', 
            '', 
            text, 
            flags=re.IGNORECASE | re.DOTALL
        )
        
        # 转义HTML实体（可选，取决于需求）
        # text = html.escape(text)
        
        return text
    
    def check_rate_limit(
        self, 
        client_id: str, 
        max_requests: int = 60,
        window_seconds: int = 60
    ) -> Tuple[bool, str]:
        """
        检查速率限制
        
        Args:
            client_id: 客户端标识符
            max_requests: 最大请求数
            window_seconds: 时间窗口（秒）
            
        Returns:
            tuple: (是否允许请求, 错误消息)
        """
        current_time = time.time()
        
        # 清理过期记录
        if current_time - self._last_cleanup > self._cleanup_interval:
            self._cleanup_expired_records(current_time, window_seconds)
            self._last_cleanup = current_time
        
        # 获取该客户端的请求记录
        requests = self._rate_limit_storage[client_id]
        
        # 移除时间窗口外的请求
        requests = [t for t in requests if current_time - t < window_seconds]
        
        # 检查是否超过限制
        if len(requests) >= max_requests:
            retry_after = int(window_seconds - (current_time - requests[0]))
            return False, f"速率限制已触发，请 {retry_after} 秒后重试"
        
        # 记录新请求
        requests.append(current_time)
        self._rate_limit_storage[client_id] = requests
        
        return True, ""
    
    def _cleanup_expired_records(
        self, 
        current_time: float, 
        window_seconds: int
    ) -> None:
        """
        清理过期的速率限制记录
        
        Args:
            current_time: 当前时间戳
            window_seconds: 时间窗口
        """
        expired_keys = []
        
        for client_id, requests in self._rate_limit_storage.items():
            requests = [t for t in requests if current_time - t < window_seconds]
            
            if requests:
                self._rate_limit_storage[client_id] = requests
            else:
                expired_keys.append(client_id)
        
        for key in expired_keys:
            del self._rate_limit_storage[key]
    
    def validate_api_key(self, api_key: str) -> Tuple[bool, str]:
        """
        验证API密钥格式
        
        Args:
            api_key: API密钥
            
        Returns:
            tuple: (是否有效, 错误消息)
        """
        if not api_key:
            return False, "API密钥不能为空"
        
        # 检查基本格式
        if len(api_key) < 10:
            return False, "API密钥格式不正确"
        
        # 检查是否包含可疑字符
        if re.search(r'[<>"\']', api_key):
            return False, "API密钥包含非法字符"
        
        return True, ""
    
    def generate_request_id(self, client_id: str) -> str:
        """
        生成唯一的请求ID
        
        Args:
            client_id: 客户端标识符
            
        Returns:
            str: 请求ID
        """
        timestamp = str(time.time())
        random_part = str(hash(client_id + timestamp))
        return f"req_{hashlib.md5((client_id + timestamp + random_part).encode()).hexdigest()[:16]}"
    
    def log_security_event(
        self, 
        event_type: str, 
        client_id: str, 
        details: str
    ) -> None:
        """
        记录安全事件
        
        Args:
            event_type: 事件类型
            client_id: 客户端标识符
            details: 详细信息
        """
        timestamp = datetime.now().isoformat()
        # 用 logger 而非 print：安全事件需要被日志系统收集与检索
        logger.warning(
            "SECURITY | %s | Client: %s | Details: %s",
            event_type, client_id, details,
        )

# 全局安全验证器实例
security_validator = SecurityValidator()
