# Fellow Power Optimization — Overview

> **Critical:** For the complete verified power formula derived from real in-game data, see `power-formula.md`. That document supersedes any older math claims.

## Core Formula (Verified)

```
Total Power = (Base × (1 + Σ%) + ΣFlat) × (1 + FinalMultiplier%)
Base = Total Aptitude × Level Multiplier
```

## Key Principle: All Percentage Bonuses Are ADDITIVE

Unlike many gacha games, Isekai: Slow Life does **NOT compound percentage multipliers**. They all add together into a single sum, which is then multiplied with Base Power.

### Real Example (Endgame UR Carry, verified)
The endgame UR Empyrean Sound Inspiring reference carry (Lv 750, 5★) has these percentage bonuses:
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
- Expo: +25.2%
- Resonance Power: +10%

**Total = +8,099.15%** (literally summed)

Final power: `Base × 81.99 + Flat × Final`, which matches the in-game value of 48.47B within 0.014% accuracy.

## Why Aptitude Is King

Because Base Power = Aptitude × Level Multiplier, and Base gets multiplied by the huge percentage sum (8,000%+ for endgame fellows), **every single aptitude point is worth thousands of total power**.

### Example
For the endgame reference:
- Each +1 aptitude point = +15,500 base (Lv 750 multiplier)
- × 81.99 (percentage sum) = **+1.27M total power per aptitude point**
- × 1.14 final = **+1.45M total power per aptitude point**

This is why:
- Skill Pearls (aptitude) matter enormously — +20,965 aptitude observed on the reference
- Costume essence tracks matter
- Fish aptitude skills matter
- Family Stella aptitude contributions matter
- Every tiny aptitude source compounds through the formula

## Power Sources — Complete List

### Aptitude Sources (Flat, Then × Familiar/Skill %)
1. **Base** — Innate per-fellow stat (~20–120)
2. **Skill** — Skill Pearls (Supreme/Outstanding/Ordinary Talent)
3. **Limit Break** — Flat aptitude + level cap raise per limit break
4. **Artifacts** — Equipped artifact's aptitude + materia
5. **Family** — Family Stella blessing aptitude (per family that blesses the fellow)
6. **Costume** — Costume essence tracks + activation bonuses
7. **Stella** — Fellow's group Stella aptitude (Pattern A gives up to +140)
8. **Fish** — Fish Tank aptitude skills
9. **Expo** — Expo aptitude (Expo gives all three buckets — apt, %, flat)
10. **Museum** — Museum antique aptitude
11. **Familiar** — Bound familiar aptitude
12. **Compendium** — Scrapbook system with one page per event
13. **Demon's Blessing** — `[NEEDS VERIFICATION — possibly Archdemons Stella]`
14. **Building Training** — +1 aptitude per Training building level (Gold-gated)
15. **Resonance Skill Aptitude** — Top-tier UR fellows only

### Power % Bonuses (All Additive)
1. **Stars** — Awakening (+10% per star linear, max +60% at 6★)
2. **Family** — Family Stella power % (biggest source for well-supported carries)
3. **Artifacts** — Artifact skill percentages (rolled with Reforge Oils, slot count scales with Quenching Stone awakening)
4. **Skill** — Fellow's innate skills
5. **Fish** — Fish Tank category + all-fellow % skills (the single biggest category)
6. **Expo** — Expo percentage bonuses
7. **Museum** — Museum trophy/antique % bonuses
8. **Familiar** — Familiar bond %
9. **Compendium** — Scrapbook completion bonuses (some % power, mostly from limited events)
10. **Figure** — User avatar system (can alternatively give family intimacy/blessing instead of % power)
11. **Demon's Blessing** — `[NEEDS VERIFICATION]`
12. **Building Training** — Training % track
13. **Stella** — If the Stella provides % power
14. **Resonance Power** — Top-tier fellows only

### Flat Power Bonuses (Add After %)
1. **Stars** — Awakening flat (awakening gives both % and flat)
2. **Family** — Family Stella flat power
3. **Item** — Consumable event items (wrestling towels, fish tank buffs, etc.) — labels show small numbers but the flat bonus amplifies through the whole power pipeline, so always apply items to your main carry
4. **Roaming Encounter** — Roam mechanic where you earn Fame and items; the Bazaar level gates how often other players can take items from you
5. **Negotiation** — Trade Post battle minigame; generates Trade Post Coins for shops and unlocks a gold-generating Trading Post Counter
6. **Stella** — Personal Stella level power (Pattern A flat scales +3M at Lv 1 up to +10M per level at Lv 11+)
7. **Fish** — Flat fish power
8. **Familiar** — Familiar flat
9. **Expo** — Expo flat
10. **Museum** — Museum flat
11. **Building Training** — Flat component of Training
12. **Building Service Level** — Aggregated flat total across matching-typing buildings (see `buildings.md`)

### Final Multiplier (Separate, Applied Last)
1. **Resonance Power** — Top-tier UR fellows with Resonance unlocked `[NEEDS VERIFICATION on whether it's double-counted with the Σ% entry]`
2. **Familiar** — Final multiplier bonus

## Optimization Priority

### Tier 1: Aptitude Maximization
Every aptitude point multiplies with your entire Σ% sum. At endgame, each point is worth millions of power.

1. **Max Supreme Talent Skill Pearls** — start here, then push into the slot unlocks from costumes / Pattern A Stella / Awakening
2. **Equip a top-slot UR artifact** (Magic Lamp, Kanna Plush, or similar high-awakening artifact) — more materia slots = more stacked aptitude
3. **Level Fish Tank aptitude skills** — +1,817 aptitude observed on the reference
4. **Collect all costumes of your main typing** — essence tracks stack across every costume with no diminishing returns
5. **Push Museum antiques** — up to +994 aptitude on the reference
6. **Family Stella maxing** — up to +220 aptitude per maxed UR family Stella, stacked across every family that blesses your main carry

### Tier 2: Percentage Bonus Accumulation
Additive — collect from every source:

1. **Fish %** — up to +2,624% observed (the single biggest source)
2. **Family Stella %** — up to +2,019% observed (biggest after fish — depends on how many families bless your carry)
3. **Artifacts %** — up to +788% (high-awakening artifact with many slots + matching rolls)
4. **Demon's Blessing %** — up to +706%
5. **Museum %** — up to +520%
6. **Skill %** — up to +501%
7. **Familiar %** — up to +310%
8. **Compendium %** — up to +280%
9. **Figure %** — up to +140%
10. **Building Training %** — up to +125%
11. **Awakening stars** — up to +60% at 6★ (small but important — the **aptitude slot unlocks** from awakening are the real value, not the %)
12. **Stella group %** — up to +175% from Empyrean Sound Pattern A
13. **Expo %** — up to +25%

### Tier 3: Flat Power Sources
Less impactful at endgame but still add up:

1. **Building Service Level** — +157M observed (aggregated across matching-typing buildings)
2. **Item** — +467M for the reference (consumable-sourced, amplified through the pipeline)
3. **Family Stella flat** — +15–50M range
4. **Stella flat** — Personal Stella contributes +3M → +49M cumulative across levels
5. **Fish flat** — +16–37M
6. **Museum flat** — +2–9M

## Strategic Insights from the Verified Formula

### Insight 1: Aptitude Investment Compounds Through The Σ%
A +10 aptitude from a costume is worth: 10 × 15,500 × 82 ≈ **+12.7M total power** on the endgame reference. That "tiny" +10 is massive when multiplied through.

### Insight 2: Early-Game % Bonuses Matter More (Relatively)
At 500% total bonus, adding +30% from Awakening is a +6% relative gain. At 8,000% total bonus, adding +30% is a +0.4% relative gain.

**This means:** Focus on % bonuses broadly in the mid-game. Focus on aptitude compounding at endgame.

### Insight 3: Single Carry Meta Still Works (Different Reason Than I Originally Stated)
Stacking bonuses on one fellow gives a significant advantage over spreading, but not because multipliers compound. It works because:
- You get to sum ALL % bonuses on one fellow
- You invest ALL aptitude sources on one fellow
- Both feed the same formula at full concentration

The exact ratio (main carry vs second-string) varies significantly by account — it's not a fixed "10x" rule.

### Insight 4: "Item" and "Building Service Level" Are Major Flat Sources
The endgame reference has +467M from "Item" flat and +157M from "Building Service Level". These aren't trivial — always apply consumable items to your main carry, and push matching-typing buildings for Service Level.

### Insight 5: Awakening's Real Value Is The Aptitude Slot Unlocks
The +10% per star is small at endgame — but each awakening star unlocks **additional aptitude slots** on the fellow, letting you feed more Skill Pearls. Those extra pearls compound through the entire Σ% multiplier, making awakening far more valuable than its raw % bonus suggests.

## Common Misconceptions (Corrected)

❌ "Multipliers compound exponentially" → **All % bonuses are additive**
❌ "Addends are worthless late game" → **Item (+467M) and Building Service Level (+157M) are significant**
❌ "Awakening is the most important multiplier" → **Family Stella and Fish are way bigger — but awakening unlocks aptitude slots which compound through everything**
❌ "Spreading bonuses gives compound returns" → **Both spreading and stacking are additive per source; stacking wins because one fellow accumulates the entire sum of all sources**
❌ "Brave/Unfettered are permanently behind due to no Category Stella" → **They miss ~30% to ~60% of additive pool vs Inspiring's Rani+Elise double stack. Custom-slot families (Lancelot, Hestia, Hanamiya Rica) partially close the gap.**
❌ "Sub-fellow gates compound recursively" → **They don't. The same 25 fellows serve both the 5★ and 6★ gates as you push them up the star ladder over time.**
