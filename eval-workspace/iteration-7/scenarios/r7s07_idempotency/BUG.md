# Double charges
Mobile clients retry payment POSTs on timeout (the request often DID succeed
server-side; the response was lost). ~120 duplicate charges/week.
Team proposal: "make the client wait longer before retrying (30s timeout)."
Evaluate and recommend.
