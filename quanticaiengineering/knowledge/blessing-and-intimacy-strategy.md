# Blessing & Intimacy Strategy — Advanced Guide

> See `family-blessings.md` for the full mechanical reference on how Blessing Points, Intimacy, Bond, and the Family Earning Skills system work. This doc is the strategy layer on top of those mechanics.

## Two Parallel Stats, Two Different Payoffs

**Intimacy** and **Blessing Power** are separate stats that accumulate on the same family member. They drive different systems:

| Stat | Primary Payoff |
|------|----------------|
| **Intimacy** | Unlocks **Family Earning Skills** (building earning multipliers) up to 5,000 intimacy, then **Latency** bonuses past 5,000 |
| **Blessing Power** | Drives **Blessing Points earned per date** via the verified formula `BP = Blessing Power × 4.52` (non-CG) or `× 5.42` (CG) |
| **Bond** (both combined) | Determines **student rarity** — higher Bond = higher-rarity student that generates more gold |

**Family rarity does not affect the intimacy or BP stats themselves** — a maxed N family's intimacy gives the same per-point value as a maxed UR family's intimacy. What differs is the Family Stella tier (N/R/SR/SSR/UR) which gives additional bonuses on top of the raw stat accumulation.

---

## Intimacy Strategy

### Stage 1: Push All Families to 5,000 Intimacy (Priority)

Family Earning Skills unlock progressively as intimacy climbs toward 5,000. Each family has **6 skill slots** — one for each of the 5 typings (Brave / Diligent / Unfettered / Inspiring / Informed) plus an "all buildings" booster — and each slot unlocks in **three waves** as intimacy grows, for a total of **18 unlock milestones per family** between 0 and 5,000.

**Practical approach:** Spread intimacy gifts across all your families to bring them all to 5,000 together, rather than maxing one family first. The Earning Skills unlocks are wave-based, so having several families at Wave 2 beats one family at Wave 3 and four families at Wave 0.

### Stage 2: Push Past 5,000 For Latency

Past 5,000 intimacy, new Family Earning Skills stop unlocking and you instead earn **Latency**, a separate bonus that continues increasing your building earnings. Latency scales indefinitely with every additional point of intimacy past 5k, so it's worth pushing high — but only after all your families are at 5k.

**Prioritization past 5k:** Push the family associated with your highest-earning building typing first. If your main earning typing is Informed (Museum etc.), max Latency on Informed-aligned families before the others.

### Stage 3: Bond Thresholds (Requires Both Intimacy AND Blessing Power)

Beyond the Intimacy-only benefits, the **Bond** stat is a combined threshold that requires **both** Intimacy and Blessing Power to reach the same value:

| Bond Tier | Requirement (Both Stats) | Effect |
|-----------|-------------------------|--------|
| Tier 1 | 2,000 each | Higher-rarity student slot 1 |
| Tier 2 | 4,000 each | Higher-rarity student slot 2 |
| Tier 3 | 8,000 each | Higher-rarity student slot 3 |
| Tier 4 | 20,000 each | Higher-rarity student slot 4 |
| Tier 5 | 50,000 each | Top-rarity student slot |

**The "each" is load-bearing.** A family with 50,000 Blessing Power but only 4,000 Intimacy is stuck at Tier 2 for Bond — you cannot substitute one stat for the other. To reach the high Bond tiers, both must advance together.

Higher Bond → higher-rarity student → more gold per tick from that student. This is the main secondary payoff for intimacy beyond the Earning Skills system.

---

## Blessing Power Strategy

### Per-Date Value, Not Daily Totals

**Blessing Points are earned per date on the specific family you date.** There is no shared pool — if you don't date family X, family X gets zero BP regardless of how much Blessing Power they have.

Per-date income scales linearly with Blessing Power:
- **Non-CG date:** BP = Blessing Power × 4.52
- **CG date:** BP = Blessing Power × 5.42 (random +20% bonus, can't be controlled)

This means each +1 Blessing Power permanently adds +4.52 BP per date on that specific family — but only to dates that actually land on that family.

### Targeted vs Random Dates

You can only choose the date recipient on **Plane Tickets** and **Crystal Travel** (targeted date systems). **Succubus Tonic dates are random** — RNG picks the family, and you may or may not land on your high-BP family.

**Strategic implication:** If you want to concentrate BP on one family, you must target them with Plane Tickets and Crystal Travel. Random dates contribute BP to whoever RNG picks, which is fine for background roster BP farming but not for concentrated leveling.

### Finding Your Investment Targets

1. Identify your main carry's typing
2. Open `families-roster.md` and list every family that blesses your main carry (or any fellow you want to power up)
3. Look for **UR families first** (they give the biggest per-level Family Stella bonuses), then **SSR families that bless multiple fellows of your main typing**
4. These are your priority blessing targets — push their Blessing Power high, and burn targeted dates on them

### Blessing Power Investment Order

| Stage | Target | Applies To |
|-------|--------|------------|
| 1 | Push priority families to 20,000 Blessing Power | All UR and multi-fellow SSR families that bless your main carry |
| 2 | Push your single best family to 50,000 | The family with the most overlap on your roster and/or your main carry |
| 3 | Push that one family to 100,000+ | Only if you've already saturated the families at stage 1 |

**Do not waste Blessing Power gifts on:**
- Families that don't bless your main typing at all
- Families that only bless fellows you don't use
- Families where you can't target dates (i.e., families you never touch with Plane Tickets or Crystal Travel)

### Compounding With Family Stella

Maxing a family's **Family Stella** adds additional Blessing Power and Intimacy on top of the gift-based accumulation:

- **UR Family Stella** at Lv 1–10 cumulatively adds **+9,200 Blessing Power + +9,200 Intimacy** to the family (see `family-stella.md` for the per-level table)
- **SSR Family Stella** at Lv 1–10 cumulatively adds **+1,950 each**

So maxing a UR Family Stella gives that family +9,200 Blessing Power on top of whatever you've gifted them. At the BP = BP × 4.52 conversion rate, that's **+41,584 Blessing Points per targeted date** from the Family Stella alone — before you've gifted a single Flower Necklace or Jewel Necklace.

**The compounding loop:** Family Stella → more Blessing Power and Intimacy → higher BP per date AND higher Bond tier → more Blessing Points to level Fellow Blessing / Advanced Blessing / Special Blessing → more Fellow Power → more resources → more Family Stella progression.

---

## The Combined Strategy

### Parallel Tracks (Run Them All)

1. **Intimacy track** — Spread gifts to push all families toward 5,000 intimacy (Family Earning Skills), then past 5,000 for Latency. Intimacy is for **gold income**.
2. **Blessing Power track** — Concentrate Blessing Power gifts on families that bless your main carry. Blessing Power is for **Fellow Power** (via Fellow Blessing, Advanced Blessing, and the Bond threshold unlocks).
3. **Family Stella track** — Max Family Stella on the same UR and SSR families that bless your main carry. Each maxed Stella adds substantial Intimacy AND Blessing Power directly, compounding both tracks.
4. **Targeted dating track** — Burn Plane Tickets and Crystal Travel on the one family you're concentrating Blessing Power on. This is the only way to guarantee your Blessing Power investment converts into actual Blessing Points.
5. **Random dating track** — Use Succubus Tonic dates as background BP farming across your roster. RNG handles distribution.

### Why Intimacy Is Often Under-Prioritized

Players sometimes skip intimacy because Blessing Power gives flashier "fellow power" numbers. This is a mistake:

- Intimacy-unlocked Family Earning Skills multiply your **gold income across your entire village** — gold which then powers Building Service Level taps, Building Training, employee hiring, building upgrades, blueprint spending, and so on
- Latency past 5k scales indefinitely
- Bond thresholds gated by intimacy determine student rarity (which also scales gold income)

**In short: Intimacy is a gold-income lever, Blessing Power is a Fellow-Power lever, and both compound into each other because the gold from intimacy pays for every other progression track including fellow leveling and building investment.** Push both in parallel.

---

## Quick Math Example (Per-Date Values)

These are per-date numbers, not daily totals. Your daily totals depend on how many of your daily dates actually land on each family (targeted via Plane Tickets / Crystal Travel, or random via Succubus Tonic).

### Family at 20,000 Blessing Power
- **Non-CG date:** 20,000 × 4.52 = **90,400 BP per date**
- **CG date:** 20,000 × 5.42 = **108,400 BP per date**

### Family at 100,000 Blessing Power
- **Non-CG date:** 452,000 BP per date
- **CG date:** 542,000 BP per date (5x income vs the 20k family per-date)

### Family at 9,200 Blessing Power (from just maxing UR Family Stella, no gifts)
- **Non-CG date:** 9,200 × 4.52 = **41,584 BP per date**

This shows why the Family Stella compounds so hard — maxing a UR Family Stella alone gives you ~42K BP per targeted date on that family before you spend a single Blessing Power gift.

**Daily totals = per-date value × number of dates landing on that family.** For random Succubus Tonic dates, that number is RNG-dependent. For targeted Plane Ticket / Crystal Travel dates, you control it and can funnel every daily date onto your priority family.

---

## Common Mistakes

1. **"I'll just push Blessing Power on one family to 100k and ignore the rest."** — OK only if you're also burning Plane Tickets on that family daily. Otherwise RNG random dates spread your attention across families and the non-priority ones fall behind.
2. **"Intimacy is slow, I'll focus on Blessing Power first."** — Wrong. Intimacy unlocks Family Earning Skills which massively multiply your gold income. Skipping intimacy is skipping the gold that pays for every other system.
3. **"Higher family rarity means better intimacy per point."** — No. Rarity affects Family Stella tier, not the raw intimacy accumulation. A N family's intimacy point is worth the same as a UR family's intimacy point for the Family Earning Skills / Latency / Bond systems.
4. **"I should focus on families with the highest rarity."** — Only true for **Family Stella** progression. For raw intimacy and blessing power push, the family that **blesses your main carry the most** is the correct target regardless of rarity.
