# Number Reader
An AI program that can be trained to read numbers on a 16x16 black and white image. This program does not use any ai-specific libraries that are made to simplify the process of creating an ai model, since I wanted to learn how the fundamentals work first, so it only uses numpy for simple mathematical functions like dot products  and array mapping etc. 

![ai results](https://user-images.githubusercontent.com/96302110/213899417-5ee56354-d802-43ed-9941-cb3d1024b2bc.gif)

### Requirements:
- Python (should probably work with anything over Python 3.6, but definitely not an older version)
- PyGame library (if not installed, go on cmd/terminal and write "pip install pygame")
- NumPy library (same as above, "pip install numpy")
- Art skills of a 3 year old

You can use INPUTNumberReader.py to have the program predict what youre drawing once you submit the drawing, and to create your own training/testing dataset or add to the provided one, you can use the BinaryImage.py program, controls and instructions for the program are listed below:

- [Left Click] to draw
- [Backspace, CTRL or Z] to erase current drawing and restart in case of an error
- [Enter or Space] to submit current drawing into the data set
- [Escape] to quit the program prematurely (your progress will be saved in traindata.txt and testdata.txt given that you made it there)
- The first half of the drawings will be training data, the second half will be used for testing
- You have to draw the number you see on the top left

Once you have your training and testing data, you can use TRAINNumberReader.py to train your AI and calculate the weights and the bias, which will be saved in the files "weights.txt" and "bias.txt", i would recommend changing the file names before continuing to create new models as they will be overwritten in new training sessions. It will also ask you for the iteration count and learning rate, which default to 1000 and 0.01 respectively, i wouldn't recommend changing the learning rate unless you know what you're doing, but 1000 is supposed to be a relatively small number of iterations, so feel free to increase that.

If you don't plan on creating your own training and testing data, i included the weights and bias for a 110k iteration training session using a 1000 image training data set, and also a testing set of 200+ labeled images to predict. You can use those in TRAINNumberReader.py, and INPUTNumberReader.py if you want to input your own test images on the spot instead of using the given set.

### Weights updates:
- V0.1: 431 image dataset, 110,000+ iterations, 0.01 learning rate, 16.99% accuracy
- V0.2: 650 image dataset, 11,000+ iterations, 0.011 learning rate, 17.96% accuracy
- V0.3: 1000 image dataset, 10,000+ iterations, 0.01 learning rate, 14.56% accuracy
 At this point i did some more research to find why the accuracy was not improving, and i found out that the model i had created was actually not doing great because it only had a single layer of neurons, which makes it a Linear Classifier, as opposed to a Neural Network which would be much more useful in this task where we analyze images, so i made a 2 layer neural network version of it.
- V1: 1000 image dataset neural network, 10,000+ iterations, 0.01 learning rate, 83.01% accuracy
