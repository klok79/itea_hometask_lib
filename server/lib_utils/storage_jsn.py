"""
Клас реалізує збереження переліків книг та читачів у файлах JSON в форматі: Один рядок на книгу/читача
Дані в рядку в форматі JSON у вигляді словника
"""
from lib_utils.storage_abs import StorageAbs
from lib_utils.storage_ex import StorageEx
from lib_utils.tools import LibTools as tls
from lib_utils.book import Book
from lib_utils.reader import Reader
import json


class FileJsonStorage(StorageAbs, StorageEx):

    def __init__(self, list_classnames: list, list_paths: list, new_ln: str, void_value: str):
        """
        Класс коннектора для збереження даних книг та читачів в текстових файлах у форматі один рядок - один запис,
        Значення відділяються символами табуляції, поля визначаються їх позицією в рядку.

        :param list_classnames: Перелік назв класів об'єктів, запис/зчитування яких підтримується
        :param list_paths: Перелік шляхів до файлів даних відповідних класів
        :param new_ln: Символ переносу рядка
        :param void_value: Значення, яке вважається порожнім в полях книги (використовується для максимального номера)
        """
        StorageEx.__init__(self, list_classnames, list_paths)
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
        def get_dict_value(x_dict: dict, key: str, to_str: bool = True):
            if key in x_dict.keys():
                if to_str:
                    return str(x_dict[key])
                else:
                    return x_dict[key]



        # --------------------------------------------------------------------------
        self.set_mode(obj_classname)
        file_path = self.get_source(obj_classname)

        info_list, result_list, max_uin, succ_count, recs_count, err_count = [], [], 0, 0, 0, 0
        # --------------------------------------------------------------------------------------------------------------
        try:
            with open(file_path, 'r') as f:
                for rec in f:
                    recs_count += 1
                    try:
                        obj_dict = json.loads(rec)
                    except Exception as ex:
                        info_list.append(f'Пошкоджений запис [{recs_count}][{rec}] ігнорується{self.pt_ln}{ex}')
                        err_count += 1
                        continue
                    # -------------------- Тепер треба перевірити словник -------------------------------
                    if self.book_mode:
                        fields = [get_dict_value(obj_dict, 'uin'),
                                  get_dict_value(obj_dict, 'title'),
                                  get_dict_value(obj_dict, 'author'),
                                  get_dict_value(obj_dict, 'year'),
                                  get_dict_value(obj_dict, 'reader_uin')
                                  ]
                    elif self.reader_mode:
                        fields = [get_dict_value(obj_dict, 'uin'),
                                  get_dict_value(obj_dict, 'name'),
                                  get_dict_value(obj_dict, 'birthday'),
                                  ]
                    # ----------------------------------------------------------------------------------
                    uin = tls.check_uin(fields[0])
                    title_or_name = tls.check_value(fields[1])
                    author_or_birthday, publish_year, reader_uin = None, None, None
                    if self.book_mode:
                        author_or_birthday = tls.check_value(fields[2])
                        publish_year = tls.check_pulish_year(fields[3])
                        reader_uin = tls.check_uin(fields[4], False)
                    elif self.reader_mode:
                        author_or_birthday = tls.check_date_str(fields[2])
                    # ----- Визначення ознаки корректності зчинаних даних для всіх класів ---------
                    if self.book_mode:
                        succ = None not in (uin, title_or_name, author_or_birthday, publish_year, reader_uin)
                    elif self.reader_mode:
                        succ = None not in (uin, title_or_name, author_or_birthday)
                    # -----------------------------------------------------------------------------
                    if succ:
                        # ----- Якщо всі дані коректні - додаємо запис в перелік обєктів -----
                        x_obj = None
                        if uin > max_uin:
                            max_uin = uin
                        if self.book_mode:
                            x_obj = Book(uin, title_or_name, author_or_birthday, publish_year, reader_uin)
                        elif self.reader_mode:
                            x_obj = Reader(uin, title_or_name, author_or_birthday)
                        result_list.append(x_obj)
                        succ_count += 1
                    else:
                        # ----- Якщо деякі дані не коректні -----
                        if tls.is_void_record(uin, fields, self.void_value):
                            # ----- Якщо некоректність викликана порожнім записом -----
                            max_uin = uin
                            succ_count += 1
                        else:
                            # ---- Якщо зчитані не коретні значення -----
                            err_start = err_count
                            err_str = f'Запис {recs_count} в файлі {file_path} містить пошкоджене'
                            if uin is None:
                                err_str, err_count = push_err_str(err_str, f' поле [uin] [{fields[0]}]', err_count)
                            if title_or_name is None:
                                s_target = "title" if self.book_mode else "name" if self.reader_mode else ''
                                err_str, err_count = push_err_str(err_str, f' поле [{s_target}] [{fields[1]}]',
                                                                  err_count)
                            if author_or_birthday is None:
                                s_target = "author" if self.book_mode else "birthday" if self.reader_mode else ''
                                err_str, err_count = push_err_str(err_str, f' поле [{s_target}] [{fields[2]}]',
                                                                  err_count)
                            if self.book_mode:
                                if publish_year is None:
                                    err_str, err_count = push_err_str(err_str, f' поле [year] [{fields[3]}]', err_count)
                                if reader_uin is None:
                                    err_str, err_count = push_err_str(err_str, f' поле [reader_uin] [{fields[4]}]',
                                                                      err_count)
                            if err_start < err_count:
                                info_list.append(err_str)
                                continue
                s_target = "книг" if self.book_mode else "читачів" if self.reader_mode else ''
                s_err = f'Дані всіх {s_target} успішно зчитані з файлу' if succ_count == recs_count else f'Зчитано {succ_count} записів {s_target} з {recs_count}'
                info_list.append(s_err)
        #----------------------------------------------
        except FileNotFoundError:
            info_list.append(f'Файл {file_path} не знайдений в пакеті')
            return result_list, max_uin

        # self.show_messages(info_list, err_count > 0)
        self.show_messages(info_list, False)
        # if info_list:
        #     for info in info_list:
        #         print(info)
        #     if len(info_list) > 1:
        #         input('Натисніть що небудь для продовження: ')
        return result_list, max_uin
        # --------------------------------------------------------------------------------------------------------------









    # ------------------------------------------------------------------------------------------------------------------
    def dump(self, list_obj: list, obj_classname: str, max_uin: int = None) -> bool:
        """
        Метод записує весь перелік книг або читачів в текстовий файл у модулі проекту

        :param list_obj: перелік (list) цільових об'єктів, що підлягають запису.
        :param obj_classname: Назва класу об'єктів, що записуються
        :param max_uin: Максимальний унікальний номер об'єкту (Для збереження у файл)
        :return: Ознаку успішності запису.
        """

        self.set_mode(obj_classname)
        file_path = self.get_source(obj_classname)
        true_max_uin = 0
        succ = False
        lines = []
        # --------------------------------------------------------------------------------------------------------------
        try:
            with open(file_path, 'w') as f:
                for obj in list_obj:
                    uin = obj.get_uin()
                    if uin > true_max_uin:
                        true_max_uin = uin
                    obj_json = json.dumps(obj.get_attr_dict())
                    f.write(obj_json + self.pt_ln)
                # ----- Додаємо порожній запис з максимальним номером -----
                if max_uin is not None:
                    if max_uin > true_max_uin:
                        # !!! ОТУТ МОЖНА ВИКОРИСТАТИ МЕТОД КЛАСУ ЯКЩО ПЕРЕДАТИ НЕ НАЗВУ КЛАСУ А САМ КЛАС !!!!
                        # ХОЧА ПЕРЕЛІК ПАРАМЕТРІВ РІЗНИЙ - ТРЕБА ТАНЦЮВАТИ З БУБНОМ. ТОМУ ПОКИ ТАК
                        if self.book_mode:
                            obj_dict = Book.build_attr_dict(max_uin, self.void_value, self.void_value, self.void_value,
                                                            self.void_value)
                        elif self.reader_mode:
                            obj_dict = Reader.build_attr_dict(max_uin, self.void_value, self.void_value)
                        obj_json = json.dumps(obj_dict)
                        f.write(obj_json)
                s_target = "книг" if self.book_mode else "читачів" if self.reader_mode else ''
                print(f'Збереження бази даних {s_target} у файл успішне')
                succ = True
        except Exception as ex:
            print(f'Не вдалося відкрити файл {file_path} для запису. ' +
                  f'Якщо він відкритий іншою програмою - закрийте її та повторіть. {self.pt_ln}{ex}')
        return succ

        # --------------------------------------------------------------------------------------------------------------

        # for obj in list_obj:
        #     record = None
        #     # ----- Визначаємо існуючий максимальний номер -----
        #     x_uin = obj.get_uin()     # Метод має бути у об'єктів всіх класів, що підтримуються
        #     if x_uin > true_max_uin:
        #         true_max_uin = x_uin
        #     # ----- Створюємо запис -----
        #     if self.book_mode:
        #         record = f'{x_uin}{self.pt_tab}{obj.get_title()}{self.pt_tab}{obj.get_author()}{self.pt_tab}{obj.get_year()}{self.pt_tab}{obj.get_reader_uin()}{self.pt_ln}'
        #     elif self.reader_mode:
        #         record = f'{x_uin}{self.pt_tab}{obj.get_name()}{self.pt_tab}{obj.get_birthday()}{self.pt_ln}'
        #     lines.append(record.encode('UTF-8'))
        # # ----- Додаємо порожній запис з максимальним номером -----
        # if max_uin is not None:
        #     if max_uin > true_max_uin:
        #         record = None
        #         if self.book_mode:
        #             record = f'{max_uin}{self.pt_tab}{self.void_value}{self.pt_tab}{self.void_value}{self.pt_tab}{self.void_value}{self.pt_tab}{self.void_value}{self.pt_ln}'
        #         elif self.reader_mode:
        #             record = f'{max_uin}{self.pt_tab}{self.void_value}{self.pt_tab}{self.void_value}{self.pt_ln}'
        #         lines.append(record.encode('UTF-8'))
        # try:
        #     with open(file_path, 'wb') as file:
        #         file.writelines(lines)
        #         s_target = "книг" if self.book_mode else "читачів" if self.reader_mode else ''
        #         print(f'Збереження бази даних {s_target} у файл успішне')
        #         succ = True
        # except Exception as ex:
        #     print(f'Не вдалося відкрити файл {file_path} для запису. ' +
        #                      f'Якщо він відкритий іншою програмою - закрийте її та повторіть. {self.pt_ln}{ex}')
        # return succ
