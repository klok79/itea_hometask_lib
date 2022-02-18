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
        reader_id - Унікальний номер користувача, якому видана дана книга, якщо книга в бібліотеці - то < 0
        """
        self.title = title
        self.author = author
        self.publishing_year = publishing_year
        self.uin = uin
        self.reader_uin = reader_uin

    def __str__(self):
        status = 'знаходиться ' + 'в бібліотеці' if self.reader_uin < 0 else f'на руках у читача {self.reader_uin}'
        return f'id:{self.uin}, автор: {self.author}, назва: {self.title}, ' \
               f'рік публікації: {self.publishing_year}, {status}'

    def get_uin(self):
        return self.uin

    def get_title(self):
        return self.title

    def get_author(self):
        return self.author

    def get_year(self):
        return self.publishing_year

    def get_reader_uin(self):
        return self.reader_uin

    def get_attr_dict(self) -> dict:
        return {"uin": self.uin, "title": self.title, "author": self.author, "year": self.publishing_year, "reader_uin": self.reader_uin}

    @staticmethod
    def build_attr_dict(uin: int, title: str, author: str, publishing_year: int, reader_uin: int) -> dict:
        return {"uin": uin, "title": title, "author": author, "year": publishing_year, "reader_uin": reader_uin}

    @classmethod
    def create_object(cls, uin: int, title: str, author: str, publishing_year: int, reader_uin: int):
        return cls(uin, title, author, publishing_year, reader_uin)















