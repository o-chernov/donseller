#!/bin/sh
# Запуск контейнера Donseller: дождаться базы, применить миграции,
# затем выполнить команду из CMD (uvicorn).
set -eu

# Ждём базу до 60 секунд: после перезагрузки сервера приложение может
# стартовать раньше PostgreSQL. В slim-образе нет pg_isready, поэтому
# проверяем настоящим подключением через asyncpg. Не дождались — выходим
# с ошибкой, Docker перезапустит контейнер.
python - <<'PY'
import asyncio
import os
import sys
import time

import asyncpg

TIMEOUT = 60


async def wait_for_db(url: str) -> None:
    deadline = time.monotonic() + TIMEOUT
    waiting = False
    while True:
        try:
            conn = await asyncpg.connect(url, timeout=5)
        except Exception as exc:
            if time.monotonic() >= deadline:
                print(f"entrypoint: база недоступна {TIMEOUT} с: {exc!r}", file=sys.stderr)
                sys.exit(1)
            if not waiting:
                print(f"entrypoint: жду базу (до {TIMEOUT} с): {exc!r}", file=sys.stderr)
                waiting = True
            await asyncio.sleep(2)
        else:
            await conn.close()
            if waiting:
                print("entrypoint: база доступна", file=sys.stderr)
            return


url = os.environ.get("DATABASE_URL")
if not url:
    print("entrypoint: не задан DATABASE_URL (см. .env)", file=sys.stderr)
    sys.exit(1)
asyncio.run(wait_for_db(url))
PY

# Миграции: alembic применяет только новые, повторный запуск безопасен
alembic upgrade head

# Заменяем shell на команду из CMD, чтобы сигналы остановки шли прямо ей
exec "$@"
