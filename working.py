import numpy as np
from random import shuffle

class Neighborhood(object):
	"""docstring for Neighborhood"""
	def __init__(self):
		super(Neighborhood, self).__init__()
		# self.nl = open('Data Files/neighborHoodLayout.txt').read()
		self.nl = [30, 30]  # this is our neighborhood layout (grid)
		# the below are racial diversity thresholds. The first variable in each is the amount
		# of diversity you require to live in that space (positive diversity), and the latter 
		# is the level of diversity at which you will leave (negative diversity).
		self.diverseReqToLeave = [.2, .7]
		self.diverseReqToEnter = [.2, .7]
		self.uniqID = 0  # iterate to give people unique ID #s
		self.percDiversCare = 0.1
		self.racePercentages = [.33, .33]  # white, black, the rest are empty spots
		self.streets = [[6,7,8], [10,11,12]]
		# self.streets = [[],[]]
		# self.tester = [[.3, .7, .3], [.7, .3, .1], [.7, .1, .7]]
		self.main = []
		self.createPopulation()
		self.output(self.main)
		for a in xrange(10):
			self.moveThroughTime()
		self.output(self.main)

	def createPopulation(self):
		for a in xrange(self.nl[0]):
			column = []
			for b in xrange(self.nl[1]):
				if a not in self.streets[0] and b not in self.streets[1]:
					person  = self.createPerson(a, b)  # option for static testing ", self.tester[a][b]"
				else:
					person = None
				column.append(person)
			self.main.append(column)

	def createPerson(self, a, b):
		x = np.random.random()
		div = np.random.random()
		if div < self.percDiversCare:
			careDiv = True
		else:
			careDiv = False
		if x < self.racePercentages[0]:
			person = {
				'race': 'black',
				'careDiv': careDiv,
				'ID': self.uniqID
				}
		elif x >= self.racePercentages[0] and x < self.racePercentages[0] + self.racePercentages[1]:
			person = {
				'race': 'white',
				'careDiv': careDiv,
				'ID': self.uniqID
				}
		else:
			person = {}
		self.uniqID += 1
		return person

	def moveThroughTime(self):
		movers = []
		openSpots = []
		spotsToBeOpened = []  # keeps spots to be cleared until iteration done
		# checks who wants to move and finds all open spots...
		for r, row in enumerate(self.main):
			for c, person in enumerate(row):
				if person is not None:
					if person != {}:
						wantToMove = self.wantsToMove(person, r, c, 'leave')
						if wantToMove:
							spotsToBeOpened.append([r,c])
							openSpots.append([r, c])
							movers.append(person)
					else:
						openSpots.append([r, c])
		for r, c in spotsToBeOpened:
			self.main[r][c] = {}
		shuffle(openSpots)  # randomizes the orderin of the move locations
		shuffle(movers)  # ibid for movers
		
		noAcceptableSpot = 0
		# moves the people...
		while len(movers) != 0:
			newSpot = None
			pers = int(np.floor(np.random.random()*len(movers)))
			for spot in openSpots:
				if self.wantsToMove(movers[pers], spot[0], spot[1], 'enter'):
					newSpot = spot
					break
			if newSpot is None:
				noAcceptableSpot += 1
				spot = int(np.floor(np.random.random()*len(openSpots)))
				newSpot = [openSpots[spot][0], openSpots[spot][1]]
			self.main[newSpot[0]][newSpot[1]] = movers[pers]
			openSpots.remove(newSpot)
			movers.pop(pers)
		print 'No good spots #:', noAcceptableSpot

	def wantsToMove(self, person, r, c, kind):
		neighbors = []
		test = []
		test1 = []
		for row in xrange(r-2, r+3):
			for col in xrange(c-2, c+3):
				if row > -1 and row < self.nl[0]:
					if col > -1 and col < self.nl[1]:
						if row != r or col != c:
							test1.append([row, col])
							p = self.main[row][col]
							if p != {}:
								neighbors.append(p)
								test.append([row, col])
		race = []
		for n in neighbors:
			if n is not None:
				if n['race'] == person['race']:
					race.append(1)
				else:
					race.append(0)
		percSame = np.average(race)
		percDif = 1-percSame
		if kind == 'leave':
			wantToMove = False
			percSameReqMin = self.diverseReqToLeave[1]
			percDifReqMin = self.diverseReqToLeave[0]
			if person['careDiv'] and percDif < percDifReqMin:
				wantToMove = True
			elif percSame < percSameReqMin:
				wantToMove = True
		elif kind == 'enter':
			wantToMove = True
			percSameReqMin = self.diverseReqToEnter[1]
			percDifReqMin = self.diverseReqToEnter[0]
			if person['careDiv'] and percDif < percDifReqMin:
				wantToMove = False
			elif percSame < percSameReqMin:
				wantToMove = False
		return wantToMove

	def output(self, state):
		print 'Number of people:', len([per for row in state for per in row if per != {}])
		for row in state:
			line = []
			for p in row:
				result = ' '
				if p is None:
					result = '.'
				# elif p.get('race') == 'black':
				# 	result = 'B'
				# elif p.get('race') == 'white':
				# 	result = 'W'
				elif p.get('careDiv') == True:
					result = 'D'
				elif p.get('careDiv') == False:
					result = 'R'
				line.append(result)
			print ' '.join(line)
		print ''
		print '  '.join(['-' for a in self.main])
		print ''



def main():
	ex = Neighborhood()

if __name__ == '__main__':
	main()