from socket import socket

"""
Реализуем короткую версию протокола - размер пакета и сам пакет
так называемый header
Колличество байт под размер - мы определяем сами
"""
default_header_size = 10
default_pack_size = 5    # Стандартній размер 4096
default_encoding = '866'

msg_1 = 'hello'
msg_2 = 'hellohellohellohellohello'

# print(f'{len(msg_1):{default_pack_size}}')
# print(f'{len(msg_2):{default_pack_size}}')

# ----------------------------------------------------------------------------------------------------------------------
def safely_send(conn:socket, data: bytes, prompt: str) -> ():
    try:
        return conn.send(data)
    except Exception as ex:
        print(f'Точка {prompt}. Помилка сокета: {ex}')
        return 0
        
# ----------------------------------------------------------------------------------------------------------------------
def send_msg(msg: bytes, conn: socket, header_size:int = default_header_size) -> bool:
    # Определяем размер сообщения, готовим заголовок
    msg_size = f'{len(msg):{header_size}}'
    # Отправляем заголовок
    if safely_send(conn, msg_size.encode(default_encoding), 's1') != header_size:
        print(f'ERROR: can\'t send size message')
        return False
        # Отправляем cooбщение
    if safely_send(conn, msg, 's2') !=len(msg):
        print(f'ERROR: can\'t send message')
        return False
    return True

# ----------------------------------------------------------------------------------------------------------------------
def safelly_recv(conn: socket, h_size: int, prompt: str) -> bytes:
    try:
        return conn.recv(h_size)
    except Exception as ex:
        print(f'Точка {prompt}. Помилка сокета: {ex}')
        return b''

# ----------------------------------------------------------------------------------------------------------------------
def recv_msg(conn: socket,
             header_size:int = default_header_size,
             size_pack: int = default_pack_size):
    # Читаем заголовок
    # data = conn.recv(header_size)
    data = safelly_recv(conn, header_size, 'r1')
    # Проверяем что там
    if not data or len(data) != header_size:
        print(f'ERROR: can\'t read size message')
        return False

    size_msg = int(data.decode(default_encoding))

    # Дальше будем читать большое сообщение по 5 байт
    msg = b''

    while True:
        if size_msg <= size_pack:
            # pack = conn.recv(size_msg)
            pack = safelly_recv(conn, size_msg, 'r2')
            if not pack:
                return False
            msg += pack
            break

        pack = safelly_recv(conn, size_pack, 'r3')
        if not pack:
            return False
        size_msg -= size_pack
        msg += pack

    return msg