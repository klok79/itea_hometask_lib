# 1. Класс библиотека
# Поля:
# - +список книг (list Book)
# - +список читателей (list Reader)
# Методы:
# - + Добавить книгу
# - + Удалить книгу
# - Отдать книгу читателю
# - Принять книгу от читателя
# - +Вывести список всех книг
# - +Вывести список книг в библиотеке (в наличии)
# - +Вывести списк книг, которые не в наличии
# - Отсортировать список книг по названию, автору, году издания (lambda будет плюсом)


from lib_utils.book import Book
from lib_utils.reader import Reader
from lib_utils.tools import LibTools as tls
from lib_utils.storage_fts import FileTabsStorage
from os import system
from datetime import datetime


class Library:
    # --------------------------------------------------------- #
    def __init__(self):
        self._booklist_file_name = 'lib_data/book_list.txt'
        self._readerlist_file_name = 'lib_data/reader_list.txt'
        self._void_value = '-' * 5
        self.max_book_uin = 0
        self.max_reader_uin = 0
        self.head_len = 65
        self.pt_tab = '\t'
        self.pt_ln = '\n'
        self.list_book = self.load_list_book()
        self.list_reader = self.load_list_reader()
        self._booklist_saved = True
        self._readerlist_saved = True

    # ---------------------------------------------------------------------------------------------------------------- #
    @staticmethod
    def get_table_head(head: str, size: int, upper: bool = False) -> str:
        """
        Метод формує красиву шапочку для таблиці / меню

        :param head: Заголовок таблиці
        :param size: Ширина таблиці. Якщо вказана ширина менше кількості символів заголовку -
                     буде сформований блок шириною під заголовок
        :param upper: Ознака переведення заголовку у верхній регістр
        :return: Вертає рядок із заголовком по центру оздоблений з двох боків символами =
        """
        if upper:
            head = head.upper()
        len_head = len(head)
        if size < (len_head + 4):
            size = len_head + 4
        left = (size - len_head) // 2 - 1
        right = size - len_head - left - 2
        return f'{"=" * left} {head} {"=" * right}'

    # ---------------------------------------------------------------------------------------------------------------- #
    @staticmethod
    def clear_screen(condition: bool = True):
        """
        Метод умовної очистки консолі

        :param condition: Ознака необхідності очистки консолі
        :return: Не вертає нічого
        """
        if condition:
            system('cls')

    # ---------------------------------------------------------------------------------------------------------------- #
    def show_resume_action(self, prompt: str, bottom_len: int = None):
        """
        Метод виводить результат відпрацювання пункта меню. Скорочує запис кода

        :param prompt: Текст, який буде виведений як резюме роботи пункта меню
        :param bottom_len: Кількість символів риски підкреслювання після тексту
        :return: Не вертає нічого
        """
        if bottom_len is None:
            bottom_len = self.head_len
        print(f'{self.pt_ln}{prompt}{self.pt_ln}{"-" * bottom_len}')

    # ---------------------------------------------------------------------------------------------------------------- #
    def get_bookpos_by_uin(self, book_uin: int):
        """
        Метод вертає позицію книги з заданим uin в переліку книг

        :param book_uin: Унікальний номер книги, що розшукається
        :return: Порядковий номер (індекс) книги з вказаним номером в переліку книг або None, якщо такої книги немає
        """
        pos = 0
        for book in self.list_book:
            if book.uin == book_uin:
                return pos
            pos += 1

    # ---------------------------------------------------------------------------------------------------------------- #
    def get_readerpos_by_uin(self, reader_uin: int):
        """
        Метод вертає позицію читача з заданим uin в переліку читачів

        :param reader_uin: Унікальний номер книги, що розшукається
        :return: Порядковий номер (індекс) читача з вказаним номером в переліку читачів або None,
        якщо такого читача немає
        """
        pos = 0
        for reader in self.list_reader:
            if reader.uin == reader_uin:
                return pos
            pos += 1

    # ---------------------------------------------------------------------------------------------------------------- #
    def select_menu(self, title: str = None, menu_width: int = None, cls: bool = True, menu: dict = None,
                    question: str = 'Оберіть пункт меню'):
        """
        Метод готує консоль, виводить в неї словник, очікує вводу (input) ключа словника
        :param title: Заголовок меню
        :param menu_width: Ширина меню
        :param cls: Ознака необхідності попередньої очистки консолі
        :param menu: Словник, в якому ключі - це текстові значення (наразі числа), значення - довільний текст
        :param question: Текст, що буде виведений під таблицею меню
        :return: Введений текстовий ключ або None
        """
        Library.clear_screen(cls)
        if menu_width is None:
            menu_width = self.head_len
        if title is not None:
            print(self.get_table_head(f'{title}', menu_width, False))
        count = 0
        for key in menu:
            if len(key) > count:
                count = len(key)
        for key, value in menu.items():
            print(f'{key:>{count}}. {value}')
        if menu_width > 0:
            print('-' * menu_width)
        value = input(f'{question}: ')
        if value in menu:
            return value

    # ---------------------------------------------------------------------------------------------------------------- #
    def main_loop(self):
        """
        Метод диспетчер головного циклу. Виводить меню, очікує вводу та перенеаправляє потік
        :return: Нічого не вертає
        """
        main_menu = {
            '1': 'Додати книгу в бібліотеку',
            '2': 'Видалити книгу з  бібліотеки',
            '3': 'Зареєструвати нового читача',
            '4': 'Видалити читача',
            '5': 'Видати книгу читачу',
            '6': 'Прийняти книгу від читача',
            '7': 'Вивести перелік книг',
            '8': 'Вивести перелік читачів',
            '9': 'Відсортувати перелік книг',
            '10': 'Відсортувати перелік користувачів',
            '11': 'Зберегри / Завантажити',
            '12': 'Вивести пререлік книг без виєбонів',
            '13': 'Вивести пререлік читачів без виєбонів',
            '0': 'Завершити роботу'
        }
        menu_function = [
            self.before_exit,               # +0 Завершити роботу
            self.add_book,                  # +1 Додати книгу в бібліотеку
            self.delete_book,               # +2 Видалити книгу з бібліотеки (Можна тільки наявні в бібліотеці книги)
            self.add_reader,                # +3 Зареєструвати читача
            self.delete_reader,             # +4 Видалити читача (Можна тільки тих читачів, у яких немає книг на руках)
            self.give_out_book_to_reader,   # +5 Видати книгу читачу
            self.accept_book_from_reader,   # +6 Прийняти книгу від читача
            self.show_book_list,            # +7 Вивести перелік книг
            self.show_reader_list,          # +8 Вивести перелік читачів
            self.sort_list_book,            # +9 Відсортувати перелік книг
            self.sort_list_readers,         # +10 Відсортувати перелік користувачів
            self.file_job,                  # +11 Зберегти / Завантажити
            self.easy_show_listbook,        # +12 Вивести пререлік книг без виєбонів
            self.easy_show_readerbook       # +13 Вивести пререлік читачів без виєбонів
        ]
        while True:
            value = self.select_menu(title='ГОЛОВНЕ МЕНЮ БІБЛІОТЕКИ', menu=main_menu,
                                     question='Введіть номер дії, яку необхідно зробити')
            if value is not None:
                menu_function[int(value)]()
                if value == '0':
                    break
                else:
                    print('Натисніть Enter для продовження')
                    input()

    # ---------------------------------------------------------------------------------------------------------------- #
    def easy_show_listbook(self):
        for book in self.list_book:
            print(book)
        print(f'max_uin = {self.max_book_uin}')

    # ---------------------------------------------------------------------------------------------------------------- #
    def easy_show_readerbook(self):
        for reader in self.list_reader:
            print(reader)
        print(f'max_uin = {self.max_reader_uin}')

    # ---------------------------------------------------------------------------------------------------------------- #
    def add_book(self):
        """
        Метод очікує вводу послідовно назви, автора та року публікації книги перевіряє введені значення,
        створює та додає екземпляр книги в перелік книг.
        Скидає ознаку збереженості переліку книг
        :return: Нічого не вертає
        """
        Library.clear_screen()
        print(self.get_table_head('Додавання нової книги в бібліотеку', self.head_len, True))
        value = input('Введіть повністю наву книги: ')
        title = tls.check_value(value)
        if not title:
            self.show_resume_action('Назва книги не введена. Книга не додана.')
            return
        value = input("Введіть автора книги: ")
        author = tls.check_value(value)
        if not author:
            self.show_resume_action('Автор не введений. Книга не додана.')
            return
        value = input("Введіть рік публікації книги:")
        publ_year = tls.check_pulish_year(value)
        if not publ_year:
            s_err = 'не введений' if value == "" else f'[{value}] введений не корректно'
            self.show_resume_action(f'Рік публікації {s_err}. Книга не додана.')
            return
        self.max_book_uin += 1
        book = Book(self.max_book_uin, title, author, publ_year,  -1)
        self.list_book.append(book)
        self.show_resume_action(f'Книга "{book}" додана в бібліотеку')
        self._booklist_saved = False

    # ---------------------------------------------------------------------------------------------------------------- #
    def add_reader(self):
        """
        Метод очікує вводу, перевіряє введені значення, створює та додає екземпляр читача в перелік читачів
        Скидає ознаку збереженості переліку читачів
        :return: Нічого не вертає
        """
        Library.clear_screen()
        print(self.get_table_head('Реєстрація нового читача в бібліотеці', self.head_len, True))
        value = input("Введіть повне ім'я читача (ПІБ, титул, тощо): ")
        reader_name = tls.check_value(value)
        if not reader_name:
            self.show_resume_action("Ім'я читача не введене. Реєстрація відхилена.")
            return
        value = input("Введіть дату народження читача:")
        birthday = tls.check_date_str(value)
        if not birthday:
            s_err = 'не введена' if value == '' else f'[{value}] введена не коректно'
            self.show_resume_action(f'Дата дня народження {s_err}. Реєстрація відхилена.')
            return
        self.max_reader_uin += 1
        reader = Reader(self.max_reader_uin, reader_name, birthday)
        self.list_reader.append(reader)
        self.show_resume_action(f'Новий користувач  "{reader}" зареєстрований')
        self._readerlist_saved = False

    # ---------------------------------------------------------------------------------------------------------------- #
    def delete_book(self):
        """
        Метод виводить перелік не виданих книг, очікує вводу номера та видаляє вказану книгу
        Видалити можна тільки книги, що знаходяться в бібліотеці
        :return: Нічого не ветає
        """
        Library.clear_screen()
        print(self.get_table_head('Видалення книги з бібліотеки', self.head_len, True))
        if len(self.list_book) > 0:
            showed_books = self.show_book_list(-1, False, True)
            print('Видаленню підлягають тільки ті книги, які знаходяться в бібліотеці (не видані читачам на руки)')
            value = input('Введіть номер книги, яку необхідно видалити з бібліотеки: ').strip()
            if value in showed_books:
                book_pos = self.get_bookpos_by_uin(showed_books[value])
                del_book = str(self.list_book[book_pos])
                self.list_book.pop(book_pos)
                self.show_resume_action(f'Книга [{del_book}] видалена з бібліотеки')
                self._booklist_saved = False
            else:
                self.show_resume_action('Видалення книги відхилене')
        else:
            self.show_resume_action('В бібліотеці немає книг')

    # ---------------------------------------------------------------------------------------------------------------- #
    def delete_reader(self):
        """
        Метод виводить перелік читачів, що не мають книг на руках, очікує вводу номера та видаляє вказаного читача
        :return: Нічого не вертає
        """
        Library.clear_screen()
        print(self.get_table_head('Видалення читача з бібліотеки', self.head_len, True))
        if len(self.list_reader) > 0:
            showed_readers = self.show_reader_list(-1, False, True)
            print('Видаленню підлягають тільки ті читачі, які не мають на руках жодної книги')
            value = input('Введіть номер читача, якого необхідно видалити з бібліотеки: ').strip()
            if value in showed_readers:
                reader_pos = self.get_readerpos_by_uin(showed_readers[value])
                del_reader = str(self.list_reader[reader_pos])
                self.list_reader.pop(reader_pos)
                self.show_resume_action(f'Читач [{del_reader}] видалений з бібліотеки')
                self._readerlist_saved = False
            else:
                self.show_resume_action('Видалення читача відхилене')
        else:
            self.show_resume_action('У бібліотеки немає зареєстрованих читачів')

    # ---------------------------------------------------------------------------------------------------------------- #
    def file_job(self):
        """
        Метод реалізує опцію меню роботи з файлами шляхом відображення додаткового меню
        :return: Нічого не вертає
        """
        menu = {
            '1': 'Зберегти перелік книг у файл',
            '2': 'Завантажити перелік книг з файлу',
            '3': 'Зберегти перелік читачів у файл',
            '4': 'Завантажити перелік читачів з файлу'
        }
        value = self.select_menu(title='РОБОТА З ФАЙЛАМИ ДАНИХ', menu=menu, question='Оберіть необхідну дію')
        if value is not None:
            file_methods = [self.save_list_book,
                            self.load_list_book,
                            self.save_list_reader,
                            self.load_list_reader]
            file_methods[int(value) - 1]()
            self.show_resume_action('Файлова операція закінчена')
        else:
            self.show_resume_action('Дія не обрана. Операція відмінена')

    # ---------------------------------------------------------------------------------------------------------------- #
    def save_list_book(self):
        """
         Метод зберігає весь перелік книг в текстовий файл book_list.txt в директорії проекту
         В разі успішного збереження - встановлює ознаку збереженості переліку книг

        :return: Нічого не вертає
        """
        connector = FileTabsStorage(self.pt_tab,self.pt_ln, self._void_value)
        x_list = connector.fetch_dict_list(self.list_book, self.max_book_uin, Book)
        if connector.dump(self._booklist_file_name, x_list, Book):
            self._booklist_saved = True


    # ---------------------------------------------------------------------------------------------------------------- #
    def save_list_reader(self):
        """
        Метод зберігає весь перелік читачів в текстовий файл reader_list.txt в модулі проекту.
        В разі успішного збереження - встановлює ознаку збереженості переліку читачів

        :return: Нічого не вертає
        """
        connector = FileTabsStorage(self.pt_tab,self.pt_ln, self._void_value)
        x_list = connector.fetch_dict_list(self.list_reader, self.max_reader_uin, Reader)
        if connector.dump(self._readerlist_file_name, x_list, Reader):
            self._readerlist_saved = True

    # ---------------------------------------------------------------------------------------------------------------- #
    def load_list_book(self):
        """
        Метод намагається зчитати весь перелік книг з текстового файлу book_list.txt в модулі проекту
        Перевіряє коректність даних. Не коректні записи ігноруються. Встановлює max_uin книг та ознаку збереженості
        переліку книг

        :return: Список об'єктів книг, зчитаних з файла
        """

        connector = FileTabsStorage(self.pt_tab, self.pt_ln, self._void_value)
        x_dict, info_list, self.max_book_uin = connector.load(self._booklist_file_name, Book)
        book_list = connector.fetch_objects_list(x_dict, info_list, Book)
        self._booklist_saved = len(book_list) != 0
        return book_list

    # ---------------------------------------------------------------------------------------------------------------- #
    def load_list_reader(self):
        """
        Метод намагається зчитати весь перелік читачів з текстового файлу reader_list.txt в модулі проекту
        Перевіряє коректність даних. Не коректні записи ігноруються. Встановлює max_uin читачів та ознаку збереженості
        переліку читачів

        :return: Список об'єктів книг, зчитаних з файла
        """
        connector = FileTabsStorage(self.pt_tab, self.pt_ln, self._void_value)
        # x_dict, info_list, self.max_reader_uin = connector.load_readers(self._readerlist_file_name)
        x_dict, info_list, self.max_reader_uin = connector.load(self._readerlist_file_name, Reader)
        reader_list = connector.fetch_objects_list(x_dict, info_list, Reader)
        self._readerlist_saved = len(reader_list) != 0
        return reader_list

    # ---------------------------------------------------------------------------------------------------------------- #
    def give_out_book_to_reader(self):
        """
        Видати наявну в бібліотеці книгу зареєстрованому читачу
        Метод виводить перелік наявних книг та очікує вводу номеру книги, після чого виводить перелік всіх читачів та
        очікує вводу номеру читача.Якщо все введено коректно - вносить uin читача в reader_uin обраної книгу.
        Скидає ознаку збереженості переліку книг
        :return: Нічого не вертає
        """

        Library.clear_screen()
        print(self.get_table_head('видача книги читачу', self.head_len, True))
        showed_books = self.show_book_list(-1, False, True)
        if showed_books:
            value = input('Оберіть книгу, яку видати читачу на руки: ')
            if value in showed_books:
                book = self.list_book[self.get_bookpos_by_uin(showed_books[value])]
                showed_readers = self.show_reader_list(0, False, True)
                if showed_readers:
                    value = input('Оберіть читача, якому видається книга: ')
                    if value in showed_readers:
                        reader = self.list_reader[self.get_readerpos_by_uin(showed_readers[value])]
                        book.reader_uin = reader.uin
                        print(f'Книга [{book}] видана читачу [{reader}]')
                        self._booklist_saved = False
                    else:
                        print('Номер читача вказаний не коректно. Видача книги не можлива')
                else:
                    print('Відсутні зареєстровані читачі бібліотеки. Видача книги не можлива')
                # ---------------------------------
            else:
                print('Номер книги вказаний не коректно. Видача книги не можлива')
        else:
            print('Немає доступних книг. Видача книги не можлива')

    # ---------------------------------------------------------------------------------------------------------------- #
    def accept_book_from_reader(self):
        """
        Прийняти книгу від читача
        Метод виводить перелік читачів, у яких є книги на руках, очікує вводу номера.
        Якщо у вказаного читача на руках декілька книг  - виводить перелік цих книг та очікує вводу номера книги
        Якщо все введено коректно встановлює reader_uin обраної книги в -1

        :return: Нічого не вертає
        """

        Library.clear_screen()
        print(self.get_table_head('прийом книги від читача', self.head_len, True))
        showed_readers = self.show_reader_list(1, False, True)
        if showed_readers:
            value = input('Введіть номер читача, від якого приймається книга: ')
            if value in showed_readers:
                reader = self.list_reader[self.get_readerpos_by_uin(showed_readers[value])]
                reader_books = self.get_reader_books(reader.uin, 'list_book')
                showed_books = self.show_book_list(0, False, True, reader_books, f'книг читача {reader}')
                value = input('Оберіть книгу, яку необхідно прийняти від читача: ')
                if value in showed_books:
                    book = reader_books[int(value) - 1]
                    book.reader_uin = -1
                    print(f'Читач [{reader}] здав книгу [{book}] в бібліотеку')
                    self._booklist_saved = False
                else:
                    print('Номер книги вказаний не коректно. Прийом книги не можливий')
            else:
                print('Номер читача вказаний не коректно. Прийом книги не можливий')

        else:
            print('Відсутні читачі, які мають книги на руках. Прийом книги не можливий')

    # ---------------------------------------------------------------------------------------------------------------- #
    def show_book_list(self, book_status: int = None, cls: bool = True, ret_showed: bool = False,
                       target_list: list = None, tile: str = ''):
        """
        Метод виводить на екран таблицю з книгами
        :param book_status: book_status - вказівник, які книги виводити: (
                            більше 0 - Виводити книги, що видані читачам,
                            = 0  Виводити всі зареєстровані книги,
                            менше 0 - Виводити книги, що не видані читачам)
        :param cls: Ознака того, що перед виводом переліку необхідно очистити консоль
        :param ret_showed: Ознака того, що необхідно повернути перелік uin виведених в консоль книг
        :param target_list: перелік об'єктів книг з якого необхідно робити вивод згідно статусу. По замовчанню -
                    перелык всіх вниг бібліотеки
        :param tile: Заголовок таблиці в яку будуть виведені книги. По замовчанню значення обирається відповідно статусу
        :return: Якщо вказаний параметр ret_showed = True - вертає словник виведених книг в якому ключ - це
                 порядковий номер книги у виведеному переліку, а значення - uin цієї книги
        """

        # --------------------------------------*---------------
        def get_max_lens(target: list):
            """
            Допоміжний метод вичисляє максимальні довжини назви та автора книги

            :param target: Перелік об'єктів книг, для якого вираховуються значення
            :return: Кортеж (максимальна довжина поля автора, максимальна довжина поля назви)
            """
            x_max_author = 0
            x_max_title = 0
            for x_book in target:
                al = len(x_book.author)
                tl = len(x_book.title)
                x_max_author = al if al > x_max_author else x_max_author
                x_max_title = tl if tl > x_max_title else x_max_title
            return x_max_author, x_max_title

        # --------------------------------------*---------------
        def select_book_type(x_cls: bool):
            """
            Допоміжний метод додаткового вибору типу переліку

            :param x_cls: Ознака необхідності очистки консолі перед виводом меню вибора типу переліку
            :return: Число 0, -1 або 1 в залежності від вибору користувача
            """
            menu = {
                '1': 'Виводити всі книги, що зареєстровані в бібліотеці',
                '2': 'Виводити тільки ті книги, які видані читачам',
                '3': 'Виводити тільки ті книги, що знаходяться в бібліотеці (не видані читачам) ',
            }
            value = self.select_menu(title='ВИБІР КАТЕГОРІЮ КНИГДЛЯ ВИВОДУ', menu=menu, cls=x_cls, question='Оберіть категорію книг')
            if value is not None:
                return 0 if value == '1' else -1 if value == '3' else 1
            # --------------------------------------*---------------

        # ----- Розширення для будь-якого переліку книг ----- #
        if target_list is None:
            target_list = self.list_book
        else:
            book_status = 0
        # ----- Визначаємося з типом переліку книг -----
        if book_status is None:
            if not self.list_book:
                book_status = 0
            else:
                book_status = select_book_type(cls)
                if book_status is None:
                    print('Категорія переліку не обрана, перелік не буде виведений')
                    return
        # ----- Вичисляємо геометрію таблиці -----
        max_author, max_title = get_max_lens(target_list)
        max_num = len(str(self.max_book_uin))
        Library.clear_screen(cls)
        # ------------
        if tile == '':
            str_status = 'всіх книг' if book_status == 0 else 'книг, що видані читачам' if book_status > 0 else 'книг, що знаходяться в бібліотеці'
        else:
            str_status = tile
        # ------------
        total_len = 2 + max_num + 3 + max_author + 3 + max_title + 3 + 6
        print(self.get_table_head(f'перелік {str_status}', total_len, True))
        # ----- Для випадку коли треба повернути перелік uin виведених книг ----- #
        showed_books = {}
        # ----- Нічого не робимо, якщо книг немає -----
        if not target_list:
            print(f'В бібліотеці немає книг{self.pt_ln}{"-" * (total_len)}')
            return showed_books if ret_showed else None
        # ----- Вивод переліку -----
        book_pos = 0
        for book in target_list:
            succ = True if book_status == 0 else book.reader_uin > 0 if book_status > 0 else book.reader_uin < 0
            if succ:
                book_pos += 1
                if ret_showed:
                    showed_books[str(book_pos)] = book.uin
                print(f'| {book_pos:>{max_num}} | {book.author:<{max_author}} | {book.title:<{max_title}} | {book.publishing_year:4} |')
        if book_pos == 0:
            if book_status == 0:
                str_status = 'книг '
            print(f'{str_status} немає'.capitalize())
        print(f'{"-" * (total_len)}')
        if ret_showed:
            return showed_books

    # ---------------------------------------------------------------------------------------------------------------- #
    def show_reader_list(self, reader_status: int = None, cls:bool = True, ret_showed:bool = False):
        """
        Метод виводить на екран таблицю з читачами

        :param reader_status: вказівник, яких читаачів виводити:(
                                більше 0 - Виводити читачів, що мають на руках книги;
                                0  Виводити всіх читачів;
                                менше 0 - Виводити читачів, що не мають книг на руках;)

        :param cls: Ознака того, що перед виводом переліку необхідно очистити консоль
        :param ret_showed: Ознака того, що необхідно повернути перелік uin виведених в консоль книг
        :return: Якщо вказаний параметр ret_showed = True - вертає словник виведених читачів в якому ключ - це
                 порядковий номер книги у виведеному переліку, а значення - uin цього читача
        """

        # --------------------------------------------------------------
        def get_longer_name_len() -> int:
            """
            Допоміжний метод вичисляє максимальну довжини імені читача

            :return: Максимальну довжину імені читача в переліку читачів
            """
            max_name = 0
            for reader in self.list_reader:
                nl = len(reader.name)
                if nl > max_name:
                    max_name = nl
            return max_name

        # --------------------------------------------------------------
        def select_reader_type(x_cls) -> int:
            """
            Допоміжний метод додаткового вибору типу переліку

            :param x_cls: Ознака необхідності очистки консолі перед виводом меню
            :return: Число 0, -1 або 1 в залежності від вибору користувача
            """
            menu = {
                '1': 'Виводити всіх зареєстрованих читачів',
                '2': 'Виводити тільки тих читачів, які мають книги на руках',
                '3': 'Виводити тільки тих читачів, які не мають книг на руках',
            }
            value = self.select_menu(title='ВИБІР КАТЕГОРІї ЧИТАЧІВ ДЛЯ ВИВОДУ', cls=x_cls, menu=menu, question='Оберіть категорію читачів')
            if value is not None:
                return 0 if value == '1' else -1 if value == '3' else 1

        # ----- Визначаємося з типом переліку читачів -----
        if reader_status is None:
            if not self.list_reader:
                reader_status = 0
            else:
                reader_status = select_reader_type(cls)
                if reader_status is None:
                    print('Категорія переліку не обрана, перелік не буде виведений')
                    return
        # ----- Вичисляємо геометрію таблиці -----
        max_name = get_longer_name_len()
        max_num = len(str(self.max_reader_uin))
        Library.clear_screen(cls)
        str_status = 'всіх читачів' if reader_status == 0 else 'читачів, що мають на руках книги' if reader_status > 0 else 'читачів, що не мають на руках книг'
        count_len = len(str(len(self.list_book)))
        total_len = 2 + max_num + 3 + max_name + 16 + count_len + 2
        print(self.get_table_head(f'перелік {str_status}', total_len, True))
        # ----- Для випадку коли треба повернути перелік uin виведених читачів ----- #
        showed_readers = {}
        # ----- Нічого не робимо, якщо книг немає -----
        if not self.list_reader:
            print(f'У бібліотеки немає читачів{self.pt_ln}{"-" * (total_len)}')
            return showed_readers if ret_showed else None
        # ----- Вивод переліку -----
        reader_pos = 0
        for reader in self.list_reader:
            count = self.get_reader_books(reader.uin, 'count')
            if reader_status == 0:
                succ = True
            else:
                succ = count == 0 if reader_status < 0 else count > 0
            if succ:
                reader_pos += 1
                if ret_showed:
                    showed_readers[str(reader_pos)] = reader.uin
                print(f'| {reader_pos:>{max_num}} | {reader.name:<{max_name}} | {reader.birthday:<{10}} | {count:{count_len}} |')
        if reader_pos == 0:
            if reader_status == 0: str_status = 'читачів'
            print(f'{str_status} немає'.capitalize())
        print(f'{"-" * (total_len)}')
        if ret_showed:
            return showed_readers

    # ---------------------------------------------------------------------------------------------------------------- #
    def get_reader_books(self, reader_uin: int, ret_type:str):
        """
        Метод шукає в переліку книг ті, що видані користувачу з вказаним reader_uin

        :param reader_uin: Унікальний номер цільового читача
        :param ret_type: Тип результату, що поверне функція: (
                         "count" - поверне кількість книг
                         "list_uin" - поверне перелік uin книг, які видані користовачу
                         "list_book" - поверне перелік об'єктів книг, які видані користовачу
        :return:
        """

        if ret_type not in ('count', 'list_uin','list_book'):
            return
        reader_books = []
        count = 0
        for book in self.list_book:
            if book.reader_uin == reader_uin:
                if ret_type == 'count':
                    count += 1
                elif ret_type == 'list_uin':
                    reader_books.append(book.uin)
                else:
                    reader_books.append(book)
        if ret_type == 'count':
            return count
        else:
            return reader_books

    # ---------------------------------------------------------------------------------------------------------------- #
    def before_exit(self):
        """
        Метод перед завершенням роботи пропонує зберегти змінені переліки книг та читачів

        :return: Нічого не вертає
        """
        Library.clear_screen()
        print(self.get_table_head('завершення роботи бібліотеки', self.head_len, True))
        if not self._booklist_saved:
            value = input('База даних книг не збережена. Для її збереження ведіть що небудь: ')
            if tls.check_value(value):
                self.save_list_book()
        if not self._readerlist_saved:
            value = input('База даних читачів не збережена. Для її збереження ведіть що небудь: ')
            if tls.check_value(value):
                self.save_list_reader()
        self.show_resume_action('Бібліотека зачинена')

    # ---------------------------------------------------------------------------------------------------------------- #
    def sort_list_book(self):
        """
         Метод забезпечує вибір параметру та напрямку сортування переліку книг, сортування за вивід результату

        :return: Нічого не вертає
        """

        if self.list_book:
            # ----- Вибір категорії сортування ----- #
            menu = {'1': 'За назвою (згідно абетки)',
                    '2': 'За назвою (довжина)',
                    '3': 'За автором (згідно абетки)',
                    '4': 'За автором (довжина)',
                    '5': 'За роком публікації',
                    '6': 'За послідовністю введення в базу',
                    '7': 'За номером читача',
            }
            sort_categoty = self.select_menu(title='сортування переліку книг',menu=menu,question='Оберіть категорію сортування')
            if sort_categoty is None:
                self.show_resume_action('Категорія сортування обрана не коректно. Сортування не можливе.')
                return
            # ----- Вибір напрямку сортування ----- #
            menu = {'1': 'За наростанням',
                    '2': 'За зменшенням'
                    }
            sort_reverse = self.select_menu(menu=menu, question='Оберіть напрямок сортування')
            if sort_reverse is None:
                self.show_resume_action('Напрямок сортування обраний не коректно. Сортування не можливе.')
                return
            sort_reverse = sort_reverse == '2'
            # ----- Сортування ----- #
            if sort_categoty == '1':
                self.list_book.sort(key=lambda x: x.title, reverse=sort_reverse)
            elif sort_categoty == '2':
                self.list_book.sort(key=lambda x: len(x.title), reverse=sort_reverse)
            elif sort_categoty == '3':
                self.list_book.sort(key=lambda x: x.author, reverse=sort_reverse)
            elif sort_categoty == '4':
                self.list_book.sort(key=lambda x: len(x.author), reverse=sort_reverse)
            elif sort_categoty == '5':
                self.list_book.sort(key=lambda x: x.publishing_year, reverse=sort_reverse)
            elif sort_categoty == '6':
                self.list_book.sort(key=lambda x: x.uin, reverse=sort_reverse)
            else:
                self.list_book.sort(key=lambda x: x.reader_uin, reverse=sort_reverse)
            self.show_resume_action('Перелік книг відсортований')
            self._booklist_saved = False
            value = input('Для вивода переліку всіх книг введіть що небудь: ').strip()
            if value:
                self.show_book_list(0)
            self.show_resume_action('Сортування завершено.')
        else:
            self.show_resume_action('База даних книг бібліотеки порожня. Сортування не можливе.')


    def sort_list_readers(self):
        """
        Метод забезпечує вибір параметру та напрямку сортування переліку читачів, сортування за вивід результату

        :return: Нічого не вертає
        """
        if self.list_reader:
            # ----- Вибір категорії сортування ----- #
            menu = {'1': 'За іменем (згідно абетки)',
                    '2': 'За іменем (довжина)',
                    '3': 'За віком',
                    '4': 'За послідовністю введення в базу',
                    '5': 'За кількістю книг на руках',
                    }
            sort_categoty = self.select_menu(title='сортування переліку читачів', menu=menu, question='Оберіть категорію сортування')
            if sort_categoty is None:
                self.show_resume_action('Категорія сортування обрана не коректно. Сортування не можливе.')
                return
            # ----- Вибір напрямку сортування ----- #
            menu = {'1': 'За наростанням',
                    '2': 'За зменшенням'
                    }
            sort_reverse = self.select_menu(menu=menu, question='Оберіть напрямок сортування')
            if sort_reverse is None:
                self.show_resume_action('Напрямок сортування обраний не коректно. Сортування не можливе.')
                return
            sort_reverse = sort_reverse == '2'
            # ----- Сортування ----- #
            if sort_categoty == '1':
                self.list_reader.sort(key=lambda x: x.name, reverse=sort_reverse)
            elif sort_categoty == '2':
                self.list_reader.sort(key=lambda x: len(x.name), reverse=sort_reverse)
            elif sort_categoty == '3':
                self.list_reader.sort(key=lambda x: int(str(datetime.now() - datetime.strptime(x.birthday,'%d.%m.%Y')).split(' ')[0]), reverse=not sort_reverse)
            elif sort_categoty == '4':
                self.list_reader.sort(key=lambda x: x.uin, reverse=sort_reverse)
            else :
                self.list_reader.sort(key=lambda x: self.get_reader_books(x.uin,'count'), reverse=sort_reverse)
            self.show_resume_action('Перелік читачів відсортований')
            self._readerlist_saved = False
            value = input('Для вивода переліку всіх читачів введіть що небудь: ').strip()
            if value:
                self.show_reader_list(0)
            self.show_resume_action('Сортування завершено.')
        else:
            self.show_resume_action('База даних читачів бібліотеки порожня. Сортування не можливе.')