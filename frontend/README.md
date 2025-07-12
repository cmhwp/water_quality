# 水质数据管理系统 - 前端

基于 Vue 3 + TypeScript + Vite + DaisyUI 的现代化水质数据管理系统前端应用。

## 功能特性

- **用户界面**: 普通用户可以查看数据可视化大屏（开发中）
- **管理员登录**: 管理员可以登录进入数据管理界面
- **数据管理**: 完整的水质数据 CRUD 操作
- **权限控制**: 基于角色的访问控制
- **响应式设计**: 移动端友好的界面设计
- **实时数据**: 通过 API 获取实时水质数据

## 技术栈

- **Vue 3**: 渐进式JavaScript框架
- **TypeScript**: 类型安全的JavaScript超集
- **Vite**: 快速的前端构建工具
- **Vue Router**: 官方路由管理器
- **Pinia**: 状态管理库
- **Axios**: HTTP客户端
- **TailwindCSS**: 实用优先的CSS框架
- **DaisyUI**: 基于TailwindCSS的UI组件库

## 快速开始

### 环境要求

- Node.js 18+
- npm 或 yarn

### 安装依赖

```bash
npm install
```

### 配置API

确保后端服务运行在 `http://localhost:8000`，如果不是，请修改 `src/utils/request.ts` 中的 `API_BASE_URL`。

### 生成API服务

```bash
npm run openapi
```

### 启动开发服务器

```bash
npm run dev
```

应用将在 `http://localhost:5173` 上启动。

### 构建生产版本

```bash
npm run build
```

### 预览生产版本

```bash
npm run preview
```

## 项目结构

```
frontend/
├── public/                 # 静态资源
├── src/
│   ├── assets/            # 样式和资源文件
│   ├── components/        # 可复用组件
│   ├── router/            # 路由配置
│   ├── services/          # API服务（自动生成）
│   ├── stores/            # 状态管理
│   ├── utils/             # 工具函数
│   ├── views/             # 页面组件
│   │   ├── admin/         # 管理员页面
│   │   ├── Home.vue       # 首页
│   │   └── NotFound.vue   # 404页面
│   ├── App.vue            # 根组件
│   └── main.ts            # 入口文件
├── tailwind.config.js     # TailwindCSS配置
├── vite.config.ts         # Vite配置
└── package.json
```

## 路由说明

- `/` - 首页（数据可视化大屏）
- `/admin/login` - 管理员登录页面
- `/admin/dashboard` - 管理员数据管理页面
- `/admin` - 重定向到管理员面板

## 权限控制

- **普通用户**: 可以访问首页查看数据可视化
- **管理员**: 需要登录后才能访问数据管理功能

默认管理员账户：
- 邮箱: `admin@waterquality.com`
- 密码: `admin123`

## API集成

本项目使用 `@umijs/openapi` 自动生成前端API服务：

1. 配置文件: `openapi.config.js`
2. 生成命令: `npm run openapi`
3. 生成的服务位于: `src/services/api/`

## 状态管理

使用 Pinia 进行状态管理：

- `useAuthStore`: 用户认证状态管理
  - 登录/登出
  - 用户信息
  - 权限检查

## 样式系统

- **TailwindCSS**: 提供原子化CSS类
- **DaisyUI**: 提供预设计的组件
- **自定义主题**: 在 `tailwind.config.js` 中配置

## 开发指南

### 添加新页面

1. 在 `src/views/` 中创建Vue组件
2. 在 `src/router/index.ts` 中添加路由
3. 如需权限控制，在路由meta中添加相应配置

### 添加新的API服务

1. 确保后端API已更新
2. 运行 `npm run openapi` 重新生成API服务
3. 在组件中导入并使用新的API方法

### 样式开发

- 优先使用 TailwindCSS 类
- 使用 DaisyUI 组件提高开发效率
- 在 `tailwind.config.js` 中自定义主题

## 部署说明

### 构建优化

```bash
npm run build
```

### 部署到静态服务器

构建完成后，`dist/` 目录包含所有静态文件，可以部署到任何静态服务器。

### 环境变量

在 `.env` 文件中配置环境变量：

```env
VITE_API_BASE_URL=http://localhost:8000/api/v1
```

## 常见问题

### Q: API请求失败怎么办？

A: 检查：
1. 后端服务是否运行
2. API地址是否正确
3. 网络连接是否正常
4. 认证token是否有效

### Q: 样式不生效怎么办？

A: 检查：
1. TailwindCSS是否正确安装
2. 样式类名是否正确
3. 是否需要重启开发服务器

### Q: 路由不工作怎么办？

A: 检查：
1. 路由配置是否正确
2. 组件是否正确导入
3. 权限检查是否通过

## 贡献指南

1. Fork 项目
2. 创建特性分支
3. 提交更改
4. 推送到分支
5. 创建 Pull Request

## 许可证

MIT License
