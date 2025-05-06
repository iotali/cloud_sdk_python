# IoT云平台SDK (Python)

这是一个用于连接和管理IoT设备的Python SDK，提供了与IoT云平台交互的简便方法。

## 功能特性

- 设备管理
  - 设备注册 (`register_device.py`)
  - 设备详情查询 (`device_detail.py`)
  - 设备状态查询 (`device_status.py`)
  - 批量设备状态查询 (`batch_device_status.py`)
- 远程控制
  - RRPC消息发送 (`rrpc.py`)

## 安装要求

1. Python 3.6 或更高版本
2. 安装依赖库：

```bash
pip install -r requirements.txt
```

## 快速开始

### 1. 设备注册

```python
from register_device import register_quick_device

# 设置基础配置
base_url = "http://your-iot-platform-url"
token = "your-auth-token"
product_key = "your-product-key"

# 注册设备
result = register_quick_device(
    base_url=base_url,
    token=token,
    device_name="your_device_name",
    nick_name="设备显示名称",
    product_key=product_key
)
```

### 2. 查询设备详情

```python
from device_detail import query_device_detail

# 通过设备名称查询
result = query_device_detail(
    base_url="http://your-iot-platform-url",
    token="your-auth-token",
    device_name="your_device_name"
)

# 或通过设备ID查询
result = query_device_detail(
    base_url="http://your-iot-platform-url",
    token="your-auth-token",
    device_id="your_device_id"
)
```

### 3. 查询设备状态

```python
from device_status import query_device_status

# 查询设备在线状态
result = query_device_status(
    base_url="http://your-iot-platform-url",
    token="your-auth-token",
    device_name="your_device_name"
)
```

### 4. 批量查询设备状态

```python
from batch_device_status import batch_query_device_status

# 批量查询多个设备状态
device_names = ["device1", "device2", "device3"]
result = batch_query_device_status(
    base_url="http://your-iot-platform-url",
    token="your-auth-token",
    device_names=device_names
)
```

### 5. 发送RRPC消息

```python
from rrpc import send_rrpc_message

# 向设备发送RRPC消息
result = send_rrpc_message(
    base_url="http://your-iot-platform-url",
    token="your-auth-token",
    device_name="your_device_name",
    message_content="your_message"
)
```

## 注意事项

- 使用前请确保已获取正确的认证令牌和产品密钥
- 所有API调用都会返回完整的响应内容，便于进一步处理和分析
- 提供了友好的错误处理和提示信息

## 贡献

欢迎提交问题和改进建议，也欢迎通过Pull Request来提交代码贡献。

## 许可证

[添加您的许可证信息] 