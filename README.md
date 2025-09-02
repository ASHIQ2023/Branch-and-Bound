# Problem Example 
The owner of a machine shop is planning to expand by purchasing some new machines - press and lathes. The owner has estimated that each press purchase will increase profit by \$ 100 per day and each lathe will increase profit by \$ 150 daily. The number of machines the owner can purchase is limited by the cost of the machines and the available floor space in the shop. The machine purchase prices, and space reqiurements are as follows:  
   
|**Machine**|**Required Floor Space ft<sup>2</sup>**| **Purchase Price** |  
|:-------|---------:|:------------------:|
|Press| 15 |      \$ 8000       |
|Lathe| 30 |      \$ 4000       |  
The owner has a budget of \$ 40000 for purchasing machines and 200 square feet of available floor space. The owner wants to know how many of each type of machine to purchase to maximize the daily increase in profit.

# Mathematical Formulation  

### Decision Variables  
$x_p$ = Number of Presses  
$x_l$ = Number of Lathes

### Objective Function  
Maximize $ = \$100x_p + \$150x_l $
### Constraint  
subject to,  
&emsp; &emsp; &emsp; &emsp; &emsp;    $8000x_p + 4000x_l \leq  40000$  
&emsp; &emsp; &emsp; &emsp; &emsp; &emsp;$15x_p + 30x_l \leq 200$  

### Sign Constraint
&emsp; &emsp; &emsp;   $x_l \geq 0 $ and integer   
&emsp; &emsp; &emsp;   $x_p \geq 0$ and integer


# Code Algorithm
# Branch and Bound Algorithm

## Algorithm Framework

**Algorithm 1: Branch and Bound for Integer Programming**

&emsp; &emsp; &emsp; **Input**: *Linear programming problem with integer restrictions*  
&emsp; &emsp; &emsp; **Output**: *Optimal integer solution or indication of infeasibility*  

&emsp; &emsp; &emsp; **Initialize:**  
&emsp; &emsp; &emsp; &emsp;&emsp;&emsp;&emsp; *Create root node $N_0$*  
&emsp; &emsp; &emsp; &emsp;&emsp;&emsp;&emsp; *Set active node list $L = \{N_0\}$*  
&emsp; &emsp; &emsp; &emsp;&emsp;&emsp;&emsp; *Set incumbent solution $z^* = -\infty$*  
&emsp; &emsp; &emsp; &emsp;&emsp;&emsp;&emsp; *Set best solution $x_{\text{best}} = \varnothing$*  

&emsp; &emsp; &emsp; **While $L \neq \varnothing$ do:**  
&emsp; &emsp; &emsp; &emsp;&emsp;&emsp;&emsp; *Select node $N_k$ from $L$ with highest upper bound (UB)*  
&emsp; &emsp; &emsp; &emsp;&emsp;&emsp;&emsp; *Remove $N_k$ from $L$*  
&emsp; &emsp; &emsp; &emsp;&emsp;&emsp;&emsp; *Solve LP relaxation of $N_k$*  

&emsp; &emsp; &emsp; &emsp;&emsp;&emsp;&emsp; **If infeasible then:**  
&emsp; &emsp; &emsp; &emsp;&emsp;&emsp;&emsp;&emsp;&emsp; *Continue to next iteration*  

&emsp; &emsp; &emsp; &emsp;&emsp;&emsp;&emsp; **If unbounded then:**  
&emsp; &emsp; &emsp; &emsp;&emsp;&emsp;&emsp;&emsp;&emsp; *Terminate, problem is unbounded*  

&emsp; &emsp; &emsp; &emsp;&emsp;&emsp;&emsp; **If feasible then:**  
&emsp; &emsp; &emsp; &emsp;&emsp;&emsp;&emsp;&emsp;&emsp; *Let $(x^*, z_k)$ be the optimal solution of relaxation*  
&emsp; &emsp; &emsp; &emsp;&emsp;&emsp;&emsp;&emsp;&emsp; **If $z_k \leq z^*$ then:** *(Prune by bound)*  
&emsp; &emsp; &emsp; &emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp; *Continue to next iteration*  

&emsp; &emsp; &emsp; &emsp;&emsp;&emsp;&emsp;&emsp;&emsp; **If $x^*$ is integer then:**  
&emsp; &emsp; &emsp; &emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp; **If $z_k > z^*$ then:**  
&emsp; &emsp; &emsp; &emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp; *Update $z^* = z_k$, $x_{\text{best}} = x^*$*  
&emsp; &emsp; &emsp; &emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp; *Continue to next iteration*  

&emsp; &emsp; &emsp; &emsp;&emsp;&emsp;&emsp;&emsp;&emsp; **Else (non-integer solution):**  
&emsp; &emsp; &emsp; &emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp; *Select branching variable $x_j$ with max fractional part*  
&emsp; &emsp; &emsp; &emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp; *Create two child nodes:*  
&emsp; &emsp; &emsp; &emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp; $N_{\text{left}}$: add constraint $x_j \leq \lfloor x_j^* \rfloor$  
&emsp; &emsp; &emsp; &emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp; $N_{\text{right}}$: add constraint $x_j \geq \lceil x_j^* \rceil$  
&emsp; &emsp; &emsp; &emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp; *Add $N_{\text{left}}$ and $N_{\text{right}}$ to $L$*  

&emsp; &emsp; &emsp; **Return:**   
&emsp; &emsp; &emsp; &emsp;&emsp;&emsp;&emsp;*Optimal solution $(x_{\text{best}}, z^*)$ if found, otherwise report infeasible*  



# Result

**Optimal Objective Value**  
*Optimal daily profit increase: $1,250* 

**Optimal Solution (Integer Values)**  
*Purchase $x_p = 2$ presses*  
*Purchase $x_l = 10$ lathes*  

**Resource Utilization**  
*Total cost used: $40,000 / $40,000 (0 remaining)*  
*Floor space used: 200 ft² / 200 ft² (0 remaining)*  
