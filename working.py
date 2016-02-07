import numpy as np

class Neighborhood(object):
	"""docstring for Neighborhood"""
	def __init__(self):
		super(Neighborhood, self).__init__()
		self.neighborhoodLayout = open('Data Files/neighborHoodLayout.txt').read()
		self.neighborhoodLayout = [1, 2]
		self.main = []
		self.createPopulation()
		print self.main

	def createPopulation(self):
		for a in xrange(self.neighborhoodLayout[0]):
			column = []
			for b in xrange(self.neighborhoodLayout[1]):
				person  = self.createPerson(a, b)
				column.append(person)
			self.main.append(column)

	def createPerson(self, a, b):
		person = {
			'race': 'black'
			}
		return person

def main():
	ex = Neighborhood()

if __name__ == '__main__':
	main()