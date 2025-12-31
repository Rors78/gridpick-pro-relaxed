# GridPick Pro (RELAXED) 🎨

**The calm colors grid trading analyzer - optimized for Pydroid3**

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

### 🎨 Calm Colors Theme (RELAXED Mode)
Unlike most trading bots with harsh, eye-straining colors, GridPick Pro RELAXED uses:
- **Soft, calm color palette** designed for extended viewing
- **Easy on the eyes** during long trading sessions
- **Professional appearance** without the typical "hacker green"
- **Configurable** - turn colors off if needed

This is the **final Pydroid3 version** before the web browser port - and it's the best one!

### 🎯 Core Features

- **Dual Data Sources**: Kraken API (primary) + CoinGecko (fallback)
- **Grid Opportunity Scanner**: Finds optimal grid trading setups
- **Dynamic Take-Profit Calculator**: ATR-based profit targets
- **Cycle Time Estimator**: Estimates grid completion time
- **Concurrent Analysis**: ThreadPoolExecutor for fast scanning
- **Extensive Watchlist**: 36 default pairs including BTC, ETH, SOL, memecoins
- **Mobile Optimized**: Built for Pydroid3 on Android
- **Environment Configurable**: Control everything via env vars

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

Edit line 47 in the script:
```python
USE_COLOR = False  # Change True to False
```

**Color palette** (calm theme):
- Grey - headers and dividers
- Red - sell levels
- Green - buy levels
- Yellow - warnings
- Blue - key metrics
- Cyan - highlights
- Magenta - TP targets

---

## 📈 Output Example

```
╔══════════════════════════════════════════════════════════════╗
║          GridPick Pro (RELAXED) - Top 5 Picks               ║
╚══════════════════════════════════════════════════════════════╝

#1  SOL/USDT  [Kraken]
    ATR: 2.45%  Chop: 0.68  Drift: +1.2%  Vol: $125M
    Grid: 0.82% spacing (3.4x ATR)
    Entry: $142.50  Buy: $141.33  Sell: $143.67
    TP: $145.80 (+2.3%)  Est: ~8.5 hours

#2  LINK/USDT  [CoinGecko]
    ATR: 1.89%  Chop: 0.71  Drift: -0.5%  Vol: $78M
    Grid: 0.65% spacing (3.1x ATR)
    ...
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

**Take-Profit**:
- Based on recent price action
- Adjusts for market conditions
- **Note**: TP time estimation needs improvement (known issue)

---

## 📁 Export Features

GridPick saves results to `exports/` directory:
- `gridpick_latest.json` - Last scan results
- `gridpick_latest.csv` - CSV format
- `gridpick_latest.txt` - Human-readable
- `gridpick_log.jsonl` - Append-only log
- Timestamped snapshots

---

## ⚠️ Known Issues & Roadmap

### Current Issues
1. **Grid spacing too tight** - Microscopic spacing needs better scaling
2. **TP time assessment faulty** - Cycle estimator needs recalibration
3. **Volume filtering** - Could be more sophisticated

### Planned Improvements
- Fix grid spacing algorithm (make it more conservative)
- Improve TP time estimation accuracy
- Add backtest mode
- Enhanced volume analysis
- Web UI version (grok-gridpick spinoff in progress)

---

## 🎯 Best Use Cases

**Ideal For**:
- Finding grid trading opportunities
- Analyzing multiple pairs quickly
- Identifying ranging markets
- Mobile trading analysis (Pydroid3)
- Visual market scanning with calm colors

**Not Ideal For**:
- Automated execution (analysis only)
- Trending markets (looks for chop)
- Ultra-low latency (25s refresh default)

---

## 📱 Pydroid3 Optimization

This bot was built specifically for Pydroid3:
- Minimal dependencies (requests only)
- Efficient memory usage
- Terminal-friendly output
- No heavy libs (no pandas, numpy, TA-Lib)
- Works offline once data fetched

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

## 📊 Comparison with Other Versions

| Version | Status | Notes |
|---------|--------|-------|
| **GridPick Pro RELAXED** | ✅ Final | This version - calm colors, Pydroid3 |
| grok-gridpick (web) | 🚧 Beta | Web UI spinoff, not as good yet |
| gridpick_enhanced | 📦 Archive | Earlier version |

**This is the recommended version** for terminal/mobile use!

---

## 🤝 Contributing

This is a personal trading tool. Feel free to fork and modify for your own use.

Improvements welcome:
- Better grid spacing algorithm
- More accurate TP time estimation
- Additional exchange support
- Enhanced filters

---

## 📄 License

MIT License - See LICENSE file

---

## 🎨 Why "RELAXED"?

Most trading terminals use harsh, bright colors that cause eye strain during long sessions.

GridPick Pro RELAXED uses a carefully chosen calm color palette that:
- Reduces eye fatigue
- Looks professional
- Maintains readability
- Makes long analysis sessions comfortable

**Your eyes will thank you!** 👁️✨

---

**Built with care for US traders who value both compliance and comfort.**

**Final Pydroid3 version** - optimized, tested, and ready to use!
