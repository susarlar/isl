# Skill Pearls — Advanced Guide

> **Heads up:** "Skill Pearls" here means the gold-tier Skill Pearls used on fellow Talent skills. The game also has **White Pearls** (bait production speed) and **Black Pearls** (account-wide % boosts) — those are completely different currencies. See `pearls.md` for the full three-pearl reference.

## What Skill Pearls Do

Skill Pearls upgrade **Talent-based Aptitude skills** on individual fellows, directly increasing a fellow's Aptitude stat. Since Base Power = Aptitude × Level Multiplier, every point of Aptitude scales with your level.

**Skill Pearls are fellow-only.** You cannot spend them on buildings, artifacts, fish, or any other system. Buildings are Gold-gated (see `buildings.md`).

## Three Talent Tiers

| Talent Tier          | Aptitude per Level | Skill Pearl Cost/Level | Max Level | Max Aptitude Gain |
|----------------------|-------------------|------------------------|-----------|-------------------|
| **Supreme Talent**   | +3                | 3 Skill Pearls         | 300       | 900 aptitude      |
| **Outstanding Talent** | +2              | 2 Skill Pearls         | 300       | 600 aptitude      |
| **Ordinary Talent**  | +1                | 1 Skill Pearl          | 300       | 300 aptitude      |

## Efficiency Analysis

### Per-Pearl Return (Same at All Tiers)
- 1 Skill Pearl always gives +1 Aptitude regardless of tier
- 3 pearls on Supreme = +3 aptitude (1 level)
- 3 pearls on Ordinary = +3 aptitude (3 levels)
- **Short-term efficiency is identical**

### Why Tier Matters: Caps
- **Supreme:** Can reach 900 aptitude from talents alone
- **Outstanding:** Caps at 600 aptitude
- **Ordinary:** Caps at 300 aptitude

**For advanced players (45+):** You WILL hit Ordinary caps first. Always invest in Supreme Talent first if you're approaching caps on lower tiers.

### For F2P vs Spenders
- **F2P:** Caps take very long to reach. Spread pearls where needed for immediate power.
- **Spenders:** Invest heavily in Supreme Talent — the 900 cap is your ceiling, and every point multiplies with level, awakening, artifacts, and Stella.

## Other Aptitude Skill Categories

### Expertise Skills (Book-Based)
5 types matching fellow categories: Inspiring, Diligent, Brave, Informed, Unfettered

| Detail | Value |
|--------|-------|
| Max Level | 300 |
| Increase | +1 or +2 per level |
| Cost | Books (30,000 books for full mastery per character) |

### Trading Skills (Bazaar Scroll-Based)
5 types: Cuisine, Handicraft, Weaponry, Grimoire, Souvenir

| Detail | Value |
|--------|-------|
| Max Level | 200 |
| Cost | 15,000–42,000 Bazaar Scrolls per level range |

## How to Obtain Skill Pearls

| Source | Amount | Frequency |
|--------|--------|-----------|
| Event point shops | 1-5 per event (5,000 points each) | Per event cycle |
| Fishing event rankings | Up to 15 (Rank 1) | Per fishing event |
| Crafting | Variable | Ongoing |
| Battle Pass | Variable | Per season |
| Ranking rewards | Variable | Competitive events |

## Skill Pearl Investment Strategy for Level 45+ Players

### Priority 1: Main Carry Fellow
1. Max Supreme Talent first (highest cap, best long-term scaling)
2. Then Outstanding Talent
3. Ordinary Talent last (lowest cap, will max soonest anyway)

### Priority 2: Building Operators
- Invest in fellows assigned to your highest-earning buildings
- Aptitude increases both Fellow Power AND operation efficiency

### Priority 3: Roster for Awakening Gates
- Getting 15 fellows to 3★ for the 4★ gate requires them to be reasonably strong
- Some Skill Pearl investment in gate fellows is necessary

## Power Impact Example

Hypothetical 120-base-aptitude UR fellow at Level 500 (illustrative, not a specific fellow):
- Base: 120 × 7,590 = **910,800**
- +100 aptitude from Skill Pearls: 220 × 7,590 = **1,669,800** (+83% power!)
- +300 aptitude (all talent caps maxed): 420 × 7,590 = **3,187,800** (+250% over base!)

> The Lv 500 multiplier of 7,590/apt is flagged as `[NEEDS VERIFICATION]` in `power-formula.md` — only the Lv 750 multiplier (~15,500/apt) is verified from real snapshots.

**Real-data ceiling:** On the endgame UR Empyrean Sound reference carry (Lv 750, 5★), the observed Skill Pearl aptitude contribution is **+20,965** — far beyond the base 900/600/300 talent caps, because higher Stella levels, awakenings, and costume/artifact unlocks all raise the skill pearl aptitude ceiling beyond the initial Talent caps. The 900 cap on Supreme Talent is the **starting** cap — progression in other systems unlocks additional pearl slots that let you keep feeding skill pearls long after Supreme Talent is "maxed."

And remember — this base power then gets multiplied by awakening %, artifacts, Advanced Blessing, Stella, Fish, Family, and every other % source. Aptitude is the foundation that everything else scales from.

## The Full Aptitude Slot System (Per Fellow)

Skill Pearls are **only one of several resources** that feed aptitude slots on a fellow. Each SSR or UR fellow has a stack of distinct aptitude slots, each fed by a different resource and each with its own level cap:

### SSR Fellow — Aptitude Slots
1. **Supreme Talent (aptitude slot 1)** — Level cap 300, costs **3 Skill Pearls per level**, gives **+3 aptitude per level** → max +900 aptitude
2. **Aptitude Slot 2** — Level cap 300, costs **2 Skill Pearls per level**, gives **+2 aptitude per level** → max +600 aptitude
3. **Insight 1** — Fed with **Books**. Books are earned from events and as a **one-time reward per graduated student** at the School (each graduation produces books). **100 books = +1 aptitude**. Cap **330**, gives **+660 aptitude at cap**, **no diminishing returns**.
4. **Limit Break slots** — **One slot unlocked per awakened star**. Each slot is fed with **1 Skill Pearl per level**, giving **+1 aptitude per level**. So at 6★ you have 6 Limit Break slots stacked on top of each other. Note: R/SR/N fellows cannot be awakened, so they have **no Limit Break slots at all**.
5. **Fellow-specific Special aptitude slot** — A slot that exists on the fellow from the moment you acquire them. The slot has a **different in-game name for each fellow** (it's tied to the fellow's theme), but mechanically it's the same type of slot: feed **3 Skill Pearls per level**, gives **+3 aptitude per level**.
6. **Proficiency slot** — Fed with **Bazaar Scrolls**. `[NEEDS VERIFICATION]` exact cost growth — there are diminishing returns in some form but the precise growth curve isn't documented.
7. **Alraune's Essence slot** — Fed with **Alraune's Essence** bought from **Farm Points**. The first few Alraune's Essences come at a discount; past that, the cost escalates. **The discount resets daily**, so buying a few Alraune's Essences every day is cheaper than buying many in one session.

### UR Fellow — Additional Slots
Everything SSR has, PLUS:
- **Insight 2** — A second Insight slot with its own Book feed (fills in parallel with Insight 1)
- **Costume-based aptitude slot** — Fellow costumes (3★+) unlock dedicated slots on the wearing fellow; see `costumes.md` for per-rarity feed rules

**Note:** URs don't get a separate "bonus awakening slot" on top of the per-star Limit Break slots — those are the same thing. What distinguishes URs from SSRs in terms of aptitude slots is having the **Insight 2 track** and (for invested fellows) the additional costume-sourced slots.

### R / SR / N Fellows
**Cannot be awakened.** This means:
- No Limit Break slots
- No awakening bonus slot
- Still have Talent, Insight, Proficiency, etc. but their ceiling is much lower because the awakening-gated slots are unavailable

This is one of the core reasons R/SR/N fellows can never compete with invested SSR/UR carries at endgame — the number of aptitude slots available to feed is structurally smaller.

### Typing-Specific vs Type-Agnostic Resources

| Resource | Type-Agnostic or Per-Typing? |
|----------|------------------------------|
| **Skill Pearls** (Supreme/Outstanding/Ordinary Talent, Slot 2, Limit Break, Special) | **Type-agnostic** — feed any fellow regardless of typing |
| **Books** (Insight 1 / Insight 2) | **Per typing** — Inspiring books only work on Inspiring fellows, etc. |
| **Bazaar Scrolls** (Proficiency) | **Per typing** — each typing has its own scroll currency |
| **Alraune's Essence** (Farm Points) | **Per typing** — each typing has its own essence |

**Strategic implication:** Because books, scrolls, and alraune essences are per-typing, they are **naturally concentrated on whichever typing you main** — you can't accidentally spread them across multiple typings. Skill Pearls are the one resource you actively need to budget, because any pearl can go anywhere.

## Real-Data Ceiling

On the endgame UR Empyrean Sound Inspiring reference carry (Lv 750, 5★), the observed Skill Pearl aptitude contribution is **+20,965** — far above the base Supreme Talent cap of 900 because of the many additional slots (Slot 2, Limit Break slots from awakening, Special, Proficiency, Alraune, Costume slots, etc.). The +20,965 is not an outlier — it's what a well-developed main carry should be aiming for, and higher is possible with deeper investment.

And remember — this base power then gets multiplied by awakening %, artifacts, Advanced Blessing, Stella, Fish, Family, and every other % source. Aptitude is the foundation that everything else scales from.
