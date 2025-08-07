# LLMBroker

LLMBroker 是一个统一的大语言模型代理服务，提供统一的API接口来访问多个不同的LLM提供商（OpenAI、Claude、通义千问等）。

## 特性

- 🚀 **统一接口**: 兼容OpenAI API格式，支持多个LLM提供商
- 🔧 **参数注入**: 自动注入默认参数，支持参数覆盖
- 📋 **配置管理**: 灵活的YAML配置文件，支持环境变量
- 🛡️ **错误处理**: 完善的错误处理和响应格式化
- 📝 **请求日志**: 详细的请求日志记录和监控
- 🔄 **负载均衡**: 支持多模型配置和转发

## 支持的模型提供商

- **OpenAI**: GPT-3.5-turbo, GPT-4, GPT-4-turbo等
- **Anthropic**: Claude-3 系列模型
- **阿里云**: 通义千问系列模型
- **扩展性**: 易于添加新的提供商支持

## 快速开始

### 1. 安装依赖

```bash
pip install -r requirements.txt
```

### 2. 配置环境变量

创建 `.env` 文件或设置环境变量：

```bash
# OpenAI API Key
export OPENAI_API_KEY="your-openai-api-key"

# Anthropic API Key
export ANTHROPIC_API_KEY="your-anthropic-api-key"

# 阿里云DashScope API Key
export DASHSCOPE_API_KEY="your-dashscope-api-key"
```

### 3. 修改配置文件

编辑 `config.yaml` 文件，配置需要使用的模型：

```yaml
models:
  gpt-3.5-turbo:
    provider: "openai"
    model_name: "gpt-3.5-turbo"
    api_key: "${OPENAI_API_KEY}"
    default_params:
      temperature: 0.7
      max_tokens: 1000
```

### 4. 启动服务

```bash
# 使用启动脚本
./run.sh

# 或者直接运行
python -m app.main

# 或者使用uvicorn
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

### 5. 测试API

服务启动后，访问 `http://localhost:8000/docs` 查看API文档。

#### 聊天完成示例

```bash
curl -X POST "http://localhost:8000/v1/chat/completions" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "gpt-3.5-turbo",
    "messages": [
      {"role": "user", "content": "Hello, how are you?"}
    ],
    "temperature": 0.7
  }'
```

#### 文本完成示例

```bash
curl -X POST "http://localhost:8000/v1/completions" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "gpt-3.5-turbo",
    "prompt": "The future of AI is",
    "max_tokens": 100
  }'
```

## API接口

### 聊天完成 - `/v1/chat/completions`

兼容OpenAI ChatGPT API格式：

```json
{
  "model": "gpt-3.5-turbo",
  "messages": [
    {"role": "system", "content": "You are a helpful assistant."},
    {"role": "user", "content": "Hello!"}
  ],
  "temperature": 0.7,
  "max_tokens": 1000
}
```

### 文本完成 - `/v1/completions`

兼容OpenAI Completions API格式：

```json
{
  "model": "gpt-3.5-turbo",
  "prompt": "Once upon a time",
  "max_tokens": 100,
  "temperature": 0.7
}
```

### 模型列表 - `/models`

获取所有可用模型：

```bash
curl http://localhost:8000/models
```

### 健康检查 - `/health`

服务健康状态检查：

```bash
curl http://localhost:8000/health
```

## 配置说明

### 模型配置

```yaml
models:
  model-alias:  # 模型别名，客户端使用这个名称
    provider: "openai"           # 提供商：openai, claude, qwen
    model_name: "gpt-3.5-turbo"  # 实际模型名称
    api_key: "${API_KEY}"        # API密钥（支持环境变量）
    base_url: "https://..."      # API基础URL
    default_params:              # 默认参数
      temperature: 0.7
      max_tokens: 1000
```

### 代理配置

```yaml
proxy:
  default_model: "gpt-3.5-turbo"         # 默认模型
  enable_parameter_injection: true       # 启用参数注入
  enable_request_logging: true          # 启用请求日志
  timeout: 60                           # 请求超时时间
```

## 项目结构

```
LLMBroker/
├── app/
│   ├── __init__.py        # 包初始化
│   ├── main.py            # FastAPI 入口和路由
│   ├── clients.py         # 多模型客户端封装
│   ├── config.py          # 配置加载
│   ├── proxy.py           # 代理逻辑
│   └── utils.py           # 工具函数
├── config.yaml            # 配置文件
├── requirements.txt       # 依赖包列表
├── README.md             # 项目文档
└── run.sh                # 启动脚本
```

## 开发指南

### 添加新的模型提供商

1. 在 `clients.py` 中创建新的客户端类，继承 `BaseModelClient`
2. 实现 `chat_completion` 和 `text_completion` 方法
3. 在 `ModelClientManager.CLIENT_CLASSES` 中注册新客户端
4. 更新配置文件示例

### 参数注入机制

代理服务会自动合并模型的默认参数和请求参数：

1. 从配置文件加载模型的默认参数
2. 从请求中提取参数
3. 合并参数（请求参数优先级更高）
4. 传递给模型API

### 错误处理

所有错误都会被转换为标准格式：

```json
{
  "error": {
    "message": "错误描述",
    "type": "error_type",
    "code": "ERROR_CODE"
  }
}
```

## 部署指南

### Docker 部署

```dockerfile
FROM python:3.9-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### 环境变量

确保在部署环境中设置必要的API密钥：

```bash
OPENAI_API_KEY=your-key
ANTHROPIC_API_KEY=your-key
DASHSCOPE_API_KEY=your-key
```

## 贡献指南

1. Fork 项目
2. 创建特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 打开 Pull Request

## 许可证

MIT License

## 联系方式

- 作者: LanZhengPeng
- 项目链接: [GitHub Repository]
