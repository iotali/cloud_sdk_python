import requests
import json
import logging
from typing import Dict, List, Optional, Union, Any

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)


class IoTClient:
    """
    IoT云平台SDK客户端类
    提供与IoT云平台交互的基础功能
    """
    
    def __init__(self, base_url: str, token: str, logger=None):
        """
        初始化IoT客户端

        Args:
            base_url: API基础URL
            token: 认证令牌
            logger: 可选的日志记录器
        """
        self.base_url = base_url.rstrip('/')
        self.token = token
        self.logger = logger or logging.getLogger('iotsdk')
        
        # 检查参数有效性
        if not self.base_url:
            raise ValueError("无效的base_url")
        if not self.token:
            raise ValueError("无效的token")
            
        self.logger.info(f"IoT客户端已初始化: {self.base_url}")
        
    def _make_request(self, 
                     endpoint: str, 
                     payload: Dict = None, 
                     method: str = 'POST',
                     additional_headers: Dict = None) -> Dict:
        """
        发送API请求的通用方法

        Args:
            endpoint: API端点路径
            payload: 请求体数据
            method: HTTP方法(默认POST)
            additional_headers: 附加的请求头

        Returns:
            Dict: API响应结果
        """
        # 构建完整URL
        url = f"{self.base_url}{endpoint}"
        
        # 设置请求头
        headers = {
            "Content-Type": "application/json",
            "token": self.token
        }
        
        # 添加附加的请求头
        if additional_headers:
            headers.update(additional_headers)
            
        # 准备请求数据
        payload_data = json.dumps(payload) if payload else None
        
        self.logger.debug(f"发送请求: {method} {url}")
        self.logger.debug(f"请求头: {headers}")
        self.logger.debug(f"请求体: {payload_data}")
        
        try:
            # 发送请求
            if method.upper() == 'POST':
                response = requests.post(url, headers=headers, data=payload_data)
            elif method.upper() == 'GET':
                response = requests.get(url, headers=headers, params=payload)
            else:
                raise ValueError(f"不支持的HTTP方法: {method}")
                
            # 检查HTTP状态码
            response.raise_for_status()
            
            # 解析响应
            result = response.json()
            
            self.logger.debug(f"收到响应: {result}")
            
            return result
            
        except requests.exceptions.RequestException as e:
            self.logger.error(f"请求错误: {e}")
            raise
        except json.JSONDecodeError as e:
            self.logger.error(f"JSON解析错误: {e}")
            raise ValueError(f"无法解析响应为JSON: {e}")
            
    def check_response(self, response: Dict) -> bool:
        """
        检查API响应是否成功

        Args:
            response: API响应

        Returns:
            bool: 是否成功
        """
        if not response:
            return False
            
        success = response.get("success", False)
        
        if not success:
            error_msg = response.get("errorMessage", "未知错误")
            self.logger.warning(f"API调用失败: {error_msg}")
            
        return success 