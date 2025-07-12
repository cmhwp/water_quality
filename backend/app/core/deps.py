"""
依赖注入模块
"""
from typing import Optional
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from app.db.base import get_db
from app.core.security import verify_token, create_credentials_exception
from app.models.user import User
from app.schemas.user import TokenData

# HTTP Bearer 认证方案
security = HTTPBearer()


def get_token(
    credentials: HTTPAuthorizationCredentials = Depends(security)
) -> str:
    """获取原始token字符串"""
    return credentials.credentials


def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
) -> User:
    """获取当前用户"""
    token = credentials.credentials
    payload = verify_token(token)
    
    if payload is None:
        raise create_credentials_exception()
    
    user_id: Optional[int] = payload.get("sub")
    if user_id is None:
        raise create_credentials_exception()
    
    try:
        user_id = int(user_id)
    except ValueError:
        raise create_credentials_exception()
    
    user = db.query(User).filter(User.id == user_id).first()
    if user is None:
        raise create_credentials_exception("User not found")
    
    if not user.is_active:  # type: ignore
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Inactive user"
        )
    
    return user


def get_current_active_user(
    current_user: User = Depends(get_current_user),
) -> User:
    """获取当前活跃用户"""
    if not current_user.is_active:  # type: ignore
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Inactive user"
        )
    return current_user


def get_current_admin_user(
    current_user: User = Depends(get_current_active_user),
) -> User:
    """获取当前管理员用户"""
    if not current_user.is_admin:  # type: ignore
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions"
        )
    return current_user


def get_optional_current_user(
    credentials: Optional[HTTPAuthorizationCredentials] = Depends(security),
    db: Session = Depends(get_db)
) -> Optional[User]:
    """获取可选的当前用户（用于公开API）"""
    if not credentials:
        return None
    
    try:
        return get_current_user(credentials, db)
    except HTTPException:
        return None 