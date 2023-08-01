import sys

# Global Variables:
instances = []
attributes = []
remainingAttributes = []

testingInstances = []

baseLinePredictor = None
root = None

class Instance:
    def __init__(self, category, inputs):
        self.category = category
        self.inputs = inputs # a list of boolean vars

class Node:
    def __init__(self, attribute, left, right, category = None, probability = None, isLeaf = False):
        self.attribute = attribute
        self.left = left
        self.right = right

        self.category = category
        self.probability = probability
        self.isLeaf = isLeaf

    def report(self, indent = ""):
        if self.isLeaf:
            if self.probability == 0: # For testing purposes
                print(indent + " Unknown")
            else:
                print(indent + " Class: " + self.category + ", Probability: " + str(self.probability))
        else:
            print(indent + self.attribute + " = True")
            self.left.report(indent + "   ")
            print(indent + self.attribute + " = False")
            self.right.report(indent + "   ")

class DecisionTree:
    def __init__(self, maxDepth):
        self.root = None
        self.maxDepth = maxDepth

def calcWeightedImpurity(trueInstances, falseInstances):
    trueLiveCounter = 0
    falseLiveCounter = 0
    for i in trueInstances:
        if i.category == "live":
            trueLiveCounter += 1
    for i in falseInstances:
        if i.category == "live":
            falseLiveCounter += 1

    truePBI = 0
    falsePBI = 0
    totalInstances = len(trueInstances) + len(falseInstances)
    if trueLiveCounter != 0:
        truePBI = (trueLiveCounter * (len(trueInstances) - trueLiveCounter))/((trueLiveCounter + (len(trueInstances) - trueLiveCounter))**2)
    if falseLiveCounter != 0:
        falsePBI = (falseLiveCounter * (len(falseInstances) - falseLiveCounter))/((falseLiveCounter + (len(falseInstances) - falseLiveCounter))**2)

    wAvgPBI = (len(trueInstances)/totalInstances) * truePBI + (len(falseInstances)/totalInstances) * falsePBI
    return wAvgPBI
    

# Find the attribute that will return a node with the lowest impurity
def findBestAttribute(passedInstances):
    bestAtt = remainingAttributes[0]
    bestInstsTrue = list()
    bestInstsFalse = list()
    minImpurity = 10000.0

    for a in remainingAttributes:
        trueInstances = list()
        falseInstances = list()
        for i in passedInstances:
            if i.inputs[attributes.index(a)] == "true":
                trueInstances.append(i)
            else:
                falseInstances.append(i)

        weightedAverageImpurity = calcWeightedImpurity(trueInstances, falseInstances)

        if minImpurity > weightedAverageImpurity:
            minImpurity = weightedAverageImpurity
            bestAtt = a
            bestInstsTrue = trueInstances
            bestInstsFalse = falseInstances
        
    remainingAttributes.remove(bestAtt)
    left = buildTree(bestInstsTrue, remainingAttributes)
    right = buildTree(bestInstsFalse, remainingAttributes)

    return Node(bestAtt, left, right)

def getBaseLinePredictor(instancesList):
    liveCount = 0
    for i in instancesList:
        if(i.category == "live"): 
            liveCount += 1
    if(liveCount > len(instancesList) - liveCount): 
        return Node("LIVE", None, None, "live", liveCount/len(instancesList), True)
    else: 
        return Node("LIVE", None, None, "die", (len(instancesList) - liveCount)/len(instancesList), True)

def checkInstancesPurity(remainingInstances):
    alive = remainingInstances[0].category
    for i in remainingInstances:
        if i.category != alive:
            return False
    return True     

def buildTree(remainingInstances, remainingAttributes):
    if len(remainingInstances) == 0:
        return getBaseLinePredictor(instances.copy())
    elif checkInstancesPurity(remainingInstances):
        alive = remainingInstances[0].category
        return Node(alive, None, None, alive, 1, True)
    elif len(remainingAttributes) == 0:
        return getBaseLinePredictor(remainingInstances)
    else:
        return findBestAttribute(remainingInstances)

def getPrediction(testInstance):
    currentNode = root
    while True:
        if currentNode.isLeaf:
            break
        attribute = currentNode.attribute
        attributeIndex = attributes.index(attribute)
        boolVal = testInstance.inputs[attributeIndex]
        if boolVal == "true":
            currentNode = currentNode.left
        else:
            currentNode = currentNode.right
    return currentNode.category
   
#Implementation/the main program:
if len(sys.argv) != 3:
    print("Error: wrong number of command line arguments")
    sys.exit(1)

# Load in the 'hepatitis-training' dataset
with open(sys.argv[1]) as trainingSet:
    for line in trainingSet:
        elements = line.split()
        if len(attributes) == 0:
            elements.pop(0) # Remove the 'Class' header
            attributes = elements
        else:
            category = elements[0] 
            elements.pop(0) # Remove the 'Class' value
            instances.append(Instance(category, elements)) 

with open(sys.argv[2]) as testingSet:
    next(testingSet) # Skip the header line
    for line in testingSet:
        elements = line.split()
        category = elements[0]
        elements.pop(0) # Remove the 'Class' value
        testingInstances.append(Instance(category, elements))

remainingAttributes = attributes.copy()
root = buildTree(instances, attributes)

root.report(" ")
print()

correctCounter = 0
for i in testingInstances:
    prediction = getPrediction(i)
    if prediction == i.category:
        correctCounter += 1


print("Correct Counter: " + str(correctCounter))
print("Length of all Instances: " + str(len(testingInstances)))
print("Accuracy Percentage: " + str(correctCounter/len(testingInstances)))
print()

# Baseline predictor outcome:
baseLinePredictorCategory = getBaseLinePredictor(instances).category
baseLineCounter = 0
for i in instances:
    if baseLinePredictorCategory == i.category:
        baseLineCounter += 1

print("Correct Base Line Counter: " + str(correctCounter))
print("Length of all instances: " + str(len(testingInstances)))
print("Base Line Accuracy Percentage: " + str(correctCounter/len(testingInstances)))

    







