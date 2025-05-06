import requests
import json
import base64

url = "http://121.40.253.224:10081/api/v1/device/rrpc"
headers = {
    "Content-Type": "application/json",
    "token": "488820fb-41af-40e5-b2d3-d45a8c576eea"
}
payload = {
    "deviceName": "testcv002",
    "productKey": "kdlxqvXX",
    "requestBase64Byte": "AQMAAAABhAo=",
    "timeout": 5000
}

response = requests.post(url, headers=headers, data=json.dumps(payload))

# 解析JSON响应
response_data = response.json()

# 检查是否成功
if response_data.get("success") == True:
    # 获取Base64编码的字符串
    base64_payload = response_data.get("payloadBase64Byte")
    
    # 解码Base64字符串
    decoded_bytes = base64.b64decode(base64_payload)
    
    # 将字节转换为字符串
    decoded_string = decoded_bytes.decode('utf-8')
    
    # 输出解码后的字符串
    print("解码后的payload:")
    print(decoded_string)
    
    # 如果解码后的字符串是JSON格式，可以进一步解析
    try:
        json_data = json.loads(decoded_string)
        print("解析为JSON:")
        print(json.dumps(json_data, indent=2, ensure_ascii=False))
    except json.JSONDecodeError:
        print("解码后的字符串不是有效的JSON格式")
else:
    print("请求失败:", response_data)