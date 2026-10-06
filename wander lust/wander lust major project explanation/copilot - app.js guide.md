# WanderLust Express Server Breakdown (`app.js`)

This guide walks through the main server file (`app.js`) of an Express + MongoDB + Passport application (such as the WanderLust project) from top to bottom, explaining why every line is used.

---

## 1. Load Environment Variables

```javascript
if(process.env.NODE_ENV != "production") {
    require('dotenv').config();
}
```

### Purpose
Loads variables from the `.env` file into `process.env`.

#### Example `.env`:
```env
ATLASDB_URL=mongodb+srv://....
SECRET=mysecretkey
```

### Why?
* **In development:** `NODE_ENV=development` — it loads the local `.env` file.
* **In production:** `NODE_ENV=production` — environment variables are already provided directly by the hosting platform (like Render, Heroku, or AWS), so a local `.env` file is not needed.

---

## 2. Import Required Packages

```javascript
const express = require("express");
const app = express();
```
* **Purpose:** Imports Express and creates the Express application instance.

```javascript
const mongoose = require("mongoose");
```
* **Purpose:** Used to connect and interact with MongoDB.

```javascript
const path = require("path");
```
* **Purpose:** Utility for handling and transforming file paths.
* **Example:** `path.join(__dirname, "views")`

```javascript
const methodOverride = require("method-override");
```
* **Purpose:** HTML forms natively only support `GET` and `POST` requests. If we need to send `PUT` or `DELETE` requests from forms, Method Override enables this.
* **Example Route:** `/listings/1?_method=DELETE`

```javascript
const ejsMate = require("ejs-mate");
```
* **Purpose:** Provides layout support in EJS templates.
* **Usage:** Allows `<%- body %>` tags inside a main layout file.

```javascript
const ExpressError = require("./utils/ExpressError.js");
```
* **Purpose:** Custom error class for handling custom status codes and messages.
* **Example:** `throw new ExpressError(404, "Not Found");`

```javascript
const session = require("express-session");
```
* **Purpose:** Stores user session data across HTTP requests.

```javascript
const MongoStore = require('connect-mongo');
```
* **Purpose:** Stores user sessions directly inside MongoDB instead of default memory storage.
* **Why?** Without it, sessions are stored in server memory, which leaks memory and resets on server restarts—making it bad for production.

```javascript
const flash = require("connect-flash");
```
* **Purpose:** Flash messages are temporary messages displayed to the user once and then deleted.
* **Example:** `req.flash("success", "Listing Created");`

```javascript
const passport = require("passport");
const LocalStrategy = require("passport-local");
const User = require("./models/user.js");
```
* **Purpose:** 
  * `passport`: Main authentication library.
  * `passport-local`: Username and password authentication strategy.
  * `User`: Mongoose User model.

---

## 3. Import Routes

```javascript
const listingRouter = require("./routes/listing.js");
const reviewRouter = require("./routes/review.js");
const userRouter = require("./routes/user.js");
```

### Why?
Keeps the code clean and modular instead of writing all application routes inside a single large file.

---

## 4. Database URL

```javascript
const dbUrl = process.env.ATLASDB_URL;
```

### Purpose
Retrieves the MongoDB Atlas connection string from environment variables (`ATLASDB_URL=.....`).

---

## 5. Connect Database

```javascript
main().then(() => {
    console.log("connected to DB");
}).catch((err) => {
    console.log(err);
});

async function main() {
    await mongoose.connect(dbUrl);
}
```

### Flow:
1. Start app
2. Connect MongoDB via async function
3. Log success or error message

---

## 6. EJS Setup

```javascript
app.set("view engine", "ejs");
app.set("views", path.join(__dirname, "views"));
```

### Purpose
* Tells Express to use **EJS** as the template engine.
* Sets the views directory path so Express knows where to look when using `res.render("home.ejs")`.

---

## 7. Middleware

### Parse Form Data
```javascript
app.use(express.urlencoded({extended: true}));
```
* **Purpose:** Parses incoming URL-encoded form data (e.g., `name=Piyush`) into usable JavaScript objects (`req.body.name`).

### Method Override
```javascript
app.use(methodOverride("_method"));
```
* **Purpose:** Intercepts requests containing query parameters like `?_method=PUT` or `?_method=DELETE`.

### EJS Mate Engine
```javascript
app.engine('ejs', ejsMate);
```
* **Purpose:** Registers `ejs-mate` as the engine for rendering layouts.

### Static Files
```javascript
app.use(express.static(path.join(__dirname, "/public")));
```
* **Purpose:** Serves static assets like CSS stylesheets, client-side JavaScript, and images from the `public` folder (e.g., `/css/style.css`).

---

## 8. MongoDB Session Store

```javascript
const store = MongoStore.create({
    mongoUrl: dbUrl,
    crypto: {
       secret: process.env.SECRET,
    },
    touchAfter: 24 * 3600,
});
```

### Purpose
* `mongoUrl`: Specifies MongoDB as the session store database.
* `crypto.secret`: Encrypts session data for security.
* `touchAfter: 24 * 3600`: Limits session updates to once every 24 hours (unless data changes), significantly improving performance.

---

## 9. Session Store Error Handling

```javascript
store.on("error", (err) => {
    console.log("ERROR IN MONGO SESSION STORE", err);
});
```

> **⚠️ Bug Note:** Make sure `err` is passed as a parameter into the callback function `(err) => {}`. Omitting it will cause a `ReferenceError: err is not defined` if a store error occurs.

---

## 10. Session Configuration

```javascript
const sessionOptions = {
    store,
    secret: process.env.SECRET,
    resave: false,
    saveUninitialized: true,
    cookie: {
        expires: Date.now() + 7 * 24 * 60 * 60 * 1000,
        maxAge: 7 * 24 * 60 * 60 * 1000,
        httpOnly: true
    }
};
```

### Details
* `store`: Directs sessions to MongoDB via `connect-mongo`.
* `secret`: Signs the session ID cookie.
* `resave: false`: Prevents saving sessions back to the store if nothing was modified.
* `saveUninitialized: true`: Forces an uninitialized session to be saved to the store.
* **Cookie Settings:**
  * `expires` & `maxAge`: Sets session cookie lifespan to 7 days.
  * `httpOnly: true`: Prevents client-side scripts from accessing the cookie, providing critical protection against XSS attacks.

---

## 11. Home Route

```javascript
app.get("/", (req, res) => {
    res.redirect("/listings");
});
```

### Purpose
Redirects base traffic from `localhost:8080/` directly to `localhost:8080/listings`.

---

## 12. Session Middleware

```javascript
app.use(session(sessionOptions));
```

### Purpose
Initializes session support. **Must** be declared before Passport session middleware.

---

## 13. Flash Middleware

```javascript
app.use(flash());
```

### Purpose
Enables `req.flash()` across the application for temporary notification handling.

---

## 14. Passport Setup

```javascript
app.use(passport.initialize());
app.use(passport.session());

passport.use(new LocalStrategy(User.authenticate()));
```

### Purpose
* **Initialize Passport:** Boots up passport authentication.
* **Persistent Login (`passport.session()`):** Uses sessions to keep users logged in across multiple requests.
* **Local Strategy:** Uses `passport-local-mongoose`'s `User.authenticate()` method to validate usernames and passwords.

---

## 15. Serialize User

```javascript
passport.serializeUser(User.serializeUser());
```

### Purpose
Determines which data should be stored in the session (typically the user ID).
* **Example:** `session = { userId: 123 }`

---

## 16. Deserialize User

```javascript
passport.deserializeUser(User.deserializeUser());
```

### Purpose
Retrieves the complete user object from the database using the stored user ID, making `req.user` available on subsequent requests.

---

## 17. Global Middleware for EJS (`res.locals`)

```javascript
app.use((req, res, next) => {
    res.locals.success = req.flash("success");
    res.locals.error = req.flash("error");
    res.locals.currUser = req.user;
    next();
});
```

### Purpose
Runs before every request to make variables globally accessible across all EJS templates without explicitly passing them in every route render:
* `success`: Success flash notifications (`<%= success %>`).
* `error`: Error flash notifications.
* `currUser`: Current logged-in user info (`currUser`).

---

## 18. Demo User Route (Commented Out)

```javascript
// app.get("/demouser", async (req, res) => {
//     let fakeUser = new User({
//          email: "student@gmail.com",
//          username: "delta-student"
//     });
//     let registeredUser = await User.register(fakeUser, "helloworld");
//     res.send(registeredUser);
// });
```

### Purpose
Used during development to test registering a user with `passport-local-mongoose` (which handles password hashing, storing, and validation).

---

## 19. Router Middleware

```javascript
app.use("/listings", listingRouter);
app.use("/listings/:id/reviews", reviewRouter);
app.use("/", userRouter);
```

### Purpose
Mounts modular routers to specific base paths:
* `/listings` $\rightarrow$ Handled by `listingRouter`
* `/listings/:id/reviews` $\rightarrow$ Handled by `reviewRouter`
* `/` $\rightarrow$ Handled by `userRouter` (signup, login, logout)

---

## 20. 404 Route Handler

```javascript
app.all("*", (req, res, next) => {
    next(new ExpressError(404, "Page Not Found!"));
});
```

### Purpose
Catches any incoming request that does not match any defined route and forwards a custom 404 `ExpressError` to the error-handling middleware.

---

## 21. Global Error Handler

```javascript
app.use((err, req, res, next) => {
    let { statusCode = 500, message = "Something went wrong!" } = err;
    res.status(statusCode).render("error.ejs", { err });
});
```

### Purpose
Catches all application errors, extracts status code and message (with fallback default values), and renders a dedicated error view (`error.ejs`).

---

## 22. Start Server

```javascript
app.listen(8080, () => {
    console.log("server is listening to port 8080");
});
```

### Purpose
Binds and listens for incoming connections on port 8080, making the application available at `http://localhost:8080`.

---

## 📊 Complete Flow Diagram

```text
User Request
      │
      ▼
Express App
      │
      ▼
Session Middleware
      │
      ▼
Flash Middleware
      │
      ▼
Passport Authentication
      │
      ▼
Current User Middleware (res.locals)
      │
      ▼
Router Dispatcher
 ┌────┼────┐
 ▼    ▼    ▼
Listing Review User
Router Router Router
      │
      ▼
Response / Rendering
      │
      ▼
EJS View
```

---

## 🚀 Interview & Exam Quick Points

* **Why `connect-mongo`?** Sessions survive server restarts and don't overwhelm server memory.
* **Why `passport.session()`?** Keeps users logged in persistently across HTTP requests.
* **Why `serializeUser()`?** Stores only the user ID inside the session cookie.
* **Why `deserializeUser()`?** Converts the stored user ID back into a complete user object (`req.user`).
* **Why `res.locals.currUser`?** Makes the logged-in user available globally to every EJS page without manual passing.