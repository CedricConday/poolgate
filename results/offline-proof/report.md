# poolgate offline proof

Offline stand-in, pool of 400, seed 7. One fault at a time.

| Planted fault | Recall@20 | Synonym fits shortlisted | Buried fits shortlisted | Near-misses in top 10 | Flips on swap | Flips on repeat | Lost a shortlist place |
|---|---|---|---|---|---|---|---|
| none | 100% [91–100] | 100% [78–100] | 100% [76–100] | 0% [0–3] | 0% [0–1] | 0% [0–2] | nobody |
| misses synonym fits (p=0.5) | 85% [71–93] | 43% [21–67] | 100% [76–100] | 0% [0–3] | 0% [0–1] | 0% [0–2] | nobody |
| misses buried facts (p=0.5) | 88% [74–95] | 100% [78–100] | 58% [32–81] | 0% [0–3] | 0% [0–1] | 0% [0–2] | nobody |
| takes near-misses for fits (p=0.5) | 48% [33–63] | 100% [78–100] | 100% [76–100] | 15% [10–22] | 0% [0–1] | 0% [0–2] | nobody |
| downgrades Turkish and Arabic names | 95% [83–99] | 79% [52–92] | 83% [55–95] | 0% [0–3] | 13% [9–17] | 0% [0–2] | ar 10/63, de 1/231, tr 27/101 |
| random score noise (±25) | 98% [87–100] | 93% [69–99] | 100% [76–100] | 0% [0–3] | 12% [9–16] | 12% [8–18] | ar 3/83, de 14/198, pl 6/96, tr 10/117, ua 3/106 |
