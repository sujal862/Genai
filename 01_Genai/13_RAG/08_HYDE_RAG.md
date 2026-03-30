HyDE works by generating a fake but plausible answer to the query using an LLM, then embedding that hypothetical answer instead of the raw query for vector search.
Why? Because a generated answer lives in the same semantic space as your actual documents — much closer than a short user question does.
Flow: Query → LLM generates fake answer → embed it → vector search → retrieve real chunks → final answer.
Strength: Works great when queries are casual/question-form but documents are dense and technical (e.g. Kubernetes docs).
Risk: If the LLM hallucinates a totally wrong hypothetical, retrieval gets worse, not better.






