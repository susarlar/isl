# Buildings — Fellow Power Contributions

Buildings are a major, often underrated source of fellow power. Every building in your village has a **single typing assignment** (Brave, Diligent, Unfettered, Inspiring, or Informed) and contributes power **only to fellows matching that typing**. Push buildings whose typing matches your main carry.

## The Three Building-Sourced Power Contributions

Each building provides up to three distinct bonuses to fellows of its matching typing:

### 1. Building Service Level (Flat Power)
A flat power bonus bought directly with **Gold**. Every tap raises the Building Service Level, which raises the flat power contribution to fellows of that building's typing.

- **Pricing:** Diminishing returns — each tap costs more than the last
- **Appears in the power breakdown as:** `Building Service Level +XXX`
- **Verified value:** +157.1M is seen on 4 of the 7 verified fellow snapshots, showing a well-developed Inspiring-side village stack
- **Applies to:** All fellows whose typing matches the building's typing
- **Strategy:** Keep tapping until the marginal gold cost exceeds your income — this is pure gold → power conversion with no RNG

### 2. Building Training (Aptitude Gacha)
A gacha-style system that raises the **aptitude** contribution of fellows matching the building's typing. This is the "Building Training" line that appears in both the flat aptitude sources and the Σ% breakdown.

**How the gacha works:**
- Each press costs **Gold** (cost scales with current Building Training level)
- You can press the button **up to 20 times per level**
- Within those 20 presses you have a chance to hit a **roll-up** that advances you to the next level early
- If you don't hit a roll-up in 20 presses, **pity kicks in** — you still advance to the next level but only gain **+1 aptitude** at the transition
- Higher the Building Training level, the more gold each press consumes
- A lucky early roll-up gives you more aptitude per gold spent than hitting pity

**In practice:** Building Training is RNG-gated — sometimes you level up in 2 presses, sometimes you burn all 20 and hit pity. It's still worth pushing, but don't panic when you hit pity streaks.

### 3. Building Appearance / Fellow Power % Gacha
A **second gacha track**, mechanically identical to Building Training but targeting **Fellow Power %** instead of aptitude. This contributes to the Σ% pool on fellows of the matching typing.

- Same 20-press-per-level structure with a pity mechanic
- Same gold-cost scaling (higher level = more gold per press)
- Same RNG pattern — lucky roll-ups beat pity
- **Appears in the power breakdown as:** `Building Appearance +X%` (and/or under Building Training %, depending on which track)

## Typing Matchmaking

**Each building has exactly one typing.** A Brave-tagged building's Service Level, Training, and Appearance tracks boost ONLY Brave fellows. If your main carry is Diligent, pumping gold into a Brave-typed building does nothing for them.

**Strategic implication:** Audit your buildings and identify which ones match your main carry's typing. Those are your highest-ROI buildings. Buildings of the "wrong" typing are still worth maintaining for economy but not for fellow power pushes.

## Priority Order

When investing gold into buildings for fellow power:

1. **Building Service Level** on matching-typing buildings — deterministic, no RNG, pure gold → flat power
2. **Building Training (aptitude gacha)** — aptitude is multiplied by everything else so it scales hard
3. **Building Appearance (power % gacha)** — additive into Σ% pool, high value on well-developed fellows

If your main carry is Inspiring, do all three tracks on every Inspiring-tagged building. Ignore the tracks on other-typed buildings until you've capped the matching ones.

## Where It Shows Up in the Formula

Recalling the complete formula:
```
TOTAL FELLOW POWER = (Base × (1 + Σ%) + ΣFlat) × (1 + FinalMultiplier%)
```

Building contributions land in these buckets:
- **Building Training aptitude** → added to flat aptitude sources → feeds into `Base`
- **Building Training %** → added to the Σ% pool → multiplies `Base`
- **Building Appearance %** → added to the Σ% pool → multiplies `Base`
- **Building Service Level** → added to ΣFlat → adds after the % multiplication

Because aptitude and % both sit upstream of the massive Σ% multiplier, Building Training is disproportionately valuable on well-developed fellows with high Σ% totals.

## Pity Budgeting Tips

- Don't spend gold on gacha tracks until you've maxed Service Level at the current tier — Service Level has no RNG
- If your gold income is tight, prefer Service Level taps (deterministic) over gacha presses
- When you do push gacha: commit to going all 20 presses at a level so you at least bank the pity — stopping mid-level wastes partial progress
- Higher building levels have dramatically higher gold costs per press — plan your village gold income accordingly

## Gaps in This Doc

- Exact gold-cost scaling per Building Training / Appearance level is not in our verified data
- Per-building typing assignments are not enumerated here (depends on your village layout)
- If you have data on max Building Training / Appearance caps or exact pity math, contact **Su**
