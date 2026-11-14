# REQ-TERMINAL revision 4
Approved 2026-10-10 by the developer-display domain owner, Mira.
The Status enum has QUEUED, RUNNING, DONE and CANCELLED. is_terminal returns False for
QUEUED and RUNNING, and True for DONE and CANCELLED. This is the complete input domain.
The expected table was authored by the domain owner before the current implementation.
No behavior for arbitrary strings, foreign objects or dynamically modified enum classes is promised.
