# dpra
This repo contains Differentially Private Resource Allocators (DPRAs) of different mechanisms.
Theoretical utility comparison and tradeoff (between privacy and utility) can be reimpletmented by running the .py files named theo_utility_comparison and theo_tradeoff.py.
simulation_lib.py includes defnitions for simulation of different mechnisms, including 
- constant mechanism (cst.py), 
- uniform mechanism (uni.py), 
- one-sided geometric mechanism (geo1.py)
- double geometric mechanism (geo2.py)
- DPRA proposed by Angel et al. (akr.py)

Each of the .py file has a corresponding .ipynb file that reproduces the results in our paper. If it takes a long time to run, please consider reducing the simulation rounds by changing the parameter RD.

The code in this repo are able to reimplement the results in our paper.

We hope this repo help you have a better understanding of DPRA.



## Requirements and Description

### Hardware Dependencies
Our results are produced mainly using Apple M1 Pro with 32GB RAM running macOS Ventura 13.0. 

Beyond that, we have also tested our code on other platforms listed as follows:
1. Ubuntu machine (Ubuntu 20.04.5 LTS with 256GB memory and an AMD 3970x CPU)
2. Google Colab (Python 3 on a Google Compute Engine backend with 12.7 GB system RAM)

The peak RAM utilization observed during our test on Apple M1 Pro was 18.1 GB. Thus, we recommend having a minimum of ~18GB RAM available for the simulation.

### Software Dependencies
#### OS Dependencies
DPRA has been tested on macOS Ventura 13.0 and Ubuntu 20.04.5 LTS.

### Core Dependencies 
Python 3.6+ 

git

pip3

virtualenv (or conda)
 
### Python Dependencies
numpy 

matplotlib

math

random

itertools

collections

### Execution Time Estimations
Each simulation of 100 million rounds takes about 9 - 10 mins on Apple M1 Pro with 32GB RAM running macOS Ventura 13.0.
Plotting takes a few seconds.

## How It Works
In our paper, we proposed four different mechanism to achieve differentially private resource allocation:

- constant mechanism (cst.py, cst.ipynb)
- uniform mechanism (uni.py, uni.ipynb)
- one-sided geometric mechanism (geo1.py, geo1.ipynb)
- double geometric mechanism (geo2.py, geo2.ipynb)
- And we compared our mechanism with 
- akr (akr.py, akr.ipynb) proposed by Angel et al. [1].

More specifically, all the mechanisms have tunable parameters.

- constant mechanism (cst.py, cst.ipynb)

    parameter(s): c

- uniform mechanism (uni.py, uni.ipynb)

    parameter(s): x0 (starting point), x (end point)

- one-sided geometric mechanism (geo1.py, geo1.ipynb)
  
    parameter(s): x0 (starting point), p (geometric parameter)

- double geometric mechanism (geo2.py, geo2.ipynb)

    parameter(s): miu (bias), s (geometric scale)

- akr (akr.py, akr.ipynb) 

    parameter(s): miu (bias), s (laplace scale)

To reproduce the parameter study results (Figure 5-7), please refer to dpra_para.ipynb.
For comparison across all mechanisms, a thorough parameter search needs to be done. In general, the goal for each mechanism is to search for parameters that achieves the best utility when having the same privacy budget. After a thorough parameter search, we could use the best utility and privacy pairs to draw the comparison (Figure 2, 8). Besides, Figure 3 can be found in geo1.ipynb, Figure 4 can be found in geo2.ipynb.

## Running DPRA
To run DPRA, we provide two option, but recommend the reviewers to use the jupyter notebook (option2).

### Option 1
To test the mechanism, simple run each mechanism’s corresponding .py file. For example, run
python cst.py


### Option 2
We also made the jupyter notebook for all the mechanism for the ease of artifact evaluation. Each .ipynb file has the output cells also being saved. To rerun these mechanisms, simply run all the cells in the jupyter notebook. 

Note that due to large round of simulation, the experiments may take a little while, to reduce the round number, please set the parameter RD to a smaller number.


## References
[1] Sebastian Angel, Sampath Kannan, and Zachary Ratliff. 2020. Private resource allocators and their applications. In 2020 IEEE Symposium on Security and Privacy (SP). IEEE, 372–391.




