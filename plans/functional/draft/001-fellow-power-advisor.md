# Plan: Convert to Isekai Slow Life Fellow Power Advisor

## Overview

Transform the Policy Corpus RAG chatbot into an **Isekai: Slow Life Fellow Power Advisor** targeting advanced players (guild level 45+). The bot will specialize in Fellow Power optimization across six core systems: Fish, Costume Levels, Skill Pearls, Fellow Level, Awakening, and Stella.

## Target Audience

- Advanced players (level 45+)
- Guild members who already understand basics
- Players optimizing Fellow Power score, not learning what buildings are
- Focus on multiplicative stacking, resource efficiency, and endgame scaling

## Phase 1: Foundation (This Session)

### 1.1 Remove Git History
- Delete `.git` directory inside `quanticaiengineering/`
- Initialize fresh git repo at the project root (`isekaichattybot/`)
- Clean `.gitignore` for new project scope

### 1.2 Rebrand the Application
- Rename references from "Policy Corpus RAG" / "Quantic AI Engineering" to "Isekai Fellow Power Advisor"
- Update `config.py`: system prompt, query prompt, app name
- Update `server.py`: routes, titles, descriptions
- Update `web_app.py`: UI references
- Update HTML templates and static assets
- Update `render.yaml` and deployment config

### 1.3 Replace Policy Documents with Game Knowledge Base
Delete `policies/` content and replace with structured Isekai Slow Life knowledge documents:

```
knowledge/
├── fellow-power-overview.md      # How power is calculated (formula, addends vs multipliers)
├── fellow-leveling.md            # Levels, limit breaks, EXP stones, crystal costs
├── fellow-awakening.md           # Stars, acquaint stones, awakening skills, priority
├── skill-pearls.md               # Talent tiers, aptitude scaling, optimization
├── costumes.md                   # Costume levels, aptitude bonuses, acquisition
├── stella.md                     # Character-specific boosts, category-wide buffs
├── fishing.md                    # Fish skills, fish tank, combinations, sea fishing
├── fellow-tier-list.md           # Tier rankings, base aptitude, meta strategies
├── artifacts.md                  # Reforging, magic ore, type matching
├── family-blessings.md           # Fellow blessing vs advanced blessing, intimacy
├── advanced-strategies.md        # Multiplier stacking, single-carry meta, resource priority
└── resource-guide.md             # Where to get acquaint stones, skill pearls, crystals
```

### 1.4 Update System Prompt for Advanced Players
The AI should:
- Assume the user knows basics (buildings, employee hiring, etc.)
- Give specific numbers, formulas, and breakpoints
- Recommend optimal resource allocation
- Compare strategies with math (e.g., "3 skill pearls on Supreme Talent = +3 aptitude, vs 3 on Ordinary = +3 aptitude but lower cap")
- Reference specific fellows by name and aptitude values
- Advise on multiplier stacking strategies

## Phase 2: Performance Optimization (Later)

### 2.1 Chunking Strategy
- Tune chunk size for game guide content (shorter, more precise chunks)
- Consider semantic chunking by game system (each section = one chunk)
- Evaluate chunk overlap for cross-system questions

### 2.2 Retrieval Tuning
- Optimize TOP_K for game knowledge (likely lower K since domain is narrow)
- Tune similarity threshold for game-specific vocabulary
- Consider metadata filtering by game system

### 2.3 Embedding Quality
- Evaluate if `all-MiniLM-L6-v2` handles gaming terminology well
- Consider fine-tuning or switching to a model better for game jargon

## Phase 3: Discord Integration (Later)
- Add Discord bot interface
- Ingest guild guides (internal, outdated — flag staleness)
- Support slash commands for quick lookups
- Per-guild configuration

## Success Criteria

- Bot accurately answers questions about Fellow Power optimization
- Responses include specific numbers (aptitude values, crystal costs, power multipliers)
- Bot understands system interactions (e.g., "How does Stella affect my awakened Neptune?")
- Advanced players find advice actionable, not beginner-level
