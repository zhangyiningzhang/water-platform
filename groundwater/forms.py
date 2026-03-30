from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

class ExcelUploadForm(forms.Form):
    excel_file = forms.FileField(
        label='选择 Excel 文件',
        help_text='仅支持 .xlsx, .xls, .csv 格式的文件',
    )

    def clean_excel_file(self):
        file = self.cleaned_data.get('excel_file')
        if file:
            # 检查文件扩展名
            valid_extensions = ['.xlsx', '.xls', '.csv']
            file_extension = str(file.name).lower()
            if not any(file_extension.endswith(ext) for ext in valid_extensions):
                raise ValidationError(_('仅支持上传 .xlsx, .xls, .csv 格式的文件。'))
            
            # 检查文件大小（例如，限制为 5MB）
            max_size = 5 * 1024 * 1024  # 5MB
            if file.size > max_size:
                raise ValidationError(_('文件大小不能超过 5MB。'))
            
            return file
        else:
            raise ValidationError(_('请上传一个文件。'))