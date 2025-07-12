# Git 忽略文件说明

本项目包含了三个 `.gitignore` 文件，分别针对不同的目录和用途：

## 📂 文件结构

```
water_quality/
├── .gitignore                 # 项目根目录 - 通用忽略规则
├── backend/.gitignore         # 后端目录 - Python/FastAPI 专用
├── frontend/.gitignore        # 前端目录 - 前端框架专用
└── GITIGNORE.md              # 本说明文件
```

## 🔧 各文件作用

### 1. 根目录 `.gitignore`
- **位置**: `/.gitignore`
- **作用**: 整个项目的通用忽略规则
- **包含内容**:
  - 编辑器和IDE配置文件
  - 操作系统生成的文件
  - 通用的临时文件和日志文件
  - 环境变量文件
  - 证书文件
  - 备份文件

### 2. 后端 `.gitignore`
- **位置**: `/backend/.gitignore`
- **作用**: Python/FastAPI 项目专用忽略规则
- **包含内容**:
  - Python 字节码文件 (`__pycache__/`, `*.pyc`)
  - 虚拟环境目录 (`venv/`, `env/`)
  - Python 包构建文件 (`*.egg-info/`, `dist/`)
  - 数据库文件 (`*.db`, `*.sqlite3`)
  - FastAPI 相关文件
  - 测试覆盖率报告
  - 日志文件
  - 配置文件
  - Docker 和部署相关文件

### 3. 前端 `.gitignore`
- **位置**: `/frontend/.gitignore`
- **作用**: 前端项目专用忽略规则
- **包含内容**:
  - Node.js 依赖 (`node_modules/`)
  - 构建输出 (`dist/`, `build/`)
  - 缓存文件 (`.cache/`, `.parcel-cache`)
  - 各种前端框架的构建文件
  - TypeScript 编译缓存
  - 测试覆盖率报告
  - 环境变量文件
  - 锁定文件（可选忽略）

## 🎯 设计原则

### 1. 层次化管理
- 根目录处理通用文件
- 子目录处理特定技术栈的文件
- 避免重复和冲突

### 2. 安全优先
- 忽略所有可能包含敏感信息的文件
- 环境变量文件 (`.env*`)
- 配置文件 (`config.local.*`)
- 证书文件 (`*.key`, `*.pem`)

### 3. 开发效率
- 忽略IDE和编辑器生成的文件
- 忽略操作系统特定文件
- 忽略构建和缓存文件

## 📋 重要文件说明

### 🔒 必须忽略的文件
```
.env*                          # 环境变量文件
*.key                          # 私钥文件
*.pem                          # 证书文件
config.local.*                 # 本地配置文件
water_quality.db               # 项目数据库文件
```

### 📦 构建相关文件
```
__pycache__/                   # Python 字节码
node_modules/                  # Node.js 依赖
dist/                          # 构建输出
build/                         # 构建目录
*.egg-info/                    # Python 包信息
```

### 🖥️ 开发工具文件
```
.vscode/                       # VS Code 配置
.idea/                         # PyCharm/IntelliJ 配置
.DS_Store                      # macOS 系统文件
Thumbs.db                      # Windows 缩略图
```

## 🚀 使用建议

### 1. 新成员加入项目时
- 确保复制 `.env.example` 到 `.env` 并配置
- 不要提交包含真实密钥的配置文件

### 2. 添加新的文件类型时
- 在相应的 `.gitignore` 中添加规则
- 考虑是否需要在根目录也添加通用规则

### 3. 特殊情况处理
- 如果需要提交某些通常被忽略的文件，使用 `git add -f` 强制添加
- 对于大型数据文件，考虑使用 Git LFS

## 🔄 维护和更新

### 定期检查
- 确保新的构建工具和依赖被正确忽略
- 更新对应的框架和工具的忽略规则
- 关注社区最佳实践

### 版本控制
- 忽略规则的更改也需要版本控制
- 重要更改要在提交信息中说明

## 📚 参考资源

- [GitHub 官方 .gitignore 模板](https://github.com/github/gitignore)
- [Python .gitignore 模板](https://github.com/github/gitignore/blob/main/Python.gitignore)
- [Node.js .gitignore 模板](https://github.com/github/gitignore/blob/main/Node.gitignore)
- [Git 忽略文件文档](https://git-scm.com/docs/gitignore) 