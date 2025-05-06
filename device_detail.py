import requests
import json
from datetime import datetime

def query_device_detail(base_url, token, device_name=None, device_id=None):
    """
    调用设备详情查询API
    
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
    endpoint = f"{base_url}/api/v1/quickdevice/detail"
    
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
            print("\n✅ 设备详情查询成功!")
            # 格式化显示设备状态
            device_status = result["data"]["status"]
            status_map = {
                "ONLINE": "在线",
                "OFFLINE": "离线",
                "UNACTIVE": "未激活"
            }
            status_text = status_map.get(device_status, device_status)
            
            # 格式化显示时间
            def format_time(time_str):
                if not time_str:
                    return "未知"
                try:
                    dt = datetime.fromisoformat(time_str.replace("Z", "+00:00"))
                    return dt.strftime("%Y-%m-%d %H:%M:%S")
                except:
                    return time_str
            
            # 显示详细信息
            device_info = result["data"]
            print(f"设备ID: {device_info.get('deviceId', '未知')}")
            print(f"设备名称: {device_info.get('deviceName', '未知')}")
            print(f"设备昵称: {device_info.get('nickName', '未知')}")
            print(f"设备状态: {status_text}")
            print(f"产品密钥: {device_info.get('productKey', '未知')}")
            print(f"产品名称: {device_info.get('productName', '未知')}")
            print(f"设备密钥: {device_info.get('deviceSecret', '未知')}")
            print(f"IP地址: {device_info.get('ipAddress', '未知')}")
            print(f"固件版本: {device_info.get('firmwareVersion', '未知')}")
            print(f"创建时间: {format_time(device_info.get('createTime'))}")
            print(f"激活时间: {format_time(device_info.get('activeTime'))}")
            print(f"上线时间: {format_time(device_info.get('onlineTime'))}")
        else:
            print("\n❌ 设备详情查询失败!")
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
    print("\n通过设备编码查询设备详情:")
    device_name = "test_device_001"  # 替换为您的设备编码
    query_device_detail(base_url, token, device_name=device_name)
    
    # 方式2：通过设备ID查询
    print("\n通过设备ID查询设备详情:")
    device_id = "1918869061958107136"  # 替换为您要查询的设备ID
    query_device_detail(base_url, token, device_id=device_id)
    
    # 您也可以同时提供两个参数
    # query_device_detail(base_url, token, device_name=device_name, device_id=device_id)