import requests
import json
from datetime import datetime

def batch_query_device_status(base_url, token, device_name_list=None, device_id_list=None):
    """
    调用批量查询设备运行状态API
    
    参数:
    base_url (str): API基础URL
    token (str): 认证令牌
    device_name_list (list, optional): 设备编码列表
    device_id_list (list, optional): 设备唯一标识列表
    
    返回:
    dict: API响应结果
    """
    # 参数验证
    if not device_name_list and not device_id_list:
        raise ValueError("设备编码列表(deviceName)和设备ID列表(deviceId)至少需要提供一个")
    
    if device_name_list and device_id_list:
        print("警告: 同时提供了deviceName和deviceId列表，根据API说明，这可能导致不可预期的结果")
    
    # 检查设备数量限制
    device_count = len(device_name_list or []) + len(device_id_list or [])
    if device_count > 100:
        raise ValueError(f"单次请求最多支持查询100个设备，当前请求包含{device_count}个设备")
    
    # 构建API端点
    endpoint = f"{base_url}/api/v1/quickdevice/batchGetDeviceState"
    
    # 构建请求体
    payload = {}
    if device_name_list:
        payload["deviceName"] = device_name_list
    if device_id_list:
        payload["deviceId"] = device_id_list
    
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
            print("\n✅ 批量设备状态查询成功!")
            
            # 统计各状态设备数量
            status_counts = {"ONLINE": 0, "OFFLINE": 0, "UNACTIVE": 0}
            
            # 获取设备状态列表
            devices_data = result.get("data", [])
            print(f"共返回 {len(devices_data)} 个设备信息")
            
            if devices_data:
                print("\n设备状态列表:")
                print("-" * 80)
                print(f"{'设备ID':<25} {'设备名称':<20} {'状态':<12} {'最后在线时间':<25} {'IP地址':<15}")
                print("-" * 80)
                
                for device_info in devices_data:
                    device_status = device_info.get("deviceStatus", {})
                    
                    # 提取设备信息
                    device_id = device_status.get("deviceId", "未知")
                    device_name = device_status.get("deviceName", "未知")
                    status = device_status.get("status", "未知")
                    
                    # 更新状态计数
                    if status in status_counts:
                        status_counts[status] += 1
                    
                    # 转换状态为中文
                    status_map = {
                        "ONLINE": "在线",
                        "OFFLINE": "离线",
                        "UNACTIVE": "未激活"
                    }
                    status_text = status_map.get(status, status)
                    
                    # 处理时间戳 - 注意API返回的是数值类型或ISO格式字符串
                    last_online_time = device_status.get("lastOnlineTime")
                    time_str = "未知"
                    
                    if last_online_time:
                        # 尝试处理为数值时间戳
                        if isinstance(last_online_time, (int, float)):
                            dt = datetime.fromtimestamp(last_online_time / 1000)
                            time_str = dt.strftime("%Y-%m-%d %H:%M:%S")
                        # 尝试处理为ISO格式字符串
                        elif isinstance(last_online_time, str):
                            try:
                                # 移除Z和毫秒部分
                                dt_str = last_online_time.replace("Z", "+00:00")
                                dt = datetime.fromisoformat(dt_str)
                                time_str = dt.strftime("%Y-%m-%d %H:%M:%S")
                            except:
                                time_str = last_online_time
                    
                    # 获取IP地址
                    ip_address = device_status.get("asAddress", "未知")
                    
                    # 打印设备信息
                    print(f"{device_id:<25} {device_name:<20} {status_text:<12} {time_str:<25} {ip_address:<15}")
                
                # 打印设备状态统计
                print("-" * 80)
                print(f"在线设备: {status_counts['ONLINE']} 台, 离线设备: {status_counts['OFFLINE']} 台, 未激活设备: {status_counts['UNACTIVE']} 台")
            else:
                print("没有找到符合条件的设备")
        else:
            print("\n❌ 批量设备状态查询失败!")
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
    
    # 示例1: 通过设备编码列表查询
    device_name_list = ["test_device_001", "hbqPvaMbBQ"]
    print("\n通过设备编码列表查询设备状态:")
    batch_query_device_status(base_url, token, device_name_list=device_name_list)
    
    # 示例2: 通过设备ID列表查询
    device_id_list = ["1919529369445859328", "1917119950812610560"]
    print("\n通过设备ID列表查询设备状态:")
    batch_query_device_status(base_url, token, device_id_list=device_id_list)