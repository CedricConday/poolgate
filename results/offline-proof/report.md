# poolgate offline proof

Offline stand-in, pool of 400, seed 7. One fault at a time.

| Planted fault | Recall@20 | Synonym fits shortlisted | Buried fits shortlisted | Near-misses in top 10 | Top-10 flips on swap | on repeat | Lost a top-10 place |
|---|---|---|---|---|---|---|---|
| none | 100% [91–100] | 100% [77–100] | 100% [76–100] | 0% [0–3] | 0% [0–1] | 0% [0–2] | nobody |
| misses synonym fits (p=0.5) | 85% [70–93] | 46% [23–71] | 100% [76–100] | 0% [0–3] | 0% [0–1] | 0% [0–2] | nobody |
| misses buried facts (p=0.5) | 87% [73–94] | 100% [77–100] | 58% [32–81] | 0% [0–3] | 0% [0–1] | 0% [0–2] | nobody |
| takes near-misses for fits (p=0.5) | 49% [34–64] | 100% [77–100] | 100% [76–100] | 14% [9–21] | 0% [0–1] | 0% [0–2] | nobody |
| downgrades Turkish and Arabic names | 95% [83–99] | 77% [50–92] | 83% [55–95] | 0% [0–3] | 11% [8–15] | 0% [0–2] | ar 10/76, de 1/212, tr 23/107 |
| random score noise (±25) | 97% [87–100] | 92% [67–99] | 100% [76–100] | 0% [0–3] | 11% [8–15] | 11% [7–17] | ar 3/96, de 12/185, pl 4/96, tr 10/110, ua 3/113 |
