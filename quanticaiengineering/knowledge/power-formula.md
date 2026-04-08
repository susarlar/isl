# Fellow Power Formula — VERIFIED

> **This is the definitive formula**, derived from real in-game power breakdowns across 7 fellow snapshots collected from a single Inspiring-main account: Fifi (N), Woolf (R), Neptune (UR — under-invested), Stephanie (SSR), Kaye (SSR), Black (SSR), and one endgame UR Empyrean Sound Inspiring carry at Lv 750, 5★. Formula accuracy verified at 99.98%+ against the endgame reference.
>
> Because all data is from one account, cross-account generalizations (e.g., the "main carry is 5-10x stronger than second-string" rule) may not hold everywhere. Formula structure is universal; specific % values are account-dependent.

## The Complete Formula

```
TOTAL FELLOW POWER = (Base × (1 + Σ%) + ΣFlat) × (1 + FinalMultiplier%)

Where:
  Base = Total Aptitude × Level Multiplier
  Total Aptitude = (Σ Flat Aptitude) × (1 + AptFamiliar% + AptSkill%)
```

## 🚨 CRITICAL: All Percentage Bonuses Are ADDITIVE

**The single most important mechanical fact in the game:** power percentage bonuses from different sources **add together**, they do NOT compound.

### Example (Endgame UR Carry, verified)
From a real snapshot of an endgame UR Empyrean Sound Inspiring carry at Lv 750, 5★:

- Stars: +50%
- Family: +2,019.5%
- Artifacts: +788.25%
- Skill: +501%
- Fish: +2,624.5%
- Museum: +519.7%
- Familiar: +310%
- Compendium: +280%
- Figure: +140%
- Demon's Blessing: +706%
- Building Training: +125%
- Resonance Power: +10%
- Expo: +25.2%
- **TOTAL: +8,099.15%** (summed, not multiplied)

Applied as: `Base × (1 + 80.9915) = Base × 81.9915`

If these were multiplicative, the result would be ~10^20 power. It's not. They're additive.

## Verified Math

### Woolf (SR R-rarity, Lv 600)
- Base: 49.25M
- Σ%: 4,708.65%
- ΣFlat: 187.061M
- Final%: 0%
- **Calculated: 2,555,321,125**
- **Actual: 2,555,195,661**
- **Accuracy: 99.995%**

### Endgame UR Carry (UR, Empyrean Sound, Lv 750, 5★)
- Base: 508.7M
- Σ%: 8,099.15%
- ΣFlat: 804.464M
- Final%: 14% (Resonance 10% + Familiar 4%)
- **Calculated: 48,464,637,657**
- **Actual: 48,471,403,770**
- **Accuracy: 99.986%**

## Formula Component Breakdown

### 1. Aptitude Calculation

Aptitude sources ADD flat values, then get multiplied by aptitude-level Familiar% and Skill% bonuses (usually 0, but top fellows get them):

**Aptitude Sources (flat, add together):**
- Base (innate stat, ~20–120 depending on fellow rarity)
- Skill (from Skill Pearls — Supreme/Outstanding/Ordinary Talent)
- Limit Break (from leveling past breakpoints — flat aptitude + level cap raise)
- Artifacts (from equipped artifact's aptitude + materias)
- Family (from Family Stella blessing bonds)
- Costume (from Costume essence track + activations)
- Stella (from Fellow's own Stella group)
- Fish (from Fish Tank aptitude skills)
- Expo (Expo gives aptitude + % power + flat power — all three; do Expo daily)
- Museum (from Museum antiques — typed per-fellow aptitude)
- Familiar (from Familiar binding)
- Compendium (scrapbook system with one page per event — collecting a certain number of fellows from each event unlocks milestone bonuses, some aptitude, some % power, some other. Most Compendium pages are from **limited events**, which means the available progression depends on which events you've participated in historically.)
- Demon's Blessing (assumed to be Archdemons Stella output) `[NEEDS VERIFICATION]`
- Building Training (Gold-gated, +1 aptitude per Training building level; see `buildings.md`)
- Resonance Skill Aptitude (top-tier UR only)

**Aptitude Percentage Bonuses (apply last):**
- Familiar % (e.g., the endgame UR carry has +7.66% Familiar aptitude bonus)
- Skill %

**Formula:**
```
Total Aptitude = (Σ all flat aptitude sources) × (1 + AptFamiliar% + AptSkill%)
```

### 2. Base Power

Base Power = Total Aptitude × Level Multiplier

Level multiplier per aptitude point, from verified real-account snapshots and unverified estimates:

- Lv 1: 300/apt `[NEEDS VERIFICATION]`
- Lv 100: 925/apt `[NEEDS VERIFICATION]`
- Lv 300: 3,362/apt `[NEEDS VERIFICATION]`
- **Lv 500: ~7,588/apt** ✅ (verified — Cimitir snapshot: aptitude 3,747, base +28.43M → 28.43M / 3,747 ≈ 7,588. The old estimate of 7,590 is essentially correct.)
- **Lv 600: ~10,393/apt** ✅ (verified — Gabrael UR snapshot: aptitude 14,403, base +149.7M → 149.7M / 14,403 ≈ 10,393. **This supersedes the earlier "Lv 700 = 13,680" estimate**, which was based on wiki data and cannot be reconciled with the Gabrael Lv 600 snapshot.)
- Lv 700: (not yet verified — previous wiki estimate of 13,680 should not be trusted given the Lv 600 correction)
- **Lv 750: ~15,500/apt** ✅ (verified — endgame UR carry: base 508.7M / aptitude 32,823 ≈ 15,497)

### Verified growth between verified points
- Lv 500 → Lv 600: 7,588 → 10,393 (+37% across 100 levels)
- Lv 600 → Lv 750: 10,393 → 15,500 (+49% across 150 levels)

The multiplier grows roughly 30-40% per 100 levels in the verified range.

**Why intermediate levels like Lv 700 are hard to pin down exactly:** In-game "base power" back-calculations depend on the fellow's total invested state (Skill Pearls, Limit Breaks, Insight, costume slots, etc.). A fellow at Lv 700 with maxed investments may show a different effective base-per-aptitude than one with partial investments, making it tricky to get a clean "just level multiplier" number at every level. The three verified points above (Lv 500, 600, 750) are the cleanest we have — treat intermediate levels as rough interpolation.

### 3. Power Percentage Bonuses (Σ%)

These ADD together. The sum is then multiplied with Base.

**Categories (all additive):**
- Stars (Awakening — +10% per star, linear, max +60% at 6★)
- Family (from Family Stella power bonus to blessed fellow)
- Artifacts (from equipped artifact's skill percentages)
- Skill (from fellow's own talent/skill bonuses)
- Fish (from Fish Tank % skills — category + all fellow)
- Expo (Expo's % power contribution — see Aptitude list above, Expo gives all three buckets)
- Museum (from Museum trophy/antique power %)
- Familiar (from bound familiar)
- Compendium (scrapbook system — some entries give % power bonuses in addition to aptitude)
- Figure (Figure is your **user avatar** system — can give either intimacy+blessing to your entire family, OR % power to fellows, depending on which Figure you've equipped)
- Demon's Blessing (assumed Archdemons Stella) `[NEEDS VERIFICATION]`
- Building Training (% track — Training gives aptitude, % power, and flat power all together)
- Stella (if the Stella gives % power — depends on which Stella)
- Resonance Power (top-tier UR fellows only)

### 4. Flat Power Bonuses (ΣFlat)

Added to the final power AFTER the percentage multiplication. Still additive among themselves.

**Sources:**
- Stars (Awakening also has a flat addend in addition to its % — awakening gives both)
- Family (Family Stella flat power)
- Item (consumable event items — wrestling towels, fish tank buffs, etc. Flat label is small but the value amplifies through the full power pipeline, so always apply items to your main carry)
- Roaming Encounter (you roam randomly on the map to earn **Fame** and items. Roaming stamina regenerates over time and also accumulates when friends gift you back after you gift them. The roaming Bazaar is where items are awarded — the **more leveled up** your Bazaar is, the fewer people can "kick you off" of it to steal your items. **Leveling up the Bazaar has a huge Fame bottleneck** — Fame is the scarce resource here.)
- Negotiation (a battle mini-game where you fight fellows to earn **Trade Post Coins**. Coins are spent in shops — guild shop, banquet shop, challenge shop, etc. The **more battles you win**, the more your **Trading Post Counter** accumulates; you can then upgrade the Trading Post Counter itself, which generates Gold when you claim it. Negotiation is both a flat-power source AND a gold income lever.)
- Stella (if the Stella gives flat power — top UR Stellas give personal +3M–+49M)
- Fish (flat power fish skills)
- Familiar
- Expo (flat power contribution — see Aptitude list for Expo's full three-bucket split)
- Museum (flat museum bonuses)
- Demon's Blessing (flat portion) `[NEEDS VERIFICATION]`
- Building Training (flat component — Training gives aptitude, % power, and flat power all together)
- Building Service Level (aggregated flat total across all matching-typing buildings — see `buildings.md`)

### 5. Final Multiplier (applied AFTER everything)

A separate multiplier at the very end. Known sources:
- Resonance Power (top-tier UR fellows with Resonance unlocked)
- Familiar (final bonus)

Formula:
```
Total = (Base × (1 + Σ%) + ΣFlat) × (1 + FinalMultiplier%)
```

Resonance Power appears in the Final multiplier bracket for fellows with Resonance unlocked — it's a niche top-tier mechanic and only matters once your main carry has Resonance enabled.

**`[NEEDS VERIFICATION]`** In the endgame UR carry's verified breakdown, "Resonance Power +10%" appears in BOTH the Σ% list AND the Final multiplier (Final% = 14% = Resonance 10% + Familiar 4%). The math only reproduces the observed 48.47B total if Resonance is counted in both places. This could mean (a) the game really applies Resonance twice, (b) the in-game UI displays the same value in two places but applies it once, or (c) the snapshot OCR captured the same field twice. Not yet resolved.

**`[NEEDS VERIFICATION]`** Whether there are any OTHER sources that land in the Final multiplier bracket beyond Resonance and Familiar is not confirmed. This list may be incomplete.

## Strategic Implications

### 1. Aptitude Is King (More Than Ever)

Because aptitude feeds Base, and Base gets multiplied by the huge percentage sum (8,099% for the Endgame UR Carry reference!), every single point of aptitude is multiplied by the entire sum.

**For the Endgame UR Carry:** each +1 aptitude = +15,500 × 81.99 = **+1.27M total power** (× 1.14 final = +1.45M)

This is why Skill Pearls, Artifacts, Costume essence track, Fish aptitude, Family Stella aptitude all matter even when they seem like tiny numbers — they ALL get multiplied by the massive percentage pool.

### 2. Single Carry Still Works (But For a Different Reason)

Multipliers do not compound — they add. Single carry still works because:

- One fellow accumulates ALL the % sources on themselves
- Endgame UR Carry at full investment: 8,099% total
- A less-invested roster fellow might have far less
- **The gap varies widely by account** — for accounts that concentrate hard on one main carry the gap can be substantial; for more spread-out rosters it's smaller. Don't treat "5-10x stronger" as a fixed ratio.
- Also factor in the aptitude gap (more investment in main)

### 3. Percentage Sources Don't "Compete"

Since they're additive, you should collect from as many DIFFERENT sources as possible:
- Fish gives 2,624% — massive source
- Family gives 2,019% — massive source
- Artifacts gives 788% — big
- Demon's Blessing gives 706% — big
- Museum gives 520% — meaningful
- Stars only gives up to +60% (6★, linear +10%/star) — small but **Acquaint Stones are scarce**, so don't treat this as "free" — the resource cost is real even if the % gain is modest at endgame
- **Every source matters, no matter how small**

### 4. Flat Bonuses Matter More Than I Thought

The Endgame UR Carry has 804M flat bonuses which add to her 41.7B percentage-multiplied base, contributing ~1.7% to her total. Small but real. At lower investment levels, flat bonuses can be 5–10% of total power.

### 5. Building Service Level Is a Hidden Massive Flat Source

Notice how 4 of the 7 fellows show **+157.1M** in "Building Service Level" — this is a PASSIVE flat bonus given to all fellows whose typing matches a building's typing. Every building has a single typing assignment and boosts only fellows of that typing. Building Service Level comes from leveling up the building through normal gold purchases (diminishing returns per tap). See `buildings.md` for the full breakdown.

### 6. "Item" Flat Power Is From Consumables

The "Item" row (+467M on the Endgame UR Carry) is the stacked contribution from **consumable items** — event rewards like wrestling towels, fish tank buffs, and similar flat-power consumables. The key insight: an item label may say something small like "+100 Fellow Power", but when you apply it to a well-developed fellow the actual contribution is **much larger** because the item's flat bonus goes through the full power pipeline — it gets amplified by the Σ% pool and Final multiplier on that fellow.

**Practical rule:** Always use your consumable items on your main carry. Items applied to low-investment fellows waste most of their potential value.

## Quick Power Calculation Examples

### Scenario: How much does +30% Awakening add?

On the Endgame UR Carry (Base 508.7M, real snapshot):
- Without Awakening: Σ% = 8,049.15 → power contribution = 508.7M × 81.49 = 41,453M
- With Awakening: Σ% = 8,099.15 → power contribution = 508.7M × 81.99 = 41,708M
- **Gain: +255M** (~0.5% total power gain)

On a hypothetical low-investment fellow (illustrative only, Base 50M and Σ% 500%):
- Without: 50M × 6 = 300M
- With +30%: 50M × 6.3 = 315M
- **Gain: +15M** (~5% total power gain)

**Conclusion:** Awakening's +30% is MORE impactful (in relative terms) when your total Σ% is LOW. At endgame with 8,000%+ totals, adding 30% is a rounding error.

### Scenario: How much does a new Fish % skill add?

A +60% Barreleye fish skill on the Endgame UR Carry:
- Adds +60% to fish category in Σ%
- New contribution: 508.7M × 0.60 = +305M direct
- Plus it increases future multipliers on Base
- **Gain: ~305M** (~0.6% total power gain)

On a hypothetical low-investment fellow (illustrative, Base 50M, Σ% 500%):
- Gain: 50M × 0.60 = +30M (~10% total power gain)

## Verified Data Points

### Fifi (N rarity, older fellow)
- Aptitude: 3,816
- Base: 34.09M

### Woolf (R, Lv 600)
- Aptitude: 4,736
- Base: 49.25M
- Total: 2,555,195,661

### Neptune (UR Informed, 120 base apt — under-invested on an Inspiring-main account)
- Aptitude: 4,768
- Base: 49.58M
- **Note:** This snapshot is from an account that mains Inspiring, where Neptune was not a main investment target. Despite having 120 base aptitude as a UR, she appears similar to Woolf here simply because the account never funneled Skill Pearls, artifacts, costume essence, or other aptitude sources into her. **This data point is NOT representative of a fully-invested Neptune.** It illustrates what a 120-apt UR looks like when nobody invests in her, not her ceiling.

### Stephanie (SSR Otherworld Valiants)
- Aptitude: 5,599
- Base: 58.22M

### Kaye (SSR Otherworld Valiants)
- Aptitude: 5,946
- Base: 61.83M

### Black (SSR Elites Inspiring)
- Aptitude: 6,274
- Base: 65.24M
- Total: ~4,254,021,001

### Endgame UR Carry (UR Empyrean Sound Inspiring, endgame, Lv 750, 5★)
- Aptitude: 32,823 (!!)
- Base: 508.7M
- Total: **48,471,403,770**
- Key stats: 20,965 Skill aptitude (Supreme Talent maxed + more), 3,515 Artifact, 1,817 Fish, 1,000 Costume, 994 Museum, 689 Family

**The Endgame UR Carry has 8.6x more aptitude than Black** (32,823 vs 6,274). That aptitude gap alone, multiplied by both a higher Base multiplier AND a higher Σ%, is why she's ~11x more powerful.
