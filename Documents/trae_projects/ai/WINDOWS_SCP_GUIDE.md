# Windows 系统文件传输指南

## 问题分析

从您的终端输出可以看到，您在使用 `scp` 命令时遇到了两个问题：

1. **命令语法错误**：`scp` 命令的正确格式应该是 `scp [选项] 源文件 用户@主机:目标路径`
2. **Windows 可能未启用 OpenSSH**：Windows 默认可能没有安装或启用 OpenSSH 功能

## 解决方案

### 方案一：启用 Windows OpenSSH 功能

#### 1. 以管理员身份打开 PowerShell

- 右键点击开始菜单，选择"Windows PowerShell(管理员)"
- 或者搜索"PowerShell"，右键点击并选择"以管理员身份运行"

#### 2. 安装 OpenSSH 客户端

```powershell
Add-WindowsCapability -Online -Name OpenSSH.Client~~~~0.0.1.0
```

#### 3. 验证安装

```powershell
ssh -V
scp -V
```

### 方案二：使用正确的 SCP 命令语法

启用 OpenSSH 后，使用正确的命令格式：

```bash
# 从当前目录复制整个 my_first_network 文件夹到服务器
scp -r my_first_network root@112.28.0.160:/root/openagents/
```

**注意**：
- 确保在命令中包含完整的目标路径
- 如果服务器的 SSH 端口不是默认的 22，请使用 `-P 端口号` 选项
- 首次连接时会提示确认服务器指纹，输入 "yes" 确认

### 方案三：使用图形化工具 WinSCP

如果您更习惯使用图形界面，可以使用 WinSCP：

#### 1. 下载并安装 WinSCP

从官网下载：[https://winscp.net/eng/download.php](https://winscp.net/eng/download.php)

#### 2. 配置连接

- **协议**：选择 "SFTP"
- **主机名**：112.28.0.160
- **端口号**：22
- **用户名**：root
- **密码**：输入您的服务器密码

#### 3. 传输文件

- 左侧浏览到本地的 `my_first_network` 文件夹
- 右侧浏览到服务器的 `/root/openagents/` 目录
- 将左侧的文件夹拖拽到右侧即可完成传输

## 其他注意事项

1. **防火墙设置**：确保服务器的 22 端口（SSH）已开放
2. **文件权限**：传输完成后，可以在服务器上使用 `ls -la /root/openagents/` 检查文件权限
3. **中文路径**：尽量避免在文件路径中使用中文，可能会导致传输问题

如果您在使用过程中遇到任何问题，请随时向我咨询！