# mdcover

在线 Markdown 文档转换工具

- 前端：React + Vite + Ant Design + `@uiw/react-md-editor`
- 后端：FastAPI + Python-Markdown + Jinja2 + WeasyPrint + pypandoc
- 部署：Docker + Docker Compose（前端 Nginx，后端 FastAPI）

## 核心转换链路

- HTML / PDF：`Markdown -> HTML片段 -> Jinja2包裹完整HTML -> 导出`
- Word：`Markdown(原文) -> pypandoc -> DOCX`（不走 HTML 中间态）

## 目录

```text
mdcover/
├── docker-compose.yml
├── frontend/
└── backend/
```

## 前置要求

1. Docker 24+（建议）
2. Docker Compose v2+
3. `backend/fonts/` 下有可用中文字体文件（当前默认使用 `SourceHanSansSC-Regular.otf`）

## 一键启动（本地）

```bash
docker compose up --build -d
```

查看状态：

```bash
docker compose ps
```

查看日志：

```bash
docker compose logs -f backend frontend
```

停止并删除容器：

```bash
docker compose down
```

访问地址：

- 前端：<http://localhost:5173>
- 后端健康检查：<http://localhost:8000/api/health>

***

## 打镜像步骤

### 1) 单独构建后端镜像

```bash
docker build -t mdcover-backend:0.1.0 ./backend
```

### 2) 单独构建前端镜像

```bash
docker build -t mdcover-frontend:0.1.0 ./frontend
```

### 3) 查看本地镜像

```bash
docker images | grep mdcover
```

## 推送镜像（可选）

如果需要发布到私有仓库：

```bash
docker tag mdcover-backend:0.1.0 <registry>/mdcover-backend:0.1.0
docker tag mdcover-frontend:0.1.0 <registry>/mdcover-frontend:0.1.0

docker push <registry>/mdcover-backend:0.1.0
docker push <registry>/mdcover-frontend:0.1.0
```

***

## 部署步骤

## 服务器直接构建（基于源码）

1. 上传/拉取项目代码到服务器。
2. 确认 `backend/fonts/SourceHanSansSC-Regular.otf` 存在。
3. 启动：

```bash
docker compose up -d --build
```

1. 验证：

```bash
docker compose ps
curl -sS http://localhost:8000/api/health
```

***

## 冒烟测试

### 健康检查

```bash
curl -sS http://localhost:8000/api/health
```

### HTML 导出

```bash
curl -sS -X POST "http://localhost:8000/api/convert/html" \
  -H "Content-Type: application/json" \
  -d '{"markdown":"# Hello"}' | head
```

### PDF 导出

```bash
curl -sS -X POST "http://localhost:8000/api/convert/pdf" \
  -H "Content-Type: application/json" \
  -d '{"markdown":"# PDF\n\n中文测试"}' \
  -o /tmp/mdcover-test.pdf -D -
```

### Word 导出

```bash
curl -sS -X POST "http://localhost:8000/api/convert/word" \
  -H "Content-Type: application/json" \
  -d '{"markdown":"# Word\n\n- item1\n- item2"}' \
  -o /tmp/mdcover-test.docx -D -
```

