# 花生壳端口映射配置指南与故障排除

## 问题分析总结

经过详细检查，我们发现以下问题：

1. **域名解析问题**：花生壳域名 `1nz171374pe64.vicp.fan` 无法通过 DNS 正确解析
2. **端口映射配置**：花生壳已配置正确的端口映射（OpenAgents: 80 → 192.168.194.179:8701；Ollama: 38502 → 192.168.194.179:8700）
3. **本地服务状态**：OpenAgents 网络服务在本地运行正常（0.0.0.0:8701）

## 配置建议

### 1. 花生壳客户端配置

**检查花生壳客户端状态**：
- 确保花生壳客户端已登录并运行
- 检查客户端中的域名状态是否为"在线"
- 验证域名解析是否正常：`nslookup 1nz171374pe64.vicp.fan`

**端口映射配置调整**：
```
OpenAgents 映射：
- 类型：HTTP
- 外网地址：http://1nz171374pe64.vicp.fan
- 内网地址：192.168.194.179:8701

Ollama 映射：
- 类型：HTTP
- 外网地址：http://1nz171374pe64.vicp.fan:38502
- 内网地址：192.168.194.179:8700
```

### 2. OpenAgents 网络配置

**network.yaml 正确配置**：
```yaml
network:
  name: "Test Network Offline 2"
  mode: "centralized"
  node_id: "test-network-offline-2"

  transports:
    - type: "http"
      config:
        host: "0.0.0.0"
        port: 8701
        cors_enabled: true
    - type: "grpc"
      config:
        host: "0.0.0.0"
        port: 8600

network_profile:
  discoverable: true
  name: "Production Learning Assistant Network"
  description: "A production OpenAgents network for personalized learning assistance"
  authentication:
    type: "none"
  host: "1nz171374pe64.vicp.fan"
  port: 80

log_level: "INFO"
```

### 3. 本地服务验证

**检查 OpenAgents 服务状态**：
```bash
# 查看服务是否运行
curl http://localhost:8701/api/health

# 检查端口监听
netstat -an | findstr "8701"
```

**检查 Ollama 服务状态**：
```bash
# 查看服务是否运行
curl http://localhost:8700/api/tags

# 检查端口监听
netstat -an | findstr "8700"
```

## 故障排除步骤

### 1. 域名解析问题

**问题**：域名无法解析
**解决方法**：
- 检查花生壳客户端是否在线
- 确认域名是否已激活
- 尝试刷新花生壳客户端的 DNS 缓存
- 使用花生壳提供的 IP 直接访问测试：`http://[花生壳公网IP]:[端口]/api/health`

### 2. 端口映射问题

**问题**：域名可解析但无法访问服务
**解决方法**：
- 检查防火墙设置，确保 8701 和 8700 端口已开放
- 验证路由器端口转发配置
- 尝试关闭 Windows Defender 防火墙进行测试
- 检查 ISP 是否屏蔽了相关端口

### 3. 本地服务问题

**问题**：本地服务无法访问
**解决方法**：
- 重启 OpenAgents 网络：`openagents network start my_first_network`
- 检查服务日志获取详细错误信息
- 确认配置文件中的端口设置是否正确

## 替代方案

如果花生壳配置持续出现问题，可以考虑使用以下替代方案：

### 使用 ngrok 进行临时端口映射

1. 下载并安装 ngrok：https://ngrok.com/download
2. 运行以下命令映射 OpenAgents 端口：
   ```bash
   ngrok http 8701
   ```
3. 使用生成的 ngrok URL 访问服务

### 使用 Cloudflare Tunnel

1. 创建 Cloudflare 账户
2. 安装 cloudflared 客户端
3. 运行以下命令创建隧道：
   ```bash
   cloudflared tunnel --url http://localhost:8701
   ```

## 后续维护建议

1. **定期检查 IP 地址**：如果使用动态 IP，定期检查并更新花生壳配置
2. **设置固定 IP**：在路由器中为计算机设置静态 IP 地址
3. **监控服务状态**：定期检查服务是否正常运行
4. **更新软件版本**：保持花生壳客户端、OpenAgents 和 Ollama 为最新版本

## 联系方式

如果问题仍然存在，建议联系：
- 花生壳技术支持：https://service.oray.com/
- OpenAgents 社区：https://openagents.com/community

---

**最后更新时间**：2025-04-09 12:30:00
**状态**：花生壳域名解析问题待解决，本地服务运行正常