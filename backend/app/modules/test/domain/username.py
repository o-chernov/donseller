# Username — часть адреса профиля (/<username>), правила как в GitHub:
# латиница, цифры и дефис; дефис только внутри и не два подряд.
# Хранится строчными: /Oleg и /oleg — один профиль.
USERNAME_MIN_LENGTH = 3
USERNAME_MAX_LENGTH = 39
USERNAME_PATTERN = r"^[a-zA-Z0-9]+(?:-[a-zA-Z0-9]+)*$"

# Имена, которые нужны самому проекту. Добавить имя сюда можно всегда,
# а отобрать занятое у пользователя — нет: поэтому в списке и разделы,
# которых ещё нет, но которые следуют из принятых планов.
#
# Адрес верхнего уровня во фронтенде — только из этого списка. Новый раздел —
# сначала имя сюда; если оно уже занято, раздел вкладывается под существующий
# адрес (например, /settings/...).
#
# Только допустимые username в нижнем регистре: адреса короче трёх символов
# (/en, /me) и с точкой (/robots.txt) защищены форматом. Ослабнет формат —
# пересмотреть список.
RESERVED_USERNAMES = frozenset({
    # Вход и аккаунт: модуль «Основа»; этими словами чаще всего маскируют фишинг
    "auth", "login", "logout", "signin", "signup", "register", "registration",
    "oauth", "callback", "confirm", "verify", "password", "email", "account",
    "profile", "settings",
    # Разделы продукта: модули из архитектуры, подписка PRO, планировщик, учёт времени
    "dashboard", "integrations", "activity", "tournament", "leaderboard", "seasons",
    "analytics", "insights", "messages", "notifications", "billing", "subscription",
    "pro", "upgrade", "checkout", "planner", "time", "onboarding", "search",
    # Страницы сайта
    "about", "features", "pricing", "faq", "help", "support", "contact", "legal",
    "terms", "privacy", "docs", "blog", "changelog",
    # Служебное: поддомены и статика
    "api", "app", "www", "admin", "static", "assets", "media", "health",
    # Бренд и доверие: от этих имён можно написать пользователю «от лица проекта»
    "myway", "mywayis", "administrator", "root", "moderator", "staff", "team",
    "official", "system", "security", "bot", "noreply", "no-reply", "abuse", "info",
    # Технические значения и заглушки: ломают шаблоны и логи, путаются с удалённым аккаунтом
    "null", "undefined", "none", "nan", "true", "false", "self", "new", "edit",
    "anonymous", "guest", "unknown", "deleted", "user",
})


def is_reserved_username(username: str) -> bool:
    return username.lower() in RESERVED_USERNAMES
