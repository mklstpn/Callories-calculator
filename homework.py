import datetime as dt
from typing import Optional


class Record():
    """Класс в котором мы получаем данные, которые ввел пользователь
    И форматируем дату в пригодный для дальнейшей работы формат.
    """

    DATE_FORMAT = '%d.%m.%Y'

    def __init__(self, amount, comment, date: Optional[str] = None) -> None:
        self.amount = amount
        self.comment = comment
        if date is None:
            self.date = dt.date.today()
        else:
            self.date = dt.datetime.strptime(
                date, Record.DATE_FORMAT).date()


class Calculator():
    """Родительский класс в котором определены основные методы:
    add_record() - добавляет новую запись в список
    get_today_stats() - суточная сумма всех трат или съеденных каллорий
    get_week_stats() - недельная сумма всех трат или съеденных каллорий.
    """
    today = dt.date.today()

    def __init__(self, limit) -> None:
        self.limit = limit
        self.records = []

    def add_record(self, record):
        self.records.append(record)

    def get_today_stats(self):
        today_stat = []
        for record in self.records:
            if record.date == Calculator.today:
                today_stat.append(record.amount)
        today_amount = sum(today_stat)
        return today_amount

    def get_week_stats(self):
        week_stat = []
        week = Calculator.today - dt.timedelta(days=7)
        for record in self.records:
            if week < record.date and record.date <= self.today:
                week_stat.append(record.amount)
        week_amount = sum(week_stat)
        return week_amount

    def get_balance(self):
        balance_left = self.limit - self.get_today_stats()
        return balance_left


class CashCalculator(Calculator):
    """Дочерний класс в котором определены методы калькулятора денег:
    Метод get_today_cash_remained() вычисляет сумму оставшихся денег
    пользователя в различной валюте.
    """
    EURO_RATE: float = 89.91
    USD_RATE: float = 73.70
    RUB_RATE: float = 1

    def __init__(self, limit) -> None:
        super().__init__(limit)

    def get_today_cash_remained(self, currency):
        currences = {'eur': ('Euro', CashCalculator.EURO_RATE),
                     'usd': ('USD', CashCalculator.USD_RATE),
                     'rub': ('руб', CashCalculator.RUB_RATE)}
        name, rate = currences[currency]
        if currency not in currences:
            return 'Неверный формат валюты'
        cash_left = round(Calculator.get_balance(self) / rate, 2)
        if cash_left > 0:
            alert = f'На сегодня осталось {cash_left} {name}'
            return alert
        if cash_left < 0:
            cash_left = abs(cash_left)
            alert = (f'Денег нет, держись: твой долг - '
                     f'{cash_left} {name}')
            return alert
        if cash_left == 0:
            return 'Денег нет, держись'


class CaloriesCalculator(Calculator):
    """Дочерний класс в котором определены методы калькулятора каллорий:
    Метод get_calories_remained() вычисляет количество каллорий,
    которые пользователь еще может получить.
    """

    def get_calories_remained(self):
        calories_left = Calculator.get_balance(self)
        if calories_left > 0:
            return (f'Сегодня можно съесть что-нибудь ещё, но с общей '
                    f'калорийностью не более {calories_left} кКал')
        return 'Хватит есть!'
