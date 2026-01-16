# 13_SSR - SSR 自建服务器部署方案

安全可控的 SSR Docker 自建镜像 + 一键部署脚本

---

## 📁 目录结构

```
13_SSR/
├── selfbuild/              # 自建方案
│   ├── Dockerfile          # 自建镜像定义
│   ├── build-docker.sh     # 镜像构建脚本
│   ├── deploy.sh           # 一键部署脚本
│   ├── install.sh          # 一键安装脚本
│   ├── ssr-plus.sh         # 管理脚本
│   └── README.md           # 详细使用文档
│
├── 服务器部署指南.md        # 完整部署教程
└── 防火墙配置说明.md        # 防火墙配置详解
```

---

## 🚀 快速开始

### ⚡ 一键部署（推荐）

在服务器上执行一条命令：

```bash
wget -O install.sh https://raw.githubusercontent.com/basteng/test/main/13_SSR/selfbuild/install.sh && chmod +x install.sh && bash install.sh
```

或使用 curl：

```bash
curl -fsSL https://raw.githubusercontent.com/basteng/test/main/13_SSR/selfbuild/install.sh | bash
```

**就这么简单！** 脚本会自动：
1. ✅ 下载所有部署文件
2. ✅ 安装 Docker
3. ✅ 构建 SSR 镜像
4. ✅ 配置防火墙
5. ✅ 启动管理界面

---

## ✨ 核心特性

### 安全可控
- ✅ **完全自建镜像**：从官方 ShadowsocksR 源码构建
- ✅ **透明可审计**：完整的 Dockerfile，构建过程透明
- ✅ **版本固定**：使用 SSR 3.2.2 稳定版

### 自动化
- ✅ **一键安装**：一条命令完成所有部署
- ✅ **自动配置防火墙**：支持 UFW/firewalld/iptables
- ✅ **开机自启**：容器自动重启，无需手动管理

### 功能完善
- ✅ **跨平台支持**：Debian/Ubuntu/CentOS/RHEL/Rocky/AlmaLinux/Fedora/openSUSE
- ✅ **IPv4/IPv6 双栈**：同时支持 IPv4 和 IPv6
- ✅ **BBR 加速**：一键启用 TCP BBR + Fast Open
- ✅ **健康检查**：Docker 原生健康检查机制

---

## 📖 使用文档

### 核心文档

- **[服务器部署指南.md](./服务器部署指南.md)** - 从租服务器到成功运行的完整流程
- **[防火墙配置说明.md](./防火墙配置说明.md)** - 防火墙配置详解和常见问题
- **[selfbuild/README.md](./selfbuild/README.md)** - 详细的技术文档和高级操作

### 快速链接

| 需求 | 查看文档 |
|------|---------|
| 第一次部署 | [服务器部署指南.md](./服务器部署指南.md) |
| 防火墙问题 | [防火墙配置说明.md](./防火墙配置说明.md) |
| 高级配置 | [selfbuild/README.md](./selfbuild/README.md) |
| 故障排查 | [selfbuild/README.md - 故障排查](./selfbuild/README.md#故障排查) |

---

## 🎯 典型使用场景

### 场景 1：新服务器快速部署

```bash
# 1. SSH 连接服务器
ssh root@你的服务器IP

# 2. 执行一键安装
wget -O install.sh https://raw.githubusercontent.com/basteng/test/main/13_SSR/selfbuild/install.sh && chmod +x install.sh && bash install.sh

# 3. 在菜单中选择 1 安装 SSR，设置端口和密码
# 4. 复制 ssr:// 链接到客户端
```

### 场景 2：管理现有 SSR

```bash
# 进入部署目录
cd /root/ssr-selfbuild

# 运行管理脚本
bash ssr-plus.sh

# 选择对应的功能：
# 2) 修改配置
# 3) 查看配置
# 4-6) 启动/停止/重启
# 8) 启用 BBR 加速
```

### 场景 3：多服务器批量部署

```bash
# 导出镜像
docker save ssr-selfbuild:latest -o ssr-image.tar

# 传输到其他服务器
scp ssr-image.tar root@另一台服务器:/root/

# 在另一台服务器导入
docker load -i ssr-image.tar
```

---

## 🔧 高级操作

### 自定义镜像

编辑 `selfbuild/Dockerfile` 修改：
- SSR 版本
- 默认配置
- 预装组件

### 推送到私有仓库

```bash
# 标记镜像
docker tag ssr-selfbuild:latest your-registry.com/ssr:1.0

# 推送
docker push your-registry.com/ssr:1.0
```

### 多端口部署

```bash
# 运行多个实例，不同端口
docker run -dit --name ssr-8388 -p 8388:8388 --restart unless-stopped ssr-selfbuild:latest
docker run -dit --name ssr-8389 -p 8389:8389 --restart unless-stopped ssr-selfbuild:latest
```

---

## 💰 成本估算

**推荐配置**（Vultr/DigitalOcean）：
- 服务器：$5/月（1核 1GB 1TB流量）
- 个人使用流量充足
- **总计：≈ ¥35/月**

---

## 🔒 安全建议

1. **使用强密码**：至少 16 位，包含大小写字母+数字+符号
2. **定期更新**：定期重建镜像获取安全更新
3. **启用防火墙**：限制只开放必要端口
4. **使用 SSH 密钥**：禁用密码登录
5. **定期更换端口和密码**

---

## 📊 性能优化

### 推荐配置

**加密方式**：`chacha20-ietf`（性能和安全平衡）
**协议**：`auth_sha1_v4`（兼容性好）
**混淆**：`plain`（性能最佳）

### 系统优化

在管理脚本中选择 `8) 启用系统加速`：
- 启用 TCP BBR 拥塞控制
- 启用 TCP Fast Open
- 显著提升网络性能

---

## 🙏 致谢

本项目在开发过程中参考了以下项目，特此致谢：

- **[Alvin9999/SSR-Plus](https://github.com/Alvin9999/SSR-Plus)** - 原始 SSR 管理脚本，提供了脚本结构和功能设计的参考
- **[shadowsocksrr/shadowsocksr](https://github.com/shadowsocksrr/shadowsocksr)** - ShadowsocksR 官方实现

本项目为完全重写的自建方案，包含以下改进：
- ✅ 自建 Docker 镜像（安全可控）
- ✅ 自动防火墙配置
- ✅ 完整的部署文档
- ✅ 一键安装脚本

---

## 📝 许可证

本项目仅供学习和研究使用。请遵守当地法律法规，合法使用代理工具。

---

## 🆘 获取帮助

- **查看文档**：[服务器部署指南.md](./服务器部署指南.md)
- **故障排查**：[selfbuild/README.md](./selfbuild/README.md)
- **查看日志**：`docker logs ssr`

---

**Happy Coding!** 🚀
