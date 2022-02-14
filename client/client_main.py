"""
Модуль существует тольео для создание экземпляра класса клиента библиотеки и запуск
его цикла ожидания. Примерный план "что делать" написан в аналогичном модуле
server_main.py серверного проекта
"""

from client_library import Client_library
console = Client_library('localhost', 5555)
console.main_loop()
