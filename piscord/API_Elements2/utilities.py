class Cache:
	def __init__(self, func):
		self.func = func
		self.results = {}

	def __call__(self,ref):
		if ref in self.results:
			return self.results[ref]
		result = self.func(ref)
		self.results[ref] = result
		return result

class API_Element:

	def to_json(self):
		output = {}
		for x,y in self.__dict__.items():
			if x.endswith("__bot"):
				continue
			if y != None:
				if type(y) == list:
					e=[]
					for p in y:
						if isinstance(p,API_Element):
							p = p.to_json()
						e += [p]
					y = e
				if isinstance(y,API_Element):
					y = y.to_json()
				output[x]=y
		return output