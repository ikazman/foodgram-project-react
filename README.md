![foodgram_project_react workflow](https://github.com/ikazman/foodgram-project-react/actions/workflows/main.yml/badge.svg)

# foodgram_finale_project
### Описание проекта:

Cайт Foodgram, «Продуктовый помощник»: yа этом сервисе пользователи могут публиковать рецепты, подписываться на публикации других пользователей, добавлять понравившиеся рецепты в список «Избранное», а перед походом в магазин скачивать сводный список продуктов, необходимых для приготовления одного или нескольких выбранных блюд.

&nbsp;

### Как запустить проект:
&nbsp;

1) Клонировать репозиторий и перейти в него в командной строке:

```bash
git clone git@github.com:ikazman/foodgram-project-react.git
```

```bash
cd foodgram-project-react
```

2) Подключиться к серверу из терминала
```bash
ssh <username>@<ip-adress>
```

3) Установить docker и docker-compose, дать необходимый допуск docker-compose
```bash
sudo apt install docker.io
```
```bash
sudo curl -L "https://github.com/docker/compose/releases/download/1.29.2/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
```
```bash
sudo chmod +x /usr/local/bin/docker-compose
```

4) В локальном файле nginx/default.conf указать публичный ip-адрес сервера

5) Скопировать на сервер docker-compose.yaml и nginx/default.conf:
```bash
scp docker-compose.yaml <username>@<ip-adress>:/home/<username>/
scp -r nginx/default.conf <username>@<ip-adress>:/home/<username>/
```
6) Добавить в Secrets GitHub Actions переменные окружения:
```bash

#на сервере отладка должна быть выключена
DEBUG=False

ALLOWED_HOSTS = ['localhost', '127.0.0.1',] # явно указываем разрешенные хосты

DB_ENGINE=django.db.backends.postgresql # указываем, что работаем с postgresql
DB_NAME=<имя базы данных>
POSTGRES_USER=<имя пользователя базы данных>
POSTGRES_PASSWORD=<пароль для базы данных>
DB_HOST=<название сервиса (контейнера)>
DB_PORT=5432 # порт для подключения к БД 
SECRET_KEY=<секретный ключ проекта> # ключ для сборки Джанго


CLOUD_HOST=<публичный ip-адрес сервера>
CLOUD_USER=<имя пользователя для подключения к серверу>

DOCKER_PASSWORD=<пароль от dockerhub>
DOCKER_USERNAME=<имя пользователя dockerhub>

SSH_KEY=<приватная часть SSH-ключа>
SSH_PASSPHRASE=<секретная фраза для SSH-ключа> # если установлена

TELEGRAM_TO=<id пользователя, которому будет направлено сообщение>
TELEGRAM_TOKEN=<токен бота, который будет направлять сообщение>

```

7) После деплоя выполнить на серевере команды для миграций и сбора статики:
```python
sudo docker-compose exec backend python manage.py migrate --no-input
sudo docker-compose exec backend python manage.py collectstatic --no-input
```
8) Выполнить на сервере команды для заполения базы:

```python
docker-compose exec backend python manage.py guybrush --path data
```
&nbsp;
---
### Документация к api: http://217.28.228.130/api/doc/
&nbsp;

### Образ на DockerHub: ikazmandockerhub/foodgram:latest 
