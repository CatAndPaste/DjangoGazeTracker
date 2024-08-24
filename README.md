### Django Gaze Tracking

Минимальное Django-приложение, которое использует библиотеку [GazeTracking](https://github.com/antoinelame/GazeTracking) для отслеживания направления взгляда на изображениях, полученных с камеры устройства пользователя. Пакет GazeTracking включен в проект.

### Установка

Для установки необходимых зависимостей выполните следующую команду из корневой директории проекта:

```pip install -r requirements.txt```

### Запуск приложения

Для запуска приложения с использованием uvicorn (необходим для работы WebSocket) на порту 8000 выполните из корневой директории проекта:

```uvicorn DjangoGazeTracker.asgi:application --host 0.0.0.0 --port 8000```

Или для доступа только с локальной машины:

```uvicorn DjangoGazeTracker.asgi:application --host 127.0.0.1 --port 8000```

После этого страница приложения будет доступна по адресу:

`http://<IP сервера>:8000/`
(`http://127.0.0.1:8000/`, если запущен локально)


### Docker

Скопируйте проект на удалённый сервер:

```
git clone https://github.com/CatAndPaste/DjangoGazeTracker.git
cd DjangoGazeTracker
```

И используйте из корневой директории проекта:

```
docker-compose build
docker-compose up
```

**Docker и Docker Compose должны быть установлены на удалённой машине (Ubuntu/Debian):**

```
sudo apt-get update
sudo apt-get install -y docker.io
```
```
sudo curl -L "https://github.com/docker/compose/releases/download/$(curl -s https://api.github.com/repos/docker/compose/releases/latest | grep -Po '"tag_name": "\K.*\d')/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose
```