from aiogram.dispatcher.filters.state import StatesGroup, State


class MyState(StatesGroup):
	SendBuy = State()
	SendSell = State()
	SendPromoCode = State()
	Payment = State()
