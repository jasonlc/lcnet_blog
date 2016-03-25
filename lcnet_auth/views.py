#encoding:utf-8
from django.shortcuts import render
from django.views.generic import View
from django.http import Http404,HttpResponse
from django.core.mail import send_mail,EmailMessage
from django.contrib.auth.forms import PasswordChangeForm,SetPasswordForm
from django.contrib import auth
from django.contrib.sites.models import get_current_site
from PIL import Image
import datetime,time
import os
import json
import base64
import logging
from django.core.exceptions import PermissionDenied
from lcnet_auth.forms import LcNetUserCreationForm
# from lcnet_blog.settings import EMAIL_HOST_USER
logger=logging.getLogger('project.interesting.stuff')

# def send_html_mail(subject,html_content,recipient_list):
#         msg = EmailMessage(subject, html_content, EMAIL_HOST_USER, recipient_list)
#         msg.content_subtype = "html"
#         msg.send()

class UserControl(View):
    def post(self,request,*args,**kwargs):
        slug=self.kwargs.get('slug')
        if slug=='login':
            return self.login(request)
        elif slug=='logout':
            return self.logout(request)
        elif slug == "register":
            return self.register(request)
        elif slug=="changetx":
            return self.changetx(request)
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
    def register(self,request):
        username=self.request.POST.get("username","")
        password1=self.request.POST.get("password1","")
        password2=self.request.POST.get("password2","")
        email=self.request.POST.get("email","")
        form=LcNetUserCreationForm(request.POST)
        errors=[]

        if form.is_valid():
            current_site = get_current_site(request)
            site_name = current_site.name
            domain = current_site.domain
            title = u"欢迎来到 %s ！" % site_name
            message = u"你好！ %s ,感谢注册 %s ！\n\n" % (username,site_name) + \
                      u"请牢记以下信息：\n" + \
                      u"用户名：%s" % username+"\n" + \
                      u"邮箱：%s" % email+"\n" + \
                      u"网站：http://%s" % domain+"\n\n"
            # from_email = None
            # try:
            #     # send_mail(title, message, from_email, [email])
            #     send_html_mail(title,message,[email])
            # except Exception as e:
            #     logger.error(u'[UserControl]用户注册邮件发送失败:[%s]/[%s],错误信息为：%s' % (username,email,e))
            #     return HttpResponse(u"发送邮件错误!\n注册失败",status=500)
            new_user = form.save()
            user = auth.authenticate(username=username, password=password2)
            auth.login(request,user)
        else:
            #如果表单不正确,保存错误到errors列表中
            for k,v in  form.errors.items():
                #v.as_text() 详见django.forms.util.ErrorList 中
                errors.append(v.as_text())
        mydict = {"errors":errors}
        return HttpResponse(json.dumps(mydict),content_type="application/json")


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

    def changetx(self,request):
        if not request.user.is_authenticated():
            logger.error(u'[UserControl]用户未登陆')
            raise PermissionDenied

        #本地保存头像
        data =  request.POST['tx']
        if not data:
            logger.error(u'[UserControl]用户上传头像为空:[%s]',request.user.username)
            return HttpResponse(u"上传头像错误",status=500)
        imgData = base64.b64decode(data)
        filename ="tx_100x100_"+'%d' % request.user.id+".jpg"
        filedir = "lcnet_auth/static/tx/"
        if not os.path.exists(filedir):
            os.makedirs(filedir)

        path = filedir + filename

        file=open(path, "wb+")
        file.write(imgData)
        file.flush()
        file.close()

        #修改头像分辨率
        im = Image.open(path)
        out = im.resize((100, 100),Image.ANTIALIAS)
        out.save(path)


        #选择上传头像到七牛还是本地
        try:
	        #上传头像到七牛
            from lcnet_blog.settings import qiniu_access_key,qiniu_secret_key,qiniu_bucket_name
            import qiniu

            assert qiniu_access_key and qiniu_secret_key and qiniu_bucket_name
            q = qiniu.Auth(qiniu_access_key, qiniu_secret_key)

            print qiniu_access_key

            key = filename
            localfile = path

            mime_type = "text/plain"
            params = {'x:a': 'a'}

            token = q.upload_token(qiniu_bucket_name, key)
            ret, info = qiniu.put_file(token, key, localfile, mime_type=mime_type, check_crc=True)

            #图片连接加上 v?时间  是因为七牛云缓存，图片不能很快的更新，用filename?v201504261312的形式来获取最新的图片
            request.user.img = "http://7xrtw5.com1.z0.glb.clouddn.com/"+filename + "?v" + time.strftime('%Y%m%d%H%M%S')
            request.user.save()

            #验证上传是否错误
            if ret['key'] != key or ret['hash'] != qiniu.etag(localfile):
                logger.error(u'[UserControl]上传头像错误：[%s]' % request.user.username)
                return HttpResponse(u"上传头像错误",status=500)

            return HttpResponse(u"上传头像成功!\n(注意有10分钟缓存)")

        except Exception as e:
            request.user.img = "/static/tx/"+filename
            request.user.save()

            #验证上传是否错误
            if not os.path.exists(path):
                logger.error(u'[UserControl]用户上传头像出错:[%s]',request.user.username)
                return HttpResponse(u"上传头像错误",status=500)

            return HttpResponse(u"上传头像成功!\n(注意有10分钟缓存)")