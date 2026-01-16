FROM python:3.9-slim

LABEL maintainer="自建SSR镜像"
LABEL description="ShadowsocksR Docker Image"
LABEL version="1.0.0"

# 设置环境变量
ENV PYTHONUNBUFFERED=1 \
    SSR_VERSION=3.2.2 \
    TZ=Asia/Shanghai

# 安装系统依赖
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        git \
        libsodium23 \
        curl \
        ca-certificates \
        procps \
    && rm -rf /var/lib/apt/lists/*

# 克隆 ShadowsocksR 源码
WORKDIR /usr/local
RUN git clone -b manyuser https://github.com/shadowsocksrr/shadowsocksr.git shadowsocks && \
    cd shadowsocks && \
    git checkout 3.2.2 || git checkout master

# 创建配置目录
RUN mkdir -p /etc/shadowsocks-r

# 添加启动脚本
RUN echo '#!/bin/bash\n\
CFG="/etc/shadowsocks-r/config.json"\n\
if [ ! -f "$CFG" ]; then\n\
  echo "{\n\
    \"server\":\"0.0.0.0\",\n\
    \"server_ipv6\":\"::\",\n\
    \"server_port\":20000,\n\
    \"local_address\":\"127.0.0.1\",\n\
    \"local_port\":1080,\n\
    \"password\":\"dongtaiwang.com\",\n\
    \"timeout\":120,\n\
    \"method\":\"chacha20-ietf\",\n\
    \"protocol\":\"auth_sha1_v4\",\n\
    \"protocol_param\":\"\",\n\
    \"obfs\":\"plain\",\n\
    \"obfs_param\":\"\",\n\
    \"redirect\":\"\",\n\
    \"dns_ipv6\":false,\n\
    \"fast_open\":false,\n\
    \"workers\":1\n\
  }" > "$CFG"\n\
fi\n\
exec python /usr/local/shadowsocks/shadowsocks/server.py -c "$CFG"\n\
' > /usr/local/bin/entrypoint.sh && \
    chmod +x /usr/local/bin/entrypoint.sh

# 暴露端口 (默认 20000，实际使用时会通过配置文件修改)
EXPOSE 20000/tcp 20000/udp

# 健康检查
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
  CMD pgrep -f "server.py" || exit 1

# 工作目录
WORKDIR /usr/local/shadowsocks

# 启动命令
ENTRYPOINT ["/usr/local/bin/entrypoint.sh"]
