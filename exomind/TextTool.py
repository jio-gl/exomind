

class TextTool:

	__text = None

	def __init__(self, text):
		self.text = text

	def extract_elements(self):
		raise Exception('TextTool is an abstract class, redefine method "extract_elements"')

	def set_text(self, text):
		self.text = text
