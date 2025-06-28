#!/usr/bin/env python
import os
import sys
import django

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'finance_app.settings')
django.setup()

from django.contrib.auth.models import User

def create_superuser():
    username = 'admin'
    email = 'admin@example.com'
    password = 'admin123'
    
    # Verificar se o usuário já existe
    if User.objects.filter(username=username).exists():
        print(f'Usuário {username} já existe!')
        user = User.objects.get(username=username)
        user.set_password(password)
        user.is_superuser = True
        user.is_staff = True
        user.save()
        print(f'Senha do usuário {username} foi atualizada para: {password}')
    else:
        # Criar novo superusuário
        user = User.objects.create_superuser(
            username=username,
            email=email,
            password=password
        )
        print(f'Superusuário criado com sucesso!')
        print(f'Username: {username}')
        print(f'Email: {email}')
        print(f'Senha: {password}')
    
    print('\nCredenciais para acessar o admin:')
    print(f'URL: http://localhost:8000/admin/')
    print(f'Username: {username}')
    print(f'Senha: {password}')

if __name__ == '__main__':
    create_superuser() 