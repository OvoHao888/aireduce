# 讯文 · AI 文本润色平台

> **开发周期：2026.05 – 2026.06** ｜ 2026.10 整理开源
>
> 2026 年 10 月整理时做了一轮排查与加固：把鉴权模块接入请求链路，
> 并修复深度模式偶发输出英文的问题（约 25% 概率）。

🔧 **安全、高效的文本降重工具**

## ✨ 功能特性

### 🎯 双模式降重
- **🚀 快速降重**：基于词汇替换策略，适合初稿处理
- **🎯 深度降重**：多阶段深度重构，适合高标准场景

### 🔒 安全性
- 口令 bcrypt 哈希存储
- 提示词注入实时检测（12 类模式，命中即拒）
- 接口级速率限制（处理接口 60 次/分，登录接口 10 次/分）
- 安全事件写入日志，便于审计

### 🎨 精美UI
- 毛细玻璃效果
- 动态粒子背景
- 暖色调配色
- 流畅动画过渡

### 👤 用户功能
- 个人中心管理
- 密卡购买与兑换
- 使用记录追踪
- VIP特权系统

## 🚀 快速开始

### 前置准备

**① 数据库**（必需）—— 创建库并导入表结构：

```bash
mysql -u root -p < backend/init.sql
```

脚本会创建 `aireduce_db` 与全部表，并写入演示数据。

**② 配置文件** —— 复制 `backend/.env.example` 为 `backend/.env`，至少填写三项：

| 变量 | 说明 |
|---|---|
| `DB_PASSWORD` | 本机 MySQL 的 root 口令 |
| `SECRET_KEY` | 随机字符串，**至少 32 位**（`openssl rand -hex 32` 可生成） |
| `API_KEY` | 大模型 API Key（也可启动后在管理后台的「API配置」页填写） |

> 下面的启动脚本会自动检查这两步；未完成时会打印提示并退出，
> 而不是启动一个连不上数据库的后端。

### 方式1：使用启动脚本（推荐）

**Windows用户**：双击 `启动系统.bat`

**Linux/macOS用户**：
```bash
chmod +x 启动系统.sh
./启动系统.sh
```

### 方式2：手动启动

#### 后端启动
```bash
# 进入后端目录
cd backend

# 创建虚拟环境（首次）
python -m venv venv

# 激活虚拟环境
# Windows:
venv\Scripts\activate
# Linux/macOS:
source venv/bin/activate

# 安装依赖
pip install -r requirements.txt

# 启动服务
python main.py
```

#### 前端启动
```bash
# 进入前端目录
cd AIReduce

# 安装依赖
npm install

# 启动开发服务器
npm run dev
```

## 📝 使用指南

### 1. 配置API
首次使用时，需要在界面中配置您的API密钥：
- 点击"API配置"
- 输入API密钥
- 选择AI模型（推荐：DeepSeek R1）

### 2. 选择模式
- **快速降重**：适合日常降重，速度快
- **深度降重**：适合高标准场景，效果更好

### 3. 输入文本
在左侧文本框中输入需要降重的文本

### 4. 开始处理
点击"开始处理"按钮，等待处理完成

### 5. 查看结果
处理完成后，在右侧查看降重结果

### 6. 复制/下载
- 点击"复制结果"复制到剪贴板
- 点击"下载文本"保存为文件

## 📂 项目结构

```
aigc/
├── AIReduce/                 # Vue3 前端
│   ├── src/
│   │   ├── views/            # 页面组件
│   │   │   ├── Home.vue      # 工作台
│   │   │   ├── PersonalCenter.vue  # 个人中心
│   │   │   ├── TokenCard.vue       # 密卡中心
│   │   │   └── UsageRecords.vue    # 使用记录
│   │   ├── components/       # 公共组件
│   │   │   ├── ParticleBackground.vue  # 粒子背景
│   │   │   ├── GlassCard.vue         # 玻璃卡片
│   │   │   └── AppHeader.vue         # 顶部导航
│   │   ├── router/           # 路由配置
│   │   └── styles/           # 样式文件
│   └── package.json
│
├── backend/                  # Python 后端
│   ├── main.py              # FastAPI主应用
│   ├── config.py            # 配置文件
│   ├── prompts.py           # 提示词管理
│   ├── security.py           # 安全验证
│   ├── processor.py         # AI处理器
│   └── requirements.txt     # Python依赖
│
├── 启动系统.bat             # Windows启动脚本
├── 启动系统.sh              # Linux/macOS启动脚本
└── README.md                # 项目文档
```

## 🔧 技术栈

### 前端
- **Vue 3**: 渐进式JavaScript框架
- **Vue Router 4**: Vue.js官方路由管理器
- **Vite**: 下一代前端构建工具
- **CSS3**: 高级样式特性

### 后端
- **FastAPI**: 现代Python Web框架
- **Uvicorn**: ASGI服务器
- **Pydantic**: 数据验证
- **OpenAI SDK**: AI模型接口

## 🎨 UI特性

### 毛细玻璃效果
```css
.glass {
  background: rgba(255, 255, 255, 0.75);
  backdrop-filter: blur(20px);
  border: 1px solid rgba(255, 255, 255, 0.3);
  box-shadow: 0 8px 32px rgba(230, 126, 34, 0.1);
}
```

### 动态粒子背景
- 使用Canvas API绘制
- 暖色调粒子（橙色、金色、珊瑚色）
- 粒子间连线效果
- 自动适配窗口大小

### 暖色调配色
- **主色**：橙色 (#e67e22)
- **辅助色**：金色 (#f39c12)
- **强调色**：珊瑚红 (#e74c3c)
- **背景色**：米色系 (#fdf6e3, #fef9f3, #fff8f0)

## 🔒 安全特性

以下能力都在请求链路上真实生效（`backend/security.py` + `backend/deps.py`），
不是只写在文档里的配置项。

### 口令存储
- 用户口令与管理员口令统一用 **bcrypt**（随机盐 + 成本因子）存储
- 校验使用 bcrypt 的恒定时间比较；兼容历史无盐 SHA-256 哈希以平滑迁移

### 输入验证
- 文本长度 10 – 50000 字符
- 拒绝全空白输入与 NULL 字节
- HTML 清理：移除 `<script>`、内联事件处理器、`javascript:`、`<iframe>`

### 提示词注入防护
命中即拒绝（返回 400 并记录安全事件），覆盖 12 类模式：
- 指令忽略 / 上下文忽略（`ignore previous instructions`、`forget everything`）
- 角色扮演（`you are now …`、`pretend to be …`）
- 提示词覆盖与泄露（`new instructions`、`reveal your system prompt`）
- 脚本注入（`<script`、`javascript:`、`on\w+=`、`<iframe`）

### 速率限制
按客户端地址计数，超限返回 **429** 并带 `Retry-After`：

| 接口 | 限制 |
|---|---|
| `POST /api/process`、`/api/process/stream` | 60 次 / 分钟 |
| `POST /api/users/login`、`POST /api/admin/login` | 10 次 / 分钟（防撞库） |

### 卡密兑换
对卡密行加排他锁（`SELECT … FOR UPDATE`），
保证并发场景下同一张卡只能成功兑换一次。

## 💡 常见问题

### Q: 如何获取API密钥？
A: 推荐使用SiliconFlow或DeepSeek的API服务。

### Q: 处理速度慢怎么办？
A: 可以尝试：
1. 减少输入文本长度
2. 选择"快速降重"模式
3. 使用性能更好的API模型

### Q: 如何购买密卡？
A: 在"密卡中心"页面选择套餐进行购买。

### Q: 如何兑换密卡？
A: 在"密卡中心"页面的"密卡兑换"区域输入密卡码即可。

## 📄 许可证

本项目仅供学习和研究使用。
