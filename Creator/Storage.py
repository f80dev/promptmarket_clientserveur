class Storage:

	domain_server=""

	def __init__(self,domain_server=""):
		self.domain_server=domain_server

	def add(self,content,overwrite=False):
		pass

	def list(self):
		pass

	def get(self,key):
		pass

	def rem(self,key):
		pass

	def burn(self,key):
		self.rem(key)