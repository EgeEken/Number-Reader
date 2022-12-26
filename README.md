# Number Reader
An AI program that can be trained to read numbers on a 16x16 black and white image.

### Requirements:
- Python (should probably work with anything over Python 3.6, but definitely not an older version)
- PyGame library (if not installed, go on cmd/terminal and write "pip install pygame")
- NumPy library (same as above, "pip install numpy")
- Art skills of a 3 year old if you are planning on creating your own dataset (if you dont have it, you could try practicing on paint)

To create your own training/testing dataset, you can use the BinaryImage.py program, controls and instructions for the program are listed below:

- [Left Click] to draw
- [Backspace, CTRL or Z] to erase current drawing and restart in case of an error
- [Enter or Space] to submit current drawing into the data set
- [Escape] to quit the program prematurely (your progress will be saved in traindata.txt and testdata.txt given that you made it there)
- The first half of the drawings will be training data, the second half will be used for testing
- You have to draw the number you see on the top left

Once you have your training and testing data, you can use NumberReader.py to train your AI and calculate the weights and the bias, which will be saved in the files "weights.txt" and "bias.txt", i would recommend changing the file names before continuing to create new models as they will be overwritten in new training sessions. It will also ask you for the iteration count and learning rate, which default to 1000 and 0.01 respectively, i wouldn't recommend changing the learning rate unless you know what you're doing, and if you do know what you're doing, you can find my results from testing various learning rates with the same amount of iterations and the same data set below, but 1000 is supposed to be a relatively small number of iterations, so feel free to increase that.

<details><summary>Learning rate test results: (click here to open)</summary>
<p>

<img width="472" alt="image" src="https://user-images.githubusercontent.com/96302110/209546184-a95e89fd-1bca-4bcb-836b-9cf812861a41.png">

</p>
</details>

If you don't plan on creating your own training and testing data, i included the weights and bias for a 110k iteration training session using a 400+ image training data set, and also a test dataset of 200+ images to predict. You can use those in NumberReader.py, and INPUTNumberReader.py if you want to input your own test images on the spot instead of using the given set.

Admittedly, the accuracy of this model is far from ideal, achieving only a 16.99% accuracy with the testing set i provided. While that's still better than the 10% you would expect from a completely untrained, random model, I will update this repository with better weights and biases later on, so stay tuned.
