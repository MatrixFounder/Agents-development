### 4.1. Conceptual Data Model

**Entities:**

#### Entity: [Name, e.g., "User"]

**Description:** [What this entity represents]

**Attributes:**
- `id` (UUID) — unique identifier
- `email` (String, unique) — user email
- `password_hash` (String) — password hash
- `created_at` (DateTime) — creation date
- `status` (Enum: pending, active, blocked) — account status

**Relationships:**
- One User has many Sessions (1:N)
- One User has one Profile (1:1)

### 4.2. Logical Data Model

**For Relational DB:**

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | UUID | PRIMARY KEY | Unique identifier |
| email | VARCHAR(255) | UNIQUE, NOT NULL | User email |
| password_hash | VARCHAR(255) | NOT NULL | Bcrypt password hash |
| created_at | TIMESTAMP | NOT NULL, DEFAULT NOW() | Creation date |
| updated_at | TIMESTAMP | NOT NULL, DEFAULT NOW() | Update date |
| status | VARCHAR(20) | NOT NULL, DEFAULT 'pending' | Account status |

**For NoSQL DB:**

```json
{
  "_id": "ObjectId",
  "email": "string (unique)",
  "password_hash": "string",
  "created_at": "ISODate",
  "updated_at": "ISODate",
  "status": "string (enum: pending, active, blocked)",
  "profile": {
    "first_name": "string",
    "last_name": "string",
    "avatar_url": "string"
  },
  "sessions": [
    {
      "token": "string",
      "created_at": "ISODate",
      "expires_at": "ISODate"
    }
  ]
}
```
