# Approved requirements
REQ-TOTAL revision 1: total_cents returns the sum of supplied integer item amounts.
REQ-PAY revision 2, approved 2026-10-10 by payments owner:
A tenant and payment key identify one durable charge for 24 hours. The same key and
payload return its original charge; a conflicting payload must be rejected.
Revision 1 covered retries for five minutes only.
