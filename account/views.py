from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login

# Create your views here.


@login_required
def home(request):
    return render(request, 'account/home.html')


def register(request):
    if request.user.is_authenticated:
        return redirect("blog:blog-list")

    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('blog:blog-list')
    else:
        form = UserCreationForm
        
    return render(request, 'registration/register.html', {'form':form})