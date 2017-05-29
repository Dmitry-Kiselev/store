from haystack import indexes

from catalogue.models import Product


class ProductIndex(indexes.SearchIndex, indexes.Indexable):
    # Search text
    text = indexes.CharField(
        document=True, use_template=True,
        template_name='search/indexes/item_text.txt')

    name = indexes.CharField()
    product_category = indexes.CharField()
    description = indexes.CharField()
    price = indexes.IntegerField()

    def get_model(self):
        return Product

    def index_queryset(self, using=None):
        return self.get_model().objects.order_by('-updated_at')
