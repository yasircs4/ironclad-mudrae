# Synthetic checker example

Run the exact command in the repository README. It should return STRUCTURALLY_COMPLETE_PENDING_REVIEW and release_authorized: false. It verifies an explanatory document's presence and hash, not application correctness. All files and identities here are synthetic. No screenshots, tests or provider outcomes are invented.

Changing the contract without changing the owner-pinned hash must return INVALID_INPUT. Changing the explanatory artifact must return INCOMPLETE. Run experiments on a separate copy and preserve the shipped example.
