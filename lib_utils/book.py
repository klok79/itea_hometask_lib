# 2. Класс книга
# Поля:
# - ID
# - Название
# - Автор
# - Год издания
# - ??? (этот параметр нужен!!!)

class Book:

    def __init__(self, uin: int, title: str, author: str, publishing_year: int, reader_uin: int = -1):
        """
        Об'єкт буде створюватися вже після того як введені Назва, автор, рік видавництва.
        Книга відразу стає доступною для видачі
        title (Назва) - довільний текст, не пусто
        author (Автор) - три capitalized слова
        publishing_year (Рік публікації) - число від 0 до поточного року
        uin - унікальний номер книги. При додаванні книги має формуватися автоматично як наступний після найбільшого
              серед всіх книг необхідний алгоритм його визначення, визначений в класі бібліотеки, бо перелік всіх
              книг зберігається саме в бібліотеці
        reader_id - Унікальний номер користувача, якому видана дана книга, якщо книга в бібліотеці - то <0
        """
        self.title = title
        self.author = author
        self.publishing_year = publishing_year
        self.uin = uin
        self.reader_uin = reader_uin


    def __str__(self):
        status = 'знаходиться ' + 'в бібліотеці' if self.reader_uin < 0 else f'на руках у читача {self.reader_uin}'
        return f'id:{self.uin}, автор: {self.author}, назва: {self.title}, рік публікації: {self.publishing_year}, {status}'


















