from profile_decorator import profile
import random
import collections

random.seed(20)


def create_products(num):
    """Create a list of random products with 3-letter alphanumeric name."""
    return [''.join(random.choices('ABCDEFG123', k=3)) for _ in range(num)]

def sort_counter(counter_dict):
    return {k: v for k, v in sorted(counter_dict.items(),
                                    key=lambda x: x[1],
                                    reverse=True)}

# version3
@profile(sort_by='cumulative', lines_to_print=10, strip_dirs=True)
def product_counter_v3(products):
    """Get count of products in descending order."""
    return collections.Counter(products)


if __name__ == '__main__':
    num = 1_000_000  # assume we have sold 1,000,000 products
    products = create_products(num)
    counter_dict1 = product_counter_v3(products)  
