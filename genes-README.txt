Ryan Vasios
genes.py README

open python 
import genes
from genes import *

Thanks for checking out my project.  It culminates in two experiments.

Experiment One:  Evolving a converged strategy and testing for stability
To run simply call the function:
>>> evolutionsimulation_self()

It will print the number of rounds it took for the genetic algorithm to converge, a sample game between two players from our final, resultant generation, the score they obtained with one another, and assessment of their stability ( ie their ability to withstand invasion by random strategies)

Experiment Two: Evolving strategies against TIT-FOR-TAT with Noise
To run simply call the function:
>>> evolutionsimulation_TFTN()
BE ADVISED THIS TAKES TWO MINUTES TO RUN DON'T PANIC

It will print a comparison of the initial and final generations in terms of their relation to the genome of TIT-FOR-TAT
