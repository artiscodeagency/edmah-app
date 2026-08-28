from django.contrib.auth import login
from django.shortcuts import redirect, render

from .forms import RegisterForm
from .models import User


def register_view(request):
    if request.user.is_authenticated:
        return redirect('apprenant_dashboard')

    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.role = User.Role.APPRENANT
            user.save()
            login(request, user)
            return redirect('apprenant_dashboard')
    else:
        form = RegisterForm()

    return render(request, 'accounts/register.html', {'form': form})
