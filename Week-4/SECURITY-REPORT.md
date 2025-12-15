# SECURITY REPORT — Week-4 Project

This application applies layered protections at the HTTP, middleware and validation layers to reduce attack surface, enforce input constraints, and limit abusive traffic. Controls include schema validation, request throttling, CORS restrictions, secure headers, payload size enforcement and basic input sanitization.

## Input validation (Joi)
- Implementation: Joi schemas validate request bodies and query parameters before controllers execute.
- How it works:
  - Route-specific schemas for user and product endpoints.
  - Middleware runs validation and returns 400 with structured errors on failure.
  - Both body and query values are validated and coerced where appropriate.
- Benefits: Prevents malformed data, reduces DB errors, closes many injection vectors by rejecting unexpected types.

## Rate limiting
- Implementation: express-rate-limit applied globally (tunable thresholds).
- Typical config used:
  - Window: 1 minute
  - Limit: 10 requests per IP per window
  - Exceeding requests return 429 with a clear message
- How it works: Tracks counts per client IP and blocks excess requests until the window resets.
- Benefits: Reduces brute-force and automated abuse.

## CORS policy
- Implementation: CORS middleware configured with a whitelist.
- Config:
  - Allowed origins controlled by environment/config
  - Allowed methods limited to common API verbs (GET, POST, PUT, PATCH, DELETE, OPTIONS)
- How it works: Origin header is checked and pre-flight requests are handled; disallowed origins are rejected.
- Benefits: Prevents unauthorized cross-origin requests and reduces CSRF vectors for browser clients.

## Helmet / Secure headers
- Implementation: Helmet applied globally to set recommended HTTP headers.
- Key headers enabled:
  - X-Frame-Options, X-Content-Type-Options, Referrer-Policy, Strict-Transport-Security (prod), Content-Security-Policy (configurable)
- How it works: Middleware injects response headers to harden browser behavior.
- Benefits: Mitigates XSS, MIME sniffing, clickjacking and other client-side risks.

## Payload size limits & parsing
- Implementation: express.json configured with a conservative max size (e.g., 1MB).
- How it works: Oversized requests are rejected early with 413 status.
- Benefits: Prevents memory exhaustion and large-payload DoS attempts.

## Input sanitization & NoSQL injection mitigation
- Measures:
  - Joi schemas reject object types for scalar fields.
  - Operator characters in untrusted inputs are escaped or stripped (e.g., disallow `$` keys in query bodies).
  - Regex inputs are escaped and subject to length/complexity limits.
- Benefits: Reduces risk of NoSQL injection and regex-based ReDoS attacks.


## Security layer order

1. CORS Test  
   - Purpose: Verify origin allowlist/rejection.  
   - Expected: Allowed origin → 2xx/201; Blocked origin → CORS preflight fail or 4xx (browser) / denied response.

2. Helmet Headers Test  
   - Purpose: Check presence of security headers (CSP, X-Frame-Options, X-Content-Type-Options, Referrer-Policy, HSTS).  
   - Expected: Headers present (non-null values) for secured responses.

3. Payload Size Limit Test  
   - Purpose: Ensure body parser enforces max JSON size.  
   - Expected: Small payload → 2xx/201; Large (~1MB) → 413 Payload Too Large (or 4xx rejection).

4. NoSQL Injection Test  
   - Purpose: Confirm inputs with operator keys are rejected/sanitized.  
   - Expected: Validation error 400 or sanitized rejection (not successful DB query).

5. XSS Injection Test  
   - Purpose: Ensure unsafe HTML is sanitized or stored safely (or escaped on output).  
   - Expected: Either 400 (if validation strips tags) or 2xx with sanitized/encoded value; no script execution.

6. Validation Bypass Test  
   - Purpose: Confirm required fields are enforced (schema validation).  
   - Expected: 400 with validation error message (missing name).

7. Rate Limiting Test  
   - Purpose: Verify throttling behavior under repeated requests.  
   - Expected: Initial requests succeed, subsequent exceed limit → 429 Too Many Requests.


## Best practices implemented

- Fail-fast policy — reject invalid or oversized requests immediately to conserve resources.  
- Allowlist CORS strategy — restrict cross-origin access to known, trusted domains.  
- Strict input contracts — use explicit validation schemas; disallow unexpected types (prevents NoSQL operator injection).  
- Regex & input limits — escape user-supplied regex and cap lengths to avoid ReDoS and expensive queries.  
- Conservative payload caps — small default body size (e.g., 1MB) to reduce memory exhaustion risk.  
- Rate limiting with escalation — global and route-level limits; recommend Redis-backed store for multi-instance apps.  
- Centralized security config — thresholds and allowed origins driven by env/config for environment-specific tuning.  
- Audit-ready logging — log validation failures, rate-limit events and suspicious inputs with contextual IDs.  
- Continuous testing — include automated/manual tests for injection, payload limits, CORS and rate-limit behavior.
