#!/bin/bash
# SSR Docker 镜像构建脚本
# 用于自建 SSR Docker 镜像

set -e  # 遇到错误立即退出

# ========== 配置 ==========
IMAGE_NAME="ssr-selfbuild"
IMAGE_TAG="latest"
FULL_IMAGE_NAME="${IMAGE_NAME}:${IMAGE_TAG}"

# 颜色
RED='\e[31m'
GREEN='\e[32m'
YELLOW='\e[33m'
BLUE='\e[34m'
CYAN='\e[36m'
NC='\e[0m'

# ========== 检查环境 ==========
echo -e "${BLUE}[1/4] 检查构建环境...${NC}"

# 检查 Docker
if ! command -v docker >/dev/null 2>&1; then
    echo -e "${RED}❌ 错误: 未安装 Docker${NC}"
    echo -e "${YELLOW}请先安装 Docker: https://docs.docker.com/get-docker/${NC}"
    exit 1
fi

# 检查 Docker 是否运行
if ! docker info >/dev/null 2>&1; then
    echo -e "${RED}❌ 错误: Docker 服务未运行${NC}"
    echo -e "${YELLOW}请启动 Docker: sudo systemctl start docker${NC}"
    exit 1
fi

# 检查 Dockerfile
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
DOCKERFILE="${SCRIPT_DIR}/Dockerfile"

if [ ! -f "$DOCKERFILE" ]; then
    echo -e "${RED}❌ 错误: 未找到 Dockerfile${NC}"
    echo -e "${YELLOW}请确保 Dockerfile 在脚本同目录: ${SCRIPT_DIR}${NC}"
    exit 1
fi

echo -e "${GREEN}✅ 环境检查通过${NC}"

# ========== 清理旧镜像 ==========
echo -e "${BLUE}[2/4] 清理旧镜像...${NC}"

if docker images | grep -q "^${IMAGE_NAME}"; then
    read -p "发现已存在的镜像 ${FULL_IMAGE_NAME}，是否删除? [y/N]: " confirm
    if [[ "$confirm" =~ ^[Yy]$ ]]; then
        docker rmi -f "${FULL_IMAGE_NAME}" 2>/dev/null || true
        echo -e "${GREEN}✅ 旧镜像已删除${NC}"
    else
        echo -e "${YELLOW}⚠️  保留旧镜像，将覆盖构建${NC}"
    fi
else
    echo -e "${YELLOW}未发现旧镜像，直接构建${NC}"
fi

# ========== 构建镜像 ==========
echo -e "${BLUE}[3/4] 开始构建 Docker 镜像...${NC}"
echo -e "${CYAN}镜像名称: ${FULL_IMAGE_NAME}${NC}"
echo -e "${CYAN}构建目录: ${SCRIPT_DIR}${NC}"
echo ""

# 构建镜像（显示详细输出）
if docker build \
    --tag "${FULL_IMAGE_NAME}" \
    --file "${DOCKERFILE}" \
    --progress=plain \
    "${SCRIPT_DIR}"; then
    echo ""
    echo -e "${GREEN}✅ 镜像构建成功！${NC}"
else
    echo ""
    echo -e "${RED}❌ 镜像构建失败${NC}"
    exit 1
fi

# ========== 验证镜像 ==========
echo -e "${BLUE}[4/4] 验证镜像...${NC}"

# 检查镜像是否存在
if docker images | grep -q "^${IMAGE_NAME}.*${IMAGE_TAG}"; then
    echo -e "${GREEN}✅ 镜像验证成功${NC}"

    # 显示镜像信息
    echo ""
    echo -e "${CYAN}==================== 镜像信息 ====================${NC}"
    docker images "${FULL_IMAGE_NAME}" --format "table {{.Repository}}\t{{.Tag}}\t{{.Size}}\t{{.CreatedAt}}"
    echo -e "${CYAN}================================================${NC}"

    # 快速测试
    echo ""
    echo -e "${YELLOW}是否进行快速测试? [y/N]: ${NC}"
    read -t 10 test_confirm || test_confirm="n"

    if [[ "$test_confirm" =~ ^[Yy]$ ]]; then
        echo -e "${BLUE}启动测试容器...${NC}"

        # 删除旧的测试容器
        docker rm -f ssr-test-temp 2>/dev/null || true

        # 启动测试容器
        if docker run -d --name ssr-test-temp \
            -p 21000:20000 \
            "${FULL_IMAGE_NAME}" bash -c "sleep infinity"; then

            sleep 2

            # 检查容器状态
            if docker ps | grep -q "ssr-test-temp"; then
                echo -e "${GREEN}✅ 测试容器启动成功${NC}"
                echo -e "${YELLOW}提示: 测试容器名称为 ssr-test-temp，端口 21000${NC}"
                echo -e "${YELLOW}清理命令: docker rm -f ssr-test-temp${NC}"
            else
                echo -e "${RED}❌ 测试容器启动失败${NC}"
                docker logs ssr-test-temp
                docker rm -f ssr-test-temp 2>/dev/null || true
            fi
        else
            echo -e "${RED}❌ 无法启动测试容器${NC}"
        fi
    else
        echo -e "${YELLOW}跳过测试${NC}"
    fi
else
    echo -e "${RED}❌ 镜像验证失败${NC}"
    exit 1
fi

# ========== 完成 ==========
echo ""
echo -e "${GREEN}========================================${NC}"
echo -e "${GREEN}🎉 镜像构建完成！${NC}"
echo -e "${GREEN}========================================${NC}"
echo ""
echo -e "${CYAN}下一步操作：${NC}"
echo -e "  1. 使用镜像: ${YELLOW}${FULL_IMAGE_NAME}${NC}"
echo -e "  2. 修改 ssr-plus.sh 中的镜像名称"
echo -e "  3. 运行管理脚本: ${YELLOW}bash ssr-plus.sh${NC}"
echo ""
echo -e "${CYAN}高级操作：${NC}"
echo -e "  - 推送到私有仓库: ${YELLOW}docker tag ${FULL_IMAGE_NAME} your-registry.com/${IMAGE_NAME}:${IMAGE_TAG}${NC}"
echo -e "  - 导出镜像: ${YELLOW}docker save ${FULL_IMAGE_NAME} -o ssr-image.tar${NC}"
echo -e "  - 导入镜像: ${YELLOW}docker load -i ssr-image.tar${NC}"
echo ""
