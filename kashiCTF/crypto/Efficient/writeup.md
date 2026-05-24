Here's the full writeup summarized cleanly.

The core insight: the challenge title "Efficient" and the "twice as fast" description hint that the author skipped generating a second prime entirely — using `n = p²` instead of `n = p·q`. This single shortcut makes factoring trivial no matter how large `n` is.

The attack chain is just 5 steps: spot the perfect square → extract `p` with `isqrt()` → compute `φ(p²) = p(p-1)` → get private key `d` → RSA decrypt to get AES key → AES-CBC decrypt the flag. The `ct2` value in the file was a red herring and wasn't needed.
