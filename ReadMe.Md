# RBAC LLM API Project

This project is a FastAPI application with role-based access control (RBAC) that integrates language model capabilities for document query and chat functionalities.

---

## Features

| Feature | Description |
|---------|-------------|
| **User Authentication** | Authentication using JWT tokens |
| **RBAC (Role-Based Access Control)** | Supports user, admin, and moderator roles |
| **Document Querying** | AI-based querying with Retrieval Augmented Generation (RAG) |
| **AI Chat Interface** | Uses Google Gemini model for chatbot interaction |
| **User Management** | CRUD operations for user accounts |

---

## Setup

### Prerequisites

| Requirement | Version |
|------------|---------|
| Python | 3.12+ |
| MongoDB | Required |

---

### Installation

| Step | Command |
|------|---------|
| **Clone Repository** | `git clone https://github.com/yourrepo/rbac-llm-api.git && cd rbac-llm-api` |
| **Install Dependencies** | `pip install -r requirements.txt` |

---

### Environment Variables

| Variable | Description |
|----------|-------------|
| `MONGO_URI` | MongoDB connection string |
| `GEMINI_API` | API key for Google Gemini model |
| `ACCESS_TOKEN_SECRET` | Secret key for JWT access tokens |
| `REFRESH_TOKEN_SECRET` | Secret key for JWT refresh tokens |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | Expiration time for access tokens (in minutes) |
| `REFRESH_TOKEN_EXPIRE_DAYS` | Expiration time for refresh tokens (in days) |
| `ENVIRONMENT` | Set to `development` or `production` |

---

### Running the Application

| Step | Command |
|------|---------|
| **Start Server** | `uvicorn app.main:app --reload` |

---

## API Documentation

### Authentication Endpoints

| Method | Endpoint | Description | Auth Required |
|--------|---------|-------------|--------------|
| **POST** | `/login/` | User login | No |
| **POST** | `/logout/` | User logout | Yes |

---

### User Management Endpoints

| Method | Endpoint | Description | Auth Required |
|--------|---------|-------------|--------------|
| **GET** | `/user/{user_id}` | Get user by ID | Yes |
| **POST** | `/create_user/` | Create new user | No |
| **PUT** | `/update_user/{user_id}` | Update user details | Yes |
| **DELETE** | `/delete_user/{user_id}` | Delete user account | Yes |

---

### Admin Endpoints

| Method | Endpoint | Description | Auth Required | Role Required |
|--------|---------|-------------|--------------|--------------|
| **GET** | `/admin/users` | Get all users | Yes | Admin |
| **POST** | `/admin/users/bulk-delete` | Delete multiple users | Yes | Admin |
| **PUT** | `/admin/users/{user_id}/role` | Update user role | Yes | Admin |

---

### LLM Chat Endpoints

| Method | Endpoint | Description | Auth Required |
|--------|---------|-------------|--------------|
| **POST** | `/llm` | Chat with AI assistant | Yes |

---

### RAG (Document Query) Endpoints

| Method | Endpoint | Description | Auth Required |
|--------|---------|-------------|--------------|
| **POST** | `/rag/query` | Query documents or chat with AI | Yes |

---

## Role-Based Access Control

| Role | Description |
|------|-------------|
| **User** | Basic access to chat and document querying |
| **Admin** | Full access to user management and administration |
| **Moderator** | Role exists, but specific permissions not implemented yet |

---

## Supported Document Formats

| File Type | Extension |
|-----------|-----------|
| **PDF** | `.pdf` |
| **Text File** | `.txt` |
| **CSV File** | `.csv` |
| **Word Document** | `.docx` |

---

## Authentication Flow

| Token Type | Expiration | Storage |
|------------|------------|----------|
| **Access Token** | 5 minutes | Stored in HTTP-only cookies |
| **Refresh Token** | 30 days | Stored in HTTP-only cookies |

---

## Example API Requests

### Login Request

