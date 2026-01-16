#!/bin/bash
# SSR 一键部署脚本
# 自动构建镜像并启动管理界面

set -e

# 颜色
RED='\e[31m'
GREEN='\e[32m'
YELLOW='\e[33m'
BLUE='\e[34m'
CYAN='\e[36m'
NC='\e[0m'

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

echo -e "${CYAN}================================${NC}"
echo -e "${CYAN}  SSR 一键部署脚本${NC}"
echo -e "${CYAN}================================${NC}"
echo ""

# 检查是否已有镜像
if docker images | grep -q "^ssr-selfbuild"; then
    echo -e "${GREEN}✅ 检测到已有镜像: ssr-selfbuild:latest${NC}"
    echo ""
    read -p "是否跳过构建，直接运行管理脚本? [Y/n]: " skip_build

    if [[ ! "$skip_build" =~ ^[Nn]$ ]]; then
        echo -e "${BLUE}跳过构建，启动管理脚本...${NC}"
        cd "${SCRIPT_DIR}/Alvin9999"
        exec bash ssr-plus.sh
    fi
fi

# 构建镜像
echo -e "${BLUE}[步骤 1/2] 构建 Docker 镜像...${NC}"
cd "${SCRIPT_DIR}"

if [ ! -f "build-docker.sh" ]; then
    echo -e "${RED}❌ 错误: 未找到 build-docker.sh${NC}"
    exit 1
fi

chmod +x build-docker.sh
bash build-docker.sh

# 检查构建结果
if ! docker images | grep -q "^ssr-selfbuild"; then
    echo -e "${RED}❌ 镜像构建失败${NC}"
    exit 1
fi

echo ""
echo -e "${GREEN}✅ 镜像构建完成${NC}"
echo ""

# 启动管理脚本
echo -e "${BLUE}[步骤 2/2] 启动管理脚本...${NC}"
sleep 2

cd "${SCRIPT_DIR}/Alvin9999"

if [ ! -f "ssr-plus.sh" ]; then
    echo -e "${RED}❌ 错误: 未找到 ssr-plus.sh${NC}"
    exit 1
fi

chmod +x ssr-plus.sh
exec bash ssr-plus.sh
