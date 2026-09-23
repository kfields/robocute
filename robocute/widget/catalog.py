
#from crunge.engine.widget import Widget
from crunge.engine.ui.flex import Row, Column

from ..catalog import Catalog

class CatalogWidget(Row):
    def __init__(self, children, catalog: Catalog):
        super().__init__(children=children)
        self.catalog = catalog

    def get_page(self, page_name):
        return self.catalog.get_page(page_name)

    def get_next_page(self, page_name):
        return self.catalog.get_next_page(page_name)

    def get_prev_page(self, page_name):
        return self.catalog.get_prev_page(page_name)
