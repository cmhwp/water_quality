"""
认证API路由
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.db.base import get_db
from app.schemas.user import UserLogin, Token, UserResponse
from app.services.user_service import UserService
from app.core.deps import get_current_user, get_token
from config import settings

router = APIRouter()


@router.post("/login", response_model=Token, summary="用户登录")
def login(
    user_login: UserLogin,
    db: Session = Depends(get_db)
):
    """用户登录"""
    user_service = UserService(db)
    
    # 认证用户
    user = user_service.authenticate_user(user_login.username, user_login.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="用户名或密码错误"
        )
    
    # 检查用户状态
    if not user.is_active:  # type: ignore
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="用户已被禁用"
        )
    
    # 生成访问令牌
    access_token = user_service.create_access_token_for_user(user)
    
    return Token(
        access_token=access_token,
        token_type="bearer",
        expires_in=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60,
        user=UserResponse.from_orm(user)
    )


@router.post("/logout", summary="用户退出登录")
def logout(
    token: str = Depends(get_token),
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """用户退出登录"""
    user_service = UserService(db)
    
    # 将token加入黑名单
    success = user_service.logout_user(token)
    
    if not success:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="退出登录失败"
        )
    
    return {"message": "退出登录成功"}


@router.get("/me", response_model=UserResponse, summary="获取当前用户信息")
def get_current_user_info(
    current_user = Depends(get_current_user)
):
    """获取当前用户信息"""
    return UserResponse.from_orm(current_user)


@router.post("/refresh", response_model=Token, summary="刷新令牌")
def refresh_token(
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """刷新令牌"""
    user_service = UserService(db)
    
    # 生成新的访问令牌
    access_token = user_service.create_access_token_for_user(current_user)
    
    return Token(
        access_token=access_token,
        token_type="bearer",
        expires_in=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60,
        user=UserResponse.from_orm(current_user)
    ) 