---
name: supabase-db-triage
description: Audits PostgreSQL schemas, enforces Row Level Security (RLS) policies, validates database migrations, and designs high-performance indexes on Supabase.
---

# Supabase Database & Security Triage

Specialized skill for **PostgreSQL on Supabase**, focusing on relational modeling, **Row Level Security (RLS)** enforcement, migration safety, and query performance.

---

## 1. Golden Rules of Supabase Database Architecture

1. **Mandatory Row Level Security (RLS)**:
   Every single public table MUST have RLS enabled. Never expose an unprotected table to PostgREST.
   ```sql
   ALTER TABLE public.contracts ENABLE ROW LEVEL SECURITY;
   ```

2. **Strict User Isolation**:
   Data belonging to a user MUST be bounded by `auth.uid()`.
   ```sql
   CREATE POLICY "Users can only read their own contracts"
   ON public.contracts
   FOR SELECT
   USING (auth.uid() = user_id);
   ```

3. **Atomic Migrations**:
   All migration scripts in `supabase/migrations/<timestamp>_<name>.sql` must be transactional and idempotent.
   ```sql
   BEGIN;
   -- Migration steps here
   COMMIT;
   ```

4. **Foreign Key Indexing**:
   Always create indexes on columns used in `WHERE`, `JOIN`, or RLS policies (e.g. `user_id`, `created_at`).

---

## 2. Standard Migration Template

```sql
-- Migration: Create Vehicle Contracts Table
BEGIN;

CREATE TABLE IF NOT EXISTS public.vehicle_contracts (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES auth.users(id) ON DELETE CASCADE,
    plate_number TEXT NOT NULL,
    max_kilometers INT NOT NULL CHECK (max_kilometers > 0),
    start_date DATE NOT NULL,
    end_date DATE NOT NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT timezone('utc'::text, now()),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT timezone('utc'::text, now()),
    CONSTRAINT valid_dates CHECK (end_date > start_date)
);

-- Index for RLS and lookup
CREATE INDEX IF NOT EXISTS idx_vehicle_contracts_user_id ON public.vehicle_contracts(user_id);

-- Enable RLS
ALTER TABLE public.vehicle_contracts ENABLE ROW LEVEL SECURITY;

-- Policies
CREATE POLICY "Users select own vehicle contracts"
    ON public.vehicle_contracts FOR SELECT
    TO authenticated
    USING (auth.uid() = user_id);

CREATE POLICY "Users insert own vehicle contracts"
    ON public.vehicle_contracts FOR INSERT
    TO authenticated
    WITH CHECK (auth.uid() = user_id);

CREATE POLICY "Users update own vehicle contracts"
    ON public.vehicle_contracts FOR UPDATE
    TO authenticated
    USING (auth.uid() = user_id)
    WITH CHECK (auth.uid() = user_id);

COMMIT;
```

---

## 3. RLS Security Audit Checklist

- [ ] Does every table have `ENABLE ROW LEVEL SECURITY`?
- [ ] Are policies restricted to `TO authenticated` or `TO anon` explicitly?
- [ ] Are updates guarded with both `USING` and `WITH CHECK` clauses?
- [ ] Are sensitive audit tables (`audit_logs`) insert-only without update/delete policies?
- [ ] Are functions declared with `SECURITY DEFINER` and explicit `SET search_path = public`?

---

## 4. Automated Verification Gate: `backend_sanity_check.py`

The pre-handoff quality gate for Backend developers (`Senior Backend Developer` -> `Backend QA Engineer`).

### Capabilities:
1. **TypeScript Type Safety**: Executes `tsc --noEmit` to verify type soundness with 0 errors.
2. **Automated Tests**: Runs `npm test` and enforces 0 failures and >= 1 passing test.
3. **Database Security Audit**: Statically audits all PostgreSQL migrations in `supabase/migrations/*.sql`:
   - Checks that all `CREATE TABLE` statements have paired `ALTER TABLE ... ENABLE ROW LEVEL SECURITY;`.
   - Verifies tenant isolation in policies (`auth.uid() = user_id`).
   - Scans for hardcoded service_role keys or secrets leakage.
   - Verifies idempotency (`IF NOT EXISTS`) and transaction boundaries.

### Usage:
```bash
# Full Backend Pre-Handoff Quality Gate
python scripts/backend_sanity_check.py --project-dir ./ --feature-id FEAT-009 --output handoffs/dev_to_qa_FEAT-009.json

# Statically Audit PostgreSQL Migrations Only
python scripts/backend_sanity_check.py --project-dir ./ --audit-migrations-only

# Generate Synthetic Compliant Sample Payload
python scripts/backend_sanity_check.py --mock-sample --output handoffs/sample_backend_handoff.json

# Audit Existing Handoff Payload
python scripts/backend_sanity_check.py --dev-handoff handoffs/dev_to_qa_FEAT-009.json
```

