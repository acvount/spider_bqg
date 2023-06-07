from util.color_log import Log
from util.mysql import Database
from util.request import Request
from util.mongo import Mongo
from util.snow import IdWorker
from bs4 import BeautifulSoup
from multiprocessing.dummy import Pool

class BookDetailAndChapter:

    class XiangShuBookDetail:
        category_cache = {
            '玄幻小说':1,
            '修真小说':2,
            '都市小说':3,
            '穿越小说':4,
            '网游小说':5,
            '科幻小说':6,
        }
        book_domain = 'https://www.ibiquges.com'
        def get_book_detail_from_bs_object(self,bs_object):
            main_info = bs_object.select_one("div[class='box_con']")
            return {
                'auther':main_info.select_one('div[id="info"] p:nth-child(1)').text.split('：')[1],
                'pic_url':main_info.select_one('div[id="fmimg"] img')['src'],
                'category':self.category_cache[main_info.select_one('div[class="con_top"] a:nth-child(3)').text],
                'last_update_chapter_name':main_info.select_one('div[id="info"] p:nth-child(4) a').text,
                'update_time':main_info.select_one('div[id="info"] p:nth-child(3)').text.split('：')[1],
                'status':1,
            }

        def get_chapter_list_from_bs_object(self,bs_object):
            id_work = IdWorker(10,10)
            chapters = bs_object.select("div[id='list'] dl dd a")
            return [{
                'id': id_work.get_id(),
                'name': item.text,
                'url': self.book_domain + item['href'],
                'state': 0,
            } for item in chapters]

    def __init__(self):
        self.log = Log()
        self.request = Request()

    def generate_book_detail_data(self, book):
        content = self.request.get_request(book['source_url']).text
        chapters = self.XiangShuBookDetail().get_chapter_list_from_bs_object(BeautifulSoup(content, 'html.parser'))
        mongo = Mongo(host='localhost', port=27017, username='admin', password='admin', db_name='bookstore')
        mongo.insert_many('chapter_nav', chapters)
        db_client = Database(db='bookstore', user='root', pwd='123456', host='localhost')
        detail = self.XiangShuBookDetail().get_book_detail_from_bs_object(BeautifulSoup(content, 'html.parser'))
        db_client.execute_update_by_column_value('book', detail, {'id': book['id']})
    def fetch_book_detail_by_book(self):
        db_client = Database(db='bookstore', user='root', pwd='123456', host='localhost')
        books = db_client.execute_query('SELECT * FROM book where status = 0')
        pool = Pool(30)
        pool.map(self.generate_book_detail_data, books)

if __name__ == '__main__':
    book_manager = BookDetailAndChapter()
    book_manager.fetch_book_detail_by_book()
