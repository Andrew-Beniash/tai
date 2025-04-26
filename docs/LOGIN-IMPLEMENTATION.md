# Login Implementation Documentation

## Overview

This document describes the implementation of the login functionality for the AI Tax Engagement Prototype. The login system simulates authentication using hardcoded users (Jeff and Hanna) and stores session information in the frontend localStorage.

## Backend Implementation

### User Model

The user model is defined in `backend/app/models/user.py` and includes:
- `User`: Base user model with id, name, and role
- `UserInDB`: Extended user model that includes password (for database storage)
- `UserResponse`: User model for API responses (excludes sensitive information)
- `Token`: JWT token model
- `TokenData`: Data stored in JWT token

### Authentication Endpoints

The login API is implemented in `backend/app/api/login.py` and provides:
- `/api/login`: POST endpoint that authenticates users and returns a JWT token
- `/api/users/me`: GET endpoint that returns the current authenticated user
- `/api/login-test`: GET endpoint for testing authentication configuration

### Authentication Flow

1. User submits credentials (username and password)
2. Backend validates against hardcoded users in `settings.HARDCODED_USERS`
3. If valid, a JWT token is generated with user ID in the payload
4. Token is returned to the client for subsequent authenticated requests

### Hardcoded Users

For this prototype, two users are defined in `backend/app/core/config.py`:
- Jeff (Role: Preparer)
- Hanna (Role: Reviewer)

Both users have the password "password" for simplicity.

## Frontend Implementation

### Authentication API Client

The authentication API client is implemented in `frontend/src/api/auth.ts` and provides:
- `login(username, password)`: Authenticates with the backend and stores user in localStorage
- `getCurrentUser()`: Gets the current user from localStorage
- `logout()`: Clears the user from localStorage
- `isLoggedIn()`: Checks if a user is logged in

### Authentication Context

The authentication context is implemented in `frontend/src/context/AuthContext.tsx` and provides:
- `AuthProvider`: React context provider that manages authentication state
- `useAuth()`: Custom hook for accessing authentication context

### Login Page

The login page is implemented in `frontend/src/pages/LoginPage.tsx` and provides:
- Form for entering username and password
- Quick login buttons for Jeff and Hanna
- Error handling and loading states
- Redirection to projects page after successful login

### Protected Routes

Protected routes are implemented in `frontend/src/App.tsx` to ensure only authenticated users can access certain pages. If a user tries to access a protected route without being logged in, they are redirected to the login page.

## Session Management

For this prototype, session management is simplified:
1. User information is stored in localStorage after successful login
2. JWT token is stored in localStorage for authentication with backend
3. Protected routes check for user in localStorage
4. Session is cleared on logout

## Testing

To test the login functionality:
1. Start both backend and frontend servers
2. Navigate to the login page
3. Enter credentials (username: "jeff" or "hanna", password: "password")
4. Alternatively, use the quick login buttons
5. After successful login, you should be redirected to the projects page

## Security Notes

This implementation is for a prototype only and has several security limitations:
- Passwords are stored in plaintext (in a production app, they would be hashed)
- JWT secret key is hardcoded (in a production app, it would be a secured environment variable)
- localStorage is vulnerable to XSS attacks (in a production app, more secure storage options would be used)
- No CSRF protection is implemented
