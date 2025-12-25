# 网络连接故障排除指南

## 问题分析
网络服务器在本地运行成功，但通过花生壳域名的外部访问超时。这表明存在端口转发或防火墙问题。

## 步骤1：验证本地服务器状态
首先，确认服务器在本地运行且可访问：

```powershell
# 检查服务器是否正在运行
tasklist | findstr "python"

# 测试本地健康检查
curl.exe -s http://localhost:8700/api/health
```

## 步骤2：检查网络绑定配置
确保服务器绑定到正确的网络接口。当前 `network.yaml` 中的配置看起来是正确的（绑定到 0.0.0.0:8700），但让我们验证一下：

```powershell
# 检查哪些进程正在监听8700端口
netstat -an | findstr "8700"
```

您应该看到类似以下内容：
```
TCP    0.0.0.0:8700           0.0.0.0:0              LISTENING
```

## 步骤3：验证花生壳端口转发
1. 打开花生壳应用程序
2. 检查端口转发配置：
   - 确保内部IP地址与您计算机的本地IP匹配（例如，192.168.x.x）
   - 确保内部端口设置为8700
   - 确保外部端口也设置为8700（或验证配置了什么外部端口）
   - 确保协议设置为TCP

## 步骤4：检查Windows防火墙设置
1. 打开Windows Defender防火墙
2. 点击"高级设置"
3. 检查入站和出站规则：
   - 确保有允许TCP流量通过8700端口的入站规则
   - 确保有允许TCP流量通过8700端口的出站规则
   - 如果没有规则存在，为8700端口创建新规则

## 步骤5：测试外部端口可访问性
使用端口检查工具验证8700端口是否可以从外部访问：

1. 访问 https://www.canyouseeme.org/
2. 输入端口8700
3. 点击"Check Port"

## 步骤6：验证花生壳域名状态
检查花生壳域名是否正确解析且服务正在运行：

```powershell
# 检查DNS解析
nslookup 1nz171374pe64.vicp.fun

# 检查域名是否可达（即使端口关闭）
ping 1nz171374pe64.vicp.fun
```

## 步骤7：重启服务
1. 重启花生壳应用程序
2. 重启OpenAgents网络服务器：

```powershell
# 首先，停止所有运行的实例
Stop-Process -Name "python" -ErrorAction SilentlyContinue

# 然后重启服务器
cd c:\Users\biren\Documents\trae_projects\ai
python -m openagents network start ./my_first_network
```

## 步骤8：使用替代端口测试
如果您的ISP阻止了8700端口，请尝试使用不同的端口：

1. 更新 `network.yaml` 使用不同的端口（例如，8080）：
   ```yaml
   transports:
     - type: "http"
       config:
         host: "0.0.0.0"
         port: 8080
         cors_enabled: true
   ```

2. 更新花生壳端口转发以使用新端口
3. 重启服务器
4. 测试新端口

## 步骤9：检查路由器配置
如果您在路由器后面，请确保：
1. 路由器上启用了UPnP（用于自动端口转发）
2. 如果UPnP已禁用，请在路由器上手动配置端口转发：
   - 将外部端口8700转发到内部IP:8700
   - 使用TCP协议

## 预期结果
解决连接问题后，您应该能够从外部访问健康检查端点：

```powershell
curl.exe -s http://1nz171374pe64.vicp.fun:8700/api/health
```

这应该返回与本地健康检查类似的JSON响应。

## 注意事项
- 如果您在公共网络（学校、办公室）上，可能有网络限制阻止端口转发
- 一些ISP出于安全原因阻止常用端口
- 确保您的计算机有静态本地IP地址，以避免重启后端口转发配置问题