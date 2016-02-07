import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.animation as animation


class HeatFlow(object):
	"""docstring for HeatFlow"""
	def __init__(self):
		super(HeatFlow, self).__init__()
		self.startingTemp = 10 + 273.15  # K
		self.waterSize = [100, 100, 10]  # m
		self.units = [35, 35, 6]
		self.unitSize = [self.waterSize[a]/float(self.units[a]) for a in xrange(3)]
		self.main = []
		self.sidesTemp = 10 + 273.15  # K
		self.topTemp = 10 + 273.15  # K
		self.source1Temp = 40 + 273.15  # K
		self.source2Temp = 40 + 273.15  # K
		self.source1Vel = [0, 0, 40]  # m/s
		self.source2Vel = [0, 0, -40]  # m/s
		self.expectedTest = 0 
		self.source1 = [[int(self.units[0]/2)-3, int(self.units[0]/2)+3], [4, 6]]
		self.source2 = [[int(self.units[0]/2)-3, int(self.units[0]/2)+3], [self.units[1]-6, self.units[1]-4]]
		# self.source=[[0,self.units[0]],[0,self.units[1]]]
		self.createStartingState(self.units)
		# self.processThroughTime(5, self.main)
		self.plotState(30, 40, save=False, vel=False)
		# self.animateState(10, 20)
	
	def createStartingState(self, units):
		for x in xrange(units[0]):
			column = []
			for y in xrange(units[1]):
				newItem = self.createInitiatalItem([x, y, z])
				column.append(pillar)
			self.main.append(column)

	def createInitiatalItem(self, position):
		item = {
			'position': position,
			'time': 0,
			'temperature': self.startingTemp,
			'velocity': [0, 0, 0],
			}
		return item

	def processThroughTime(self, interval, state):
		newState = []
		for x in state:
			column = []
			for y in x:
				pillar = []
				for z in y:
					item = self.interaction(z, interval)
					pillar.append(item)
				column.append(pillar)
			newState.append(column)
		return newState

	def interaction(self, item, interval):
		touchItemPositions = []
		for i in xrange(3):
			for a in [item['position'][i]-1, item['position'][i]+1]:
				if i == 0:
					newSpot = [a, item['position'][1], item['position'][2]]
				elif i == 1:
					newSpot = [item['position'][0], a, item['position'][2]]
				else:
					newSpot = [item['position'][0], item['position'][1], a]
				touchItemPositions.append(newSpot)
		newVelocity, swapPos = self.simpleVelocityFlow(item, touchItemPositions, interval)
		newTemp = self.simpleHeatFlow(item, touchItemPositions, interval, swapPos)
		item['temperature'] = newTemp
		item['velocity'] = newVelocity
		item['time'] = item['time'] + interval
		return item

	def simpleHeatFlow(self, item, touchItemPositions, time, swapPos):
		interTemps = []
		area = self.unitSize[0]*self.unitSize[1]  # m^2
		curTemp = item['temperature']
		for itemTouchedPosition in touchItemPositions:
			if itemTouchedPosition == swapPos:
				m = 30
			else:
				m = 1
			x = itemTouchedPosition[0]
			y = itemTouchedPosition[1]
			z = itemTouchedPosition[2]
			if z == self.units[2] and self.source1[0][0] <= x <= self.source1[0][1] and self.source1[1][0] <= y <= self.source1[1][1]:
				k =  -0.01  # water to air, ish
				interTemp = self.source1Temp
			elif z == -1 and self.source2[0][0] <= x <= self.source2[0][1] and self.source2[1][0] <= y <= self.source2[1][1]:
				k =  -0.01  # water to air, ish
				interTemp = self.source2Temp
			elif z == self.units[2]:
				k =  -0.05  # water to air, ish
				interTemp = self.topTemp
			elif x in [-1, self.units[0]] or y in [-1, self.units[1]] or z == -1:
				k =  -0.05  # water to air, ish
				interTemp = self.sidesTemp
			else:
				k =  -0.06  # water to water, ish
				touched = self.main[x][y][z]
				interTemp = touched['temperature']
			newTemp = interTemp + (curTemp - interTemp) * np.exp(k * time / float(m))
			interTemps.append(newTemp)
		newTemp = sum(interTemps) / float(len(interTemps))
		return newTemp

	def simpleVelocityFlow(self, item, touchItemPositions, time):
		interVels = []
		curVel = item['velocity']
		curPos = item['position']
		for itemTouchedPosition in touchItemPositions:
			x = itemTouchedPosition[0]
			y = itemTouchedPosition[1]
			z = itemTouchedPosition[2]
			if z == self.units[2] and self.source1[0][0] <= x <= self.source1[0][1] and self.source1[1][0] <= y <= self.source1[1][1]:
				interVel = self.source1Vel
			elif z == -1 and self.source2[0][0] <= x <= self.source2[0][1] and self.source2[1][0] <= y <= self.source2[1][1]:
				interVel = self.source2Vel
			elif z == self.units[2]:
				interVel = None
			elif x in [-1, self.units[0]] or y in [-1, self.units[1]] or z == -1:
				interVel = None
			else:
				touched = self.main[x][y][z]
				interVel = touched['velocity']
			interVels.append(interVel)
		vx = []
		vy = []
		vz = []
		for a in interVels:
			if not a is None:
				signs = []
				for b in xrange(3):
					if np.random.random() > .5:
						signs.append(-1)
					else:
						signs.append(1)
				vx.append(a[0]+np.random.random()*.1*signs[0])
				vy.append(a[1]+np.random.random()*.1*signs[1])
				vz.append(a[2]+np.random.random()*.1*signs[2])
		newVelocity = []
		for i, item in enumerate([vx, vy, vz]):
			newVel = sum(item) / float(len(item))
			oldVel = curVel[i]
			newVelocity.append((newVel*5+oldVel)/6)
		if newVelocity[0] == 0:
			newVelocity = curVel
			swapPosition = None
		else:
			theta = np.arctan(newVelocity[1]/float(newVelocity[0]))*180/np.pi
			psi = np.arctan(newVelocity[2]/float(newVelocity[0]))*180/np.pi
			if newVelocity[1] < 0 and newVelocity[0] < 0:
				theta += 180
			if newVelocity[2] < 0 and newVelocity[0] < 0:
				psi += 180
			quad = [0, 0, 0]
			if -45 < psi <= 45:
				if -45 < theta <= 45:
					quad[0] = 1
				elif 45 < theta <= 135:
					quad[1] = 1
				elif 135 < theta <= 225:
					quad[0] = -1
				else:
					quad[1] = -1
			elif 45 < psi <= 135:
				quad[2] = 1
			elif 135 < psi <= 225:
				if -45 < theta <= 45:
					quad[0] = 1
				elif 45 < theta <= 135:
					quad[1] = 1
				elif 135 < theta <= 225:
					quad[0] = -1
				else:
					quad[1] = -1
			else:
				quad[2] = -1
			if quad[2] == -1:
				self.expectedTest += 1
			swapPosition = [curPos[i]+quad[i] for i in xrange(3)]
			checkPosition = [curPos[i]-quad[i] for i in xrange(3)]
			for i, el in enumerate(checkPosition):
				if el < 0 or el > self.units[i]:
					newVelocity[i] = -newVelocity[i]
		return newVelocity, swapPosition

	def plotState(self, timeInterval, numSteps, save=True, vel=False):
		first = True
		i = 0
		while i < numSteps:
			self.expectedTest = 0
			i += 1
			self.main = self.processThroughTime(timeInterval, self.main)
			print i, self.expectedTest/(float(np.product(self.units)))
		xs = []
		ys = []
		zs = []
		vxs = []
		vys = []
		vzs = []
		c = []
		s = []
		l = []
		for x in self.main:
			for y in x:
				for z in y:
					vx = float(z['velocity'][0])
					vy = float(z['velocity'][1])
					vz = float(z['velocity'][2])
					xs.append(z['position'][0])
					ys.append(z['position'][1])
					zs.append(z['position'][2])
					vxs.append(vx)
					vys.append(vy)
					vzs.append(vz)
					c.append(z['temperature'])
					s.append(20)
					l.append((float(vx)**2+float(vy)**2+float(vz)**2)**(1/float(2)))
		fig = plt.figure(figsize=(8, 10))
		ax = fig.add_subplot(111, projection='3d')
		# ax.colorbar(label='radius')
		ax.view_init(20, 20)
		if vel:
			ax.quiver(xs, ys, zs, vxs, vys, vzs, length=.4)
		else:
			ax.scatter(xs, ys, zs, c=c, s=s, alpha=0.7)
		if save:
			fig.savefig('test%s.png'%str(i), bbox_inches='tight')
		else:
			plt.show()

	def returnData(self, state, i):
		xs = []
		ys = []
		zs = []
		c = []
		s = []
		for x in state:
			for y in x:
				for z in y:
					xs.append(z['position'][0])
					ys.append(z['position'][1])
					zs.append(z['position'][2])
					c.append(z['temperature'])
					s.append(50)
		return xs, ys, zs, c, s

	def animateState(self, timeInterval, numSteps):
		dpi = 100
		numframes = numSteps
		fig = plt.figure(figsize=(8, 10))

		ax = fig.add_subplot(111, projection='3d')
		ax.view_init(20, 20)
		ax.colorbar(label='radius')

		def update_plot(i):
			"""Update the scatter plot."""
			print i,
			self.main = self.processThroughTime(timeInterval, self.main)
			xs, ys, zs, c, s = self.returnData(self.main, i)
			print max(c), min(c)
			scat = ax.scatter(xs, ys, zs, c=c, alpha=0.7, animated=True)
			return scat,

		ani = animation.FuncAnimation(
			fig,
			update_plot,
			frames=xrange(numframes-1)
			)
		writer = animation.writers['ffmpeg'](fps=5)
		ani.save('demo.mp4', writer=writer, dpi=dpi)


def main():
	ex = HeatFlow()

if __name__ == '__main__':
	main()