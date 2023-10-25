from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Profile, Twit
from .forms import TwitForm, UserSignUp, ProfilePicForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django import forms

def home(request):
    if request.user.is_authenticated:
        form = TwitForm(request.POST or None)
        if request.method == "POST":
            if form.is_valid():
                twit = form.save(commit=False)
                twit.user = request.user
                twit.save()
                messages.success(request, ("Twitingiz chop etilgur!"))
                return redirect('home')
        twits = Twit.objects.all().order_by("-created_at")
        return render(request, 'home.html', {"twits": twits, "form": form,})
    else:
        twits = Twit.objects.all().order_by("-created_at")
        return render(request, 'home.html', {"twits": twits})
def profile_list(request):
    if request.user.is_authenticated:
        profiles = Profile.objects.exclude(user=request.user)
        return render(request, 'profile_list.html', {"profiles": profiles})
    else:
        messages.success(request, ("Tweet uchun tizimga kirishingiz kerak!"))
        return redirect('home')
    
def unfollow(request, pk):
    if request.user.is_authenticated:
        profile = Profile.objects.get(user_id=pk)
        request.user.profile.follows.remove(profile)
        request.user.profile.save()
        messages.success(request, (f"Siz {profile.user.username}ni tark etdingiz..."))
        return redirect(request.META.get("HTTP_REFERER"))

    else:
        messages.success(request, ("Tweet uchun tizimga kirishingiz kerak!"))
        return redirect('home')
    
def follow(request, pk):
    if request.user.is_authenticated:
        profile = Profile.objects.get(user_id=pk)
        request.user.profile.follows.add(profile)
        request.user.profile.save()
        messages.success(request, (f"Siz {profile.user.username} bilan do'stlashdingiz!"))
        return redirect(request.META.get("HTTP_REFERER"))

    else:
        messages.success(request, ("Tweet uchun tizimga kirishingiz kerak!"))
        return redirect('home')
    
def profile(request, pk):
    if request.user.is_authenticated:
        profile = Profile.objects.get(user_id=pk)
        twits = Twit.objects.filter(user_id=pk).order_by("-created_at")
        if request.method == "POST":
            current_user_profile = request.user.profile
            action = request.POST['follow']
            if action == "unfollow":
                current_user_profile.follows.remove(profile)
            elif action == "follow":
                current_user_profile.follows.add(profile)
            current_user_profile.save()
        return render(request, "profile.html", {"profile":profile, "twits":twits})
    else:
        messages.success(request, ("Tweet uchun tizimga kirishingiz kerak!"))
        return redirect('home')

def followers(request, pk):
    if request.user.is_authenticated:
        if request.user.id == pk:
            profiles = Profile.objects.get(user_id=pk)
            return render(request, 'followers.html', {"profiles": profiles})
        else:
            messages.success(request, ("Bu sizning profilingiz emas-ku!"))
            return redirect('home')
    else:
        messages.success(request, ("Tweet uchun tizimga kirishingiz kerak!"))
        return redirect('home')
    
def follows(request, pk):
    if request.user.is_authenticated:
        if request.user.id == pk:
            profiles = Profile.objects.get(user_id=pk)
            return render(request, 'follows.html', {"profiles": profiles})
        else:
            messages.success(request, ("Bu sizning profilingiz emas-ku!"))
            return redirect('home')
    else:
        messages.success(request, ("Tweet uchun tizimga kirishingiz kerak!"))
        return redirect('home')

def login_user(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, ("Kirdingiz! Yaxshi twitlar yozing!"))
            return redirect('home')
        else:
            messages.success(request, ("Har ishniki ayladim, xatoliq bo'ldi! To'g'ri yozingey!"))
            return redirect('login')
    else:
        return render(request, "login.html", {})

def logout_user(request):
    logout(request)
    messages.success(request, ("Yosh ketdingiz. Hammamiz ham boramiz shu yoqqa, shoshmasangiz ham bo'lardi..."))
    return redirect('home')

def register_user(request):
    form = UserSignUp()
    if request.method == "POST":
        form = UserSignUp(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            email = form.cleaned_data['email']
            # # Log in the muhtaram user
            user = authenticate(username=username, password=password)
            login(request, user)
            messages.success(request, ("To'damizga muvaffaqiyatli qo'shildingiz! Salom tweetchi!"))
            return redirect('home')
    return render(request, "register.html", {'form': form})

def update_user(request):
    if request.user.is_authenticated:
        current_user = User.objects.get(id=request.user.id)
        profile_user = Profile.objects.get(user__id=request.user.id)
        user_form = UserSignUp(request.POST or None, request.FILES or None, instance=current_user)
        profile_form = ProfilePicForm(request.POST or None, request.FILES or None, instance=profile_user)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            login(request, current_user)
            messages.success(request, ("Saqlandi👍"))
            return redirect('home')

        return render(request, "update_user.html", {'user_form':user_form, 'profile_form':profile_form})
    else:
        messages.success(request, ("Oldin tizimga kirishingiz kerak!"))
    return redirect('home')

def twit_like(request, pk):
    if request.user.is_authenticated:
        twit = get_object_or_404(Twit, id=pk)
        if twit.likes.filter(id=request.user.id):
            twit.likes.remove(request.user)
        else:
            twit.likes.add(request.user)
        return redirect(request.META.get("HTTP_REFERER"))

    else:
        messages.success(request, ("Oldin tizimga kirishingiz kerak!"))
    return redirect('home')

def shu_twit(request, pk):
    twit = get_object_or_404(Twit, id=pk)
    if twit:
        return render(request, "shu_twit.html", {'twit': twit})
    else:
        messages.success(request, ("Haskerlik qilmang! Unaqa twit jo'q, shunday ekan, tur jo'qal😁"))
        return redirect('home')

def delete_twit(request, pk):
    if request.user.is_authenticated:
        twit = get_object_or_404(Twit, id=pk)
        if request.user.username == twit.user.username:
            twit.delete()
            messages.success(request, ("Borsakelmasga badarg'a qilindi!"))
            return redirect(request.META.get("HTTP_REFERER"))
        else:
            messages.success(request, ("Haskerlik qilmang! Bu twit sizga tegishli emas, tegmang!"))
            return redirect('home')
    else:
        messages.success(request, ("Oldin tizimga kirvolingey🦿"))
        return redirect(request.META.get("HTTP_REFERER"))
    
def edit_twit(request, pk):
    if request.user.is_authenticated:
        twit = get_object_or_404(Twit, id=pk)
        if request.user.username == twit.user.username:
            form = TwitForm(request.POST or None, instance=twit)
            if request.method == "POST":
                if form.is_valid():
                    twit = form.save(commit=False)
                    twit.user = request.user
                    twit.save()
                    messages.success(request, ("Twitingiz jisman o'zgardi!"))
                    return redirect('home')
                else:
                    messages.success(request, ("Haskerlik qilmang! Bu twit sizga tegishli emas, tegmang!"))
                return redirect('home')
            else:
                return render(request, "edit_twit.html", {'form':form, 'twit':twit})
    else:
            messages.success(request, ("Oldin tizimga kirvolingey🦿"))
            return redirect('home')
    
def search(request):
    if request.method == "POST":
        search = request.POST['search']
        searched = Twit.objects.filter(body__contains = search)
        return render(request, 'search.html', {'search': search, 'searched': searched})
    else:
        return render(request, 'search.html', {})
    
def search_user(request):
    if request.method == "POST":
        search = request.POST['search']
        searched = User.objects.filter(username__contains = search)
        return render(request, 'search_user.html', {'search': search, 'searched': searched})
    else:
        return render(request, 'search_user.html', {})