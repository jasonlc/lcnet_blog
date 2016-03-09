#encoding:utf-8
from django.shortcuts import render
from django.views.generic import View
from django.http import Http404,HttpResponse
from django.contrib.auth.forms import PasswordChangeForm,SetPasswordForm
from django.contrib import auth
import json
import logging
from django.core.exceptions import PermissionDenied

logger=logging.getLogger(__name__)


class UserControl(View):
    def post(self,request,*args,**kwargs):
        slug=self.kwargs.get('slug')
        if slug=='login':
            return self.login(request)
        elif slug=='logout':
            return self.logout(request)
        elif slug=='changepassword':
            return self.changepassword(request)
        raise PermissionDenied

    def get(self,request,*args,**kwargs):
        return Http404

    def login(self,request):
        username=request.POST.get("username","")
        password=request.POST.get("password","")
        user=auth.authenticate(username=username,password=password)

        errors=[]

        if user is not None:
            auth.login(request,user)
        else:
            errors.append("密码或用户名不正确")

        mydict={"errors":errors}
        return HttpResponse(json.dumps(mydict),content_type="application/json")

    def logout(self,request):
        if not request.user.is_authenticated():
            logger.error(u'[UserControl]用户未登陆')
            raise PermissionDenied
        else:
            auth.logout(request)
            return HttpResponse('OK')

    def changepassword(self,request):
        if not request.user.is_authenticated():
            logger.error(u'[UserControl]用户未登陆')
            raise PermissionDenied

        form = PasswordChangeForm(request.user,request.POST)

        errors = []
        #验证表单是否正确
        if form.is_valid():
            user = form.save()
            auth.logout(request)
        else:
            #如果表单不正确,保存错误到errors列表中
            for k,v in  form.errors.items():
                #v.as_text() 详见django.forms.util.ErrorList 中
                errors.append(v.as_text())

        mydict = {"errors":errors}
        return HttpResponse(json.dumps(mydict),content_type="application/json")