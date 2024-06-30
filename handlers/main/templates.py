from aiogram import types
import config

start = """🏘 Меню"""

welcome = f"""<b>⭐️ Добро пожаловать в лучший магазин - UpStand!
Выбери один пункт из меню для начала работы.
💕Техническая поддержка - @{config.support_link}</b>"""


def rules_button(text: str = "📕 Правила", web_app_url="https://telegra.ph/Pravila-Magazina-04-23-5") -> types.InlineKeyboardButton:
	return types.InlineKeyboardButton(
		text=text,
		web_app=types.WebAppInfo(url=web_app_url)
	)

start_inline_keyboard = types.InlineKeyboardMarkup(
	inline_keyboard=[[rules_button(text="📕 Правила")]]
)

start_keyboard = types.ReplyKeyboardMarkup(
	resize_keyboard=True,
	keyboard=[
		[types.KeyboardButton("⭐️ Купить Gold"), types.KeyboardButton("📤 Вывести Gold")],
		[types.KeyboardButton("🤵 Профиль")],
		[types.KeyboardButton("🤍 Отзывы"), types.KeyboardButton("❓ Помощь")]
	]
)


reviews = """<b>💙 Отзывы наших клиентов:</b>"""

reviews_markup = types.InlineKeyboardMarkup(
	inline_keyboard=[
		[types.InlineKeyboardButton(text='🔗 Перейти', url=config.reviews_link)]
	]
)

support = """<b>❓ Если у тебя случилась проблема или нашел баг/ошибку в боте, напиши в тех поддержку.</b>

<i>ℹ️ Помощь работает с 8 до 23 по МСК</i>"""

support_markup = types.InlineKeyboardMarkup(
	inline_keyboard=[
		[types.InlineKeyboardButton(text='🧑‍💻 Обратиться за помощью', url=f"https://t.me/{config.support_link}")]
	]
)

def profile(username, user_id, time_created) -> str:
	text = f"""<b>🪪 Профиль Игрока</b>

👤 <b>Никнейм:</b> {username}
🆔 <b>TG ID:</b> <code>{user_id}</code>

⭐️ <b>Gold:</b> 0

💳 <b>Сумма пополнений:</b> 0 ₽ 
🌐 <b>Всего куплено Gold:</b> 0 G
📤 <b>Число выводов:</b> 0

👑 <b>UpGold:</b> Неактивен

ℹ️ {time_created.strftime("%Y.%m.%d %H:%M:%S")}"""

	return text


profile_markup = types.InlineKeyboardMarkup(
	inline_keyboard=[
		[types.InlineKeyboardButton(text='🏷️ Промокод', callback_data='promocode'), rules_button()],
		[types.InlineKeyboardButton(text='👑 Купить UpGold', callback_data='buy_upGold')],
		[types.InlineKeyboardButton(text='📚 История выводов', callback_data='withdrawal_history')],
		[types.InlineKeyboardButton(text='👥 Пригласить друга', callback_data='invite_friend')],
	]
)

withdraw = """<b>Для вывода голды просто введи желаемое количество. Например, отправь "100"

⭐️ Баланс: 0G</b>"""

withdraw_markup = types.InlineKeyboardMarkup(
	inline_keyboard=[
		[types.InlineKeyboardButton(text='⭐️Купить Gold', callback_data='buy_gold')],
		[rules_button("📌 Правила покупки")],
	]
)

buy_gold = """<b>Для покупки голды просто введи желаемое количество. Например, отправь "100"

Сколько голды ты хочешь купить? 💰</b>"""

buy_gold_markup = types.InlineKeyboardMarkup(
	inline_keyboard=[
		[rules_button("📌 Правила покупки")],
	]
)

not_enough = """<b>❌ Недостаточно Gold для вывода.

⭐️ Баланс: 0 G</b>"""

not_enough_markup = types.InlineKeyboardMarkup(
	inline_keyboard=[
		[types.InlineKeyboardButton(text='⭐️Купить Gold', callback_data='buy_gold')],
		[types.InlineKeyboardButton(text='🔄 Изменить количество', callback_data='edit_amount')],
	]
)

withdrawal_history = """<b>🗂 История выводов

📤 Всего выводов: 0</b>"""

def invite_friend(username, user_id, register_at):
	text = f"""<b>📈 Ваша личная статистика за все время:

🪪 Никнейм: {username}
💳 Баланс: 0
👥 Количество приглашенных: 0

🔗 Ваша ссылка:  <code>https://t.me/upstandoff_bot?start={user_id}</code></b>

<i>Дата регистрации: {register_at.strftime("%Y.%m.%d %H:%M:%S")}</i>"""

	return text

back_markup = types.InlineKeyboardMarkup(
	inline_keyboard=[
		[types.InlineKeyboardButton(text="◀️ Назад", callback_data='back')]
	]
)

promocode = """<b>Введите купон:</b>"""

def accept_order(gold):
	text = f"""<b>Итого:

💵 Сумма: {gold * config.price} руб.
⭐️ Кол-во: {gold} G</b>

<i>Мы берем комиссию рынка 25% на себя.</i>"""

	return text

accept_order_markup = types.InlineKeyboardMarkup(
	inline_keyboard=[
		[types.InlineKeyboardButton(text="✅ Подтвердить покупку", callback_data="accept_order")],
		[types.InlineKeyboardButton(text="🔄 Изменить количество", callback_data="buy_gold")],
	]
)

choose_payment = """<b>💳 Выбор Способа Оплаты</b>"""

choose_payment_markup = types.InlineKeyboardMarkup(
	inline_keyboard=[
		[types.InlineKeyboardButton(text="🟢 | Сбербанк", callback_data='pay$0')],
		[types.InlineKeyboardButton(text="🟣 | Юmoney", callback_data='pay$1')],
	]
)

def send_money(gold, pay):
	if pay == 0:
		p = "🟢 | Сбербанк"
	else:
		p = "🟣 | Юmoney"
	text = f"""<b>{p}:

💳 Карта: <code>{config.requisites[pay]}</code>

💰 Сумма: {gold} RUB

✅ После оплаты нажми кнопку «Оплатил»</b>"""

	return text

send_money_markup = types.InlineKeyboardMarkup(
	inline_keyboard=[
		[types.InlineKeyboardButton(text="✅ Оплатил", callback_data="money_sended")],
		[types.InlineKeyboardButton(text="❌ Отменить заказ", callback_data="cancel_order")]
	]
)

send_photo = """<b>Пришли фото чека!

<i>⚠️ На нем должно быть видно время, сумма и получатель.</i></b>"""

send_photo_markup = types.InlineKeyboardMarkup(
	inline_keyboard=[
		[types.InlineKeyboardButton(text="❌ Отменить заказ", callback_data="cancel_order")],
	]
)

sended_photo = """<b>✅ Заявка на пополнение принята.

⏳ Проверка чека в течение 1 часа. Ожидай!</b>"""

buy_upGold = f"""<b>👑 Подписка UpGold

💎 - Статус "Vip клиент": Выделите себя среди клиентов и получите особый статус.
⏩ - Ускоренный вывод: Вывод голды станет еще быстрее и удобнее.
🤝 - Персональная техподдержка: Ваш запрос всегда будет в приоритете.
💰 - 5% скидка на покупку голды: Экономьте при пополнении своего баланса.
🏆 - Участие в конкурсах: Получите шанс выиграть ценные призы в наших конкурсах среди спонсоров.

💸 Цена: {config.upGoldPrice}₽ в месяц.
</b>
<i>ℹ️ Данные привилегии будут доступы после покупки. Подписка оплачивается на месяц!</i>"""

buy_upGold_markup = types.InlineKeyboardMarkup(
	inline_keyboard=[
		[types.InlineKeyboardButton(text="✅ Купить подписку", callback_data="buy_up_gold")],
		[types.InlineKeyboardButton(text="◀️ Назад", callback_data='back')]
	]
)