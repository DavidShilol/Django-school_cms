from django import forms

class RegisterInfo(forms.Form):
    name = forms.CharField()
    sex = forms.ChoiceField(choices=(('男', 1), ('女', 2)))
    idcard = forms.CharField(min_length=18, max_length=18)
    phone = forms.CharField(min_length=11, max_length=11)
    password = forms.CharField(min_length=6)
    repeat_passwd = forms.CharField(min_length=6)

class LoginInfo(forms.Form):
    workid = forms.CharField()
    password = forms.CharField()
