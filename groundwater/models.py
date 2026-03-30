from django.db import models
from django.utils import timezone
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

class WellDataManager(models.Manager):
    def get_town_wells(self, town_name):
        return self.filter(town=town_name)

class WellData(models.Model):
    """
    存储井数据的模型类。
    
    包括位置信息、水文信息、井结构信息等。
    """
    # 主键/唯一标识
    index = models.IntegerField(verbose_name='序号', unique=True, db_index=True)
    
    # 位置信息
    town = models.CharField(max_length=50, verbose_name='乡镇', db_index=True)
    code = models.CharField(max_length=20, verbose_name='井编码', unique=True, db_index=True)
    location = models.CharField(max_length=200, verbose_name='位置')
    longitude = models.CharField(
        max_length=50,
        verbose_name='经度',
        help_text="格式: 度(°)",
        db_index=True
    )
    latitude = models.CharField(
        max_length=50,
        verbose_name='纬度',
        help_text="格式: 度(°)",
        db_index=True
    )
    
    # 水文信息
    irrigation_method = models.CharField(
        max_length=50, 
        verbose_name='灌溉方式',
        choices=[
            ('喷灌', '喷灌'),
            ('滴灌', '滴灌'),
            ('漫灌', '漫灌'),
            ('其他', '其他')
        ],
        default='喷灌'  # 添加默认值
    )
    groundwater_depth = models.CharField(max_length=50, verbose_name='初始地下水埋深(m)', null=True, blank=True)
    drawdown = models.CharField(max_length=50, verbose_name='水位下降值(m)', null=True, blank=True)
    final_groundwater_depth = models.CharField(max_length=50, verbose_name='最终地下水埋深(m)', null=True, blank=True)
    
    # 井结构信息
    well_age = models.CharField(max_length=50, verbose_name='井龄(年)', null=True, blank=True)
    well_depth = models.CharField(max_length=50, verbose_name='井深(m)', null=True, blank=True)
    well_diameter = models.CharField(max_length=50, verbose_name='井径(mm)', null=True, blank=True)
    well_casing_material = models.CharField(
        max_length=50, 
        verbose_name='井管材质',
        choices=[
            ('钢管', '钢管'),
            ('PVC', 'PVC'),
            ('混凝土', '混凝土'),
            ('其他', '其他')
        ],
        default='钢管'  # 添加默认值
    )
    wellhead_elevation = models.CharField(max_length=50, verbose_name='井口高程(m)', null=True, blank=True)
    
    # 抽水设备信息
    power = models.CharField(max_length=50, verbose_name='功率(kW)', null=True, blank=True)
    head = models.CharField(max_length=50, verbose_name='扬程(m)', null=True, blank=True)
    flow = models.CharField(max_length=50, verbose_name='流量(m³/h)', null=True, blank=True)
    
    # 计算系数
    conversion_factor = models.CharField(max_length=50, verbose_name='以电折水系数', null=True, blank=True)
    
    # 时间戳
    created_at = models.DateTimeField(
        verbose_name='创建时间', 
        default=timezone.now,
        editable=False
    )
    updated_at = models.DateTimeField(
        verbose_name='更新时间', 
        auto_now=True
    )

    objects = WellDataManager()

    def clean(self):
        # 示例：简单的文本验证
        if self.well_diameter and not self.well_diameter.replace('.', '', 1).isdigit():
            raise ValidationError(_('井径必须为有效的数值文本格式'))
        # 可以添加更多的数据验证逻辑

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.town} - {self.code} ({self.location})"

    class Meta:
        verbose_name = '井数据'
        verbose_name_plural = '井数据'
        ordering = ['town', 'code']
        indexes = [
            models.Index(fields=['town']),
            models.Index(fields=['code']),
            models.Index(fields=['longitude', 'latitude']),
        ]

    def to_dict(self):
        """返回模型的字典表示，用于序列化"""
        return {
            'id': self.id,
            'index': self.index,
            'town': self.town,
            'code': self.code,
            'location': self.location,
            'longitude': self.longitude,
            'latitude': self.latitude,
            'irrigation_method': self.irrigation_method,
            'groundwater_depth': self.groundwater_depth,
            'drawdown': self.drawdown,
            'final_groundwater_depth': self.final_groundwater_depth,
            'well_age': self.well_age,
            'well_depth': self.well_depth,
            'well_diameter': self.well_diameter,
            'well_casing_material': self.well_casing_material,
            'wellhead_elevation': self.wellhead_elevation,
            'power': self.power,
            'head': self.head,
            'flow': self.flow,
            'conversion_factor': self.conversion_factor,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }

    @classmethod
    def export_as_dict(cls):
        return list(cls.objects.values())