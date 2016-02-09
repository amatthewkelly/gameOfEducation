import numpy as np
import json
import matplotlib.pyplot as plt 
from random import shuffle

class Neighborhood(object):
	"""docstring for Neighborhood"""
	def __init__(self):
		super(Neighborhood, self).__init__()
		# self.cityBuild['neighborHoodLayout'] = open('Data Files/neighborHoodLayout.txt').read()
		self.iterations = 10
		self.movingThreshold = 50000
		self.cityBuild = {
			'neighborHoodLayout': [50, 50],  # this is our neighborhood layout (grid)
			'cityGrid': [1, 1],  # this is our city layout (grid)
			'streets': []  # specifies street locations within neighborhoods ([row], [column])
			}
		self.popStats = {
			'diverseReqToLeave': {
				'positive': .3,  # amount of diversity you require to live in that space if you care about diversity (positive diversity)
				'neighbors': .5,  # level of diversity at which you will leave if you don't care about diversity (negative diversity)
				'neighborhood': .3  # diversity required of your neighborhood (negative diversity)
				},
			'diverseReqToEnter': {
				'positive': .3,
				'neighbors': .5,
				'neighborhood': .3
				},
			'uniqID': 0,  # iterate to give people unique ID #s
			'percDiversCare': 0.0,  # percentage of people who care about diversity
			'racePercentages': [.33, .33],  # white, black, the rest are empty spots
			'wealthIndexPeakByRace': [6, 4],  # white, black (out of 10, 9 heightest 0 lowest)
			# the below distributions are skewed normal distributions for blacks and whites.
			'blackSocDistr': [int(b*100000) for b in [max(np.random.normal(loc=-3)+5, 0) for a in xrange(1000)] if b < 10],
			'whiteSocDistr': [int(b*100000) for b in [max(np.random.normal(loc=3)+5, 0) for a in xrange(1000)] if b < 10]
			}
		# the below places streets into a conveninet format for latter calculations...
		self.cityLayout = [[[
			self.cityBuild['streets'], [2+(b*3) for b in xrange((self.cityBuild['neighborHoodLayout'][0]-2)/3)]
			] for b in xrange(
				self.cityBuild['cityGrid'][1]
				)]for a in xrange(self.cityBuild['cityGrid'][0])]
		self.city = []  # the main array for holding the current population state
		self.neighborhoodData = []
		self.runningNData = []
		self.evaluate()

	def evaluate(self, write=True):
		print 'Evaluating with: (%d people) (%d neighborhoods) (%d iterations) (write = %s)' % (
			self.cityBuild['neighborHoodLayout'][0]*self.cityBuild['neighborHoodLayout'][1]*self.cityBuild['cityGrid'][0]*self.cityBuild['cityGrid'][1],
			self.cityBuild['cityGrid'][0]*self.cityBuild['cityGrid'][1],
			self.iterations,
			str(write)
			)
		if write:
			self.text_file = open("Output.txt", "w")
		self.createPopulation(new=True)  # if new is False, will use the saved population
		self.stateOutput(self.city, 'race', message='initial', write=write, headerOn=True) # prints the current state of the city
		self.stateOutput(self.city, 'income', message='initial', write=write) # prints the current state of the city
		first = True
		for a in xrange(self.iterations):
			self.tester = []
			unHappyMovers = self.moveThroughTime()
			if first:
				first = False	
			x = [[b['percBlack'], b['socio']] for b in self.neighborhoodData]
			self.runningNData.append(x)
			print str(a)+' ('+str(unHappyMovers)+')',
		print 'Finished\n'
		self.stateOutput(self.city, 'race', message='final', write=write) # prints the current state of the city
		self.stateOutput(self.city, 'income', message='final', write=write) # prints the current state of the city
		if write:
			self.text_file.close()
			print 'Saved'
		# self.statsOutput()  # outPuts neighborhood specific stats...

	def createPopulation(self, new=False):
		layoutIndex = 0
		if new:
			for n in xrange(np.sum([len(a) for a in self.cityLayout])):
				self.neighborhoodData.append({})
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
				'race': 'black',  # never changes (obviously)
				'careDiv': careDiv,  # also never changes, though we could factor in apathy here later,
									 # I imagine this factor will general map to socioEconomic
				'ID': self.popStats['uniqID'],  # like a SSN
				'income': income,  # generated for starting population from skewed gaussian with assumption
								   # that whites are wealthier than blacks. From there it updates. Assumption
								   # for now is that this update is based on neighborhood socioEconomic, not
								   # immediate neighbors
				'neighborhood': neighborhood,  # not currently used for computation, so at end this reflects
											   # starting neighborhood. As such it does not update throughout
											   # so is not a realiable marker of current pos (see self.city, and
											   # other companion layout variables for location reference)
				'age': 0  # should iterate with each cycle, we can imagine age specific variables that would
						  # make this important, especially if we dive into families
				}
		elif x >= self.popStats['racePercentages'][0] and x < self.popStats['racePercentages'][0] + self.popStats['racePercentages'][1]:
			socVal = int(np.floor(np.random.random()*len(self.popStats['whiteSocDistr'])))
			income = self.popStats['whiteSocDistr'][socVal]
			person = {
				'race': 'white',
				'careDiv': careDiv,
				'ID': self.popStats['uniqID'],
				'income': income,
				'neighborhood': neighborhood,
				'age': 0
				}
		else:
			person = {}
		self.popStats['uniqID'] += 1
		return person

	def moveThroughTime(self):
		movers = []
		openSpots = []
		spotsToBeOpened = []  # keeps spots that will be cleared until they can be reinserted
		# checks who wants to move and finds all open spots...
		for n in xrange(len(self.city)):
			self.updateNeighborHoodStats(n)
		for n, neigh in enumerate(self.city):
			for r, row in enumerate(neigh):
				for c, person in enumerate(row):
					if person is not None:
						if person != {}:
							moveWanted, neighbors = self.wantToMove(person, n, r, c, 'leave')
							self.city[n][r][c] = self.updateValuesFromArea(person, n)
							if moveWanted:
								spotsToBeOpened.append([n, r, c])
								openSpots.append([n, r, c])
								movers.append(person)
						else:
							openSpots.append([n, r, c])
		# clears out the old spots in the map
		for n, r, c in spotsToBeOpened:
			self.city[n][r][c] = {}
		shuffle(openSpots)  # randomizes the orderin of the move locations
		shuffle(movers)  # ibid for movers
		noAcceptableSpot = 0
		# moves the people, after checking for an acceptable new spot...
		while len(movers) != 0:
			newSpot = None
			pers = int(np.floor(np.random.random()*len(movers)))
			# checks available spots for acceptable one...
			for spot in openSpots:
				moveWanted, neighbors = self.wantToMove(movers[pers], spot[0], spot[1], spot[2], 'enter')
				if moveWanted:
					newSpot = spot
					break
			# if no available spot is acceptable, assigns an available spot at random (even though it isn't acceptable)
			if newSpot is None:
				noAcceptableSpot += 1
				spot = int(np.floor(np.random.random()*len(openSpots)))
				newSpot = [openSpots[spot][0], openSpots[spot][1], openSpots[spot][2]]
			self.city[newSpot[0]][newSpot[1]][newSpot[2]] = movers[pers]
			openSpots.remove(newSpot)
			movers.pop(pers)
		return noAcceptableSpot
		# print 'No good spots #:', noAcceptableSpot

	def wantToMove(self, person, n1, r, c, kind):
		neighbors = []
		for row in xrange(r-2, r+3):
			for col in xrange(c-2, c+3):
				if row > -1 and row < self.cityBuild['neighborHoodLayout'][0]:
					if col > -1 and col < self.cityBuild['neighborHoodLayout'][1]:
						if row != r or col != c:
							p = self.city[n1][row][col]
							if p != {}:
								neighbors.append(p)
		race = []
		for n in neighbors:
			if n is not None:
				if n['race'] == person['race']:
					race.append(1)
				else:
					race.append(0)
		percSame = np.average(race)
		percDif = 1-percSame
		neighbSame = self.neighborhoodData[n1]['percBlack']
		if person['race'] == 'white':
			neighbSame = 1 - neighbSame
		# print percSame/float(self.popStats['diverseReqToEnter'][1]), percDif/float(self.popStats['diverseReqToEnter'][0])
		if kind == 'leave':
			wantToMove = False
			if person['careDiv'] and percDif < self.popStats['diverseReqToLeave']['positive']:
				wantToMove = True
			elif percSame < self.popStats['diverseReqToLeave']['neighbors'] or neighbSame < self.popStats['diverseReqToLeave']['neighborhood']:
				wantToMove = True
			if person['income'] < self.movingThreshold:
				wantToMove = False
		elif kind == 'enter':
			wantToMove = True
			if person['careDiv'] and percDif < self.popStats['diverseReqToLeave']['positive']:
				wantToMove = False
			elif percSame < self.popStats['diverseReqToLeave']['neighbors'] or neighbSame < self.popStats['diverseReqToLeave']['neighborhood']:
				wantToMove = False
			if person['income'] < self.neighborhoodData[n1]['socio']:
				wantToMove = False
		return wantToMove, neighbors

	def movingFitnessFunction(self, race, socio):
		pass

	def updateNeighborHoodStats(self, n):
		socVals = []
		raceVals = []
		for row in self.city[n]:
			for per in row:
				if per is not None and per != {}:
					socVals.append(per['income'])
					if per['race'] == 'black':
						raceVals.append(1)
					else:
						raceVals.append(0)
		self.neighborhoodData[n]['socio'] = int(np.mean(socVals))
		self.neighborhoodData[n]['percBlack'] = int(1000*np.mean(raceVals))/float(1000)

	def updateValuesFromArea(self, person, n):
		nSoc = self.neighborhoodData[n]['socio']
		pSoc = int(person['income'])
		newSoc = pSoc*((pSoc/float(max(nSoc, 1))-1)*.025+1)
		person['income'] = newSoc
		return person

	def stateOutput(self, state, kind, message='', write=False, headerOn=False):
		def personReturn(p, kind):
			temp = None
			if kind == 'race':
				if p == {}:
					temp = '  '
				elif p is None:
					temp = ' .'
				elif p['race'] == 'black':
					temp = ' B'
				elif p['race'] == 'white':
					temp = ' W'
			elif kind == 'income':
				if p == {}:
					temp = '  '
				elif p is None:
					temp = ' .'
				else:
					temp = str(int(np.floor(p['income']/float(100000))))
					if len(temp) == 1:
						temp = ' '+temp
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
						temp2.append(personReturn(item, kind))
					temp.append(' '.join(temp2))
				master.append('     '.join(temp))
			if nRow != self.cityBuild['cityGrid'][0] - 1:
				master.append('\n'.join(['  '.join([
					'' for a in xrange(self.cityBuild['cityGrid'][1]*self.cityBuild['neighborHoodLayout'][1]+(self.cityBuild['cityGrid'][1]-1)*2)
					])+' ' for a in xrange(2)]))
		if write:
			tempHead = {}
			for key in self.popStats.keys():
				if key not in ['blackSocDistr', 'whiteSocDistr']:
					tempHead[key] = self.popStats[key]
			header = json.dumps([{'iterations': self.iterations}, tempHead, json.dumps(self.cityBuild)])
			if headerOn:
				self.text_file.write(header)
			mes = '\nmessage: '+message
			self.text_file.write(mes)
			body = '\n'+'\n'.join(master)+'\n'+'\n'
			self.text_file.write(body)
		else:
			print 'Number of people:', len([per for neigh in state for row in neigh for per in row if per != {}])
			print message
			for row in master:
				print row
			print ''
			print '  '.join(['-' for a in self.city])
			print ''

	def statsOutput(self, write=False):
		master = []
		for n in xrange(len(self.runningNData[0])):
			temp = []
			for i in xrange(len(self.runningNData)):
				temp.append(self.runningNData[i][n][1])
			master.append(temp)
		fig = plt.figure()
		ax1 = fig.add_subplot(111)
		x = np.array(range(len(self.runningNData)))
		for y in master:
			ax1.scatter(x, y)
			b, c = np.polyfit(x, y, 1)  # adds a regresstion line
			ax1.plot(x,  b*x + c, '-')  # a*x**2 +
		plt.show()


def main():
	ex = Neighborhood()

if __name__ == '__main__':
	main()