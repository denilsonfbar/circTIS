circTIS
=======
**circTIS** is a computational tool designed to translation initiation sites (TIS) prediction in circRNAs.

Repository of circTIS development: [https://github.com/denilsonfbar/circTIS-exps-BSB2023](https://github.com/denilsonfbar/circTIS-exps-BSB2023)

## Quick installation

Clone the circTIS repository:
```
git clone https://github.com/denilsonfbar/circTIS.git
```

Enter the circTIS folder:
```
cd circTIS
```

Create Conda environment from ```environment.yml``` configuration file:
```
conda env create -f environment.yml
```

Activate the created environment:
```
conda activate circtis_env
```


## Running

Run the prediction example using Python interpreter:
```
python3 circtis.py -f example/circRNA_seqs.fa
```

OR

Give execution privileges to the circCodAn script file:
```
chmod +x circtis.py
```

And run the example directly from the script file:
```
./circtis.py -f example/circRNA_seqs.fa
```

OR

If you need to run circTIS from anywhere on the file system, update the PATH variable:
```
export PATH=$PATH:path/to/circTIS
```

And run the example from anywhere on the file system:
```
circtis.py -f path/to/example/circRNA_seqs.fa
```

### Expected example output
```
2023-05-31 15:48:48 -> started circTIS v1.0
2023-05-31 15:49:01 -> prediction finished
Number of input sequences -> 100
Number of predicted TIS   -> 92
All possible TIS file     -> example/circTIS_output/all_possible_TIS.tsv
Predicted TIS file        -> example/circTIS_output/predicted_TIS.tsv
```

The files with the outputs of circTIS execution are recorded at the addresses given.


## Manual installation

Install the following requirements:

- [Python3](https://www.python.org/)
- [Pandas](https://pandas.pydata.org/docs/getting_started/install.html)
- [Biopython](https://biopython.org/wiki/Download)
- [Shogun 6.1.3](https://anaconda.org/conda-forge/shogun)

Carry out of the same steps described in **Installation** section, except for creating and activating the Conda environment.


## Usage

```
Usage: circtis.py [options]

Options:
  -h, --help            show this help message and exit
  -f file, --file=file  mandatory - input circRNAs file (FASTA format). Ex:
                        example/circRNA_seqs.fa
  -t string, --tis=string
                        optional - TIS types for search. Options:
                        ATG
                        NC1 [ATG, CTG, GTG, TTG]
                        NC2 [ATG, CTG, GTG, TTG, AAG, ACG, AGG, ATA, ATC, ATT]
                        [default = NC1]
  -o folder, --output=folder
                        optional - path to output folder. Ex:
                        path/to/output_folder
                        if not declared, it will be created at the circRNAs
                        input folder
                        [default = "circTIS_output"]
```

Basic example to find TIS in circRNA sequences:
```
python3 circTIS.py -f example/circRNA_seqs.fa
```

## Reference

If you use or discuss circTIS, please cite:

Barbosa, D.F., Oliveira, L.S., Kashiwabara, A.Y. (2023). circTIS: A Weighted Degree String Kernel with Support Vector Machine Tool for Translation Initiation Sites Prediction in circRNA. In: Reis, M.S., de Melo-Minardi, R.C. (eds) Advances in Bioinformatics and Computational Biology. BSB 2023. Lecture Notes in Computer Science, vol 13954. Springer, Cham. [https://doi.org/10.1007/978-3-031-42715-2_2](https://doi.org/10.1007/978-3-031-42715-2_2)


## License

[GNU GPLv3](https://www.gnu.org/licenses/gpl-3.0.html)


## Contact

To report bugs, to ask for help and to give any feedback, please contact denilsonfbar@gmail.com
