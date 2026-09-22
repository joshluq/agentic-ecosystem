---
name: supabase-edge-functions
description: Scaffolds, tests, and validates serverless Edge Functions built with TypeScript and Deno on Supabase. Handles webhook processing, background tasks, and secure API integrations.
---

# Supabase Edge Functions (TypeScript / Deno)

Skill for engineering high-performance serverless **Edge Functions** on Supabase running on the **Deno** runtime.

---

## 1. Edge Function Design Architecture

- **Runtime**: Deno with modern TypeScript.
- **Location**: `supabase/functions/<function-name>/index.ts`.
- **CORS Handling**: Universal preflight handling via `serveWithOptions` or custom headers.
- **Authentication**: JWT verification via Supabase Client (`@supabase/supabase-js`).

---

## 2. Standard Edge Function Template

```typescript
// supabase/functions/calculate-renting-penalty/index.ts
import { serve } from "https://deno.land/std@0.168.0/http/server.ts";
import { createClient } from "https://esm.sh/@supabase/supabase-js@2";

const corsHeaders = {
  "Access-Control-Allow-Origin": "*",
  "Access-Control-Allow-Headers": "authorization, x-client-info, apikey, content-type",
};

serve(async (req) => {
  if (req.method === "OPTIONS") {
    return new Response("ok", { headers: corsHeaders });
  }

  try {
    const authHeader = req.headers.get("Authorization");
    if (!authHeader) {
      return new Response(JSON.stringify({ error: "Missing Authorization header" }), {
        status: 401,
        headers: { ...corsHeaders, "Content-Type": "application/json" },
      });
    }

    const supabaseClient = createClient(
      Deno.env.get("SUPABASE_URL") ?? "",
      Deno.env.get("SUPABASE_ANON_KEY") ?? "",
      { global: { headers: { Authorization: authHeader } } }
    );

    // Get current authenticated user
    const { data: { user }, error: userError } = await supabaseClient.auth.getUser();
    if (userError || !user) {
      return new Response(JSON.stringify({ error: "Unauthorized" }), {
        status: 401,
        headers: { ...corsHeaders, "Content-Type": "application/json" },
      });
    }

    const { contractId, currentKm } = await req.json();

    // Query contract bounded by user
    const { data: contract, error: dbError } = await supabaseClient
      .from("vehicle_contracts")
      .select("*")
      .eq("id", contractId)
      .eq("user_id", user.id)
      .single();

    if (dbError || !contract) {
      return new Response(JSON.stringify({ error: "Contract not found" }), {
        status: 404,
        headers: { ...corsHeaders, "Content-Type": "application/json" },
      });
    }

    const excessKm = Math.max(0, currentKm - contract.max_kilometers);
    const penaltyPerKm = 0.12; // 0.12 EUR per excess km
    const penaltyTotal = excessKm * penaltyPerKm;

    return new Response(
      JSON.stringify({
        excessKilometers: excessKm,
        penaltyAmount: penaltyTotal,
        currency: "EUR",
      }),
      {
        status: 200,
        headers: { ...corsHeaders, "Content-Type": "application/json" },
      }
    );
  } catch (err) {
    return new Response(JSON.stringify({ error: err.message }), {
      status: 500,
      headers: { ...corsHeaders, "Content-Type": "application/json" },
    });
  }
});
```

---

## 3. Testing & Validation Commands

```bash
# Local testing with Supabase CLI
supabase functions serve calculate-renting-penalty --no-verify-jwt

# Deploy to Supabase Cloud
supabase functions deploy calculate-renting-penalty
```
