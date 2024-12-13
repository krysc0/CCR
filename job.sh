#!/bin/bash

#SBATCH --cluster=ub-hpc
#SBATCH --partition=general-compute
#SBATCH --qos=general-compute
#SBATCH --mail-user={UBIT}@buffalo.edu
#SBATCH --mail-type=end
#SBATCH --time=00:20:00
#SBATCH --job-name="array"
#SBATCH --output=array.out
#SBATCH --error=array.err
#SBATCH --array=1-5%5
#SBATCH --ntasks=1
#SBATCH --mem=32M

module load gcccore/11.3.0
module load python/3.10.4-bare

python ./jobarray.py --index=$SLURM_ARRAY_TASK_ID