import numpy as np
import time

NUM_PIXELS = 16 * 16

train_pixels, train_labels = [], []
test_pixels, test_labels = [], []
temp_pixels = []

try:
    with open("traindata.txt") as traindata:
        for trainline in traindata:
            if "1" in trainline or "0" in trainline:
                for num in trainline[:NUM_PIXELS]:
                    temp_pixels.append(int(num))
                train_pixels.append(temp_pixels)
                temp_pixels = []
                train_labels.append(int(trainline[NUM_PIXELS]))
except FileNotFoundError:
    print("No training data found, assuming weights and bias will be given")

try:
    with open("testdata.txt") as testdata:
        for testline in testdata:
            if "1" in testline or "0" in testline:
                for num2 in testline[:NUM_PIXELS]:
                    temp_pixels.append(int(num2))
                test_pixels.append(temp_pixels)
                temp_pixels = []
                test_labels.append(int(testline[NUM_PIXELS]))
except FileNotFoundError:
    print("No test data found, will not be able to test accuracy of model after training")

train_pixels = np.array(train_pixels)
train_labels = np.array(train_labels)
test_pixels = np.array(test_pixels)
test_labels = np.array(test_labels)

def init_params(w1, B1, w2, B2, w3, B3):
    
    W1 = w1
    b1 = B1
    W2 = w2
    b2 = B2
    W3 = w3
    b3 = B3
    
    if type(w1) == str:
        W1 = np.random.rand(NUM_PIXELS, NUM_PIXELS) - 0.5
    if type(B1) == str:
        b1 = np.random.rand(NUM_PIXELS, 1) - 0.5
        
    if type(w2) == str:
        W2 = np.random.rand(NUM_PIXELS, NUM_PIXELS) - 0.5
    if type(B2) == str:
        b2 = np.random.rand(NUM_PIXELS, 1) - 0.5
        
    if type(w3) == str:
        W3 = np.random.rand(NUM_PIXELS, 10) - 0.5
    if type(B3) == str:
        b3 = np.random.rand(10, 1) - 0.5
    
    return W1, b1, W2, b2, W3, b3

def forward_prop(W1, b1, W2, b2, W3, b3, pixels):
    
    Z1 = np.dot(W1, pixels.T) + b1
    A1 = np.maximum(0, Z1)
    
    Z2 = np.dot(W2, A1) + b2
    A2 = np.maximum(0, Z2)
    
    Z3 = np.dot(W3.T, A2) + b3
    A3 = np.exp(Z3) / sum(np.exp(Z3))
    
    return Z1, A1, Z2, A2, Z3, A3
    
def one_hot(Y):
    one_hot_Y = np.zeros((Y.size, Y.max() + 1))
    one_hot_Y[np.arange(Y.size), Y] = 1
    return one_hot_Y.T

def backward_prop(Z1, A1, Z2, A2, Z3, A3, W1, W2, W3, pixels, Y):
    
    I_Y = one_hot(Y)
    
    dZ3 = A3 - I_Y
    dW3 = 1 / len(pixels.T) * np.dot(dZ3, A2.T)
    db3 = 1 / len(pixels.T) * np.sum(dZ3)
    
    dZ2 = np.dot(W3, dZ3) * (Z2 > 0)
    dW2 = 1 / len(pixels.T) * np.dot(dZ2, A1.T)
    db2 = 1 / len(pixels.T) * np.sum(dZ2)
    
    dZ1 = np.dot(W2.T, dZ2) * (Z1 > 0)
    dW1 = 1 / len(pixels.T) * np.dot(dZ1, pixels)
    db1 = 1 / len(pixels.T) * np.sum(dZ1)
    
    return dW1, db1, dW2, db2, dW3, db3

def update_params(W1, b1, W2, b2, W3, b3, dW1, db1, dW2, db2, dW3, db3, learning_rate):
    
    W1 = W1 - learning_rate * dW1
    b1 = b1 - learning_rate * db1
    
    W2 = W2 - learning_rate * dW2
    b2 = b2 - learning_rate * db2
    
    W3 = W3 - learning_rate * dW3.T
    b3 = b3 - learning_rate * db3
    
    return W1, b1, W2, b2, W3, b3

def accuracy(predictions, tests):
    return np.mean(predictions == tests)

def predict_tests(tests, W1, b1, W2, b2, W3, b3):
    _, _, _, _, _, A3 = forward_prop(W1, b1, W2, b2, W3, b3, tests)
    return np.argmax(A3, 0)

def train(params, train_pixels, train_labels, learning_rate=0.01, itercount=1000):
    W1, b1, W2, b2, W3, b3 = params
    for i in range(itercount):
        Z1, A1, Z2, A2, Z3, A3 = forward_prop(W1, b1, W2, b2, W3, b3, train_pixels)
        dW1, db1, dW2, db2, dW3, db3 = backward_prop(Z1, A1, Z2, A2, Z3, A3, W1, W2, W3, train_pixels, train_labels)
        W1, b1, W2, b2, W3, b3 = update_params(W1, b1, W2, b2, W3, b3, dW1, db1, dW2, db2, dW3, db3, learning_rate)
        if i % (itercount//10) == 0:
            print(f"Iteration {i} trained, ({(i/itercount)*100}% done)")
    return W1, b1, W2, b2, W3, b3


a = input("How many training iterations? (default 1000): ")
if a == "":
    a = 1000
try:
    a = int(a)
except:
    print("Invalid input, using default (1000 iterations)")
    a = 1000
b = input("What is the learning rate (default: 0.01): ")
if b == "":
    b = 0.01
try:
    b = float(b)
except:
    print("Invalid input, using default (0.01 learning rate)")
    b = 0.01

def wb_file_input(inputtxt:str, default, shape:tuple, shapefix:bool = False):
    a = input(inputtxt)
    if a == "":
        a = default
    if ".txt" not in a:
        a += ".txt"
    try:
        a = np.loadtxt(a, dtype = float)
        if shapefix:
            a = a.reshape(shape)
        if (a.shape == shape):
            return a
        print("Shape of file does not match, will create new one for training")
        return "None"
    except FileNotFoundError:
        print("File not found, will create new one for training")
        return "None"
    
weightcheck = input("Do you want to use weights and biases from existing files? (press enter for no, anything else for yes): ")

if weightcheck in {"", "no", "n", "No", "N", "NO", "nO"}:
    w1 = "None"
    w2 = "None"
    w3 = "None"
    B1 = "None"
    B2 = "None"
    B3 = "None"
else:
    w1 = wb_file_input("Weights 1 file name? (default: W1.txt):", "W1.txt", (NUM_PIXELS, NUM_PIXELS))
    w2 = wb_file_input("Weights 2 file name? (default: W2.txt):", "W2.txt", (NUM_PIXELS, NUM_PIXELS))
    w3 = wb_file_input("Weights 3 file name? (default: W3.txt):", "W3.txt", (NUM_PIXELS, 10))
    
    B1 = wb_file_input("Biases 1 file name? (default: b1.txt):", "b1.txt", (NUM_PIXELS, 1), True)
    B2 = wb_file_input("Biases 2 file name? (default: b2.txt):", "b2.txt", (NUM_PIXELS, 1), True)
    B3 = wb_file_input("Biases 3 file name? (default: b3.txt):", "b3.txt", (10, 1), True)

params = init_params(w1, B1, w2, B2, w3, B3)

start = time.time()
W1, b1, W2, b2, W3, b3 = train(params, train_pixels, train_labels, b, a)
timer = round(time.time() - start, 2)
print(f"Training with {a} iterations, {b} learning rate and {len(train_labels)} data sources complete (took {timer} seconds, {round(timer/a, 4)}s per iteration on average)")


predictions = predict_tests(test_pixels, W1, b1, W2, b2, W3, b3)
acc = accuracy(predictions, test_labels)


print("----------------------------------------------------------------------------------------------------")
print(f"Answers:     {test_labels}")
print(f"Predictions: {predictions}")
print("Accuracy: " + str(round(acc*100, 2)) + "% with " + str(len(test_labels)) + " predictions")
print("----------------------------------------------------------------------------------------------------")

np.savetxt("W1.txt", W1)
np.savetxt("W2.txt", W2)
np.savetxt("W3.txt", W3)
np.savetxt("b1.txt", b1)
np.savetxt("b2.txt", b2)
np.savetxt("b3.txt", b3)

print("Saved weights and biases to W1.txt, W2.txt, W3.txt, b1.txt, b2.txt and b3.txt (respectively)")