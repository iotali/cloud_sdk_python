"""
IoT SDK设备管理示例
"""

import sys
import os

# 将上级目录添加到模块搜索路径中，以便导入iotsdk
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import iotsdk
from iotsdk.client import IoTClient  # 直接导入IoTClient类
from iotsdk.utils import pretty_print_json
import base64  # 添加base64模块用于消息编码

# 基础配置
BASE_URL = "https://xxx.xxx.com"

PRODUCT_KEY = "NrateJMx"
# 应用凭证配置
APP_ID = "app-680***"
APP_SECRET = "6808aa30614c4c9f3238***"


def initialize_client_with_credentials_example():
    """使用应用凭证初始化客户端示例"""
    print("\n===== 使用应用凭证初始化客户端示例 =====")
    
    # 使用应用凭证初始化客户端
    client = IoTClient.from_credentials(  # 使用直接导入的IoTClient类
        base_url=BASE_URL,
        app_id=APP_ID,
        app_secret=APP_SECRET
    )
    
    print("\n客户端初始化成功!")
    print(f"Base URL: {client.base_url}")
    print(f"Token: {client.token[:10]}...") # 只显示token的前10个字符
    
    return client


def register_device_example(client):
    """设备注册示例"""
    print("\n===== 设备注册示例 =====")
    
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
    
    
def query_device_detail_example(client):
    """设备详情查询示例"""
    print("\n===== 设备详情查询示例 =====")
    
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
    
    
def query_device_status_example(client):
    """设备状态查询示例"""
    print("\n===== 设备状态查询示例 =====")
    
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
    
    
def batch_query_device_status_example(client):
    """批量设备状态查询示例"""
    print("\n===== 批量设备状态查询示例 =====")
    
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
    
    
def send_rrpc_message_example(client):
    """发送RRPC消息示例"""
    print("\n===== 发送RRPC消息示例 =====")
    
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
    

def send_custom_command_example(client):
    """自定义指令下发示例"""
    print("\n===== 自定义指令下发示例 =====")
    
    # 准备消息内容（JSON字符串）
    message_content = '{"washingMode": 2, "washingTime": 30}'
    print(f"原始消息内容: {message_content}")
    
    # 将消息内容转换为Base64编码
    message_bytes = message_content.encode('utf-8')
    base64_message = base64.b64encode(message_bytes).decode('utf-8')
    
    # 构建请求体
    payload = {
        "deviceName": "32test",
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


def test_client_functionality(client):
    """测试客户端基本功能"""
    print("\n===== 测试客户端功能 =====")
    
    # 创建设备管理器
    device_manager = iotsdk.create_device_manager(client)
    
    # 查询设备状态
    response = device_manager.get_device_status(device_name="32test")
    
    # 检查结果
    if client.check_response(response):
        print("\n使用客户端测试成功!")
        status_data = response.get("data", {})
        print(f"设备状态: {status_data.get('status', 'N/A')}")
    else:
        print("\n操作失败!")


if __name__ == "__main__":
    """运行示例"""
    
    # 首先创建一个全局客户端实例，后续所有示例共用此实例
    print("\n===== 创建SDK客户端 =====")
    print("使用应用凭证自动获取token...")
    client = initialize_client_with_credentials_example()
    register_device_example(client)
    query_device_detail_example(client)
    
    # 测试客户端基本功能
    test_client_functionality(client)
    
    # 运行各个功能示例，复用同一个客户端实例
    send_custom_command_example(client)
    send_rrpc_message_example(client)
    
    
    query_device_status_example(client)
    batch_query_device_status_example(client)
    
    print("\n===== 示例运行完成 =====")
    print("一个客户端实例被用于执行所有API调用")
    