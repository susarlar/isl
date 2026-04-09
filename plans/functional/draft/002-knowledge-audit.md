# Plan: Knowledge Base Audit Sweep

## Overview

Finish the systematic doc-by-doc audit of the `knowledge/` base to eliminate hallucinations, unverified claims, and stale wiki data. The audit methodology has already been applied to ~17 docs across several sessions; this plan tracks the remaining docs and documents the audit process so future drift can be caught using the same loop.

## Why This Matters

The bot's answer quality is capped by the accuracy of the knowledge base. We've already caught (and fixed) several load-bearing errors:
- "Multipliers compound exponentially" (wrong — they're additive)
- "Limit breaks act as multipliers" (wrong — they're flat aptitude + level cap raises)
- "Spread EXP stones evenly" (wrong — concentrated leveling wins)
- "Neptune is a top-tier Informed main" (wrong — widely considered weak)
- "Heracles has 0 family blessings" (wrong — he has 6)
- "Hermes has 9 family blessings" (wrong — she has 6)
- "Sea Fishing event" mentioned in 4 docs (wrong — no such system exists)
- "Building Appearance" treated as an active mechanic (wrong — retired event)
- "15 daily targeted dates" math (wrong — random dates can't be targeted)
- "Family Blessing Bond unlock" terminology (wrong — Bond is a different stat)
- "+50% max awakening at endgame" (wrong — +60% at 6★, linear +10%/star)

Each wrong claim directly shapes bot answers. The audit is load-bearing work.

## Audit Methodology (Repeatable)

For each doc, we run a three-step loop:

1. **Enumerate assumptions:** list every load-bearing factual claim, framing, or number in the doc — not as "this is wrong" but as "this is an assertion that could be wrong." Flag particularly: derived math, wiki-sourced numbers, strategic claims, terminology, and generalizations.
2. **User correction pass:** the user (who has the in-game account and is the domain expert) confirms, corrects, or flags "unknown" for each assumption.
3. **Surgical fixes:** apply corrections, mark unknowns with `[NEEDS VERIFICATION]`, rewrite sections where the original framing was fundamentally wrong.

## Progress So Far

| Doc | Status |
|---|---|
| `_INCONSISTENCIES.md` | ✅ Done (merged resolutions, deleted) |
| `fellow-leveling.md` | ✅ Partially done (limit break + EXP stone fixes) |
| `fellow-awakening.md` | ✅ Done |
| `stella.md` / `stella-tables.md` | ✅ Done |
| `fellow-database.md` | ✅ Done + Rarity Capability Matrix added |
| `artifacts.md` | ✅ Done |
| `family-blessings.md` | ✅ Done |
| `family-stella.md` | ✅ Done |
| `families-roster.md` | ✅ New doc (merged blessing-chart.md) |
| `blessing-chart.md` | ✅ Deleted (merged into families-roster.md) |
| `fishing.md` | ✅ Done |
| `power-formula.md` | ✅ Done (Lv 500/600/750 verified, Lv 700 flagged) |
| `buildings.md` | ✅ Done |
| `costumes.md` | ✅ Done (full rewrite) |
| `skill-pearls.md` | ✅ Done (aptitude slot system) |
| `blessing-and-intimacy-strategy.md` | ✅ Done (full rewrite) |
| `advanced-strategies.md` | ✅ Done |
| `category-guide.md` | ✅ Done |
| `typing-mains-guide.md` | ✅ Done |
| `awakening-priority.md` | ✅ Done |
| `events-and-siege.md` | ✅ Done (minor) |
| `guild-guide-strategy.md` | ✅ Done (minor) |
| `fellow-power-overview.md` | ✅ Done |
| `pearls.md` | ✅ Created |
| `top-fellows-quickref.md` | ✅ Created |
| `master-index.md` | ✅ Created (for retrieval) |
| `fellow-tier-list.md` | ⏳ Pending |
| `museum.md` | ⏳ Pending |
| `museum-antiques.md` | ⏳ Partial (Quick Answer section added but not full audit) |
| `leveling-priorities.md` | ⏳ Pending |
| `resource-guide.md` | ⏳ Pending |

## Remaining Docs (Priority Order)

### 🟡 `fellow-tier-list.md`
**Why audit:** tier lists are the most opinionated/subjective docs and most likely to contain outdated meta claims. Also the doc most likely to inadvertently recommend Neptune or mis-categorize fellows. Likely has pre-audit "Single Carry Meta" framing that needs to match the current rewritten `advanced-strategies.md`.

### 🟡 `museum.md`
**Why audit:** doc header already admits "Public wiki data on the Museum is sparse. Most details below need in-game verification." Lots of `[NEEDS VERIFICATION]` territory. Candidates: building operator slot unlock counts (50/200/800/5000), earnings rate progression (100% → 6000%), blueprint costs, "Debt Ledger" mechanic, Museum Rank system, Museum Tasks for Collector titles.

### 🟡 `museum-antiques.md`
**Why audit:** we added a front-loaded "Quick Answer" section during the museum antique bot-refusal fix, but the rest of the doc wasn't fully audited. Candidates: bronze/silver/gold upgrade mechanics, cave typing coverage, the "awake effect" trigger counts (per 30 donations, per 300 trade post opponents, etc.), Mural/Dragon awake scaling.

### 🟢 `leveling-priorities.md`
**Why audit:** small doc, mostly "level targets per rarity" table. Quick pass to confirm targets (450 for non-main roster, 550 for 4★ gate, 700 for 5★, 750 for 6★) and the "main typing fellows outscale other-typing URs once fish kicks in" claim.

### 🟢 `resource-guide.md`
**Why audit:** resource source ordering/priority (Skill Pearls, Crystal Ores, Magic Ore, Blessing Points, Character Fragments). Already cleaned for Sea Fishing references during the fishing audit, but the rest needs a priority-ranking check.

## Acceptance Criteria

- Every doc listed as ⏳ Pending above is ✅ Done
- Each audited doc either has no `[NEEDS VERIFICATION]` flags OR all flags explicitly reference open questions the user couldn't answer
- The vector DB is rebuilt after the last audit pass
- The full audit pass is committed in logical chunks (one commit per doc or per doc-group)
- The audit methodology doc is updated in this plan with any new lessons learned

## Out of Scope

- New feature development (intake v2, rate limiting, etc.)
- Adding content to the knowledge base (this plan is about fixing existing content, not expanding coverage)
- LLM prompt engineering (already covered by separate iteration on `prompts.py`)
- Retrieval layer fixes (already covered by the hybrid retrieval + chunker patches)

## Methodology Lessons Learned (From Prior Audit Passes)

1. **Don't trust any "verified" label in an old doc.** The old `power-formula.md` said "VERIFIED" at the top but was based on OCR from the user's one account, so "verified" meant "consistent with one data point" — not "definitive." Most generalizations from one snapshot turned out to need qualification.

2. **Numbers are load-bearing.** Every specific number (+50% at 5★, 7,590/apt at Lv 500, 15 sub-fellows for 4★ gate, etc.) is a point of potential failure. Flag any number you can't trace back to a real snapshot or explicit user confirmation as `[NEEDS VERIFICATION]`.

3. **Terminology drifts.** "Bond" has two meanings (Intimacy+BP combined stat that gates student rarity VS "Family Blessing bond" which was my incorrect coinage). Audit for terms that mean multiple things in different docs.

4. **Wiki-sourced content is especially risky** because wikis are often outdated for a live gacha game. Family rosters, fellow lists, event schedules, Stella formulas — all need account-anchored verification.

5. **Ask for reasons, not just corrections.** When the user says "Neptune is bad", ask WHY — so the bot can articulate it ("VIP-gated, fragment-capped, weak Stella group"). A bare "don't recommend Neptune" rule without reasons is fragile.

6. **Acquisition matters.** Players don't start with every fellow/family — events gate a lot of content. Strategy docs should always assume the user may not have every piece.

7. **Retrieval quality is downstream of doc structure.** The chunker struggled with heading-only stubs; the retriever struggles with named entities; the master-index doc was needed for meta-queries. When you find an audit-related doc that also retrieves badly, fix both at once.

## Rough Time Estimate

Not estimating — each doc pass takes as long as the user's domain-expert feedback takes. Historically: small docs (~5 assumptions) take 5 minutes of audit + 10 minutes of fixes. Medium docs (~15 assumptions) take 15 minutes + 20 minutes. Large docs with full rewrites take 30+ minutes of combined effort. The 5 remaining docs are mostly small/medium so this should be achievable in 1-2 focused sessions.

## Next Step

Pick one doc from the ⏳ Pending list and run the audit loop on it. Start with `fellow-tier-list.md` because it's most likely to contain wrong strategic framing that contradicts the already-audited `advanced-strategies.md`.

---

# Assumptions Per Remaining Doc

Below is the pre-flight assumption audit for each of the 5 remaining docs. The user can review all of them in one pass and give feedback in batches, rather than doing an interactive Q&A per doc.

## 1. `fellow-tier-list.md`

### 1.1 Stale / wrong content (already obvious from comparison with audited docs)
- **Line 10:** *"Amaterasu — Best ecosystem support (2 Cat Stella + most family blessings)"* — the "2 Cat Stella" refers to Rani+Elise stacking on Inspiring, which we verified. But "most family blessings" isn't quite accurate — she has 7 families, tied with Sunna and Freesia. Small overclaim.
- **Line 13:** *"Neptune — VIP 8, solo Divine Gospel Stella owner"* — this doc still frames Neptune as a top-tier carry. Needs the "DO NOT RECOMMEND" framing we applied elsewhere.
- **Line 14:** *"Orivita — Pairs with Hermes for double UR Unfettered"* — OK framing, matches what we know.
- **Line 90:** *"Divine Gospel | A (UR, +175%) | Personal fragments | Neptune (only Stella unlocked), Mammon, Trady, Mescal, Shlomo"* — doesn't mention VIP gating, rarity split (Neptune UR vs Mammon/Trady/Mescal/Shlomo SSR), or that Mammon/Trady/Mescal/Shlomo follow Pattern C rhythm not Pattern A. Needs to match the corrected `stella-tables.md`.
- **Line 91:** *"Archdemons | B (SSR, +50%/+100% Lv20)"* — the "+100% at Lv 20" claim is new and not in `stella-tables.md`. Is Archdemons Lv 20 actually +100%? Our stella-tables shows +3M flat per level from 21-40 but doesn't show a "+100% at Lv 20" breakpoint. **Risk:** wiki-sourced or invented.
- **Line 104-107:** *"Single Carry Meta — This one fellow should represent 30-50% of your total power"* — we verified elsewhere that the actual gap varies by account and isn't a fixed ratio. The "30-50%" claim should be softened.
- **Line 111-113:** *"Archdemons are the cheapest gate-fillers ... shared Purple Stars"* — this is the same "shared currency = cheaper for awakening" claim we corrected in `fellow-awakening.md`. Purple Stars are for Stella, not Awakening. Awakening uses Acquaint Stones which are the same cost for every fellow.
- **Line 126-128:** *"Amaterasu (Base 120, fully invested): Total aptitude 32,823, Total Power 48.47B"* — not anonymized. Should use "Endgame UR Carry" to match power-formula.md.
- **Line 135-141:** **Type Comparison table** — lists "Neptune" as Informed best carry. Should be Aegle. The whole row is stale.
- **Line 138:** *"Inspiring — Has Cat Stella (Rani + Elise) — Best max power"* — OK, matches our verified stacking.
- **Line 140:** *"Brave — NO Cat Stella — Permanent -30% category gap"* — correct.
- **Line 141:** *"Unfettered — NO Cat Stella — Has 2 URs (Orivita + Hermes) but no Cat Stella"* — correct.

### 1.2 Aptitude ranking table claims
- **Line 41:** *"~75 Aptitude — Avar, Lux, Super, Ira, Acedia (Archdemons)"* — assumes all 5 Archdemons are 75 apt. Verified? Probably from wiki.
- **Line 42:** *"~75 Aptitude — Kaye, Stephanie, Nip, Salvo, Avril (Otherworld Valiants)"* — same, all 5 at 75 apt. Wiki assumption.
- **Line 44:** *"~70 Aptitude — Emosen, Ida, Jewlry, Augustine, Anne, Loya, Mulberry, Bubo (Followers)"* — same, all 8 at 70 apt. Suspicious uniformity.
- **Line 24:** *"~100 Aptitude — Hermes (UR Ancient Magi, economic boost)"* — is Hermes actually 100 base apt or is this wiki? She's UR Ancient Magi which we established should be 120 base apt for all Magi URs. **Contradiction: fellow-database.md lists Hermes at ~100, but the "All Empyrean Sound and Ancient Magi UR fellows are 120 base apt" rule from the user's latest statement would put her at 120. Which is correct?**
- **Line 25:** *"~100 Aptitude — Mescal (Unfettered, Divine Gospel, Tier SS combat)"* — is Mescal actually 100 base apt?
- **Line 19:** *"~110 Aptitude — Shlomo (Inspiring, Divine Gospel, VIP 7)"* — is Shlomo actually 110?
- **Line 30:** *"~90 Aptitude — Trady (Diligent, Divine Gospel, VIP 4)"* — is Trady actually 90?

**All the base aptitude numbers for Divine Gospel and sub-120 fellows need verification.** The user said "all Empyrean Sound and Ancient Magi URs are 120 base apt". What about Divine Gospel URs? If Divine Gospel Neptune is 120 but Hermes (Magi) is 100, that contradicts the "all Magi are 120" statement. This is a load-bearing inconsistency.

### 1.3 Power Tier List claims
- **Lines 52-73:** The SS/S/A/B/C power tier list uses Ira/Salvo/Kaye/Lux/Mammon as top picks. These are all ~75 apt SSR fellows. **But** the whole point of the 120-apt analysis is that aptitude matters most at endgame. A tier list that puts 75-apt SSRs in Tier SS contradicts the "120-apt UR is the best carry" logic elsewhere in the same doc. **Is this tier list measuring "combat score at a specific stage" vs "max endgame power"?**
- **Line 79:** *"Tier B — Beginner-Friendly (Outscaled at 45+) — Angie, Liz, Adeline, Cimitir, Elise, Rani, Quenchy"* — this lists Rani and Elise as "outscaled at 45+" but elsewhere we've established they're essential +60% category boost for Inspiring mains. **Is this doc calling the SR Category Stella fellows "outscaled" while other docs call them "essential"? Contradiction.**

### 1.4 Stella Group Quick Reference
- **Line 87-100:** Stella pattern table. Claims Empyrean Sound/Ancient Magi/Divine Gospel all give "+175%" at Lv 10. Already noted in stella-tables.md that the actual per-level breakdown is more nuanced. Also: "(Lv20 +100%)" for Archdemons needs verification.
- **Line 100:** *"(Standalone) | D (SR, +30% category)"* — OK but should note it's +30% per standalone, and Inspiring has +60% from Rani+Elise stacking.

---

## 2. `museum.md`

The doc header already admits: *"Public wiki data on the Museum is sparse. Most details below need in-game verification."* So most of this doc is already flagged as unverified. Key assumptions I'd question:

### 2.1 Building Earnings
- **Line 25-30:** Earnings progression: 100% at Lv 1, 200% at Lv 2, 6000% at Lv 16. **Is this accurate, or wiki-sourced?** The jump from 200% to 6000% over 14 levels is suspicious — doesn't fit any simple growth curve I can see.
- **Line 27:** *"Max employees (Lv1) 1,000 / Max employees (Lv20) 20,000"* — verified?
- **Line 33-36:** *"Level 5: 165 blueprints / Level 6: 220 / Level 15: 2,200"* — suspicious sparse data, wiki-sourced?

### 2.2 Fellow Operating Slots
- **Line 41-45:** Slot unlocks at 50, 200, 800, 5000 employees. Is this accurate?
- **Line 47:** *"Cimitir is the specialty fellow"* — confirmed earlier? Probably yes based on fellow-database.

### 2.3 Trophy list
- **Line 55-79:** Complete trophy list mapping events to trophies. Most entries are plausible but the "Penglai Immortal Trophy", "Bubble Trophy", "Frantic Forest Trophy" etc. naming is wiki-sourced. **Which trophies are real and which are invented wiki entries?**

### 2.4 Claims to validate
- **Line 123:** *"Museum's Debt Ledger has been mentioned in patch notes"* — what is this and does it still exist?
- **Line 99-103:** *"Museum rank system received a May 2025 update"* — is this a real patch or wiki speculation?
- **Line 115-117:** *"Little Collector / Elite Collector fixed titles"* — real?
- **Line 130-131:** Recommends "Augustine, Stephanie, Super, and any UR Informed (Neptune, Ao Li, Aegle)" as best Informed fellows for Museum. **Still lists Neptune.** Needs the Neptune update.

---

## 3. `museum-antiques.md`

Already has the Quick Answer section at the top from my earlier fix. Remaining unaudited claims:

### 3.1 Per-typing antique table
- **Line 66:** *"Oyster Trap / per 30 guild donations → +% Inspiring power"* — verified trigger count?
- **Line 67:** *"Narwhal / per 300 trade post opponents defeated"* — verified trigger count?
- **Line 68:** *"Sledge / per 500 educations"* — verified trigger count?
- **Line 69:** *"Bear-Eared Seal / per 100 field trips"* — verified?
- **Line 70:** *"Mammoth / per X study tour rewards claimed"* — "X" is explicit placeholder. **Need actual number.**

### 3.2 Event pass antiques
- **Line 77-80:** Gold Poker (Casino on Yacht), Medal of 15 Trials (Cloud Kingdom), Mysterious Cauldron (Penglai). Names and source events confirmed? These are event-gated so availability depends on whether those events have ever run on the user's account.

### 3.3 Cave / Excavation antiques
- **Line 87-91:** Mural, Dragon, Ironhead Turtle, Abandoned Portal. All claims about what cave they're in and what they do need verification.
- **Line 97-102:** **Cave typing coverage table** — Memory Cave, Frozen Abyss, Ice Shipwreck, Original Ruins. Are these 4 caves real and current? Verified? The "Original Ruins — GET ONE OF EACH AND GET OUT" advice is suspicious because it assumes completion, not investment. Is that still the meta?
- **Line 91:** *"Abandoned Portal — Excavation cave | SSR(+) aptitude / All Fellow Power %"* — real antique?
- **Line 90:** *"Ironhead Turtle — Frozen Abyss / Ice Shipwreck — SSR(+) aptitude / Open Celebration Banquets (free banquets)"* — the "opens Celebration Banquets" awake effect is an unusual mechanic. Confirmed?

### 3.4 Celebration Banquets section
- **Line 119-122:** Three banquet types (regular 4 people, wine/grape 8 people, celebration free). Is this accurate?

### 3.5 Bronze/Silver/Gold upgrade mechanics
- **Line 110-115:** *"Bronze → Silver → Gold with diminishing returns at each tier"* — do these tiers actually work the way I described, or is it a simpler system where you just spend any points to upgrade?

---

## 4. `leveling-priorities.md`

Small doc, mostly a priority table. Few assumptions:

### 4.1 Level targets per rarity
- **Line 11-14 (Main Typing targets):** *"Main typing SSR: 600, then 650 slowly / Main typing N/R/SR: 600 down the line"* — is pushing **even N fellows of your main typing to 600** really correct? The claim is "lower-rarity main-typing fellows outscale other-typing URs once fishing kicks in." **Is this true? It implies a massive crystal investment on N fellows — seems extreme.**
- **Line 24-29 (Other typings targets):** *"N/R/SR/SSR other typings: 450. UR other typings: 500-550"* — where do these specific numbers come from? Is 450 a real gate or wiki guess?
- **Line 31:** *"You only need Lv 550 for the 4★ awakening gate"* — we verified 550 is the 4★ gate level in fellow-awakening.md ✓

### 4.2 The "outscale" claim
- **Line 15:** *"When sorted by power, your lower-rarity main typing fellows will eventually pass UR fellows of other typings — the typing-wide multipliers (Fish, Family, Stella, costumes) compound enough that even an N main-typing fellow can outpower a non-main UR"* — **Is this actually true?** It's a specific empirical claim. Given the verified formula (additive % pool, base aptitude × level multiplier), an N fellow with ~20 base apt vs a UR with 120 base apt at the same level would need the N's typing-wide multipliers to compensate for 6x less base aptitude. That's a lot. **Has the user actually observed this, or is it wiki speculation?**

### 4.3 Sorting tip
- **Line 18:** *"Always sort fellows by power and unequip all artifacts first to get accurate comparisons"* — is "unequip artifacts" an actual game action? Or is the user expected to mentally subtract artifact contributions? If it's a real action, is the UI for it named correctly?

### 4.4 Crystal conservation
- **Line 46-52:** Crystal spending recommendations. The claim "Save crystals for the Lv 700 → Lv 750 push for your main carry (5★ → 6★ gate)" aligns with verified awakening gates. ✓

---

## 5. `resource-guide.md`

Resource sources + priorities. Quick pass:

### 5.1 Priority rankings
- **Line 13:** *"Acquaint Stones Priority: Event commissions > Event gacha > Crafting > Fountain"* — is this ranking correct? We verified fountain drops are rare + slow in fellow-awakening.md. Event commissions as #1 is plausible but unverified.
- **Line 25:** *"Skill Pearls Priority: Fishing event ranking > Event shops > Battle Pass > Crafting"* — fishing event ranking #1 implies tournament competition; is it really the top source?
- **Line 37:** *"Crystal Ores Priority: Guild Exchange > Event shops > Fishing event ranking > Adventure"* — Guild Exchange is listed #1. Plausible.

### 5.2 Specific source numbers
- **Line 10:** *"Crafting: 20 Fragments → 1 Acquaint Stone"* — verified in fellow-awakening.md audit ✓
- **Line 19:** *"Fishing event shop: 1-5 skill pearls (5,000 pts each)"* — is 5,000 pts the correct price?
- **Line 20:** *"Fishing event ranking (Rank 1): 15 Skill Pearls"* — verified?
- **Line 33:** *"Fishing event ranking: Up to 40 Bravery Ore (Rank 1)"* — verified?

### 5.3 Blessing Points section
- **Line 47-53:** *"Dating Family members / Sailing Trip: Good amount + 1 child / Airship Journey: Good amount + twins"* — we removed Sailing Trip from family-blessings.md because it wasn't confirmed. Should also be removed here. Airship Journey we confirmed as event-sourced and spent on School task. The framing here is stale.

### 5.4 Character Fragments section
- **Line 56-** (not shown but likely): gacha dupe rates, character shop, event drops. Any specific numbers need verification.

### 5.5 Magic Ore / Blueprint sources
- **Line 39-46:** Magic Ore sources (Adventure stages, Event rewards, Guild Exchange). Plausible but specific amounts not given.

---

# Summary Of Risk Profile

| Doc | Risk | Blocker For Bot Answers? |
|---|---|---|
| **fellow-tier-list.md** | 🔴 HIGH — contains "Neptune best Informed", "Rani/Elise outscaled", suspicious aptitude numbers for Ancient Magi fellows (Hermes ~100 vs the "all Magi are 120" rule), and the "+100% at Archdemon Lv 20" claim that isn't in stella-tables.md. Also the Tier SS power ranking contradicts the 120-apt-UR primacy argument in the same doc. **High impact on tier list questions.** | Yes — any "who is the best X main" query will hit this doc |
| **museum.md** | 🟡 MEDIUM — the doc admits most content is wiki-sourced and unverified. Main risk is stale trophy lists and the Lv 16 earnings claim. Still references Neptune as an Informed operator. | Museum-specific questions will hit this, but the doc already hedges heavily |
| **museum-antiques.md** | 🟡 MEDIUM — cave taxonomy and trigger count numbers (30 / 300 / 500 / 100 / X) need verification. The Quick Answer at the top is already fixed. | Antique questions will hit this but the Quick Answer usually answers them well |
| **leveling-priorities.md** | 🟡 MEDIUM — the "push N fellows of your main typing to Lv 600" claim is extreme. If wrong, the doc is actively misleading. | Leveling questions will hit this |
| **resource-guide.md** | 🟢 LOW — mostly source lists with some specific numbers. Priority rankings are the main unverified claims. Sailing Trip reference needs cleanup to match family-blessings.md. | Resource questions will hit this but most answers are bounded by ordering |

## Audit Order Recommendation

1. **`fellow-tier-list.md` first** — highest risk, contradicts other audited docs in multiple places, and is central to "who should I main" questions
2. **`leveling-priorities.md`** — medium risk, small doc, resolves quickly
3. **`resource-guide.md`** — low risk, small doc, mostly cleanup
4. **`museum-antiques.md`** — medium risk, mostly trigger-count verification
5. **`museum.md`** — medium risk, already heavily hedged, lowest priority
