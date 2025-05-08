# IoT云平台SDK (Python)

这是一个用于连接和管理IoT设备的Python SDK，提供了与IoT云平台交互的简便方法。

## SDK结构

SDK采用模块化设计，主要包含以下组件：

- **IoTClient**: 核心客户端类，处理API请求、认证和基础通信
- **DeviceManager**: 设备管理模块，提供设备相关的所有操作
- **Utils**: 工具函数集，提供格式化、数据处理等辅助功能

## 功能特性

- 认证管理
  - 通过token直接认证
  - **新增：** 通过应用凭证(appId/appSecret)自动获取token
- 设备管理
  - 设备注册
  - 设备详情查询
  - 设备状态查询
  - 批量设备状态查询
- 远程控制
  - RRPC消息发送
  - 自定义指令下发（异步）

## 安装要求

1. Python 3.6 或更高版本
2. 安装依赖库：

```bash
pip install -r requirements.txt
```

## 快速开始

### 1. 创建客户端和设备管理器

#### 方式一：使用token创建客户端（传统方式）

```python
import iotsdk

# 创建IoT客户端
client = iotsdk.create_client(
    base_url="https://your-iot-platform-url",
    token="your-auth-token"
)

# 创建设备管理器
device_manager = iotsdk.create_device_manager(client)
```

#### 方式二：使用应用凭证创建客户端（推荐方式）

```python
from iotsdk.client import IoTClient

# 使用应用凭证自动获取token并创建客户端
client = IoTClient.from_credentials(
    base_url="https://your-iot-platform-url",
    app_id="your-app-id",
    app_secret="your-app-secret"
)

# 创建设备管理器
device_manager = iotsdk.create_device_manager(client)
```

### 2. 设备注册

```python
# 注册设备
response = device_manager.register_device(
    product_key="your-product-key",
    device_name="your-device-name",  # 可选
    nick_name="设备显示名称"  # 可选
)

# 检查结果
if client.check_response(response):
    device_info = response["data"]
    print(f"设备ID: {device_info['deviceId']}")
    print(f"设备密钥: {device_info['deviceSecret']}")
```

### 3. 查询设备详情

```python
# 通过设备名称查询
response = device_manager.get_device_detail(device_name="your-device-name")

# 或通过设备ID查询
response = device_manager.get_device_detail(device_id="your-device-id")

# 处理结果
if client.check_response(response):
    device_info = response["data"]
    print(f"设备状态: {device_info['status']}")
```

### 4. 查询设备状态

```python
# 查询设备在线状态
response = device_manager.get_device_status(device_name="your-device-name")

# 处理结果
if client.check_response(response):
    status_data = response["data"]
    print(f"设备状态: {status_data['status']}")
    print(f"状态时间戳: {status_data['timestamp']}")
```

### 5. 批量查询设备状态

```python
# 批量查询多个设备状态
device_names = ["device1", "device2", "device3"]
response = device_manager.batch_get_device_status(device_name_list=device_names)

# 处理结果
if client.check_response(response):
    devices_data = response["data"]
    for device in devices_data:
        print(f"设备名称: {device['deviceName']}")
        print(f"设备状态: {device['status']}")
        print(f"最后在线时间: {device['lastOnlineTime']}")
        print("-------------------")
```

### 6. 发送RRPC消息

```python
# 向设备发送RRPC消息
response = device_manager.send_rrpc_message(
    device_name="your-device-name",
    product_key="your-product-key",
    message_content="Hello Device",
    timeout=5000  # 超时时间(毫秒)
)

# 处理响应
if client.check_response(response):
    if "payloadBase64Byte" in response:
        import base64
        decoded_response = base64.b64decode(response["payloadBase64Byte"]).decode('utf-8')
        print(f"设备响应: {decoded_response}")
```

### 7. 发送自定义指令（异步）

```python
import base64
import json

# 向设备发送自定义指令
message_content = json.dumps({
    'command': 'set_mode',
    'params': {
        'mode': 2,
        'duration': 30
    }
})

# 使用设备管理器发送自定义指令
endpoint = "/api/v1/device/down/record/add/custom"
payload = {
    "deviceName": "your-device-name",
    "messageContent": base64.b64encode(message_content.encode('utf-8')).decode('utf-8')
}
response = client._make_request(endpoint, payload)

if client.check_response(response):
    print("自定义指令下发成功!")
```

## 完整示例

### 使用应用凭证并重用客户端

```python
from iotsdk.client import IoTClient
import iotsdk
import json

# 配置参数
base_url = 'https://your-iot-platform-url'
app_id = 'your-app-id'
app_secret = 'your-app-secret'
product_key = 'your-product-key'

try:
    # 初始化客户端（仅一次）
    client = IoTClient.from_credentials(base_url, app_id, app_secret)
    print(f"客户端初始化成功，Token: {client.token[:10]}...")
    
    # 创建设备管理器
    device_manager = iotsdk.create_device_manager(client)
    
    # 执行多个操作，复用同一个客户端
    device_name = "test-device-1"
    
    # 查询设备状态
    status_response = device_manager.get_device_status(device_name=device_name)
    if client.check_response(status_response):
        status = status_response.get("data", {}).get("status", "unknown")
        print(f"设备状态: {status}")
    
    # 发送指令
    command_json = json.dumps({'command': 'refresh'})
    message_response = device_manager.send_rrpc_message(
        device_name=device_name,
        product_key=product_key,
        message_content=command_json
    )
    
    # 其他操作...
    
except Exception as e:
    print(f"错误: {e}")
```

## 示例代码

参见 `examples` 目录下的示例文件，特别是 `device_examples.py`，展示了如何使用应用凭证初始化客户端并执行各种设备操作。

## 异常处理

SDK提供了统一的异常处理机制：

```python
try:
    response = device_manager.get_device_status(device_name="your-device-name")
    if client.check_response(response):
        # 处理成功响应
        pass
    else:
        # 处理API错误
        error_msg = response.get("errorMessage", "未知错误")
        print(f"API调用失败: {error_msg}")
except Exception as e:
    # 处理网络或其他异常
    print(f"发生异常: {e}")
```

## 自定义日志

SDK支持自定义日志记录器：

```python
import logging

# 创建自定义日志记录器
logger = logging.getLogger("my-iot-app")
logger.setLevel(logging.DEBUG)

# 创建处理器和格式化器
handler = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)

# 创建带自定义日志的客户端（使用token）
client = iotsdk.create_client(
    base_url="https://your-iot-platform-url",
    token="your-auth-token",
    logger=logger
)

# 或使用应用凭证创建
client = IoTClient.from_credentials(
    base_url="https://your-iot-platform-url",
    app_id="your-app-id",
    app_secret="your-app-secret",
    logger=logger
)
```

## 注意事项

- **认证方式**：推荐使用应用凭证方式自动获取token
- **客户端复用**：创建一次客户端实例后在应用程序中复用，避免重复获取token
- 使用前请确保已获取正确的认证令牌/应用凭证和产品密钥
- 所有API调用都会返回完整的响应内容，便于进一步处理和分析
- 自定义指令下发需要设备已订阅相应的主题

## 贡献

欢迎提交问题和改进建议，也欢迎通过Pull Request来提交代码贡献。

## 许可证

MIT License