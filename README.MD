# Google Scholar Data Mining

## Description

The purpose of the this project is to investigate the underlying phenomenons such as gender imbalance in academia via analyzing a vast amount of data crawled from Google Scholar. 

The codes consists of 
* data collection
* data cleaning
* gender determination
* data analysis

## Conclusion

Male researchers are dominant in most disciplines and much more competitve in academic impact, which was observed by the analysis of different academic performance measures such as h-index, citation quantities and publication number. Besides, it seems that male researchers are more likely to cooperate with other researchers.

## How to reproduce the project
Since parts of the codes depend on others' work here I just give brief guidance on how to reporduce the outcomes.

### A.0 Directory Structure

*	data-collection. The directory contains all the codes of the Node.js crawler and cleaning scripts.
*	data-analysis. The directory consists of various Python scripts that used to generate different charts and get concrete number during analysis.
*	image-base-gender-imputation. The directory contains different code files about the portrait-based model for gender determination
*	text-based-gender-imputation. This directory contains all the Python scripts about name-based model including the scripts of different experiments on machine learning algorithms.
ensemble. The directory is about the codes of the ensemble model including cross validation and gender inference.


### A.1 Crawler
#### A.1.1 Installation

Go to this [link](https://nodejs.org/en/) and download the Node.js and make sure the version is 7.0 or above.

Download the NPM from [here](https://www.npmjs.com/)

Globally Install Gulp via “npm install –g gulp”

CD into the data-collection directory and run “npm install” 

The above command will install all dependencies and libraries automatically

Install MongoDB 3.4 or above version from [here](https://www.mongodb.com/download-center) 

Run MongoDB at port 27018 and make sure the database name is GoogleScholar or you can also modify the config.json to meet personal requirements

modify the config.json as you wish

#### A.1.2 Run the crawler

All the below commands require data-collection as the current directory

Keep the MongoDB running

Check the gulp.js and change the parameters of the functions as you wish

Run “gulp profile” to crawl research profiles

Run “gulp pubs” to fetch publications for researchers

Run “gulp portraits” to get researchers’ avatars

Run “gulp col” to get collaborators for each researcher

Run “gulp clean” to clean the venues and copy them into a new collection

### A.2 Image Alignment

Clone the facenet repository from [here](https://github.com/davidsandberg/facenet).

How to do the alignment please refer to this [issue](https://github.com/davidsandberg/facenet/issues/55).

Then use the commands in command.txt to do the image alignment

### A.3 The Name-based Model

Codes in this directory are trivial so I just give out brief descriptions of each script

Download scikit-learn, numpy, matplotlib as dependencies.

Make sure all the scripts are invoked in the ‘scirpts/’ directory

Also make sure the text data is ready you can make use of the createTxt script

model_selection.py is used for algorithms selection and model evaluatoin

DB.py is used as an interface to interactive with database

createTxt.py is used for generating text dataset from image dataset

parameter_search.py is used for searching hyper parameters for random forest

ML.py in charge of training the model and provides results to the ensemble model

Other scripts are just for experiments.

### A.4 The Portrait-based Model

Clone the TensorFlow repository from [here](https://github.com/tensorflow/tensorflow)

Get the aligned dataset ready

Run the retrain.py method for training, refer to this [link](https://www.tensorflow.org/tutorials/image_retraining)

If you want the parameters I used, check command.txt

With the model you trained, use cv.py to do cross validation

Some python scripts are OpenCV and it is used for algorithms comparison

### A.5 The Ensemble Model

In the ensemble directory

Get the data ready including both text data & image data

Run ensemble_cv.py to evaluate the ensemble model

Use gender_imputation_ensemble.py to infer gender information of the researchers