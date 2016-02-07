import numpy as np

class Neighborhood(object):
	"""docstring for Neighborhood"""
	def __init__(self):
		super(Neighborhood, self).__init__()
		self.population = open('Data Files/neighborHoodLayout.txt').read()
		print self.population


def main():
	ex = Neighborhood()

if __name__ == '__main__':
	main()