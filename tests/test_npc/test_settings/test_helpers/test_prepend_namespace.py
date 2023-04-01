from npc.settings.helpers import prepend_namespace

class TestWithNoNamespace:
	data = {"test": True}
	namespace = None

	def test_returns_raw_data(self):
		result = prepend_namespace(self.data, self.namespace)

		assert result == self.data

class TestWithEmptyNamespace:
	data = {"test": True}
	namespace = ""

	def test_returns_raw_data(self):
		result = prepend_namespace(self.data, self.namespace)

		assert result == self.data

class TestWithSimpleNamespace:
	data = {"test": True}
	namespace = "passing"
	
	def test_returns_data_inside_namespace(self):
		result = prepend_namespace(self.data, self.namespace)

		assert result == {"passing": {"test": True}}

class TestWithNestedNamespace:
	data = {"test": True}
	namespace = "deep.passing"
	
	def test_returns_data_inside_namespace(self):
		result = prepend_namespace(self.data, self.namespace)

		assert result == {"deep": {"passing": {"test": True}}}
