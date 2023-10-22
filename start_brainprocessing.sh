#!/bin/bash

# Create Conda Environment
# cd /xdisk/nkchen/chidiugonna/condaenvs/
# . ./startCondaPuma.sh
# conda create -y --prefix /xdisk/nkchen/chidiugonna/condaenvs/brainprocessing python=3.11
#


CURRDIR=$PWD
cd /xdisk/nkchen/chidiugonna/condaenvs/
. ./startCondaPuma.sh
conda activate ./brainprocessing
cd $CURRDIR
