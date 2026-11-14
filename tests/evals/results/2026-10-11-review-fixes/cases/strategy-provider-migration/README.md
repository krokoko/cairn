# Payment adapter migration
The existing integration uses the provider's v1 create_charge endpoint with integer cents.
The requested change uses v2 create_payment with amount_minor, currency and a tenant-scoped
idempotency key. Old and new application versions will overlap for one deployment window.
A provider timeout can occur after the provider commits a charge. An application rollback
cannot cancel an already committed charge. The supplied local model predates this migration.
Only local artifacts are included; current provider execution and hosting settings are absent.
