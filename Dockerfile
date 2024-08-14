11.1# FROM --platform=linux/arm64 python:3.9
FROM --platform=linux/amd64 registry.cn-hangzhou.aliyuncs.com/docker-tk-1024/docker-repo:0.1
ENV TZ=Asia/Shanghai
ARG DEBIAN_FRONTEND=noninteractive

RUN apt-get update && apt-get install -y python3-opencv libglib2.0-0 libsm6 libxext6 libxrender-dev && rm -rf /var/lib/apt/lists/*

RUN  pip install -U pip && pip install onnxruntime && pip install cnocr[serve] --index-url https://mirrors.aliyun.com/pypi/simple

CMD ["cnocr", "serve", "-H", "0.0.0.0", "-p", "8501"]

EXPOSE 8501
