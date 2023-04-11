from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


def register(request):
    if request.method != 'POST':
        form = UserCreationForm()
    else:
        form= UserCreationForm(data=request.POST)
        if form.is_valid():
            new_user=form.save()
            login(request, new_user)
            return redirect('HomePage')
        
    context = {'form': form}
    return render(request, 'registration/register.html', context)
 
def Licence(request):

    return render(request, 'registration/licence.html')

def logout(request):

    return render(request, 'registration/logout.html')

def change_user_name(request, pk):
    user = User.objects.get(pk=pk)
    user.username = request.POST.get('username')
    user.save()
    return redirect('HomePage')