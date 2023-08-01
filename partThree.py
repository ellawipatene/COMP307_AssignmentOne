import sys
import random

# Global Variables
instances = []

def activationFunc(x):
    if x >= 0:
        return 1
    else:
        return -1

class Instance:
    def __init__(self, inputs, category):
        self.inputs = inputs
        self.category = category
        self.intCategory = 0

        if self.category == "g":
            self.intCategory = 1
        else:
            self.intCategory = -1

class Perceptron:
    def __init__(self, learningRate = 0.1, iterations = 100):
        self.learningRate = learningRate
        self.iterations = iterations
        self.bias = random.uniform(-1,1)

        # Set up the array of weights
        numFeatures = len(instances[0].inputs)
        self.weights = [0 for i in range(numFeatures)]
        for i in range(numFeatures):
            self.weights[i] = random.uniform(-1,1)

    def predict(self, instance):
        sum = 0
        for w in range(len(self.weights)):
            sum += float(instance.inputs[w]) * self.weights[w]
        return activationFunc(sum)

    def trainPerceptron(self, instancesList = instances):
        for _ in range(self.iterations):
            errorCounter = 0
            for i in instancesList:
                target = i.intCategory
                error = target - self.predict(i) 
                if error != 0:
                    errorCounter += 1

                for w in range(len(self.weights)):
                    self.weights[w] += error * float(i.inputs[w]) * self.learningRate     

#Implementation/the main program:
if len(sys.argv) != 2:
    print("Error: wrong number of command line arguments")
    sys.exit(1)

with open(sys.argv[1]) as data:
    next(data) # Skip the header line
    for line in data:
        elements = line.split()
        category = elements[34]
        elements.pop() # Remove the 'Class' value
        instances.append(Instance(elements, category))

perceptron = Perceptron()
perceptron.trainPerceptron()

correctCounter = 0
for i in instances:
    guess = perceptron.predict(i)
    if guess == i.intCategory:
        correctCounter += 1
correctPercentage = correctCounter/len(instances)

print("Number of Correct Predictions: " + str(correctCounter))
print("Percentage of Correct Predictions: " + str(correctPercentage))

print()
print(perceptron.weights)


# FOR QUESTION THREE B ----------------------------------------------

allInstances = instances.copy()
listLen = int(len(allInstances) / 2) + 1
splitInstances = [allInstances[i:i + listLen] for i in range(0, len(allInstances), listLen)]
trainingData = splitInstances[0]
testingData = splitInstances[1]

perceptronTwo = Perceptron()
perceptronTwo.trainPerceptron(trainingData)

correctCounter = 0
for i in testingData:
    guess = perceptronTwo.predict(i)
    if guess == i.intCategory:
        correctCounter += 1
correctPercentage = correctCounter/len(testingData)

print()
print("Outcomes for split data: ")
print("Number of Correct Predictions: " + str(correctCounter))
print("Percentage of Correct Predictions: " + str(correctPercentage))





