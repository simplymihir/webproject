from django.shortcuts import render, redirect
from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from blog.models import post
from django.contrib.auth.models import User

def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            #this creates the user
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'account created for {username} successfully')
            return redirect('login')
        #else:
        #   print(form.errors)
        #   messages.warning(request, f'some error occured')
        #   return redirect('register')
    else:
        form = UserRegisterForm
    return render(request, 'users/register.html', {'forms': form})

@login_required
def profile(request,username):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST,
                                   request.FILES,
                                   instance=request.user.profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, f'Your account has been updated!')
            return redirect('profile')

    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)

    user_link=User.objects.filter(username=username).first()
    context = {
        'u_form': u_form,
        'p_form': p_form,
        'user_link': user_link,
        'posts': post.objects.filter(author=user_link).order_by('-date_posted')
    }

    return render(request, 'users/profile.html', context)

