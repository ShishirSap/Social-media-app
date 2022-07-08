from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import auth
from django.contrib import messages
from .models import Profile
from .models import Post


# Create your views here.

@login_required(login_url='signin')
def index(request):
    user_object=User.objects.get(username=request.user.username)
    user_profile=Profile.objects.get(user=user_object)
    feedposts=Post.objects.all()
    context={
        'feedposts':feedposts.reverse(),
        'user_profile':user_profile
    }
    return render(request,'index.html',context)

def signup(request):
    if request.method=='POST':
        username=request.POST['username']
        email=request.POST['email']
        password=request.POST['password']
        password2=request.POST['password2']

        if password==password2:
            if User.objects.filter(email=email).exists():
                messages.info(request,"Email already taken")
                return redirect("signup")
            elif User.objects.filter(username=username).exists():
                messages.info(request,"Usename already exists")

            else:
                user=User.objects.create_user(username=username,email=email,password=password)

                user.save()
                user_login=auth.authenticate(username=username,password=password)
                auth.login(request,user_login)

                user_model=User.objects.get(username=username)
                new_profile=Profile.objects.create(user=user_model , id_user=user_model.id)
                new_profile.save()
                return redirect('settings')
        else:
            messages.info(request,"Password not matched")
            return redirect('signup')


    return render(request,'signup.html')


def signin(request):
    if request.method=='POST':
        username=request.POST['username']
        password=request.POST['password']
        user=auth.authenticate(username=username,password=password)
        if user is not None:
            auth.login(request,user)
            return redirect('/')
        else:
            messages.info(request,"Bad Credentials")
            return redirect('signin')
    return render(request,'signin.html')

@login_required(login_url='signin')
def logout(request):
    auth.logout(request)
    return redirect('signin')

@login_required(login_url='signin')
def settings(request):
    user_profile=Profile.objects.get(user=request.user)

    if request.method=='POST':

        if request.FILES.get('image')==None:
            image=user_profile.profileimg
            bio=request.POST['bio']
            location=request.POST['location']

            user_profile.profileimg=image
            user_profile.bio=bio
            user_profile.location=location
            user_profile.save()
        if request.FILES.get('image') != None:
            image=request.FILES.get('image')
            bio=request.POST['bio']
            location=request.POST['location']

            user_profile.profileimg=image
            user_profile.bio=bio
            user_profile.location=location
            user_profile.save()
        return redirect('/settings')

    return render(request,'setting.html',{'user_profile':user_profile})

@login_required(login_url='signin')
def upload(request):
    if request.method=='POST':
        user=request.user.username
        image=request.FILES.get('image_upload')
        caption=request.POST['caption']
        new_post=Post.objects.create(user=user,image=image,caption=caption)
        new_post.save()
        
        return redirect('/')
    else:
        return redirect('/')


def profile(request,pk):
    user_object=User.objects.get(username=pk)
    user_profile=Profile.objects.get(user=user_object)
    user_posts=Post.objects.filter(user=pk)
    userpostsno=len(user_posts)

    context={
        'user_object':user_object,
        'user_profile':user_profile,
        'user_posts':user_posts,
        'userpostsno':userpostsno


    }
    return render(request,'profile.html',context)