# ExcelSync 前端

基于 Next.js、TypeScript 和 Tailwind CSS 构建的现代化 Excel 文件上传分析工具，采用玻璃拟态设计风格，支持深色模式。

## 功能特性

- 🎨 **玻璃拟态设计** - 现代化半透明 UI，带有模糊效果
- 🌙 **深色/浅色模式** - 主题切换，支持系统偏好检测
- 📁 **拖拽上传** - 直观的文件上传界面，支持验证
- ⚡ **实时处理** - 实时进度更新和状态指示器
- 📱 **响应式设计** - 移动端优先的自适应布局
- 🚀 **现代动画** - 由 Framer Motion 驱动的流畅过渡效果
- 📊 **数据预览** - 交互式表格，支持分页和导出
- 🛡️ **类型安全** - 完整的 TypeScript 实现

## 技术栈

- **框架**: Next.js 14 with App Router
- **语言**: TypeScript
- **样式**: Tailwind CSS 自定义玻璃拟态工具类
- **动画**: Framer Motion
- **文件上传**: React Dropzone
- **图标**: Lucide React

## 快速开始

1. **安装依赖**
   ```bash
   npm install
   ```

2. **环境配置**
   ```bash
   cp .env.local.example .env.local
   ```

3. **启动开发服务器**
   ```bash
   npm run dev
   ```

4. **打开浏览器**
   访问 [http://localhost:3000](http://localhost:3000)

## 项目结构

```
src/
├── app/                 # Next.js 应用目录
│   ├── globals.css     # 全局样式和 CSS 变量
│   ├── layout.tsx      # 根布局和主题提供器
│   └── page.tsx        # 主页面
├── components/
│   ├── providers/      # React 上下文提供器
│   └── ui/            # 可复用 UI 组件
├── lib/               # 工具函数和 API 服务
├── types/             # TypeScript 类型定义
└── hooks/             # 自定义 React Hook
```

## API 集成

应用包含真实和模拟 API 服务：

- **开发环境**: 使用模拟 API 进行测试
- **生产环境**: 连接到后端 API `/api/parse-excel`

### API 接口

- `POST /api/parse-excel` - 解析单个 Excel 文件
- `POST /api/parse-multiple-excel` - 解析多个文件
- `GET /api/health` - 健康检查接口

## 自定义配置

### 主题配置

颜色和设计令牌定义在：
- `tailwind.config.ts` - Tailwind 主题扩展
- `globals.css` - 浅色/深色主题的 CSS 自定义属性

### 组件样式

所有组件使用玻璃拟态设计系统：
- `.glass` - 基础玻璃效果
- `.glass-card` - 玻璃风格卡片
- `.gradient-bg` - 动画渐变背景

## 脚本命令

- `npm run dev` - 启动开发服务器
- `npm run build` - 构建生产版本
- `npm run start` - 启动生产服务器
- `npm run lint` - 运行 ESLint
- `npm run type-check` - TypeScript 类型检查

## 浏览器支持

- Chrome/Edge 88+
- Firefox 84+
- Safari 14+

## 贡献指南

1. Fork 仓库
2. 创建功能分支
3. 进行更改
4. 如适用，添加测试
5. 提交 Pull Request