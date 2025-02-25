# Используем самый свежий Python 3.12
FROM python:3.12

# Устанавливаем рабочую директорию внутри контейнера
WORKDIR /app

# Копируем файлы проекта в контейнер
COPY . .

# Устанавливаем зависимости (если есть requirements.txt — используем его)
RUN apt-get update && apt-get install -y git
RUN pip install --no-cache-dir --upgrade pip \
    && pip install Flask pytest

# Открываем порт (если приложение слушает другой порт, поменяй)
EXPOSE 5050

# Запускаем приложение
CMD ["python", "app.py"]
