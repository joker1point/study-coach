#!/usr/bin/env python3
"""
测试gRPC服务的Python脚本，用于替代grpcurl命令
"""

import grpc
import json
import sys
import socket


def test_grpc_connection(host, port):
    """测试gRPC端口连接"""
    try:
        # 只是测试连接是否建立
        channel = grpc.insecure_channel(f"{host}:{port}")
        # 尝试获取通道状态
        grpc.channel_ready_future(channel).result(timeout=5)
        return True
    except Exception as e:
        print(f"   连接错误: {e}")
        return False


def test_http_connection(host, port):
    """测试HTTP端口连接"""
    import requests
    
    try:
        # 测试OpenAgents的健康检查端点
        url = f"http://{host}:{port}/health"
        response = requests.get(url, timeout=5)
        return {
            "status": response.status_code,
            "content": response.json() if response.headers.get('content-type') == 'application/json' else response.text
        }
    except Exception as e:
        return {
            "error": str(e)
        }


def main():
    """主函数"""
    print("=== OpenAgents 服务测试工具 ===")
    print()
    
    # 默认配置
    host = "localhost"
    http_port = 8700
    grpc_port = 8600
    
    print(f"测试地址: {host}")
    print()
    
    # 测试基本端口连接
    print("1. 测试端口连接:")
    
    # 测试HTTP端口
    http_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    http_socket.settimeout(2)
    http_result = http_socket.connect_ex((host, http_port))
    http_socket.close()
    print(f"   HTTP 端口 {http_port}: {'✅ 开放' if http_result == 0 else '❌ 关闭'}")
    
    # 测试gRPC端口
    grpc_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    grpc_socket.settimeout(2)
    grpc_result = grpc_socket.connect_ex((host, grpc_port))
    grpc_socket.close()
    print(f"   gRPC 端口 {grpc_port}: {'✅ 开放' if grpc_result == 0 else '❌ 关闭'}")
    print()
    
    # 测试HTTP端点
    print("2. 测试 HTTP 服务 (端口 8700):")
    http_result = test_http_connection(host, http_port)
    if "error" in http_result:
        print(f"   错误: {http_result['error']}")
    else:
        print(f"   状态码: {http_result['status']}")
        try:
            print(f"   响应内容: {json.dumps(http_result['content'], indent=2, ensure_ascii=False)}")
        except:
            print(f"   响应内容: {http_result['content']}")
    print()
    
    # 测试gRPC服务
    print("3. 测试 gRPC 服务 (端口 8600):")
    if test_grpc_connection(host, grpc_port):
        print("   ✅ gRPC 服务连接成功")
    else:
        print("   ❌ gRPC 服务连接失败")
    print()
    
    print("=== 测试完成 ===")


if __name__ == "__main__":
    main()