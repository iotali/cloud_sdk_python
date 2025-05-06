"""
IoT SDK设备管理示例
"""

import sys
import os

# 将上级目录添加到模块搜索路径中，以便导入iotsdk
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import iotsdk
from iotsdk.utils import pretty_print_json
import base64  # 添加base64模块用于消息编码

# 基础配置
BASE_URL = "http://iot.iwillcloud.com:10081"
TOKEN = "1379b85e-1f7e-4d5b-851d-d13757960bb4"
PRODUCT_KEY = "QrjKUuXE"


def register_device_example():
    """设备注册示例"""
    print("\n===== 设备注册示例 =====")
    
    # 创建客户端
    client = iotsdk.create_client(BASE_URL, TOKEN)
    
    # 创建设备管理器
    device_manager = iotsdk.create_device_manager(client)
    
    # 注册设备
    response = device_manager.register_device(
        product_key=PRODUCT_KEY,
        device_name="32test",
        nick_name="测试设备003"
    )
    
    # 检查结果
    if client.check_response(response):
        print("\n设备注册成功!")
        device_info = response["data"]
        print(f"设备ID: {device_info['deviceId']}")
        print(f"设备密钥: {device_info['deviceSecret']}")
    
    
def query_device_detail_example():
    """设备详情查询示例"""
    print("\n===== 设备详情查询示例 =====")
    
    # 创建客户端
    client = iotsdk.create_client(BASE_URL, TOKEN)
    
    # 创建设备管理器
    device_manager = iotsdk.create_device_manager(client)
    
    # 查询设备详情
    response = device_manager.get_device_detail(device_name="32test")
    
    # 检查结果
    if client.check_response(response):
        print("\n设备详情查询成功!")
        device_info = response["data"]
        print(f"设备ID: {device_info['deviceId']}")
        print(f"设备名称: {device_info['deviceName']}")
        print(f"设备状态: {device_info['status']}")
    
    
def query_device_status_example():
    """设备状态查询示例"""
    print("\n===== 设备状态查询示例 =====")
    
    # 创建客户端
    client = iotsdk.create_client(BASE_URL, TOKEN)
    
    # 创建设备管理器
    device_manager = iotsdk.create_device_manager(client)
    
    # 查询设备状态
    response = device_manager.get_device_status(device_name="32test")
    
    # 检查结果
    if client.check_response(response):
        print("\n设备状态查询成功!")
        status_data = response["data"]
        print(f"设备状态: {status_data['status']}")
        print(f"状态时间戳: {status_data['timestamp']}")
    
    
def batch_query_device_status_example():
    """批量设备状态查询示例"""
    print("\n===== 批量设备状态查询示例 =====")
    
    # 创建客户端
    client = iotsdk.create_client(BASE_URL, TOKEN)
    
    # 创建设备管理器
    device_manager = iotsdk.create_device_manager(client)
    
    # 批量查询设备状态
    device_names = ["48j8EPRYhM", "5Csobg3zCO"]
    response = device_manager.batch_get_device_status(device_name_list=device_names)
    
    # 检查结果
    if client.check_response(response):
        print("\n批量查询设备状态成功!")
        devices_data = response["data"]
        print(f"查询到 {len(devices_data)} 个设备")
        
        for device in devices_data:
            # 直接从设备对象获取状态信息，不需要通过deviceStatus字段
            print(f"设备名称: {device['deviceName']}, 状态: {device['status']}")
            print(f"设备ID: {device['deviceId']}")
            print(f"最后在线时间: {device['lastOnlineTime']}")
            print(f"状态时间戳: {device['timestamp']}")
            print(f"接入IP: {device.get('asAddress', 'N/A')}")
            print("-" * 30)
    
    
def send_rrpc_message_example():
    """发送RRPC消息示例"""
    print("\n===== 发送RRPC消息示例 =====")
    
    # 创建客户端
    client = iotsdk.create_client(BASE_URL, TOKEN)
    
    # 创建设备管理器
    device_manager = iotsdk.create_device_manager(client)
    
    # 发送RRPC消息
    response = device_manager.send_rrpc_message(
        device_name="32test",
        product_key=PRODUCT_KEY,
        message_content="Hello from IoT SDK",
        timeout=5000
    )
    
    # 检查结果
    if client.check_response(response):
        print("\nRRPC消息发送成功!")
        if "payloadBase64Byte" in response:
            print(f"收到响应: {response['payloadBase64Byte']}")
    

def send_custom_command_example():
    """自定义指令下发示例"""
    print("\n===== 自定义指令下发示例 =====")
    
    # 创建客户端
    client = iotsdk.create_client(BASE_URL, TOKEN)
    
    # 准备消息内容（JSON字符串）
    message_content = '{"washingMode": 2, "washingTime": 30}'
    print(f"原始消息内容: {message_content}")
    
    # 将消息内容转换为Base64编码
    message_bytes = message_content.encode('utf-8')
    base64_message = base64.b64encode(message_bytes).decode('utf-8')
    
    # 构建请求体
    payload = {
        "deviceName": "5Csobg3zCO",
        "messageContent": base64_message
    }
    
    # 发送请求到自定义下发指令的API端点
    endpoint = "/api/v1/device/down/record/add/custom"
    response = client._make_request(endpoint, payload)
    
    # 检查结果
    if client.check_response(response):
        print("\n自定义指令下发成功!")
        print(f"响应数据: {response.get('data', {})}")
    else:
        print(f"\n自定义指令下发失败: {response.get('errorMessage', '未知错误')}")


if __name__ == "__main__":
    """运行示例"""
    
    # 选择要运行的示例
    send_custom_command_example()  # 添加新的自定义指令下发示例
    send_rrpc_message_example() 
    register_device_example()
    query_device_detail_example()
    query_device_status_example()
    batch_query_device_status_example()
    