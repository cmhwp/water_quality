"""
水质数据管理系统 - 主应用文件
"""
from fastapi import FastAPI, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from pydantic import ValidationError
import logging
import time
from config import settings
from app.api.v1.api import api_router

# 配置日志
logging.basicConfig(
    level=getattr(logging, settings.LOG_LEVEL),
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

# 创建FastAPI应用实例
app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.PROJECT_VERSION,
    description=settings.DESCRIPTION,
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    docs_url=f"{settings.API_V1_STR}/docs",
    redoc_url=f"{settings.API_V1_STR}/redoc",
)

# 添加CORS中间件
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.BACKEND_CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# 全局异常处理器
@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    """HTTP异常处理器"""
    logger.error(f"HTTP异常: {exc.status_code} - {exc.detail}")
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "success": False,
            "message": exc.detail,
            "error_code": exc.status_code
        }
    )


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    """请求验证异常处理器"""
    logger.error(f"请求验证错误: {exc.errors()}")
    return JSONResponse(
        status_code=422,
        content={
            "success": False,
            "message": "请求参数验证失败",
            "error_code": 422,
            "errors": exc.errors()
        }
    )


@app.exception_handler(ValidationError)
async def pydantic_validation_exception_handler(request: Request, exc: ValidationError):
    """Pydantic验证异常处理器"""
    logger.error(f"数据验证错误: {exc.errors()}")
    return JSONResponse(
        status_code=422,
        content={
            "success": False,
            "message": "数据验证失败",
            "error_code": 422,
            "errors": exc.errors()
        }
    )


@app.exception_handler(ValueError)
async def value_error_handler(request: Request, exc: ValueError):
    """值错误处理器"""
    logger.error(f"值错误: {str(exc)}")
    return JSONResponse(
        status_code=400,
        content={
            "success": False,
            "message": str(exc),
            "error_code": 400
        }
    )


@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception):
    """通用异常处理器"""
    logger.error(f"未处理的异常: {type(exc).__name__} - {str(exc)}")
    return JSONResponse(
        status_code=500,
        content={
            "success": False,
            "message": "服务器内部错误",
            "error_code": 500
        }
    )


# 添加请求日志中间件
@app.middleware("http")
async def log_requests(request: Request, call_next):
    """记录请求日志"""
    start_time = time.time()
    
    # 记录请求信息
    logger.info(f"请求开始: {request.method} {request.url}")
    
    try:
        response = await call_next(request)
        
        # 记录响应信息
        process_time = time.time() - start_time
        logger.info(f"请求完成: {request.method} {request.url} - {response.status_code} - {process_time:.4f}s")
        
        return response
    except Exception as e:
        process_time = time.time() - start_time
        logger.error(f"请求失败: {request.method} {request.url} - {str(e)} - {process_time:.4f}s")
        raise


# 健康检查端点
@app.get("/health", summary="健康检查")
async def health_check():
    """健康检查端点"""
    return {
        "status": "ok",
        "service": settings.PROJECT_NAME,
        "version": settings.PROJECT_VERSION,
        "environment": "development" if settings.DEBUG else "production"
    }


# 根路径
@app.get("/", summary="根路径")
async def root():
    """根路径"""
    return {
        "message": f"欢迎使用{settings.PROJECT_NAME}",
        "version": settings.PROJECT_VERSION,
        "docs_url": f"{settings.API_V1_STR}/docs",
        "redoc_url": f"{settings.API_V1_STR}/redoc"
    }


# 包含API路由
app.include_router(api_router, prefix=settings.API_V1_STR)


if __name__ == "__main__":
    import uvicorn
    import time
    
    logger.info(f"启动{settings.PROJECT_NAME} v{settings.PROJECT_VERSION}")
    
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.DEBUG,
        log_level=settings.LOG_LEVEL.lower()
    ) 