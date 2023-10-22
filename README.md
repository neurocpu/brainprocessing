# brainprocessing
Python package for processing and analysis of brain data. This is a test repository for exploring collaboration on a pure python package. With time it is hoped that this package will morph into something more useful.

## First steps
* Fork this repository into your Github account
* Clone the forked respository into your local development environment and cd into the root diretory of your repository
```
cd brainprocessing
```
* Start a virtual environment with python version 3.8 or greater in either `conda` or `virtualenv`
* install dependencies for the package as follows:
```
pip install -e ./
```
* if all goes well then you are ready to test the setup as detailed in the next section **Check Setup** 

## Check setup
The `basilreport.py` module performs some basic visual QC on MRI images from an ASL preprocessing pipeline. Contours of the Brain Mask are superimposed on the ASL and Calibration acquisitions to visually assess if co-registration to structural space have been successful. Run the code below to create `html` files in the `./example` folder

```
cd ./brainprocessing/example
```

```
python ../src/brainprocessing/reports/basilreport.py ./style.css ./images ./data ./final.html
```

## Your First Change
In this section you will make a change to the repository. You can add new modules to the package, or update the documentation or add new documentation. The steps to perform will be shown using the command line but they can also be replicated using a GUI in a development environment like `Visual Code` or `Github Desktop Client` 

* First thing you will want to do is create a branch so that you can isolate your development work from the main branch.


## Feature Branch
We will begin work on a feature that adds a motion section to the QC report. The development for this feature will be maintained in a new branch `motionqc`. 

* Bring any development changes that have happened into scope by doing: 
```
git fetch 
```

* Start a new branch as follows:

```
git checkout -b motionqc
```

* Complete development and push the branch to remote
```
git add .
git commit -m "Begin motion qc feature"
git push -u origin motionqc
```