from lists.models import Item, List
from django.urls import resolve
from django.test import TestCase
from django.http import HttpRequest
from lists.views import home_page
from django.template.loader import render_to_string


class HomePageTest(TestCase):

	def test_home_page_returns_correct_html(self):
		response = self.client.get('/')
		html = response.content.decode('utf-8')
		self.assertTrue(html.startswith('<html>'))
		self.assertIn('<title>To-Do lists</title>' , html)
		self.assertTrue(html.strip().endswith('</html>'))
		self.assertTemplateUsed(response , 'home.html')

	def test_uses_home_template(self):
		response = self.client.get('/')
		self.assertTemplateUsed(response , 'home.html')


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

class ListViewTest(TestCase):

	def test_uses_list_template(self):
		list_ = List.objects.create()
		response = self.client.get(f'/lists/{list_.id}/')
		self.assertTemplateUsed(response , 'list.html')

	def test_displays_only_items_for_that_list(self):
		correct_list = List.objects.create()
		Item.objects.create(text='itemey1' , list=correct_list)
		Item.objects.create(text='itemey2' , list=correct_list)
		other_list = List.objects.create()
		Item.objects.create(text='other list item 1' , list=other_list)
		Item.objects.create(text='other list item 2' , list=other_list)

		response = self.client.get(f'/lists/{correct_list.id}/')

		self.assertContains(response , 'itemey1')
		self.assertContains(response , 'itemey2')
		self.assertNotContains(response , 'other list item 1')
		self.assertNotContains(response , 'other list item 2')


class NewListTest(TestCase):
	def test_can_save_a_post_request(self):
		self.client.post('/lists/new' , data = {'item_text' : 'A new list item'})
		self.assertEqual(Item.objects.count() , 1)
		new_item = Item.objects.first()
		self.assertEqual(new_item.text , 'A new list item')

	def test_redirects_after_post(self):
		response = self.client.post('/lists/new' , data = {'item_text' : 'A new list item'})
		self.assertRedirects(response , '/lists/the-only-list-in-the-world/')