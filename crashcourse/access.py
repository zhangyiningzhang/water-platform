import requests
from base64 import b64encode

# 用户名和密码
username = 'jlsh'
password = 'jlsh123456'

# 客户端ID 和密钥
client_id = 'd9273341f5d34317a74f079e60d8ab6b'
client_secret = '76b35bf21276472da8a621f63ee7cb0a'

# 拼接 Base64 编码认证信息
auth_str = f"{client_id}:{client_secret}"
auth_base64 = b64encode(auth_str.encode()).decode()

# 请求头
headers = {
    'Authorization': f'Basic {auth_base64}',
    'Content-Type': 'text/plain',
    'cache-control': 'no-cache'
}

# 请求地址（附带用户名和密码参数）
url = f"https://app.dtuip.com/oauth/token?grant_type=password&username={username}&password={password}"

# 发起 POST 请求
response = requests.post(url, headers=headers)

# 解析返回
if response.status_code == 200:
    data = response.json()
    access_token = data.get("access_token")
    print("✅ Access Token 获取成功：", access_token)
else:
    print("❌ 获取失败：", response.status_code, response.text)