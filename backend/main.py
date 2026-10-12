from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from config import security_settings
from fastapi.responses import JSONResponse
from dotenv import load_dotenv
import os
import logging
from sqlalchemy.exc import SQLAlchemyError

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

load_dotenv()

app = FastAPI(title="AIReduce API", version="1.0.0")

@app.exception_handler(SQLAlchemyError)
async def sqlalchemy_exception_handler(request: Request, exc: SQLAlchemyError):
    logger.error(f"数据库错误: {str(exc)}")
    return JSONResponse(
        status_code=500,
        content={
            "detail": "数据库操作失败，请稍后重试",
            "error": "database_error"
        }
    )

@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception):
    logger.error(f"服务器错误: {str(exc)}")
    return JSONResponse(
        status_code=500,
        content={
            "detail": "服务器内部错误，请稍后重试",
            "error": "internal_error"
        }
    )

# 只放行配置白名单内的来源。allow_origins=["*"] 与 allow_credentials=True 同时启用时，
# 浏览器会收到按请求 Origin 回显的响应，等于任意站点都能带凭证访问本站；
# 而 config.py 里已有的 ALLOWED_ORIGINS 白名单此前完全没有生效。
app.add_middleware(
    CORSMiddleware,
    allow_origins=security_settings.allowed_origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

from routes.users import router as users_router
from routes.tokens import router as tokens_router
from routes.process import router as process_router
from routes.feedbacks import router as feedbacks_router
from routes.admin import router as admin_router
from routes.admin_users import router as admin_users_router
from routes.admin_cards import router as admin_cards_router
from routes.admin_products import router as admin_products_router
from routes.admin_records import router as admin_records_router
from routes.admin_feedbacks import router as admin_feedbacks_router
from routes.admin_config import router as admin_config_router

app.include_router(users_router)
app.include_router(tokens_router)
app.include_router(process_router)
app.include_router(feedbacks_router)
app.include_router(admin_router)
app.include_router(admin_users_router)
app.include_router(admin_cards_router)
app.include_router(admin_products_router)
app.include_router(admin_records_router)
app.include_router(admin_feedbacks_router)
app.include_router(admin_config_router)

@app.get("/health")
def health_check():
    return {"status": "healthy"}

@app.get("/")
def root():
    return {
        "message": "AIReduce API 服务正在运行",
        "version": "1.0.0",
        "docs": "/docs"
    }

if __name__ == "__main__":
    import uvicorn
    host = os.getenv("APP_HOST", "0.0.0.0")
    port = int(os.getenv("APP_PORT", 8000))
    uvicorn.run(app, host=host, port=port)