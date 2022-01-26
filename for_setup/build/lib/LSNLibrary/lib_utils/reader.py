# 3. Класс People
# - ???
# Методы:
# ???
class Reader:
    def __init__(self, uin, name, birthday):
        """

        :param reader_name:
        :param birthday:
        :param book_list:
        """
        self.uin = uin
        self.name = name
        self.birthday = birthday


    def __str__(self):
        return f"id: {self.uin}, ім'я: {self.name}, дата народження: {self.birthday}"


