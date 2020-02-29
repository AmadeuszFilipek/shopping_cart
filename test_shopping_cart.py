import unittest
from shopping_cart import Checkout, promotions_database
from functools import wraps

class TestShoppingCart(unittest.TestCase):

   promotions = promotions_database.values()
   
   def test_single_item(self):
      checkout = Checkout()
      checkout.scan('001')
      total = checkout.total
      expected = 9.25

      self.assertEqual(total, expected)

   def test_single_item(self):
      checkout = Checkout()
      checkout.scan('002')
      total = checkout.total
      expected = 45.00

      self.assertEqual(total, expected)

   def test_single_item(self):
      checkout = Checkout()
      checkout.scan('003')
      total = checkout.total
      expected = 19.95

      self.assertEqual(total, expected)

   def test_cart_01(self):
      checkout = Checkout(self.promotions)
      scan_codes = ['001', '002', '003']
      for code in scan_codes:
         checkout.scan(code)
      total = checkout.total
      expected = 66.78

      self.assertEqual(total, expected)

   def test_cart_02(self):
      checkout = Checkout(self.promotions)
      scan_codes = ['001', '003', '001']
      for code in scan_codes:
         checkout.scan(code)
      total = checkout.total
      expected = 36.95

      self.assertEqual(total, expected)

   def test_cart_03(self):
      checkout = Checkout(self.promotions)
      scan_codes = ['001', '002', '001', '003']
      for code in scan_codes:
         checkout.scan(code)
      total = round(checkout.total, 2)
      expected = 73.75

      self.assertEqual(total, expected)

if __name__ == "__main__":
   unittest.main()

