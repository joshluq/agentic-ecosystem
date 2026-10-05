# Component & API Specification: [COMPONENT_NAME]

**Feature ID**: [FEAT-XXX]  
**Component Identifier**: [e.g., NotificationsRoute / SubscriptionWebhook / FCMDispatcher]  
**Target Layer**: API Router (`src/index.ts`), Service Layer (`src/services/`), Database (`supabase/migrations/`)  
**Runtime**: Node.js 20+ (Hono v4) / Supabase Edge Functions (Deno)  
**Status**: APPROVED  

---

## 1. API Route & HTTP Method Invariants

Define all REST endpoints exposed by this backend component:

| Method | Path | Auth Scope | Entitlement Guard | Rate Limit | Description |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `GET` | `/v1/[resource]` | User JWT | Optional / `PREMIUM_REQUIRED` | 60 req/min | Paginated list of resources |
| `POST` | `/v1/[resource]/sync` | User JWT | `PREMIUM_REQUIRED` | 30 req/min | Idempotent batch sync from client |
| `PATCH` | `/v1/[resource]/:id` | User JWT | Owner Only | 60 req/min | Individual entity update |
| `DELETE` | `/v1/[resource]/:id` | User JWT | Owner Only | 30 req/min | Individual entity removal |

---

## 2. Authentication & Entitlement Guards

Specify the route middleware bindings in Hono:

```typescript
import { Hono } from 'hono';
import { withSupabase } from './middleware/auth';
import { verifyPremiumAccess } from './middleware/entitlements';

const router = new Hono();

// Route with strict user isolation and subscription entitlement check
router.get(
  '/v1/[resource]',
  withSupabase({ auth: 'user' }),
  verifyPremiumAccess,
  async (c) => {
    const user = c.get('user');
    const supabase = c.get('supabase');
    // Implementation
  }
);
```

---

## 3. Data Transfer Objects (DTO) & Payload Schemas

### 3.1 Request Payload Schema
```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "type": "object",
  "required": ["items"],
  "properties": {
    "items": {
      "type": "array",
      "items": {
        "type": "object",
        "required": ["id", "title"],
        "properties": {
          "id": { "type": "string", "format": "uuid" },
          "title": { "type": "string", "minLength": 1, "maxLength": 100 }
        }
      }
    }
  }
}
```

### 3.2 Response Payload Schema
```json
{
  "success": true,
  "data": {
    "items": [],
    "total": 0,
    "unread_count": 0
  },
  "error": null
}
```

---

## 4. PostgreSQL Relational Schema & Row Level Security (RLS)

All database tables must reside in `public`, enforce foreign key cascades, and have strict RLS enabled:

```sql
BEGIN;

CREATE TABLE IF NOT EXISTS public.[table_name] (
    id UUID PRIMARY KEY,
    user_id UUID NOT NULL REFERENCES auth.users(id) ON DELETE CASCADE,
    title TEXT NOT NULL,
    data JSONB DEFAULT '{}'::jsonb,
    is_active BOOLEAN NOT NULL DEFAULT TRUE,
    created_at TIMESTAMPTZ NOT NULL DEFAULT timezone('utc'::text, now()),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT timezone('utc'::text, now())
);

-- Performance Indices
CREATE INDEX IF NOT EXISTS idx_[table_name]_user_created 
    ON public.[table_name] (user_id, created_at DESC);

-- Enable RLS
ALTER TABLE public.[table_name] ENABLE ROW LEVEL SECURITY;

-- Strict Isolation Policies
CREATE POLICY "Users can only select own records"
    ON public.[table_name] FOR SELECT
    USING (auth.uid() = user_id);

CREATE POLICY "Users can only insert own records"
    ON public.[table_name] FOR INSERT
    WITH CHECK (auth.uid() = user_id);

CREATE POLICY "Users can only update own records"
    ON public.[table_name] FOR UPDATE
    USING (auth.uid() = user_id);

CREATE POLICY "Users can only delete own records"
    ON public.[table_name] FOR DELETE
    USING (auth.uid() = user_id);

COMMIT;
```

---

## 5. Service Layer Interface Contract

```typescript
export interface [Resource]Filter {
  limit?: number;
  offset?: number;
  activeOnly?: boolean;
}

export interface [Resource]Service {
  list(userId: string, filter: [Resource]Filter, client: SupabaseClient): Promise<ListResult>;
  syncBatch(userId: string, items: InputItem[], client: SupabaseClient): Promise<SyncResult>;
  update(userId: string, id: string, patch: Partial<InputItem>, client: SupabaseClient): Promise<Item>;
  delete(userId: string, id: string, client: SupabaseClient): Promise<boolean>;
}
```

---

## 6. HTTP Status & Error Codes

| Status Code | Error Code | Trigger Condition |
| :--- | :--- | :--- |
| `200 OK` | N/A | Successful query, update, or sync |
| `400 Bad Request` | `VALIDATION_ERROR` | Malformed payload or missing required UUID |
| `401 Unauthorized` | `UNAUTHORIZED` | Missing or invalid Supabase Bearer token |
| `403 Forbidden` | `PREMIUM_REQUIRED` | User is on FREE tier without active trial |
| `404 Not Found` | `NOT_FOUND` | Entity does not exist or belongs to another user |
| `500 Server Error` | `INTERNAL_ERROR` | Database or upstream external cloud failure |
