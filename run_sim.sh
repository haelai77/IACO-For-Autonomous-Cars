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

#SBATCH --partition=test

echo 'My first job'
hostname