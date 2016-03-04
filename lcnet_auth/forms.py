#encoding:utf-8
from django import forms
from lcnet_auth.models import LcnetUser

class LcNetUserCreationForm(forms.Form):
    error_messages={
        'duplicate_username':u'用户名已存在',
        'password_mismatch':u'两次密码不相等',
        'duplicate_email':u'此email已经存在',
    }
    username=forms.RegexField(max_length=30,regex=r'^[\w.@+-]+$',
            error_message={
            'invalid':  u"该值只能包含字母、数字和字符@/./+/-/_",
            'required': u"用户名未填"})
    email=forms.EmailField(error_messages={
        'invalid':u'email格式不正确',
        'required':u'email未填'
    })
    password=forms.CharField(widget=forms.PasswordInput,error_messages={
        'required':u'密码未填'
    })
    confirmpassword=forms.CharField(widget=forms.PasswordInput,error_messages={
        'required':u'确认密码未填'
    })
    class Meta:
        model=LcnetUser
        fileds=("username","email")

    def clean_username(self):
        username=self.cleaned_data["username"]
        try:
            LcnetUser._default_manager.get(username=username)
        except LcnetUser.DoesNotExist:
            return username
        raise forms.ValidationError(
            self.error_messages["duplicate_username"])

    def clean_confirmpassword(self):
        password=self.cleaned_data["password"]
        confirmpassword=self.cleaned_data["confirmpassword"]
        if password and confirmpassword and password!=confirmpassword:
            raise forms.validationError(
                self.error_messages["password_mismatch"]
            )
        return confirmpassword

    def clean_email(self):
        email=self.cleaned_data["email"]
        try:
            LcnetUser._default_manager.get(email=email)
        except LcnetUser.DoesNotExist:
            return email
        raise forms.validationError(
            self.error_messages["duplicate_email"]
        )

    def save(self,commit=True):
        user=super(LcNetUserCreationForm,self).save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user
