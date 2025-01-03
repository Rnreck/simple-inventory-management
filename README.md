# Inventory Management System

A full-stack inventory management system built with Flask (Backend) and Vue.js (Frontend). This system provides comprehensive functionality for managing products, orders, and user authentication.

## Features

- 🔐 User Authentication (JWT-based)
  - User registration and login
  - Role-based access control (Admin/User)
  - Secure password hashing

- 📦 Product Management
  - CRUD operations for products
  - Product categorization
  - Inventory tracking
  - Price management
  - Advanced product search and filtering

- 🛒 Order Management
  - Create and view orders
  - Order status tracking
  - Real-time inventory updates
  - Order history

- 📊 Category Management
  - Create and manage product categories
  - Category-based product organization

## Tech Stack

### Backend
- Flask - Python web framework
- Flask-RESTful - REST API framework
- Flask-JWT-Extended - JWT authentication
- PyTiDB - TiDB database connector
- Flasgger - Swagger API documentation

### Frontend
- Vue.js
- Vite
- TypeScript
- Vue Router
- Vuex/Pinia (State Management)

### Database
- TiDB

## Project Structure

```
inventory-management/
├── app/                    # Backend application
│   ├── __init__.py        # Flask app initialization
│   ├── config.py          # Configuration settings
│   ├── db.py             # Database connection
│   ├── models.py         # Data models
│   ├── resources.py      # API resources
│   ├── schema.sql        # Database schema
│   └── user_resources.py # User authentication
├── inventory-page/        # Frontend application
└── requirements.txt      # Python dependencies
```

## Setup and Installation

### Prerequisites
- Python 3.10+
- TiDB 6.1.0+
- Node.js 14+

### Backend Setup

1. Create a virtual environment:
```bash
python -m venv .venv
source .venv/bin/activate  # Linux/Mac
.venv\Scripts\activate     # Windows
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Configure TiDB:
- Create a TiDB database
- Update `config.py` with your database credentials

4. Initialize the database:
```bash
python app/init_db.py
```

5. Run the backend server:
```bash
python run.py
```

### Frontend Setup

1. Navigate to the frontend directory:
```bash
cd inventory-page
```

2. Install dependencies:
```bash
npm install
```

3. Run the development server:
```bash
npm run dev
```

## API Documentation

The API documentation is available at `/apidocs` when running the backend server. It provides detailed information about all available endpoints, request/response formats, and authentication requirements.

## Default Admin Account

- Username: admin
- Password: admin123

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details. 