# Buildings — Fellow Power Contributions

Buildings are a major, often underrated source of fellow power. Every building in your village has a **single typing assignment** (Brave, Diligent, Unfettered, Inspiring, or Informed) and contributes power **only to fellows matching that typing**. Push buildings whose typing matches your main carry.

## ⚠️ Skill Pearls Are NOT Used On Buildings

**Skill Pearls only unlock fellow aptitude talents** (Supreme / Outstanding / Ordinary Talent). You cannot spend Skill Pearls on any building system. Buildings are powered exclusively by **Gold** and **Building Upgrade Blueprints**.

If you see a recommendation telling you to "spend Skill Pearls on buildings", it's wrong — Skill Pearls belong on fellows.

## Fellow-Power Contributions From Buildings

Buildings contribute to Fellow Power through **two** permanent mechanics plus one retired event mechanic:

1. **Building Service Level** — flat power purchased with Gold, aggregated across all matching-typing buildings
2. **Building Training** — aptitude gained per level-up of the Training building (Gold-gated with a 20-press pity per level)
3. **Building Appearance** — `[RETIRED EVENT]` a limited event that gave Fellow Power %; not currently obtainable

### 1. Building Service Level (Flat Power)

The `Building Service Level +XXX` line in the fellow power breakdown is the **aggregated total** across **several buildings** of the matching typing — it is NOT the output of a single button. Each typing-matching building you own has its own Service Level track that you push with Gold, and their contributions sum under the one "Building Service Level" line in the fellow power breakdown.

- **Pricing:** No hidden RNG — each tap gives a deterministic amount of flat power. **But** the cost per tap **increases the more Service Level you've already bought** for that typing — same escalation pattern as hiring employees or spending Date Points. The more you push, the more expensive the next tap becomes.
- **Appears in the power breakdown as:** `Building Service Level +XXX` (aggregated across all matching-typing buildings)
- **Applies to:** All fellows whose typing matches one of the buildings you pushed
- **Verified value:** +157.1M is seen on 4 of the 7 verified fellow snapshots, showing a well-developed Inspiring-side village stack
- **Strategy:** **Spread your gold across multiple matching-typing buildings** rather than dumping everything into one. Each individual building's cost curve is exponential, so two buildings at low-to-mid level beat one building at high level for the same gold spend.

### 2. Building Training (Aptitude)

A Gold-gated system that raises the **aptitude** contribution of fellows matching the building's typing. Each **level** of the Training building gives **+1 aptitude per level** to matching-typing fellows (so Training building at level 50 = +50 aptitude).

**How levelling works:**
- Each press costs **Gold**. Within a given Training level, all presses cost **the same** (flat). Between levels, the next level's per-press cost is **exponentially** higher than the previous level's.
- You can press the button **up to 20 times per level** — this is the **hard cap**.
- Within those 20 presses you can hit a **roll-up** early and advance to the next level before press 20. Early roll-ups are cheaper overall because you spent fewer presses at the current level's price.
- If you don't hit a roll-up in 20 presses, press 20 is a **hard-pity guaranteed level up** — you still advance to the next level.
- **Whether you roll up early or hit pity at 20, you gain the same +1 aptitude per level.** Early roll-ups save gold, not aptitude.

**In practice:** Building Training is gold-expensive but deterministic in its aptitude gain. RNG only determines how much gold you burn to reach each new level, not the aptitude reward itself.

### 3. Building Appearance (Retired Event — Fellow Power %)

`[RETIRED EVENT]` Building Appearance was a **limited event mechanic** that gave a Fellow Power % bonus. It is no longer actively obtainable. If you see `Building Appearance +X%` on an older account's power breakdown, it's a remnant of that event. **Do not plan around acquiring Building Appearance** — new investment there is not an option.

## Village-Earnings Systems On Buildings (NOT Fellow Power)

Buildings also have two investment tracks that affect **village earnings (gold income)** — they do NOT contribute to Fellow Power. Don't confuse these with the Fellow Power mechanics above.

### Hiring Employees (Hire Cards or Gold)
Each building has an employee count. More employees → more gold income per second. You hire employees with either **Hire Cards** or **Gold**.

- **Gold hires** are available at all times but the cost **escalates rapidly** — past a certain point, Gold hiring becomes prohibitively expensive.
- **Hire Cards** become the only realistic way to add more employees once Gold cost gets out of hand. Save your Hire Cards for buildings whose typing matches your main earning-typing.
- Max employees per building is capped by the building's **upgrade level** (see Blueprints below) — you can't hire beyond the cap no matter how much Gold or how many Hire Cards you have.
- **Employees only contribute to village earnings (gold income).** They do NOT contribute to Fellow Power. Do not hire employees hoping it will strengthen your main carry — it won't.

### Building Upgrade Blueprints (Blueprints Only — No Gold)
Buildings level up by consuming **Building Upgrade Blueprints** obtained from events, village quests, and shop purchases. Upgrades cost **only Blueprints** — no Gold component.

- Upgrading a building **boosts the gold earned per employee per second** (higher building level = more throughput per employee)
- Upgrading also **raises the max employee cap** so you can hire more employees after the upgrade
- Blueprint requirement scales steeply at higher levels
- **Upgrades do NOT affect Fellow Power contributions** — Building Service Level and Building Training are independent of building upgrade level. Upgrades are a pure village-earnings lever.
- Prioritize upgrading buildings whose typing matches your main **earning** typing (for gold income), not necessarily your main carry's typing

### Fellow Assignment to Buildings (Village Earnings Boost)
You can **assign fellows to buildings**. Assigned fellows give the building a **% boost in earnings per second** based on:
1. The **fellow's level** (higher level = bigger % boost)
2. The number of **Study Notes** you've invested into that fellow (more notes = bigger % boost)

This assignment affects **gold income**, not Fellow Power. A high-level fellow with lots of Study Notes assigned to your biggest-earning building can dramatically increase gold throughput.

**Strategic implication:** Your "best-Fellow-Power fellow" and your "best-building-assignment fellow" can be different fellows. Your main carry is whoever has the most multiplier stack; your best building assignments go to whichever high-level Study-Note-invested fellows fit your earning buildings' typings.

## Typing Matchmaking

**Each building has exactly one typing.** A Brave-tagged building's Service Level, Training, and Appearance tracks boost ONLY Brave fellows. If your main carry is Diligent, pumping gold into a Brave-typed building does nothing for them.

**Strategic implication:** Audit your buildings and identify which ones match your main carry's typing. Those are your highest-ROI buildings. Buildings of the "wrong" typing are still worth maintaining for economy but not for fellow power pushes.

## Priority Order for Fellow Power Investment

When investing Gold into buildings for fellow power, always restrict to **buildings whose typing matches your main carry**, then within that set:

1. **Spread investment across multiple matching-typing buildings, not one.** Because each building's Service Level cost grows exponentially, parallelizing low-level taps across several buildings is dramatically cheaper than pushing one building deep.
2. **Push the LOWEST-Service-Level buildings first** — cheapest marginal power-per-gold sits on whichever building you've pushed the least.
3. **Training building levels** give +1 aptitude per level and should be pushed continuously — early roll-ups save gold, but you get the same aptitude reward whether you roll up or hit pity.
4. **Building Appearance** `[RETIRED EVENT]` — skip, no longer obtainable.

**Anti-pattern:** Don't pour gold into your already-highest-Service-Level building. Each successive tap there is more expensive than the taps you could have taken on any under-leveled sibling of the same typing.

If your main carry is Inspiring, do Service Level and Training on every Inspiring-tagged building, in parallel, starting with the lowest-level ones.

## Fellow-Power vs Village-Earnings — Separate Budgets

Buildings have two completely independent investment lanes:

| Lane | What It Costs | What It Gives | Typing Match |
|------|--------------|---------------|--------------|
| **Fellow Power lane** | Gold (Service Level + Training) | Fellow Power on matching-typing fellows | Must match your main carry |
| **Village Earnings lane** | Hire Cards, Gold, Blueprints | Gold income per second | Can match a different typing |

Your main carry's typing drives the Fellow Power lane. Your best earning buildings (which might be a different typing) drive the Village Earnings lane. These are separate budgets — pushing one does not help the other. Don't hire employees "for fellow power" (they don't help) and don't push Service Level "for gold income" (that's not what it does).

## Where It Shows Up in the Formula

Recalling the complete formula:
```
TOTAL FELLOW POWER = (Base × (1 + Σ%) + ΣFlat) × (1 + FinalMultiplier%)
```

Building contributions land in these buckets:
- **Building Training aptitude** → added to flat aptitude sources (+1 aptitude per Training building level) → feeds into `Base`
- **Building Service Level** → added to ΣFlat (aggregated across all matching-typing buildings) → adds after the % multiplication
- **Building Appearance %** `[RETIRED EVENT]` → if present on older accounts, it added to the Σ% pool

Because aptitude sits upstream of the massive Σ% multiplier, Building Training aptitude is disproportionately valuable on well-developed fellows with high Σ% totals.

## Training & Service Level Tips

- **Don't pour all your gold into one building.** Cost is exponential between levels, so parallel investment across several matching-typing buildings beats serial push on one. Each building's first-few-levels are cheap; any building's 40th-level is expensive.
- **Training presses within a single level are flat-cost**, so once you decide to push a Training level, commit to the full 20 presses if you haven't rolled up. Stopping mid-level wastes no aptitude (you still get +1 at level-up) but it does leave the gold you already spent unrewarded until you finish the level.
- **The cost escalation pattern applies to Service Level too** — more flat power already bought = more expensive next tap. Same exponential curve as Hire Cards/Gold and Date Points.
- **Whether to push Training first or Service Level first is not a strict priority** — it may just be a chronological thing (you tend to do them in whichever order gold allows). Spread investment across buildings, and across tracks within a building, as gold permits.

## Gaps in This Doc

- Exact Gold-cost curves per Training level (the exponential growth rate between levels) are not in our verified data
- Per-building typing assignments are not enumerated here (depends on your village layout)
- Whether Training caps at some maximum level is unknown
- Study Notes mechanics (how to earn them, how many you need per fellow to max the earnings % boost) are not documented in this doc
- If you have data on any of the above, contact **Su**
