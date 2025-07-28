from .models import Category, Product


class ProductService:

    @staticmethod
    def get_products_by_category(category: Category):
        # В задании сказано вернуть список продуктов в указанной категории, а не QuerySet
        # return [product for product in Product.objects.filter(category=category)] - первый вариант
        return [product for product in category.products.all()]
