import numpy as np

class Neighborhood(object):
	"""docstring for Neighborhood"""
	def __init__(self):
		super(Neighborhood, self).__init__()
		# self.nl = open('Data Files/neighborHoodLayout.txt').read()
		self.nl = [9, 9]  # this is our neighborhood layout (grid)
		self.diversReqToMove = 1  # if percent neighbors of same race less than this
								   # then wants to move.
		self.uniqID = 0  # iterate to give people unique ID #s
		self.main = []
		self.createPopulation()
		self.output(self.main)
		for a in xrange(30):
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
				'race': 'black',
				'ID': self.uniqID
				}
		elif x >= .25 and x < .5:
			person = {
				'race': 'white',
				'ID': self.uniqID
				}
		else:
			person = {}
		self.uniqID += 1
		return person

	def moveThroughTime(self):
		movers = []
		openSpots = []
		# checks who wants to move and finds all open spots...
		for r, row in enumerate(self.main):
			for c, person in enumerate(row):
				if person != {}:
					wantToMove = self.wantsToMove(person, r, c)
					if wantToMove:
						self.main[r][c] = {}
						openSpots.append([r, c])
						movers.append(person)
				else:
					openSpots.append([r, c])

		# moves the people...
		while len(movers) != 0:
			pers = int(np.floor(np.random.random()*len(movers)))
			spot = int(np.floor(np.random.random()*len(openSpots)))
			self.main[openSpots[spot][0]][openSpots[spot][1]] = movers[pers]
			movers.pop(pers)
			openSpots.pop(spot)

	def wantsToMove(self, person, r, c):
		neighbors = []
		for row in xrange(r-1, r+2):
			for col in xrange(c-1, c+2):
				if row > -1 and row < self.nl[0]:
					if col > -1 and col < self.nl[1]:
						if row != r or col != c:
							p = self.main[row][col]
							if p != {}:
								neighbors.append(p)
		race = []
		for n in neighbors:
			if n['race'] == person['race']:
				race.append(1)
			else:
				race.append(0)
		wantToMove = False
		if np.average(race) < self.diversReqToMove:
			wantToMove = True
		return wantToMove

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