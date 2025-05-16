import pytest


class PricingRule:
    def calculate_total(self, quantity, unit_price):
        return quantity, unit_price
    

class BulkDiscountRule(PricingRule):
    def __init__(self, bulk_quantity, bulk_discount):
        self.bulk_quantity = bulk_quantity
        self.bulk_discount = bulk_discount

    def calculate_total(self, quantity, unit_price):
        discounted_items = quantity // self.bulk_quantity
        remaining_items = quantity % self.bulk_quantity

        return (discounted_items * self.bulk_discount) + (remaining_items * unit_price)
    

class Checkout:
    def __init__(self, rules):
        self.pricing_rules = rules["pricing_rules"]
        self.unit_prices = rules["unit_prices"]
        self.items = {}

    def scan(self, item):
        if item not in self.items_price:
            raise KeyError("Item not in price list.")
        if item not in self.items:
            self.items[item] = 1
        else:
            self.items[item] += 1

    def total(self):
        total_price = 0
        for item in self.items:
            quantity = self.items[item]
            unit_price = self.unit_prices[item]

            total_price += self.pricing_rules[item].calculate_total(
                quantity=quantity, unit_price=unit_price)

        return total_price
    
    def clear(self):
        self.items = {}

    # Helper function
    def calculating_total_with_discounts(self, item_quantity, item_price, discount_quantity, discount_price):
        discounted_items = item_quantity // discount_quantity
        discounted_items_price = discounted_items * discount_price

        remaining_items = item_quantity % discount_quantity
        remaining_items_price = remaining_items * item_price

        return discounted_items_price + remaining_items_price
    
    def __repr__(self):
        return f"Checkout(items={self.items})"


class TestCheckOutPrice:
    def setup_method(self):
        self.rules = {
            "pricing_rules": {
                'A': BulkDiscountRule(bulk_quantity=3, bulk_discount=130),
                'B': BulkDiscountRule(bulk_quantity=2, bulk_discount=45),
                'C': PricingRule(),
                'D': PricingRule()
            }, 
            "unit_prices": {
                'A': 50, 
                'B': 30, 
                'C': 20, 
                'D': 15
            }
        }

    def price(self, goods):
        co = Checkout(self.rules)
        goods = list(goods)
        for good in goods:
            co.scan(good)
        return co.total()
    
    def test_totals(self):
        assert 0 == self.price("")
        assert 0 == self.price("")
        assert 50 == self.price("A")
        assert 80 == self.price("AB")
        assert 115 == self.price("CDBA")

        assert 100 == self.price("AA")
        assert 130 == self.price("AAA")
        assert 180 == self.price("AAAA")
        assert 230 == self.price("AAAAA")
        assert 260 == self.price("AAAAAA")

        assert 160 == self.price("AAAB")
        assert 175 == self.price("AAABB")
        assert 190 == self.price("AAABBD")
        assert 190 == self.price("DABABA")

    def test_incremental(self):
        co = Checkout(self.rules)
        assert 0 == co.total()
        co.scan("A")
        print(co.items)
        assert 50 == co.total()
        co.scan("B")
        print(co.items)
        assert 80 == co.total()
        co.scan("A")
        assert 130 == co.total()
        co.scan("A")
        assert 160 == co.total()
        co.scan("B")
        assert 175 == co.total()

    def test_repr(self):
        co = Checkout(self.rules)
        assert "Checkout(items={})" == repr(co)
        co.scan("A")
        co.scan("B")
        co.scan("A")
        co.scan("C")
        assert "Checkout(items={'A': 2, 'B': 1, 'C': 1})" == repr(co)

    def test_clear(self):
        co = Checkout(self.rules)
        assert 0 == co.total()
        co.scan("A")
        co.scan("B")
        co.scan("A")
        co.scan("C")
        assert 150 == co.total()
        co.clear()
        assert 0 == co.total()