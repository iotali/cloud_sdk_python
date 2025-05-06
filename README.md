# IoT云平台SDK (Python)

这是一个用于连接和管理IoT设备的Python SDK，提供了与IoT云平台交互的简便方法。

## SDK结构

SDK采用模块化设计，主要包含以下组件：

- **IoTClient**: 核心客户端类，处理API请求、认证和基础通信
- **DeviceManager**: 设备管理模块，提供设备相关的所有操作
- **Utils**: 工具函数集，提供格式化、数据处理等辅助功能

## 功能特性

- 设备管理
  - 设备注册
  - 设备详情查询
  - 设备状态查询
  - 批量设备状态查询
- 远程控制
  - RRPC消息发送

## 安装要求

1. Python 3.6 或更高版本
2. 安装依赖库：

```bash
pip install -r requirements.txt
```

## 快速开始

### 1. 创建客户端和设备管理器

```python
import iotsdk

# 创建IoT客户端
client = iotsdk.create_client(
    base_url="http://your-iot-platform-url",
    token="your-auth-token"
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

# 或者通过设备ID列表查询
device_ids = ["id1", "id2", "id3"]
response = device_manager.batch_get_device_status(device_id_list=device_ids)
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
```

## 示例代码

参见 `examples` 目录下的示例文件，展示了SDK的具体用法。

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

# 创建带自定义日志的客户端
client = iotsdk.create_client(
    base_url="http://your-iot-platform-url",
    token="your-auth-token",
    logger=logger
)
```

## 注意事项

- 使用前请确保已获取正确的认证令牌和产品密钥
- 所有API调用都会返回完整的响应内容，便于进一步处理和分析

## 贡献

欢迎提交问题和改进建议，也欢迎通过Pull Request来提交代码贡献。

## 许可证

MIT License