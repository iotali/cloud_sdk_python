"""
IoT SDK设备管理示例
"""

import sys
import os

# 将上级目录添加到模块搜索路径中，以便导入iotsdk
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import iotsdk
from iotsdk.utils import pretty_print_json

# 基础配置
BASE_URL = "http://121.40.253.224:10081"
TOKEN = "488820fb-41af-40e5-b2d3-d45a8c576eea"
PRODUCT_KEY = "kdlxqvXX"


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
        device_name="test_device_002",
        nick_name="测试设备002"
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
    response = device_manager.get_device_detail(device_name="test_device_001")
    
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
    response = device_manager.get_device_status(device_name="test_device_001")
    
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
    device_names = ["test_device_001", "hbqPvaMbBQ"]
    response = device_manager.batch_get_device_status(device_name_list=device_names)
    
    # 检查结果
    if client.check_response(response):
        print("\n批量查询设备状态成功!")
        devices_data = response["data"]
        print(f"查询到 {len(devices_data)} 个设备")
        
        for device in devices_data:
            device_status = device["deviceStatus"]
            print(f"设备名称: {device_status['deviceName']}, 状态: {device_status['status']}")
    
    
def send_rrpc_message_example():
    """发送RRPC消息示例"""
    print("\n===== 发送RRPC消息示例 =====")
    
    # 创建客户端
    client = iotsdk.create_client(BASE_URL, TOKEN)
    
    # 创建设备管理器
    device_manager = iotsdk.create_device_manager(client)
    
    # 发送RRPC消息
    response = device_manager.send_rrpc_message(
        device_name="testcv002",
        product_key=PRODUCT_KEY,
        message_content="Hello from IoT SDK",
        timeout=5000
    )
    
    # 检查结果
    if client.check_response(response):
        print("\nRRPC消息发送成功!")
        if "payloadBase64Byte" in response:
            print(f"收到响应: {response['payloadBase64Byte']}")
    

if __name__ == "__main__":
    """运行示例"""
    
    # 选择要运行的示例
    send_rrpc_message_example() 
    register_device_example()
    query_device_detail_example()
    query_device_status_example()
    batch_query_device_status_example()
    