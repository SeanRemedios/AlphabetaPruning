# AlphabetaPruning
An assignment for CISC 352 - Artificial Intelligence.

## Input File
The input file is named "alphabeta.txt"
Any amount of trees can be placed in the file, each is separated by one line.
The trees take the form:
```
{(A,MAX),(B,MIN),(C,MIN),(D,MAX),(E,MAX),(F,MAX),(G,MAX)} {(A,B),(A,C),(B,D),(B,E),(C,F),(C,G),(D,4),(D,3),(E,2),(E,7),(F,3),(F,2),(G,2),(G,8)}
```
The MIN and MAX nodes are in a list as tuples with the node value. This list is separated by the edge list. The order of the tree is MAX and MIN nodes first, top down. The edge node list is left to right, top down.
The input above is a representation of the following tree:
![alt text](https://i.imgur.com/2TOKBFG.png "Alpha-Beta tree")

## Output File
The output file is named "alphabeta_out.txt"
The output takes the form:
```
Graph #: Score #; Leaf Nodes Examined: #
```

## Usage
Type the following command into a terminal window:
```
python3 alphabeta.py
```
