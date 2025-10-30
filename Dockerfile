# 使用官方 Python 3.12 镜像作为基础镜像
FROM python:3.12-slim

# 安装 Git（因为我们需要从 GitHub 克隆代码）
RUN apt-get update && apt-get install -y git && apt-get clean

# 设置工作目录
WORKDIR /app

# 从 GitHub 克隆项目代码
RUN git clone https://github.com/Enghon/AI.git

# 进入克隆的项目目录
WORKDIR /app/AI

# 安装项目所需的 Python 库依赖
RUN pip install --no-cache-dir -r requirements.txt

# 设置 Python 输出无缓冲，方便实时查看日志
ENV PYTHONUNBUFFERED 1

# 默认启动应用（假设你项目有一个 app.py）
CMD ["python", "app.py"]
