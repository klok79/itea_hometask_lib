from abc import ABC, abstractmethod


class Storage(ABC):
    """
    Абстрактний клас опису збереження та зчитування даних бібліотеки
    """
    @abstractmethod
    def dump(self, destination: str, source: str, obj_class) -> bool:
        """
        Метод має записувати весь перелік книг або читачів в якесь джерело

        :param destination: Шлях до фізичного джерела даних книг/читачів
        :param source: Перелік (list) зі словниками, в яких в якості ключів - поля цільового об'єкту:
                  для книги "uin", "title", "author", "publishing_year", "reader_uin"
                  для читача "uin", "name", "birthday". З відповідними значеннями
        :param obj_class: Клас об'єктів, що записуються
        :param obj_class: Клас об'єктів, що очікується записати
        :return: Ознаку успішності запису.
        """
        pass

    # def load(self, file_path: str, obj_class) -> tuple:
    @abstractmethod
    def load(self, source: str, obj_class) -> tuple :
        """
        Метод має зчитувати весь перелік книг або читачів з якогось джерела
        Перевіряти коректність даних. Не коректні записи мають ігноруються.

        :param source: Шлях до фізичного джерела даних книг/читачів
        :param obj_class: Клас об'єктів, що очікується зчитати
        :return: Кортеж із 3-х значень:
                  0.) перелік (list) зі словниками, в яких в якості ключів - поля цільового об'єкту:
                  для книги "uin", "title", "author", "publishing_year", "reader_uin"
                  для читача "uin", "name", "birthday". А значення - зчитані.
                  2.) перелік (list) повідомлень
                  3.) число. максимальний uin переліку книг, який необхідно передати бібліотеці
        """
        pass


