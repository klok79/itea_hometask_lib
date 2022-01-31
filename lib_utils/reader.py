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

    def get_uin(self):
        return self.uin

    def get_name(self):
        return self.name

    def get_birthday(self):
        return self.birthday

    def get_attr_dict(self) -> dict:
        return {"uin": self.uin, "name": self.name, "birthday": self.birthday}

    @staticmethod
    def build_attr_dict(uin: int, name: str, birthday: str) -> dict:
        return {"uin": uin, "name": name, "birthday": birthday}

    @classmethod
    def create_object(cls, uin: int, name: str, birthday: str):
        return cls(uin, name, birthday)