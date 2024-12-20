import requests
import json
from typing import List, Dict
from datetime import datetime
import urllib3

# 禁用SSL警告
urllib3.disable_warnings()

class RetailAPI:
    """
    零售数据上报API客户端
    用于处理与服务器的所有交互，包括登录认证和数据上报
    """
    
    def __init__(self, base_url: str):
        self.base_url = base_url.rstrip('/')
        self.token = None
    
    def login(self, username: str, password: str) -> bool:
        """用户登录并获取访问token"""
        url = f"{self.base_url}/token/grant"
        
        # 设置请求头
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded',
            'Accept': 'application/json',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
            'User-Agent': 'Mozilla/5.0'
        }
        
        # 登录数据
        data = {
            "username": username,
            "password": password  # 使用明文密码，让服务器处理加密
        }
        
        try:
            print(f"正在尝试登录: {url}")
            print(f"用户名: {username}")
            
            response = requests.post(
                url,
                data=data,
                headers=headers,
                verify=False,  # 不验证SSL证书
                timeout=5
            )
            
            print(f"服务器响应状态码: {response.status_code}")
            print(f"服务器响应内容: {response.text}")
            
            if response.status_code == 200:
                result = response.json()
                if result.get("code") == 200:
                    self.token = result.get("token")
                    print(f"登录成功！Token: {self.token[:30]}...")
                    return True
                else:
                    print(f"登录失败，错误信息: {result.get('msg')}")
            else:
                print(f"HTTP请求失败，状态码: {response.status_code}")
            return False
        except Exception as e:
            print(f"其他异常: {str(e)}")
            return False
    
    def upload_retail_data(self, retail_data: List[Dict]) -> Dict:
        """上报零售数据到服务器"""
        if not self.token:
            raise Exception("请先登录获取token")
            
        url = f"{self.base_url}/dc/api/v1/collection/retail"
        
        # 设置请求头
        headers = {
            'Authorization': f'Bearer {self.token}',
            'Content-Type': 'application/json',
            'Accept': 'application/json',
            'User-Agent': 'Mozilla/5.0'
        }
        
        try:
            print(f"正在上报数据到: {url}")
            print("请求数据:", json.dumps(retail_data, ensure_ascii=False, indent=2))
            
            response = requests.post(
                url,
                json=retail_data,  # 使用json参数自动处理JSON序列化
                headers=headers,
                verify=False,  # 不验证SSL证书
                timeout=5
            )
            
            print(f"服务器响应状态码: {response.status_code}")
            print("服务器响应内容:", json.dumps(response.json(), ensure_ascii=False, indent=2))
            
            return response.json()
        except Exception as e:
            print(f"上报数据失败: {str(e)}")
            return None 