import requests
import json

def register_quick_device(base_url, token, device_name=None, nick_name=None, product_key=None):
    """
    调用设备快速注册API
    
    参数:
    base_url (str): API基础URL
    token (str): 认证令牌
    device_name (str, optional): 设备标识码。若未提供，系统将自动生成
    nick_name (str, optional): 设备人性化名称。若未提供，系统将使用deviceName作为默认值
    product_key (str): 产品唯一标识码
    
    返回:
    dict: API响应结果
    """
    # 构建API端点
    endpoint = f"{base_url}/api/v1/quickdevice/register"
    
    # 构建请求体
    payload = {
        "productKey": product_key
    }
    
    # 添加可选参数
    if device_name:
        payload["deviceName"] = device_name
    
    if nick_name:
        payload["nickName"] = nick_name
    
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
            print("\n✅ 设备注册成功!")
            print("设备ID:", result["data"]["deviceId"])
            print("设备密钥:", result["data"]["deviceSecret"])
        else:
            print("\n❌ 设备注册失败!")
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
    
    # 设置产品密钥 (必填项)
    product_key = "kdlxqvXX"
    
    # 设置可选参数
    device_name = "test_device_001"
    nick_name = "客厅测试设备"
    
    # 调用API
    result = register_quick_device(
        base_url=base_url,
        token=token,
        device_name=device_name,
        nick_name=nick_name,
        product_key=product_key
    )
    
    # 如果注册成功，保存设备信息以便后续使用
    if result and result.get("success"):
        device_info = result["data"]
        print("\n设备信息摘要:")
        print(f"产品密钥: {device_info['productKey']}")
        print(f"设备名称: {device_info['deviceName']}")
        print(f"显示名称: {device_info['nickName']}")
        print(f"设备ID: {device_info['deviceId']}")
        print(f"设备密钥: {device_info['deviceSecret']}")