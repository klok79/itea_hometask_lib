import time
from concurrent.futures import ThreadPoolExecutor

class Single_thread:
    """
    Чтобы запихнуть в submit ThreadPoolExecutor класс, как выяснилось, ннужно
    у этого класса переопределить метод __call__ в который нужно запихнуть ту функцию,
    которую мы передавали в качестве параметра, submit.
    Но так как при использовании класса - параметры сохраняются прямо в классе, то и передаются
    они теперь не в сам submit, а в класс, при его создании. Сам класс создается так в момент
    вызова submit.
    """
    def __init__(self, num: int, count: int):
        self.num = num
        self.count = count
        print(f'{self.__class__.__name__} {num} created')

    def __call__(self, *args, **kwargs):
        for i in range(self.count):
            print(f'{self.__class__.__name__} {self.num} run {i+1} pass from {self.count}')
            time.sleep(1)
        print(f'{self.__class__.__name__} {self.num} finished')


with ThreadPoolExecutor(max_workers=5) as ex:
    """
    Создаем класс с параметрами класса прямо при вызове submit.
    """
    ex.submit(Single_thread(1, 7))
    ex.submit(Single_thread(2, 8))
    ex.submit(Single_thread(3, 3))

