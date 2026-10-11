# Payment requirements revision 3
Approved 2026-10-10 by payments owner.
REQ-AMOUNT: For USD, preserve the integer amount in minor units; reject unsupported currencies.
REQ-ID: For one tenant and key, identical payloads return one durable charge ID for 24 hours.
A different tenant has an independent key namespace. Conflicting payloads are rejected.
REQ-RETRY: Timeout after commit and process restart must not cause a second charge.
REQ-MIGRATE: The v1/v2 overlap must preserve the same durable idempotency identity;
customers must not be charged again when a retry reaches the other application version.
Expired keys require an explicit caller decision; do not automatically charge again.
