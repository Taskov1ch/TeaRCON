from provider import db
from resources import config

async def console_add_super_admin() -> None:
	if config.console()["give_role"]:
		while True:
			admin_id = input(
				"Введите id для выдачи прав super-админа или нажмите Enter для пропуска: "
			)
			if admin_id == "":
				print("Закрытие")
				break;
			elif await db.check_admin_user(admin_id):
				print(f"{admin_id} уже есть в списке супер-админов")
			else:
				await db.add_admin(admin_id)
				print(f"{admin_id} был добавлен в список супер-админов")
	else:
		print("Режим выдачи роли выключен. Пропускаем")