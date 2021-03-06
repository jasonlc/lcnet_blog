#encoding:utf-8
from django import forms
from lcnet_auth.models import LcnetUser

class LcNetUserCreationForm(forms.ModelForm):
    error_messages = {
        'duplicate_username': u"此用户已存在.",
        'password_mismatch': u"两次密码不相等.",
        'duplicate_email':u'此email已经存在.'
    }

    username = forms.RegexField(max_length=30,regex=r'^[\w.@+-]+$',
        #错误信息 invalid 表示username不合法的错误信息, required 表示没填的错误信息
        error_messages={
            'invalid':  u"该值只能包含字母、数字和字符@/./+/-/_",
            'required': u"用户名未填"})
    email = forms.EmailField(error_messages={
        'invalid':  u"email格式错误",
        'required': u'email未填'})
    password1 = forms.CharField(widget=forms.PasswordInput,
        error_messages={
            'required': u"密码未填"
            })
    password2 = forms.CharField(widget=forms.PasswordInput,
        error_messages={
            'required': u"确认密码未填"
            })

    class Meta:
        model = LcnetUser
        fields = ("username","email")

    def clean_username(self):
        # Since User.username is unique, this check is redundant,
        # but it sets a nicer error message than the ORM. See #13147.
        username = self.cleaned_data["username"]
        try:
            LcnetUser._default_manager.get(username=username)
        except LcnetUser.DoesNotExist:
            return username
        raise forms.ValidationError(
            self.error_messages["duplicate_username"]
        )

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError(
                    self.error_messages["password_mismatch"]
            )
        return password2

    def clean_email(self):
        email = self.cleaned_data["email"]

        #判断是这个email 用户是否存在
        try:
            LcnetUser._default_manager.get(email=email)
        except LcnetUser.DoesNotExist:
            return email
        raise forms.ValidationError(
            self.error_messages["duplicate_email"]
        )



    def save(self, commit=True):
        user = super(LcNetUserCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user
