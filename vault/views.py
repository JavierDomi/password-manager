from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from .models import PasswordEntry
import base64
import os

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'vault/register.html', {'form': form})

@login_required
def home(request):
    fernet_key = request.session.get('fernet_key')
    if not fernet_key:
        return redirect('request_master_password')

    from cryptography.fernet import Fernet
    fernet = Fernet(fernet_key.encode())

    entries = PasswordEntry.objects.filter(user=request.user)
    for e in entries:
        try:
            e.decrypted_password = fernet.decrypt(e.encrypted_password.encode()).decode()
        except Exception:
            e.decrypted_password = "[No se pudo descifrar]"
    return render(request, 'vault/home.html', {'entries': entries})

@login_required
def add_password(request):
    if request.method == 'POST':
        fernet_key = request.session.get('fernet_key')
        if not fernet_key:
            return redirect('request_master_password')

        from cryptography.fernet import Fernet
        fernet = Fernet(fernet_key.encode())

        encrypted = fernet.encrypt(request.POST['password'].encode()).decode()
        salt = base64.b64encode(os.urandom(16)).decode()

        PasswordEntry.objects.create(
            user=request.user,
            site_name=request.POST['site_name'],
            site_url=request.POST['site_url'],
            username=request.POST['username'],
            encrypted_password=encrypted,
            salt=salt,
            notes=request.POST['notes'],
        )
        return redirect('home')
    return render(request, 'vault/add.html')


@login_required
def delete_password(request, id):
    PasswordEntry.objects.filter(id=id, user=request.user).delete()
    return redirect('home')
