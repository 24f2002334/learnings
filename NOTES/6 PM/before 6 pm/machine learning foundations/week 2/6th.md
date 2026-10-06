# you asked

message time: 2026-10-06 18:59:00

Hello, everyone, and welcome to another  lecture on machine learning foundations.   this is the transcript of my lecture explain everything properly

---

# chatgpt response

Absolutely. This lecture is **very important for machine learning**, because it takes the gradient from being just “a vector of partial derivatives” and gives it several **geometric meanings**.

The lecture develops four major interpretations:

1. **Gradient → linear approximation**
2. **Gradient → tangent plane**
3. **Gradient → perpendicular to contour/level sets**
4. **Gradient → direction of steepest ascent**

Then it connects the gradient to:

5. **Directional derivatives**
6. **Cauchy–Schwarz inequality**
7. **Descent directions**
8. **Hessian and quadratic approximation**
9. **Critical points and optimization**

I'll build everything from the basics and show how all these ideas connect.

---

# 1. Starting point: what is a gradient?

In the previous lecture, you learned that for

$$
f:\mathbb R^d\rightarrow\mathbb R,
$$

the gradient is the vector containing all the partial derivatives:

$$
\boxed{
\nabla f(\mathbf v)
=
\begin{bmatrix}
\frac{\partial f}{\partial x_1}(\mathbf v)\\
\frac{\partial f}{\partial x_2}(\mathbf v)\\
\vdots\\
\frac{\partial f}{\partial x_d}(\mathbf v)
\end{bmatrix}
}
$$

For example, if

$$
f(x_1,x_2)=x_1^2+x_2^2,
$$

then

$$
\frac{\partial f}{\partial x_1}=2x_1,
\qquad
\frac{\partial f}{\partial x_2}=2x_2.
$$

Therefore,

$$
\boxed{
\nabla f(x_1,x_2)=
\begin{bmatrix}
2x_1\\
2x_2
\end{bmatrix}
}
$$

That is the **computational interpretation** of the gradient.

This lecture asks:

> What does this vector actually *mean geometrically*?

---

# 2. First interpretation: gradient gives the linear approximation

You already know the one-dimensional linear approximation.

For

$$
f:\mathbb R\rightarrow\mathbb R,
$$

around $x^*$,

$$
\boxed{
f(x)\approx f(x^*)+
f'(x^*)(x-x^*)
}
$$

This says:

> Near $x^*$, we can replace the complicated function by a straight line.

The closer $x$ is to $x^*$, the better the approximation generally is.

---

# 3. What changes in multiple dimensions?

Now suppose

$$
f:\mathbb R^d\rightarrow\mathbb R.
$$

Instead of a number $x^*$, we have a vector:

$$
\mathbf v.
$$

And instead of moving along a one-dimensional line, we can move in many directions.

The multivariable version is:

$$
\boxed{
f(\mathbf x)
\approx
f(\mathbf v)
+
\nabla f(\mathbf v)^T(\mathbf x-\mathbf v)
}
$$

This is the most important formula of the lecture.

The lecture gives exactly this linear approximation and then expands the dot product into the individual partial derivatives. 

---

# 4. Understanding every part of this formula

Look at:

$$
f(\mathbf x)
\approx
f(\mathbf v)
+
\nabla f(\mathbf v)^T(\mathbf x-\mathbf v).
$$

There are three pieces.

### Piece 1:

$$
f(\mathbf v)
$$

This is the actual function value at the point where we're approximating.

---

### Piece 2:

$$
\mathbf x-\mathbf v
$$

This tells us:

> How far have we moved from the approximation point $\mathbf v$?

---

### Piece 3:

$$
\nabla f(\mathbf v)^T(\mathbf x-\mathbf v)
$$

This tells us approximately how much the function value changes because of that movement.

So conceptually:

$$
\boxed{
\text{new value}
\approx
\text{old value}
+
\text{change}
}
$$

---

# 5. Expanding the gradient formula

Suppose $d=2$.

Then:

$$
\nabla f(\mathbf v)
=
\begin{bmatrix}
\frac{\partial f}{\partial x_1}(\mathbf v)\\
\frac{\partial f}{\partial x_2}(\mathbf v)
\end{bmatrix}.
$$

And

$$
\mathbf x-\mathbf v
=
\begin{bmatrix}
x_1-v_1\\
x_2-v_2
\end{bmatrix}.
$$

Therefore:

$$
\nabla f(\mathbf v)^T(\mathbf x-\mathbf v)
$$

becomes

$$
\frac{\partial f}{\partial x_1}(\mathbf v)(x_1-v_1)
+
\frac{\partial f}{\partial x_2}(\mathbf v)(x_2-v_2).
$$

Thus:

$$
\boxed{
f(\mathbf x)\approx
f(\mathbf v)
+
\frac{\partial f}{\partial x_1}(\mathbf v)(x_1-v_1)
+
\frac{\partial f}{\partial x_2}(\mathbf v)(x_2-v_2)
}
$$

This is simply the multivariable version of the ordinary tangent-line approximation.

---

# 6. Why can we add the two changes?

This is an important intuition from the lecture.

Suppose you're at

$$
(v_1,v_2).
$$

First, change $x_1$ while keeping $x_2$ fixed.

The approximate change is

$$
\frac{\partial f}{\partial x_1}(\mathbf v)(y_1-v_1).
$$

Then change $x_2$ while keeping $x_1$ fixed.

The approximate change is

$$
\frac{\partial f}{\partial x_2}(\mathbf v)(y_2-v_2).
$$

If both changes are small, the total first-order change is approximately their sum:

$$
\boxed{
\Delta f
\approx
\frac{\partial f}{\partial x_1}(\mathbf v)(y_1-v_1)
+
\frac{\partial f}{\partial x_2}(\mathbf v)(y_2-v_2)
}
$$

That's why the gradient naturally appears.

---

# 7. Example: $f(x_1,x_2)=x_1^2+x_2^2$

The lecturer uses:

$$
\boxed{
f(x_1,x_2)=x_1^2+x_2^2
}
$$

and wants the linear approximation around

$$
\boxed{\mathbf v=(6,2)}.
$$

Let's do it carefully.

---

## Step 1: Find $f(\mathbf v)$

$$
f(6,2)=6^2+2^2
$$

$$
=36+4
$$

$$
\boxed{f(\mathbf v)=40}
$$

---

## Step 2: Find the gradient

We already know:

$$
\nabla f(x_1,x_2)
=
\begin{bmatrix}
2x_1\\
2x_2
\end{bmatrix}.
$$

At $(6,2)$:

$$
\nabla f(6,2)
=
\begin{bmatrix}
12\\
4
\end{bmatrix}.
$$

So:

$$
\boxed{\nabla f(\mathbf v)=(12,4)}
$$

---

## Step 3: Apply the formula

$$
f(\mathbf x)
\approx
f(\mathbf v)
+
\nabla f(\mathbf v)^T(\mathbf x-\mathbf v).
$$

Therefore:

$$
f(x_1,x_2)
\approx
40+
\begin{bmatrix}
12&4
\end{bmatrix}
\begin{bmatrix}
x_1-6\\
x_2-2
\end{bmatrix}.
$$

Take the dot product:

$$
=40+12(x_1-6)+4(x_2-2).
$$

Expand:

$$
=40+12x_1-72+4x_2-8.
$$

Therefore:

$$
\boxed{
L_{\mathbf v}f(x_1,x_2)
=
12x_1+4x_2-40
}
$$

This is exactly the approximation obtained in the lecture.

---

# 8. What does this approximation actually mean?

The original function is

$$
f(x_1,x_2)=x_1^2+x_2^2.
$$

That's a curved surface.

The approximation is

$$
L_{\mathbf v}f(x_1,x_2)
=
12x_1+4x_2-40.
$$

That's a **plane**.

So:

$$
\boxed{
\text{curved function}
\quad\longrightarrow\quad
\text{local plane}
}
$$

near $(6,2)$.

This plane is a good approximation only **near $(6,2)$**.

Far away from $(6,2)$, the approximation becomes less accurate.

---

# 9. A crucial property: exact at the approximation point

There's something very important about linear approximation.

At the point where you constructed the approximation,

$$
\boxed{
L_{\mathbf v}f(\mathbf v)=f(\mathbf v)
}
$$

It must match the original function exactly there.

For our example:

$$
f(6,2)=40.
$$

And:

$$
L_{\mathbf v}f(6,2)
=
12(6)+4(2)-40
$$

$$
=72+8-40
$$

$$
=40.
$$

So:

$$
\boxed{
L_{\mathbf v}f(6,2)=f(6,2)=40
}
$$

The lecture emphasizes this property. 

---

# 10. Why does the approximation depend on the point?

Suppose we approximate around:

$$
(6,2).
$$

We get one plane:

$$
12x_1+4x_2-40.
$$

But if we approximate around:

$$
(-6,2),
$$

we get a **different plane**.

Why?

Because the gradient depends on the point.

For our function:

$$
\nabla f(x_1,x_2)=(2x_1,2x_2).
$$

At $(6,2)$:

$$
(12,4).
$$

At $(-6,2)$:

$$
(-12,4).
$$

Therefore the local behavior is different.

---

# 11. Second interpretation: tangent plane

In one-variable calculus:

- graph of $f(x)$ = curve
- linear approximation = tangent line

In multivariable calculus:

- graph of $f(x_1,x_2)$ = surface
- linear approximation = tangent plane

So:

$$
\boxed{
\text{tangent line in 1D}
\quad\longrightarrow\quad
\text{tangent plane in 2D}
}
$$

The lecture explains that the graph of the linear approximation is a plane that touches the original surface at the point

$$
(\mathbf v,f(\mathbf v)).
$$



---

# 12. Why is it called a tangent plane?

Take the surface

$$
z=f(x_1,x_2).
$$

At the point

$$
(x_1,x_2)=(6,2),
$$

the height is:

$$
z=40.
$$

So the point on the 3D surface is:

$$
\boxed{(6,2,40)}.
$$

The tangent plane touches the surface at exactly this point.

The tangent plane is:

$$
\boxed{z=12x_1+4x_2-40}.
$$

So the gradient determines the local plane.

---

# 13. Important distinction: approximation vs exact equality

You should be very careful with this.

Generally:

$$
\boxed{
f(\mathbf x)\approx L_{\mathbf v}f(\mathbf x)
}
$$

when $\mathbf x$ is close to $\mathbf v$.

But at the specific point $\mathbf v$:

$$
\boxed{
f(\mathbf v)=L_{\mathbf v}f(\mathbf v)
}
$$

exactly.

So don't say:

$$
f(x)=L_{\mathbf v}f(x)
$$

everywhere.

That's false.

---

# 14. Third interpretation: gradient is perpendicular to contour lines

This is one of the most useful geometric meanings of the gradient.

First, what is a **contour** or **level set**?

For a function $f$, a level set corresponding to value $c$ is:

$$
\boxed{
\{\mathbf x:f(\mathbf x)=c\}
}
$$

In two dimensions, these usually appear as **contour lines**.

For example:

$$
f(x_1,x_2)=x_1^2+x_2^2.
$$

Set

$$
f(x_1,x_2)=40.
$$

Then:

$$
x_1^2+x_2^2=40.
$$

This is a circle.

Every point on this circle has exactly the same function value:

$$
f=40.
$$

---

# 15. What does the gradient do at a contour?

The lecture's key statement is:

$$
\boxed{
\nabla f(\mathbf v)
\text{ is perpendicular to the level set through }\mathbf v
}
$$

under the appropriate regularity conditions discussed in the lecture.

For our example, at

$$
\mathbf v=(-6,2),
$$

the gradient is:

$$
\nabla f(-6,2)
=
\begin{bmatrix}
-12\\
4
\end{bmatrix}.
$$

The contour through this point is:

$$
x_1^2+x_2^2=40.
$$

The vector

$$
(-12,4)
$$

points perpendicular to that circle at $(-6,2)$.

---

# 16. Why should the gradient be perpendicular to a contour?

Let's think intuitively.

A contour represents points where:

$$
f(\mathbf x)=\text{constant}.
$$

If you move **along the contour**, the function value doesn't change.

So:

$$
\text{change in }f=0.
$$

But the gradient tells us how $f$ changes.

Therefore, the gradient must point in a direction that is perpendicular to the direction you're travelling along the contour.

Otherwise, there would be some component of the gradient along the contour, causing $f$ to change.

So:

$$
\boxed{
\text{along contour: no change}
}
$$

while

$$
\boxed{
\text{gradient: direction of greatest change}
}
$$

and therefore:

$$
\boxed{
\text{gradient}\perp\text{contour}.
}
$$

---

# 17. The algebraic proof from the lecture

The lecturer first proves the corresponding statement for the **linear approximation**.

The linear approximation is:

$$
L_{\mathbf v}f(\mathbf x)
=
f(\mathbf v)
+
\nabla f(\mathbf v)^T(\mathbf x-\mathbf v).
$$

Consider the set where:

$$
L_{\mathbf v}f(\mathbf x)=f(\mathbf v).
$$

Substitute:

$$
f(\mathbf v)
+
\nabla f(\mathbf v)^T(\mathbf x-\mathbf v)
=
f(\mathbf v).
$$

Cancel $f(\mathbf v)$:

$$
\nabla f(\mathbf v)^T(\mathbf x-\mathbf v)=0.
$$

So:

$$
\nabla f(\mathbf v)^T\mathbf x
=
\nabla f(\mathbf v)^T\mathbf v.
$$

Compare this with the general plane equation:

$$
\mathbf w^T\mathbf x=b.
$$

We can identify:

$$
\mathbf w=\nabla f(\mathbf v).
$$

Therefore the gradient is the **normal vector of that plane**, meaning it is perpendicular to the plane.

The lecture specifically derives this relationship. 

---

# 18. Fourth interpretation: directional derivative

Now we get to another extremely important concept.

Suppose:

$$
f:\mathbb R^d\rightarrow\mathbb R.
$$

You're standing at a point:

$$
\mathbf v.
$$

You choose a direction:

$$
\mathbf u.
$$

The **directional derivative** asks:

> How quickly does $f$ change if I move from $\mathbf v$ in direction $\mathbf u$?

It is defined as:

$$
\boxed{
D_{\mathbf u}f(\mathbf v)
=
\lim_{\alpha\to0}
\frac{
f(\mathbf v+\alpha\mathbf u)-f(\mathbf v)
}{\alpha}
}
$$

---

# 19. Understanding the directional derivative formula

Start at:

$$
\mathbf v.
$$

Move a small distance $\alpha$ in direction $\mathbf u$:

$$
\mathbf v+\alpha\mathbf u.
$$

Then calculate:

$$
f(\mathbf v+\alpha\mathbf u)-f(\mathbf v).
$$

That's the change in function value.

Divide by:

$$
\alpha
$$

to get the rate of change.

Then let:

$$
\alpha\rightarrow0.
$$

That's exactly analogous to the ordinary derivative.

---

# 20. The amazing result: directional derivative = gradient dot direction

Now use the linear approximation:

$$
f(\mathbf v+\alpha\mathbf u)
\approx
f(\mathbf v)
+
\nabla f(\mathbf v)^T(\alpha\mathbf u).
$$

Therefore:

$$
f(\mathbf v+\alpha\mathbf u)-f(\mathbf v)
\approx
\alpha\nabla f(\mathbf v)^T\mathbf u.
$$

Divide by $\alpha$:

$$
\frac{
f(\mathbf v+\alpha\mathbf u)-f(\mathbf v)
}{\alpha}
\approx
\nabla f(\mathbf v)^T\mathbf u.
$$

Taking the limit gives:

$$
\boxed{
D_{\mathbf u}f(\mathbf v)
=
\nabla f(\mathbf v)^T\mathbf u
}
$$

This is one of the **most important equations in multivariable calculus**.

---

# 21. What does the dot product tell us?

We have:

$$
D_{\mathbf u}f(\mathbf v)
=
\nabla f(\mathbf v)^T\mathbf u.
$$

So the rate of change in a direction is determined by the **dot product between the gradient and that direction**.

Therefore:

### Positive dot product

$$
\nabla f(\mathbf v)^T\mathbf u>0
$$

means:

$$
\boxed{\text{function increases}}
$$

in direction $\mathbf u$.

### Negative dot product

$$
\nabla f(\mathbf v)^T\mathbf u<0
$$

means:

$$
\boxed{\text{function decreases}}
$$

in direction $\mathbf u$.

### Zero dot product

$$
\nabla f(\mathbf v)^T\mathbf u=0
$$

means:

$$
\boxed{\text{no first-order change}}
$$

in that direction.

---

# 22. Why does this matter for machine learning?

Suppose you have a loss function:

$$
L(\mathbf w).
$$

You are currently at:

$$
\mathbf w=\mathbf v.
$$

You want to decrease the loss.

You need to decide:

> Which direction should I move?

The directional derivative gives exactly the answer to:

> How quickly will the loss change if I move in direction $\mathbf u$?

That's why this concept leads naturally to **gradient descent**.

---

# 23. Cauchy–Schwarz inequality

Now the lecturer takes a small mathematical detour.

We have:

$$
\nabla f(\mathbf v)^T\mathbf u.
$$

This is an inner product/dot product.

The lecturer wants to know:

> How large or small can this dot product become?

For two vectors $\mathbf a,\mathbf b$:

$$
\boxed{
-\|\mathbf a\|\|\mathbf b\|
\leq
\mathbf a^T\mathbf b
\leq
\|\mathbf a\|\|\mathbf b\|
}
$$

This is the **Cauchy–Schwarz inequality**.

Here,

$$
\|\mathbf a\|
=
\sqrt{a_1^2+a_2^2+\cdots+a_d^2}.
$$

That's the ordinary Euclidean norm.

---

# 24. When does Cauchy–Schwarz become equality?

The upper bound:

$$
\mathbf a^T\mathbf b
=
\|\mathbf a\|\|\mathbf b\|
$$

occurs when the vectors point in the **same direction**.

That means:

$$
\mathbf a=\alpha\mathbf b
$$

with

$$
\alpha>0.
$$

The lower bound:

$$
\mathbf a^T\mathbf b
=
-\|\mathbf a\|\|\mathbf b\|
$$

occurs when they point in **opposite directions**:

$$
\mathbf a=\alpha\mathbf b,
\qquad
\alpha<0.
$$

---

# 25. Fifth interpretation: gradient = direction of steepest ascent

Now we reach perhaps the most important geometric interpretation.

Suppose you're at:

$$
\mathbf v.
$$

You want to maximize $f$.

You want to choose a direction $\mathbf u$ such that:

$$
D_{\mathbf u}f(\mathbf v)
$$

is as large as possible.

But:

$$
D_{\mathbf u}f(\mathbf v)
=
\nabla f(\mathbf v)^T\mathbf u.
$$

So we want to maximize:

$$
\nabla f(\mathbf v)^T\mathbf u.
$$

But there is one problem.

---

# 26. Why must we restrict $\mathbf u$ to unit length?

Suppose we didn't.

Then if $\mathbf u$ gives a positive increase, we could simply make $\mathbf u$ 100 times longer and get a value 100 times larger.

That wouldn't really tell us the best **direction**.

So we impose:

$$
\boxed{\|\mathbf u\|=1}
$$

Now we're comparing directions fairly.

---

# 27. Apply Cauchy–Schwarz

We want:

$$
\max_{\|\mathbf u\|=1}
\nabla f(\mathbf v)^T\mathbf u.
$$

By Cauchy–Schwarz:

$$
\nabla f(\mathbf v)^T\mathbf u
\leq
\|\nabla f(\mathbf v)\|\|\mathbf u\|.
$$

Since:

$$
\|\mathbf u\|=1,
$$

we get:

$$
\nabla f(\mathbf v)^T\mathbf u
\leq
\|\nabla f(\mathbf v)\|.
$$

Equality occurs when $\mathbf u$ points in the same direction as the gradient.

Therefore:

$$
\boxed{
\mathbf u_{\text{steepest ascent}}
=
\frac{\nabla f(\mathbf v)}
{\|\nabla f(\mathbf v)\|}
}
$$

So the gradient points in the direction of **steepest ascent**.

---

# 28. What exactly does "steepest ascent" mean?

It means:

> Among all unit-length directions, the gradient points in the direction in which the function increases the fastest.

Notice the distinction:

### Gradient itself

$$
\nabla f(\mathbf v)
$$

contains both:

- direction
- magnitude

### Unit gradient

$$
\frac{\nabla f(\mathbf v)}
{\|\nabla f(\mathbf v)\|}
$$

contains only the direction.

So when we say:

> "The gradient is the direction of steepest ascent"

we often mean its **direction**.

---

# 29. Example of steepest ascent

Take:

$$
f(x_1,x_2)=x_1^2+x_2^2.
$$

At:

$$
\mathbf v=(3,4),
$$

the gradient is:

$$
\nabla f(3,4)
=
\begin{bmatrix}
6\\8
\end{bmatrix}.
$$

Its magnitude is:

$$
\sqrt{6^2+8^2}
=
10.
$$

Therefore the unit direction of steepest ascent is:

$$
\frac{1}{10}
\begin{bmatrix}
6\\8
\end{bmatrix}
=
\begin{bmatrix}
0.6\\0.8
\end{bmatrix}.
$$

So:

$$
\boxed{
\mathbf u_{\text{steepest ascent}}=(0.6,0.8)
}
$$

---

# 30. What is the steepest descent direction?

If:

$$
\nabla f
$$

points toward steepest increase, then the opposite direction points toward steepest decrease.

Therefore:

$$
\boxed{
\mathbf u_{\text{steepest descent}}
=
-\frac{\nabla f}{\|\nabla f\|}
}
$$

This is the fundamental idea behind **gradient descent**.

---

# 31. Descent directions

The lecturer goes slightly beyond just the single steepest descent direction.

Suppose you're at:

$$
\mathbf v.
$$

You want to know:

> Which directions will decrease $f$?

We know:

$$
D_{\mathbf u}f(\mathbf v)
=
\nabla f(\mathbf v)^T\mathbf u.
$$

For the function to decrease:

$$
D_{\mathbf u}f(\mathbf v)<0.
$$

Therefore:

$$
\boxed{
\nabla f(\mathbf v)^T\mathbf u<0
}
$$

defines a **descent direction**.

So the set of descent directions is:

$$
\boxed{
\{\mathbf u:
\nabla f(\mathbf v)^T\mathbf u<0\}
}
$$

---

# 32. Visualizing descent directions

Imagine the gradient points northeast.

Then:

- directions roughly northeast → function increases
- directions perpendicular to gradient → no first-order change
- directions southwest → function decreases

The exact steepest descent direction is directly opposite the gradient.

But many other directions can also decrease the function.

That's why there isn't just one descent direction.

---

# 33. Connection to gradient descent in ML

Suppose your loss is:

$$
L(\mathbf w).
$$

You want to minimize it.

At the current parameter vector $\mathbf w$, calculate:

$$
\nabla L(\mathbf w).
$$

This points toward increasing loss.

Therefore move in the opposite direction:

$$
\boxed{
\mathbf w_{\text{new}}
=
\mathbf w-\eta\nabla L(\mathbf w)
}
$$

where $\eta>0$ is the learning rate.

This is the basic gradient descent update.

The transcript focuses on the geometric reasoning that leads to this idea rather than developing the full algorithm yet.

---

# 34. Sixth topic: higher-order approximation

The lecturer then briefly revisits something from the previous lecture.

The first-order approximation is:

$$
\boxed{
f(\mathbf x)
\approx
f(\mathbf v)
+
\nabla f(\mathbf v)^T(\mathbf x-\mathbf v)
}
$$

But we can go beyond the linear approximation.

In one variable, you learned:

$$
f(x)
\approx
f(v)+f'(v)(x-v)
+
\frac12f''(v)(x-v)^2.
$$

In multiple dimensions, the corresponding second-order approximation is:

$$
\boxed{
f(\mathbf x)
\approx
f(\mathbf v)
+
\nabla f(\mathbf v)^T(\mathbf x-\mathbf v)
+
\frac12
(\mathbf x-\mathbf v)^T
H_f(\mathbf v)
(\mathbf x-\mathbf v)
}
$$

where:

$$
\boxed{H_f(\mathbf v)}
$$

is the **Hessian matrix**.

---

# 35. What is the Hessian?

The gradient contains first derivatives:

$$
\nabla f=
\begin{bmatrix}
f_{x_1}\\
f_{x_2}\\
\vdots\\
f_{x_d}
\end{bmatrix}.
$$

The Hessian contains **second derivatives**.

For two variables:

$$
H_f=
\begin{bmatrix}
\frac{\partial^2f}{\partial x_1^2}
&
\frac{\partial^2f}{\partial x_1\partial x_2}
\\[4pt]
\frac{\partial^2f}{\partial x_2\partial x_1}
&
\frac{\partial^2f}{\partial x_2^2}
\end{bmatrix}.
$$

So:

$$
\boxed{
\text{gradient = first-order information}
}
$$

while

$$
\boxed{
\text{Hessian = second-order information}
}
$$

The lecturer notes that the Hessian is a $d\times d$ matrix and that more advanced optimization methods can use quadratic approximations, although most ML work in this course will focus on linear approximations. 

---

# 36. Why do we need the Hessian?

The gradient tells us:

> Which way is the function changing?

The Hessian tells us more about:

> How is that change itself changing?

In other words, it gives information about the **curvature** of the function.

That's why second-order optimization methods can sometimes make more sophisticated decisions than ordinary gradient descent.

---

# 37. Seventh topic: critical points

Now the lecture connects gradients to maxima and minima.

In one-variable calculus, you learned:

$$
f'(x^*)=0
$$

at an interior local maximum or minimum.

The multivariable equivalent is:

$$
\boxed{
\nabla f(\mathbf v)=\mathbf 0
}
$$

where

$$
\mathbf 0=
\begin{bmatrix}
0\\
0\\
\vdots\\
0
\end{bmatrix}.
$$

The important point is that this is a **zero vector**, not just the scalar number $0$.

---

# 38. What is a critical point?

A point satisfying

$$
\boxed{\nabla f(\mathbf v)=\mathbf0}
$$

is called a **critical point**.

So the set of critical points is:

$$
\boxed{
\{\mathbf v:\nabla f(\mathbf v)=\mathbf0\}
}
$$

The lecturer emphasizes this definition. 

---

# 39. Why does a minimum have zero gradient?

Imagine standing at the bottom of a bowl.

At the exact bottom, there is no direction in which you can make a tiny movement and immediately go downward.

So there is no first-order direction of decrease.

Therefore:

$$
\nabla f(\mathbf v)=0.
$$

Similarly, at the top of a hill:

$$
\nabla f(\mathbf v)=0.
$$

---

# 40. But gradient = 0 does NOT necessarily mean minimum

This is extremely important.

The lecturer explicitly says:

$$
\boxed{
\nabla f(\mathbf v)=0
\not\Rightarrow
\mathbf v\text{ is a minimum}
}
$$

A critical point can be:

- local minimum
- local maximum
- saddle point

So finding:

$$
\nabla f=0
$$

only gives you **candidate points**.

You still need further analysis.

---

# 41. Example of a critical point that is not a minimum

Consider:

$$
f(x,y)=x^2-y^2.
$$

Calculate the gradient:

$$
\nabla f(x,y)
=
\begin{bmatrix}
2x\\
-2y
\end{bmatrix}.
$$

Set it equal to zero:

$$
2x=0,
\qquad
-2y=0.
$$

Therefore:

$$
(x,y)=(0,0).
$$

So $(0,0)$ is a critical point.

But is it a minimum?

No.

Along the $x$-axis:

$$
f(x,0)=x^2,
$$

which increases away from zero.

But along the $y$-axis:

$$
f(0,y)=-y^2,
$$

which decreases away from zero.

So the point is a **saddle point**.

This illustrates why:

$$
\nabla f=0
$$

is only a necessary condition for an interior optimum, not a sufficient condition.

---

# 42. First-order necessary condition for optimality

The lecturer calls:

$$
\boxed{
\nabla f(\mathbf v)=0
}
$$

the **first-order necessary condition for optimality**.

"Necessary" means:

> If an appropriate interior point is a differentiable local optimum, then its gradient must be zero.

But it does **not** mean:

> Every point with gradient zero is an optimum.

That's the distinction you should remember.

---

# 43. The entire lecture in one chain

This is the most important part.

Everything you've learned connects together:

### Step 1: Partial derivatives

$$
\frac{\partial f}{\partial x_1},
\ldots,
\frac{\partial f}{\partial x_d}
$$

tell us how the function changes in each coordinate direction.

↓

### Step 2: Put them together

$$
\boxed{\nabla f}
$$

This gives the gradient.

↓

### Step 3: Linear approximation

$$
\boxed{
f(\mathbf x)
\approx
f(\mathbf v)
+
\nabla f(\mathbf v)^T(\mathbf x-\mathbf v)
}
$$

The gradient completely determines the local linear approximation.

↓

### Step 4: Tangent plane

The graph of this linear approximation is the **tangent plane**.

↓

### Step 5: Directional derivative

For any direction $\mathbf u$:

$$
\boxed{
D_{\mathbf u}f(\mathbf v)
=
\nabla f(\mathbf v)^T\mathbf u
}
$$

↓

### Step 6: Cauchy–Schwarz

The largest possible dot product with a unit vector occurs when that vector points in the same direction as the gradient.

↓

### Step 7: Steepest ascent

$$
\boxed{
\mathbf u_{\text{ascent}}
=
\frac{\nabla f}{\|\nabla f\|}
}
$$

↓

### Step 8: Steepest descent

$$
\boxed{
\mathbf u_{\text{descent}}
=
-\frac{\nabla f}{\|\nabla f\|}
}
$$

↓

### Step 9: Optimization

To minimize a function, move in a descent direction.

↓

### Step 10: Critical points

At an interior optimum:

$$
\boxed{\nabla f=0}
$$

---

# 44. The four interpretations of the gradient

You should be able to recognize these immediately in an exam.

## Interpretation 1 — Computational

$$
\boxed{
\nabla f=
\text{vector of all partial derivatives}
}
$$

---

## Interpretation 2 — Linear approximation

$$
\boxed{
f(\mathbf x)
\approx
f(\mathbf v)
+
\nabla f(\mathbf v)^T(\mathbf x-\mathbf v)
}
$$

The gradient determines the local linear approximation.

---

## Interpretation 3 — Normal to contour

$$
\boxed{
\nabla f(\mathbf v)
\perp
\text{level set through }\mathbf v
}
$$

The gradient points perpendicular to the contour.

---

## Interpretation 4 — Steepest ascent

$$
\boxed{
\nabla f(\mathbf v)
\text{ points in the direction of maximum increase}
}
$$

This is perhaps the most important interpretation for optimization.

---

# 45. A very useful mental picture

Imagine a mountain.

Your position is:

$$
\mathbf v.
$$

The mountain height is:

$$
f(\mathbf v).
$$

### Gradient

The gradient points in the direction where you climb **most rapidly**.

### Negative gradient

$$
-\nabla f
$$

points in the direction where you descend most rapidly.

### Contour

A contour is like a line drawn around the mountain connecting locations with the same height.

The gradient crosses that contour at $90^\circ$.

### Linear approximation

If you zoom in extremely close to your current location, the mountain surface looks approximately like a flat plane.

That's the tangent plane.

### Critical point

At the top/bottom/appropriate saddle-type flat point:

$$
\nabla f=0.
$$

This one mental picture ties almost the entire lecture together.

---

# 46. Exam-ready formula sheet

### Multivariable linear approximation

$$
\boxed{
L_{\mathbf v}f(\mathbf x)
=
f(\mathbf v)
+
\nabla f(\mathbf v)^T(\mathbf x-\mathbf v)
}
$$

### Expanded form

$$
\boxed{
L_{\mathbf v}f(\mathbf x)
=
f(\mathbf v)
+
\sum_{i=1}^d
\frac{\partial f}{\partial x_i}(\mathbf v)
(x_i-v_i)
}
$$

### Directional derivative

$$
\boxed{
D_{\mathbf u}f(\mathbf v)
=
\nabla f(\mathbf v)^T\mathbf u
}
$$

### Cauchy–Schwarz

$$
\boxed{
|\mathbf a^T\mathbf b|
\leq
\|\mathbf a\|\|\mathbf b\|
}
$$

### Steepest ascent

$$
\boxed{
\frac{\nabla f(\mathbf v)}
{\|\nabla f(\mathbf v)\|}
}
$$

### Steepest descent

$$
\boxed{
-\frac{\nabla f(\mathbf v)}
{\|\nabla f(\mathbf v)\|}
}
$$

### Descent direction

$$
\boxed{
\nabla f(\mathbf v)^T\mathbf u<0
}
$$

### Second-order approximation

$$
\boxed{
f(\mathbf x)\approx
f(\mathbf v)
+
\nabla f(\mathbf v)^T(\mathbf x-\mathbf v)
+
\frac12
(\mathbf x-\mathbf v)^T
H_f(\mathbf v)
(\mathbf x-\mathbf v)
}
$$

### Critical point

$$
\boxed{
\nabla f(\mathbf v)=\mathbf0
}
$$

---

## The one sentence you should remember

> **The gradient tells you how a multivariable function changes locally: it determines the tangent plane, points perpendicular to the contours, gives directional derivatives through a dot product, and points toward the direction of steepest ascent.**

That is the central idea connecting essentially every part of this lecture.