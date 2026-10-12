"""
FastAPI 横切依赖。

速率限制必须挂在接口入口，而不是散落在业务逻辑里 ——
security.py 里那套实现此前只被 import、从未被调用，
于是"每分钟 60 次限流"实际上是纸面承诺。
"""

import logging
from typing import Callable

from fastapi import HTTPException, Request, status

from security import security_validator

logger = logging.getLogger(__name__)


def _client_id(request: Request) -> str:
    """按客户端地址标识。

    注意：只有部署在可信反向代理之后时才应改读 X-Forwarded-For，
    否则客户端可以随意伪造该头绕过限流。
    """
    return request.client.host if request.client else "unknown"


def rate_limit(scope: str, max_requests: int, window_seconds: int = 60) -> Callable:
    """生成一个限流依赖。

    用法::

        @router.post("/login", dependencies=[Depends(rate_limit("login", 10))])

    超限时返回 429 并带上 Retry-After，同时记录一条安全事件。
    """

    def dependency(request: Request) -> None:
        client = _client_id(request)
        allowed, message = security_validator.check_rate_limit(
            f"{scope}:{client}",
            max_requests=max_requests,
            window_seconds=window_seconds,
        )
        if not allowed:
            security_validator.log_security_event(
                "RATE_LIMIT", client, f"{scope} -> {message}"
            )
            raise HTTPException(
                status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                detail=message,
                headers={"Retry-After": str(window_seconds)},
            )

    return dependency
