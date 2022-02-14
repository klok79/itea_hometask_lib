from lib_utils.book import Book
from lib_utils.reader import Reader

class StorageEx:

    # ------------------------------------------------------------------------------------------------------------------
    def __init__(self, list_classnames: list, list_sources: list):
        """
        Батьківський клас для всіх класів коннекторів зберігання/зчитування даних

        :param list_classnames: Перелік назв класів об'єктів, запис/зчитування яких підтримується
        :param list_sources: Перелік шляхів до джерела даних відповідних класів
        """
        if len(list_classnames) != len(list_sources):
            raise AttributeError (f'Перелікт list_classnames list_paths мають не однакову кількість значень')
        self.class_names = list_classnames
        self.sources = list_sources
        self.book_mode = False      # Значення True буде означати, що процедури load та dump дочірніх класів
        self.reader_mode = False    # читають / пишуть дані книг / читачів

    # ------------------------------------------------------------------------------------------------------------------
    def get_source(self, class_name: str) -> str:
        """
        Метод вертає джерело даних для класу з вказаною назвою

        :param class_name: Назва класу, джерело даних якого необхідно отримати.
        При передчі назви класу, який не підтримується - ненерується помилка AttributeError
        :return: Джерело даних
        """
        for i in range(len(self.class_names)):
            if self.class_names[i] == class_name:
                return self.sources[i]
        raise AttributeError(f'Класс {class_name} не підтримується')

    # ------------------------------------------------------------------------------------------------------------------
    def set_mode(self, class_name: str) -> None:
        """
        Метод встановлює режим типу об'яктів що будуть записуватися / зчитуватися по назві класу.
        При передчі назви класу, який не підтримується - ненерується помилка AttributeError

        :param class_name: Назва класу, режим роботи з яким необхідно встановити
        :return: Нічого
        """
        if class_name not in (Book.__name__, Reader.__name__):
            raise AttributeError(f'Класс {class_name} не підтримується')
        self.book_mode = class_name == Book.__name__
        self.reader_mode = class_name == Reader.__name__

    # ------------------------------------------------------------------------------------------------------------------
    @staticmethod
    def show_messages(message_list: list, need_wait: bool):
        if message_list:
            for message in message_list:
                print(message)
            if need_wait:
                input('Натисніть що небудь для продовження: ')

    # ------------------------------------------------------------------------------------------------------------------
    # @staticmethod
    # def false_include(*args):
