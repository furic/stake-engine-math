# 🏰 Tower Defense Game

## 🎮 Game Overview

**Defend Your Realm in this Epic 5x5 Cluster-Pay Medieval Fantasy Adventure!**

Welcome to a thrilling tower defense slot experience where strategy meets spectacular wins! In this immersive 2.5D medieval fantasy battlefield, hordes of monsters surround your homeland, and only your tactical prowess can save the day. Build mighty towers, forge powerful clusters, and defend your fortress against the endless siege!

## 🎯 Core Mechanics

**Battle Grid:** 5-reel, 5-row fortress layout with cluster-pay mechanics (3+ connected symbols)
- **No tumbling or cascading** - pure strategic positioning matters
- **Cluster-based payouts** grouped by army size: 5-9 formations, 10-14 battalions, 15+ legendary forces
- **Resource-to-Tower Upgrade System:** Gather 5 resource lands to construct mighty defensive towers

## 🛡️ Symbol Arsenal

**🌿 5 Resource Lands (L1-L5)** - Essential materials for tower construction:
- **💎 Crystal (L1)** - Rare gems that power ultimate defenses
- **⚒️ Iron (L2)** - Metallic strength for advanced weaponry
- **🌊 Lake (L3)** - Mystical waters that enhance magical properties
- **🪨 Stone (L4)** - Sturdy building blocks for solid fortifications
- **🪵 Wood (L5)** - Foundation material for basic defenses

**🏗️ Tower Structures** - Elite defensive installations:
- **✨ Magic Tower (M1/H1)** - Arcane energy projection systems
- **🔥 Cannon Tower (M2/H2)** - Explosive firepower installations
- **❄️ Ice Tower (M3/H3)** - Freezing area control defenses
- **🪨 Catapult Tower (M4/H4)** - Heavy siege bombardment units
- **🏹 Archery Tower (M5/H5)** - Swift projectile defense systems

**✨ Wild Symbol** - Magical essence that transforms to aid your defense
**💫 Scatter Symbol** - Ancient runes that unlock bonus campaigns

**Victory Rewards:** Prize towers bestow their treasures at the end of each spin, rewarding your strategic placement!

## ⚔️ Base Game: The Siege Begins

**The Forbidden Center:** The heart of your fortress (3rd reel, 3rd row) remains sealed - a mysterious void that no symbol can occupy. This sacred ground holds ancient power, waiting to be unleashed...

**Tactical Upgrades:** When your resource lands form successful clusters, they evolve into mighty tower defenses!
- **5+ symbol clusters** → Mid-tier towers (M1-M5) emerge from gathered resources
- **10+ symbol clusters** → High-tier towers (H2-H5) rise to dominate the battlefield

**🏗️ Construction System:** Collect 5 matching resource lands to automatically construct the corresponding tower:
- 5 Crystal → Magic Tower | 5 Iron → Cannon Tower | 5 Lake → Ice Tower | 5 Stone → Catapult Tower | 5 Wood → Archery Tower

**🌟 Bonus Campaign Trigger:** Gather 3+ Scatter runes to unlock the legendary campaign
- **8+ Free Spins** awarded for your heroic efforts

## 🔥 Bonus Game: Free Spins Campaign

**The Sacred Awakening:** The forbidden center transforms into a **permanent Wild symbol**, radiating magical energy throughout the entire campaign!

**Persistent Towers:** Your prize symbols become **sticky defenders**, maintaining their positions throughout all free spins while continuing to pay tribute after each battle.

**Campaign Extension:** Discover 2+ Scatter runes during the campaign to earn **2+ additional spins** - the battle continues!

## 💎 Super Bonus Game: Legendary Conquest

**Ultimate Power:** Experience all Bonus Game features enhanced with **progressive multipliers**!

**Escalating Glory:** Each successful upgrade increases the **global multiplier by +1**, accumulating tremendous power that persists throughout the entire Super Bonus campaign.

**Victory grows stronger with every strategic move!**

## 📊 Technical Event System

**Event List:**

- **`reveal`** – Reveals the initial board state at the start of a round
- **`win`** – Comprehensive summary including multipliers, symbol positions, and detailed pay info for each cluster formation
- **`upgrade`** – Tracks the evolution of resource lands into powerful tower defenses
- **`trigger_free_spins`** – Triggers the start of free spins (bonus campaign)
- **`update_free_spins`** – Updates the current free spin count and emits related events
- **`update_global_mult`** – (Not used in Tower Defense, but present in the codebase for other games) Updates the global multiplier

## 🔧 Analysis Tools

### 🎯 Strategic Analysis Scripts

#### `analyze_clustering.py`
**Purpose:** Evaluates the tactical potential of each resource land in your construction strategy.
**Usage:** `python analyze_clustering.py`
**Battle Intelligence:** 
- Analyzes horizontal and vertical formation opportunities
- Calculates clustering effectiveness for each resource type (L1-L5)
- Identifies maximum cluster potential and distribution strategies
- Critical for understanding why certain resource lands have lower collection rates

#### `analyze_wins.py`
**Purpose:** Analyzes victory distribution from battle records (books JSON files).
**Usage:** `python analyze_wins.py [filename]`
**Victory Analytics:**
- Parses books_base.json and books_bonus.json battle logs
- Counts victories per resource/tower type with detailed tactical breakdown
- Shows cluster sizes and reward amounts for L4/L5 resource lands
- Provides percentage distribution of wins across all resource and tower types
- Default analyzes `library/books/books_base.json`

### 🎮 Combat Commands

```bash
# Analyze current resource land clustering potential
python analyze_clustering.py

# Review victory distribution after construction
python analyze_wins.py
```

### ⚖️ Battle Configuration Status

**Current Resource & Tower Hierarchy:**
- **L1 (Crystal Resources):** 1.0x - 60.0x 💎 → ✨ Magic Tower
- **L2 (Iron Resources):** 0.5x - 30.0x ⚒️ → 🔥 Cannon Tower
- **L3 (Lake Resources):** 0.2x - 12.0x 🌊 → ❄️ Ice Tower
- **L4 (Stone Resources):** 0.1x - 6.0x 🪨 → 🪨 Catapult Tower
- **L5 (Wood Resources):** 0.05x - 3.5x 🪵 → 🏹 Archery Tower

**🎯 Optimization Status:** ✅ **Construction Complete**
- L4 and L5 resource clustering optimized for balanced collection rates
- All resource types now achieve comparable gathering rates (18-25%)
- Tower construction mechanics verified and functioning at peak performance
- **Ready for epic fortress building!**