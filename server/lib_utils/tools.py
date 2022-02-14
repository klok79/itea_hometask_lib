from datetime import datetime


class LibTools:
    # ---------------------------------------------------------------------------------------------------------------- #
    @staticmethod
    def check_uin(uin: str, only_positive: bool = True):
        """
        Метод перевіряє коректність uin (число, але не нуль).  Застосовується після зчитування даних з файлу

        :param uin: Унікальний номер книги/читача, що підлягає перевірці.
        :param only_positive: Ознака того, що очікуються тільки додатні значення номеру
        :return: Введене число, якщо воно відповідає умовам, або None
        """
        if uin is None:
            return
        uin = uin.strip()
        try:
            uin = int(uin)
        except ValueError:
            uin = 0
        if only_positive:
            return uin if uin > 0 else None
        else:
            return None if uin == 0 else uin

    # ---------------------------------------------------------------------------------------------------------------- #
    @staticmethod
    def check_pulish_year(publish_year: str, max_year: int = None, min_year: int = 0):
        """
        Метод перевіряє корректність введеного року публікації.
        Застосовується після функції input / зчитування даних з файлу

        :param publish_year: Рік, що підлягає перевірці.
        :param max_year: Максимально коректний рік. По замовчанню - поточний
        :param min_year: Мінімально коректний рік. По замовчанню - нульовий
        :return: Введене число, якщо воно відповідає умовам, або None
        """
        if publish_year is None:
            return
        publish_year = publish_year.strip()
        if publish_year.isdigit():
            publish_year = int(publish_year)
            if max_year is None:
                max_year = datetime.now().year
            if (publish_year > min_year) and (publish_year <= max_year):
                return publish_year

    # ---------------------------------------------------------------------------------------------------------------- #
    @staticmethod
    def check_value(value: str):
        """
         Метод перевіряє, чи value містить якісь дані. Застосовується після функції input

        :param value: текстове значення, що підлягає перевірці.
        :return: Введене значення без ведучих та ведених пробілів, якщо воно є, або None
        """
        if value is None:
            return
        value = value.strip()
        return value if value != '' else None

    # ---------------------------------------------------------------------------------------------------------------- #
    @staticmethod
    def check_date_str(s_date: str):
        """
        Метод перевіряє коректність введеної текстом дати. Застосовується після функції input

        :param s_date: Текстова дата, що підлягає перевірці
        :return: Введене значення дати переформатоване через крапку, якщо воно є, або None
        """
        if s_date is None:
            return
        d_arr = s_date.split('.')
        if len(d_arr) != 3:
            d_arr = s_date.split('/')
            if len(d_arr) != 3:
                return None
        day, month, year = d_arr
        try:
            dt = datetime(int(year), int(month), int(day))
            return dt.strftime('%d.%m.%Y')
        except ValueError:
            return None

    # ---------------------------------------------------------------------------------------------------------------- #
    @staticmethod
    def is_void_record(uin: int, fields: list, void_value: str) -> bool:
        """
        Метод перевіряє, чи є запис, зчитаний з файлу порожнім. Коректний порожній запис у файлі реєстру книг та
        читачів мічтить коректне uin, а всі решта полів заповнені порожній значенням (тут порожнє значення це: "-----")
        Використовується методами load_list_book_from_file та load_list_reader_from_file
        :param uin: Унікальний номер, що перевіряється
        :param fields: Перелік всіх полів крім uin окремого запису зчитаного з файлу
        :param void_value: Константа, що означає порожнє значення.
        :return: Ознаку того, чи є запис порожнім
        """
        succ = False
        if uin:
            for i in range(1, len(fields)):
                succ = fields[i] == void_value
                if not succ:
                    break
        return succ
