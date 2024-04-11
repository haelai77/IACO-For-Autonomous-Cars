#!/bin/bash

#SBATCH --job-name=GA_test
#SBATCH --mail-type=BEGIN,END,FAIL
#SBATCH --mail-user=um21226@bristol.ac.uk


#SBATCH --mem-per-cpu=3500
#SBATCH --account=cosc029884

#SBATCH --nodes=1
#SBATCH --ntasks-per-node=1
#SBATCH --cpus-per-task=20

#SBATCH --time=01:00:00

#SBATCH --partition=test

#SBATCH --output=/user/home/um21226/results/test/test_GA/GA.out

module purge

. ~/initConda.sh

conda activate diss

# 6000 timesteps because we do 5000 to let city settle down then take the next agents that finish in the next 1000 timesteps
python -u ./code/main.py -ga -density 3.0 -t_max=6000 -pop_size=20 -tourney_size=3 -max_gen=100
