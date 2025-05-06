from datetime import datetime
from typing import Optional, Dict, Any
import json

def format_timestamp(timestamp_ms: Optional[int]) -> str:
    """
    将毫秒时间戳格式化为可读字符串
    
    Args:
        timestamp_ms: 毫秒时间戳
        
    Returns:
        str: 格式化后的时间字符串
    """
    if not timestamp_ms:
        return "未知"
        
    try:
        dt = datetime.fromtimestamp(timestamp_ms / 1000)  # 毫秒转秒
        return dt.strftime("%Y-%m-%d %H:%M:%S")
    except Exception:
        return str(timestamp_ms)
        
def format_iso_time(time_str: Optional[str]) -> str:
    """
    将ISO格式时间字符串转换为可读字符串
    
    Args:
        time_str: ISO格式时间字符串
        
    Returns:
        str: 格式化后的时间字符串
    """
    if not time_str:
        return "未知"
        
    try:
        dt = datetime.fromisoformat(time_str.replace("Z", "+00:00"))
        return dt.strftime("%Y-%m-%d %H:%M:%S")
    except Exception:
        return time_str
        
def format_offline_duration(timestamp_ms: int) -> str:
    """
    计算并格式化离线时长
    
    Args:
        timestamp_ms: 离线时的毫秒时间戳
        
    Returns:
        str: 格式化的离线时长
    """
    now_ms = int(datetime.now().timestamp() * 1000)
    offline_duration_ms = now_ms - timestamp_ms
    offline_minutes = offline_duration_ms / (1000 * 60)
    
    if offline_minutes < 60:
        return f"约 {int(offline_minutes)} 分钟"
    
    offline_hours = offline_minutes / 60
    if offline_hours < 24:
        return f"约 {int(offline_hours)} 小时 {int(offline_minutes % 60)} 分钟"
    
    offline_days = int(offline_hours / 24)
    remaining_hours = int(offline_hours % 24)
    return f"约 {offline_days} 天 {remaining_hours} 小时"
    
def pretty_print_json(data: Dict[str, Any]) -> None:
    """
    美化打印JSON数据
    
    Args:
        data: 要打印的JSON数据
    """
    print(json.dumps(data, indent=2, ensure_ascii=False))
    
def get_status_text(status: str) -> str:
    """
    获取设备状态的中文描述
    
    Args:
        status: 设备状态码
        
    Returns:
        str: 状态的中文描述
    """
    status_map = {
        "ONLINE": "在线",
        "OFFLINE": "离线",
        "UNACTIVE": "未激活"
    }
    return status_map.get(status, status) 