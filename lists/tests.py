from lists.models import Item
from django.urls import resolve
from django.test import TestCase
from django.http import HttpRequest
from lists.views import home_page
from django.template.loader import render_to_string


class HomePageTest(TestCase):
	# def test_root_url_resolves_to_home_page_view(self):
	# 	found = resolve('/')
	# 	self.assertEqual(found.func , home_page)

	# def test_home_page_returns_correct_html(self):
	# 	request = HttpRequest()
	# 	response = home_page(request)
	# 	html = response.content.decode('utf-8')
	# 	self.assertTrue(html.startswith('<html>'))
	# 	self.assertIn('<title>To-Do lists</title>' , html)
	# 	self.assertTrue(html.endswith('</html>'))

	# def test_home_page_returns_correct_html(self):
	# 	request = HttpRequest()
	# 	response = home_page(request)
	# 	html = response.content.decode('utf-8')
	# 	expected_html = render_to_string('home.html')
	# 	self.assertEqual(html , expected_html)

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

	def test_can_save_a_post_request(self):
		response = self.client.post('/' , data = {'item_text' : 'A new list item'})
		
		self.assertEqual(Item.objects.count() , 1)
		new_item = Item.objects.first()
		self.assertEqual(new_item.text , 'A new list item')
		
		# self.assertIn('A new list item' , response.content.decode())
		# self.assertTemplateUsed(response , 'home.html')

		self.assertEqual(response.status_code , 302)
		self.assertEqual(response['location'] , '/')

	def test_only_saves_items_when_needed(self):
		self.client.get('/')
		self.assertEqual(Item.objects.count() , 0)


	class  ItemModelTest(TestCase):

		def test_saving_and_retrieving_items(self):
			first_item = Item()
			first_item.text = "text 1"
			first_item.save()

			second_item = Item()
			second_item.text = "text 2"
			second_item.save()

			saved_items = Item.objects.all()
			self.assertEqual(saved_items.count() , 2)

			item1 = saved_items[0]
			item2 = saved_items[1]
			self.assertEqual(item1 , "text 1")
			self.assertEqual(item2 , "text 2")
