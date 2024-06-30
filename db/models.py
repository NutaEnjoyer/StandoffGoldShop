from peewee import *

database = SqliteDatabase('database.db')

class BaseModel(Model):
	id = PrimaryKeyField()

	class Meta:
		database = database


class User(BaseModel):
	user_id = IntegerField()
	register_at = DateTimeField()
	gold = IntegerField(default=0)
	UpGoldUpTo = DateTimeField(null=True)
	deposite_amount = IntegerField(default=0)
	gold_buyed_amount = IntegerField(default=0)


class Withdrawal(BaseModel):
	user_id = IntegerField()
	date = DateTimeField()
	amount = IntegerField()


if __name__ == "__main__":
	database.create_tables([User])