# JWT Authentication Project (FastAPI)

This project implements a complete JWT-based authentication system using FastAPI, SQLAlchemy, and PostgreSQL.

### app/
Main application folder containing all backend logic.

### app/main.py
Initializes the FastAPI application and includes authentication routes.

### app/database.py
Handles database connection setup and provides database session dependency.

### app/models/
Contains database models (tables).

#### app/models/user.py
Defines the User table schema stored in PostgreSQL.

### app/schemas/
Handles request and response validation.

#### app/schemas/user.py
Defines Pydantic schemas for signup, login, and password change.

### app/routers/
Contains all API endpoints.

#### app/routers/auth.py
Implements signup, login, JWT token generation, and password change APIs.

### app/core/
Contains core configuration and security logic.

#### app/core/config.py
Loads environment variables like database URL and JWT settings.

#### app/core/security.py
Creates and manages JWT access tokens securely.

### app/utils/
Contains helper utility functions.

#### app/utils/password.py
Handles password hashing and verification using bcrypt.

---

## 🔐 How Authentication Works

1. User signs up → password is hashed and stored in database.
2. User logs in → credentials are verified.
3. A JWT access token is generated using the user ID.
4. Token is returned to the client for authenticated access.
5. User can change password after verifying old password.

---

## 🧠 Key Features

- Secure password hashing (bcrypt)
- JWT token-based authentication
- Clean project structure
- Environment variable configuration
- PostgreSQL database support

---

## 🚀 Tech Stack

- FastAPI
- SQLAlchemy
- PostgreSQL
- JWT (python-jose)
- Passlib (bcrypt)
