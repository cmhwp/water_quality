"""
安全和认证核心模块
"""
from datetime import datetime, timedelta
from typing import Optional, Union, Set
from jose import JWTError, jwt
from passlib.context import CryptContext
from fastapi import HTTPException, status
from config import settings

# 密码加密上下文
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Token黑名单 (在生产环境中应该使用Redis等持久化存储)
blacklisted_tokens: Set[str] = set()


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """验证密码"""
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    """生成密码哈希"""
    return pwd_context.hash(password)


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """创建访问令牌"""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now() + expires_delta
    else:
        expire = datetime.now() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt


def verify_token(token: str) -> Union[dict, None]:
    """验证令牌"""
    try:
        # 检查token是否在黑名单中
        if is_token_blacklisted(token):
            return None
            
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        return payload
    except JWTError:
        return None


def blacklist_token(token: str) -> None:
    """将token加入黑名单"""
    blacklisted_tokens.add(token)


def is_token_blacklisted(token: str) -> bool:
    """检查token是否在黑名单中"""
    return token in blacklisted_tokens


def clean_expired_tokens() -> None:
    """清理过期的token（定期调用以节省内存）"""
    expired_tokens = []
    for token in blacklisted_tokens:
        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
            # 如果token已过期，添加到待删除列表
            if datetime.fromtimestamp(payload['exp']) < datetime.now():
                expired_tokens.append(token)
        except JWTError:
            # 如果解码失败，也认为是无效token，可以清理
            expired_tokens.append(token)
    
    # 从黑名单中移除过期的token
    for token in expired_tokens:
        blacklisted_tokens.discard(token)


def get_token_from_payload(payload: dict) -> Optional[str]:
    """从payload中提取关键信息用于黑名单识别"""
    # 这个函数用于从请求中的token提取标识信息
    return None  # 在实际使用中，我们直接使用完整的token


def create_credentials_exception(detail: str = "Could not validate credentials") -> HTTPException:
    """创建认证异常"""
    return HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail=detail,
        headers={"WWW-Authenticate": "Bearer"},
    ) 