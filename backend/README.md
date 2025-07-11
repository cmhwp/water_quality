# 水质数据管理系统后端

这是一个基于FastAPI的企业级水质数据管理系统后端，提供完整的CRUD操作和RESTful API接口。

## 功能特性

- **水质数据管理**: 完整的增删改查操作
- **用户认证**: JWT token认证，支持管理员权限控制
- **数据验证**: 完善的请求参数验证和错误处理
- **数据统计**: 提供水质数据的统计分析接口
- **API文档**: 自动生成的OpenAPI/Swagger文档
- **日志记录**: 完整的请求日志和错误日志
- **数据库支持**: 基于SQLAlchemy的ORM，支持SQLite

## 技术栈

- **FastAPI**: 现代化的Python Web框架
- **SQLAlchemy**: Python ORM框架
- **Pydantic**: 数据验证和序列化
- **JWT**: 用户认证和授权
- **SQLite**: 轻量级数据库
- **Uvicorn**: ASGI服务器

## 项目结构

```
backend/
├── app/
│   ├── api/
│   │   └── v1/
│   │       ├── auth.py          # 认证API
│   │       ├── water_quality.py # 水质数据API
│   │       └── api.py          # API路由整合
│   ├── core/
│   │   ├── security.py         # 安全模块
│   │   └── deps.py            # 依赖注入
│   ├── models/
│   │   ├── water_quality.py    # 水质数据模型
│   │   └── user.py            # 用户模型
│   ├── schemas/
│   │   ├── water_quality.py    # 水质数据模式
│   │   └── user.py            # 用户模式
│   ├── services/
│   │   ├── water_quality_service.py # 水质数据服务
│   │   └── user_service.py         # 用户服务
│   ├── utils/
│   │   └── common.py          # 通用工具
│   └── db/
│       └── base.py           # 数据库配置
├── scripts/
│   └── import_data.py        # 数据导入脚本
├── main.py                   # 主应用文件
├── config.py                 # 配置文件
├── requirements.txt          # 依赖包
└── README.md                # 项目说明
```

## 安装和运行

### 1. 安装依赖

```bash
pip install -r requirements.txt
```

### 2. 导入数据

```bash
python scripts/import_data.py
```

这会创建数据库表、导入Excel数据，并创建默认管理员用户：
- 邮箱: admin@waterquality.com
- 密码: admin123

### 3. 启动服务

使用便捷启动脚本（推荐）：

```bash
python start_server.py
```

或者直接运行：

```bash
python main.py
```

或者使用uvicorn:

```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### 4. 访问API文档

- Swagger UI: http://localhost:8000/api/v1/docs
- ReDoc: http://localhost:8000/api/v1/redoc

## API接口

### 认证接口

- `POST /api/v1/auth/login` - 用户登录
- `GET /api/v1/auth/me` - 获取当前用户信息
- `POST /api/v1/auth/refresh` - 刷新令牌

### 水质数据接口

- `GET /api/v1/water-quality/` - 获取水质数据列表
- `GET /api/v1/water-quality/{id}` - 获取单个水质数据
- `POST /api/v1/water-quality/` - 创建水质数据（管理员）
- `PUT /api/v1/water-quality/{id}` - 更新水质数据（管理员）
- `DELETE /api/v1/water-quality/{id}` - 删除水质数据（管理员）
- `GET /api/v1/water-quality/statistics/overview` - 获取统计数据
- `GET /api/v1/water-quality/options/rivers` - 获取河道列表
- `GET /api/v1/water-quality/options/quality-levels` - 获取水质等级列表

### 查询参数

水质数据列表接口支持以下查询参数：

- `page`: 页码（默认1）
- `per_page`: 每页数量（默认20，最大100）
- `river_name`: 河道名称（模糊搜索）
- `code`: 编号（模糊搜索）
- `comprehensive_quality_level`: 综合水质等级
- `sampling_date_start`: 取样开始日期
- `sampling_date_end`: 取样结束日期

## 数据格式

### 水质数据字段

- `id`: 数据ID
- `sampling_date`: 取样日期
- `sampling_time`: 取样时间
- `detection_date`: 检测日期
- `code`: 编号
- `river_name`: 河道名称
- `method`: 方式
- `cod_value`: COD数值
- `cod_level`: COD等级
- `ammonia_nitrogen_value`: 氨氮数值
- `ammonia_nitrogen_level`: 氨氮等级
- `total_phosphorus_value`: 总磷数值
- `total_phosphorus_level`: 总磷等级
- `potassium_permanganate_value`: 高锰酸钾数值
- `potassium_permanganate_level`: 高锰酸钾等级
- `comprehensive_quality_level`: 综合水质等级
- `comprehensive_level_number`: 综合等级数
- `created_at`: 创建时间
- `updated_at`: 更新时间
- `remarks`: 备注

## 认证方式

API使用JWT Bearer Token认证。获取token后，在请求头中添加：

```
Authorization: Bearer {your_token}
```

## 错误处理

所有API响应都采用统一的错误格式：

```json
{
    "success": false,
    "message": "错误信息",
    "error_code": 400,
    "errors": [] // 详细错误信息（可选）
}
```

## 配置说明

主要配置项在 `config.py` 中：

- `DATABASE_URL`: 数据库连接字符串
- `SECRET_KEY`: JWT密钥
- `ACCESS_TOKEN_EXPIRE_MINUTES`: Token过期时间
- `ADMIN_EMAIL`: 默认管理员邮箱
- `ADMIN_PASSWORD`: 默认管理员密码

## 部署建议

1. 更改默认密钥和管理员密码
2. 使用生产级数据库（PostgreSQL/MySQL）
3. 配置反向代理（Nginx）
4. 启用HTTPS
5. 设置合适的日志级别
6. 配置监控和备份

## 开发说明

### 添加新功能

1. 在 `models/` 中定义数据模型
2. 在 `schemas/` 中定义数据模式
3. 在 `services/` 中实现业务逻辑
4. 在 `api/v1/` 中定义API路由
5. 在 `api/v1/api.py` 中注册路由

### 测试

```bash
# 安装测试依赖
pip install pytest pytest-asyncio httpx

# 运行测试
pytest
```

## 许可证

MIT License 