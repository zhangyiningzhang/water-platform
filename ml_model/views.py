from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
import json
import logging
import math
from .predictor import SimplePredictor
from django.http import HttpResponse 

@csrf_exempt
def post(request):
    if request.method == 'POST':
        name = request.POST.get('name', '')
        return HttpResponse('welcome!{}'.format(name))
    else:
        return HttpResponse('Method Not Allowed', status=405)

# 初始化预测器
predictor = SimplePredictor()

# 设置日志记录
logger = logging.getLogger(__name__)

# 辅助函数：安全转换数值（允许空白）
def safe_convert(value, default=0.0):
    """将值转换为浮点数，处理空白和空值"""
    if value is None:
        return default
        
    str_value = str(value).strip()
    if not str_value:  # 空字符串或空白
        return default
        
    try:
        return float(str_value)
    except (ValueError, TypeError):
        # 记录原始值以便调试
        logger.warning(f"无法转换的值: '{value}'")
        return default

@csrf_exempt
@require_http_methods(["POST"])
def predict_random(request):
    try:
        # 解析请求体中的 JSON 数据
        data = json.loads(request.body)
        
        # 日志记录原始请求数据（调试用）
        logger.debug(f"Received prediction request: {data}")

        # 安全提取并转换输入数据（允许空白）
        depth = safe_convert(data.get('depth'))
        power_usage = safe_convert(data.get('power_usage'))
        well_age = safe_convert(data.get('well_age'))
        drawdown = safe_convert(data.get('drawdown'))
        lift = safe_convert(data.get('lift'))
        pump_power = safe_convert(data.get('pump_power'))
        
        # 检查所有字段是否都缺失（特殊处理）
        if all(value == 0.0 for value in [depth, power_usage, well_age, drawdown, lift, pump_power]):
            logger.warning("所有输入字段均为空值")
            return JsonResponse({
                'status': 'error',
                'message': '至少需要提供一个有效参数'
            }, status=400)

        # 将输入数据传递给预测模型
        input_data = {
            'depth': depth,
            'power_usage': power_usage,
            'well_age': well_age,
            'drawdown': drawdown,
            'lift': lift,
            'pump_power': pump_power
        }

        prediction = predictor.predict(input_data)

        # 返回预测结果
        return JsonResponse({
            'status': 'success',
            'prediction': prediction,
            'input_used': input_data  # 返回实际使用的输入值（包含空白处理结果）
        })

    except json.JSONDecodeError:
        logger.error('Invalid JSON format in request body')
        return JsonResponse({
            'status': 'error',
            'message': 'Invalid JSON format'
        }, status=400)

    except Exception as e:
        logger.error(f'Unexpected error: {str(e)}', exc_info=True)
        return JsonResponse({
            'status': 'error',
            'message': 'An unexpected error occurred'
        }, status=500)