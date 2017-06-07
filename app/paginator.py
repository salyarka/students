from math import ceil


class Paginator:
    """
    Implements pagination.
    """

    def __init__(self, page, per_page, total_count):
        self.page = page
        self.per_page = per_page
        self.total_count = total_count

    @property
    def pages(self):
        return int(ceil(self.total_count / float(self.per_page)))

    @property
    def previous(self):
        return self.page if self.page == 1 else self.page - 1

    @property
    def next(self):
        return self.page + 1

    @property
    def has_previous(self):
        return self.page > 1

    @property
    def has_next(self):
        return self.page < self.pages
