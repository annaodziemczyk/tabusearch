from copy import deepcopy

class TabuSearch:

    jobs = None
    bestCandidate = []
    maxTabuSize = 0
    noOfIterations = 0

    def __init__(self, jobs, bestcandidate, maxtabusize, iterations):
        self.jobs = jobs
        self.bestCandidate = bestcandidate
        self.maxTabuSize = maxtabusize
        self.noOfIterations = iterations

    def start(self):
        bestSolution = self.bestCandidate
        print("Current best solution: " + str(bestSolution) + "(" + str(self.averageTardiness(bestSolution)) + ")")
        tabuList = []
        tabuList.append(self.bestCandidate)

        for iterationCount in range(0, self.noOfIterations):
            neighborhood = self.findNeighbours(self.bestCandidate)
            for candidate in neighborhood:
                if (candidate not in tabuList) and (self.averageTardiness(candidate) < self.averageTardiness(self.bestCandidate)):
                    self.bestCandidate = candidate

            if self.averageTardiness(self.bestCandidate) < self.averageTardiness(bestSolution):
                bestSolution = self.bestCandidate
                print("Current best solution: " + str(bestSolution) + "(" + str(self.averageTardiness(bestSolution)) + ")")

            tabuList.append(self.bestCandidate)
            if len(tabuList) > self.maxTabuSize:
                del tabuList[0]

        return bestSolution


    def findNeighbours(self, items):
        neighbours = []
        for index in range(0, len(items)-1):
            neighbours.append(self.swap(deepcopy(items), index, index+1))

        return neighbours

    def swap(self, list, pos1, pos2):
        list[pos1], list[pos2] = list[pos2], list[pos1]
        return list

    def averageTardiness(self, candidatesolution):
        avgTardiness = 0
        starttime = 0
        for jobName in candidatesolution:
            job = self.jobs[str(jobName)]
            completionTime = starttime + job.processingTime
            tardiness = completionTime - job.dueTime
            if tardiness > 0:
                avgTardiness += tardiness * job.penality
            starttime = completionTime

        return avgTardiness


class Job:
    name = ''
    processingTime = None
    dueTime = None
    penality = None

    def __init__(self, name, processing, due, penality):
        self.name = name
        self.processingTime = processing
        self.dueTime = due
        self.penality = penality

    def __str__(self):
        return str(self.name)


if __name__ == "__main__":

    jobs = {
        "1":Job(str(1), 9, 10, 14),
        "2":Job(str(2), 9, 8, 12),
        "3":Job(str(3), 12, 5, 1),
        "4":Job(str(4), 3, 28, 12)
    }

    search = TabuSearch(jobs, [3, 1, 4, 2], 2, 2000)
    bestSolution = search.start()
    print("Current best solution: " + str(bestSolution))





