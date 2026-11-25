# Образ Donseller: FastAPI + uvicorn в одном процессе.
# Собирается на сервере из архива коммита (см. DEPLOY.md), позже — в GitHub Actions.

# Python 3.13, как в разработке, на Debian 13 (trixie), вариант slim.
# Минорная версия Python и релиз Debian закреплены. Исправления безопасности
# базового образа приходят при сборке с --pull (так в DEPLOY.md).
FROM python:3.13-slim-trixie

# Без .pyc на диске (в контейнере файловая система только для чтения),
# вывод сразу в лог, pip без кэша и без лишних предупреждений
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    PIP_ROOT_USER_ACTION=ignore

WORKDIR /app

# Зависимости — отдельным слоем до кода: пока requirements.txt не меняется,
# Docker берёт этот слой из кэша и не ставит пакеты заново
COPY backend/requirements.txt ./
RUN pip install -r requirements.txt

# Непривилегированный пользователь с фиксированным uid/gid 10001.
# Этот же uid должен быть владельцем папки data/, если она понадобится
RUN groupadd --gid 10001 app \
 && useradd --uid 10001 --gid 10001 --no-create-home --shell /usr/sbin/nologin app

# Скрипт запуска. Бит исполнения ставим здесь: при коммите с Windows он теряется
COPY --chmod=0755 entrypoint.prod.sh /usr/local/bin/entrypoint.prod.sh

# Код и миграции. Владелец — root: приложение не может их изменить
COPY backend/alembic.ini ./
COPY backend/alembic ./alembic
COPY backend/app ./app

USER 10001:10001

EXPOSE 8000

# Перед стартом entrypoint ждёт базу и применяет миграции, затем запускает CMD.
# Один воркер: всё состояние приложения живёт в одном процессе.
# --proxy-headers и --forwarded-allow-ips '*': реальный IP клиента и https
# из заголовков nginx. Это безопасно: порт опубликован только на 127.0.0.1,
# а nginx перезаписывает X-Forwarded-For. Адрес шлюза Docker-сети, с которого
# приходят запросы, заранее неизвестен, поэтому '*'.
ENTRYPOINT ["/usr/local/bin/entrypoint.prod.sh"]
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "1", "--proxy-headers", "--forwarded-allow-ips", "*"]
