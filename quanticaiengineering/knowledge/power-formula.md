# Fellow Power Formula — VERIFIED

> **This is the definitive formula**, derived from real in-game power breakdowns across 7 fellows (Fifi, Neptune, Woolf, Stephanie, Kaye, Black, Amaterasu). Accuracy verified at 99.98%+.

## The Complete Formula

```
TOTAL FELLOW POWER = (Base × (1 + Σ%) + ΣFlat) × (1 + FinalMultiplier%)

Where:
  Base = Total Aptitude × Level Multiplier
  Total Aptitude = (Σ Flat Aptitude) × (1 + AptFamiliar% + AptSkill%)
```

## 🚨 CRITICAL: All Percentage Bonuses Are ADDITIVE

**The single most important mechanical fact in the game:** power percentage bonuses from different sources **add together**, they do NOT compound.

### Example (Amaterasu, verified)
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
- Building Appearance: +0%
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

### Amaterasu (UR, Empyrean Sound, Lv 750, 6★)
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
- Limit Break (from leveling past breakpoints)
- Artifacts (from equipped artifact's aptitude + materias)
- Family (from Family Stella blessing bonds)
- Costume (from Costume essence track + activations)
- Stella (from Fellow's own Stella group)
- Fish (from Fish Tank aptitude skills)
- Expo (from Expo exhibits)
- Museum (from Museum trophies)
- Familiar (from Familiar binding)
- Compendium (from Compendium completion)
- Demon's Blessing
- Building Appearance
- Building Training
- Event Power Conversion
- Resonance Skill Aptitude (top-tier only)

**Aptitude Percentage Bonuses (apply last):**
- Familiar % (e.g., Amaterasu has +7.66% Familiar aptitude bonus)
- Skill %

**Formula:**
```
Total Aptitude = (Σ all flat aptitude sources) × (1 + AptFamiliar% + AptSkill%)
```

### 2. Base Power

Base Power = Total Aptitude × Level Multiplier

Level multiplier at Level 750 ≈ **15,500 per aptitude point** (back-calculated from Amaterasu's 508.7M / 32,823 apt).

Earlier estimates from leveling doc:
- Lv 1: 300/apt
- Lv 100: 925/apt
- Lv 300: 3,362/apt
- Lv 500: 7,590/apt
- Lv 700: 13,680/apt
- Lv 750: ~15,500/apt (verified)

### 3. Power Percentage Bonuses (Σ%)

These ADD together. The sum is then multiplied with Base.

**Categories (all additive):**
- Stars (Awakening)
- Family (from Family Stella power bonus to blessed fellow)
- Artifacts (from equipped artifact's skill percentages)
- Skill (from fellow's own talent/skill bonuses)
- Fish (from Fish Tank % skills — category + all fellow)
- Expo
- Museum (from Museum trophy power %)
- Familiar (from bound familiar)
- Compendium
- Figure (from Figure collection)
- Demon's Blessing
- Building Appearance
- Building Training
- Stella (if the Stella gives % power — depends on which Stella)
- Resonance Power (top-tier fellows only)

### 4. Flat Power Bonuses (ΣFlat)

Added to the final power AFTER the percentage multiplication. Still additive among themselves.

**Sources:**
- Stars (Awakening flat bonus)
- Family (Family Stella flat power)
- Item (miscellaneous item bonuses)
- Roaming Encounter
- Negotiation
- Stella (if the Stella gives flat power — top UR Stellas give personal +3M–+49M)
- Fish (flat power fish skills)
- Familiar
- Expo
- Museum (flat museum bonuses)
- Demon's Blessing
- Building Appearance
- Building Service Level

### 5. Final Multiplier (applied AFTER everything)

A separate multiplier at the very end. Only certain sources appear here:
- Resonance Power (appears in both % and final) **[NEEDS VERIFICATION — possible double-count]**
- Familiar (final bonus)

Formula:
```
Total = (Base × (1 + Σ%) + ΣFlat) × (1 + FinalMultiplier%)
```

**[NEEDS VERIFICATION]:** Amaterasu's data shows "Resonance Power +10%" in BOTH the regular Power Percentage Bonus list AND the Final Power Bonus (%) list. The verified math (48.47B) only matches if Resonance Power is counted in BOTH places. Either the game really applies it twice or the OCR captured the same field twice. Needs in-game verification.

## Strategic Implications

### 1. Aptitude Is King (More Than Ever)

Because aptitude feeds Base, and Base gets multiplied by the huge percentage sum (8,099% for Amaterasu!), every single point of aptitude is multiplied by the entire sum.

**For Amaterasu:** each +1 aptitude = +15,500 × 81.99 = **+1.27M total power** (× 1.14 final = +1.45M)

This is why Skill Pearls, Artifacts, Costume essence track, Fish aptitude, Family Stella aptitude all matter even when they seem like tiny numbers — they ALL get multiplied by the massive percentage pool.

### 2. Single Carry Still Works (But For a Different Reason)

I was wrong earlier when I said multipliers compound. They don't. But single carry still works because:

- One fellow accumulates ALL the % sources on themselves
- Amaterasu at full investment: 8,099% total
- Second-string fellow: maybe 3,000% total
- Gap: ~3x raw power from percentages alone
- Plus aptitude gap (more investment in main)
- Result: main carry is 5–10x stronger than second-string

### 3. Percentage Sources Don't "Compete"

Since they're additive, you should collect from as many DIFFERENT sources as possible:
- Fish gives 2,624% — massive source
- Family gives 2,019% — massive source  
- Artifacts gives 788% — big
- Demon's Blessing gives 706% — big
- Museum gives 520% — meaningful
- Stars only gives 50% — small but free
- **Every source matters, no matter how small**

### 4. Flat Bonuses Matter More Than I Thought

Amaterasu has 804M flat bonuses which add to her 41.7B percentage-multiplied base, contributing ~1.7% to her total. Small but real. At lower investment levels, flat bonuses can be 5–10% of total power.

### 5. Building Service Level Is a Hidden Massive Flat Source

Notice how 4 of the 7 fellows show **+157.1M** in "Building Service Level" — this is a PASSIVE flat bonus given to ALL fellows based on your village development. It's additive across all fellows. Push your buildings.

**[NEEDS VERIFICATION]:** The exact mechanic for Building Service Level is undocumented. It appears tied to total building development level (sum of all building levels?) or village rank. Same for the "Item" flat bonus (+467M on Amaterasu) — likely a consumable or permanent item buff but the source is unconfirmed.

## Quick Power Calculation Examples

### Scenario: How much does +30% Awakening add?

On Amaterasu (Base 508.7M):
- Without Awakening: Σ% = 8,049.15 → power contribution = 508.7M × 81.49 = 41,453M
- With Awakening: Σ% = 8,099.15 → power contribution = 508.7M × 81.99 = 41,708M
- **Gain: +255M** (~0.5% total power gain)

On a low-investment fellow with Base 50M and Σ% 500%:
- Without: 50M × 6 = 300M
- With +30%: 50M × 6.3 = 315M
- **Gain: +15M** (~5% total power gain)

**Conclusion:** Awakening's +30% is MORE impactful (in relative terms) when your total % is LOW. At endgame with 8,000%+ totals, adding 30% is a rounding error.

### Scenario: How much does a new Fish % skill add?

A +60% Barreleye fish skill on Amaterasu:
- Adds +60% to fish category in Σ%
- New contribution: 508.7M × 0.60 = +305M direct
- Plus it increases future multipliers on Base
- **Gain: ~305M** (~0.6% total power gain)

On a low-investment fellow (Base 50M, Σ% 500%):
- Gain: 50M × 0.60 = +30M (~10% total power gain)

## Verified Data Points

### Fifi (SR-tier, older fellow)
- Aptitude: 3,816
- Base: 34.09M

### Woolf (R, Lv 600)
- Aptitude: 4,736
- Base: 49.25M
- Total: 2,555,195,661

### Neptune (UR Informed, ~120 apt)
- Aptitude: 4,768
- Base: 49.58M
- Note: Despite being 120 apt UR, Neptune's aptitude is similar to Woolf's here because of OCR data snapshot conditions

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

### Amaterasu (UR Empyrean Sound Inspiring, endgame)
- Aptitude: 32,823 (!!)
- Base: 508.7M
- Total: **48,471,403,770**
- Key stats: 20,965 Skill aptitude (Supreme Talent maxed + more), 3,515 Artifact, 1,817 Fish, 1,000 Costume, 994 Museum, 689 Family

**Amaterasu has 8.6x more aptitude than Black** (32,823 vs 6,274). That aptitude gap alone, multiplied by both higher Base multiplier AND higher Σ%, is why she's 11x more powerful.
