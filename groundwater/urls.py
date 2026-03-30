from django.urls import path
from . import views

urlpatterns = [
    # 上传 Excel 文件
    path('upload/', views.upload_excel, name='upload_excel'),
    # 获取井数据
    path('data/', views.get_well_data, name='get_well_data'),
]