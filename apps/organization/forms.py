from django import forms
from  operation.models import UserAsk
import re

# 继承ModelForm
class UserAskForm (forms.ModelForm):
    # 定义属性
    # model 必须  filelds 包含的属性 exclude 剔除的属性
    class Meta:
        model = UserAsk
        exclude = ['add_time']

    # 自定义校验规则 clean_属性名
    def clean_mobile(self):
        # 通过cleaned_data[属性名] 获取value
        mobile = self.cleaned_data['module']
        mobilereg = "^(((13[0-9]{1})|(15[0-9]{1})|(18[0-9]{1}))+\d{8})$";
        p = re.compile (mobilereg)
        if p.match (mobile):
            return mobile
        else:
            # 抛出异常
            raise forms.ValidationError ("手机号码为空", code="moblie_invalid")
