### 5.1. External APIs

#### API: [Name, e.g. "User Management API"]

**Protocol:** REST / GraphQL / gRPC / WebSocket

**Base URL:** `/api/v1/users`

**Authentication:** JWT Bearer Token

**Endpoints:**

##### POST /register

**Description:** New user registration

**Related Use Case:** UC-01

**Request:**
```json
{
  "email": "string (required, email format)",
  "password": "string (required, min 8 chars)",
  "password_confirmation": "string (required)"
}
```

**Response 201 Created:**
```json
{
  "user_id": "uuid",
  "email": "string",
  "status": "pending",
  "message": "Confirmation email sent"
}
```

**Response 400 Bad Request:**
```json
{
  "error": "validation_error",
  "details": {
    "email": ["Email already exists"],
    "password": ["Password too short"]
  }
}
```

**Response 500 Internal Server Error:**
```json
{
  "error": "internal_error",
  "message": "Failed to send confirmation email"
}
```
