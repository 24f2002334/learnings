# you asked

message time: 2026-10-06 19:38:35

Welcome to week 3 of machine learning foundations. this is the transcript of my lecture explain everything properly

---

# chatgpt response

Absolutely. Let’s turn this lecture into a **clear, structured set of notes**, starting from the intuition and then moving to the calculations and theorems.

# Week 3 — Four Fundamental Subspaces of a Matrix

The entire lecture revolves around one matrix

$$
A\in\mathbb R^{m\times n}
$$

and four important subspaces associated with it:

1. **Column space** — $\operatorname{Col}(A)$
2. **Null space** — $N(A)$
3. **Row space** — $\operatorname{Row}(A)$
4. **Left null space** — $N(A^T)$

The most important relationships are:

$$
\boxed{\operatorname{rank}(A)+\operatorname{nullity}(A)=n}
$$

and

$$
\boxed{\operatorname{rank}(A)+\operatorname{nullity}(A^T)=m}
$$

where $n$ is the number of columns and $m$ is the number of rows.

---

# 1. First: What is a subspace?

Before understanding the four spaces, remember what a **subspace** means.

A set $S$ is a subspace if:

### Condition 1: Closed under addition

If

$$
x_1,x_2\in S
$$

then

$$
x_1+x_2\in S.
$$

### Condition 2: Closed under scalar multiplication

If

$$
x\in S
$$

and $\alpha$ is any scalar, then

$$
\alpha x\in S.
$$

The four spaces we're studying are all subspaces of some Euclidean space.

---

# 2. Column Space

Suppose

$$
A=
\begin{bmatrix}
|&|&&|\\
u_1&u_2&\cdots&u_n\\
|&|&&|
\end{bmatrix}
$$

where $u_1,\ldots,u_n$ are the columns of $A$.

The **column space** is

$$
\boxed{\operatorname{Col}(A)=\operatorname{span}\{u_1,u_2,\ldots,u_n\}}
$$

In simple words:

> The column space contains **all possible linear combinations of the columns of $A$**.

For example, if

$$
A=
\begin{bmatrix}
1&2\\
3&6
\end{bmatrix},
$$

the columns are

$$
u_1=
\begin{bmatrix}
1\\3
\end{bmatrix},
\qquad
u_2=
\begin{bmatrix}
2\\6
\end{bmatrix}.
$$

But

$$
u_2=2u_1.
$$



Therefore every linear combination looks like

$$
c_1u_1+c_2u_2
=
(c_1+2c_2)u_1.
$$

So the entire column space is just the line through

$$
\begin{bmatrix}1\\3\end{bmatrix}.
$$

Thus

$$
\boxed{\operatorname{Col}(A)=
\operatorname{span}\left\{
\begin{bmatrix}1\\3\end{bmatrix}
\right\}}
$$

and its dimension is 1.

---

# 3. Why is Column Space important?

The column space becomes extremely important when solving

$$
Ax=b.
$$

Suppose

$$
A=
\begin{bmatrix}
|&|&&|\\
u_1&u_2&\cdots&u_n\\
|&|&&|
\end{bmatrix}
$$

and

$$
x=
\begin{bmatrix}
x_1\\x_2\\\vdots\\x_n
\end{bmatrix}.
$$

Then

$$
Ax=x_1u_1+x_2u_2+\cdots+x_nu_n.
$$

So $Ax$ is **always a linear combination of the columns of $A$**.

Therefore:

$$
\boxed{Ax=b\text{ has a solution iff }b\in\operatorname{Col}(A)}
$$

This is one of the key ideas of the lecture.

### Example

Suppose $A$ is a $4\times3$ matrix.

Then

$$
Ax=b
$$

means:

- 4 equations
- 3 unknowns.

The vector $b$ belongs to $\mathbb R^4$.

But the column space may only be a 2-dimensional subspace of $\mathbb R^4$.

Therefore, **not every $b\in\mathbb R^4$ can be produced by $Ax$**.

Only those $b$'s lying inside the column space can.

---

# 4. Example from the lecture

The lecture uses

$$
A=
\begin{bmatrix}
1&1&2\\
2&1&3\\
3&1&4\\
4&1&5
\end{bmatrix}
$$

because

$$
\text{column 3}=\text{column 1}+\text{column 2}.
$$

Therefore the third column doesn't provide a new independent direction.

So

$$
\operatorname{Col}(A)
=
\operatorname{span}\{u_1,u_2\}.
$$

Hence

$$
\boxed{\dim(\operatorname{Col}(A))=2}
$$

even though $A$ has three columns.

This dimension is called the **rank**.

Therefore

$$
\boxed{\operatorname{rank}(A)=2}.
$$

---

# 5. Null Space

Now we move to the second fundamental subspace.

The **null space** of $A$ is

$$
\boxed{N(A)=\{x:Ax=0\}}
$$

In words:

> Null space consists of all vectors $x$ that get mapped to the zero vector when multiplied by $A$.

So we're solving

$$
Ax=0.
$$

---

# 6. Why is the null space a subspace?

Suppose

$$
x_1,x_2\in N(A).
$$

That means

$$
Ax_1=0
$$

and

$$
Ax_2=0.
$$

Then

$$
A(x_1+x_2)
=
Ax_1+Ax_2
=
0+0
=
0.
$$

Therefore

$$
x_1+x_2\in N(A).
$$

Similarly,

$$
A(\alpha x)
=
\alpha Ax
=
\alpha(0)
=
0.
$$

Therefore

$$
\alpha x\in N(A).
$$

So $N(A)$ is indeed a subspace.

---

# 7. Intuition behind the Null Space

Remember:

$$
Ax=x_1u_1+x_2u_2+\cdots+x_nu_n.
$$

Therefore $Ax=0$ means:

> Find combinations of the columns that cancel each other out completely.

For the previous matrix, we know

$$
u_3=u_1+u_2.
$$

Therefore

$$
u_1+u_2-u_3=0.
$$

This corresponds to

$$
x=
\begin{bmatrix}
1\\1\\-1
\end{bmatrix}.
$$

Hence

$$
\boxed{
\begin{bmatrix}
1\\1\\-1
\end{bmatrix}
\in N(A)
}
$$

Since $A$ has 3 columns, $x$ has 3 components.

So the null space lives in

$$
\boxed{\mathbb R^3}.
$$

Because there is only one independent relationship among the columns, the null space is a **one-dimensional line in $\mathbb R^3$**.

---

# 8. Rank and Nullity

Two very important terms:

### Rank

$$
\boxed{\operatorname{rank}(A)
=
\dim(\operatorname{Col}(A))}
$$

It is also equal to the number of pivot columns.

### Nullity

$$
\boxed{\operatorname{nullity}(A)
=
\dim(N(A))}
$$

It is equal to the number of free variables.

Therefore:

$$
\boxed{\text{rank}+\text{nullity}
=
\text{number of columns}}
$$

This is called the **Rank-Nullity Theorem**.

If $A$ has $n$ columns and rank $r$,

$$
\boxed{\operatorname{nullity}(A)=n-r}.
$$

---

# 9. Gaussian Elimination and Null Space

The lecture then gives

$$
A=
\begin{bmatrix}
1&2&2&2\\
2&4&6&8\\
3&6&8&10
\end{bmatrix}.
$$

After Gaussian elimination:

$$
U=
\begin{bmatrix}
1&2&2&2\\
0&0&2&4\\
0&0&0&0
\end{bmatrix}.
$$

The pivot columns are columns 1 and 3.

So:

- Pivot variables: $x_1,x_3$
- Free variables: $x_2,x_4$

There are 2 free variables, so

$$
\boxed{\operatorname{nullity}(A)=2}.
$$

There are 2 pivot columns, so

$$
\boxed{\operatorname{rank}(A)=2}.
$$

And indeed:

$$
2+2=4
$$

which equals the number of columns.

---

# 10. Finding a Basis for the Null Space

We solve

$$
Ux=0.
$$

That gives

$$
x_1+2x_2+2x_3+2x_4=0
$$

and

$$
2x_3+4x_4=0.
$$

Because $x_2,x_4$ are free, we find one basis vector for each free variable.

### First: Set

$$
x_2=1,\qquad x_4=0.
$$

Then

$$
x_3=0
$$

and

$$
x_1=-2.
$$

So

$$
u=
\begin{bmatrix}
-2\\1\\0\\0
\end{bmatrix}.
$$

### Second: Set

$$
x_2=0,\qquad x_4=1.
$$

Then

$$
2x_3+4=0
$$

so

$$
x_3=-2.
$$

Then

$$
x_1+2(-2)+2=0
$$

so

$$
x_1=2.
$$

Thus

$$
v=
\begin{bmatrix}
2\\0\\-2\\1
\end{bmatrix}.
$$

Therefore

$$
\boxed{
N(A)=\operatorname{span}
\left\{
\begin{bmatrix}-2\\1\\0\\0\end{bmatrix},
\begin{bmatrix}2\\0\\-2\\1\end{bmatrix}
\right\}
}
$$

These two vectors form a **basis for the null space**.

---

# 11. What happens if $A$ is invertible?

For a square invertible matrix,

$$
Ax=0
$$

has only the solution

$$
x=0.
$$

Therefore

$$
\boxed{N(A)=\{0\}}
$$

and

$$
\boxed{\operatorname{nullity}(A)=0}.
$$

Also, its columns are linearly independent and span the entire space.

Thus

$$
\boxed{\operatorname{Col}(A)=\mathbb R^n}.
$$

So $Ax=b$ has a **unique solution for every $b$**.

---

# 12. What if $A$ is not invertible?

Then there is at least one nonzero vector

$$
x_n\neq0
$$

such that

$$
Ax_n=0.
$$

Suppose $x_p$ is one particular solution of

$$
Ax=b.
$$

Then

$$
A(x_p+x_n)
=
Ax_p+Ax_n
=
b+0
=
b.
$$

So another solution is

$$
x_p+x_n.
$$

In fact, all solutions can be written as

$$
\boxed{x=x_p+x_n,\qquad x_n\in N(A)}
$$

This is a very important connection between the **null space** and the solutions of $Ax=b$.

---

# 13. Row Space

Now we introduce the third space.

The row space is simply the span of the rows of $A$.

We can write:

$$
\boxed{\operatorname{Row}(A)=\operatorname{Col}(A^T)}
$$

Why?

Because when you transpose $A$, its rows become columns.

For example:

$$
A=
\begin{bmatrix}
1&2\\
3&4
\end{bmatrix}
$$

has rows

$$
[1\quad2]
$$

and

$$
[3\quad4].
$$

But

$$
A^T=
\begin{bmatrix}
1&3\\
2&4
\end{bmatrix}.
$$

Its columns are

$$
\begin{bmatrix}1\\2\end{bmatrix},
\qquad
\begin{bmatrix}3\\4\end{bmatrix}.
$$

Those are the transposed versions of the rows of $A$.

Hence:

$$
\boxed{\operatorname{Row}(A)=\operatorname{Col}(A^T)}.
$$

---

# 14. Row Rank = Column Rank

One of the most important theorems in linear algebra is

$$
\boxed{\text{row rank}=\text{column rank}}
$$

Therefore:

$$
\boxed{\dim(\operatorname{Row}(A))
=
\dim(\operatorname{Col}(A))
=
\operatorname{rank}(A)}
$$

So you can find the rank either by counting independent columns or independent rows.

---

# 15. Left Null Space

The fourth and final fundamental subspace is the **left null space**.

It is defined as

$$
\boxed{N(A^T)}
$$

That is,

$$
N(A^T)
=
\{y:A^Ty=0\}.
$$

Equivalently,

$$
\boxed{y^TA=0}.
$$

Why is it called the **left** null space?

Because we can write the condition as

$$
y^TA=0.
$$

Here $y^T$ is multiplying $A$ from the **left**.

---

# 16. Intuition for Left Null Space

Suppose $A$ has rows

$$
r_1,r_2,\ldots,r_m.
$$

Then

$$
y^TA=0
$$

means

$$
y_1r_1+y_2r_2+\cdots+y_mr_m=0.
$$

So the left null space contains all the combinations of the **rows of $A$** that produce zero.

This is similar to the ordinary null space, except:

### Ordinary null space

We combine **columns**:

$$
Ax=0.
$$

### Left null space

We combine **rows**:

$$
y^TA=0.
$$

That's an excellent way to remember the distinction.

---

# 17. The dimensions of all four spaces

Now suppose

$$
A\in\mathbb R^{m\times n}
$$

and

$$
\operatorname{rank}(A)=r.
$$

Then:

| Subspace | Dimension |
|---|---:|
| Column space $C(A)$ | $r$ |
| Null space $N(A)$ | $n-r$ |
| Row space $C(A^T)$ | $r$ |
| Left null space $N(A^T)$ | $m-r$ |

Therefore:

$$
\boxed{
\dim C(A)=r
}
$$

$$
\boxed{
\dim N(A)=n-r
}
$$

$$
\boxed{
\dim C(A^T)=r
}
$$

$$
\boxed{
\dim N(A^T)=m-r
}
$$

---

# 18. Two Rank-Nullity Equations

For $A\in\mathbb R^{m\times n}$:

### For $A$

Since $A$ has $n$ columns,

$$
\boxed{
r+(n-r)=n
}
$$

or

$$
\boxed{
\operatorname{rank}(A)+\operatorname{nullity}(A)=n
}
$$

### For $A^T$

$A^T$ has $m$ columns.

Therefore:

$$
\boxed{
r+(m-r)=m
}
$$

or

$$
\boxed{
\operatorname{rank}(A)+\operatorname{nullity}(A^T)=m
}
$$

This second equation gives

$$
\boxed{
\operatorname{nullity}(A^T)=m-r
}
$$

---

# 19. The Simple $2\times2$ Example

The lecture uses

$$
A=
\begin{bmatrix}
1&2\\
3&6
\end{bmatrix}.
$$

Let's find all four spaces.

## Step 1: Column space

Columns are

$$
\begin{bmatrix}1\\3\end{bmatrix},
\qquad
\begin{bmatrix}2\\6\end{bmatrix}.
$$

The second is twice the first:

$$
\begin{bmatrix}2\\6\end{bmatrix}
=
2
\begin{bmatrix}1\\3\end{bmatrix}.
$$

Therefore

$$
\boxed{
C(A)=
\operatorname{span}
\left\{
\begin{bmatrix}1\\3\end{bmatrix}
\right\}
}
$$

and

$$
\boxed{r=1}.
$$

---

## Step 2: Null space

Solve

$$
Ax=0.
$$

Let

$$
x=
\begin{bmatrix}x_1\\x_2\end{bmatrix}.
$$

Then

$$
\begin{bmatrix}
1&2\\
3&6
\end{bmatrix}
\begin{bmatrix}
x_1\\x_2
\end{bmatrix}
=
\begin{bmatrix}0\\0\end{bmatrix}.
$$

The first equation gives

$$
x_1+2x_2=0.
$$

Thus

$$
x_1=-2x_2.
$$

Set

$$
x_2=t.
$$

Then

$$
x=
\begin{bmatrix}
-2t\\t
\end{bmatrix}
=
t
\begin{bmatrix}
-2\\1
\end{bmatrix}.
$$

Therefore

$$
\boxed{
N(A)=
\operatorname{span}
\left\{
\begin{bmatrix}-2\\1\end{bmatrix}
\right\}
}
$$

and

$$
\boxed{\operatorname{nullity}(A)=1}.
$$

Notice:

$$
r+\text{nullity}=1+1=2=n.
$$

Perfect.

---

# 20. Row Space of the Same Matrix

The rows are

$$
[1\quad2]
$$

and

$$
[3\quad6].
$$

Again,

$$
[3\quad6]=3[1\quad2].
$$

Therefore

$$
\boxed{
\operatorname{Row}(A)
=
\operatorname{span}\{[1\quad2]\}
}
$$

and

$$
\boxed{\dim(\operatorname{Row}(A))=1}.
$$

As expected:

$$
\text{row rank}=\text{column rank}=1.
$$

---

# 21. Left Null Space

We now solve

$$
A^Ty=0.
$$

Since

$$
A^T=
\begin{bmatrix}
1&3\\
2&6
\end{bmatrix},
$$

we solve

$$
\begin{bmatrix}
1&3\\
2&6
\end{bmatrix}
\begin{bmatrix}
y_1\\y_2
\end{bmatrix}
=
\begin{bmatrix}0\\0\end{bmatrix}.
$$

The first equation gives

$$
y_1+3y_2=0.
$$

So

$$
y_1=-3y_2.
$$

Set $y_2=t$:

$$
y=
t
\begin{bmatrix}
-3\\1
\end{bmatrix}.
$$

Thus

$$
\boxed{
N(A^T)=
\operatorname{span}
\left\{
\begin{bmatrix}-3\\1\end{bmatrix}
\right\}
}
$$

and

$$
\boxed{\dim N(A^T)=1}.
$$

Check the formula:

$$
m-r=2-1=1.
$$

Correct.

---

# 22. The Big Picture

For an $m\times n$ matrix:

```text
                         A
                ┌─────────────────┐
                │   m rows        │
                │   n columns     │
                └─────────────────┘

        COLUMN SIDE                    ROW SIDE

     Column Space                     Row Space
       C(A)                            C(Aᵀ)
         │                                │
       dim = r                          dim = r
         │                                │
         │                                │
     Null Space                     Left Null Space
       N(A)                            N(Aᵀ)
         │                                │
     dim = n-r                        dim = m-r
```

So the four dimensions are:

$$
\boxed{r,\quad n-r,\quad r,\quad m-r}
$$

---

# 23. A Very Important Mental Model

Try to remember the four spaces using **what is being combined**.

### Column space

Combine columns:

$$
\boxed{Ax=b}
$$

and ask:

> Can $b$ be made from the columns of $A$?

---

### Null space

Combine columns to get zero:

$$
\boxed{Ax=0}
$$

and ask:

> Which combinations of columns cancel to zero?

---

### Row space

Combine rows:

$$
\boxed{\operatorname{Row}(A)=\operatorname{Col}(A^T)}
$$

---

### Left null space

Combine rows to get zero:

$$
\boxed{y^TA=0}
$$

and ask:

> Which combinations of rows cancel to zero?

---

# 24. One More Crucial Point: Where Does Each Space Live?

This is a common source of confusion.

If

$$
A\in\mathbb R^{m\times n},
$$

then:

### Columns have $m$ entries

Therefore

$$
\boxed{C(A)\subseteq\mathbb R^m}.
$$

### $x$ has $n$ entries

Therefore

$$
\boxed{N(A)\subseteq\mathbb R^n}.
$$

### Rows have $n$ entries

Therefore

$$
\boxed{\operatorname{Row}(A)\subseteq\mathbb R^n}.
$$

### $y$ has $m$ entries

Therefore

$$
\boxed{N(A^T)\subseteq\mathbb R^m}.
$$

So:

| Space | Lives in |
|---|---|
| Column space $C(A)$ | $\mathbb R^m$ |
| Null space $N(A)$ | $\mathbb R^n$ |
| Row space $C(A^T)$ | $\mathbb R^n$ |
| Left null space $N(A^T)$ | $\mathbb R^m$ |

This is **very important for machine learning**, because dimensions of vectors and matrices must match.

---

# 25. What You Should Be Able to Do After This Lecture

For an arbitrary matrix $A$, you should be comfortable doing these things:

### 1. Find rank

Perform Gaussian elimination and count pivots.

$$
\boxed{\operatorname{rank}(A)=\#\text{ pivots}}
$$

### 2. Find column space

Find the **pivot columns of the original matrix**.

Important: use the corresponding columns from the **original $A$**, not necessarily the row-reduced matrix.

### 3. Find null space

Solve

$$
Ax=0.
$$

The free variables generate the null-space basis.

### 4. Find row space

Take the nonzero rows of the row-reduced echelon form as a basis.

### 5. Find left null space

Solve

$$
A^Ty=0.
$$

### 6. Calculate dimensions

If $A$ is $m\times n$ with rank $r$:

$$
\boxed{
\begin{aligned}
\dim C(A)&=r\\
\dim N(A)&=n-r\\
\dim C(A^T)&=r\\
\dim N(A^T)&=m-r
\end{aligned}}
$$

---

# 26. The Entire Lecture in 6 Equations

If you remember nothing else, remember these:

$$
\boxed{C(A)=\operatorname{span}(\text{columns of }A)}
$$

$$
\boxed{N(A)=\{x:Ax=0\}}
$$

$$
\boxed{\operatorname{Row}(A)=C(A^T)}
$$

$$
\boxed{N(A^T)=\{y:A^Ty=0\}}
$$

$$
\boxed{\operatorname{rank}(A)+\operatorname{nullity}(A)=n}
$$

$$
\boxed{\operatorname{rank}(A)+\operatorname{nullity}(A^T)=m}
$$

And the dimensions:

$$
\boxed{
\underbrace{r}_{\text{column}}
+
\underbrace{(n-r)}_{\text{null}}
=n
}
$$

$$
\boxed{
\underbrace{r}_{\text{row}}
+
\underbrace{(m-r)}_{\text{left null}}
=m
}
$$

That is the mathematical skeleton of the entire lecture.