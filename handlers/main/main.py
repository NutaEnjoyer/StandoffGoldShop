import datetime

from aiogram import types
from aiogram.dispatcher import FSMContext

import config
import handlers.main.templates as templates
from bot_data.start_bot import bot

from db.models import User

from .states import *


async def start_handler(message: types.Message, state: FSMContext):
	u = User.get_or_none(user_id=message.from_user.id)
	if not u:
		u = User.create(user_id=message.from_user.id, register_at=datetime.datetime.now())
		u.save()
	await message.answer(templates.start, reply_markup=templates.start_keyboard)
	photo = types.InputFile("images/Добро пожаловать.jpg")
	await message.answer_photo(photo, caption=templates.welcome, reply_markup=templates.start_inline_keyboard)


async def reviews_handler(message: types.Message, state: FSMContext):
	photo = types.InputFile("images/Отзывы.jpg")

	await message.answer_photo(photo, caption=templates.reviews, reply_markup=templates.reviews_markup)

async def support_handler(message: types.Message, state: FSMContext):
	photo = types.InputFile("images/Помощь.jpg")

	await message.answer_photo(photo, caption=templates.support, reply_markup=templates.support_markup)

async def profile_handler(message: types.Message, state: FSMContext):
	photo = types.InputFile("images/Профиль.jpg")

	u = User.get_or_none(user_id=message.from_user.id)
	if not u: return

	await message.answer_photo(photo, caption=templates.profile(
		message.from_user.username, message.from_user.id, u.register_at
	), reply_markup=templates.profile_markup)

async def profile_handler_for_call(call: types.CallbackQuery, state: FSMContext):
	await state.finish()
	photo = types.InputFile("images/Профиль.jpg")

	u = User.get_or_none(user_id=call.from_user.id)
	if not u: return

	await call.message.answer_photo(photo, caption=templates.profile(
		call.from_user.username, call.from_user.id, u.register_at
	), reply_markup=templates.profile_markup)

async def withdraw_handler(message: types.Message, state: FSMContext):
	await state.set_state(MyState.SendSell)
	photo = types.InputFile("images/Введите кол-во.jpg")

	await message.answer_photo(photo, caption=templates.withdraw, reply_markup=templates.withdraw_markup)

async def buy_gold_handler(message: types.Message, state: FSMContext):
	await state.set_state(MyState.SendBuy)
	photo = types.InputFile("images/Введите кол-во.jpg")

	await message.answer_photo(photo, caption=templates.buy_gold, reply_markup=templates.buy_gold_markup)

async def send_sell(message: types.Message, state: FSMContext):
	photo = types.InputFile("images/Введите кол-во.jpg")

	await message.answer_photo(photo, caption=templates.not_enough, reply_markup=templates.not_enough_markup)

async def send_buy(message: types.Message, state: FSMContext):
	photo = types.InputFile("images/Подтвердите заказ.jpg")

	await message.answer_photo(photo, caption=templates.accept_order(int(message.text)), reply_markup=templates.accept_order_markup)
	await state.update_data(gold=int(message.text) * config.price)

async def send_promocode(message: types.Message, state: FSMContext):
	await state.finish()
	await message.answer("<b>ℹ️ Купон не найден или закончилась активация.</b>", reply_markup=templates.back_markup)

async def edit_amount(call: types.CallbackQuery, state: FSMContext):
	await call.message.delete()
	await withdraw_handler(call.message, state)

async def call_buy_gold(call: types.CallbackQuery, state: FSMContext):
	await call.message.delete()
	await buy_gold_handler(call.message, state)

async def withdrawal_history(call: types.CallbackQuery, state: FSMContext):
	await call.message.delete()

	photo = types.InputFile("images/История выводов.jpg")
	await call.message.answer_photo(photo, caption=templates.withdrawal_history, reply_markup=templates.back_markup)


async def invite_friend(call: types.CallbackQuery, state: FSMContext):
	await call.message.delete()

	photo = types.InputFile("images/Кэш за приглашение.jpg")
	u = User.get(user_id=call.from_user.id)
	await call.message.answer_photo(photo, caption=templates.invite_friend(call.from_user.username, call.from_user.id, u.register_at), reply_markup=templates.back_markup)


async def promocode(call: types.CallbackQuery, state: FSMContext):
	await call.message.delete()
	await state.set_state(MyState.SendPromoCode)
	photo = types.InputFile("images/Ведите купон.jpg")

	await call.message.answer_photo(photo, caption=templates.promocode, reply_markup=templates.back_markup)

async def back_handler(call: types.CallbackQuery, state: FSMContext):
	await call.message.delete()
	await profile_handler_for_call(call, state)

async def accept_order(call: types.CallbackQuery, state: FSMContext):
	await call.message.delete()

	await state.set_state(MyState.Payment)

	photo = types.InputFile("images/Способ оплаты.jpg")
	await call.message.answer_photo(photo, caption=templates.choose_payment, reply_markup=templates.choose_payment_markup)

async def choose_pay(call: types.CallbackQuery, state: FSMContext):
	pay = int(call.data.split('$')[1])
	await call.message.delete()
	data = await state.get_data()
	await state.finish()
	photo = types.InputFile("images/Оплатите заказ.jpg")

	await call.message.answer_photo(photo, caption=templates.send_money(data.get('gold'), pay), reply_markup=templates.send_money_markup)

async def money_sended(call: types.CallbackQuery, state: FSMContext):
	await call.message.delete()
	await call.message.answer(templates.send_photo, reply_markup=templates.send_photo_markup)


async def cancel_order(call: types.CallbackQuery, state: FSMContext):
	await call.message.delete()

async def send_photo(message: types.Message, state: FSMContext):
	await bot.delete_message(message.from_user.id, message.message_id)

	photo = types.InputFile("images/Заявка принята.jpg")
	await message.answer_photo(photo, caption=templates.sended_photo)

async def buy_upGold(call: types.CallbackQuery, state:FSMContext):
	await call.message.delete()

	photo = types.InputFile("images/Подписка UpGold.jpg")
	await call.message.answer_photo(photo, caption=templates.buy_upGold, reply_markup=templates.buy_upGold_markup)

async def buy_up_gold(call: types.CallbackQuery, state:FSMContext):
	await call.message.delete()

	await state.set_state(MyState.Payment)
	await state.update_data(gold=config.upGoldPrice)

	photo = types.InputFile("images/Способы оплаты.jpg")
	await call.message.answer_photo(photo, caption=templates.choose_payment,
									reply_markup=templates.choose_payment_markup)

def register_handlers(dp):
	dp.register_message_handler(start_handler, commands=['start', 'restart'], state='*')
	dp.register_message_handler(reviews_handler, text="🤍 Отзывы", state='*')
	dp.register_message_handler(support_handler, text="❓ Помощь", state='*')
	dp.register_message_handler(profile_handler, text="🤵 Профиль", state='*')
	dp.register_message_handler(buy_gold_handler, text="⭐️ Купить Gold", state='*')
	dp.register_message_handler(withdraw_handler, text="📤 Вывести Gold", state='*')

	dp.register_message_handler(send_buy, content_types=['text'], state=MyState.SendBuy)
	dp.register_message_handler(send_sell, content_types=['text'], state=MyState.SendSell)
	dp.register_message_handler(send_promocode, content_types=['text'], state=MyState.SendPromoCode)

	dp.register_callback_query_handler(edit_amount, text="edit_amount", state=MyState.SendSell)
	dp.register_callback_query_handler(call_buy_gold, text="buy_gold", state="*")

	dp.register_callback_query_handler(withdrawal_history, text="withdrawal_history", state="*")
	dp.register_callback_query_handler(invite_friend, text="invite_friend", state="*")
	dp.register_callback_query_handler(promocode, text="promocode", state="*")
	dp.register_callback_query_handler(back_handler, text="back", state="*")

	dp.register_callback_query_handler(accept_order, text="accept_order", state=MyState.SendBuy)
	dp.register_callback_query_handler(choose_pay, text_startswith="pay", state=MyState.Payment)
	dp.register_callback_query_handler(money_sended, text_startswith="money_sended", state="*")
	dp.register_callback_query_handler(cancel_order, text_startswith="cancel_order", state="*")

	dp.register_message_handler(send_photo, content_types=['photo'], state="*")

	dp.register_callback_query_handler(buy_upGold, text="buy_upGold", state='*')
	dp.register_callback_query_handler(buy_up_gold, text="buy_up_gold", state='*')
