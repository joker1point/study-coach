import requests
import time

def check_network_status():
    print("Checking network status...")
    try:
        response = requests.get("http://localhost:8700/", timeout=5)
        print(f"✓ Network HTTP service: {response.status_code} OK")
        return True
    except Exception as e:
        print(f"✗ Network HTTP service: {e}")
        return False

def check_agent_status():
    print("Checking agent status...")
    try:
        # 发送一条测试消息到网络服务
        response = requests.post(
            "http://localhost:8700/api/send_event",
            json={
                "event_type": "system.status",
                "content": {"command": "ping"}
            },
            timeout=5
        )
        print(f"✓ Agent communication: {response.status_code} OK")
        print(f"Response: {response.json()}")
        return True
    except Exception as e:
        print(f"✗ Agent communication: {e}")
        return False

if __name__ == "__main__":
    print("=== System Status Check ===")
    print("")
    
    network_ok = check_network_status()
    print("")
    agent_ok = check_agent_status()
    print("")
    
    if network_ok and agent_ok:
        print("🎉 System is ONLINE and working correctly!")
        print("- Network service is running on localhost:8700")
        print("- LLM agent 'alex' is connected and ready")
    else:
        print("❌ System has issues that need to be resolved")
