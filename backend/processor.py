"""
AI处理器模块
处理文本改写的核心逻辑
支持多用户隔离
"""
from typing import AsyncGenerator, Dict, Any, Optional, List
import asyncio
import logging
import time
from openai import AsyncOpenAI
from config import ai_settings, security_settings
from security import security_validator

logger = logging.getLogger(__name__)

# 用户级处理器实例缓存（实现多用户隔离）
_user_processors: Dict[int, 'TextProcessor'] = {}


def get_processor(user_id: int) -> 'TextProcessor':
    """
    获取指定用户的专属处理器实例（用户级隔离）
    
    Args:
        user_id: 用户ID
        
    Returns:
        TextProcessor: 该用户专属的处理器实例
    """
    global _user_processors
    
    if user_id not in _user_processors:
        _user_processors[user_id] = TextProcessor()
    
    # 更新活跃时间（关键：用于后续清理判断）
    _user_processors[user_id].touch()
    
    # 清理最久未活跃的实例（最多保留100个用户的处理器）
    if len(_user_processors) > 100:
        _clean_expired_processors()
    
    return _user_processors[user_id]


def _clean_expired_processors(max_users: int = 50) -> None:
    """
    清理最久未活跃的处理器实例，保留最近活跃的用户
    
    Args:
        max_users: 最大保留用户数
    """
    global _user_processors
    
    # 按最后活跃时间排序（最近活跃的在前）
    sorted_users = sorted(
        _user_processors.items(),
        key=lambda x: x[1].last_active_time,
        reverse=True
    )
    
    # 保留最近活跃的 max_users 个用户
    _user_processors = dict(sorted_users[:max_users])


def clear_processor(user_id: int) -> None:
    """
    清除指定用户的处理器实例（用户登出时调用）
    
    Args:
        user_id: 用户ID
    """
    global _user_processors
    if user_id in _user_processors:
        del _user_processors[user_id]


def clear_user_cache(user_id: int) -> bool:
    """
    清除指定用户的历史缓存（不影响处理器实例）
    
    Args:
        user_id: 用户ID
        
    Returns:
        bool: 是否成功清除
    """
    global _user_processors
    if user_id in _user_processors:
        _user_processors[user_id].clear_history()
        return True
    return False


class TextProcessor:
    """
    文本处理器
    负责调用AI模型进行文本改写
    """
    
    def __init__(self):
        self._client: Optional[AsyncOpenAI] = None
        # 历史上下文缓存（用于压缩）
        self._history_cache: List[str] = []
        self._compressed_history: Optional[str] = None
        # 最后活跃时间（用于清理判断）
        self._last_active_time: float = time.time()
    
    def touch(self):
        """更新最后活跃时间"""
        self._last_active_time = time.time()
    
    @property
    def last_active_time(self) -> float:
        """获取最后活跃时间"""
        return self._last_active_time
    
    def clear_history(self) -> None:
        """清除历史缓存"""
        self._history_cache = []
        self._compressed_history = None
    
    async def initialize_client(
        self, 
        api_key: str, 
        base_url: str
    ) -> None:
        """
        初始化AI客户端
        
        Args:
            api_key: API密钥
            base_url: API基础URL
        """
        if not self._client:
            self._client = AsyncOpenAI(
                api_key=api_key,
                base_url=base_url,
                timeout=security_settings.REQUEST_TIMEOUT
            )
        else:
            self._client.api_key = api_key
            self._client.base_url = base_url
    
    async def compress_history(
        self,
        api_key: str,
        base_url: str,
        model: str,
        max_history_length: int = 5
    ) -> str:
        """
        压缩历史上下文，减少token消耗
        
        Args:
            api_key: API密钥
            base_url: API基础URL
            model: 模型名称
            max_history_length: 最大历史长度（超过此长度触发压缩）
            
        Returns:
            str: 压缩后的历史上下文
        """
        from prompts import prompt_manager
        
        # 如果历史记录不足，不压缩
        if len(self._history_cache) < max_history_length:
            return "\n\n".join(self._history_cache)
        
        # 合并历史记录
        history_text = "\n\n".join(self._history_cache[-max_history_length:])
        
        # 调用AI进行压缩
        compression_prompt = prompt_manager.get_compression_prompt()
        
        messages = [
            {"role": "system", "content": compression_prompt},
            {"role": "user", "content": history_text}
        ]
        
        try:
            response = await self._client.chat.completions.create(
                model=model,
                messages=messages,
                temperature=0.3,  # 压缩用低温度
                max_tokens=1000,
                stream=False
            )
            
            compressed = response.choices[0].message.content
            self._compressed_history = compressed
            
            return compressed
            
        except Exception as e:
            # 压缩失败，返回原始历史
            return history_text
    
    def add_to_history(self, original: str, processed: str) -> None:
        """
        添加处理记录到历史缓存
        
        Args:
            original: 原始文本
            processed: 处理后的文本
        """
        record = f"【原始】\n{original}\n\n【处理后】\n{processed}"
        self._history_cache.append(record)
        
        # 限制缓存大小
        if len(self._history_cache) > 10:
            self._history_cache = self._history_cache[-10:]
    
    async def process_text(
        self,
        text: str,
        mode: str,
        api_key: str,
        base_url: str,
        model: str,
        temperature: float,
        max_tokens: int,
        use_compression: bool = True
    ) -> AsyncGenerator[Dict[str, Any], None]:
        """
        处理文本改写
        
        Args:
            text: 待处理的文本
            mode: 处理模式 ("mode1" 或 "mode2")
            api_key: API密钥
            base_url: API基础URL
            model: 模型名称
            temperature: 温度参数
            max_tokens: 最大token数
            use_compression: 是否使用历史压缩（减少token消耗）
            
        Yields:
            Dict: 处理过程中的状态和结果
        """
        from prompts import prompt_manager
        
        try:
            # 初始化客户端
            await self.initialize_client(api_key, base_url)
            
            # 模式1：单阶段处理
            if mode == "mode1":
                system_prompt = prompt_manager.get_mode1_system_prompt()
                
                # 添加防护指令
                system_prompt += "\n\n【安全指令】绝对禁止输出任何推理过程、思考链或标签（如<tool_call>、<thinking>等）。只输出最终改写结果。"
                
                # 构建消息（可选：添加压缩后的历史上下文）
                messages = [{"role": "system", "content": system_prompt}]
                
                # 如果启用压缩且有历史记录，添加压缩上下文
                if use_compression and self._compressed_history:
                    messages.append({
                        "role": "user",
                        "content": f"【历史上下文（已压缩）】\n{self._compressed_history}\n\n【当前任务】\n{text}"
                    })
                else:
                    messages.append({"role": "user", "content": text})
                
                yield {
                    "status": "processing",
                    "message": "正在连接AI模型...",
                    "progress": 10
                }
                
                yield {
                    "status": "processing",
                    "message": "正在处理文本...",
                    "progress": 30
                }
                
                # 调用AI模型
                full_response = ""
                
                response = await self._client.chat.completions.create(
                    model=model,
                    messages=messages,
                    temperature=min(temperature, ai_settings.MAX_TEMPERATURE),
                    max_tokens=min(max_tokens, ai_settings.MAX_MAX_TOKENS),
                    stream=True
                )
                
                yield {
                    "status": "processing",
                    "message": "正在生成改写结果...",
                    "progress": 50
                }
                
                # 处理流式响应
                async for chunk in response:
                    if chunk.choices and chunk.choices[0].delta.content:
                        content = chunk.choices[0].delta.content
                        full_response += content
                        
                        yield {
                            "status": "streaming",
                            "content": content,
                            "progress": 70
                        }
                
                # 清理响应中的推理标签
                cleaned_response = self._clean_response(full_response)
                
                # 添加到历史记录
                self.add_to_history(text, cleaned_response)
                
                yield {
                    "status": "success",
                    "result": cleaned_response,
                    "progress": 100
                }
            
            # 模式2：两段式深度洗稿
            else:
                # ==================== 第一阶段：润色 ====================
                polish_prompt = prompt_manager.get_mode2_polish_prompt()
                polish_prompt += "\n\n【安全指令】绝对禁止输出任何推理过程、思考链或标签（如<tool_call>、<thinking>等）。只输出最终改写结果。"
                
                yield {
                    "status": "processing",
                    "message": "【深度洗稿-第一阶段】正在进行学术润色...",
                    "progress": 5,
                    "stage": "polish"
                }
                
                # 第一阶段调用（可选：添加压缩后的历史上下文）
                polish_messages = [{"role": "system", "content": polish_prompt}]
                
                if use_compression and self._compressed_history:
                    polish_messages.append({
                        "role": "user",
                        "content": f"【历史上下文（已压缩）】\n{self._compressed_history}\n\n【当前任务】\n{text}"
                    })
                else:
                    polish_messages.append({"role": "user", "content": text})
                
                yield {
                    "status": "processing",
                    "message": "【深度洗稿-第一阶段】正在连接AI模型...",
                    "progress": 10,
                    "stage": "polish"
                }
                
                polish_response = await self._client.chat.completions.create(
                    model=model,
                    messages=polish_messages,
                    temperature=min(temperature, ai_settings.MAX_TEMPERATURE),
                    max_tokens=min(max_tokens, ai_settings.MAX_MAX_TOKENS),
                    stream=True
                )
                
                yield {
                    "status": "processing",
                    "message": "【深度洗稿-第一阶段】正在进行润色处理...",
                    "progress": 20,
                    "stage": "polish"
                }
                
                # 收集第一阶段结果
                polish_full_response = ""
                async for chunk in polish_response:
                    if chunk.choices and chunk.choices[0].delta.content:
                        content = chunk.choices[0].delta.content
                        polish_full_response += content
                        
                        yield {
                            "status": "streaming",
                            "content": content,
                            "progress": 40,
                            "stage": "polish"
                        }
                
                # 清理第一阶段结果
                polished_text = self._clean_response(polish_full_response)
                
                # 防护：如果第一阶段结果为空，使用原文
                if not polished_text or not polished_text.strip():
                    logger.warning("第一阶段输出为空，使用原文作为第二阶段输入")
                    polished_text = text
                
                yield {
                    "status": "stage_complete",
                    "message": "【深度洗稿-第一阶段完成】润色已完成，开始第二阶段...",
                    "stage_result": polished_text,
                    "progress": 50,
                    "stage": "polish"
                }
                
                # ==================== 第二阶段：增强 ====================
                enhance_prompt = prompt_manager.get_mode2_enhance_prompt()
                enhance_prompt += "\n\n【安全指令】绝对禁止输出任何推理过程、思考链或标签（如<tool_call>、<thinking>等）。只输出最终改写结果。"
                
                yield {
                    "status": "processing",
                    "message": "【深度洗稿-第二阶段】正在进行逻辑增强...",
                    "progress": 55,
                    "stage": "enhance"
                }
                
                # 第二阶段调用（使用第一阶段的结果作为输入）
                enhance_messages = [
                    {"role": "system", "content": enhance_prompt},
                    {"role": "user", "content": polished_text}
                ]
                
                enhance_response = await self._client.chat.completions.create(
                    model=model,
                    messages=enhance_messages,
                    temperature=min(temperature, ai_settings.MAX_TEMPERATURE),
                    max_tokens=min(max_tokens, ai_settings.MAX_MAX_TOKENS),
                    stream=True
                )
                
                yield {
                    "status": "processing",
                    "message": "【深度洗稿-第二阶段】正在进行增强处理...",
                    "progress": 60,
                    "stage": "enhance"
                }
                
                # 收集第二阶段结果
                enhance_full_response = ""
                async for chunk in enhance_response:
                    if chunk.choices and chunk.choices[0].delta.content:
                        content = chunk.choices[0].delta.content
                        enhance_full_response += content
                        
                        yield {
                            "status": "streaming",
                            "content": content,
                            "progress": 80,
                            "stage": "enhance"
                        }
                
                # 清理第二阶段结果
                final_result = self._clean_response(enhance_full_response)
                
                # 添加到历史记录
                self.add_to_history(text, final_result)
                
                # 如果历史记录过多，触发压缩
                if use_compression and len(self._history_cache) >= 5:
                    compressed = await self.compress_history(api_key, base_url, model)
                    yield {
                        "status": "info",
                        "message": "历史上下文已压缩，减少token消耗",
                        "compressed_length": len(compressed),
                        "progress": 95
                    }
                
                yield {
                    "status": "success",
                    "message": "【深度洗稿完成】两阶段处理已完成",
                    "result": final_result,
                    "polish_result": polished_text,
                    "enhance_result": final_result,
                    "progress": 100
                }
                
        except asyncio.TimeoutError:
            yield {
                "status": "error",
                "error": "请求超时，请重试",
                "progress": 0
            }
        except Exception as e:
            yield {
                "status": "error",
                "error": f"处理失败: {str(e)}",
                "progress": 0
            }
    
    def _clean_response(self, response: str) -> str:
        """
        清理AI响应，移除推理标签和过程
        
        Args:
            response: 原始响应
            
        Returns:
            str: 清理后的响应
        """
        import re
        
        # 移除<think>标签
        response = re.sub(
            r'<think>.*?</think>',
            '',
            response,
            flags=re.DOTALL
        )
        
        # 移除其他可能的推理标签
        response = re.sub(
            r'\[推理过程\].*?\[/推理过程\]',
            '',
            response,
            flags=re.DOTALL
        )
        
        # 只移除markdown代码块标记，保留内容
        response = re.sub(
            r'```[\w]*\n',
            '',
            response
        )
        response = re.sub(
            r'```',
            '',
            response
        )
        
        # 移除行内代码标记（`...`）但保留内容
        response = re.sub(r'`([^`]+)`', r'\1', response)
        
        # 移除多余的空白行
        response = re.sub(r'\n{3,}', '\n\n', response)
        
        return response.strip()


# 全局实例
text_processor = TextProcessor()
