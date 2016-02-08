import numpy as np
import json
# import matplotlib.pyplot as plt 
from random import shuffle

class Neighborhood(object):
	"""docstring for Neighborhood"""
	def __init__(self):
		super(Neighborhood, self).__init__()
		# self.cityBuild['neighborHoodLayout'] = open('Data Files/neighborHoodLayout.txt').read()
		self.cityBuild = {
			'neighborHoodLayout': [14, 14],  # this is our neighborhood layout (grid)
			'cityGrid': [3, 5],  # this is our city layout (grid)
			'streets': [[4, 9], [4, 9]]  # specifies street locations within neighborhoods (row, column)
			}
		self.popStats = {
			# the below are racial diversity thresholds. The first variable in each is the amount
			# of diversity you require to live in that space if you care about diversity (positive diversity), and the latter 
			# is the level of diversity at which you will leave if you don't care about diversity (negative diversity).
			'diverseReqToLeave': [.2, .7],
			'diverseReqToEnter': [.2, .7],
			'uniqID': 0,  # iterate to give people unique ID #s
			'percDiversCare': 0.0,  # percentage of people who care about diversity
			'racePercentages': [.33, .33],  # white, black, the rest are empty spots
			'wealthIndexPeakByRace': [6, 4],  # white, black (out of 10, 9 heightest 0 lowest)
			# the below distributions are skewed normal distributions for blacks and whites.
			'blackSocDistr': [int(b*100000) for b in [max(np.random.normal(loc=-2)+5, 0) for a in xrange(1000)] if b < 10],
			'whiteSocDistr': [int(b*100000) for b in [max(np.random.normal(loc=2)+5, 0) for a in xrange(1000)] if b < 10]
			}
		# the below places streets into a conveninet format for latter calculations...
		self.cityLayout = [[self.cityBuild['streets'] for b in xrange(
			self.cityBuild['cityGrid'][1]
			)] for a in xrange(self.cityBuild['cityGrid'][0])]
		self.city = []  # the main array for holding the current population state
		self.createPopulation(new=True)  # if new is False, will use the saved population
		self.output(self.city) # prints the current state of the city
		for a in xrange(1):
			self.moveThroughTime()
		self.output(self.city) # prints the current state of the city

	def createPopulation(self, new=False):
		layoutIndex = 0
		if new:
			for n in xrange(np.sum([len(a) for a in self.cityLayout])):
				cityIndex = 0
				streets = None
				for i, a in enumerate(self.cityLayout):
					for j, b in enumerate(a):
						if cityIndex == n:
							streets = self.cityLayout[i][j]
						cityIndex += 1
				neighborhood = []
				for a in xrange(self.cityBuild['neighborHoodLayout'][0]):
					column = []
					for b in xrange(self.cityBuild['neighborHoodLayout'][1]):
						if a not in streets[0] and b not in streets[1]:
							person  = self.createPerson(a, b, n)  # option for static testing ", self.tester[a][b]"
						else:
							person = None
						column.append(person)
					neighborhood.append(column)
				self.city.append(neighborhood)
			json.dump(self.city, open("testStartPopulation.txt", 'w'))
		else:
			self.city = json.load(open("testStartPopulation.txt"))

	def createPerson(self, a, b, neighborhood):
		x = np.random.random()
		div = np.random.random()
		if div < self.popStats['percDiversCare']:
			careDiv = True
		else:
			careDiv = False
		if x < self.popStats['racePercentages'][0]:
			socVal = int(np.floor(np.random.random()*len(self.popStats['blackSocDistr'])))
			income = self.popStats['blackSocDistr'][socVal]
			person = {
				'race': 'black',
				'careDiv': careDiv,
				'ID': self.popStats['uniqID'],
				'income': income,
				'neighborhood': neighborhood,
				'absLoc': 0
				}
		elif x >= self.popStats['racePercentages'][0] and x < self.popStats['racePercentages'][0] + self.popStats['racePercentages'][1]:
			socVal = int(np.floor(np.random.random()*len(self.popStats['whiteSocDistr'])))
			income = self.popStats['whiteSocDistr'][socVal]
			person = {
				'race': 'white',
				'careDiv': careDiv,
				'ID': self.popStats['uniqID'],
				'income': income,
				'neighborhood': neighborhood
				}
		else:
			person = {}
		self.popStats['uniqID'] += 1
		return person

	def moveThroughTime(self):
		movers = []
		openSpots = []
		spotsToBeOpened = []  # keeps spots to be cleared until iteration done
		# checks who wants to move and finds all open spots...
		for n, neigh in enumerate(self.city):
			for r, row in enumerate(neigh):
				for c, person in enumerate(row):
					if person is not None:
						if person != {}:
							moveWanted, neighbors = self.wantToMove(person, n, r, c, 'leave')
							# self.city[r][c] = self.updateValuesFromSorrounding(person, neighbors, r, c)
							if moveWanted:
								spotsToBeOpened.append([n, r, c])
								openSpots.append([n, r, c])
								movers.append(person)
						else:
							openSpots.append([n, r, c])
		for n, r, c in spotsToBeOpened:
			self.city[n][r][c] = {}
		shuffle(openSpots)  # randomizes the orderin of the move locations
		shuffle(movers)  # ibid for movers
		noAcceptableSpot = 0
		# moves the people...
		while len(movers) != 0:
			newSpot = None
			pers = int(np.floor(np.random.random()*len(movers)))
			for spot in openSpots:
				moveWanted, neighbors = self.wantToMove(movers[pers], spot[0], spot[1], spot[2], 'enter')
				if moveWanted:
					newSpot = spot
					break
			if newSpot is None:
				noAcceptableSpot += 1
				spot = int(np.floor(np.random.random()*len(openSpots)))
				newSpot = [openSpots[spot][0], openSpots[spot][1], openSpots[spot][2]]
			self.city[newSpot[0]][newSpot[1]][newSpot[2]] = movers[pers]
			openSpots.remove(newSpot)
			movers.pop(pers)
		print 'No good spots #:', noAcceptableSpot

	def wantToMove(self, person, n1, r, c, kind):
		# print person, r, c, n1, self.city[n1][r][c]
		neighbors = []
		test = []
		test1 = []
		for row in xrange(r-1, r+2):
			for col in xrange(c-1, c+2):
				if row > -1 and row < self.cityBuild['neighborHoodLayout'][0]:
					if col > -1 and col < self.cityBuild['neighborHoodLayout'][1]:
						if row != r or col != c:
							# print col, row
							# print 'here', type(self.city[n1][row])
							test1.append([row, col])
							# print n1
							# print self.city[n1]
							try:
								p = self.city[n1][row][col]
							except:
								print r, c, n1
								print self.city[n1][r][c]
								raise EOFError
							if p != {}:
								neighbors.append(p)
								test.append([row, col])
		race = []
		for n in neighbors:
			# print n
			if n is not None:
				if n['race'] == person['race']:
					race.append(1)
				else:
					race.append(0)
		percSame = np.average(race)
		percDif = 1-percSame
		if kind == 'leave':
			wantToMove = False
			percSameReqMin = self.popStats['diverseReqToLeave'][1]
			percDifReqMin = self.popStats['diverseReqToLeave'][0]
			if person['careDiv'] and percDif < percDifReqMin:
				wantToMove = True
			elif percSame < percSameReqMin:
				wantToMove = True
		elif kind == 'enter':
			wantToMove = True
			percSameReqMin = self.popStats['diverseReqToEnter'][1]
			percDifReqMin = self.popStats['diverseReqToEnter'][0]
			if person['careDiv'] and percDif < percDifReqMin:
				wantToMove = False
			elif percSame < percSameReqMin:
				wantToMove = False
		return wantToMove, neighbors

	def updateValuesFromSorrounding(self, person, neighbors, r, c):
		# for n in neighbors:
		# 	print n
		return person

	def output(self, state, write=False):
		def personReturn(p, kind):
			temp = None
			if kind == 'race':
				if p == {}:
					temp = ' '
				elif p is None:
					temp = '.'
				elif p['race'] == 'black':
					temp = 'B'
				elif p['race'] == 'white':
					temp = 'W'
			return temp
		curRow = 0
		pState = []
		for a in xrange(self.cityBuild['cityGrid'][0]):
			temp = []
			for b in xrange(self.cityBuild['cityGrid'][1]):
				temp.append(state[curRow])
				curRow += 1
			pState.append(temp)
		master = []
		for nRow in xrange(self.cityBuild['cityGrid'][0]):
			for cRow in xrange(self.cityBuild['neighborHoodLayout'][0]):
				temp = []
				for nCol in xrange(self.cityBuild['cityGrid'][1]):
					temp2 = []
					for cCol in xrange(self.cityBuild['neighborHoodLayout'][1]):
						item = pState[nRow][nCol][cRow][cCol]
						temp2.append(personReturn(item, 'race'))
					temp.append(' '.join(temp2))
				master.append('     '.join(temp))
			if nRow != self.cityBuild['cityGrid'][0] - 1:
				master.append('\n'.join(['  '.join([
					'' for a in xrange(self.cityBuild['cityGrid'][1]*self.cityBuild['neighborHoodLayout'][1]+(self.cityBuild['cityGrid'][1]-1)*2)
					])+' ' for a in xrange(2)]))
		if write:
			print 'write'
		else:
			print 'Number of people:', len([per for neigh in state for row in neigh for per in row if per != {}])
			for row in master:
				print row
			print ''
			print '  '.join(['-' for a in self.city])
			print ''


def main():
	ex = Neighborhood()

if __name__ == '__main__':
	main()