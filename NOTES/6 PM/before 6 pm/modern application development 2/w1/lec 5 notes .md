# mad 2 notes iit m

Here is a detailed breakdown of every concept covered in the transcript, with practical code examples to illustrate each point.

### 1. Strings and UTF-16 Encoding

JavaScript strings are encoded in **UTF-16**. This means the `.length` property counts *code units*, not necessarily visible characters. This can be surprising when dealing with emojis or complex Unicode characters that require two code units (surrogate pairs).

```jsx
// Simple ASCII string - works as expected
const hello = "Hello";
console.log(hello.length); // 5

// Emoji example - surprising result!
const wave = "👋";
console.log(wave.length); // 2 (not 1!)
// Because 👋 is a surrogate pair in UTF-16

// The length is predictable, but you must account for encoding
const mixed = "Hi👋";
console.log(mixed.length); // 4 (H=1, i=1, 👋=2)
```

> **Key takeaway:** Don't assume `.length` equals character count. Use libraries like `Intl.Segmenter` if you need true character counts.
> 

---

### 2. `undefined` vs. `null`

Both represent "no value," but they carry different intent.

|  | `undefined` | `null` |
| --- | --- | --- |
| **Meaning** | Not yet assigned / unknown | Intentionally empty |
| **Who sets it?** | JavaScript engine | The developer |
| **Typical use** | Uninitialized variables, missing array slots | Explicitly clearing a value |

```jsx
// undefined: JS assigns this automatically
let name;
console.log(name); // undefined

// Array with holes - elements are undefined
const arr = new Array(3);
console.log(arr[0]); // undefined

// null: YOU assign this deliberately
const user = { name: null }; // "I know this field should be empty"

// Subtle difference matters in strict comparisons
console.log(undefined == null);  // true  (loose equality)
console.log(undefined === null); // false (strict equality!)
```

> **Best practice:** Use `undefined` for things JS manages automatically. Use `null` when *you* want to say "this is intentionally empty." Always use `===` to avoid confusion.
> 

---

### 3. Variable Declarations: `let` and `const`

#### Scope

Variables declared with `let`/`const` are **block-scoped**, meaning they only exist inside `{ }`. This prevents accidental collisions with variables elsewhere.

```jsx
let x = 10;

function demo() {
    let x = 20; // Completely separate from outer x
    console.log(x); // 20
}

demo();
console.log(x); // Still 10 — no collision!
```

#### `const` — Immutable Reference, Not Immutable Content

This is the most misunderstood part of `const`. It prevents **reassignment** of the variable, but does NOT freeze object contents.

```jsx
// Primitive: truly immutable
const PI = 3.14;
PI = 3.15; // ❌ TypeError: Assignment to constant variable

// Object: reference is locked, contents are NOT
const user = { name: "Alice", age: 30 };
user.age = 31;        // ✅ Works fine! Mutating contents is allowed
user.name = "Bob";    // ✅ Also works

user = {};            // ❌ TypeError: Cannot reassign 'user'
```

#### `let` — For Values That Change

Use `let` when the variable itself needs to be reassigned, like loop counters.

```jsx
for (let i = 0; i < 5; i++) {
    console.log(i); // 0, 1, 2, 3, 4
}
// 'i' doesn't leak outside the loop block
console.log(i); // ❌ ReferenceError: i is not defined
```

---

### 4. Control Flow

#### Conditions & Strict Equality

Always prefer `===` over `==` to avoid type coercion surprises.

```jsx
let score = "90";

// Loose equality — dangerous!
if (score == 90) {
    console.log("Pass"); // This RUNS because "90" gets coerced to 90
}

// Strict equality — safe
if (score === 90) {
    console.log("Pass"); // This does NOT run — "90" !== 90
} else {
    console.log("Check your types!"); // This runs instead
}
```

#### Iteration: Three Ways to Loop

#### Classic `for` Loop (C-style)

Requires `let` because the counter changes each iteration.

```jsx
// ❌ This fails
for (const i = 0; i < 5; i++) {
    // TypeError: Assignment to constant variable
}

// ✅ Correct version
for (let i = 0; i < 5; i++) {
    console.log(i); // 0, 1, 2, 3, 4
}
```

#### `for...in` — Iterates Over Indices (Not Values!)

This is a common source of bugs. `for...in` gives you the **index/key**, not the element itself.

```jsx
const v = [10, 20, 30, 40];

for (const x in v) {
    console.log(x);     // "0", "1", "2", "3"  ← indices as STRINGS
    console.log(v[x]);  // 10, 20, 30, 40      ← actual values
}

// Why does `const` work here?
// Each iteration creates a NEW block scope.
// Within that single iteration's scope, x never changes.
// So const is valid even though x differs across iterations.
```

#### `for...of` — Iterates Over Values ✅ (Preferred)

Directly gives you the element. Cleaner and less error-prone.

```jsx
const v = [10, 20, 30, 40];

for (const x of v) {
    console.log(x); // 10, 20, 30, 40  ← actual values directly
}
```

> **Rule of thumb:** Use `for...of` for arrays. Only use `for...in` when you specifically need object keys.
> 

#### Other Control Flow Tools

These work similarly to Python/C/Java:

```jsx
// while loop
let count = 0;
while (count < 3) {
    console.log(count);
    count++;
}

// break and continue
for (const num of [1, 2, 3, 4, 5]) {
    if (num === 3) continue; // skip 3
    if (num === 5) break;    // stop at 5
    console.log(num);        // 1, 2, 4
}

// switch statement — cleaner than long if/else chains
const day = "Mon";
switch (day) {
    case "Mon": console.log("Start of week"); break;
    case "Fri": console.log("Almost weekend"); break;
    default:    console.log("Midweek");
}
```

---

### 5. Functions

Functions are **first-class objects** in JavaScript. They can be assigned to variables, passed as arguments, and returned from other functions. There are four main syntaxes.

#### Syntax 1: Function Declaration (Statement)

The most traditional form. Hoisted to the top of its scope.

```jsx
function add(x, y) {
    return x + y;
}

console.log(add(2, 3)); // 5
```

#### Syntax 2: Named Function Expression

Assigns an anonymous function to a variable. Note: no name after `function`.

```jsx
let add = function(x, y) {
    return x + y;
};

console.log(add(2, 3)); // 5
```

#### Syntax 3: Arrow Function

Concise syntax. Best for short, simple functions. Implicit return when body is a single expression.

```jsx
let add = (x, y) => x + y;

console.log(add(2, 3)); // 5

// Multi-line arrow functions need explicit return + braces
let multiply = (x, y) => {
    const result = x * y;
    return result;
};
```

> **Warning:** In real-world frontend code, people often abuse arrow functions for large complex blocks. Keep them brief for readability.
> 

#### All Three Are Equivalent

Despite different syntax, they produce identical function objects:

```jsx
function addA(x, y) { return x + y; }
let addB = function(x, y) { return x + y; };
let addC = (x, y) => x + y;

console.log(typeof addA); // "function"
console.log(typeof addB); // "function"
console.log(typeof addC); // "function"

console.log(addA(2,3), addB(2,3), addC(2,3)); // 5 5 5
```

---

### 6. IIFE (Immediately Invoked Function Expression)

Declares and executes a function in one step using wrapping parentheses + trailing `()`.

```jsx
// IIFE pattern
(function() {
    const secret = 42;
    console.log(secret); // 42
})(); // ← immediately invoked

// With parameters
((x, y) => {
    console.log(x + y); // 5
})(2, 3);

// Without the trailing (), it's just an expression — nothing runs!
(function() { console.log("never prints"); })
```

#### Why They Exist Historically

Before `let`/`const`, only `var` existed, which was **function-scoped**, not block-scoped. IIFEs were the only way to create isolated scope:

```jsx
// OLD WAY (pre-ES6) — needed IIFE for scoping
(function() {
    var temp = "isolated";
    // ...
})();

// MODERN WAY — block scope does the job
{
    let temp = "isolated";
    // ...
}
```

> **Advice:** Avoid IIFEs in modern code. Block scope with `let`/`const` is clearer. IIFEs confuse newcomers and serve no purpose today.
> 

---

### 7. Functions as Objects (Curiosity, Not Practice)

Since functions ARE objects, you can attach properties to them. Technically possible, practically discouraged.

```jsx
function add(x, y) {
    return x + y;
}

// Attaching an object to a function — legal but weird
add.v = { a: 3, b: 7 };

console.log(typeof add);   // "function"
console.log(add.v);        // { a: 3, b: 7 }
console.log(add.v.a);      // 3
console.log(add(2, 3));    // 5 — still callable normally!
```

> **Key insight:** Objects hold methods (functions). But functions holding objects is backwards and confusing. The language allows it, but there's rarely a good reason. Avoid it.
> 

---

### Quick Reference Cheat Sheet

| Concept | Do This | Avoid This |
| --- | --- | --- |
| Comparison | `===` | `==` |
| Variables | `let` / `const` | `var` |
| Array loop | `for...of` | `for...in` |
| Short functions | Arrow `=>` | Arrow for huge blocks |
| Scoping | Block `{ }` + `let` | IIFE |
| Empty value | `null` (intentional) | Mixing `null`/`undefined` carelessly |
| String length | Account for UTF-16 | Assume `.length` = chars |

If something on your end appeared truncated (e.g., a missing table row or an unrendered code block), tell me which section looked incomplete and I'll re-send just that part cleanly.