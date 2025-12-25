# 花生壳端口转发配置指南

根据您提供的花生壳界面截图，我发现当前配置需要进行调整以正确指向您的OpenAgents网络。以下是详细的配置步骤：

## 1. 花生壳配置调整

### 当前花生壳配置：
- 内网主机：192.168.85.179（正确）
- 内网端口：11434（需要修改为8700）
- 外网域名：https://me173714pe6e4.vip.gz.fastweb.com.cn
- 外网端口：443

### 需要修改的配置：
**内网端口**：将`11434`修改为`8700`（OpenAgents网络的HTTP端口）

这样花生壳才能将外部请求正确转发到您运行的OpenAgents网络服务上。

## 2. OpenAgents网络配置检查

您的OpenAgents网络配置已经正确设置：
- HTTP服务运行在`0.0.0.0:8700`
- 网络配置中的主机地址是`192.168.85.179`

## 3. 发布网络时的参数填写

修改花生壳配置后，在OpenAgents控制台发布网络时，请使用以下参数：

- **Network ID**：production-network-1
- **Network Name**：Production Learning Assistant Network
- **Network Host**：me173714pe6e4.vip.gz.fastweb.com.cn（花生壳提供的外网域名）
- **Network Port**：443（花生壳提供的外网端口）

## 4. 验证配置

配置完成后，您可以通过以下方式验证：

1. 确保花生壳服务正常运行
2. 确保OpenAgents网络服务正在运行：`openagents network start ./my_first_network`
3. 在浏览器中访问：https://me173714pe6e4.vip.gz.fastweb.com.cn

如果一切正常，健康检查应该会通过，您的网络将成功发布。

## 5. 常见问题排查

- 如果仍然出现健康检查失败，请检查：
  1. 花生壳的内网端口是否正确设置为8700
  2. OpenAgents网络是否正在运行
  3. 防火墙是否允许端口8700的入站连接
  4. 花生壳的外网域名是否已经生效

希望这些配置指南能帮助您成功发布网络！