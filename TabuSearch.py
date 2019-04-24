from copy import deepcopy

class TabuSearch:

    jobs = None
    bestCandidate = []
    maxTabuSize = 0
    noOfIterations = 0
    noOfMachines = 1

    def __init__(self, jobs, bestcandidate, maxtabusize, machines, iterations):
        self.jobs = jobs
        self.bestCandidate = bestcandidate
        self.maxTabuSize = maxtabusize
        self.noOfIterations = iterations
        self.noOfMachines = machines

    def start(self):
        bestSolution = self.bestCandidate
        print("Current best solution: " + str(bestSolution) + "(" + str(self.averageTardiness(bestSolution)) + ")")
        tabuList = []
        tabuList.append(self.bestCandidate)

        #stopping condition for the search is the specified number of interations
        for iterationCount in range(0, self.noOfIterations):
            #minimizing tardiness by trying to find a neighbour that is less tardy that the current best solution
            neighborhood = self.findNeighbours(self.bestCandidate)
            for candidate in neighborhood:
                if (candidate not in tabuList) and (self.averageTardiness(candidate) < self.averageTardiness(self.bestCandidate)):
                    self.bestCandidate = candidate

            if self.averageTardiness(self.bestCandidate) < self.averageTardiness(bestSolution):
                bestSolution = self.bestCandidate
                print("Current best solution: " + str(bestSolution) + "(" + str(self.averageTardiness(bestSolution)) + ")")

            tabuList.append(self.bestCandidate)
            #making sure we keep in memory only search list of the specified size
            if len(tabuList) > self.maxTabuSize:
                del tabuList[0]

        return bestSolution

    #we're finding neighbours through adajent pairwaise interchanges
    def findNeighbours(self, items):
        neighbours = []
        for index in range(0, len(items)-1):
            neighbours.append(self.swap(deepcopy(items), index, index+1))

        return neighbours

    #swap adajent items in find new neighbour
    def swap(self, list, pos1, pos2):
        list[pos1], list[pos2] = list[pos2], list[pos1]
        return list

    def averageTardiness(self, candidatesolution):
        avgTardiness = 0
        starttime = 0
        #calculate tardiness for each job in the candidate solution
        for jobName in candidatesolution:
            job = self.jobs[str(jobName)]
            # the job is complete after it finishes executing on last machine
            # the job cannot start on next machine until it finishes execution on previous machine
            # resulting in increased processing time
            completionTime = starttime + self.noOfMachines*job.processingTime
            tardiness = completionTime - job.dueTime
            #if job is tardy, apply penality
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

    search = TabuSearch(jobs, [3, 1, 4, 2], 2, 3, 2000)
    bestSolution = search.start()
    print("Current best solution: " + str(bestSolution))





