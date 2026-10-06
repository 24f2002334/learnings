# IIT Madras: Machine Learning Foundations

## Week 2, Lecture 1: Sets, Functions, Logic, Sequences, Vector Spaces, and Visualization

Here is the complete lecture content, including the formal definition of sequence convergence with clear step-by-step explanations.

## 1. Basic Sets and Notation

### Standard Sets

* $\mathbb{R}$: All real numbers.

  * *Examples:* $-3.2,\ 0,\ \pi,\ \sqrt{2}$

* $\mathbb{R}_+$: Non-negative reals ($x \ge 0$).

  * *Examples:* $0,\ 0.5,\ 100$ (Note: $-1 \notin \mathbb{R}_+$)

* $\mathbb{Z}$: Integers.

  * *Examples:* $-2,\ -1,\ 0,\ 1,\ 100$

* $\mathbb{Z}_+$: Non-negative integers.

  * *Examples:* $0,\ 1,\ 2,\ 3, \dots$

### Intervals in $\mathbb{R}$

* **Closed interval** $[a,b]$**:** Includes endpoints.

  * Definition: $[2,5] = \{x \in \mathbb{R} : 2 \le x \le 5\}$

  * *Contains:* $2,\ 3.7,\ 5$ (Does not contain $1.9$ or $5.1$)

* **Open interval** $(a,b)$**:** Excludes endpoints.

  * Definition: $(2,5) = \{x \in \mathbb{R} : 2 < x < 5\}$

  * *Contains:* $3,\ 4.999$ (Does not contain $2$ or $5$)

* **Mixed intervals:** $[2,5)$ means $2 \le x < 5$; $(2,5]$ means $2 < x \le 5$.

```
Visual Representation on the Real Line:
Closed [2, 5]: ---[•=========•]---  (Includes 2 and 5)
Open   (2, 5): ---(o---------o)---  (Excludes 2 and 5)

```

### Cartesian Products $\rightarrow \mathbb{R}^d$

$\mathbb{R}^d$ represents all $d$-dimensional vectors with real entries.

* $\mathbb{R}^1 = \mathbb{R}$: Points on a line.

* $\mathbb{R}^2$: Points in a plane, e.g., $(1, -2),\ (0,0),\ (\pi, e)$.

* $\mathbb{R}^3$: Points in 3D space, e.g., $(1, 0, -0.5)$.

**Example (Unit Square in** $\mathbb{R}^2$**):**

$$
[0,1]^2 = [0,1] \times [0,1] = \{(x_1,x_2) : 0 \le x_1 \le 1,\ 0 \le x_2 \le 1\}
$$

* $(0.2, 0.9) \in [0,1]^2$

* $(1.1, 0.5) \notin [0,1]^2$

## 2. Metric Spaces, Distance, and Balls

In $\mathbb{R}^d$, Euclidean distance between $x = (x_1,\dots,x_d)$ and $y = (y_1,\dots,y_d)$ is:

$$
d(x,y) = \Vert{}x - y\Vert{} = \sqrt{(x_1-y_1)^2 + \dots + (x_d-y_d)^2}
$$

### Distance Example in $\mathbb{R}^2$

Let $x = (1,2)$ and $y = (4,6)$.

$$
x - y = (-3,-4), \quad \Vert{}x-y\Vert{} = \sqrt{(-3)^2 + (-4)^2} = \sqrt{9+16} = 5
$$

### Open and Closed Balls

Fix a center $c$ and radius $\varepsilon > 0$.

* **Open ball:** $B(c,\varepsilon) = \{x \in \mathbb{R}^d : \Vert{}x - c\Vert{} < \varepsilon\}$

* **Closed ball:** $\overline{B}(c,\varepsilon) = \{x \in \mathbb{R}^d : \Vert{}x - c\Vert{} \le \varepsilon\}$

```
Visualization in R^2 with center c = (0,0) and radius e = 2:
      ^
    2 +     . . .     <- Boundary NOT included for Open Ball B(c,e)
    |   .           .   Boundary INCLUDED for Closed Ball B_bar(c,e)
  -2+-------(0,0)-------+ 2 >
    |   .           .
   -2     . . . . .

```

* **(1,1):** Distance from origin is $\sqrt{2} \approx 1.41 < 2 \rightarrow$ Inside both balls.

* **(2,0):** Distance $= 2 \rightarrow$ In closed ball, not in open ball.

* **(3,0):** Distance $= 3 \rightarrow$ In neither.

## 3. Set Operations and Logic

Assume universe $V = [0,10]$, with sets $A = [2,6]$ and $B = [4,8]$.

### Set Operations

* **Union (**$A \cup B$**):** $[2,8]$ (Points in $A$ or $B$)

* **Intersection (**$A \cap B$**):** $[4,6]$ (Points in both $A$ and $B$)

* **Difference (**$A \setminus B$**):** $[2,4)$ (Points in $A$ but not in $B$)

* **Complement (**$A^c$**):** $V \setminus A = [0,2) \cup (6,10]$

```
Number Line Diagram:
Universe V:  |---------------------------------------------| (0 to 10)
Set A:              [=======]                                (2 to 6)
Set B:                    [=======]                          (4 to 8)
Intersection:             [===]                              (4 to 6)

```

### De Morgan’s Laws Verification

Law 1: $(A \cup B)^c = A^c \cap B^c$

* Left-hand side: $A \cup B = [2,8]$, so $(A \cup B)^c = [0,2) \cup (8,10]$.

* Right-hand side: $A^c = [0,2) \cup (6,10]$ and $B^c = [0,4) \cup (8,10]$. Their overlap matches exactly $[0,2) \cup (8,10]$.

### Logic Symbols

* $\forall x \in \mathbb{R},\ x^2 \ge 0$: "For all real $x$, $x^2$ is non-negative."

* $\exists x \in \mathbb{R} \text{ s.t. } x^2 = 4$: "There exists a real $x$ with $x^2 = 4$" (True for $x = \pm 2$).

* $x > 2 \Rightarrow x^2 > 4$: Implication ("If $x > 2$, then $x^2 > 4$").

* $x^2 = 4 \Leftrightarrow (x = 2 \text{ or } x = -2)$: Equivalence ("If and only if").

## 4. Sequences and Convergence (With Formal Definition)

A sequence in $\mathbb{R}^d$ is an ordered list $(x_1, x_2, x_3, \dots)$, where each term $x_n \in \mathbb{R}^d$.

### Formal Definition of Convergence

We write:

$$
\lim_{n \to \infty} x_n = x^*
$$

This means that as $n$ grows larger and larger without bound ($n \to \infty$), the terms of the sequence get arbitrarily close to the target limit point $x^*$. 

Formally:
> **For every** $\varepsilon > 0$ (no matter how small a tolerance you choose), **there exists** a natural number $N$ such that **for all** indices $n \ge N$, the distance between $x_n$ and $x^*$ satisfies $\Vert{}x_n - x^*\Vert{} < \varepsilon$. 

In terms of balls, it means that past a certain index $N$, every subsequent point $x_n$ falls entirely inside the open ball $B(x^*, \varepsilon)$.

---

### Example 1: Convergent Sequence in $\mathbb{R}^2$

Let us analyze the sequence:

$$
x_n = \left(1 + \frac{4}{2^n},\ 3 - \frac{4}{2^n}\right)
$$

* $n = 1 \rightarrow x_1 = (3, 1)$
* $n = 2 \rightarrow x_2 = (2, 2)$
* $n = 3 \rightarrow x_3 = (1.5, 2.5)$

As $n \to \infty$, the fraction $\frac{4}{2^n} \to 0$. Therefore, the components approach $(1 + 0, 3 - 0) = (1, 3)$. 

**Target limit point:** $x^* = (1, 3)$.

#### Concrete Check Using the Formal Definition:
1. Suppose an adversarial critic hands us a tight tolerance radius $\varepsilon = 0.1$.
2. We need to find a threshold index $N$ such that for any $n \ge N$, the distance $\Vert{}x_n - x^*\Vert{} < 0.1$.
3. Notice that the distance from $x_n$ to $(1,3)$ is determined by the term $\frac{4}{2^n}$:
   
   $$
   \Vert{}x_n - x^*\Vert{} = \sqrt{\left(\frac{4}{2^n}\right)^2 + \left(-\frac{4}{2^n}\right)^2} = \sqrt{2 \cdot \left(\frac{4}{2^n}\right)^2} = \frac{4\sqrt{2}}{2^n}
   $$

4. We set up our inequality: $\frac{4\sqrt{2}}{2^n} < 0.1$. Solving for $n$ gives a specific integer $N$. Because $2^n$ grows exponentially, such an $N$ always exists for any positive $\varepsilon$.
5. Thus, the sequence converges formally to $(1, 3)$.

```
Sequence Convergence Trajectory in R^2:
  (3,1) o -> (2,2) o -> (1.5,2.5) o -> ... -> (1,3) [Target x*]

```

---

### Example 2: Non-Convergent (Oscillating) Sequence

Consider:

$$
x_n = \left(\cos\left(\frac{n\pi}{2}\right),\ \sin\left(\frac{n\pi}{2}\right)\right)
$$

Values cycle continuously:
* $n = 1 \rightarrow (0, 1)$
* $n = 2 \rightarrow (-1, 0)$
* $n = 3 \rightarrow (0, -1)$
* $n = 4 \rightarrow (1, 0)$

Because it loops endlessly around the unit circle without settling inside any shrinking neighborhood $B(x^*, \varepsilon)$ for large $n$, no such limit $x^*$ exists.

## 5. Vector Spaces, Dot Product, Norm, and Orthogonality

Let $u = (1, 2, -1)$ and $v = (0, 1, 2)$ in $\mathbb{R}^3$.

* **Linear Combinations:** E.g., $\alpha = 2, \beta = -1$:
  

  $$
  2u - v = 2(1,2,-1) - (0,1,2) = (2,4,-2) - (0,1,2) = (2,3,-4)
  $$

* **Dot Product:**
  

  $$
  u \cdot v = (1)(0) + (2)(1) + (-1)(2) = 0 + 2 - 2 = 0
  $$

  
  Since the dot product is $0$, $u$ and $v$ are **orthogonal** (perpendicular).

* **Norms (Lengths):**
  

  $$
  \Vert{}u\Vert{} = \sqrt{1^2 + 2^2 + (-1)^2} = \sqrt{6}
  $$

  $$
  \Vert{}v\Vert{} = \sqrt{0^2 + 1^2 + 2^2} = \sqrt{5}
  $$

## 6. Functions: Domain, Codomain, Graph

A function $f: A \to B$ maps each input in domain $A$ to exactly one output in codomain $B$.

* **1D Real Function:** $f: \mathbb{R} \to \mathbb{R},\ f(x) = x^2$ (Graph is a parabola in $\mathbb{R}^2$).

* **Multivariate Real Function:** $f: \mathbb{R}^2 \to \mathbb{R},\ f(x_1,x_2) = x_1^2 + x_2^2$ (Graph is a paraboloid surface in $\mathbb{R}^3$).

## 7. Visualizing 1D and 2D Functions

### Contour Plots vs. Heatmaps for $f(x_1, x_2) = x_1^2 + x_2^2$

* **Contour Plots:** Fix output levels $c$ to draw curves where $f(x_1,x_2) = c$.

  * $c = 1 \rightarrow x_1^2 + x_2^2 = 1$ (Radius 1 circle)

  * $c = 4 \rightarrow x_1^2 + x_2^2 = 4$ (Radius 2 circle)

* **Heatmaps:** Colors map to function values. Near the origin $(0,0)$, values are low (cool colors like blue); farther away, values grow large (warm colors like red).

```
Contour Plot (Concentric Circles):
         \  c=9  /
          \ --- /
          /  o  \  <- c=4 (radius 2)
         /  (0,0)\ <- c=1 (radius 1)

```

## Why This Matters for Machine Learning

1. **Loss Functions:** Parameter mappings $f: \mathbb{R}^d \to \mathbb{R}$ use contour plots and heatmaps to reveal how errors change relative to parameters.

2. **Training Iterations:** Optimization algorithms generate sequences of parameter vectors $\theta_1, \theta_2, \dots$ that converge toward a minimum loss.

3. **Core Operations:** Vector norms, dot products, and orthogonality form the backbone of linear regression, PCA, and neural network weight computations.