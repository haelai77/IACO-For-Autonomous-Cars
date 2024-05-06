#!/bin/bash

#SBATCH --job-name=vanilla_d2.3_a10
#SBATCH --mail-type=BEGIN,END,FAIL
#SBATCH --mail-user=um21226@bris.ac.uk

#SBATCH --mem=500M
#SBATCH --account=cosc029884

#SBATCH --nodes=1
#SBATCH --ntasks-per-node=1
#SBATCH --cpus-per-task=1

#SBATCH --time=01:00:00

#SBATCH --partition=veryshort
#SBATCH --array=1-1000

#SBATCH --output=/user/home/um21226/vanila_retry/density_2.3_alpha_10/%a.out

module purge

. ~/initConda.sh

conda activate diss
# -lookahead -signalling -detouring -p_weight 11.5 -d_weight 1.3 -alpha 28.6 -spread_pct 0.17 -p_dropoff 0.825
python -u ./code/main.py -density 2.3 -alpha 10