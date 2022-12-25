import numpy as np
import time
import os

NUM_PIXELS = 16 * 16

train_pixels = []
train_labels = []
test_pixels = []
test_labels = []
temp_pixels = []

with open("traindata.txt") as traindata:
    for trainline in traindata:
        if "1" in trainline or "0" in trainline:
            for num in trainline[:NUM_PIXELS]:
                temp_pixels.append(int(num))
            train_pixels.append(temp_pixels)
            temp_pixels = []
            train_labels.append(int(trainline[NUM_PIXELS]))

with open("testdata.txt") as testdata:
    for testline in testdata:
        if "1" in testline or "0" in testline:
            for num2 in testline[:NUM_PIXELS]:
                temp_pixels.append(int(num2))
            test_pixels.append(temp_pixels)
            temp_pixels = []
            test_labels.append(int(testline[NUM_PIXELS]))

def train(pixels, labels, learning_rate = 0.01, itercount = 1000):
    weights = np.zeros(NUM_PIXELS)
    bias = 0

    changeweights = -1
    changebias = -1

    for i in range(itercount):
        if i/itercount * 100 % 5 == 0:
            print(f"Training iteration {i} / {itercount}, ({i / itercount * 100}% complete)")
            try:
                if all(changeweights == weights) and (changebias == bias):
                    print(f"No change in weights or bias in the last {itercount//20} iterations, stopping training at iteration {i}")
                    return np.array(weights), bias, i
            except:
                if changeweights == weights and changebias == bias:
                    print(f"No change in weights or bias in the last {itercount//20} iterations, stopping training at iteration {i}")
                    return np.array(weights), bias, i
            changeweights = weights
            changebias = bias
        for j in range(len(pixels)):
            prediction = np.dot(weights, pixels[j]) + bias

            error = labels[j] - prediction

            wtemp = list(map(lambda x: x * learning_rate * error, pixels[j]))
            weights = list(map(lambda x, y: x + y, weights, wtemp))
            bias += learning_rate * error
    
    return np.array(weights), bias, itercount

def continuetrain(pixels, labels, w, b, learning_rate = 0.01, itercount = 1000):
    weights = w
    bias = b

    changeweights = -1
    changebias = -1

    for i in range(itercount):
        if i/itercount * 100 % 5 == 0:
            print(f"Training iteration {i} / {itercount}, ({i / itercount * 100}% complete)")
            try:
                if all(changeweights == weights) and (changebias == bias):
                    print(f"No change in weights or bias in the last {itercount//20} iterations, stopping training at iteration {i}")
                    return np.array(weights), bias, i
            except:
                if changeweights == weights and changebias == bias:
                    print(f"No change in weights or bias in the last {itercount//20} iterations, stopping training at iteration {i}")
                    return np.array(weights), bias, i
            changeweights = weights
            changebias = bias

        for j in range(len(pixels)):
            prediction = np.dot(weights, pixels[j]) + bias

            error = labels[j] - prediction

            wtemp = list(map(lambda x: x * learning_rate * error, pixels[j]))
            weights = list(map(lambda x, y: x + y, weights, wtemp))
            bias += learning_rate * error
    
    return np.array(weights), bias, itercount

def predict(pixels, weights, bias):
    predictions = np.zeros(len(pixels))

    for i in range(len(pixels)):
        prediction = np.dot(weights, pixels[i]) + bias
        predictions[i] = prediction

    return [int(round(pred)) for pred in predictions]


b = input("Is there a weights file to load? (if so, whats the filename? leave empty if no): ")
if b in {"default", "yes", "y", "weights"}:
    b = "weights.txt"
    weights = np.loadtxt(b, dtype = float)
bpass = True
if b:
    bpass = False
    try:
        weights = np.loadtxt(b, dtype = float)
        b = input("What is the bias file filename? (default: bias.txt): ")
        try:
            with open(b) as biasfile:
                bias = float(biasfile.readlines()[0])
        except:
            try:
                with open("bias.txt") as biasfile:
                    bias = float(biasfile.readlines()[0])
            except:
                print("Bias file not found, using 0 as bias")
                bias = 0
    except:
        print("Weights file not found, training new classifier")
        bpass = True

cont = 0
if not bpass:
    cont = input("Continue training? (default: no): ")
    if cont not in {"no", "n", "stop", "default", "", "0"}:
        bpass = True
        cont = "cont"

if bpass:
    a = input("How many training iterations? (default 1000): ")

    try:
        a = int(a)
    except:
        print("Invalid input, using default (1000 iterations")
        a = 1000

    c = input("What is the learning rate (default: 0.01): ")

    try:
        c = float(c)
    except:
        print("Invalid input, using default (0.01 learning rate)")
        c = 1000

    start = time.time()
    if cont == "cont":
        weights, bias, itercount = continuetrain(train_pixels, train_labels, weights, bias, c, a)
    else:
        weights, bias, itercount = train(train_pixels, train_labels, c, a)

    print("----------------------------------------------------------------------------------------------------")
    print(f"Training with {len(train_labels)} data sources and {itercount} iterations complete after {round((time.time() - start), 2)} seconds!")
    print("----------------------------------------------------------------------------------------------------")

    with open("results.txt", "a") as weightsfile:
        weightsfile.write("----------------------------------------------------------------------------------------------------")
        weightsfile.write(os.linesep)
        weightsfile.write("Weights for " + str(len(train_labels)) + " data sources and " + str(itercount) + " iterations:")
        weightsfile.write(os.linesep)
        weightsfile.write(str(weights))
        weightsfile.write(os.linesep)
        weightsfile.write("Bias for " + str(len(train_labels)) + " data sources and " + str(itercount) + " iterations:")
        weightsfile.write(os.linesep)
        weightsfile.write(str(bias))
        weightsfile.write(os.linesep)
        weightsfile.write("----------------------------------------------------------------------------------------------------")
        weightsfile.close()

    np.savetxt("weights.txt", weights, fmt = "%s")

    with open("bias.txt", "w") as bf:
        bf.write(str(bias))
        bf.close()

    print(f"Weights (saved in weights.txt): {weights}")
    print(f"Bias (saved in bias.txt): {bias}")

predictions = predict(test_pixels, weights, bias)

print("----------------------------------------------------------------------------------------------------")
print(f"Answers:     {test_labels}")
print(f"Predictions: {predictions}")

accuracy = np.mean(list(map(lambda x, y: int(x == y), predictions, test_labels)))
print("Accuracy: " + str(round(accuracy*100, 2)) + "% with " + str(len(test_labels)) + " predictions")
print("----------------------------------------------------------------------------------------------------")

