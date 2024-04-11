#!/bin/bash

#SBATCH --job-name=lookahead_3.0_0
#SBATCH --mail-type=BEGIN,END,FAIL
#SBATCH --mail-user=um21226@bris.ac.uk


#SBATCH --mem=12000M
#SBATCH --account=cosc029884

#SBATCH --nodes=1
#SBATCH --ntasks-per-node=1
#SBATCH --cpus-per-task=1

#SBATCH --time=03:00:00

#SBATCH --partition=short
#SBATCH --array=1-100

#SBATCH --output=/user/home/um21226/results2/lookahead_alpha0/density_3.0_alpha_0/%a.out

module purge

. ~/initConda.sh

conda activate diss

python -u ./code/main.py -density 3.0 -alpha 0 -lookahead
