# this class is for simulating people walking in the map 
# the people are simulated as discrete time steps
# people are simulated as position over time
# the max distance between two position of the same people is 1 meter between two time steps but this can be changed
# the people are simulated as walking in the map and the map is a 2D grid

import numpy as np
import random
import math
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import copy
import time

class DiscreTimeSimulationForPeople:
    def __init__(self, map, people, timeStep = 1, maxDistance = 1):
        self.map = map
        self.people = people
        self.timeStep = timeStep
        self.maxDistance = maxDistance
        self.time = 0
        self.timeStep = timeStep
        self.maxDistance = maxDistance
        self.peoplePosition = []
        self.peoplePosition.append(self.people)
        self.peoplePosition.append([])

    def simulate(self, time):
        for i in range(time):
            self.time += 1
            for person in self.people:
                self.movePerson(person)
            self.peoplePosition[self.time % 2] = copy.deepcopy(self.people)
            self.peoplePosition[(self.time + 1) % 2] = []
            self.people = copy.deepcopy(self.peoplePosition[self.time % 2])
            # print("time: ", self.time)
            # print("people: ", self.people)

    def movePerson(self, person):
        x, y = person
        x += random.uniform(-self.maxDistance, self.maxDistance)
        y += random.uniform(-self.maxDistance, self.maxDistance)
        x = max(0, min(self.map[0] - 1, x))
        y = max(0, min(self.map[1] - 1, y))
        person[0] = x
        person[1] = y

    def plot(self):
        fig, ax = plt.subplots()
        ax.set_xlim(0, self.map[0])
        ax.set_ylim(0, self.map[1])
        ims = []
        for i in range(self.time):
            im = ax.scatter([x[0] for x in self.peoplePosition[i % 2]], [x[1] for x in self.peoplePosition[i % 2]])
            ims.append([im])
        ani = animation.ArtistAnimation(fig, ims, interval=100, blit=True, repeat_delay=1000)
        ani.save("people_simulation.mp4")
        #show the animation
        plt.show()

if __name__ == "__main__":
    map = [10, 10]
    people = [[random.randint(0, map[0] - 1), random.randint(0, map[1] - 1)] for i in range(30)]
    simulation = DiscreTimeSimulationForPeople(map, people)
    simulation.simulate(100)
    simulation.plot()
