# AI降重系统后端

## 项目简介
这是一个安全的AI文本降重系统后端服务，使用FastAPI构建。

## 功能特性
- ✅ 双模式降重：快速降重 + 深度降重
- ✅ 流式响应：实时显示处理进度
- ✅ 安全防护：速率限制、注入检测、输入验证
- ✅ 支持多种AI模型：DeepSeek、Qwen等

## 快速开始

### 1. 安装依赖
```bash
cd backend
pip install -r requirements.txt
```

### 2. 配置环境
```bash
cp .env.example .env
# 编辑 .env 文件，填入你的API密钥
```

### 3. 启动服务
```bash
python main.py
```

### 4. 访问API文档
打开浏览器访问：http://127.0.0.1:8000/docs

## API端点

- `GET /` - 健康检查
- `GET /api/health` - 详细健康检查
- `GET /api/supported-models` - 获取支持的模型列表
- `POST /api/config` - 保存配置
- `POST /api/process` - 处理文本改写（流式响应）

## 安全特性

### 输入验证
- 文本长度限制：10-50000字符
- HTML标签清理
- 特殊字符过滤

### 提示词注入防护
- 自动检测恶意指令
- 禁止角色扮演尝试
- 移除推理过程标签

### 速率限制
- 每分钟最多60次请求
- 自动清理过期记录
- 客户端级别跟踪

## 项目结构

```
backend/
├── main.py           # 主应用入口
├── config.py         # 配置文件
├── prompts.py        # 提示词管理
├── security.py       # 安全验证模块
├── processor.py      # AI处理器
├── requirements.txt  # 依赖列表
├── .env.example      # 环境变量示例
└── README.md         # 本文件
```

## 使用示例

### Python调用示例
```python
import requests
import json

# 发送处理请求
response = requests.post(
    "http://127.0.0.1:8000/api/process",
    json={
        "text": "你的文本内容",
        "mode": "mode1",  # 或 "mode2"
        "api_key": "your_api_key",
        "base_url": "https://api.siliconflow.cn/v1",
        "model": "deepseek-ai/DeepSeek-R1",
        "temperature": 0.7,
        "max_tokens": 4096
    },
    stream=True
)

# 处理流式响应
for line in response.iter_lines():
    if line:
        data = json.loads(line.decode('utf-8').replace('data: ', ''))
        if data.get('status') == 'streaming':
            print(data.get('content'), end='')
        elif data.get('status') == 'success':
            print("\n\n处理完成！")
```

## 开发说明

### 模式说明
- **mode1（快速降重）**: 基于Fuck-AIGC策略，简单词汇替换，适合初稿降重
- **mode2（深度降重）**: 基于AI-Detection策略，深度重构，适合高标准降重

### 安全考虑
1. 所有输入都会经过严格的验证和清理
2. 提示词注入会被自动检测和阻止
3. API密钥建议通过环境变量配置，而非硬编码
4. 生产环境建议配置HTTPS和反向代理

## 注意事项
1. 请妥善保管API密钥，不要泄露给他人
2. 遵守API服务商的使用条款和速率限制
3. 处理后的文本仍需人工审核，确保准确性
4. 定期更新依赖库以获取最新安全补丁
