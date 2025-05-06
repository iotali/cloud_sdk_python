import requests
import json
from datetime import datetime

def query_device_status(base_url, token, device_name=None, device_id=None):
    """
    调用设备在线状态查询API
    
    参数:
    base_url (str): API基础URL
    token (str): 认证令牌
    device_name (str, optional): 设备编码
    device_id (str, optional): 设备唯一标识
    
    返回:
    dict: API响应结果
    """
    # 参数验证
    if not device_name and not device_id:
        raise ValueError("设备编码(deviceName)和设备ID(deviceId)至少需要提供一个")
    
    # 构建API端点
    endpoint = f"{base_url}/api/v1/quickdevice/status"
    
    # 构建请求体
    payload = {}
    if device_name:
        payload["deviceName"] = device_name
    if device_id:
        payload["deviceId"] = device_id
    
    # 设置请求头
    headers = {
        "Content-Type": "application/json",
        "token": token
    }
    
    try:
        # 发送POST请求
        response = requests.post(endpoint, headers=headers, data=json.dumps(payload))
        
        # 解析响应
        result = response.json()
        
        # 打印响应信息
        print("状态码:", response.status_code)
        print("API响应:")
        print(json.dumps(result, indent=2, ensure_ascii=False))
        
        # 检查是否成功
        if result.get("success") == True:
            print("\n✅ 设备状态查询成功!")
            
            # 获取设备状态和时间戳
            status_data = result["data"]
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
            print(f"设备状态: {status_text}")
            print(f"状态更新时间: {time_str}")
            print(f"状态时间戳: {timestamp_ms}")
            
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
                
                print(f"离线时长: {offline_text}")
        else:
            print("\n❌ 设备状态查询失败!")
            print("错误信息:", result.get("errorMessage", "未知错误"))
        
        return result
    
    except Exception as e:
        print(f"请求发生错误: {e}")
        return None

# 使用示例
if __name__ == "__main__":
    # 设置基础URL
    base_url = "http://121.40.253.224:10081"
    
    # 设置认证令牌
    token = "488820fb-41af-40e5-b2d3-d45a8c576eea"
    
    # 方式1：通过设备编码查询
    print("\n通过设备编码查询设备状态:")
    device_name = "test_device_001"  # 替换为您的设备编码
    query_device_status(base_url, token, device_name=device_name)
    
    # 方式2：通过设备ID查询
    print("\n通过设备ID查询设备状态:")
    device_id = "1919379345382572032"  # 替换为您要查询的设备ID
    query_device_status(base_url, token, device_id=device_id)