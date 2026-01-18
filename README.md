# GridPick Pro (RELAXED) 🎨

**The calm colors grid trading analyzer - now with Desktop + Pydroid3 support**

## 🇺🇸 USA Regulatory Compliant

**MADE FOR US TRADERS - FULLY COMPLIANT**

This bot is specifically designed to meet US regulatory requirements:
- ✅ **SPOT TRADING ONLY** (no futures, no derivatives)
- ✅ **LONG POSITIONS ONLY** (no shorting)
- ✅ **NO LEVERAGE** (100% compliant with US regulations)
- ✅ **US EXCHANGES ONLY** (Kraken US, CoinGecko)
- ✅ **Regulatory Compliant** for US retail traders

**Hard to find USA-compliant grid analyzers?** This is one of the few built specifically for US traders.

---

## ✨ What Makes This Special

### 🎨 Calm Colors Theme (RELAXED = Calm Colors!)
Unlike most trading bots with harsh, eye-straining colors, GridPick Pro RELAXED uses:
- **Soft, calm color palette** designed for extended viewing
- **Easy on the eyes** during long trading sessions
- **Professional appearance** without the typical "hacker green"
- **Configurable** - turn colors off if needed

### 🖥️ NEW: Desktop + Mobile Support
Now works great on both platforms:
- **Desktop**: Wide tables, clear screen refresh, box-drawing characters
- **Mobile (Pydroid3)**: Compact output, optimized for small screens
- **Auto-detect**: Automatically picks the right mode for your platform

### 🎯 Core Features

- **Dual Data Sources**: Kraken API (primary) + CoinGecko (fallback)
- **Grid Opportunity Scanner**: Finds optimal grid trading setups
- **Dynamic Take-Profit Calculator**: ATR-based profit targets
- **Cycle Time Estimator**: Estimates grid completion time
- **Concurrent Analysis**: ThreadPoolExecutor for fast scanning
- **Extensive Watchlist**: 36 default pairs including BTC, ETH, SOL, memecoins
- **Environment Configurable**: Control everything via env vars

---

## 🖥️ Desktop vs Mobile Mode

The app auto-detects your platform, but you can override:

```bash
# Force desktop mode
export PLATFORM=desktop
python gridpick_pro_relaxed.py

# Force mobile mode (Pydroid3)
export PLATFORM=mobile
python gridpick_pro_relaxed.py
```

### Desktop Mode Features
- Wide table format with full column headers
- Box-drawing characters for visual appeal
- Clear screen between refreshes (disable with `CLEAR_SCREEN=0`)
- Detailed grid configuration output
- Shows liquidity in dollars

### Mobile Mode Features
- Compact single-line output
- Minimal headers to save space
- No screen clearing (scroll-friendly)
- Abbreviated labels

---

## 📊 How It Works

GridPick Pro analyzes cryptocurrency pairs to find optimal grid trading opportunities by:

1. **ATR Analysis**: Measures volatility (Average True Range)
2. **Choppiness Index**: Identifies sideways/ranging markets (ideal for grids)
3. **Drift Detection**: Ensures price isn't trending too strongly
4. **Volume Filtering**: Minimum turnover requirements
5. **Grid Spacing**: Calculates optimal buy/sell levels
6. **Take-Profit Targets**: Dynamic TP based on volatility

**Output**: Top N pairs ranked by grid potential with full metrics

---

## 🚀 Quick Start

### Installation

```bash
pip install requests urllib3
```

### Basic Usage

```bash
python gridpick_pro_relaxed.py
```

### Advanced Configuration

Use environment variables to customize:

```bash
# Platform
export PLATFORM="desktop"       # Force desktop or mobile mode
export CLEAR_SCREEN="1"         # Clear screen between refreshes (desktop only)

# Scanning
export INTERVAL="30m"           # Candle interval (5m, 15m, 30m, 1h, 4h, 1d)
export LIMIT="240"              # Number of candles to analyze
export REFRESH="25"             # Seconds between scans
export TOPN="5"                 # Show top N picks

# Filters
export MIN_ATR_PCT="0.10"       # Minimum ATR % (volatility)
export MIN_CHOP="0.20"          # Minimum choppiness (0-1, higher = more sideways)
export MAX_DRIFT_PCT="7.0"      # Maximum price drift %
export MIN_TURNOVER_USD="50000" # Minimum 24h volume (Kraken)
export CG_MIN_TURNOVER_USD="5000" # Minimum volume (CoinGecko fallback)

# Grid & Fees
export FEE_PCT="0.10"           # Trading fee %
export MIN_GRID_MULT="3.0"      # Minimum grid spacing multiplier

# Watchlist (comma-separated)
export WATCHLIST="BTC/USDT,ETH/USDT,SOL/USDT,XRP/USDT"

python gridpick_pro_relaxed.py
```

---

## 🎨 Color Customization

**Disable colors** (for plain output):

Edit the script:
```python
USE_COLOR = False  # Change True to False
```

**Color palette** (calm theme):
- Grey - headers and dividers
- Green - qualified picks, buy signals
- Yellow - warnings, relaxed picks
- Cyan - highlights, score colors
- Dim - timestamps, secondary info

---

## 📈 Output Example

### Desktop Mode
```
╔════════════════════════════════════════════════════════════════╗
║              GridPick Pro (RELAXED) — Desktop Mode             ║
╚════════════════════════════════════════════════════════════════╝

Settings: 30m interval | ~5 days lookback | 36 pairs | 25s refresh
Filters:  ATR% ≥ 0.1 | Chop ≥ 0.2 | Drift ≤ 7.0% | Liq ≥ $50,000

  #   Q      Symbol        Score    Chop     ATR%    Drift     ADX     Liquidity         Price
──────────────────────────────────────────────────────────────────────────────────────────────
  1   ✓    SOL/USDT         72.5    0.68     2.45      1.2    42.1      $125,000    142.500000
  2   ✓    LINK/USDT        68.3    0.71     1.89      0.5    38.7       $78,000     14.250000

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🏆 TOP PICK: SOL/USDT  [QUALIFIED]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Metrics:
  Score: 72.5  |  Chop: 0.68  |  ATR: 2.45%  |  Drift: 1.2%  |  ADX: 42.1
  Liquidity: $125,000

Grid Configuration:
  Range:      141.33000000  →  143.67000000
  Levels:     24
  Step Size:  0.082%

Take Profit:
  Target:     ~8.50%
  Est. Cycle: ~12.5h
```

### Mobile Mode
```
▶ GridPick Pro (RELAXED) — 30m / ~5d | 36 pairs | refresh=25s
ATR%≥0.1 | Chop≥0.2 | Drift≤7.0%

#  Q  Symbol      Score   Chop   ATR%  Drift   ADX   Price
1  +  SOL/USDT    72.5   0.68   2.45%  1.2%   42.1  142.500000
2  +  LINK/USDT   68.3   0.71   1.89%  0.5%   38.7  14.250000

* Top Pick SOL/USDT — QUALIFIED
Score 72.5 | Chop 0.68  ATR 2.45%  Drift 1.2%
Grid: 141.33 → 143.67  Lvls: 24  Step: 0.08%
TP: ~8.50% | Est: ~12.5h
```

---

## 🔧 Technical Details

### Data Sources

**Kraken API** (primary):
- More reliable for US traders
- Better historical data
- Used for major pairs

**CoinGecko API** (fallback):
- Broader pair coverage
- Used when Kraken unavailable
- Lower volume threshold

### Calculations

**ATR** (Average True Range):
- 14-period ATR
- Expressed as % of close price
- Measures volatility

**Choppiness Index**:
- Ranges 0-1
- Higher = more sideways action
- Ideal for grid trading

**Grid Spacing**:
- `spacing = ATR * MIN_GRID_MULT`
- Ensures profitable grids after fees
- Dynamically adjusts to volatility

---

## 📱 Platform Support

| Platform | Status | Notes |
|----------|--------|-------|
| **Desktop Linux** | ✅ Full | Wide tables, clear screen |
| **Desktop macOS** | ✅ Full | Wide tables, clear screen |
| **Desktop Windows** | ✅ Full | Wide tables, clear screen |
| **Pydroid3 (Android)** | ✅ Full | Compact mode, original design |
| **Termux (Android)** | ✅ Works | Auto-detects as mobile |
| **SSH/Remote** | ✅ Works | Detects terminal width |

---

## 🎯 Best Use Cases

**Ideal For**:
- Finding grid trading opportunities
- Analyzing multiple pairs quickly
- Identifying ranging markets
- Mobile trading analysis (Pydroid3)
- Desktop market scanning
- Visual market scanning with calm colors

**Not Ideal For**:
- Automated execution (analysis only)
- Trending markets (looks for chop)
- Ultra-low latency (25s refresh default)

---

## 🛡️ Risk Warning

This is an **analysis tool only** - it does NOT execute trades automatically.

- Always verify results manually
- Grid trading carries risk in trending markets
- Past performance doesn't guarantee future results
- Start with paper trading
- Use proper position sizing

---

## 🔐 Security

- **No API keys required** (read-only public data)
- **No trading permissions** (analysis only)
- **Open source** - review the code yourself
- **Privacy focused** - no data sent to third parties

---

## 💡 Tips for Best Results

1. **Use 30m-1h timeframes** for grid trading
2. **Higher CHOP values** (0.6+) = better grid setups
3. **Low DRIFT** (under 5%) = stable grids
4. **Adjust MIN_GRID_MULT** based on fees (higher fees = higher multiplier)
5. **Check volume** - low volume = wide spreads
6. **Run during market hours** for best data

---

## 🎨 Why "RELAXED"?

Most trading terminals use harsh, bright colors that cause eye strain during long sessions.

GridPick Pro RELAXED uses a carefully chosen **calm color palette** that:
- Reduces eye fatigue
- Looks professional
- Maintains readability
- Makes long analysis sessions comfortable

**Your eyes will thank you!** 👁️✨

---

## 📄 License

MIT License - See LICENSE file

---

**Built with care for US traders who value both compliance and comfort.**

**Works on Desktop + Pydroid3** - optimized, tested, and ready to use!
