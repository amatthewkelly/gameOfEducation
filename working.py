import numpy as np

class Neighborhood(object):
	"""docstring for Neighborhood"""
	def __init__(self):
		super(Neighborhood, self).__init__()
		# self.nl = open('Data Files/neighborHoodLayout.txt').read()
		self.nl = [1, 3]  # this is our neighborhood layout (grid)
		self.main = []
		self.createPopulation()
		self.output(self.main)
		self.moveThroughTime()
		self.output(self.main)

	def createPopulation(self):
		for a in xrange(self.nl[0]):
			column = []
			for b in xrange(self.nl[1]):
				person  = self.createPerson(a, b)
				column.append(person)
			self.main.append(column)

	def createPerson(self, a, b):
		x = np.random.random()
		if x < .25:
			person = {
				'race': 'black'
				}
		elif x >= .25 and x < .5:
			person = {
				'race': 'white'
				}
		else:
			person = {}
		return person

	def moveThroughTime(self):
		temp = []
		for r, row in enumerate(self.main):
			column = []
			for c, person in enumerate(row):
				if person != {}:
					new = self.wantsToMove(person, r, c)
				else:
					new = {}
				column.append(new)
			temp.append(column)
		self.main = temp

	def wantsToMove(self, person, r, c):
		neighbors = []
		for row in xrange(r-1, r+2):
			for col in xrange(c-1, c+2):
				if row > -1 and row < self.nl[0]:
					if col > -1 and col < self.nl[1]:
						if row != r or col != c:
							person = self.main[row][col]
							if person != {}:
								neighbors.append(person)
		print neighbors

		return person


	def interaction(self, person):
		pass

	def output(self, state):
		for row in state:
			line = []
			for p in row:
				result = ' '
				if p.get('race') == 'black':
					result = 'B'
				elif p.get('race') == 'white':
					result = 'W'
				line.append(result)
			print '  '.join(line)
		print ''
		print '  '.join(['-' for a in self.main])
		print ''



def main():
	ex = Neighborhood()

if __name__ == '__main__':
	main()