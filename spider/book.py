from util.color_log import Log
from util.request import Request
from util.mysql import Database
from bs4 import BeautifulSoup
from multiprocessing.dummy import Pool

class Book:

    class XiangShuBook:

        def get_list_from_bs_object(self,bs_object):
            books = bs_object.select("div[class='novellist'] ul li a")
            return [{
                'name': item.text,
                'source_id': 1,
                'source_url': item['href'],
                'create_date':'2020-01-01 00:00:00'
            } for item in books]

    def __init__(self):
        self.log = Log()
        self.request = Request()

    def generate_book_list_data(self, source):
        content = self.request.get_request(source['home']).text
        type_mapping = {
            1: self.XiangShuBook().get_list_from_bs_object
        }
        books = type_mapping[source['type']](BeautifulSoup(content, 'html.parser'))
        db_client = Database(db='bookstore', user='root', pwd='123456', host='localhost')
        for book in books:
            db_client.execute_insert_by_index_column_not_repeat('book', book, 'name','source_url')

    def fetch_books_by_source(self):
        db_client = Database(db='bookstore', user='root', pwd='123456', host='localhost')
        sources = db_client.execute_query('SELECT * FROM source')
        Pool(3).map(self.generate_book_list_data, sources)

if __name__ == '__main__':
    book_manager = Book()
    book_manager.fetch_books_by_source()