import requests
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json

@csrf_exempt
def get_sensor_data(request):
    # 有效认证信息
    access_token = "fa812ed4-a80e-4a78-882b-8a8031a1a204"
    client_id = "d9273341f5d34317a74f079e60d8ab6b"
    user_id = 79990  # ✅ 修改在这里：真实的 userId
    sensor_id = 3125482  # 实际传感器 ID

    url = "https://app.dtuip.com/api/device/getSingleDeviceDatas"  # 假设这是正确的 API URL

    headers = {
        "Authorization": f"Bearer {access_token}",
        "tlinkAppId": client_id,
        "Content-Type": "application/json",
        "cache-control": "no-cache"
    }

    payload = {
        "userId": user_id,
        "sensorId": sensor_id
    }

    try:
        # 使用 POST 请求（接口文档明确要求）
        response = requests.post(url, headers=headers, json=payload)
        print("▶ 发送 payload:", payload)
        print("⬅ 返回内容:", response.status_code, response.text)

        data = response.json()
        return JsonResponse(data)
    except Exception as e:
        return JsonResponse({"flag": "01", "msg": str(e)})