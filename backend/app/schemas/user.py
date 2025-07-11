"""
用户认证模式
"""
from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field, validator
from pydantic import EmailStr


class UserBase(BaseModel):
    """用户基础模式"""
    
    email: EmailStr = Field(..., description="邮箱")
    username: str = Field(..., min_length=3, max_length=50, description="用户名")
    full_name: Optional[str] = Field(None, description="全名")
    is_active: bool = Field(True, description="是否激活")
    is_admin: bool = Field(False, description="是否管理员")


class UserCreate(UserBase):
    """创建用户模式"""
    
    password: str = Field(..., min_length=6, description="密码")
    
    @validator('password')
    def validate_password(cls, v):
        """验证密码强度"""
        if len(v) < 6:
            raise ValueError('密码长度至少6位')
        return v


class UserUpdate(BaseModel):
    """更新用户模式"""
    
    email: Optional[EmailStr] = Field(None, description="邮箱")
    username: Optional[str] = Field(None, min_length=3, max_length=50, description="用户名")
    full_name: Optional[str] = Field(None, description="全名")
    is_active: Optional[bool] = Field(None, description="是否激活")
    is_admin: Optional[bool] = Field(None, description="是否管理员")
    password: Optional[str] = Field(None, min_length=6, description="密码")


class UserResponse(UserBase):
    """用户响应模式"""
    
    id: int = Field(..., description="用户ID")
    created_at: datetime = Field(..., description="创建时间")
    updated_at: datetime = Field(..., description="更新时间")
    last_login: Optional[datetime] = Field(None, description="最后登录时间")
    
    class Config:
        from_attributes = True


class UserLogin(BaseModel):
    """用户登录模式"""
    
    username: str = Field(..., description="用户名或邮箱")
    password: str = Field(..., description="密码")


class Token(BaseModel):
    """令牌模式"""
    
    access_token: str = Field(..., description="访问令牌")
    token_type: str = Field(default="bearer", description="令牌类型")
    expires_in: int = Field(..., description="过期时间（秒）")
    user: UserResponse = Field(..., description="用户信息")


class TokenData(BaseModel):
    """令牌数据模式"""
    
    user_id: Optional[int] = Field(None, description="用户ID")
    username: Optional[str] = Field(None, description="用户名") 