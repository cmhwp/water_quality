"""
用户服务层
"""
from typing import Optional
from datetime import datetime
from sqlalchemy.orm import Session
from sqlalchemy import or_
from app.models.user import User
from app.schemas.user import UserCreate, UserUpdate
from app.core.security import get_password_hash, verify_password, create_access_token, blacklist_token
from config import settings


class UserService:
    """用户服务"""
    
    def __init__(self, db: Session):
        self.db = db
    
    def get_user_by_id(self, user_id: int) -> Optional[User]:
        """根据ID获取用户"""
        return self.db.query(User).filter(User.id == user_id).first()
    
    def get_user_by_email(self, email: str) -> Optional[User]:
        """根据邮箱获取用户"""
        return self.db.query(User).filter(User.email == email).first()
    
    def get_user_by_username(self, username: str) -> Optional[User]:
        """根据用户名获取用户"""
        return self.db.query(User).filter(User.username == username).first()
    
    def get_user_by_username_or_email(self, username_or_email: str) -> Optional[User]:
        """根据用户名或邮箱获取用户"""
        return self.db.query(User).filter(
            or_(User.username == username_or_email, User.email == username_or_email)
        ).first()
    
    def create_user(self, user_data: UserCreate) -> User:
        """创建用户"""
        # 检查邮箱是否已存在
        if self.get_user_by_email(user_data.email):
            raise ValueError("邮箱已存在")
        
        # 检查用户名是否已存在
        if self.get_user_by_username(user_data.username):
            raise ValueError("用户名已存在")
        
        # 创建用户
        hashed_password = get_password_hash(user_data.password)
        db_user = User(
            email=user_data.email,
            username=user_data.username,
            hashed_password=hashed_password,
            full_name=user_data.full_name,
            is_active=user_data.is_active,
            is_admin=user_data.is_admin
        )
        
        self.db.add(db_user)
        self.db.commit()
        self.db.refresh(db_user)
        return db_user
    
    def update_user(self, user_id: int, user_data: UserUpdate) -> Optional[User]:
        """更新用户"""
        db_user = self.get_user_by_id(user_id)
        if not db_user:
            return None
        
        # 检查邮箱是否已被其他用户使用
        if user_data.email and user_data.email != db_user.email:
            existing_user = self.get_user_by_email(user_data.email)
            if existing_user and existing_user.id != user_id:
                raise ValueError("邮箱已被其他用户使用")
        
        # 检查用户名是否已被其他用户使用
        if user_data.username and user_data.username != db_user.username:
            existing_user = self.get_user_by_username(user_data.username)
            if existing_user and existing_user.id != user_id:
                raise ValueError("用户名已被其他用户使用")
        
        # 更新数据
        update_data = user_data.dict(exclude_unset=True)
        if 'password' in update_data:
            update_data['hashed_password'] = get_password_hash(update_data.pop('password'))
        
        for key, value in update_data.items():
            setattr(db_user, key, value)
        
        db_user.updated_at = datetime.now()
        self.db.commit()
        self.db.refresh(db_user)
        return db_user
    
    def authenticate_user(self, username_or_email: str, password: str) -> Optional[User]:
        """认证用户"""
        user = self.get_user_by_username_or_email(username_or_email)
        if not user:
            return None
        
        if not verify_password(password, user.hashed_password):
            return None
        
        # 更新最后登录时间
        user.last_login = datetime.now()
        self.db.commit()
        
        return user
    
    def create_access_token_for_user(self, user: User) -> str:
        """为用户创建访问令牌"""
        token_data = {"sub": str(user.id), "username": user.username}
        return create_access_token(token_data)
    
    def logout_user(self, token: str) -> bool:
        """用户退出登录"""
        try:
            # 将token加入黑名单
            blacklist_token(token)
            return True
        except Exception as e:
            print(f"退出登录失败: {e}")
            return False
    
    def delete_user(self, user_id: int) -> bool:
        """删除用户"""
        db_user = self.get_user_by_id(user_id)
        if not db_user:
            return False
        
        self.db.delete(db_user)
        self.db.commit()
        return True
    
    def get_user_list(self, skip: int = 0, limit: int = 100) -> list[User]:
        """获取用户列表"""
        return self.db.query(User).offset(skip).limit(limit).all()
    
    def get_user_count(self) -> int:
        """获取用户总数"""
        return self.db.query(User).count() 