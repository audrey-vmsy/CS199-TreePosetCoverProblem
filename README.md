<h1 align='center'> :deciduous_tree: Two Heuristics for the Tree Poset Cover Problem :deciduous_tree: </h1>
<b>Abstract</b>

The Poset Cover Problem aims to find a minimum set of posets that cover a given input set of linear orders. 
This problem has practical applications in data mining, particularly in constructing directed networks from sequential data. The decision version of the problem is known to be NP-hard. 
In this study, we focus on a variant called the Tree Poset Cover Problem, which requires identifying a minimum set of tree posets needed to cover a given input set of linear orders. 
We propose two polynomial-time heuristics, namely Heuristic 1 and Heuristic 2. 
Our investigation demonstrates that both heuristics consistently produce feasible solutions and can be classified as approximation algorithms.
Furthermore, we empirically evaluate the performance of Heuristic 1 and Heuristic 2 using four datasets.

<p align = "center"> 
    <img src="Utils\images\TreePosetCoverProblem.png" alt="image">
</p>

## Usage :keyboard:
> [!NOTE]
> Make sure to run the codes in the order they're listed below – it really matters! :dizzy:
1. Generate an input file and optimal solution file (choose either exhaustive or random generation)  
    **Exhaustive**
    ```python
    python optimalsolutions.py <vertex count*> <max posets*>
    ```
    **Random**
    ```python
    python optimalsolutions2.py <vertex count*> <max posets*>
    ```
2. Generate heuristic solutions on the input file (choose either heuristic-one or heuristic-two)
    ```python
    python heuristic-<one/two>.py <vertex count*>
    ```
3. Generate analysis of optimal and heuristic solutions
    ```python
    python analysis.py <vertex count*>
    ```

*`vertex count` should be valued 3 or greater  
*`max posets` should be valued 1 or greater

> [!WARNING] 
> When using a standard or typical machine, it is advisable to limit the `<vertex count*>` to a maximum of 6 and the `<max posets*>` to a maximum of 4. Once you exceed these values, generating the desired file will require a significant amount of time.
