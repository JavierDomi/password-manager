from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import PasswordEntry, VaultSettings
from .forms import PasswordEntryForm
from .utils import derive_fernet_key_b64
from cryptography.fernet import Fernet
import os
import base64

@login_required
def home(request):
    fernet_key = request.session.get('fernet_key')
    if not fernet_key:
        return redirect('request_master_password')

    fernet = Fernet(fernet_key.encode())

    # We exclude the entry "Dummy" necessary to test the masterpassword
    entries = PasswordEntry.objects.filter(user=request.user).exclude(site_name="Dummy")

    for e in entries:
        try:
            e.decrypted_password = fernet.decrypt(e.encrypted_password.encode()).decode()
        except Exception:
            e.decrypted_password = "[Could not decrypt]"

    return render(request, 'vault/home.html', {'entries': entries})


@login_required
def add_password(request):
    master_password = request.session.get('master_password')
    if not master_password:
        return redirect('request_master_password')

    if request.method == 'POST':
        form = PasswordEntryForm(request.POST, master_password=master_password)
        if form.is_valid():
            entry = form.save(commit=False)
            entry.user = request.user
            plain_pw = form.cleaned_data.get('plain_password')
            if plain_pw:
                entry.set_password(plain_pw, master_password)
            entry.save()
            return redirect('home')

    else:
        form = PasswordEntryForm(master_password=master_password)

    return render(request, 'vault/add_password_entry.html', {'form': form})

@login_required
def edit_password(request, id):
    entry = get_object_or_404(PasswordEntry, id=id, user=request.user)
    master_password = request.session.get('master_password')
    if not master_password:
        return redirect('request_master_password')

    if request.method == 'POST':
        form = PasswordEntryForm(request.POST, instance=entry, master_password=master_password)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = PasswordEntryForm(instance=entry, master_password=master_password)

    return render(request, 'vault/edit_password_entry.html', {'form': form, 'entry': entry})

@login_required
def delete_password(request, id):
    PasswordEntry.objects.filter(id=id, user=request.user).delete()
    return redirect('home')

@login_required
def request_master_password(request):
    if request.session.get('fernet_key'):
        return redirect('home')

    if request.method == 'POST':
        master_password = request.POST.get('master_password')
        user_settings = VaultSettings.objects.filter(user=request.user).first()
        if not user_settings:
            messages.error(request, 'No encryption settings found for your account.')
            return redirect('home')

        salt = user_settings.salt
        entry = PasswordEntry.objects.filter(user=request.user).first()
        if not entry:
            messages.error(request, 'No password entries found, cannot verify master password.')
            return redirect('request_master_password')

        try:
            key_b64 = derive_fernet_key_b64(request.user.id, master_password, salt)
            fernet = Fernet(key_b64.encode())
            # Try to decrypt the first entry
            fernet.decrypt(entry.encrypted_password.encode())
        except Exception as e:
            messages.error(request, 'Incorrect master password.')
            return redirect('request_master_password')

        request.session['fernet_key'] = key_b64
        request.session['master_password'] = master_password

        next_url = request.session.pop('next_url', None)
        return redirect(next_url or 'home')

    return render(request, 'vault/request_master_password.html')



def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            salt = base64.b64encode(os.urandom(16)).decode()
            VaultSettings.objects.create(user=user, salt=salt)

            # Create an encrypted dummy entry with the master password equal to the Django password
            master_password = form.cleaned_data['password1']
            entry = PasswordEntry(user=user, site_name="Dummy", username="dummy")
            entry.set_password("dummy_password", master_password)
            entry.save()

            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'vault/register.html', {'form': form})
