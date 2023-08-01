import sys
import math
import random

#Fields:
minList = list()
maxList = list()

# Fields for Cross Fold
allWines = []
allNormalizedWines = []
kFolds = 5

trainingPredictions = []
testingPredictions = []

currentTestingWines = []
currentTrainingWines = []

#Wine class - Holds the attributes of the wine:
class Wine:
    def __init__(self, inputs, category):
                self.inputs = inputs
                self.category = int(category)

# Functions for the k Cross Fold:
def shuffleInstances():
    random.shuffle(allNormalizedWines)

def splitLists():
    allWinesCopy = allNormalizedWines.copy()
    listLen = int(len(allWinesCopy) / kFolds) + 1
    return [allWinesCopy[i:i + listLen] for i in range(0, len(allWinesCopy), listLen)]

# Functions for kNN calculations:

# Find the minimum value for each collumn
def getMin(index):
    min = sys.float_info.max
    for wine in allWines:
        if float(wine.inputs[index]) < min:
            min = float(wine.inputs[index])
    return min

# Return the max value for each collumn
def getMax(index):
    max = sys.float_info.min
    for wine in allWines:
        if float(wine.inputs[index]) > max:
            max = float(wine.inputs[index])
    return max

def normalizeAllData():
    for wine in allWines:
        elements = list()
        for i in range(0,13):
            elements.append((float(wine.inputs[i]) - minList[i])/(maxList[i] - minList[i]))
        allNormalizedWines.append(Wine(elements, wine.category))

# Calculate the euclidean distance between 2 different wines
def getEuclideanDist(wine1, wine2):
    dist = 0.0
    for i in range (len(wine1.inputs)):
        dist += (float(wine1.inputs[i]) - float(wine2.inputs[i]))**2
    return math.sqrt(dist)

# Calculate all of the distances and sort them 
def getDistances(testWine):
    distances = list()
    for wine in currentTrainingWines:
        dist = getEuclideanDist(wine, testWine)
        distances.append((wine, dist)) # Save them as a pair/2D array
    distances.sort(key=lambda w: w[1])
    return distances

# Return the relevant amount of neighbours
def getNeighbours(distances, k):
    kNeighbours = list()
    for i in range(k):
        kNeighbours.append(distances[i][0])
    return kNeighbours

# Returns the class that the program believes the test belongs to
def getPrediction(testWine, k):
    neighbours = getNeighbours(getDistances(testWine), k)
    votes = [0,0,0]
    for n in neighbours:
        votes[int(n.category) - 1] = int(votes[int(n.category) - 1]) + 1
    if votes[0] > votes[1] and votes[0] > votes[2]: return 1
    elif votes[1] > votes[0] and votes[1] > votes[2]:return 2
    else: return 3

#Implementation/the main program:
if len(sys.argv) != 3:
    print("Error: wrong number of command line arguments")
    sys.exit(1)

# Load in the 'wine-training' dataset
with open(sys.argv[1]) as trainingSet:
    next(trainingSet) # Skip the headers line
    for line in trainingSet:
        elements = line.split()
        category = elements[13]
        elements.pop()
        allWines.append(Wine(elements, category))      

# Load in the 'wine-test' dataset
with open(sys.argv[2]) as testingSet:
    next(testingSet)
    for line in testingSet:
        elements = line.split()
        category = elements[13]
        elements.pop()
        allWines.append(Wine(elements, category))

# Get the minimum and maximum values for each column         
for i in range(0,13):
    minList.append(getMin(i))
    maxList.append(getMax(i))

print(minList)
print(maxList)

# Normalize all of the testing and training data
normalizeAllData()

# kFold Cross
shuffleInstances()
foldsList = splitLists()

for i in range(kFolds):
    currentTestingWines = foldsList[i]
    currentTrainingWines = [j for j in allNormalizedWines if j not in currentTestingWines]

    correctCounter = 0
    currentList = list()
    for wine in currentTestingWines:
        categoryPrediction = getPrediction(wine, 3)
        currentList.append(categoryPrediction)
        if categoryPrediction == wine.category:
            correctCounter += 1

    print(correctCounter)
    print(str(len(currentTestingWines)))
    
    accuracy = correctCounter/len(currentTestingWines)
    testingPredictions.append(accuracy)

    print(accuracy)
    print()

meanScore = sum(testingPredictions) / kFolds
print(meanScore)


