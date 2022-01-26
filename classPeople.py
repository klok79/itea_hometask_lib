# 3. Класс People
# - ???
# Методы:
# ???
class People:
    def __init__(self, id, name, birthday):
        """

        :param reader_name:
        :param birthday:
        :param book_list:
        """
        self.id = id
        self.name = name
        self.birthday = birthday


    def __str__(self):
        return f"id: {self.id}, ім'я: {self.name}, дата народження: {self.birthday}"


