from util.color_log import Log
from util.request import Request
from util.mysql import Database
from bs4 import BeautifulSoup
from multiprocessing.dummy import Pool

class Category:

    class XiangShuCategory:

        def get_list_from_bs_object(self, bs_object):
            categories = bs_object.select("div[class='nav'] a")
            categories = categories[2:-2]
            return [{
                'pid': 0,
                'level': 1,
                'name': item.text,
            } for item in categories]

    def __init__(self):
        self.log = Log()
        self.request = Request()

    def generate_category_data(self, source):
        content = self.request.get_request(source['home']).text
        type_mapping = {
            1: self.XiangShuCategory().get_list_from_bs_object
        }
        category_list = type_mapping[source['type']](BeautifulSoup(content, 'html.parser'))

        db_client = Database(db='bookstore', user='root', pwd='123456', host='localhost')
        for category in category_list:
            db_client.execute_insert_by_index_column_not_repeat('category', category, 'name')

    def fetch_categories_by_urls(self):
        db_client = Database(db='bookstore', user='root', pwd='123456', host='localhost')
        sources = db_client.execute_query('SELECT * FROM source')
        Pool(3).map(self.generate_category_data, sources)


if __name__ == '__main__':
    category_manager = Category()
    category_manager.fetch_categories_by_urls()
