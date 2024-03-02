#!/bin/bash

#SBATCH --job-name=1000_runs
#SBATCH --mail-type=BEGIN,END,FAIL
#SBATCH --mail-user=um21226@bris.ac.uk

#SBATCH --mem=1000M
#SBATCH --account=cosc029884

#SBATCH --nodes=1
#SBATCH --ntasks-per-node=1
#SBATCH --cpus-per-task=1

#SBATCH --time=12:00:00

#SBATCH --partition=cpu

#SBATCH --output=out_directory/density_${1}__alpha_${2}/%a_density_${1}__alpha_${2}.out

module purge
module add languages/anaconda3/2022.11-3.9.13

python -u main.py -density ${1} -alpha ${2}