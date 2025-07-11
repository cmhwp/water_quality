"""
用户认证模型
"""
from datetime import datetime
from sqlalchemy import Column, Integer, String, Boolean, DateTime
from sqlalchemy.sql import func

from app.db.base import Base


class User(Base):
    """用户模型"""
    
    __tablename__ = "users"
    
    # 主键
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    
    # 用户信息
    email = Column(String(100), unique=True, index=True, nullable=False, comment="邮箱")
    username = Column(String(50), unique=True, index=True, nullable=False, comment="用户名")
    hashed_password = Column(String(255), nullable=False, comment="加密密码")
    full_name = Column(String(100), nullable=True, comment="全名")
    
    # 权限
    is_active = Column(Boolean, default=True, comment="是否激活")
    is_admin = Column(Boolean, default=False, comment="是否管理员")
    
    # 系统字段
    created_at = Column(DateTime, default=func.now(), comment="创建时间")
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now(), comment="更新时间")
    last_login = Column(DateTime, nullable=True, comment="最后登录时间")
    
    def __repr__(self):
        return f"<User(id={self.id}, email='{self.email}', username='{self.username}')>" 