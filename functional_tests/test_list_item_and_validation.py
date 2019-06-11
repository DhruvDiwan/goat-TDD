from selenium.webdriver.common.keys import Keys
from unittest import skip
from .base import FunctionalTest

class ItemValidationTest(FunctionalTest):
	@skip
	def test_cannot_add_empty_lists(self):
		self.fail('write me')
