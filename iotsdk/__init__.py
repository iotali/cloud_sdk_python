"""
IoT云平台SDK
提供与IoT云平台交互的简便方法
"""

from .client import IoTClient
from .device import DeviceManager

__version__ = "1.0.0"

def create_client(base_url: str, token: str):
    """
    创建IoT客户端
    
    Args:
        base_url: API基础URL
        token: 认证令牌
        
    Returns:
        IoTClient: IoT客户端实例
    """
    return IoTClient(base_url, token)
    
def create_device_manager(client: IoTClient):
    """
    创建设备管理器
    
    Args:
        client: IoT客户端实例
        
    Returns:
        DeviceManager: 设备管理器实例
    """
    return DeviceManager(client) 