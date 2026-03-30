# 地下水智能预测系统

基于 Django 的地下水以电折水系数预测平台，集成 BP 神经网络模型。

## 功能模块

- 用户登录 / 注册
- 设备管理
- 地下水数据查询
- ML 模型预测（以电折水系数）
- 智能分析

## 技术栈

- 后端：Django
- 前端：HTML / CSS / JS
- ML：Python（BP神经网络）
- 部署：Docker + Railway

## 本地运行

```bash
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

## Docker 运行

```bash
docker build -t crashcourse .
docker run -p 8000:8000 crashcourse
```

## 软件著作权

本项目已申请软件著作权。
