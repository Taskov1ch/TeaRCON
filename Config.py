#          Free версия бота проекта LostWeyn
#              Telegram: t.me/lostweyn_project
#
#          Контакты разработчика:
#              VK: vk.com/dimawinchester
#              Telegram: t.me/teanus
#              Github: github.com/teanus
#              24serv: talk.24serv.pro/u/teanus
#
#
#     ██╗      ██████╗ ███████╗████████╗██╗    ██╗███████╗██╗   ██╗███╗   ██╗
#     ██║     ██╔═══██╗██╔════╝╚══██╔══╝██║    ██║██╔════╝╚██╗ ██╔╝████╗  ██║
#     ██║     ██║   ██║███████╗   ██║   ██║ █╗ ██║█████╗   ╚████╔╝ ██╔██╗ ██║
#     ██║     ██║   ██║╚════██║   ██║   ██║███╗██║██╔══╝    ╚██╔╝  ██║╚██╗██║
#     ███████╗╚██████╔╝███████║   ██║   ╚███╔███╔╝███████╗   ██║   ██║ ╚████║
#     ╚══════╝ ╚═════╝ ╚══════╝   ╚═╝    ╚══╝╚══╝ ╚══════╝   ╚═╝   ╚═╝  ╚═══╝


TELEGRAM_TOKEN = 'token'  # токен бота телеграмм
db_name = 'rcon_bot.db'
MC_HOST = '127.0.0.1'  # ip адрес сервера - сейчас указан localhost
MC_PASSWORD = 'pass'  # rcon пароль сервера
MC_IP = 25576  # ркон порт сервера


console_on_role = True  # включение выдачи супер-админа через консоль (рекомендую оставить так)


on_logger_group = True  # логгирование в группе телеграмм (True - вкл, False - выкл)
logger_chat_id = ''  # id группы для логирования бота (если включено)
black_list = ['stop', 'reload', 'op', 'deop']  # список запрещенных команд
