# Day 8 Task Results

## Configuration
- Chat model: `openai/gpt-oss-120b`
- Embedding provider: FastEmbed
- Embedding model: `BAAI/bge-small-en-v1.5`
- MAX_DISTANCE: `0.6`

## Test Results

| # | Tools called (in order) | Agent's answer (short) | Correct? (Y/N) | If N, why? |
|---|---|---|---|---|
| 1 | search_handbook | CGPA 6.5 or above for placement eligibility | Y | — |
| 2 | check_exam_eligibility | 70% attendance requires condonation; Rs. 500 per course | Y | — |
| 3 | get_course_fee, search_handbook, get_course_fee, calculator | Total is Rs. 32,000 | Y | — |
| 4 | calculator | Five-day late fee is Rs. 500; total is Rs. 30,500 | Y | — |
| 5 | None | Does not know; not covered in the handbook | Y | — |

## Relevance Guard
- France query: The agent did not answer from general knowledge and stated that the answer was not covered in the handbook.
- Threshold used: `MAX_DISTANCE = 0.6`.
- Record the actual similarity scores for both queries after measuring them with the configured embedding model.
## Relevance Guard

- Embedding model: `BAAI/bge-small-en-v1.5`
- Placement query best score: `0.1768` (`placement_policy.md`)
- France query best score: `0.5731` (`hostel_rules.md`)
- Threshold: `MAX_DISTANCE = 0.6`
- The placement query retrieves relevant placement information.
- The France query's best match is unrelated, so the relevance guard should reject it if no relevant chunks pass the threshold.