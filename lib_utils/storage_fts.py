"""
Клас реалізує збереження переліків книг та читачів у текстових файлах UTF-8 в форматі: Один рядок на книгу/читача
Дані в рядку відділяються символами табуляції в заданій послідовності
"""
from lib_utils.storage_abs import Storage
from lib_utils.tools import LibTools as tls


class FileTabsStorage(Storage):

    def __init__(self, pt_tab: str, pt_ln, void_value: str):
        """
        Конструктору необхідно передати базові константи з класу бібліотеки

        :param pt_tab: Символ табуляції, яким розділені поля даних в рядку
        :param pt_ln: Символ переносу рядка
        :param void_value: Значення, яке вважається порожнім в полях книги
        """
        self.pt_tab = pt_tab
        self.pt_ln = pt_ln
        self.void_value = void_value

    # ------------------------------------------------------------------------------------------------------------------
    @staticmethod
    def get_data_flag(class_name: str) -> bool:
        """
        Метод перевіряє на коректність класс об'єкту даних (Book, Reader).
        Якщо об'єкт іншого класу - генерується помилка AttributeError

        :param class_name: назва классу об'єкту даних
        :return: True якщо class_name - Book, False якщо class_name - Reader.
        """
        if class_name not in ('Reader', 'Book'):
            raise AttributeError(f'Класс {class_name.__name__} не допустимий')
        return class_name == 'Book'

    # ------------------------------------------------------------------------------------------------------------------
    def fetch_objects_list(self, list_dict: list, info_list: list, obj_class) -> list:
        """
        Метод перетворює отриманий з файлу перелік словників з даними книг або читачів в перелік цільових об'єктів.
        Має викликатися посля метода load.

        :param list_dict: Перелік зі словниками атрибутів книги або читача
        :param info_list: Перелік повідомлень, що були згенеровані методом load зчитування даних з файлів
        :param obj_class: Класс цільового об'єкту.
        :return: Перелік цільових об'єктів (книг або читачів).
        """

        fetch_as_book = FileTabsStorage.get_data_flag(obj_class.__name__)
        result_list = []
        if list_dict:
            for x in list_dict:
                if fetch_as_book:
                    result_list.append(obj_class(x['uin'], x['title'], x['author'], x['publishing_year'], x['reader_uin']))
                else:
                    result_list.append(obj_class(x['uin'], x['name'], x['birthday']))
        if info_list:
            for info in info_list:
                print(info)
            if len(info_list) > 1:
                input('Натисніть що небудь для продовження: ')
        return result_list

    # ------------------------------------------------------------------------------------------------------------------
    def fetch_dict_list(self, obj_list: list, obj_max_uin: int, obj_class) -> list:
        """
        Метод перетворює перелік об'єктів класу Book або Readers в перелік словників з відповідними полями.
        Має викликатися перед методом dump

        :param obj_list: Перелік об'єктів класу Book або Readers
        :param obj_class: класс об'єктів, що знаходяться в словнику
        :param max_uin: максимальний унікальний номер об'єкту цільового класу
        :return: Перелік словників, готовий для запису
        """
        fetch_as_book = FileTabsStorage.get_data_flag(obj_class.__name__)
        max_uin = 0
        result_list =[]
        for x in obj_list:
            if fetch_as_book:
                result_list.append({"uin": x.uin, "title": x.title, "author": x.author,
                                  "publishing_year": x.publishing_year, "reader_uin": x.reader_uin})
            else:
                result_list.append({"uin": x.uin, "name": x.name, "birthday": x.birthday})
            max_uin = x.uin if x.uin > max_uin else max_uin
        # Якщо серед існуючих записів немає останнього, колись існуючого номера - додаємо цей номер в порожньому заисі
        if max_uin < obj_max_uin:
            if fetch_as_book:
                result_list.append({"uin": obj_max_uin, "title": self.void_value, "author": self.void_value,
                                    "publishing_year": self.void_value, "reader_uin": self.void_value})
            else:
                result_list.append({"uin": self.void_value, "name": self.void_value, "birthday": self.void_value})
        return result_list

    # ------------------------------------------------------------------------------------------------------------------
    def load(self, file_path: str, obj_class) -> tuple:
        """
        Метод намагається зчитати весь перелік книг або читачів з текстового файлу модулі проекту.
        Перевіряє коректність даних. Не коректні записи ігноруються.

        :param file_path: Шлях до файлу з даними книг або читачів
        :param obj_class: Клас об'єктів, що очікується зчитати
        :return: Кортеж із 3-х значень:
                  0.) перелік (list) зі словниками, в яких в якості ключів - поля цільвого об'єкту:
                  для книги "uin", "title", "author", "publishing_year", "reader_uin"
                  для читача "uin", "name", "birthday". А значення - зчитані.
                  2.) перелік (list) повідомлень
                  3.) число. максимальний uin переліку книг або читачів, який необхідно передати бібліотеці
        """
        # --------------------------------------------------------------------------
        def push_err_str(err_str: str, prompt: str, err_count: int):
            """
            Допоміжний метод нарощування тексту помилки. Вставляє кому перед не першою помилкою та нарощує текст помилки
            .Також збільшує лічильник помилок в записі

            :param err_str: Результуючий текст, що нарощується
            :param prompt:  Текст, що буде доданий до результуючого тексту
            :param err_count: Кількість частин нарощування (кількість помилок)
            :return: Текст err_str з доданим до нього через кому текстом prompt.
            """
            if err_count > 0:
                err_str = err_str + ','
            return f'{err_str} {prompt}', err_count + 1
        # --------------------------------------------------------------------------

        as_book = FileTabsStorage.get_data_flag(obj_class.__name__)
        info_list = []
        result_list = []
        max_uin = 0
        try:
            with open(file_path, 'rb') as file:
                lines = file.read().decode('UTF-8')
        except FileNotFoundError:
            info_list.append(f'Файл {file_path} не знайдений в пакеті')
            return result_list, info_list, max_uin
        # ----- Розбір зчитаних даних ----- #
        err_count = 0
        if lines:
            recs_count = 0
            rec_list = lines.splitlines()
            succ_count = 0
            for rec in rec_list:
                if rec == '':
                    continue
                recs_count += 1
                fields = rec.split(self.pt_tab)
                # ----- Контроль полів ----- #
                if len(fields) == 5 if as_book else 3:
                    uin = tls.check_uin(fields[0])
                    title_or_name = tls.check_value(fields[1])
                    author_or_birthday, publish_year, reader_uin = None, None, None
                    if as_book:
                        author_or_birthday = tls.check_value(fields[2])
                        publish_year = tls.check_pulish_year(fields[3])
                        reader_uin = tls.check_uin(fields[4], False)
                    else:
                        author_or_birthday = tls.check_date_str(fields[2])
                    void_rec = tls.is_void_record(uin, fields, self.void_value)
                    if as_book:
                        succ = False not in (uin, title_or_name, author_or_birthday, publish_year, reader_uin)
                    else:
                        succ = False not in (uin, title_or_name, author_or_birthday)
                    succ = succ or void_rec
                    # ---- Аналізуємо зчитані поля -----
                    if succ:
                        if void_rec:
                            max_uin = uin
                        else:
                            # ---- Розпізнаємо помилку для повідомлення -----
                            err_start = err_count
                            err_str = f'Запис {recs_count} в файлі {file_path} містить пошкоджене'
                            if uin == False:
                                err_str, err_count = push_err_str(err_str, f' поле [uin] [{fields[0]}]', err_count)
                            if title_or_name == False:
                                err_str, err_count = push_err_str(err_str, f' поле [{"title" if as_book else "name"}] [{fields[1]}]', err_count)
                            if author_or_birthday == False:
                                err_str, err_count = push_err_str(err_str, f' поле [{"author" if as_book else "birthday"}] [{fields[2]}]', err_count)
                            if as_book:
                                if publish_year == False:
                                    err_str, err_count = push_err_str(err_str, f' поле [publish_year] [{fields[3]}]', err_count)
                                if reader_uin == False:
                                    err_str, err_count = push_err_str(err_str, f' поле [reader_uin] [{fields[4]}]', err_count)
                            if err_start < err_count:
                                info_list.append(err_str)
                                continue
                    if uin > max_uin:
                        max_uin = uin
                    if not void_rec:
                        if as_book:
                            x_dict = {"uin": uin, "title": title_or_name, "author": author_or_birthday, "publishing_year": publish_year, "reader_uin": reader_uin}
                        else:
                            x_dict = {"uin":uin, "name": title_or_name, "birthday": author_or_birthday}
                        result_list.append(x_dict)
                        succ_count += 1
                else:
                    info_list.append(f'Пошкоджений запис [{recs_count}][{rec}] ігнорується')
            s_err = f'Дані всіх {"книг" if as_book else "читачів"} успішно зчитані з файлу' if succ_count == recs_count else f'Зчитано {succ_count} записів з {recs_count}'
            info_list.append(s_err)
        return result_list, info_list, max_uin

    # ------------------------------------------------------------------------------------------------------------------
    def dump(self, file_path: str, list_dict: list, obj_class):
        """
        Метод записує весь перелік книг або читачів в текстовий файл у модулі проекту

        :param file_path: Шлях до файлу з даними книг або читачів
        :param list_dict: Перелік (list) зі словниками, в яких в якості ключів - поля цільвого об'єкту:
                  для книги "uin", "title", "author", "publishing_year", "reader_uin"
                  для читача "uin", "name", "birthday". З відповідними значеннями
        :param obj_class: Клас об'єктів, що записуються
        :return: Ознаку успішності запису.
        """

        fetch_as_book = FileTabsStorage.get_data_flag(obj_class.__name__)
        succ = False
        lines = []
        for book in list_dict:
            if fetch_as_book:
                record = f'{book["uin"]}{self.pt_tab}{book["title"]}{self.pt_tab}{book["author"]}{self.pt_tab}{book["publishing_year"]}{self.pt_tab}{book["reader_uin"]}{self.pt_ln}'
            else:
                record = f'{book["uin"]}{self.pt_tab}{book["name"]}{self.pt_tab}{book["birthday"]}{self.pt_ln}'
            lines.append(record.encode('UTF-8'))
        try:
            with open(file_path, 'wb') as file:
                file.writelines(lines)
                print(f'Збереження бази даних {"книг" if fetch_as_book else "читачів"} у файл успішне')
                succ = True
                return True
        except Exception as ex:
            print(f'Не вдалося відкрити файл {file_path} для запису. ' +
                             f'Якщо він відкритий іншою програмою - закрийте її та повторіть. {self.pt_ln}{ex}')
        return succ