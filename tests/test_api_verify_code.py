import requests

# 测试数据
test_data = {
    'email': 'none3548393247@163.com',
    'code': '484354'
}

# 发送 POST 请求
response = requests.post(
    'http://127.0.0.1:8000/api/verify-code',
    json=test_data
)

# 打印响应
print(f"状态码: {response.status_code}")
print(f"响应内容: {response.text}")