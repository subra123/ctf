You found it! 🎉

The flag is:
```
kashiCTF{50_you_did_endup_ge77ing_the_flag_hehe}
```

Hidden in an HTML comment on `/Index` page!

---

**Writeup for Sanity 1:**

**Challenge:** Sanity 1 (Misc) — "Try searching this site"

**Steps:**
1. Check `robots.txt` → found first half: `kashiCTF{50_you_did`
2. Notice `/flag` page says "try asking a robot" — hints at robot-readable files
3. Run gobuster with `common.txt` → discovers `/Index` (non-standard page)
4. `curl` the `/Index` page and grep for flag → found second half in an **HTML comment**: `_endup_ge77ing_the_flag_hehe}`

**Flag:** `kashiCTF{50_you_did_endup_ge77ing_the_flag_hehe}`

**Lesson:** Always check `robots.txt`, run directory fuzzing, and grep page source for hidden HTML comments!
