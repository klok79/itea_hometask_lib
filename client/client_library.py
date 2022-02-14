import socket, time, json
from ITEA_socket_utils import msg_utils as su
from os import system

class Client_library:
    # ---------------------------------------------------------- #
    def __init__(self, ip: str, port: int):
        """
        Клас взаємодії людини з бібліотекою.
        :param ip:
        :param port:
        """
        self.ip = ip
        self.ok = '!@#--ok--#@!'
        self.fail = '!@#--fail--#@!'
        self.port = port
        self.pt_ln = '\n'
        # self.head_len = 65
        self.sock = socket.socket()     # При разриві - хрен знає що робити
        self.connect_socket()


    # ---------------------------------------------------------------------------------------------------------------- #
    def connect_socket(self, remake: bool = False, attempts: int = 20) -> bool:
        if remake:
            self.sock.close()
            self.sock = socket.socket()
        pass_num = 0
        while True:
            try:
                pass_num += 1
                if pass_num > attempts:
                    print(f"Сервер не відповідає. ")
                    self.sock = None
                    break
                print(f"Спроба {pass_num} з'єднання з сервером: ")
                self.sock.connect((self.ip, self.port))
                print("З'єднання з сервером встановлено")
                return True
            except ConnectionRefusedError as ex:
                print(ex)
                time.sleep(1)
        return False
    # ---------------------------------------------------------------------------------------------------------------- #
    def decode_msg(self, msg: bytes, encoding: str = su.default_encoding):
        """
        Метод декодує та перехоплює помилки декодування повідомлення, отримане з сокета
        :param msg: Повідомлення, отримане із сокета
        :param encoding: Кодування, що було застосоване при відправці повідомлення сервером
        :return: Строку, якщо декодування успішне, або None
        """
        try:
            return msg.decode(encoding)
        except Exception as ex:
            print(f'Помилка при декодуванні повідомлення:{self.pt_ln}{ex}')


    # ---------------------------------------------------------------------------------------------------------------- #
    def loads_json(self, msg: str):
        """
        Метод перетворює текст в json та перехоплює помилки перетворення тексту
        :param msg: Декодований текст повідомлення, отриманого з сокету
        :return: Об'єкт (словник), що передавався сокетом
        """
        try:
            return json.loads(msg)
        except Exception as ex:
            print(f'Помилка при відновленні словника JSON:{self.pt_ln}{ex}')

    # ---------------------------------------------------------------------------------------------------------------- #
    @staticmethod
    def get_dict_value(msg_dict: dict, key: str):
        """
        Метод корректно поверне значення словника по ключу, навіть якщо переданий не словник та відсутній ключ
        :param msg_dict: словник, що отриманий з сокета
        :param key: параметричний ключ ('title', 'dict' або 'input')
        :return: Кортеж(Значення відповідного ключа, ознака успішності)
        """
        try:
            if key in msg_dict:
                return msg_dict[key], True
            else:
                print(f'Ключ {key} відсутній в словнику [{msg_dict}]')
        except Exception as ex:
            print(f'Помилка [{ex}] словника  [{msg_dict}]')
        return None, False


    # ---------------------------------------------------------------------------------------------------------------- #
    def main_loop(self):
        if self.sock is None:
            print("З'єднання із сервером відсутнє. Продовження не можливе")
            return
        # В циклі клієнт завжди очікує надходження повідомлення. Повідомлення завжди містить словник з однаковими полями
        while True:
            msg = su.recv_msg(self.sock)        # Тут воно має висіти постійно
            if not msg:
                print("Кажись сервер закрив з'єднання. Пробуємо перепідключитися")
                if not self.connect_socket(True, 2):
                    break
            msg = self.decode_msg(msg)
            if msg is None: continue        # ??? Велике питання
            # Декодовано без помилок
            data = self.loads_json(msg)
            if data is None: continue       # ??? Велике питання
            # ----- Отримали словник з даними без помилок ----- #
            succes = [0, 0, 0, 0, 0, 0]
            s_title, succes[0] = Client_library.get_dict_value(data,'title')
            b_cls, succes[1] = Client_library.get_dict_value(data, 'cls')
            b_input, succes[2] = Client_library.get_dict_value(data, 'input')
            s_question, succes[3] = Client_library.get_dict_value(data, 'question')
            l_list, succes[4] = Client_library.get_dict_value(data, 'l_list')
            exit, succes[5] = Client_library.get_dict_value(data, 'exit')
            if False not in succes:
                # ----- 1. Опціональна очистка консолі ----- #
                if b_cls: system('cls')
                # ----- 2. Опціональний вивід першого повідомлення ----- #
                if s_title: print(s_title)
                # ----- 3. Опціональний вивід переліку рядків----- #
                if l_list:
                    for line in l_list:
                        print(line)
                # ----- 5. Опціональне очікування вводу від користувача ----- #
                value = self.ok
                if b_input:
                    value = input(s_question)
                    # Якщо дані не уточнювалися - вертаємо ознаку
                    if not s_question: value = self.ok
            else:
                value = self.fail
            data = json.dumps(value).encode(su.default_encoding)
            succ = su.send_msg(data, self.sock)
            if exit: break
            if not succ:
                if not self.connect_socket(True, 2):
                    break








