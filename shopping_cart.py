# coding: utf8
import itertools as it
from collections import Counter
from datetime import date
from datetime import datetime
import math

items_database = {
   '001': {
      'name': 'Red Scarf',
      'cost': 9.25
   },
   '002': {
      'name': 'Silver cufflinks',
      'cost': 45.00
   },
   '003': {
      'name': 'Silk Dress',
      'cost': 19.95
   }
}

promotions_database = {
   1: {
      'type': 'global',
      'description': "When spending over £60, 10% off total discount",
      'threshold': 60,
      'value': 0.1,
      'item': None,
      'start-date': '2020-02-27',
      'end-date': None
   },
   2: {
      'type': 'on-item',
      'description': 'When purchasing 2 or more of the Red Scarf its price is reduced to £8.50',
      'threshold': 2,
      'value': 8.5,
      'item': '001',
      'start-date': '2020-02-27',
      'end-date': None
   }
}

class Checkout:
   
   ids = it.count()

   def __init__(self, promotions=[]):
      self.promotions = promotions
      self.id = self.ids.__next__()
      self.cart = Counter()

   def scan(self, item):
      self.cart[item] += 1

   @property
   def total(self):
      promotions = active_promotions(self.promotions)

      total = 0
      for item, times in self.cart.items():
         item_cost = items_database[item]['cost']
         
         # check discounts on items
         for promotion in on_item_promotions(promotions):
            if shall_discount(item, promotion, times):
               item_cost = promotion['value']
               break

         total += times * item_cost

      # check global discounts
      for promotion in global_promotions(promotions):
         if total >= promotion['threshold']:
            total = total - total * promotion['value']
      
      return total

def shall_discount(item, promotion, times):
   if promotion['item'] != item: 
      return False

   if promotion['threshold'] <= times:
      return True

def is_promotion_active(promotion):
   today = datetime.today()
   start_date = promotion['start-date']
   start_date = datetime.strptime(start_date, "%Y-%m-%d")

   end_date = promotion['end-date']
   if end_date is not None:
      end_date = datetime.strptime(end_date, "%Y-%m-%d")
      return (start_date <= today) and (today <= end_date)
   else:
      return (start_date <= today)

def active_promotions(promotions):
   valid_promotions = filter(lambda p: is_promotion_active(p), promotions)
   return list(valid_promotions)
   
def on_item_promotions(promotions):
   promotions_per_item = filter(lambda p: p['type'] == 'on-item', promotions)
   return list(promotions_per_item)

def global_promotions(promotions):
   promotions_per_item = filter(lambda p: p['type'] == 'global', promotions)
   return list(promotions_per_item)

