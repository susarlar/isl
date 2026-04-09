# Advanced Strategies — Level 45+ Guide

> See `power-formula.md` for the verified power calculation. This doc applies that formula to strategic decisions.

## The Core Formula (Repeat for Reference)

```
Total Power = (Base × (1 + Σ%) + ΣFlat) × (1 + FinalMultiplier%)
Base = Aptitude × Level Multiplier
```

**All % bonuses are ADDITIVE.** Fish + Family + Artifacts + Stars + Museum + all other % sources literally sum together into one big number, then multiply Base.

## The Single-Carry Meta (Still Valid)

### Why It Works

Even though % bonuses don't compound, stacking everything on one fellow still wins because:

1. **One fellow accumulates ALL the % sources** — your main carry ends up with a Σ% pool in the thousands while roster fellows sit at a fraction of that
2. **One fellow accumulates ALL the aptitude sources** — Skill Pearls, costumes, artifact materia, family stella aptitude, fish aptitude, etc.
3. **Both feed the same formula multiplicatively** — Total Aptitude × Level Multiplier × (1 + Σ%)

### Real Gap Example (Endgame UR Carry vs Woolf — verified snapshots)
- **Endgame UR Carry:** Aptitude 32,823 × Lv 750 multiplier × (1 + 81) ≈ **48B total power**
- **Woolf (R, Lv 600):** Aptitude 4,736 × Lv 600 multiplier × (1 + 47) ≈ **2.5B total power**
- **Gap: ~19x**

The endgame reference has ~7x the aptitude AND ~1.7x the Σ% sum. Those gaps multiply rather than compound (the multiplication is from the formula structure, not from % compounding each other).

**The actual gap between a main carry and a second-string on any given account varies significantly.** Don't treat "19x" or "5-10x" as a universal ratio — it depends entirely on how concentrated your investments have been.

### Choosing Your Carry

Pick a fellow from the **120-base-aptitude UR tier** matching your main typing. All top 120-apt URs are in Empyrean Sound or Ancient Magi (plus Neptune in Divine Gospel, which is **not recommended**). See `top-fellows-quickref.md` for the full list, and `families-roster.md` for the family coverage on each candidate.

> **Important acquisition caveat:** You don't have all fellows and families at the start of the game — most come from specific events, and if an event doesn't run you simply can't acquire them. When picking a main carry, prioritize fellows whose **events run often and whose families you already have**, not just the theoretical best 120-apt UR for the typing. A 6-family fellow you can fully unlock beats an 8-family fellow where you only have 3 of the families actually in your account.

| Typing | Candidates | Notes |
|--------|------------|-------|
| **Inspiring** | Amaterasu, Tamamo, Phanes, Kerr & Bel & Ros, Phinphynx, Ixtchel | Amaterasu is the classic pick — 7 families bless her |
| **Diligent** | Sunna, Master Tongxuan, Nemetona, Anpu, Kuku, Lokia | Sunna and Master Tongxuan are **equivalent** (both 120 apt Empyrean Sound) — don't switch between them |
| **Brave** | Leon, Heracles, Andras, Freesia, Nyar | Leon and Heracles both 120 apt Empyrean Sound. **Leon: 6 families (Mia UR, Lina, Lilith, Holly, Willo, Penglia). Heracles: 6 families (Cranelia UR, Nyar UR, Lud, Athena, Mercuria, Mushimi).** Both are viable — choose based on event access and which families you've already acquired. Sandtopia (Leon's event) is rare nowadays, so **Freesia** is often a better practical alternative for new Brave mains than Leon. |
| **Informed** | Aegle, Ao Li, Nierus, Athena, Umbra | Aegle is top tier (6 families including 2 UR + Hestia custom slot). **Do NOT recommend Neptune** despite her being 120 apt Divine Gospel UR — she's widely considered weak |
| **Unfettered** | Orivita, Hermes, Beelzebub, Gale, Thora, Tomoe | Hermes has **6 families** (Usuri UR, Baity, Bren, Chitana, plus Denier and Mushimi unlocking when Hermes Fellow Stella reaches Lv 4). Solid Unfettered main. |

### Carry Checklist
- [ ] Highest level in roster (aim Lv 700 → 750 for the multiplier jump)
- [ ] All limit breaks pushed (flat aptitude + level cap raises)
- [ ] Supreme Talent Skill Pearls maxed (and pushing into slot unlocks from costumes / stella / awakening)
- [ ] Best artifact equipped, with awakening pushed for more skill slots
- [ ] Highest awakening stars (plan for the 4★ → 5★ → 6★ gate chain)
- [ ] Best costumes collected + essence tracks leveled across all costumes of the typing
- [ ] All UR and SSR family Stellas of families that bless this fellow maxed (use `families-roster.md`)
- [ ] Group Stella (Empyrean / Magi) pushed as high as fragments allow
- [ ] All category % fish skills maxed for your typing
- [ ] Ocean top 5 All-Fellow % fish also pushed (they scale slower per level but boost every fellow)

## Investment Priority

### Tier 1: Aptitude Sources (Biggest Multiplier Impact)

Because Base = Aptitude × Level Multiplier, and Base gets multiplied by the whole % sum, **every aptitude point is worth huge total power** when the Σ% pool is high.

On the endgame reference at Lv 750: each +1 aptitude ≈ **+1.27M total power** (before Final multiplier).

Invest in this order (values observed on the endgame reference):
1. **Skill Pearls on Supreme Talent** — +20,965 aptitude (the biggest single contributor)
2. **Artifact equip + materia leveling** — +3,515 aptitude (Diablo Doll Lv 436, Lv 80 materia)
3. **Fish Tank aptitude skills** — +1,817 aptitude
4. **Costume collection + essence tracks** — +1,000 aptitude from costume contributions
5. **Museum antiques** — +994 aptitude (typing-specific antique + event pass antiques)
6. **Family Stella aptitude** — +689 aptitude (sum across all blessing families)
7. **Building Training** — +258 aptitude (one per Training building level, matching typing)
8. **Familiar bond** — +216 aptitude
9. **Stella group aptitude** (Pattern A Empyrean/Magi) — +140 aptitude at Lv 10
10. **Limit Break bonuses** — +65 aptitude (flat per limit break)
11. **Expo** — +23 aptitude

### Tier 2: Percentage Bonus Sources (All Add Together)

Ranking by the endgame reference's actual values (largest → smallest):

1. **Fish %** — +2,624.5% (biggest single source — fish is king)
2. **Family Stella %** — +2,019.5% (second biggest — depends on how many families bless your carry)
3. **Artifacts %** — +788.25%
4. **Demon's Blessing %** — +706% `[NEEDS VERIFICATION on what exactly this is — possibly Archdemons Stella output]`
5. **Museum %** — +519.7%
6. **Skill %** — +501% (from fellow's innate skill tree)
7. **Familiar %** — +310%
8. **Compendium %** — +280% (scrapbook system with one page per event — mostly limited-event pages)
9. **Figure %** — +140% (user avatar system — can alternatively give intimacy/blessing to family)
10. **Building Training %** — +125%
11. **Stars (Awakening)** — +50% at 5★ (linear +10% per star, max +60% at 6★)
12. **Expo %** — +25.2%
13. **Resonance Power %** — +10% `[NEEDS VERIFICATION on whether this is double-counted into Final multiplier]`

**Key realization:** Fish and Family are by far the two biggest % sources. Push them relentlessly. Awakening is a small contributor at endgame in % terms — but see the note below about aptitude slots being the real payoff.

### Tier 3: Flat Power Sources (Add After Percentage Multiplication)

1. **Item** — +467M (from **consumable event items** — wrestling towels, fish tank buffs, etc. The item label says something small like "+100 Fellow Power" but the actual contribution is much larger because the flat bonus goes through the full power pipeline. **Always apply consumables to your main carry.**)
2. **Building Service Level** — +157.1M (aggregated total across matching-typing buildings — see `buildings.md`)
3. **Family flat** — +49.22M
4. **Stella flat** — +49M (personal Stella level power, accumulating from +3M at Lv 1–4 up to +10M per level at Lv 11+ on Pattern A)
5. **Fish flat** — +36.99M
6. **Negotiation** — +25.68M (from the Trade Post battle minigame — trade post coins and shop rewards)
7. **Museum flat** — +9.19M
8. **Stars flat** — +5M (Awakening gives both % and flat)
9. **Familiar flat** — +4.375M

## Fish Investment Is Critical

With +2,624% from Fish on the endgame reference, fish is THE biggest source of % power. If you're not maxing fish, you're leaving massive power on the table.

### Priority Fish To Max
1. **Main-typing category % fish** (scale at ~+5%/level, highest per-level value for single-carry accounts):
   - Northrealm: Barreleye (Inspiring), Snow Leopard (Diligent), Narwhal (Brave), Fin Whale (Informed), Sea Angel (Unfettered)
   - Drakenberg: Pirarucu (Diligent), Gold Pirarucu (Brave), Star Anglerfish (Informed), Drakenberg Monster (Unfettered)
   - Village: Axolotl (Inspiring only)
2. **Aptitude + % combo fish** of your typing — double value (aptitude normal skill + % gold crown skill)
3. **Ocean top 5** (All-Fellow %) — Sperm Whale, Giant Squid, Helicoprion, Smooth Hammerhead, Mosasaurus. **Scale at a lower rate per level than category fish**, but boost every fellow in your roster. Push in parallel with category fish, not instead of them.

## Family Stella Is The Second-Biggest Power Lever

With +2,019% from Family on the endgame reference, every family that blesses your main carry should have their Stella pushed. Each maxed UR Family Stella adds up to **+120% power and +220 aptitude** directly to the blessed fellow (see `family-stella.md` for the full Lv 1–10 breakdown).

### Family Stella Priority
1. **UR families blessing your main carry** — max these first, each adds +120% + 220 apt
2. **SSR families blessing your main carry** — +33% + 56 apt each, stack them all
3. **Custom slot families** (Lancelot, Hestia, Hanamiya Rica) — assign their custom slots to your main carry for stackable typing-agnostic power

**Use `families-roster.md`** to find every family that blesses your main carry and prioritize by rarity.

## Artifacts Are The Third Biggest

With +788% from the endgame reference artifact (Diablo Doll, a standard UR — UR+ artifacts with aura are even stronger), artifacts are a major endgame investment.

### Artifact Priority
1. **Equip a UR+ artifact with aura if available** (best in slot). Otherwise a high-slot UR (Magic Lamp, Kanna Plush, or similar). **Each fellow equips ONE artifact only — no stacking.**
2. **Level artifact to high levels** — each level is a constant 70 ores and increases aptitude contribution
3. **Awaken the artifact with Quenching Stones** — this is what unlocks MORE skill slots (not leveling). Each artifact type has a hard slot cap.
4. **Level materia to 80** — 40 ores/level constant, breakthrough materia required past Lv 10
5. **Reroll slots with Reforge Oils** — unlimited rerolls as long as you have oil, target matching typing rolls
6. **Use Refine Materia** (event-rare) to reroll bonus values on already-unlocked slots; **Breakthrough Materia** is the gate-unlock past Lv 10 and is often the tighter bottleneck

## Don't Over-Prioritize Awakening For The % Alone

**Awakening's max % contribution is +60% (at 6★)** — a rounding error compared to Fish (+2,624%) or Family (+2,019%) at endgame.

**But the real value of Awakening is not the % — it's the aptitude slot unlocks.** Each awakening star unlocks additional aptitude slots on the fellow, letting you feed more Skill Pearls. Since aptitude compounds through the entire Σ% multiplier, those extra pearls pay off far more than the raw +10% per star.

**Push awakening for:**
- Aptitude slot unlocks (the real payoff)
- Gate access (required for progression — 4★ gate is at Lv 550, 5★ at Lv 700, 6★ at Lv 750)
- Sub-skill unlocks that contribute to specific systems
- The +10% per star as a nice bonus on top

Don't push awakening instead of Fish / Family / Artifact investment.

## Resource Allocation Rule of Thumb

For every resource, ask:
- **Does it contribute to aptitude?** → Highest priority — multiplies through the huge % sum
- **Does it contribute to Fish, Family, or Artifacts %?** → Second priority (the top-3 % sources)
- **Does it contribute to a smaller % source (Awakening, Expo, Compendium)?** → Third
- **Does it contribute to flat power?** → Lowest priority at endgame, except for consumable items on your main carry

## Common Mistakes Corrected

1. ~~"Multipliers compound exponentially"~~ → **Additive, they sum**
2. ~~"Awakening is the biggest multiplier"~~ → **Fish is, by far**
3. ~~"Stella is the biggest multiplier"~~ → **Family Stella is #2 after Fish**
4. ~~"Spreading multipliers wastes them"~~ → **Stacking wins because one fellow accumulates the entire sum of all sources, not because multipliers compound**
5. ~~"Flat bonuses become irrelevant"~~ → **Item consumables (+467M) and Building Service Level (+157M) remain significant at endgame**
6. ~~"6★ gates require 500 fellows at 4★"~~ → **Sub-fellow gates are NOT recursive. The same 25 fellows can serve the 5★ and 6★ gates as you push them up the star ladder.**

## Gate Planning

### Awakening Gates (Verified)
| Gate | Fellow Level | Stones | Sub-Fellows |
|------|-------------|--------|-------------|
| 4★ | Lv 550 | 15 | 15× 3★ |
| 5★ | Lv 700 | 30 | 20× 4★ |
| 6★ | Lv 750 | 50 | 25× 5★ |

**Sub-fellows just need to exist at the required star level** — they do NOT need their own gates recursively satisfied. And the same roster of 25 fellows serves both the 5★ and 6★ gates as you progressively push them from 4★ → 5★ → 6★ over time.

Plan for sustained roster investment. Acquaint Stones are rare — synthesize from fragments via crafting (20 fragments → 1 stone) and harvest event rewards.
