import requests
from typing import Dict, Any, Optional, List

class RetailAPI:
    def __init__(self, base_url: str):
        self.base_url = base_url
        self.token = None
        # 设置请求超时和禁用代理
        self.session = requests.Session()
        self.session.trust_env = False  # 禁用环境变量中的代理设置
        self.timeout = 30  # 增加超时时间到30秒
        
    def login(self, username: str, password: str) -> bool:
        """登录并获取token"""
        url = f"{self.base_url}/token/grant"
        print(f"正在尝试登录: {url}")
        print(f"用户名: {username}")
        
        try:
            response = self.session.post(
                url,
                data={
                    "username": username,
                    "password": password
                },
                headers={
                    'Content-Type': 'application/x-www-form-urlencoded'
                },
                timeout=self.timeout,
                verify=False
            )
            
            print(f"响应状态码: {response.status_code}")
            print(f"响应内容: {response.text}")
            
            if response.status_code == 200:
                result = response.json()
                if result.get("code") == 200:
                    self.token = f"Bearer {result.get('token')}"
                    print(f"获取到token: {self.token}")
                    return True
                else:
                    print(f"登录失败: {result.get('msg')}")
                    return False
            else:
                print(f"HTTP错误: {response.status_code}")
                return False
                
        except requests.exceptions.Timeout:
            print("连接超时")
            return False
        except requests.exceptions.RequestException as e:
            print(f"请求异常: {str(e)}")
            return False
        except Exception as e:
            print(f"其他异常: {str(e)}")
            return False
            
    def upload_retail_data(self, data: List[Dict]) -> Optional[Dict]:
        """上报零售数据"""
        if not self.token:
            print("未登录，请先调用login方法")
            return None
        
        url = f"{self.base_url}/dc/api/v1/collection/retail"
        print(f"开始上报数据到: {url}")
        print(f"使用token: {self.token}")
        
        headers = {
            'Content-Type': 'application/json',
            'Authorization': self.token
        }
        
        try:
            print(f"上报数据示例: {data[0] if data else 'No data'}")
            print(f"上报数据条数: {len(data)}")
            
            response = self.session.post(
                url,
                json=data,
                headers=headers,
                timeout=self.timeout,
                verify=False
            )
            
            print(f"响应状态码: {response.status_code}")
            print(f"响应内容: {response.text}")
            
            if response.status_code == 200:
                result = response.json()
                print(f"上报结果: {result}")
                return result
            else:
                print(f"上报失败: HTTP {response.status_code}")
                print(f"错误信息: {response.text}")
                return None
                
        except Exception as e:
            print(f"上报异常: {str(e)}")
            print(f"异常类型: {type(e)}")
            return None 