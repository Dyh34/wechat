from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q
from django.http import HttpResponse,JsonResponse
from django.shortcuts import render
from .models import WeChatUser,Status
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.contrib.auth.models import User

# Create your views here.
def home(request):
    return render(request,'homepage.html')
"""
@login_required
def show_user(request):
    return render(request,'user.html',{
        'user':{
            'name':'xiao po',
            'motto':'i love kungfu',
            'email':'po@disney.com',
            'region':'Shannxi',
            'pic':'Po2.jpg'
        }
    })
"""
@login_required
def show_user(request):
    """
    po = {
        'user': {
            'name': 'xiao po',
            'motto': 'i love kungfu',
            'email': 'po@disney.com',
            'region': 'Shannxi',
            'pic': 'Po2.jpg'
        }
    }
    """
    user = WeChatUser.objects.get(user=request.user)
    return render(request,"user.html",{"user":user})
"""
@login_required
def show_status(request):
    keyword=request.GET.get('keyword')
    if not keyword:
        statuses = Status.objects.all()
    else:
        statuses = Status.objects.filter(Q(user__user__username__contains=keyword) |
                                         Q(text__contains=keyword))
        p = Paginator(statuses, 2)
        page = request.GET.get("page",1)
        statuses = p.page(page)
    return render(request,'status.html',{"statuses":statuses,
                                                              "keyword":keyword,
                                                              #"page":int(page),
                                                              #"page_range":p.page_range
                                         })
"""


@login_required
def show_status(request):
    keyword = request.GET.get('keyword', '')

    # 根据是否有 keyword 过滤 Status 对象
    if keyword:
        statuses = Status.objects.filter(
            Q(user__user__username__icontains=keyword) |
            Q(text__icontains=keyword)
        )
    else:
        statuses = Status.objects.all()

    # 分页逻辑
    paginator = Paginator(statuses, 3)  # 每页显示2条状态
    page = request.GET.get("page", 1)

    try:
        statuses_page = paginator.page(page)
    except PageNotAnInteger:
        # 如果页码不是整数，显示第一页
        statuses_page = paginator.page(1)
        page = 1
    except EmptyPage:
        # 如果页码超出范围，显示最后一页
        statuses_page = paginator.page(paginator.num_pages)
        page = paginator.num_pages

    return render(request, 'status.html', {
        "statuses": statuses_page,
        "keyword": keyword,
        "page": int(page),
        "page_range": paginator.page_range
    })
@login_required
def submit_post(request):
    user = WeChatUser.objects.get(user=request.user)
    text = request.POST.get('text')
    uploaded_file = request.FILES.get('pics')
    if uploaded_file:
        name = uploaded_file.name
        with open("./moments/static/image/{}".format(name),"wb+") as handle:
            for block in uploaded_file.chunks():
                handle.write(block)
    else:
        name=''
    if text:
        Status(user=user,text=text,pics=name).save()
        #Status.save()
        return redirect('/status')
    return render(request,'my_post.html')


@login_required
def friends(request):
    return render(request,'friends.html')


@login_required
def register_user(request):
    try:
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")
        user=User(username=username,email=email)
        user.set_password(password)
        user.save()
        WeChatUser.objects.create(user=user)
    except Exception as err:
        result = False
        message = str(err)
    else:
        result = True
        message="RegisterUser"
    return JsonResponse({"result":result,"message":message})


@login_required
def update_user(request):
    try:
        pic = request.POST.get("pic")
        email = request.POST.get("email")
        region = request.POST.get("region")
        motto = request.POST.get("motto")
        if pic:
            WeChatUser.objects.filter(user=request.user).update(pic=pic)
        if region:
            WeChatUser.objects.filter(user=request.user).update(region=region)
        if motto:
            WeChatUser.objects.filter(user=request.user).update(motto=motto)
        if email:
            User.objects.filter(username=request.user).update(email=email)
    except Exception as err:
        result = False
        message = str(err)
    else:
        result = True
        message="Update successfully!"
    return JsonResponse({"result":result,"message":message})