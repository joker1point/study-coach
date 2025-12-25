# OpenAgents 网络部署到服务器指南

## 服务器信息

根据您提供的信息，您的服务器配置如下：
- **公网IP**: 112.28.0.160
- **内网IP**: 172.16.0.4
- **配置**: CPU 2核, 内存 2GB, 系统盘 40GB
- **流量**: 200GB/月, 带宽 3Mbps

## 部署前准备

### 1. 连接服务器

使用SSH连接到您的服务器：

```bash
ssh root@112.28.0.160
```

### 2. 更新系统

```bash
# CentOS/RHEL
yum update -y

# Ubuntu/Debian
apt update && apt upgrade -y
```

### 3. 安装Docker和Docker Compose

```bash
# 安装Docker
curl -fsSL https://get.docker.com | sh

# 安装Docker Compose
curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
chmod +x /usr/local/bin/docker-compose

# 启动Docker服务
 systemctl start docker
 systemctl enable docker
```

## 部署OpenAgents网络

### 1. 克隆项目

```bash
git clone https://github.com/openagents-org/openagents.git
cd openagents
```

如果没有Git，先安装：
```bash
# CentOS/RHEL
yum install git -y

# Ubuntu/Debian
apt install git -y
```

### 2. 复制您的网络配置

将本地的 `my_first_network` 目录复制到服务器上：

```bash
# 在本地执行
 scp -r my_first_network root@112.28.0.160:/root/openagents/
```

### 3. 创建环境变量文件

```bash
cd /root/openagents
touch .env
nano .env
```

在 `.env` 文件中添加以下内容：

```env
OPENAGENTS_JWT_SECRET=your_secure_jwt_secret_key_here
OPENAGENTS_HOST=112.28.0.160
```

### 4. 构建Docker镜像

```bash
docker-compose build
```

### 5. 启动系统

```bash
docker-compose up -d
```

### 6. 验证部署

检查容器状态：

```bash
docker-compose ps
```

查看日志：

```bash
docker-compose logs -f
```

## 网络配置

### 1. 配置防火墙

```bash
# 开放端口 8600 (gRPC) 和 8700 (HTTP)

# CentOS/RHEL
firewall-cmd --permanent --add-port=8600/tcp
firewall-cmd --permanent --add-port=8700/tcp
firewall-cmd --reload

# Ubuntu/Debian
ufw allow 8600/tcp
ufw allow 8700/tcp
ufw reload
```

### 2. 配置网络配置文件

更新 `my_first_network/network.yaml` 文件中的网络配置：

```bash
nano /root/openagents/my_first_network/network.yaml
```

修改以下部分：

```yaml
network_profile:
  # ...
  authentication:
    type: "jwt"
    config:
      secret_key: "your_secure_jwt_secret_key_here"
  host: "112.28.0.160"  # 公网IP
  port: 8700
```

## 访问OpenAgents网络

部署完成后，您可以通过以下方式访问OpenAgents网络：

- **HTTP访问**: http://112.28.0.160:8700
- **gRPC访问**: 112.28.0.160:8600
- **OpenAgents Studio**: 在浏览器中访问 https://studio.openagents.org，然后连接到您的网络

## 系统维护

### 1. 停止系统

```bash
docker-compose down
```

### 2. 更新系统

```bash
# 拉取最新代码
git pull

# 重新构建镜像
docker-compose build --no-cache

# 重启系统
docker-compose up -d
```

### 3. 查看智能体状态

```bash
docker-compose logs -f diagnosis-agent tutoring-agent review-agent
```

## 故障排除

### 问题：容器无法启动

检查日志：
```bash
docker-compose logs -f <容器名>
```

### 问题：无法访问网络服务

检查端口是否开放：
```bash
netstat -tuln | grep 8700
netstat -tuln | grep 8600
```

检查防火墙配置：
```bash
# CentOS/RHEL
firewall-cmd --list-ports

# Ubuntu/Debian
ufw status
```

## 安全建议

1. **更改默认的JWT密钥**
2. **定期更新Docker镜像**
3. **限制SSH访问**
4. **使用HTTPS（生产环境）**
5. **定期备份数据目录**

---

部署完成后，您的OpenAgents网络将在新服务器上运行，您可以通过公网IP 112.28.0.160 访问和管理您的智能体网络。