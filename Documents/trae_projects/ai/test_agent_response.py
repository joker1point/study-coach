# Simple test script to send a message to the learning assistant agent

import requests
import json

# Network configuration
NETWORK_HOST = "localhost"
NETWORK_PORT = 8700

# Message to send
message = "你好，学习助手！能帮我简单解释一下Python中的面向对象编程吗？"

# Send a POST request to the network's HTTP API to post a message to the general channel
def send_message_to_channel(channel, message):
    url = f"http://{NETWORK_HOST}:{NETWORK_PORT}/api/channels/{channel}/messages"
    headers = {
        "Content-Type": "application/json"
    }
    payload = {
        "content": {
            "text": message
        },
        "message_type": "channel_message"
    }
    
    try:
        response = requests.post(url, headers=headers, data=json.dumps(payload))
        response.raise_for_status()
        print(f"Message sent to channel {channel} successfully!")
        print(f"Response: {response.json()}")
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error sending message: {str(e)}")
        return None

if __name__ == "__main__":
    print(f"Sending message to general channel: {message}")
    send_message_to_channel("general", message)
    print("Check the OpenAgents Studio for the learning assistant's response.")