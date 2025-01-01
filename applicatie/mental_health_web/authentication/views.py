from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login

def register(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # Log de gebruiker meteen in na registratie
            return redirect('home')  # Verwijs naar de home-pagina of een andere pagina
    else:
        form = UserCreationForm()
    return render(request, 'authentication/register.html', {'form': form})
