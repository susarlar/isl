# Knowledge Base Inconsistency Audit

> This doc tracks internal logic inconsistencies in the knowledge base. Use it to identify what needs fixing or verification before adding new content.

## Resolution Status Legend
- **🔴 BROKEN** — Definitely wrong, contradicts verified in-game data, must fix
- **🟡 UNCLEAR** — Possibly wrong or conflicting between docs, needs verification
- **🟢 NOTED** — Acknowledged limitation, flagged in docs

---

## 🔴 BROKEN Inconsistencies (Fix Required)

### #1: Limit Breaks "act as multipliers"
**Files:** `fellow-leveling.md` lines 20, 61
**Problem:** Says limit breaks "act as multipliers, not addends." This contradicts the verified power formula.
**Reality:** From real fellow data, "Limit Break" appears as a flat aptitude contribution (+50 to +65). It's an aptitude source, not a multiplier. Limit breaks ALSO raise the level cap (which lets you level higher = bigger Base via the level multiplier table).
**Fix:** Replace "multipliers" with "aptitude bonuses + level cap raises".

### #2: Born Aptitude = 100 (+5/level) claim
**Files:** `fellow-database.md` line 22
**Problem:** Says "UR Empyrean Sound fellows have Born Aptitude of 100 (+5 per level)". This came from the Fandom wiki.
**Reality:** From verified in-game data (Amaterasu, Neptune, etc.), the "Base" aptitude shown in-game IS the "120 apt" community number — it's a STATIC base, not a leveling formula. Amaterasu's Base+120, Neptune's Base+120, Stephanie's Base+75, Black's Base+80, Woolf's Base+35, Fifi's Base+20.
**Fix:** Remove the "100 +5/level" claim. Document Base aptitude as a fixed per-fellow stat.

### #3: "120 apt fellow before multipliers" math
**Files:** `fellow-tier-list.md` lines 121-125
**Problem:** "120 × 13,680 = 1,641,600 base (before multipliers)" — this implies multipliers apply ON TOP of base, suggesting compound. Also misleads readers about what "120 apt" means.
**Reality:** Base = TOTAL aptitude × level multiplier. The "120" in tier lists is the BASE component of aptitude, not total. Amaterasu's actual total aptitude is 32,823 (not 120). Then total power = (Base × (1 + Σ%) + Flat) × Final.
**Fix:** Clarify that "120 apt" is the base component, and demonstrate the full calculation using verified Amaterasu math.

### #4: "Spread EXP Stones evenly because additive nature"
**Files:** `fellow-leveling.md` line 67
**Problem:** "Spread EXP Stones evenly — the additive nature means you get more total power from leveling 10 fellows from 100→200 than pushing one fellow from 500→600"
**Reality:** This is wrong. While the formula is additive in % bonuses, leveling a fellow:
1. Raises their level multiplier (not additive — multiplicative on each fellow's base)
2. Each level of investment compounds with that fellow's existing aptitude pool
A fellow already at 500 with 5,000 aptitude going to 600 gains way more power than 10 fellows at 100 going to 200. Single-carry meta still wins for leveling.
**Fix:** Reverse the advice — push your main carry's level first, spread leftovers.

### #5: Stella.md claims "12 known Stella groups"
**Files:** `stella.md`
**Problem:** Counts standalone SR Category fellows (Rani, Elise, Liz, Angie) as "groups" — they're not groups, they're standalone Pattern D fellows.
**Reality:** There are 11 actual groups + 4 standalone Category Stella fellows.
**Fix:** Clarify the distinction.

---

## 🟡 UNCLEAR / Needs Verification

### #6: Awakening percentage scaling beyond 3★
**Files:** `fellow-awakening.md`
**Problem:** Doc says 1★=+10%, 2★=+20%, 3★=+30%, but Amaterasu (likely 6★ at Lv750) shows only "Stars+50%" total.
**Conflict:** If linear progression continued, 6★ would be +60%. But Amaterasu shows +50%. Possible reasons:
1. The percentage caps or scales non-linearly past 3★
2. Amaterasu is actually 5★, not 6★ (Lv750 might just be the level cap, not a 6★ requirement)
3. The "+10% per star" was always wrong/wiki misinformation
**Action needed:** Confirm with in-game data. What's the actual % bonus per star at 4★/5★/6★?

### #7: Rani + Elise SR Category Stella stacking
**Files:** Multiple strategy docs
**Problem:** We assumed Rani's +30% and Elise's +30% both stack additively (total +60% to all Inspiring fellows).
**Conflict:** Never verified — could be capped at one Category Stella per type.
**Action needed:** Confirm in-game whether having both Rani and Elise Stella unlocked gives +60% or +30% to Inspiring fellows.

### #8: Resonance Power double-counting
**Files:** `power-formula.md`
**Problem:** Amaterasu's data shows "Resonance Power +10%" in BOTH the regular Power Percentage Bonus list AND the Final Power Bonus (%) list.
**Conflict:** Only fellow with this. Either:
1. It really is double-counted (applied once in Σ%, once in Final)
2. The OCR captured the same field twice
3. The game shows it in both places but only applies once
**Action needed:** Verify in-game whether Resonance Power is one bonus or two.

### #9: "Item +467M" mystery flat power
**Files:** `power-formula.md`, `advanced-strategies.md`
**Problem:** Amaterasu has "+467M" from "Item" in flat power bonuses. We don't know what this is.
**Action needed:** Identify what "Item" power source is in-game (consumable buff? Permanent item? Set bonus?)

### #10: "Building Service Level +157.1M" passive
**Files:** `power-formula.md`
**Problem:** 4 of 7 fellows show identical "+157.1M Building Service Level" — looks like a passive village-wide bonus, but no doc explains the mechanic.
**Action needed:** Document how Building Service Level works and how to increase it.

### #11: Ancient Magi member count
**Files:** `stella.md` says 5 members (Phanes, Nemetona, Andras, Ao Li, Hermes)
**Files:** `fellow-database.md` says Hermes is in Ancient Magi (Unfettered)
**Conflict:** Hermes was originally listed as Ancient Magi in the wiki. But the user later put Hermes in Empyrean Sound (as Brave). Then they corrected and said Hermes is in Magi (Unfettered).
**Action needed:** Final confirmation — is Hermes in Magi or Empyrean Sound? What's her type?

### #12: Stella Lv11+ assumptions
**Files:** Multiple docs
**Problem:** Strategy docs reference "max Stella" without specifying what level. Pattern A (UR groups) verified Lv1-20. Pattern B verified Lv1-20 (Archdemon goes to Lv40). Pattern C (Followers) only Lv1-10. Pattern D (SR Category) only Lv1-10.
**Action needed:** Either get the higher-level data or stop saying "max" when we don't know the cap.

### #13: Mio's Fan as a "UR" artifact
**Files:** `artifacts.md`
**Problem:** "Mio's Fan" is listed as "(UR? unique)" in real account examples but doesn't appear in the Magic Lamp/Kanna Plush UR list. Probably a unique fellow-specific artifact for Mio.
**Action needed:** Clarify if there are fellow-specific unique artifacts vs the standard pool.

---

## ✅ RESOLVED (User-verified, 2026-04-07)

### #R1: Hanamiya Rica is family
- **Status:** Resolved. Rica is an SSR family (upgradable to UR with custom fellow boosts). Streamer collab.

### #R2: UR* / UR+ artifacts confirmed
- **Status:** Resolved. UR+ artifacts have aura (upgradable like Stella with character pieces) plus extra materia slots.

### #R3: Quench is a separate resource
- **Status:** Resolved. Quench is different from Magic Ore. Used to awaken new skill slots on artifacts. Has diminishing returns.

### #R4: Echo artifacts are fellow-specific
- **Status:** Resolved. Echo artifacts only boost specific fellows (e.g., Milim artifact for Unfettered, Allucia artifact for Diligent). Only worth upgrading if the fellow is your main typing.

### #R5: Support tag is a separate artifact category
- **Status:** Resolved. Support-tagged artifacts give bonus power to "the equipped fellow" (any fellow), not a specific one.

### #R6: Materia +2 means slot unlocks
- **Status:** Resolved. Boosting materia "to +2" means unlocking 2 materia slots first, then later boosting to +5.

### #R7: Siege Warfare 1% loss is per-match-chain only
- **Status:** Resolved. The 1% per win loss only applies during a single match chain — recovers between chains.

### #R8: Awakening unlocks artifact level cap
- **Status:** Resolved. Aegle 4★ unlocks "Level limit for all artifacts +18", plus other bonuses (Negotiation, Expo sales, etc.). Magi's fellow and Rimuru also unlock artifact caps.

### #R9: Mio 4★ awakening boosts blessing points
- **Status:** Resolved. Mio 4★: each date with a family member gives that member +9% more blessing points.

### #R10: Mulberry boosts familiar tower combat
- **Status:** Resolved.

### #R11: Crysta boosts SSR fellows
- **Status:** Resolved.

### #R12: Kaye boosts banquet popularity
- **Status:** Resolved.

### #R13: 7 fishing locations confirmed
- **Status:** Resolved. Spots are: Village River, Drakenburg River Bank, Drakenburg Lake Center, Drakenburg Inner Lake, Crushed Ice, Glacier Bay, Unfrozen Sea Cave.

### #R14: Aegle Stella 10 free path
- **Status:** Resolved. 1 free daily gacha ticket → trade points for Aegle fragments → Stella 10 over time.

### #R15: Treasure Hunt = Excavation Game
- **Status:** Resolved. Same minigame, different name in different contexts.

### #R16: Celebration Banquet is a free banquet
- **Status:** Resolved. Free banquet (regular = 4 people beer/cheese, wine/grape = 8 people, celebration = free, opened by Ironhead Turtle awakening).

### #R17: Antiques and Trophies are separate
- **Status:** Resolved. Antiques come from the excavation minigame, trophies come from event rankings.

## 🟢 NOTED / Acknowledged

### #14: Lokia and Ixtchel rarity-upgrade mechanic
**Status:** Documented in `fellow-database.md`. SSR fellows that become UR (and change groups for Lokia: Diligent SSR → Empyrean Sound UR).

### #15: Wiki data is generally outdated
**Status:** Memory file flags this — trust user data over wiki for newer content.

### #16: Group Stella data gaps
**Status:** Uncrowned, Greyrat Family, Dungeon Challenger have only partial member lists. Documented in stella-tables.md.

### #17: Building system gaps
**Status:** Only Museum has detailed data. Other 15+ buildings undocumented. Listed in gap audit.

### #18: SR fellows have no group sets
**Status:** User confirmed. SR families don't have blessing sets; SR fellows like Fawna are standalone with no group affiliation.

---

## Cross-Doc Conflicts

### #C1: Bren rarity
- **Old (wrong):** "Bren (4x)" in some docs — implied a special "4x blessing" tier
- **Verified:** Bren is SSR with 8 blessing slots
- **Status:** Fixed in `category-guide.md`, `blessing-chart.md`. Verify nothing else mentions "4x".

### #C2: Magellan/Jewlry as family vs fellow
- **Old (wrong):** Magellan and Jewlry listed as family-Stella-based custom slot families
- **Verified:** Both are fellows. Magellan = Elites (Inspiring SSR). Jewlry = Followers (Diligent SSR). Lancelot is the family that fixes-blesses both as fellows.
- **Status:** Fixed in `blessing-chart.md`, `fellow-database.md`. Verify nothing else lists them as family.

### #C3: Sylphiette type
- **Old (wrong):** Listed as a fellow with TBD type
- **Verified:** Sylphiette is family, not fellow. Families have no type.
- **Status:** Fixed in `fellow-database.md`, `blessing-chart.md`.

---

## Recommended Verification Questions for User

When ready to fully resolve, ask the user:

1. What % bonus does each star give from 0★ to 6★ exactly?
2. If you have both Rani Stella and Elise Stella unlocked, do they stack to +60% on Inspiring fellows or only +30%?
3. What is "Item" as a flat power source? Where does the +467M on Amaterasu come from?
4. What is Building Service Level? How is it calculated?
5. Is Hermes in Ancient Magi (Unfettered) or Empyrean Sound? What's her type?
6. Are there fellow-specific unique artifacts (like Mio's Fan) outside the standard pool?
7. Does Resonance Power get applied twice (once in % sum, once in final multiplier)?

## Recommended Actions for Bot Quality

1. **Fix Limit Break wording** in `fellow-leveling.md` — replace "multipliers" with correct math
2. **Reverse the EXP Stone advice** in `fellow-leveling.md` — single-carry leveling is correct
3. **Remove Born Aptitude 100+5 claim** in `fellow-database.md`
4. **Update fellow-tier-list.md** Why 120 Aptitude section with verified math
5. **Add flag tags** in docs for unverified items (e.g., `[NEEDS VERIFICATION]`)
