FROM python:3.12-slim

WORKDIR /app

# 安装依赖
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 复制项目代码
COPY . .

EXPOSE 8000

# 启动Django（生产用gunicorn）
CMD ["gunicorn", "crashcourse.wsgi:application", "--bind", "0.0.0.0:8000"]
