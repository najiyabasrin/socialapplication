from django.shortcuts import render,redirect
from socialapp.forms import LoginForm,RegistrationForm,PostForm
from django.contrib.auth.models import User
from django.views.generic import View,CreateView,FormView,TemplateView,ListView
from django.urls import reverse_lazy
from django.contrib.auth import authenticate,login,logout
from socialapp.models import Post


# Create your views here.



class SignupView(CreateView):
    model=User
    form_class=RegistrationForm
    template_name="register.html"
    success_url=reverse_lazy("signin")





class LoginView(FormView):
    form_class=LoginForm
    template_name="login.html"



    def post(self,request,*args,**kw):
        form=LoginForm(request.POST)
        if form.is_valid():
            uname=form.cleaned_data.get("username")
            pwd=form.cleaned_data.get("password")
            user=authenticate(request,username=uname,password=pwd)
            if user:
                login(request,user)
                print("success")
                return redirect("home")

            else:
                return render(request,self.template_name,{"form":form})


class IndexView(CreateView,ListView):
    template_name="index.html"
    form_class=PostForm
    model=Post
    success_url=reverse_lazy("home")
    context_object_name="title"


    def form_valid(self, form):
        form.instance.user=self.request.user
        return super().form_valid(form)


    def get_queryset(self):
        return Post.objects.all().exclude(user=self.request.user)
        
    

def add_comment(request,*args,**kw):
    title_id=kw.get("id")  
    tit=Post.objects.get(id=title_id)
    com=request.POST.get("comment")
    tit.comment_set.create(comment=com,user=request.user)
    return redirect("home")

def upvote_view(request,*args,**kw):
    title_id=kw.get("id")
    tit=Post.objects.get(id=title_id)
    tit.upvote.add(request.user)
    tit.save()
    return redirect("home")