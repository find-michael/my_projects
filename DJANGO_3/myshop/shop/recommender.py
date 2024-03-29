import redis
from django.conf import settings
from .models import Product


# Nawiązanie połączenia z bazą danych Redis
r = redis.Redis(host = settings.REDIS_HOST, port = settings.REDIS_PORT, db = settings.REDIS_DB)

class Recommender(object):

    def get_product_key(self, id):
        return 'product:{}:purchased_with'.format(id)

    def products_bought(self, products):
        product_ids = [p.id for p in products]
        for product_id in product_ids:
            for with_id in product_ids:
                # Pobranie innych produktów kupionych razem z analizowanymi
                if product_id != with_id:
                    # Inkrementacja punktacji dla produktu kupionego razem z analizowanym
                    r.zincrby(self.get_product_key(product_id), amount=1, value=with_id)

    def suggest_products_for(self, products, max_results=6):
        product_ids = [p.id for p in products]

        if len(products) == 1:
            # Jeżeli jest tylko jeden produkt
            suggestions = r.zrange(self.get_product_key(product_ids[0]), 0, -1, desc=True)[:max_results]
        else:
            # Wygenerowanie klucza podstawowego
            flat_ids = ''.join([str(id) for id in product_ids])
            temp_key = 'tmp_{}'.format(flat_ids)
            # Wiele produktów, sumowanie punktów wszystkich produktów,
            # umieszczenie w kluczu tymczasowym posortowanej kolekcji wynikowej
            keys = [self.get_product_key(id) for id in product_ids]
            r.zunionstore(temp_key, keys)
            # Usunięcie identyfikatorów produktów, dla których przygotowujemy rekomendacje
            r.zrem(temp_key, *product_ids)
            # Pobranie identyfikatorów produktów wedłóg ich punktacji, w kolejności malejącej
            suggestions = r.zrange(temp_key, 0, -1, desc=True)[:max_results]
            # Usunięcie klucza podstawowego
            r.delete(temp_key)

        suggested_product_ids = [int(id) for id in suggestions]
        # Pobranie sugerowanych produktów i ułożenie ich w kolejności pojawienia się
        suggested_products = list(Product.objects.filter(id__in=suggested_product_ids))
        suggested_products.sort(key=lambda x: suggested_product_ids.index(x.id))
        return suggested_products

    def clear_purchases(self):
        for id in Product.objects.values_list('id', flat=True):
            r.delete(self.get_product_key(id))