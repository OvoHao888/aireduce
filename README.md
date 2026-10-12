# AI降重系统

🔧 **安全、高效的文本降重工具**

## ✨ 功能特性

### 🎯 双模式降重
- **🚀 快速降重**：基于词汇替换策略，适合初稿处理
- **🎯 深度降重**：多阶段深度重构，适合高标准场景

### 🔒 安全性
- 多层安全防护
- 实时威胁检测
- 自动安全响应
- API密钥本地存储，不上传服务器

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

### 输入验证
- 文本长度限制：10-50000字符
- HTML标签清理
- NULL字节过滤
- 特殊字符转义

### 提示词注入防护
自动检测恶意指令：
- "ignore previous instructions"
- "you are now a different AI"
- `<script>alert('xss')</script>`
- 等20+种恶意模式

### 速率限制
- 每分钟60次请求限制
- 客户端IP级别跟踪
- 自动清理过期记录

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

## 🙏 致谢

- [Fuck-AIGC](https://github.com/): 提供快速降重提示词
- [AI-Detection-Reduction-Tool](https://github.com/): 提供深度降重提示词

## 反馈

有问题欢迎提 [Issue](https://github.com/OvoHao888/aireduce/issues)。

---

**🔧 AI降重系统 - 让文本更具原创性**
