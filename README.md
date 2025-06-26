# Como rodar o projeto com Docker

1. Copie o arquivo `.env.example` para `.env` e ajuste as variáveis conforme necessário.
2. Execute `docker-compose up --build` para subir o ambiente (Django + PostgreSQL).
3. O Django estará disponível em `http://localhost:8000`.

# Comandos úteis
- Para rodar migrações: `docker-compose exec web python manage.py migrate`
- Para criar superusuário: `docker-compose exec web python manage.py createsuperuser` 