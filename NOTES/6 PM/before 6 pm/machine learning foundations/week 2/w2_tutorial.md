# you asked

message time: 2026-10-06 19:00:58

hello and welcome to this tutorial on
week 2 contents of machine learning
foundations course
in this tutorial we would be solving
some problems from the topics linear
approximation higher order
approximations multivariate linear
approximation and directional
derivatives
 these were some of the example
problems on the topics that were covered
in the lecture i hope you were able to
understand
thank you  , this is the transcript of  a tutorial explain everything properly

---

# chatgpt response

Absolutely. This tutorial is essentially a **problem-solving companion to the lecture you just shared**. It takes the theory of linear approximation, higher-order approximation, multivariate approximation, and directional derivatives and shows you **how to actually solve problems**.

I'll explain the concepts first, then work through the examples step by step, including **why each step is being done**.

---

# 1. The big picture

This tutorial covers four main topics:

1. **Linear approximation**
2. **Higher-order approximation**
3. **Multivariate linear approximation**
4. **Directional derivatives**

The common idea behind all of them is:

> A complicated function can often be approximated locally by something simpler.

For example:

$$
\text{complicated curve}
\quad\rightarrow\quad
\text{straight line}
$$

or

$$
\text{complicated surface}
\quad\rightarrow\quad
\text{plane}.
$$

The important word is **locally**.

An approximation that is excellent near one point can become poor when you move far away from that point.

---

# 2. Linear approximation

## 2.1 What is the basic idea?

Suppose you have a nonlinear function:

$$
f(x).
$$

Its graph may be curved.

But if you zoom in sufficiently close to a particular point $x=a$, the curve looks almost like a straight line.

That straight line is the **tangent line**.

Therefore, instead of evaluating the complicated function directly, we can use the tangent line to estimate its value.

This is called:

- linear approximation
- linearization
- local linear approximation
- tangent-line approximation

They all refer to essentially the same idea in this context.

---

# 3. The linear approximation formula

The equation is:

$$
\boxed{
L(x)=f(a)+f'(a)(x-a)
}
$$

This is one of the formulas you should memorize.

Let's understand where it comes from.

The equation of a straight line is:

$$
y-y_1=m(x-x_1).
$$

or:

$$
y=y_1+m(x-x_1).
$$

For the tangent line:

- the point is $(a,f(a))$
- the slope is $f'(a)$

Therefore:

$$
y=f(a)+f'(a)(x-a).
$$

Since we're using this line to approximate $f(x)$:

$$
\boxed{
f(x)\approx f(a)+f'(a)(x-a)
}
$$

---

# 4. What do $a$, $f(a)$, and $f'(a)$ mean?

This is very important.

### $a$

This is the **point around which you're approximating**.

### $f(a)$

This is the exact function value at the approximation point.

### $f'(a)$

This is the slope of the function at $a$.

### $x-a$

This tells us how far we've moved from the approximation point.

So:

$$
\boxed{
\text{approximate value}
=
\text{known value}
+
\text{slope}\times\text{distance moved}
}
$$

That's exactly what the formula says.

---

# 5. Why must $x$ be close to $a$?

Suppose we construct a tangent line at $a$.

Right next to $a$, the curve and tangent line are extremely close.

But if you move far away, the curve bends while the tangent line remains straight.

Therefore:

$$
\boxed{
x\approx a
}
$$

is an important condition.

The farther $x$ is from $a$, generally the larger the approximation error becomes.

This is why linear approximation is called a **local** approximation.

---

# 6. Example 1: approximate $\sqrt{50}$

We want:

$$
\sqrt{50}.
$$

Directly calculating it might not be convenient if we don't have a calculator.

So define:

$$
f(x)=\sqrt{x}.
$$

We want:

$$
f(50).
$$

---

## Step 1: Choose a nearby convenient point

We need a value near 50 whose square root we already know.

The obvious choice is:

$$
49.
$$

because:

$$
\sqrt{49}=7.
$$

Therefore:

$$
\boxed{a=49}
$$

This is one of the most important steps in linear approximation:

> Choose a nearby point where the function is easy to evaluate.

---

# 7. Step 2: Find the derivative

We have:

$$
f(x)=\sqrt{x}=x^{1/2}.
$$

Therefore:

$$
f'(x)=\frac12x^{-1/2}
$$

or:

$$
\boxed{
f'(x)=\frac{1}{2\sqrt{x}}
}
$$

At $a=49$:

$$
f'(49)=\frac{1}{2\sqrt{49}}
$$

$$
=\frac1{14}.
$$

---

# 8. Step 3: Apply the formula

Recall:

$$
L(x)=f(a)+f'(a)(x-a).
$$

Therefore:

$$
L(x)
=
7+\frac1{14}(x-49).
$$

So:

$$
\boxed{
L(x)=7+\frac{x-49}{14}
}
$$

This is our tangent-line approximation.

---

# 9. Step 4: Use it to calculate $\sqrt{50}$

Put:

$$
x=50.
$$

Then:

$$
L(50)
=
7+\frac{50-49}{14}.
$$

Therefore:

$$
=7+\frac1{14}
$$

$$
=7.071428\ldots
$$

So:

$$
\boxed{\sqrt{50}\approx7.071}
$$

The actual value is approximately:

$$
7.071067\ldots
$$

So the approximation is extremely good.

---

# 10. Why did this work so well?

Because:

$$
50
$$

is very close to:

$$
49.
$$

We're using a tangent line constructed at 49 to estimate the function at 50.

The distance is only:

$$
50-49=1.
$$

The tutorial emphasizes that the approximation becomes worse as we move farther from the chosen point.

---

# 11. What happens if we use $x=100$?

Our approximation is:

$$
L(x)=7+\frac{x-49}{14}.
$$

At $x=100$:

$$
L(100)
=
7+\frac{51}{14}.
$$

This gives approximately:

$$
10.643.
$$

But:

$$
\sqrt{100}=10.
$$

So the approximation is quite poor.

Why?

Because $100$ is far away from $49$.

This gives you an important rule:

$$
\boxed{
\text{Closer to }a
\Rightarrow
\text{usually better approximation}
}
$$

---

# 12. Example 2: approximate $e^{0.017}$

Now we want:

$$
e^{0.017}.
$$

Define:

$$
f(x)=e^x.
$$

We want:

$$
f(0.017).
$$

---

## Step 1: Choose $a$

A nearby value where $e^x$ is easy to calculate is:

$$
a=0.
$$

because:

$$
e^0=1.
$$

---

## Step 2: Find the derivative

For:

$$
f(x)=e^x,
$$

we have:

$$
f'(x)=e^x.
$$

Therefore:

$$
f(0)=1
$$

and:

$$
f'(0)=1.
$$

---

# 13. Step 3: Construct the linear approximation

$$
L(x)=f(0)+f'(0)(x-0).
$$

Therefore:

$$
L(x)=1+x.
$$

So:

$$
\boxed{
e^x\approx1+x
}
$$

when $x$ is close to 0.

This is a very famous approximation.

---

# 14. Estimate $e^{0.017}$

Put:

$$
x=0.017.
$$

Then:

$$
e^{0.017}\approx1+0.017.
$$

Therefore:

$$
\boxed{
e^{0.017}\approx1.017
}
$$

Again, because $0.017$ is very close to 0, the approximation is excellent.

---

# 15. What if we use $x=1$?

The approximation gives:

$$
e^1\approx1+1=2.
$$

But the actual value is:

$$
e\approx2.718.
$$

That's a much bigger error.

Again:

$$
1
$$

is much farther from the approximation point $0$ than:

$$
0.017.
$$

---

# 16. Example 3: $f(x)=\sqrt{x+4}$, find $f(6)$

We're given:

$$
f(x)=\sqrt{x+4}.
$$

We want:

$$
f(6).
$$

Direct substitution gives:

$$
f(6)=\sqrt{10}.
$$

We want to approximate this.

---

## Step 1: Choose a nearby convenient $a$

We want $a+4$ to be a perfect square.

Since:

$$
9=3^2,
$$

we want:

$$
a+4=9.
$$

Thus:

$$
a=5.
$$

So:

$$
\boxed{a=5}
$$

and:

$$
f(5)=\sqrt9=3.
$$

---

# 17. Step 2: Find the derivative

$$
f(x)=(x+4)^{1/2}.
$$

Therefore:

$$
f'(x)
=
\frac12(x+4)^{-1/2}
$$

or:

$$
\boxed{
f'(x)=\frac1{2\sqrt{x+4}}
}
$$

At $x=5$:

$$
f'(5)
=
\frac1{2\sqrt9}
=
\frac16.
$$

---

# 18. Step 3: Construct the approximation

$$
L(x)=f(5)+f'(5)(x-5).
$$

Therefore:

$$
\boxed{
L(x)=3+\frac{x-5}{6}
}
$$

---

# 19. Step 4: Calculate $f(6)$

Put $x=6$:

$$
L(6)
=
3+\frac{6-5}{6}.
$$

Therefore:

$$
L(6)
=
3+\frac16
$$

$$
=3.166666\ldots
$$

So:

$$
\boxed{
\sqrt{10}\approx3.1667
}
$$

The actual value is approximately:

$$
3.1623.
$$

So there is a small error.

Again, $6$ is reasonably close to $5$, so the approximation is fairly good.

---

# 20. The general strategy for linear approximation problems

Whenever you see:

> "Use linear approximation to estimate $f(b)$"

follow these steps.

### Step 1

Identify:

$$
f(x)
$$

and the desired point $b$.

### Step 2

Choose a nearby easy point:

$$
a.
$$

### Step 3

Calculate:

$$
f(a).
$$

### Step 4

Calculate:

$$
f'(x).
$$

### Step 5

Calculate:

$$
f'(a).
$$

### Step 6

Write:

$$
\boxed{
L(x)=f(a)+f'(a)(x-a)
}
$$

### Step 7

Substitute the desired value $x=b$.

---

# 21. Higher-order approximations

Now comes the natural question:

> What if the tangent line isn't accurate enough?

Instead of stopping with a straight line, we can include additional terms.

The linear approximation is:

$$
f(x)\approx
f(a)+f'(a)(x-a).
$$

The quadratic approximation adds:

$$
\frac{f''(a)}{2!}(x-a)^2.
$$

So:

$$
\boxed{
f(x)\approx
f(a)+f'(a)(x-a)
+
\frac{f''(a)}{2!}(x-a)^2
}
$$

---

# 22. Why does adding another term help?

A straight line can capture:

- the value of the function
- its slope

But it doesn't capture curvature.

The second derivative tells us about curvature.

So adding:

$$
f''(a)
$$

allows the approximation to bend.

That's why a quadratic approximation can be much better than a straight line.

---

# 23. Third-order approximation

If we add the third derivative:

$$
\boxed{
f(x)\approx
f(a)
+
f'(a)(x-a)
+
\frac{f''(a)}{2!}(x-a)^2
+
\frac{f'''(a)}{3!}(x-a)^3
}
$$

Notice:

$$
2!=2
$$

and:

$$
3!=6.
$$

---

# 24. General Taylor approximation

The general pattern is:

$$
\boxed{
f(x)\approx
f(a)
+
f'(a)(x-a)
+
\frac{f''(a)}{2!}(x-a)^2
+
\frac{f'''(a)}{3!}(x-a)^3
+\cdots
}
$$

This is the beginning of the **Taylor expansion**.

The tutorial doesn't develop the full theory, but that's the mathematical structure behind these higher-order approximations.

---

# 25. Applying higher-order approximation to $\sqrt{x+4}$

Previously we used:

$$
f(x)=\sqrt{x+4}
$$

and:

$$
a=5.
$$

The linear approximation gave approximately:

$$
3.1667
$$

for $f(6)$, while the actual value is approximately:

$$
3.1623.
$$

Now add second- and third-order terms.

The tutorial uses a third-order approximation and obtains approximately:

$$
\boxed{3.1622}
$$

at $x=6$.

That's much closer to the true value.

---

# 26. Why higher-order approximations work better

Think of it this way:

### First order

Uses:

$$
f(a),\quad f'(a)
$$

So it knows:

- where the function is
- its slope

### Second order

Adds:

$$
f''(a)
$$

So it also knows:

- curvature

### Third order

Adds:

$$
f'''(a)
$$

and captures still more local behavior.

Therefore:

$$
\boxed{
\text{more terms}
\Rightarrow
\text{potentially better local approximation}
}
$$

But there's a tradeoff: more derivatives and more calculations.

---

# 27. Multivariate linear approximation

Now we move from one variable to multiple variables.

Previously:

$$
f(x).
$$

Now consider:

$$
\boxed{
f(x,y)
}
$$

We want to approximate this function around:

$$
(a,b).
$$

The formula becomes:

$$
\boxed{
L(x,y)
=
f(a,b)
+
\frac{\partial f}{\partial x}(a,b)(x-a)
+
\frac{\partial f}{\partial y}(a,b)(y-b)
}
$$

This is the two-variable version of the tangent-line formula.

---

# 28. Why do partial derivatives appear?

With one variable, we have:

$$
f'(a).
$$

With two variables, there are two independent ways to move:

### Change $x$, hold $y$ fixed

$$
\frac{\partial f}{\partial x}
$$

### Change $y$, hold $x$ fixed

$$
\frac{\partial f}{\partial y}
$$

So we need both.

This gives:

$$
\boxed{
\text{total local change}
\approx
\text{x-change}
+
\text{y-change}
}
$$

---

# 29. Connection to the gradient

The formula:

$$
L(x,y)
=
f(a,b)
+
f_x(a,b)(x-a)
+
f_y(a,b)(y-b)
$$

can be written much more compactly as:

$$
\boxed{
L(\mathbf x)
=
f(\mathbf a)
+
\nabla f(\mathbf a)^T(\mathbf x-\mathbf a)
}
$$

So the multivariate linear approximation from this tutorial is exactly the same idea as the gradient-based linear approximation from your previous lecture.

---

# 30. Example: $f(x,y)=xe^{xy}$

The tutorial considers:

$$
\boxed{
f(x,y)=xe^{xy}
}
$$

and wants the linear approximation around:

$$
\boxed{(1,0)}.
$$

Then it uses that approximation to estimate:

$$
f(1.1,-0.1).
$$

Since:

$$
(1.1,-0.1)
$$

is close to:

$$
(1,0),
$$

linear approximation should work reasonably well.

---

# 31. Step 1: Find $f(1,0)$

We have:

$$
f(x,y)=xe^{xy}.
$$

Therefore:

$$
f(1,0)
=
1\cdot e^{(1)(0)}
$$

$$
=1\cdot e^0
$$

$$
=\boxed1.
$$

---

# 32. Step 2: Find $f_x$

We have:

$$
f(x,y)=xe^{xy}.
$$

Differentiate with respect to $x$.

Because both $x$ and $e^{xy}$ depend on $x$, use the product rule:

$$
f_x
=
e^{xy}
+
x\frac{\partial}{\partial x}(e^{xy}).
$$

Using the chain rule:

$$
\frac{\partial}{\partial x}e^{xy}
=
ye^{xy}.
$$

Therefore:

$$
\boxed{
f_x=e^{xy}+xye^{xy}
}
$$

or:

$$
f_x=e^{xy}(1+xy).
$$

---

# 33. Evaluate $f_x(1,0)$

Substitute:

$$
x=1,\quad y=0.
$$

Then:

$$
e^{xy}=e^0=1
$$

and:

$$
xy=0.
$$

Therefore:

$$
\boxed{
f_x(1,0)=1
}
$$

---

# 34. Step 3: Find $f_y$

Start with:

$$
f(x,y)=xe^{xy}.
$$

Here $x$ is treated as constant when differentiating with respect to $y$.

Therefore:

$$
f_y
=
x\frac{\partial}{\partial y}(e^{xy}).
$$

By the chain rule:

$$
\frac{\partial}{\partial y}e^{xy}
=
xe^{xy}.
$$

So:

$$
\boxed{
f_y=x^2e^{xy}
}
$$

At $(1,0)$:

$$
f_y(1,0)
=
1^2e^0
=
1.
$$

Therefore:

$$
\boxed{
f_y(1,0)=1
}
$$

---

# 35. Step 4: Build the linear approximation

The formula is:

$$
L(x,y)
=
f(a,b)
+
f_x(a,b)(x-a)
+
f_y(a,b)(y-b).
$$

Here:

$$
(a,b)=(1,0).
$$

So:

$$
L(x,y)
=
1+1(x-1)+1(y-0).
$$

Therefore:

$$
L(x,y)=1+x-1+y
$$

and:

$$
\boxed{
L(x,y)=x+y
}
$$

This is beautiful because the complicated function

$$
xe^{xy}
$$

has been replaced locally by the simple linear function:

$$
x+y.
$$

---

# 36. Estimate $f(1.1,-0.1)$

Use:

$$
L(x,y)=x+y.
$$

Therefore:

$$
L(1.1,-0.1)
=
1.1-0.1
$$

$$
=\boxed1.
$$

So:

$$
\boxed{
f(1.1,-0.1)\approx1
}
$$

The exact value is approximately:

$$
0.98542.
$$

So the error is relatively small, which makes sense because the point is close to $(1,0)$.

---

# 37. Now: directional derivatives

This is the final major topic.

First understand ordinary partial derivatives.

Suppose:

$$
f(x,y).
$$

Then:

$$
\frac{\partial f}{\partial x}
$$

means:

> How quickly does $f$ change if I change $x$, while keeping $y$ fixed?

Geometrically, you're moving horizontally in the $xy$-plane.

---

# 38. What about $\partial f/\partial y$?

Similarly:

$$
\frac{\partial f}{\partial y}
$$

means:

> How quickly does $f$ change if I change $y$, while keeping $x$ fixed?

Geometrically, you're moving vertically in the $xy$-plane.

So partial derivatives only examine changes along the coordinate axes.

---

# 39. But what if I want an arbitrary direction?

Imagine you're standing on a hill.

You don't necessarily want to walk:

- directly east
- directly west
- directly north
- directly south.

You might walk northeast, northwest, or in some completely arbitrary direction.

Then you want to know:

> What is the slope of the hill in THIS particular direction?

That's exactly what the **directional derivative** measures.

---

# 40. Direction vector

Suppose the direction is represented by:

$$
\mathbf u.
$$

Usually we use a **unit vector**:

$$
\boxed{\|\mathbf u\|=1}
$$

because we want $\mathbf u$ to represent direction without an arbitrary scaling of distance.

---

# 41. Directional derivative formula

The directional derivative of $f$ at a point in direction $\mathbf u$ is:

$$
\boxed{
D_{\mathbf u}f
=
\nabla f\cdot\mathbf u
}
$$

or:

$$
\boxed{
D_{\mathbf u}f
=
f_xu_1+f_yu_2
}
$$

for two variables.

So it is a **weighted sum of the partial derivatives**.

The weights are the components of the direction vector.

---

# 42. Why does this make sense?

Suppose:

$$
\mathbf u=(u_1,u_2).
$$

This means the movement consists of:

- $u_1$ amount in the $x$-direction
- $u_2$ amount in the $y$-direction

The change in $f$ therefore combines:

$$
f_xu_1
$$

and:

$$
f_yu_2.
$$

So:

$$
\boxed{
D_{\mathbf u}f
=
f_xu_1+f_yu_2
}
$$

---

# 43. Very important: normalize the direction vector

Suppose the problem says:

> Find the directional derivative in the direction of $(3,4)$.

Do **not** immediately use:

$$
(3,4).
$$

That isn't a unit vector.

Its magnitude is:

$$
\|(3,4)\|
=
\sqrt{3^2+4^2}
=
5.
$$

Therefore the unit vector is:

$$
\boxed{
\mathbf u=
\left(\frac35,\frac45\right)
}
$$

or:

$$
\boxed{
\mathbf u=(0.6,0.8)
}
$$

This normalization step is extremely important.

---

# 44. General normalization formula

If the given direction vector is:

$$
\mathbf d=(a,b),
$$

then:

$$
\|\mathbf d\|
=
\sqrt{a^2+b^2}.
$$

The corresponding unit vector is:

$$
\boxed{
\mathbf u
=
\frac{\mathbf d}{\|\mathbf d\|}
}
$$

Therefore:

$$
\boxed{
\mathbf u=
\left(
\frac{a}{\sqrt{a^2+b^2}},
\frac{b}{\sqrt{a^2+b^2}}
\right)
}
$$

---

# 45. Directional derivative example

Suppose:

$$
f(x,y)
$$

is given and the direction is:

$$
(3,4).
$$

The general procedure is:

### Step 1

Find:

$$
f_x,\qquad f_y.
$$

### Step 2

Normalize the direction:

$$
(3,4)\rightarrow
\left(\frac35,\frac45\right).
$$

### Step 3

Use:

$$
D_{\mathbf u}f
=
f_x\frac35+f_y\frac45.
$$

### Step 4

If the problem gives a point $(x_0,y_0)$, substitute it.

That's the complete procedure.

---

# 46. Interpreting the answer

Suppose you calculate:

$$
D_{\mathbf u}f(2,-3)=5.
$$

What does 5 mean?

It means:

> At the point $(2,-3)$, if you move in the specified unit direction, the function is increasing at a rate of approximately 5 units of function value per unit of distance.

If instead you got:

$$
-5,
$$

it would mean:

> The function is decreasing at that rate in that direction.

If you got:

$$
0,
$$

then there is no first-order change in that direction.

---

# 47. Directional derivative vs partial derivative

This distinction is very important.

### Partial derivative with respect to $x$

$$
\boxed{
f_x
}
$$

means movement specifically in the $x$-direction.

That corresponds to:

$$
\mathbf u=(1,0).
$$

### Partial derivative with respect to $y$

$$
\boxed{
f_y
}
$$

corresponds to:

$$
\mathbf u=(0,1).
$$

### Directional derivative

$$
\boxed{
D_{\mathbf u}f=\nabla f\cdot\mathbf u
}
$$

allows **any direction**.

So you can think of partial derivatives as special cases of directional derivatives.

---

# 48. Connection to the previous lecture

This tutorial connects directly to your previous lecture.

You learned:

$$
\boxed{
D_{\mathbf u}f(\mathbf v)
=
\nabla f(\mathbf v)^T\mathbf u
}
$$

in the lecture.

The tutorial now gives you the **problem-solving procedure** for actually calculating it.

So the conceptual progression is:

$$
\text{partial derivatives}
$$

↓

$$
\text{gradient}
$$

↓

$$
\text{directional derivative}
$$

↓

$$
\text{rate of change in any chosen direction}.
$$

---

# 49. How all four topics connect

This is the most important conceptual map from the tutorial.

### Linear approximation

For one variable:

$$
\boxed{
f(x)\approx f(a)+f'(a)(x-a)
}
$$

---

### Higher-order approximation

Add derivatives:

$$
\boxed{
f(x)\approx
f(a)+f'(a)(x-a)
+\frac{f''(a)}{2!}(x-a)^2+\cdots
}
$$

---

### Multivariate linear approximation

For two variables:

$$
\boxed{
f(x,y)\approx
f(a,b)
+
f_x(a,b)(x-a)
+
f_y(a,b)(y-b)
}
$$

---

### Directional derivative

Choose a direction:

$$
\boxed{
D_{\mathbf u}f
=
\nabla f\cdot\mathbf u
}
$$

---

# 50. The problem-solving checklist

When solving questions from this tutorial, identify which category you're in.

## Type 1: "Approximate $f(b)$ using linear approximation"

Use:

$$
L(x)=f(a)+f'(a)(x-a).
$$

Choose $a$ close to $b$ where $f(a)$ is easy.

---

## Type 2: "Find a quadratic approximation"

Use:

$$
L_2(x)=
f(a)+f'(a)(x-a)
+\frac{f''(a)}{2!}(x-a)^2.
$$

---

## Type 3: "Find a third-order approximation"

Use:

$$
L_3(x)=
f(a)+f'(a)(x-a)
+\frac{f''(a)}{2!}(x-a)^2
+\frac{f'''(a)}{3!}(x-a)^3.
$$

---

## Type 4: "Find the linearization of $f(x,y)$ around $(a,b)$"

Use:

$$
\boxed{
L(x,y)=
f(a,b)+f_x(a,b)(x-a)+f_y(a,b)(y-b)
}
$$

---

## Type 5: "Find the directional derivative"

1. Find gradient.
2. Find/normalize direction vector.
3. Dot them together.

$$
\boxed{
D_{\mathbf u}f=\nabla f\cdot\mathbf u
}
$$

---

# 51. Common mistakes to avoid

### Mistake 1: Choosing a poor approximation point

For $\sqrt{50}$, choosing $a=100$ makes no sense when $49$ is nearby and easy.

Choose:

$$
\boxed{\text{nearby + easy}}
$$

---

### Mistake 2: Forgetting $f'(a)$

The formula is:

$$
f(a)+\boxed{f'(a)}(x-a).
$$

Not just:

$$
f(a)+(x-a).
$$

---

### Mistake 3: Using $f'(x)$ instead of $f'(a)$

Once you've chosen the approximation point $a$, evaluate the derivative there.

---

### Mistake 4: Forgetting the distance term

It is:

$$
x-a,
$$

not simply $x$.

---

### Mistake 5: Using a non-unit vector for directional derivatives

If the direction is $(3,4)$, first convert it to:

$$
\left(\frac35,\frac45\right).
$$

---

### Mistake 6: Forgetting partial derivatives in multivariable problems

For:

$$
f(x,y),
$$

you need:

$$
f_x
\quad\text{and}\quad
f_y.
$$

---

### Mistake 7: Assuming the approximation is exact everywhere

The tangent approximation is only exact at the approximation point.

Generally:

$$
\boxed{
f(x)\approx L(x)
}
$$

near $a$, not everywhere.

---

# 52. Final conceptual summary

The tutorial is teaching you one big idea from several angles:

> **A complicated function can be understood locally using simpler mathematical objects.**

For a one-variable function:

$$
\boxed{
\text{curve}\rightarrow\text{tangent line}
}
$$

For a two-variable function:

$$
\boxed{
\text{surface}\rightarrow\text{tangent plane}
}
$$

For even better approximation:

$$
\boxed{
\text{line/plane}\rightarrow\text{higher-order polynomial}
}
$$

For movement in an arbitrary direction:

$$
\boxed{
\text{directional derivative}
=
\nabla f\cdot\mathbf u
}
$$

And the central formula tying the multivariable material together is:

$$
\boxed{
f(\mathbf x)
\approx
f(\mathbf v)
+
\nabla f(\mathbf v)^T(\mathbf x-\mathbf v)
}
$$

while the central calculation for directional derivatives is:

$$
\boxed{
D_{\mathbf u}f(\mathbf v)
=
\nabla f(\mathbf v)^T\mathbf u.
}
$$

If you understand **why these two formulas work**, rather than merely memorizing them, most of the tutorial's problems become straightforward.