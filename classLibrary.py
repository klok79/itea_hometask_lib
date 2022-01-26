# 1. Класс библиотека
# Поля:
# - +список книг (list Book)
# - +список читателей (list People)
# Методы:
# - + Добавить книгу
# - + Удалить книгу
# - Отдать книгу читателю
# - Принять книгу от читателя
# - +Вывести список всех книг
# - +Вывести список книг в библиотеке (в наличии)
# - +Вывести списк книг, которые не в наличии
# - Отсортировать список книг по названию, автору, году издания (lambda будет плюсом)


from classBook import Book
from classPeople import People
from os import system
from datetime import datetime


class Library:
    # --------------------------------------------------------- #
    def __init__(self):
        self._booklist_file_name = 'book_list.txt'
        self._peoplelist_file_name = 'people_list.txt'
        self._void_value = '-' * 5
        self.max_book_id = 0
        self.max_reader_id = 0
        self.head_len = 65
        self.pt_tab = '\t'
        self.pt_ln = '\n'
        self.list_book = self.load_list_book_from_file()
        self.list_people = self.load_list_reader_from_file()
        self._booklist_saved = True
        self._peoplelist_saved = True

    @staticmethod
    # --------------------------- Метод формує красиву шапочку для таблиці / меню ------------------------------------ #
    def get_table_head(head, size, upper=False):
        if upper:
            head = head.upper()
        len_head = len(head)
        if size < (len_head + 4):
            size = len_head + 4
        left = (size - len_head) // 2 - 1
        right = size - len_head - left - 2
        return f'{"=" * left} {head} {"=" * right}'

    # ------------------------------- Метод умовної очистки консолі -------------------------------------------------- #
    @staticmethod
    def clear_screen(condition=True):
        if condition:
            system('cls')

    # ---------------------- Метод виводить результат відпрацювання пункта меню. Скорочує запис кода ----------------- #
    def show_resume_action(self, prompt, bottom_len=None):
        if bottom_len is None:
            bottom_len = self.head_len
        print(f'{self.pt_ln}{prompt}{self.pt_ln}{"-" * bottom_len}')

    # ---------------------------------------- Метод перевіряє, чи введені дані -------------------------------------- #
    @staticmethod
    def check_value(value):
        value = value.strip()
        if value != '':
            return value
        return False

    # --------------------------- Метод перевіряє коректність дати та вертає її текстом ------------------------------ #
    @staticmethod
    def check_date_str(s_date):
        d_arr = s_date.split('.')
        if len(d_arr) != 3:
            d_arr = s_date.split('/')
            if len(d_arr) != 3:
                return False
        day, month, year = d_arr
        try:
            dt = datetime(int(year), int(month), int(day))
            return dt.strftime('%d.%m.%Y')
        except ValueError:
            return False

    # ----------------------------- Метод перевіряє коректність id (число, але не нуль) ------------------------------ #
    @staticmethod
    def check_id(id, only_positive=True):
        id = id.strip()
        try:
            id = int(id)
        except ValueError:
            id = 0
        if only_positive:
            return id if id > 0 else False
        else:
            return False if id == 0 else id

    # --------------------- Метод перевіряє корректність введеного року пуюлікації та вертає його -------------------- #
    @staticmethod
    def check_pulish_year(publish_year, max_year=None, min_year=0):
        publish_year = publish_year.strip()
        if publish_year.isdigit():
            publish_year = int(publish_year)
            if max_year is None:
                max_year = datetime.now().year
            if (publish_year > min_year) and (publish_year <= max_year):
                return publish_year
        return False

    # --------------------------- Метод вертає позицію книги з заданим id в переліку книг  --------------------------- #
    def get_bookpos_by_id(self, id):
        pos = 0
        for book in self.list_book:
            if book.id == id:
                return pos
            pos += 1


    # ------------------------- Метод вертає позицію читача з заданим id в переліку читачів  ------------------------- #
    def get_readerpos_by_id(self, id):
        pos = 0
        for reader in self.list_people:
            if reader.id == id:
                return pos
            pos += 1


    # --------------------- Метод нарощування тексту помилки в методах завантаження з файлів ------------------------- #
    def _push_load_error_info(self, err_str, prompt, err_count):
        """ використовується методами load_list_book_from_file та load_list_people_from_file. Вставляє кому перед не
        першою помилкою та нарощує текст помилки. Також збільшує лічильник помилок в записі"""
        if err_count > 0:
            err_str = err_str + ','
        return f'{err_str} {prompt}', err_count + 1


    # ----------- Метод перевіряє, чи є запис, зчитаний з файлу порожнім (містить тільки max_id) --------------------- #
    def _is_void_record(self, id, fields):
        """Використовується методами load_list_book_from_file та load_list_people_from_file  """
        succ = False
        if id:
            for i in range(1, len(fields)):
                succ = fields[i] == self._void_value
                if not succ:
                    break
        return succ


    # --------------------- Метод виводить словник, очікує вводу ключа словника, вертаж ключ або None ---------------- #
    def select_menu(self, title = None, menu_width = None, cls = True, menu = None, question = 'Оберіть пункт меню'):
        Library.clear_screen(cls)
        if menu_width is None:
            menu_width = self.head_len
        if title is not None:
            print(self.get_table_head(f'{title}', menu_width, False))
        if type(menu) == type({}):
            count = 0
            for key in menu:
                if len(key) > count: count = len(key)
            for key, value in menu.items():
                print(f'{key:>{count}}. {value}')
            if menu_width > 0:
                print('-' * menu_width)
            value = input(f'{question}: ')
            if value in menu:
                return value


    # ----------- Метод диспетчер головного циклу. Виводить меню, очікує вводу та перенеаправляє потік --------------- #
    def main_loop(self):
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
            '12': 'Вивести перелік всіх книг без виєбонів',
            '0': 'Завершити роботу'
        }
        menu_function = [
            self.before_exit,                   # + Завершити роботу
            self.add_book,                      # + Додати книгу в бібліотеку
            self.delete_book,                   # + Видалити книгу з бібліотеки (Видалити можна тільки наявні в бібліотеці книги)
            self.add_reader,                    # + Зареєструвати читача
            self.delete_reader,                 # + Видалити читача (Видалити можна тільки тих читачів, у яких немає книг на руках)
            self.give_out_book_to_reader,       # + Видати книгу читачу
            self.accept_book_from_reader,       # + Прийняти книгу від читача
            self.show_book_list,                # + Вивести перелік книг
            self.show_reader_list,              # + Вивести перелік читачів
            self.sort_list_book,                # + Відсортувати перелік книг
            self.sort_list_readers,             # + Відсортувати перелік користувачів
            self.file_job                      # + Зберегти / Завантажити
        ]
        while True:
            value = self.select_menu(title='ГОЛОВНЕ МЕНЮ БІБЛІОТЕКИ', menu=main_menu, question='Введіть номер дії, яку необхідно зробити')
            if value is not None:
                menu_function[int(value)]()
                if value == '0':
                    break
                else:
                    print('Натисніть Enter для продовження')
                    input()

    # --------- Метод очікує вводу, перевіряє введені значення, створює та додає екземпляр книги в перелік книг ------ #
    def add_book(self):
        Library.clear_screen()
        print(self.get_table_head('Додавання нової книги в бібліотеку', self.head_len, True))
        value = input('Введіть повністю наву книги: ')
        title = Library.check_value(value)
        if not title:
            self.show_resume_action('Назва книги не введена. Книга не додана.')
            return
        value = input("Введіть автора книги: ")
        author = Library.check_value(value)
        if not author:
            self.show_resume_action('Автор не введений. Книга не додана.')
            return
        value = input("Введіть рік публікації книги:")
        publ_year = Library.check_pulish_year(value)
        if not publ_year:
            s_err = 'не введений' if value == "" else  f'[{value}] введений не корректно'
            self.show_resume_action(f'Рік публікації {s_err}. Книга не додана.')
            return
        self.max_book_id += 1
        self.list_book.append(Book(self.max_book_id, title, author, publ_year,  -1))
        self.show_resume_action(f'Книга "{self.list_book[len(self.list_book) - 1]}" додана в бібліотеку')
        self._booklist_saved = False


    # ------ Метод очікує вводу, перевіряє введені значення, створює та додає екземпляр читача в перелік читачів ----- #
    def add_reader(self):
        Library.clear_screen()
        print(self.get_table_head('Реєстрація нового читача в бібліотеці', self.head_len, True))
        value = input("Введіть повне ім'я читача (ПІБ, титул, тощо): ")
        reader = Library.check_value(value)
        if not reader:
            self.show_resume_action("Ім'я читача не введене. Реєстрація відхилена.")
            return
        value = input("Введіть дату народження читача:")
        birthday = Library.check_date_str(value)
        if not birthday:
            s_err = 'не введена' if value == '' else f'{value} введена не коректно'
            self.show_resume_action(f'Дата дня народження {s_err}. Реєстрація відхилена.')
            return
        self.max_reader_id += 1
        self.list_people.append(People(self.max_reader_id, reader, birthday))
        self.show_resume_action(f'Новий користувач  "{self.list_people[len(self.list_people) - 1]}" зареєстрований')
        self._peoplelist_saved = False


    # -------------- Метод виводить перелік не виданих книг, очікує вводу номера та видаляє вказану книгу ---------- #
    def delete_book(self):
        """Видалити можна тільки книги, що знаходяться в бібліотеці"""
        Library.clear_screen()
        print(self.get_table_head('Видалення книги з бібліотеки', self.head_len, True))
        if len(self.list_book) > 0:
            showed_books = self.show_book_list(-1, False, True)
            print('Видаленню підлягають тільки ті книги, які знаходяться в бібліотеці (не видані читачам на руки)')
            value = input('Введіть номер книги, яку необхідно видалити з бібліотеки: ').strip()
            if value in showed_books:
                book_pos = self.get_bookpos_by_id(showed_books[value])
                del_book = str(self.list_book[book_pos])
                self.list_book.pop(book_pos)
                self.show_resume_action(f'Книга [{del_book}] видалена з бібліотеки')
                self._booklist_saved = False
            else:
                self.show_resume_action('Видалення книги відхилене')
        else:
            self.show_resume_action('В бібліотеці немає книг')


    # --------- Метод виводить перелік не читачів не боржників, очікує вводу номера та видаляє вказаного читача ------ #
    def delete_reader(self):
        Library.clear_screen()
        print(self.get_table_head('Видалення читача з бібліотеки', self.head_len, True))
        if len(self.list_people) > 0:
            showed_readers = self.show_reader_list(-1, False, True)
            print('Видаленню підлягають тільки ті читачі, які не мають на руках жодної книги')
            value = input('Введіть номер читача, якого необхідно видалити з бібліотеки: ').strip()
            if value in showed_readers:
                reader_pos = self.get_readerpos_by_id(showed_readers[value])
                del_reader = str(self.list_people[reader_pos])
                self.list_people.pop(reader_pos)
                self.show_resume_action(f'Читач [{del_reader}] видалений з бібліотеки')
                self._peoplelist_saved = False
            else:
                self.show_resume_action('Видалення читача відхилене')
        else:
            self.show_resume_action('У бібліотеки немає зареєстрованих читачів')


    # ----------------------------------- Метод реалізує опцію меню роботи з файлами---------------------------------- #
    def file_job(self):
        menu = {
            '1': 'Зберегти перелік книг у файл',
            '2': 'Завантажити перелік книг з файлу',
            '3': 'Зберегти перелік читачів у файл',
            '4': 'Завантажити перелік читачів з файлу'
        }
        value = self.select_menu(title='РОБОТА З ФАЙЛАМИ ДАНИХ', menu=menu, question='Оберіть необхідну дію')
        if value is not None:
            file_methods = [self.save_list_book_to_file,
                            self.load_list_book_from_file,
                            self.save_list_reader_to_file,
                            self.load_list_reader_from_file]
            file_methods[int(value) - 1]()
            self.show_resume_action('Файлова операція закінчена')
        else:
            self.show_resume_action('Дія не обрана. Операція відмінена')


    # ------------------ Метод зберігає весь перелік книг в текстовий файл book_list.txt в модулі проекту ------------ #
    def save_list_book_to_file(self):
        lines = []
        max_id = 0
        for book in self.list_book:
            record = f'{book.id}{self.pt_tab}{book.title}{self.pt_tab}{book.author}{self.pt_tab}' \
                     f'{book.publishing_year}{self.pt_tab}{book.reader_id}{self.pt_ln}'
            record = record.encode('UTF-8')
            lines.append(record)
            if book.id > max_id:
                max_id = book.id
        if max_id < self.max_book_id:   # -- Якщо книги були видалені з кінця переліку --
            record = f'{self.max_book_id}{self.pt_tab}{self._void_value}{self.pt_tab}{self._void_value}' \
                     f'{self.pt_tab}{self._void_value}{self.pt_tab}{self._void_value}{self.pt_ln}'
            record = record.encode('UTF-8')
            lines.append(record)
        try:
            with open(self._booklist_file_name, 'wb') as file:
                file.writelines(lines)
                print('Збереження бази даних книг у файл успішне')
                self._booklist_saved = True
                return True
        except Exception as ex:
            print(f'Не вдалося відкрити файл {self._booklist_file_name} для запису. ' +
                  f'Якщо він відкритий іншою програмою - закрийте її та повторіть. {self.pt_ln}{ex}')



    # ------------- Метод зберігає весь перелік читачів в текстовий файл people_list.txt в модулі проекту ------------ #
    def save_list_reader_to_file(self):
        lines = []
        max_id = 0
        for reader in self.list_people:
            record = f'{reader.id}{self.pt_tab}{reader.name}{self.pt_tab}{reader.birthday}{self.pt_ln}'
            record = record.encode('UTF-8')
            lines.append(record)
            if reader.id > max_id:
                max_id = reader.id
        if max_id < self.max_reader_id:  # -- Якщо читачі були видалені з кінця переліку --
            record = f'{self.max_reader_id}{self.pt_tab}{self._void_value}{self.pt_tab}{self._void_value}{self.pt_ln}'
            lines.append(record)
        try:
            with open(self._peoplelist_file_name, 'wb') as file:
                file.writelines(lines)
                print('Збереження бази даних читачів у файл успішне')
                self._peoplelist_saved = True
                return True
        except Exception as ex:
            print(f'Не вдалося відкрити файл {self._peoplelist_file_name} для запису. ' +
                f'Якщо він відкритий іншою програмою - закрийте її та повторіть. {self.pt_ln}{ex}')


    # ------------------------------Метод зчитує з файлу перелік книг ------------------------------------------------ #
    def load_list_book_from_file(self):
        """
        Метод намагається зчитати весь перелік книг з текстового файлу book_list.txt в модулі проекту
        Перевіряє коректність даних. Не коректні записи ігноруються. Встановлює max_id
        """
        try:
            with open(self._booklist_file_name, 'rb') as file:
                lines = file.read().decode('UTF-8')
        except FileNotFoundError:
            print(f'Файл {self._booklist_file_name} не знайдений в пакеті')
            lines = ''
        # ----- Розбір зчитаних даних ----- #
        max_id = 0
        book_list = []
        if lines != '':
            recs_count = 0
            rec_list = lines.split(self.pt_ln)
            succ_count = 0
            for rec in rec_list:
                if rec == '':
                    continue
                recs_count += 1
                fields = rec.split(self.pt_tab)
                if len(fields) == 5:
                    id = Library.check_id(fields[0])
                    title = Library.check_value(fields[1])
                    author = Library.check_value(fields[2])
                    publish_year = Library.check_pulish_year(fields[3])
                    reader_id = Library.check_id(fields[4], False)
                    void_rec = False
                    if False in (id, title, author, publish_year, reader_id):
                        void_rec = self._is_void_record(id, fields)
                        if void_rec:
                            max_id = id
                        else:
                            err_count = 0
                            err_str = f'Запис {recs_count} містить пошкоджене'
                            if id == False:
                                err_str, err_count = self._push_load_error_info(err_str, f' поле [id] [{fields[0]}]', err_count)
                            if title == False:
                                err_str, err_count = self._push_load_error_info(err_str, f' поле [title] [{fields[1]}]', err_count)
                            if author == False:
                                err_str, err_count = self._push_load_error_info(err_str, f' поле [author] [{fields[2]}]', err_count)
                            if publish_year == False:
                                err_str, err_count = self._push_load_error_info(err_str, f' поле [publish_year] [{fields[3]}]', err_count)
                            if reader_id == False:
                                err_str, err_count = self._push_load_error_info(err_str, f' поле [reader_id] [{fields[4]}]', err_count)
                            print(err_str)
                            continue
                    if id > max_id: max_id = id
                    if not void_rec:
                        book_list.append(Book(id, title, author, publish_year, reader_id))
                        succ_count += 1
                else:
                    print(f'Пошкоджений запис [{recs_count}][{rec}] ігнорується' )
            s_err = 'Дані всіх книг успішно зчитані з файлу' if succ_count == recs_count else f'Зчитано {succ_count} записів з {recs_count}'
            print(s_err)
            self.max_book_id = max_id
            if book_list:
                self._booklist_saved = True
        return book_list


    # ----------------------------------------- Метод зчитує з файлу перелік читачів --------------------------------- #
    def load_list_reader_from_file(self):
        """
        Метод намагається зчитати весь перелік читачів з текстового файлу people_list.txt в модулі проекту
        Перевіряє коректність даних. Не коректні записи ігноруються. Встановлює max_id"""

        try:
            with open(self._peoplelist_file_name, 'rb') as file:
                lines = file.read().decode('UTF-8')
        except FileNotFoundError:
            print(f'Файл {self._peoplelist_file_name} не знайдений в пакеті')
            lines = ''
        # ----- Розбір зчитаних даних ----- #
        max_id = 0
        reader_list = []
        if lines != '':
            recs_count = 0
            rec_list = lines.split(self.pt_ln)
            succ_count = 0
            for rec in rec_list:
                if rec == '':
                    continue
                recs_count += 1
                fields = rec.split(self.pt_tab)
                if len(fields) == 3:
                    id = Library.check_id(fields[0])
                    name = Library.check_value(fields[1])
                    birthday = Library.check_date_str(fields[2])
                    void_rec = False
                    if False in (id, name, birthday):
                        void_rec = self._is_void_record(id, fields)
                        if void_rec:
                            max_id = id
                        else:
                            err_count = 0
                            err_str = f'Запис {recs_count} містить пошкоджене'
                            if id == False:
                                err_str, err_count = self._push_load_error_info(err_str, f' поле [id] [{fields[0]}]', err_count)
                            if name == False:
                                err_str, err_count = self._push_load_error_info(err_str, f' поле [name] [{fields[1]}]', err_count)
                            if birthday == False:
                                err_str, err_count = self._push_load_error_info(err_str, f' поле [birthday] [{fields[2]}]', err_count)
                            print(err_str)
                            continue
                    if id > max_id: max_id = id
                    if not void_rec:
                        reader_list.append(People(id, name, birthday))
                        succ_count += 1
                else:
                    print(f'Запис [{recs_count}][{rec}] пошкоджений і буде проігнорований' )
            s_err = 'Дані всіх читачів успішно зчитані з файлу' if succ_count != recs_count else f'Зчитано {succ_count} записів з {recs_count}'
            print(s_err)
            self.max_book_id = max_id
            if reader_list:
                self._peoplelist_saved = True
        return reader_list


    # -------------------------- Видати наявну в бібліотеці книгу зареєстрованому читачу ----------------------------- #
    def give_out_book_to_reader(self):
        Library.clear_screen()
        print(self.get_table_head('видача книги читачу', self.head_len, True))
        showed_books = self.show_book_list(-1, False, True)
        if showed_books:
            value = input('Оберіть книгу, яку видати читачу на руки: ')
            if value in showed_books:
                book = self.list_book[self.get_bookpos_by_id(showed_books[value])]
                showed_readers = self.show_reader_list(0, False, True)
                if showed_readers:
                    value = input('Оберіть читача, якому видається книга: ')
                    if value in showed_readers:
                        reader = self.list_people[self.get_readerpos_by_id(showed_readers[value])]
                        book.reader_id = reader.id
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


    # ----------------------------------------- Прийняти книгу від читача -------------------------------------------- #
    def accept_book_from_reader(self):
        Library.clear_screen()
        print(self.get_table_head('прийом книги від читача', self.head_len, True))
        showed_readers = self.show_reader_list(1, False, True)
        if showed_readers:
            value = input('Введіть номер читача, від якого приймається книга: ')
            if value in showed_readers:
                reader = self.list_people[self.get_readerpos_by_id(showed_readers[value])]
                reader_books = self.get_reader_books(reader.id, 'list_book')
                showed_books = self.show_book_list(0, False, True,reader_books, f'книг читача {reader}')
                value = input('Оберіть книгу, яку необхідно прийняти від читача: ')
                if value in showed_books:
                    book = reader_books[int(value) - 1]
                    book.reader_id = -1
                    print(f'Читач [{reader}] здав книгу [{book}] в бібліотеку')
                    self._booklist_saved = False
                else:
                    print('Номер книги вказаний не коректно. Прийом книги не можливий')
            else:
                print('Номер читача вказаний не коректно. Прийом книги не можливий')

        else:
            print('Відсутні читачі, які мають книги на руках. Прийом книги не можливий')


    # ---------------------------------- Метод виводить на екран таблицю з книгами:----------------------------------- #
    def show_book_list(self, book_status = None, cls = True, ret_showed = False, target_list = None, tile = ''):
        """ book_status - вказівник, що виводити:
        > 0 - Виводити книги, що видані читачам, = 0  Виводити всі зареєстровані книги, < 0 - Виводити книги, що не видані читачам
        """

        # ----- Допоміжний метод вичисляє максимальні довжини назви та автора -----
        def get_max_lens(target):
            max_author = 0
            max_title = 0
            for book in target:
                al = len(book.author)
                tl = len(book.title)
                max_author = al if al > max_author else max_author
                max_title = tl if tl > max_title else max_title
            return max_author, max_title

        # ----- Допоміжний метод додаткового вибору типу переліку -----
        def select_book_type(cls):
            menu = {
                '1': 'Виводити всі книги, що зареєстровані в бібліотеці',
                '2': 'Виводити тільки ті книги, які видані читачам',
                '3': 'Виводити тільки ті книги, що знаходяться в бібліотеці (не видані читачам) ',
            }
            value = self.select_menu(title='ВИБІР КАТЕГОРІЮ КНИГДЛЯ ВИВОДУ', menu=menu, cls=cls, question='Оберіть категорію книг')
            if value is not None:
                return 0 if value == '1' else -1 if value == '3' else 1

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
        max_num = len(str(self.max_book_id))
        Library.clear_screen(cls)
        # ------------
        if tile == '':
            str_status = 'всіх книг' if book_status == 0 else 'книг, що видані читачам' if book_status > 0 else 'книг, що знаходяться в бібліотеці'
        else:
            str_status = tile
        # ------------
        total_len = 2 + max_num + 3 + max_author + 3 + max_title + 3 + 6
        print(self.get_table_head(f'перелік {str_status}', total_len, True))
        # ----- Для випадку коли треба повернути перелік id виведених книг ----- #
        showed_books = {}
        # ----- Нічого не робимо, якщо книг немає -----
        if not target_list:
            print(f'В бібліотеці немає книг{self.pt_ln}{"-" * (total_len)}')
            return showed_books if ret_showed else None
        # ----- Вивод переліку -----
        book_pos = 0
        for book in target_list:
            succ = True if book_status == 0 else book.reader_id > 0 if book_status > 0 else book.reader_id < 0
            if succ:
                book_pos += 1
                if ret_showed:
                    showed_books[str(book_pos)] = book.id
                print(f'| {book_pos:>{max_num}} | {book.author:<{max_author}} | {book.title:<{max_title}} | {book.publishing_year:4} |')
        if book_pos == 0:
            if book_status == 0: str_status = 'книг '
            print(f'{str_status} немає'.capitalize())
        print(f'{"-" * (total_len)}')
        if ret_showed:
            return showed_books



    # ----------------------------------- Метод виводить на екран таблицю з читачами --------------------------------- #
    def show_reader_list(self, reader_status = None, cls = True, ret_showed = False):
        """ reader_status - вказівник, що виводити:
            > 0 - Виводити читачів, що мають на руках книги, = 0  Виводити всіх читачів, < 0 - Виводити читачів, що не мають книг на руках
            """

        # ----- Допоміжний метод вичисляє максимальну довжини імені читача -----
        def get_longer_name_len():
            max_name = 0
            for reader in self.list_people:
                nl = len(reader.name)
                if nl > max_name: max_name = nl
            return max_name

        # ----- Допоміжний метод додаткового вибору типу переліку -----
        def select_reader_type(cls):
            menu = {
                '1': 'Виводити всіх зареєстрованих читачів',
                '2': 'Виводити тільки тих читачів, які мають книги на руках',
                '3': 'Виводити тільки тих читачів, які не мають книг на руках',
            }
            value = self.select_menu(title='ВИБІР КАТЕГОРІї ЧИТАЧІВ ДЛЯ ВИВОДУ', cls=cls, menu=menu, question='Оберіть категорію читачів')
            if value is not None:
                return 0 if value == '1' else -1 if value == '3' else 1

        # ----- Визначаємося з типом переліку читачів -----
        if reader_status is None:
            if not self.list_people:
                reader_status = 0
            else:
                reader_status = select_reader_type(cls)
                if reader_status is None:
                    print('Категорія переліку не обрана, перелік не буде виведений')
                    return
        # ----- Вичисляємо геометрію таблиці -----
        max_name = get_longer_name_len()
        max_num = len(str(self.max_reader_id))
        Library.clear_screen(cls)
        str_status = 'всіх читачів' if reader_status == 0 else \
            'читачів, що мають на руках книги' if reader_status > 0 else 'читачів, що не мають на руках книг'
        count_len = len(str(len(self.list_book)))
        total_len = 2 + max_num + 3 + max_name + 16 + count_len + 2
        print(self.get_table_head(f'перелік {str_status}', total_len, True))
        # ----- Для випадку коли треба повернути перелік id виведених читачів ----- #
        showed_readers = {}
        # ----- Нічого не робимо, якщо книг немає -----
        if not self.list_people:
            print(f'У бібліотеки немає читачів{self.pt_ln}{"-" * (total_len)}')
            return showed_readers if ret_showed else None
        # ----- Вивод переліку -----
        reader_pos = 0
        for reader in self.list_people:
            count = self.get_reader_books(reader.id, 'count')
            if reader_status == 0:
                succ = True
            else:
                succ = count == 0 if reader_status < 0 else count > 0
            if succ:
                reader_pos += 1
                if ret_showed:
                    showed_readers[str(reader_pos)] = reader.id
                print(f'| {reader_pos:>{max_num}} | {reader.name:<{max_name}} | {reader.birthday:<{10}} | {count:{count_len}} |')
        if reader_pos == 0:
            if reader_status == 0: str_status = 'читачів'
            print(f'{str_status} немає'.capitalize())
        print(f'{"-" * (total_len)}')
        if ret_showed:
            return showed_readers


    # ------------- Метод вертає кількість або перелік id книг або перелік книг, які видані читачу reader_id --------- #
    def get_reader_books(self, reader_id, ret_type = 'count or list_id or list_book'):
        if ret_type not in ('count', 'list_id','list_book'):
            return
        reader_books = []
        count = 0
        for book in self.list_book:
            if book.reader_id == reader_id:
                if ret_type == 'count':
                    count += 1
                elif ret_type == 'list_id':
                    reader_books.append(book.id)
                else:
                    reader_books.append(book)
        if ret_type == 'count':
            return count
        else:
            return reader_books


    # ---------------- Метод перед завершенням роботи пропонує зберегти змінені переліки книг та читачів ------------- #
    def before_exit(self):
        Library.clear_screen()
        print(self.get_table_head('завершення роботи бібліотеки', self.head_len, True))
        if not self._booklist_saved:
            value = input('База даних книг не збережена. Для її збереження ведіть що небудь: ')
            if Library.check_value(value):
                self.save_list_book_to_file()
        if not self._peoplelist_saved:
            value = input('База даних читачів не збережена. Для її збереження ведіть що небудь: ')
            if Library.check_value(value):
                self.save_list_book_to_file()
        self.show_resume_action('Бібліотека зачинена' )

    # --- Метод забезпечує вибір параметру та напрямку сортування переліку книг, сортування за вивід результату ------ #
    def sort_list_book(self):
        if self.list_book:
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
            menu = {'1': 'За наростанням',
                    '2': 'За зменшенням'
                    }
            sort_reverse = self.select_menu(menu=menu, question='Оберіть напрямок сортування')
            if sort_reverse is None:
                self.show_resume_action('Напрямок сортування обраний не коректно. Сортування не можливе.')
                return
            sort_reverse = sort_reverse == '2'
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
                self.list_book.sort(key=lambda x: x.id, reverse=sort_reverse)
            else:
                self.list_book.sort(key=lambda x: x.reader_id, reverse=sort_reverse)
            self.show_resume_action('Перелік книг відсортований')
            self._booklist_saved = False
            value = input('Для вивода переліку всіх книг введіть що небудь: ').strip()
            if value:
                self.show_book_list(0)
            self.show_resume_action('Сортування завершено.')
        else:
            self.show_resume_action('База даних книг бібліотеки порожня. Сортування не можливе.')


    # --- Метод забезпечує вибір параметру та напрямку сортування переліку читачів, сортування за вивід результату ------ #
    def sort_list_readers(self):
        if self.list_people:
            menu = {'1': 'За іменем (згідно абетки)',
                    '2': 'За іменем (довжина)',
                    '3': 'За віком',
                    '4': 'За послідовністю введення в базу',
                    '5': 'За кількістю книг на руках',
            }
            sort_categoty = self.select_menu(title='сортування переліку читачів',menu=menu,question='Оберіть категорію сортування')
            if sort_categoty is None:
                self.show_resume_action('Категорія сортування обрана не коректно. Сортування не можливе.')
                return
            menu = {'1': 'За наростанням',
                    '2': 'За зменшенням'
                    }
            sort_reverse = self.select_menu(menu=menu, question='Оберіть напрямок сортування')
            if sort_reverse is None:
                self.show_resume_action('Напрямок сортування обраний не коректно. Сортування не можливе.')
                return
            sort_reverse = sort_reverse == '2'
            if sort_categoty == '1':
                self.list_people.sort(key=lambda x: x.name, reverse=sort_reverse)
            elif sort_categoty == '2':
                self.list_people.sort(key=lambda x: len(x.name), reverse=sort_reverse)
            elif sort_categoty == '3':
                self.list_people.sort(key=lambda x:int(str(datetime.now() - datetime.strptime(x.birthday,'%d.%m.%Y')).split(' ')[0]), reverse=not sort_reverse)
            elif sort_categoty == '4':
                self.list_people.sort(key=lambda x: x.id, reverse=sort_reverse)
            else :
                self.list_people.sort(key=lambda x: self.get_reader_books(x.id,'count'), reverse=sort_reverse)
            self.show_resume_action('Перелік читачів відсортований')
            self._peoplelist_saved = False
            value = input('Для вивода переліку всіх читачів введіть що небудь: ').strip()
            if value:
                self.show_reader_list(0)
            self.show_resume_action('Сортування завершено.')
        else:
            self.show_resume_action('База даних читачів бібліотеки порожня. Сортування не можливе.')
