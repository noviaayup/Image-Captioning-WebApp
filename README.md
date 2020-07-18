# Image-Captioning-WebApp

Image-Captioning-WebApp is a application that provides details about images feed into it and reads them out.

## Installation

Install all the dependencies mentioned in requirement.txt.
Change the directory to the current folder on powershell (Windows).

## Usage

```bash
python caption.py
```
1. Go to https:// 127.0.0.1:5000/image-caption/ on web browser.
2. Upload the required Image.
3. Wait for the image to be processed.

## Working

The image (jpg format) is uploaded in the web app, which is sent to the backend
deep learning model to convert images to text. The text describing the images is then
read out so that a person can understand it.

## Model Representation

![alt text](https://github.com/Harsh5557/Image-Captioning-WebApp/blob/master/static/img/paper.png)

## Deep Learning Model

Used a subset of 30,000 captions from the MS-COCO dataset and their
corresponding images to train our model.
Choosing more data would result in improved captioning quality.
Used InceptionV3 (which is pre-trained on Imagenet) to classify each image.
Limited the vocabulary size to the top 5,000 words (to save memory). Replaced all
other words with the token "UNK" (unknown).

## Model Details

● Extracted the image features from the lower convolutional layer of
InceptionV3 giving us a vector of shape (8, 8, 2048).  
● Then squashed that to the shape of (64, 2048).  
● This vector is then passed through the CNN Encoder (which consists of a single
Fully connected layer).  
● The RNN (here GRU) attends over the image to predict the next word.

## Example

![alt text](https://github.com/Harsh5557/Image-Captioning-WebApp/blob/master/static/img/Cattle.JPG)

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.
