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


x = {
    '1': 58,
    '2': 55
}

for i, j in x.items():
    print(i, j)
