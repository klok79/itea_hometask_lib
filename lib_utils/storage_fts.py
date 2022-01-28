"""
Клас реалізує збереження переліків книг та читачів у текстових файлах UTF-8 в форматі: Один рядок на книгу/читача
Дані в рядку відділяються символами табуляції в заданій послідовності
"""
from lib_utils.storage_abs import StorageAbs
from lib_utils.storage_ex import StorageEx
from lib_utils.tools import LibTools as tls
from lib_utils.book import Book
from lib_utils.reader import Reader


class FileTabsStorage(StorageAbs, StorageEx):

    def __init__(self, list_classnames: list, list_paths: list, tab: str, new_ln: str, void_value: str):
        """
        Класс коннектора для збереження даних книг та читачів в текстових файлах у форматі один рядок - один запис,
        Значення відділяються символами табуляції, поля визначаються їх позицією в рядку.

        :param list_classnames: Перелік назв класів об'єктів, запис/зчитування яких підтримується
        :param list_paths: Перелік шляхів до файлів даних відповідних класів
        :param tab: Символ табуляції, яким розділені поля даних в рядку
        :param new_ln: Символ переносу рядка
        :param void_value: Значення, яке вважається порожнім в полях книги (використовується для максимального номера)
        """
        StorageEx.__init__(self, list_classnames, list_paths)
        self.pt_tab = tab
        self.pt_ln = new_ln
        self.void_value = void_value

    # ------------------------------------------------------------------------------------------------------------------
    def load(self, obj_classname: str) -> tuple:
        """
        Метод намагається зчитати весь перелік книг або читачів з текстового файлу модулі проекту.
        Перевіряє коректність даних. Не коректні записи ігноруються.

        :param obj_classname: Назва класу об'єктів, що очікується зчитати
        :return: Кортеж із 2-х значень:
                  0.) перелік (list) цільових об'єктів.
                  1.) число. максимальний uin цільових об'єктів, який необхідно передати бібліотеці
        """
        # --------------------------------------------------------------------------
        def push_err_str(text: str, prompt: str, count: int) -> tuple:
            """
            Допоміжний метод нарощування тексту помилки. Вставляє кому перед не першою помилкою та нарощує текст помилки
            .Також збільшує лічильник помилок в записі

            :param text: Результуючий текст, що нарощується
            :param prompt:  Текст, що буде доданий до результуючого тексту
            :param count: Кількість частин нарощування (кількість помилок)
            :return: Текст err_str з доданим до нього через кому текстом prompt.
            """
            if count > 0:
                text = text + ','
            return f'{text} {prompt}', count + 1
        # --------------------------------------------------------------------------
        self.set_mode(obj_classname)
        file_path = self.get_source(obj_classname)
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
                succ = (self.book_mode and len(fields) == 5) or (self.reader_mode and len(fields) == 3)
                if succ:
                    uin = tls.check_uin(fields[0])
                    title_or_name = tls.check_value(fields[1])
                    author_or_birthday, publish_year, reader_uin = None, None, None
                    if self.book_mode:
                        author_or_birthday = tls.check_value(fields[2])
                        publish_year = tls.check_pulish_year(fields[3])
                        reader_uin = tls.check_uin(fields[4], False)
                    elif self.reader_mode:
                        author_or_birthday = tls.check_date_str(fields[2])
                    void_rec = tls.is_void_record(uin, fields, self.void_value)
                    # ------------------------
                    if self.book_mode:
                        succ = False not in (uin, title_or_name, author_or_birthday, publish_year, reader_uin)
                    elif self.reader_mode:
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
                                s_target = "title" if self.book_mode else "name" if self.reader_mode else ''
                                err_str, err_count = push_err_str(err_str, f' поле [{s_target}] [{fields[1]}]', err_count)
                            if author_or_birthday == False:
                                s_target = "author" if self.book_mode else "birthday" if self.reader_mode else ''
                                err_str, err_count = push_err_str(err_str, f' поле [{s_target}] [{fields[2]}]', err_count)
                            if self.book_mode:
                                if publish_year == False:
                                    err_str, err_count = push_err_str(err_str, f' поле [year] [{fields[3]}]', err_count)
                                if reader_uin == False:
                                    err_str, err_count = push_err_str(err_str, f' поле [reader_uin] [{fields[4]}]', err_count)
                            if err_start < err_count:
                                info_list.append(err_str)
                                continue
                    if uin > max_uin:
                        max_uin = uin
                    if not void_rec:
                        x_obj = None
                        if self.book_mode:
                            x_obj = Book(uin, title_or_name, author_or_birthday, publish_year, reader_uin)
                        elif self.reader_mode:
                            x_obj = Reader(uin, title_or_name, author_or_birthday)
                        result_list.append(x_obj)
                        succ_count += 1
                else:
                    info_list.append(f'Пошкоджений запис [{recs_count}][{rec}] ігнорується')
            # --------------------------------------------------
            s_target = "книг" if self.book_mode else "читачів" if self.reader_mode else ''
            s_err = f'Дані всіх {s_target} успішно зчитані з файлу' if succ_count == recs_count else f'Зчитано {succ_count} записів з {recs_count}'
            info_list.append(s_err)
        #----------------------------------------------
        if info_list:
            for info in info_list:
                print(info)
            if len(info_list) > 1:
                input('Натисніть що небудь для продовження: ')
        return result_list, max_uin

    # ------------------------------------------------------------------------------------------------------------------
    def dump(self, list_obj: list, obj_classname: str) -> bool:
        """
        Метод записує весь перелік книг або читачів в текстовий файл у модулі проекту

        :param list_obj: перелік (list) цільових об'єктів, що підлягають запису.
        :param obj_classname: Назва класу об'єктів, що записуються
        :return: Ознаку успішності запису.
        """

        self.set_mode(obj_classname)
        file_path = self.get_source(obj_classname)
        succ = False
        lines = []
        for obj in list_obj:
            record = None
            if self.book_mode:
                record = f'{obj.get_uin}{self.pt_tab}{obj.get_title()}{self.pt_tab}{obj.get_author()}{self.pt_tab}{obj.get_year()}{self.pt_tab}{obj.get_reader_uin()}{self.pt_ln}'
            elif self.reader_mode:
                record = f'{obj.get_uin()}{self.pt_tab}{obj.get_name()}{self.pt_tab}{obj.get_birthday()}{self.pt_ln}'
            lines.append(record.encode('UTF-8'))
        try:
            with open(file_path, 'wb') as file:
                file.writelines(lines)
                s_target = "книг" if self.book_mode else "читачів" if self.reader_mode else ''
                print(f'Збереження бази даних {s_target} у файл успішне')
                succ = True
                return True
        except Exception as ex:
            print(f'Не вдалося відкрити файл {file_path} для запису. ' +
                             f'Якщо він відкритий іншою програмою - закрийте її та повторіть. {self.pt_ln}{ex}')
        return succ