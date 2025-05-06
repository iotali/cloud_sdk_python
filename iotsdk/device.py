from typing import Dict, List, Optional, Union, Any
from datetime import datetime
import logging

from .client import IoTClient

class DeviceManager:
    """设备管理模块，提供设备相关操作"""
    
    def __init__(self, client: IoTClient):
        """
        初始化设备管理模块
        
        Args:
            client: IoT客户端实例
        """
        self.client = client
        self.logger = client.logger
        
    def register_device(self, 
                        product_key: str, 
                        device_name: Optional[str] = None, 
                        nick_name: Optional[str] = None) -> Dict:
        """
        注册设备
        
        Args:
            product_key: 产品唯一标识码
            device_name: 设备标识码，可选，若未提供则自动生成
            nick_name: 设备显示名称，可选
            
        Returns:
            Dict: 注册结果，包含设备ID和密钥等信息
        """
        endpoint = "/api/v1/quickdevice/register"
        
        # 构建请求体
        payload = {
            "productKey": product_key
        }
        
        # 添加可选参数
        if device_name:
            payload["deviceName"] = device_name
            
        if nick_name:
            payload["nickName"] = nick_name
            
        # 发送请求
        response = self.client._make_request(endpoint, payload)
        
        # 检查结果并格式化输出
        if self.client.check_response(response):
            device_info = response["data"]
            self.logger.info(f"设备注册成功: {device_info['deviceName']}")
            
            # 输出详细信息
            self.logger.info("设备信息摘要:")
            self.logger.info(f"产品密钥: {device_info['productKey']}")
            self.logger.info(f"设备名称: {device_info['deviceName']}")
            self.logger.info(f"显示名称: {device_info['nickName']}")
            self.logger.info(f"设备ID: {device_info['deviceId']}")
            self.logger.info(f"设备密钥: {device_info['deviceSecret']}")
        
        return response
        
    def get_device_detail(self, 
                          device_name: Optional[str] = None, 
                          device_id: Optional[str] = None) -> Dict:
        """
        查询设备详情
        
        Args:
            device_name: 设备编码，可选
            device_id: 设备唯一标识，可选
            
        Returns:
            Dict: 设备详情信息
            
        注意:
            device_name和device_id至少需要提供一个
        """
        # 参数验证
        if not device_name and not device_id:
            raise ValueError("设备编码(deviceName)和设备ID(deviceId)至少需要提供一个")
            
        endpoint = "/api/v1/quickdevice/detail"
        
        # 构建请求体
        payload = {}
        if device_name:
            payload["deviceName"] = device_name
        if device_id:
            payload["deviceId"] = device_id
            
        # 发送请求
        response = self.client._make_request(endpoint, payload)
        
        # 检查结果并格式化输出
        if self.client.check_response(response):
            device_info = response["data"]
            device_status = device_info["status"]
            
            # 格式化设备状态
            status_map = {
                "ONLINE": "在线",
                "OFFLINE": "离线",
                "UNACTIVE": "未激活"
            }
            status_text = status_map.get(device_status, device_status)
            
            # 输出设备基础信息
            self.logger.info(f"设备ID: {device_info.get('deviceId', '未知')}")
            self.logger.info(f"设备名称: {device_info.get('deviceName', '未知')}")
            self.logger.info(f"设备状态: {status_text}")
            
        return response
        
    def get_device_status(self, 
                          device_name: Optional[str] = None, 
                          device_id: Optional[str] = None) -> Dict:
        """
        查询设备在线状态
        
        Args:
            device_name: 设备编码，可选
            device_id: 设备唯一标识，可选
            
        Returns:
            Dict: 设备状态信息
            
        注意:
            device_name和device_id至少需要提供一个
        """
        # 参数验证
        if not device_name and not device_id:
            raise ValueError("设备编码(deviceName)和设备ID(deviceId)至少需要提供一个")
            
        endpoint = "/api/v1/quickdevice/status"
        
        # 构建请求体
        payload = {}
        if device_name:
            payload["deviceName"] = device_name
        if device_id:
            payload["deviceId"] = device_id
            
        # 发送请求
        response = self.client._make_request(endpoint, payload)
        
        # 检查结果并格式化输出
        if self.client.check_response(response):
            status_data = response["data"]
            device_status = status_data.get("status")
            timestamp_ms = status_data.get("timestamp")
            
            # 状态映射
            status_map = {
                "ONLINE": "在线",
                "OFFLINE": "离线",
                "UNACTIVE": "未激活"
            }
            status_text = status_map.get(device_status, device_status)
            
            # 时间戳格式化
            if timestamp_ms:
                dt = datetime.fromtimestamp(timestamp_ms / 1000)  # 毫秒转秒
                time_str = dt.strftime("%Y-%m-%d %H:%M:%S")
            else:
                time_str = "未知"
                
            # 显示状态信息
            self.logger.info(f"设备状态: {status_text}")
            self.logger.info(f"状态更新时间: {time_str}")
            
            # 如果设备离线，计算离线时长
            if device_status == "OFFLINE" and timestamp_ms:
                now_ms = int(datetime.now().timestamp() * 1000)
                offline_duration_ms = now_ms - timestamp_ms
                offline_minutes = offline_duration_ms / (1000 * 60)
                
                if offline_minutes < 60:
                    offline_text = f"约 {int(offline_minutes)} 分钟"
                else:
                    offline_hours = offline_minutes / 60
                    if offline_hours < 24:
                        offline_text = f"约 {int(offline_hours)} 小时 {int(offline_minutes % 60)} 分钟"
                    else:
                        offline_days = int(offline_hours / 24)
                        remaining_hours = int(offline_hours % 24)
                        offline_text = f"约 {offline_days} 天 {remaining_hours} 小时"
                
                self.logger.info(f"离线时长: {offline_text}")
                
        return response
        
    def batch_get_device_status(self, 
                                device_name_list: Optional[List[str]] = None, 
                                device_id_list: Optional[List[str]] = None) -> Dict:
        """
        批量查询设备运行状态
        
        Args:
            device_name_list: 设备编码列表，可选
            device_id_list: 设备唯一标识列表，可选
            
        Returns:
            Dict: 批量设备状态信息
            
        注意:
            device_name_list和device_id_list至少需要提供一个
        """
        # 参数验证
        if not device_name_list and not device_id_list:
            raise ValueError("设备编码列表(deviceName)和设备ID列表(deviceId)至少需要提供一个")
            
        # 检查设备数量限制
        device_count = len(device_name_list or []) + len(device_id_list or [])
        if device_count > 100:
            raise ValueError(f"单次请求最多支持查询100个设备，当前请求包含{device_count}个设备")
            
        endpoint = "/api/v1/quickdevice/batchGetDeviceState"
        
        # 构建请求体
        payload = {}
        if device_name_list:
            payload["deviceName"] = device_name_list
        if device_id_list:
            payload["deviceId"] = device_id_list
            
        # 发送请求
        response = self.client._make_request(endpoint, payload)
        
        # 检查结果并统计输出
        if self.client.check_response(response):
            # 统计各状态设备数量
            status_counts = {"ONLINE": 0, "OFFLINE": 0, "UNACTIVE": 0}
            
            # 获取设备状态列表
            devices_data = response.get("data", [])
            self.logger.info(f"共返回 {len(devices_data)} 个设备信息")
            
            # 遍历统计
            for device_info in devices_data:
                device_status = device_info.get("deviceStatus", {})
                status = device_status.get("status", "未知")
                
                # 更新状态计数
                if status in status_counts:
                    status_counts[status] += 1
            
            # 打印设备状态统计
            self.logger.info(f"在线设备: {status_counts['ONLINE']} 台, " +
                           f"离线设备: {status_counts['OFFLINE']} 台, " +
                           f"未激活设备: {status_counts['UNACTIVE']} 台")
                
        return response
        
    def send_rrpc_message(self, 
                         device_name: str, 
                         product_key: str, 
                         message_content: str, 
                         timeout: int = 5000) -> Dict:
        """
        发送RRPC消息
        
        Args:
            device_name: 设备编码
            product_key: 产品唯一标识码
            message_content: 消息内容
            timeout: 超时时间(毫秒)，默认5000ms
            
        Returns:
            Dict: 消息发送结果
        """
        import base64
        
        endpoint = "/api/v1/device/rrpc"
        
        # 消息内容Base64编码
        message_bytes = message_content.encode('utf-8')
        base64_message = base64.b64encode(message_bytes).decode('utf-8')
        
        # 构建请求体
        payload = {
            "deviceName": device_name,
            "productKey": product_key,
            "requestBase64Byte": base64_message,
            "timeout": timeout
        }
        
        # 发送请求
        response = self.client._make_request(endpoint, payload)
        
        # 检查结果并解析响应
        if self.client.check_response(response):
            # 获取Base64编码的响应
            base64_payload = response.get("payloadBase64Byte")
            
            if base64_payload:
                # 解码Base64字符串
                try:
                    decoded_bytes = base64.b64decode(base64_payload)
                    decoded_string = decoded_bytes.decode('utf-8')
                    
                    self.logger.info("解码后的响应内容:")
                    self.logger.info(decoded_string)
                    
                    # 尝试解析为JSON
                    try:
                        import json
                        json_data = json.loads(decoded_string)
                        self.logger.info("解析为JSON成功")
                    except json.JSONDecodeError:
                        self.logger.debug("响应内容不是有效的JSON格式")
                        
                except Exception as e:
                    self.logger.error(f"解析响应内容失败: {e}")
            else:
                self.logger.warning("响应中没有包含payloadBase64Byte字段")
                
        return response 