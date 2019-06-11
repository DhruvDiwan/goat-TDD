from django.test import TestCase
from lists.models import Item , List

class  ListAndItemModelTest(TestCase):

	def test_saving_and_retrieving_items(self):
		list_ = List()
		list_.save()

		first_item = Item()
		first_item.text = "text 1"
		first_item.list = list_
		first_item.save()

		second_item = Item()
		second_item.text = "text 2"
		second_item.list = list_
		second_item.save()

		saved_list = List.objects.first()
		self.assertEqual(saved_list , list_)


		saved_items = Item.objects.all()
		self.assertEqual(saved_items.count() , 2)

		item1 = saved_items[0]
		item2 = saved_items[1]
		self.assertEqual(item1.text , "text 1")
		self.assertEqual(item1.list , list_)
		self.assertEqual(item2.text , "text 2")
		self.assertEqual(item2.list , list_)
