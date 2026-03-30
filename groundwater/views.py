# groundwater/views.py
import pandas as pd
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render
from .models import WellData
from .forms import ExcelUploadForm
from django.views.decorators.http import require_http_methods
from django.core.files.storage import FileSystemStorage
import json
from django.views.decorators.csrf import csrf_exempt
import logging
from django.db import transaction
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

# 配置日志记录
logger = logging.getLogger(__name__)

# 在处理函数加此装饰器即可
@csrf_exempt
def post(request):
    if request.method == 'POST':
        name = request.POST.get('name', '')
        return HttpResponse('welcome!{}'.format(name))
    else:
        return HttpResponse('Method Not Allowed', status=405)

# 添加文件格式验证函数
def validate_excel_file(file):
    if not file.name.endswith(('.xlsx', '.xls', '.csv')):
        raise ValidationError(_('Invalid file format. Only Excel files are allowed.'))

@require_http_methods(["GET", "POST"])
def upload_excel(request):
    if request.method == 'POST':
        form = ExcelUploadForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                file = request.FILES['excel_file']
                validate_excel_file(file)  # 添加文件格式验证
                fs = FileSystemStorage()
                filename = fs.save(file.name, file)
                file_path = fs.path(filename)
                
                df = pd.read_excel(file_path, dtype=str)  # 指定dtype为str，防止自动转换
                WellData.objects.all().delete()
                records = []
                for index, row in df.iterrows():
                    records.append(WellData(
                        index=row[0],
                        town=row[1],
                        code=row[2],
                        location=row[3],
                        longitude=row[4],
                        latitude=row[5],
                        irrigation_method=row[6],
                        groundwater_depth=row[7],
                        drawdown=row[8],
                        final_groundwater_depth=row[9],
                        well_age=row[10],
                        well_depth=row[11],
                        well_diameter=row[12],
                        well_casing_material=row[13],
                        wellhead_elevation=row[14],
                        power=row[15],
                        head=row[16],
                        flow=row[17],
                        conversion_factor=row[18]
                    ))
                # 使用批量创建提高效率
                with transaction.atomic():  # 使用事务确保批量创建的原子性
                    WellData.objects.bulk_create(records)
                return JsonResponse({'message': '数据上传成功！'})
            except ValidationError as ve:
                logger.error('Invalid file format: %s', str(ve))
                return JsonResponse({'message': f'数据上传失败：{str(ve)}'}, status=400)
            except Exception as e:
                logger.error('Error processing Excel file: %s', str(e))
                return JsonResponse({'message': f'数据上传失败：{str(e)}'}, status=500)
        else:
            return JsonResponse({'message': '表单验证失败！'}, status=400)
    else:
        form = ExcelUploadForm()
        return render(request, 'upload.html', {'form': form})

def get_well_data(request):
    data = list(WellData.objects.values())
    return JsonResponse(data, safe=False)