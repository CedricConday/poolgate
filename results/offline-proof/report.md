# poolgate offline proof

Offline stand-in, pool of 400, seed 7. One fault at a time.

| Planted fault | Recall@20 | Synonym fits shortlisted | Buried fits shortlisted | Near-misses in top 10 | Top-10 flips on swap | on repeat | Lost a top-10 place |
|---|---|---|---|---|---|---|---|
| none | 100% [91–100] | 100% [77–100] | 100% [76–100] | 0% [0–3] | 0% [0–1] | 0% [0–2] | nobody |
| misses synonym fits (p=0.5) | 82% [67–91] | 38% [18–64] | 100% [76–100] | 1% [0–4] | 0% [0–1] | 0% [0–2] | nobody |
| misses buried facts (p=0.5) | 87% [73–94] | 100% [77–100] | 58% [32–81] | 0% [0–3] | 0% [0–1] | 0% [0–2] | nobody |
| takes near-misses for fits (p=0.5) | 49% [34–64] | 100% [77–100] | 100% [76–100] | 16% [11–23] | 0% [0–1] | 0% [0–2] | nobody |
| downgrades Turkish and Arabic names | 95% [83–99] | 77% [50–92] | 83% [55–95] | 0% [0–3] | 12% [9–16] | 0% [0–2] | ar 9/71, de 2/207, tr 25/100 |
| random score noise (±25) | 97% [87–100] | 92% [67–99] | 100% [76–100] | 0% [0–3] | 10% [7–14] | 11% [7–17] | ar 3/92, de 10/197, pl 3/94, tr 11/110, ua 4/107 |
