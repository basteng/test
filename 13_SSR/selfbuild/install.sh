#!/bin/bash
# SSR 自建镜像一键安装脚本
# 自动下载所有文件并部署

set -e

# 颜色
RED='\e[31m'
GREEN='\e[32m'
YELLOW='\e[33m'
BLUE='\e[34m'
CYAN='\e[36m'
NC='\e[0m'

echo -e "${CYAN}================================${NC}"
echo -e "${CYAN}  SSR 自建镜像一键安装${NC}"
echo -e "${CYAN}================================${NC}"
echo ""

# GitHub Raw 文件基础URL
GITHUB_RAW="https://raw.githubusercontent.com/basteng/test/main/13_SSR/selfbuild"

# 工作目录
WORK_DIR="/root/ssr-selfbuild"

echo -e "${BLUE}[1/4] 创建工作目录...${NC}"
mkdir -p "$WORK_DIR"
cd "$WORK_DIR"

echo -e "${BLUE}[2/4] 下载部署文件...${NC}"

# 检查是否有 wget 或 curl
if command -v wget >/dev/null 2>&1; then
    DOWNLOAD="wget -q --show-progress -O"
elif command -v curl >/dev/null 2>&1; then
    DOWNLOAD="curl -fsSL -o"
else
    echo -e "${RED}❌ 错误: 系统中未找到 wget 或 curl${NC}"
    echo -e "${YELLOW}请安装: apt install wget 或 yum install wget${NC}"
    exit 1
fi

# 下载所有必要文件
echo -e "${CYAN}  - 下载 Dockerfile...${NC}"
$DOWNLOAD Dockerfile "${GITHUB_RAW}/Dockerfile"

echo -e "${CYAN}  - 下载 build-docker.sh...${NC}"
$DOWNLOAD build-docker.sh "${GITHUB_RAW}/build-docker.sh"

echo -e "${CYAN}  - 下载 ssr-plus.sh...${NC}"
$DOWNLOAD ssr-plus.sh "${GITHUB_RAW}/ssr-plus.sh"

echo -e "${CYAN}  - 下载 README.md...${NC}"
$DOWNLOAD README.md "${GITHUB_RAW}/README.md"

echo ""
echo -e "${GREEN}✅ 所有文件下载完成${NC}"
echo ""

# 添加执行权限
echo -e "${BLUE}[3/4] 设置执行权限...${NC}"
chmod +x build-docker.sh ssr-plus.sh

# 检查 Docker
echo -e "${BLUE}[4/4] 检查 Docker...${NC}"
if ! command -v docker >/dev/null 2>&1; then
    echo -e "${YELLOW}⚠️  未检测到 Docker，部署脚本会自动安装${NC}"
else
    echo -e "${GREEN}✅ Docker 已安装${NC}"
fi

echo ""
echo -e "${GREEN}========================================${NC}"
echo -e "${GREEN}🎉 准备完成！${NC}"
echo -e "${GREEN}========================================${NC}"
echo ""
echo -e "${CYAN}文件已下载到: ${YELLOW}${WORK_DIR}${NC}"
echo ""
echo -e "${CYAN}接下来将自动启动部署...${NC}"
echo -e "${YELLOW}提示: 镜像构建需要 3-5 分钟，请耐心等待${NC}"
echo ""

read -t 5 -p "按回车继续，或等待 5 秒自动开始..." || true
echo ""

# 开始部署
echo -e "${BLUE}开始部署 SSR...${NC}"
echo ""

# 检查是否已有镜像
if docker images 2>/dev/null | grep -q "^ssr-selfbuild"; then
    echo -e "${GREEN}✅ 检测到已有镜像: ssr-selfbuild:latest${NC}"
    echo -e "${YELLOW}跳过构建，直接启动管理脚本...${NC}"
    echo ""
    exec bash ssr-plus.sh
fi

# 构建镜像
echo -e "${BLUE}构建 Docker 镜像（首次运行需要几分钟）...${NC}"
bash build-docker.sh

# 启动管理脚本
echo ""
echo -e "${BLUE}启动管理脚本...${NC}"
sleep 2
exec bash ssr-plus.sh
