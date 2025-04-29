# 🚀 Nexios API Application

A modern, feature-rich API application built with the Nexios framework, featuring robust authentication, database integration, and a clean architecture.

## ✨ Features

- 🔐 JWT-based Authentication System
- 📦 Modular Route Structure
- 🗃️ Database Integration
- 🛠️ Environment Configuration Management
- 📝 OpenAPI Documentation
- ⚡ High-Performance Async Operations

## 🔧 Technical Stack

- Python 3.9+
- Nexios Framework (v2.3.2)
- Dependencies:
  - python-jose[cryptography]: JWT token handling
  - passlib[bcrypt]: Password hashing
  - python-multipart: Form data processing
  - aiosqlite: Async SQLite support
  - voltar: Schema validation

## 📁 Project Structure

```
app/
├── migrations/        # Database migrations
├── models/           # Data models
├── routes/           # API routes
│   ├── auth/        # Authentication endpoints
│   └── index/       # Main application endpoints
├── schemas/         # Data validation schemas
├── utils/           # Utility functions
├── config.py        # Application configuration
└── main.py          # Application entry point
```

## 🔒 Authentication System

The application implements a JWT-based authentication system with the following features:

- User registration and login endpoints
- Access token (30 minutes validity)
- Refresh token (7 days validity)
- Secure password hashing with bcrypt

### Authentication Endpoints

#### Sign Up
```http
POST /auth/signup
Content-Type: application/json

{
    "email": "user@example.com",
    "password": "secure_password"
}
```

#### Login
```http
POST /auth/login
Content-Type: application/json

{
    "email": "user@example.com",
    "password": "secure_password"
}
```

## 🚀 Getting Started

### Prerequisites

- Python 3.9 or higher
- Poetry (recommended) or pip

### Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd nexios-api-app
```

2. Install dependencies:
```bash
# Using Poetry (recommended)
poetry install

# Using pip
pip install -r requirements.txt
```

3. Create a `.env` file:
```env
DEBUG=True
secret_key=your-secure-secret-key
DB_URL=sqlite:///db.sqlite3
```



## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Open a Pull Request

## 📄 License

This project is licensed under the terms of the license provided with the repository.

---

Built with ❤️ using [Nexios Framework](https://github.com/nexios-labs/nexios)

