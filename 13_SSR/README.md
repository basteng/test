# 自建 SSR Docker 镜像 + 一键管理脚本

## 项目介绍

本项目提供了完整的 SSR（ShadowsocksR）自建方案，包括：
- **Dockerfile**: 自建安全可控的 SSR Docker 镜像
- **build-docker.sh**: 一键构建镜像脚本
- **ssr-plus.sh**: 完整的 SSR 服务管理脚本

相比使用第三方镜像，自建镜像具有以下优势：
- ✅ **安全可控**: 完全掌握镜像内容，避免潜在风险
- ✅ **透明可审计**: 源码和构建过程完全透明
- ✅ **自定义配置**: 可根据需求修改镜像内容
- ✅ **版本可控**: 固定 SSR 版本，避免意外更新

---

## 快速开始

### 步骤 1: 构建 Docker 镜像

```bash
# 进入项目目录
cd 13_SSR

# 添加执行权限
chmod +x build-docker.sh

# 构建镜像（需要几分钟时间）
bash build-docker.sh
```

构建成功后，你会看到镜像信息：
```
镜像名称: ssr-selfbuild:latest
```

### 步骤 2: 运行管理脚本

```bash
# 进入管理脚本目录
cd Alvin9999

# 添加执行权限
chmod +x ssr-plus.sh

# 运行管理脚本
bash ssr-plus.sh
```

### 步骤 3: 安装 SSR 服务

在管理脚本菜单中选择 `1` 安装 SSR：
```
请输入端口 [默认20000]: 8388
请输入密码 [默认dongtaiwang.com]: your-password
选择加密方式 [推荐16]: 16
选择协议 [推荐2]: 2
选择混淆 [推荐1]: 1
```

完成后会自动显示 SSR 连接链接，复制到客户端即可使用。

---

## 文件说明

### 核心文件

| 文件名 | 说明 |
|--------|------|
| `Dockerfile` | SSR Docker 镜像定义文件 |
| `build-docker.sh` | 镜像构建脚本 |
| `Alvin9999/ssr-plus.sh` | SSR 服务管理脚本 |
| `README.md` | 使用说明文档（本文件） |

### Dockerfile 特性

- **基础镜像**: Python 3.9 Slim（轻量化）
- **SSR 版本**: 3.2.2（稳定版）
- **内置组件**:
  - ShadowsocksR 完整服务端
  - 自动启动守护脚本
  - 健康检查机制
- **默认配置**:
  - 端口: 20000（可自定义）
  - 加密: chacha20-ietf
  - 协议: auth_sha1_v4
  - 混淆: plain

---

## 管理脚本功能

管理脚本 `ssr-plus.sh` 提供以下功能：

### 1. 安装 SSR
自动安装 Docker（如需要）并部署 SSR 服务，配置开机自启。

### 2. 修改配置
修改端口、密码、加密方式、协议、混淆等参数。

### 3. 查看配置
显示当前配置和 SSR 连接链接。

### 4. 启动/停止/重启
控制 SSR 服务运行状态。

### 5. 卸载 SSR
完全移除 SSR 容器和镜像。

### 6. 系统加速
启用 BBR + TCP Fast Open（提升网络性能）。

### 7. 脚本更新
检查并更新管理脚本到最新版本。

---

## 高级操作

### 自定义镜像名称

如果需要使用不同的镜像名称，修改以下文件：

**1. build-docker.sh（第 7-8 行）**
```bash
IMAGE_NAME="your-custom-name"
IMAGE_TAG="v1.0"
```

**2. Alvin9999/ssr-plus.sh（第 8 行）**
```bash
DOCKER_IMAGE="your-custom-name:v1.0"
```

### 推送到私有仓库

构建完成后，可以推送到私有 Docker 仓库：

```bash
# 1. 标记镜像
docker tag ssr-selfbuild:latest your-registry.com/ssr:latest

# 2. 登录私有仓库
docker login your-registry.com

# 3. 推送镜像
docker push your-registry.com/ssr:latest

# 4. 修改管理脚本使用私有仓库镜像
# 编辑 ssr-plus.sh，修改 DOCKER_IMAGE 变量
```

### 导出/导入镜像

在无网络环境部署时，可以导出镜像：

```bash
# 导出镜像
docker save ssr-selfbuild:latest -o ssr-image.tar

# 传输到目标服务器后导入
docker load -i ssr-image.tar
```

### 多端口部署

需要运行多个 SSR 实例时：

```bash
# 修改容器名称和端口
docker run -dit --name ssr-8388 \
  --restart unless-stopped \
  -p 8388:8388 \
  ssr-selfbuild:latest

docker run -dit --name ssr-8389 \
  --restart unless-stopped \
  -p 8389:8389 \
  ssr-selfbuild:latest
```

---

## 系统要求

### 最低配置
- **CPU**: 1 核
- **内存**: 512MB
- **磁盘**: 1GB 可用空间
- **系统**:
  - Debian 9+
  - Ubuntu 16.04+
  - CentOS 7+
  - RHEL 7+
  - Rocky Linux 8+
  - AlmaLinux 8+
  - Fedora 30+
  - openSUSE Leap 15+

### 推荐配置
- **CPU**: 2+ 核
- **内存**: 1GB+
- **网络**: 稳定的公网 IP

---

## 客户端配置

### 获取连接信息

运行管理脚本后选择 `3) 查看配置`，会显示：
- 服务器 IP
- 端口
- 密码
- 加密方式
- 协议
- 混淆
- **SSR 链接**（ssr:// 开头）

### 导入客户端

1. **Windows/macOS/Linux**
   - 使用 ShadowsocksR 客户端
   - 从剪贴板导入 ssr:// 链接
   - 或手动填写配置参数

2. **Android**
   - 使用 ShadowsocksR Android
   - 扫描二维码或导入链接

3. **iOS**
   - 使用支持 SSR 的客户端
   - 手动配置参数

---

## 性能优化

### 1. 启用 BBR 加速

管理脚本中选择 `8) 启用系统加速`，会自动配置：
- **TCP BBR**: 拥塞控制算法
- **TCP Fast Open**: 减少握手延迟

```bash
# 手动检查 BBR 状态
sysctl net.ipv4.tcp_congestion_control
# 输出应为: bbr

sysctl net.core.default_qdisc
# 输出应为: fq
```

### 2. 调整加密方式

性能排序（快→慢）：
1. `none` - 无加密（不推荐）
2. `chacha20-ietf` - **推荐**（平衡性能和安全）
3. `aes-256-gcm` - 高安全性
4. `aes-256-cfb` - 兼容性好

### 3. 选择合适协议

推荐组合：
- **日常使用**: `auth_sha1_v4` + `plain`
- **严格环境**: `auth_chain_a` + `tls1.2_ticket_auth`

---

## 故障排查

### 问题 1: Docker 构建失败

**症状**: `git clone` 超时或失败

**解决方案**:
```bash
# 设置 Git 代理
git config --global http.proxy http://127.0.0.1:7890
git config --global https.proxy https://127.0.0.1:7890

# 或使用国内镜像
# 修改 Dockerfile 中的 git clone 地址
```

### 问题 2: 容器启动失败

**症状**: `docker ps` 看不到容器

**解决方案**:
```bash
# 查看容器日志
docker logs ssr

# 检查端口占用
netstat -tlnp | grep 20000

# 重新创建容器
docker rm -f ssr
bash ssr-plus.sh  # 选择 1 重新安装
```

### 问题 3: 客户端无法连接

**检查清单**:
1. 服务器防火墙是否开放端口
   ```bash
   # CentOS/RHEL
   firewall-cmd --add-port=20000/tcp --permanent
   firewall-cmd --reload

   # Ubuntu/Debian
   ufw allow 20000/tcp
   ufw reload
   ```

2. 云服务器安全组是否开放端口
   - 阿里云/腾讯云/AWS 等需要在控制台配置

3. SSR 服务是否运行
   ```bash
   docker exec ssr pgrep -f server.py
   # 有输出说明正在运行
   ```

4. 配置是否正确
   ```bash
   bash ssr-plus.sh  # 选择 3 查看配置
   ```

### 问题 4: 性能较差

**优化建议**:
1. 启用 BBR 加速（管理脚本选项 8）
2. 更换加密方式为 `chacha20-ietf`
3. 选择地理位置更近的服务器
4. 检查服务器带宽是否充足

---

## 安全建议

1. **使用强密码**: 至少 16 位随机字符
2. **定期更新**: 定期重建镜像获取安全更新
3. **限制访问**: 使用防火墙限制访问来源（如有需要）
4. **监控日志**: 定期检查容器日志
   ```bash
   docker logs ssr --tail 100
   ```
5. **备份配置**: 定期备份配置文件
   ```bash
   docker exec ssr cat /etc/shadowsocks-r/config.json > config-backup.json
   ```

---

## 版本信息

- **Dockerfile 版本**: 1.0.0
- **SSR 版本**: 3.2.2
- **管理脚本版本**: v1.2.2
- **最后更新**: 2026-01-16

---

## 常见问题 FAQ

**Q: 为什么要自建镜像而不是用现成的？**
A: 自建镜像可以完全掌控内容，避免潜在的安全风险，并且可以自定义配置。

**Q: 构建镜像需要多久？**
A: 通常需要 3-5 分钟，取决于网络速度和服务器性能。

**Q: 可以在 ARM 架构上运行吗？**
A: 可以，但需要修改 Dockerfile 基础镜像为 `python:3.9-slim-arm64v8`。

**Q: 如何升级 SSR 版本？**
A: 修改 Dockerfile 中的 `SSR_VERSION` 变量，重新构建镜像。

**Q: 忘记密码怎么办？**
A: 运行管理脚本选择 `2) 修改配置`，重新设置密码。

**Q: 支持 IPv6 吗？**
A: 支持，容器默认监听 `::`（IPv6 全地址）。

---

## 许可证

本项目基于原 SSR-Plus 项目修改，仅供学习和研究使用。

请遵守当地法律法规，合法使用代理工具。

---

## 贡献与反馈

如有问题或建议，欢迎提交 Issue 或 Pull Request。

**Happy Coding!** 🚀
