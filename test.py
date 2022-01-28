from lib_utils.storage_fts import FileTabsStorage
from lib_utils.book import Book
from lib_utils.reader import Reader
# from library import Library
#
# lb = Library()
# obj = FileTabsStorage(lb.pt_tab, lb._void_value)
# result = obj.load_books(lb._booklist_file_name)
# for i in result:
#     print(i)

book_list = []
# book_list.append(Book(1,'one','oauthor',200,-1))
# book_list.append(Book(2,'two','tauthor',201,0))
# book_list.append(Book(3,'three','thauthor',202,1))
# book_list.append(Book(4,'four','fauthor',203,2))
# book_list.append(Book(5,'five','fiauthor',204,3))


# connector = FileTabsStorage('\t','\n', '-----')
# dict_list = connector.fetch_dict_list(book_list, Book)
# for x in dict_list:
#     print(x)

# def func1(lst1: list, lst2: list, *args):
#     print(lst1)
#     print(lst2)
#     print(args)
#
#
#
# func1([1,2],['popa', 'dopa', 'ah'])

from abc import ABC, abstractmethod
from lib_utils.storage_ex import StorageEx
#
# # ----------------------------------------------------------------------------------------------------------------------
@abstractmethod
class AbsParent(ABC):
    """
    Опис класа батька
    """
    @abstractmethod
    def func1(self, a, b):
        pass

    @abstractmethod
    def func2(self, c, d, e):
        pass
#
# # ----------------------------------------------------------------------------------------------------------------------

class Dother(AbsParent, StorageEx):
    """
    Опис класа доці
    """
    def __init__(self, lst1, lst2, *args):
        """
        Ініт класа доці

        :param arg1: аргумент 1 класа доці
        :param arg2: аргумент 2 класа доці
        :param args: аргумент 3 класа доці
        """
        StorageEx.__init__(self, lst1, lst2)
        # super(StorageEx, self).__init__()
        self.args = args

    def job(self, name):
        # print(self.__class__.__name__)
        a = StorageEx.get_source(self, name)
        print(a)

    def func1(self, a, b):
        print('func1')

    def func2(self, a, b, c):
        print('func2')



s = Dother(['nm1', 'nm2'], ['sr3', 'sr4'], 'sr5', 'ar6')
s.job('nm2')
print(s.class_names)
print(s.sources)




