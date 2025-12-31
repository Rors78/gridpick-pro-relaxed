#!/usr/bin/env python3
# ==========================================================
#  GridPick Pro (RELAXED)
#  Kraken primary — CoinGecko fallback
#  Dynamic Take-Profit + TPDEBUG output + Cycle Estimator
# ==========================================================
import os, sys, time, math, json, random, shutil
from statistics import mean
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor, as_completed
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

# -------------------- Config --------------------
KRAKEN_API = "https://api.kraken.com/0/public"
CG_API     = "https://api.coingecko.com/api/v3"

INTERVAL = os.environ.get("INTERVAL", "30m").lower()
LIMIT    = int(os.environ.get("LIMIT", "240"))
REFRESH  = int(os.environ.get("REFRESH", "25"))
TOPN     = int(os.environ.get("TOPN", "5"))

# Filters
MIN_ATR_PCT = float(os.environ.get("MIN_ATR_PCT",  "0.10"))
MIN_CHOP    = float(os.environ.get("MIN_CHOP",     "0.20"))
MAX_DRIFT   = float(os.environ.get("MAX_DRIFT_PCT","7.0"))
MIN_TURNOVER_USD   = float(os.environ.get("MIN_TURNOVER_USD", "50000"))
CG_MIN_TURNOVER_USD= float(os.environ.get("CG_MIN_TURNOVER_USD", "5000"))

# Grid & fees
FEE_PCT       = float(os.environ.get("FEE_PCT","0.10"))
MIN_GRID_MULT = float(os.environ.get("MIN_GRID_MULT","3.0"))

# Watchlist
DEFAULT_WATCH = [
  "BTC/USDT","ETH/USDT","SOL/USDT","XRP/USDT","ADA/USDT","LINK/USDT",
  "LTC/USDT","DOGE/USDT","AVAX/USDT","SUI/USDT","OPEN/USDT","ENA/USDT",
  "PEPE/USDT","PENGU/USDT","WIF/USDT","BONK/USDT","WLD/USDT","HBAR/USDT",
  "FLOKI/USDT","APEX/USDT","RFC/USDT","IP/USDT","PI/USDT","LINEA/USDT",
  "HYPE/USDT","MYX/USDT","CAKE/USDT","ASTER/USDT","AVNT/USDT","XPL/USDT",
  "SEI/USDT","ZKC/USDT","MBTC/USDT","TRUMP/USDT","EIGEN/USDT","0G/USDT"
]
WATCHLIST = [s.strip().upper() for s in os.environ.get("WATCHLIST", ",".join(DEFAULT_WATCH)).split(",") if s.strip()]

# Force color in PyDroid; set to False if you want plain output
USE_COLOR = True
def _c(s): return s if USE_COLOR else ""
FG = {k:_c(v) for k,v in {
  "gry":"\033[90m","red":"\033[91m","grn":"\033[92m","ylw":"\033[93m",
  "blu":"\033[94m","mag":"\033[95m","cyn":"\033[96m","wht":"\033[97m"
}.items()}
BOLD=_c("\033[1m"); RESET=_c("\033[0m")

# -------------------- HTTP --------------------
SESSION = requests.Session()
SESSION.headers.update({"User-Agent":"GridPickPro/relaxed"})
retry = Retry(total=4, backoff_factor=0.6,
              status_forcelist=[418,429,500,502,503,504],
              allowed_methods=["GET"])
SESSION.mount("https://", HTTPAdapter(max_retries=retry))
SESSION.mount("http://",  HTTPAdapter(max_retries=retry))

def jget(url, params=None, timeout=8):
    try:
        r = SESSION.get(url, params=params, timeout=timeout)
        r.raise_for_status()
        return r.json()
    except Exception:
        return None

# -------------------- Helpers --------------------
def interval_minutes(s: str) -> int:
    lut = {"15m":15,"30m":30,"1h":60,"240m":240,"60m":60}
    return lut.get(s, 30)
IV_MIN = interval_minutes(INTERVAL)

def cscore(x):
    if x>=75: return FG["cyn"]
    if x>=60: return FG["grn"]
    if x>=45: return FG["ylw"]
    return FG["gry"]

# -------------------- Kraken OHLC --------------------
def k_altname(sym):
    return sym.replace("/","")

def fetch_ohlc_kraken(sym):
    alt = k_altname(sym)
    params = {"pair":alt, "interval":IV_MIN}
    j = jget(f"{KRAKEN_API}/OHLC", params=params)
    if not j or "result" not in j: return []
    res = j["result"]
    arr = next(iter({k:v for k,v in res.items() if k!="last"}.values()), [])
    out=[]
    for r in arr[-LIMIT:]:
        try:
            t=int(r[0])*1000; o=float(r[1]); h=float(r[2]); l=float(r[3]); c=float(r[4]); v=float(r[6])
            out.append((t,o,h,l,c,v))
        except Exception:
            continue
    return out

# -------------------- CoinGecko Fallback --------------------
CG_CACHE = {}
def cg_search_id(symbol_base: str):
    key=symbol_base.lower()
    if key in CG_CACHE: return CG_CACHE[key]
    j = jget(f"{CG_API}/search", {"query": symbol_base})
    if not j: return None
    for coin in j.get("coins", []):
        if coin.get("symbol","").lower()==symbol_base.lower():
            CG_CACHE[key]=coin.get("id"); return CG_CACHE[key]
    if j.get("coins"):
        CG_CACHE[key]=j["coins"][0].get("id")
        return CG_CACHE[key]
    return None

def cg_turnover_usd(sym: str):
    base = sym.split("/")[0]
    cid = cg_search_id(base)
    if not cid: return 0.0
    j = jget(f"{CG_API}/coins/markets", {"vs_currency":"usd","ids":cid})
    try:
        vol = float(j[0]["total_volume"])
        return vol
    except Exception:
        return 0.0

# -------------------- Indicators --------------------
def atr_pct(rows, period=14):
    if len(rows)<max(period+1, 20): return 0.0
    trs=[]; prev_c = rows[0][4]
    for (_,_,h,l,c,_) in rows:
        tr = max(h-l, abs(h-prev_c), abs(l-prev_c))
        trs.append(tr)
        prev_c = c
    atr = mean(trs[-period:])
    px  = rows[-1][4]
    return (atr/px)*100 if px>0 else 0.0

def drift_pct(rows):
    if not rows: return 0.0
    c0 = rows[0][4]; cN = rows[-1][4]
    return abs((cN-c0)/c0)*100 if c0>0 else 0.0

def chop_factor(rows):
    closes = [c for *_,c,_ in rows]
    flips=0
    for i in range(2,len(closes)):
        d1=closes[i]-closes[i-1]; d0=closes[i-1]-closes[i-2]
        if d1*d0<0: flips+=1
    return flips/max(len(closes)-2,1)

def adx_like(rows, look=14):
    if len(rows)<look+2: return 50.0
    closes=[c for *_,c,_ in rows]
    ups=downs=0
    for i in range(1,look+1):
        d=closes[-i]-closes[-i-1]
        ups   += (d>0)
        downs += (d<0)
    bal = abs(ups-downs)/look
    return 50*(1+bal)

# -------------------- Liquidity --------------------
def kraken_turnover_usd(rows):
    if not rows: return 0.0
    alpha=0.2; ema=0.0
    for (_,_,h,l,c,v) in rows[-48:]:
        mid=(h+l)/2.0
        ema = alpha*(v*mid)+(1-alpha)*ema
    return ema

# -------------------- Scoring --------------------
def score_symbol(sym, rows, liq_usd):
    if not rows: return None
    px = rows[-1][4]
    atrp = atr_pct(rows)
    drift = drift_pct(rows)
    chop = chop_factor(rows)
    adx  = adx_like(rows)

    qualified = (atrp>=MIN_ATR_PCT and chop>=MIN_CHOP and drift<=MAX_DRIFT and liq_usd>=MIN_TURNOVER_USD)

    if atrp <= 0: vol = 0.0
    elif atrp < 0.2: vol = atrp/0.2
    elif atrp > 1.5: vol = max(0.0, 1.0 - (atrp-1.5)/1.5)
    else: vol = 1.0
    drift_pen = min(1.0, drift/12.0)
    liq_boost = 1.0/(1.0+math.exp(-(liq_usd-MIN_TURNOVER_USD)/(MIN_TURNOVER_USD*0.6)))
    adx_pen   = min(1.0, max(0.0,(adx-22.0)/50.0))

    raw = (0.40*chop + 0.35*vol + 0.15*liq_boost - 0.15*drift_pen - 0.10*adx_pen)
    score = max(0.0, min(1.0, raw))*100.0

    return {
        "symbol": sym, "price": px,
        "atr_pct": atrp, "chop": chop, "drift": drift, "adx": adx,
        "turnover": liq_usd, "score": round(score,1),
        "qualified": qualified
    }

# -------------------- Grid Suggestion --------------------
def fee_okay(span_pct, grids):
    step = span_pct/max(grids,2)
    return step >= (FEE_PCT*MIN_GRID_MULT)

def suggest_grid(px, atrp, liq_ok=True):
    span = max(0.03, min(0.08, atrp / 30.0))
    if not liq_ok: span *= 1.2
    lo = px*(1-span); hi=px*(1+span)
    grids = max(12, min(40, int(18 + atrp*10)))
    span_pct = (hi-lo)/px*100.0

    guard=0
    while not fee_okay(span_pct, grids) and guard<8:
        if grids>18: grids=int(grids*0.9)
        else:
            span*=1.08; lo=px*(1-span); hi=px*(1+span)
            span_pct=(hi-lo)/px*100.0
        guard+=1

    step_pct = span_pct / grids

    # --- Dynamic TP formula ---
    chop_val = random.uniform(0.3, 0.7)
    drift_val = random.uniform(0.0, 5.0)
    try:
        from inspect import currentframe
        outer = currentframe().f_back
        m = outer.f_locals.get("m", {})
        chop_val = m.get("chop", chop_val)
        drift_val = m.get("drift", drift_val)
    except Exception:
        pass

    per = (atrp * chop_val) / (1 + drift_val / 5)
    tp_pct = min(20.0, max(5.0, 4.0 + per * 25))

    # --- cycle-duration estimate ---
    # Realistic velocity: price moves at ~0.35 * ATR per bar in choppy conditions
    velocity_per_bar = atrp * 0.35
    bars_to_tp = max(10, min(500, tp_pct / max(velocity_per_bar, 0.01)))
    hours_est = bars_to_tp * IV_MIN / 60
    if hours_est >= 48:
        cycle_str = f"~{hours_est/24:.1f}d"
    else:
        cycle_str = f"~{hours_est:.1f}h"

    tpdebug = bool(int(os.environ.get("TPDEBUG", "0"))) or ("--tpdebug" in sys.argv)
    if tpdebug:
        print(
            f"{FG['gry']}[TPDEBUG] px={px:.4f} atr%={atrp:.3f} chop={chop_val:.2f} drift={drift_val:.1f} "
            f"PER={per:.4f} → TP%={tp_pct:.2f} est={cycle_str}{RESET}"
        )

    return {"lo":lo,"hi":hi,"grids":grids,"step_pct":step_pct,"tp_pct":tp_pct,"cycle":cycle_str}

# -------------------- Scan --------------------
def scan_once():
    results=[]
    batch=6; workers=3
    for i in range(0, len(WATCHLIST), batch):
        chunk = WATCHLIST[i:i+batch]
        with ThreadPoolExecutor(max_workers=min(workers, len(chunk))) as ex:
            futs={ex.submit(fetch_ohlc_kraken, s): s for s in chunk}
            for fut in as_completed(futs):
                sym=futs[fut]; rows=[]
                try: rows=fut.result()
                except Exception: rows=[]
                if not rows: continue
                liq = kraken_turnover_usd(rows)
                if liq < MIN_TURNOVER_USD:
                    liq_cg = cg_turnover_usd(sym)
                    if liq_cg >= CG_MIN_TURNOVER_USD: liq = liq_cg
                rec = score_symbol(sym, rows, liq)
                if rec: results.append(rec)
        time.sleep(0.3)
    results.sort(key=lambda r: r["score"], reverse=True)
    return results

# -------------------- Display --------------------
def banner():
    ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    hdr = (f"{BOLD}▶ GridPick Pro (RELAXED) — {INTERVAL} / ~{int(LIMIT*IV_MIN/1440)}d  "
           f"| Kraken→CoinGecko {len(WATCHLIST)} pairs | refresh={REFRESH}s{RESET}")
    print(hdr)
    print(f"Filters: ATR%≥{MIN_ATR_PCT} | Chop≥{MIN_CHOP} | Drift≤{MAX_DRIFT}% | "
          f"Liq ≥ ${int(MIN_TURNOVER_USD):,} / ${int(CG_MIN_TURNOVER_USD):,} (CG)")
    print(FG["gry"] + ts + RESET)

def row_line(i, r):
    badge = "🟢" if r["qualified"] else "⚠️"
    return (f"{FG['gry']}{i:<2}{RESET} {badge} "
            f"{BOLD}{r['symbol']:<10}{RESET}  "
            f"{cscore(r['score'])}{r['score']:>5.1f}{RESET}  "
            f"chop {r['chop']:.2f}  atr {r['atr_pct']:.2f}%  "
            f"drift {r['drift']:.1f}%  adx {r['adx']:.1f}  "
            f"px {r['price']:.6f}")

def print_table(top):
    print(f"{BOLD}#  Q  Symbol      Score   Chop   ATR%  Drift   ADX   Price{RESET}")
    for i, r in enumerate(top, 1):
        print(row_line(i, r))

def print_pick(m):
    rec = suggest_grid(m["price"], m["atr_pct"], liq_ok=(m["turnover"]>=MIN_TURNOVER_USD))
    note = "QUALIFIED" if m["qualified"] else "RELAXED ⚠"
    print(f"\n{BOLD}🏆 Top Pick {m['symbol']} — {note}{RESET}")
    print(f"Score {cscore(m['score'])}{m['score']:.1f}{RESET} | "
          f"Chop {m['chop']:.2f}  ATR {m['atr_pct']:.2f}%  Drift {m['drift']:.1f}%  "
          f"ADX {m['adx']:.1f}  Liq ${int(m['turnover']):,}")
    print(f"Grid ⇒ {FG['cyn']}{rec['lo']:.6f}{RESET} → {FG['cyn']}{rec['hi']:.6f}{RESET}   "
          f"Levels ⇒ {FG['ylw']}{rec['grids']}{RESET}   Step ≈ {rec['step_pct']:.2f}%")
    print(f"TP ⇒ ~{rec['tp_pct']:.2f}% (full-cycle take-profit) "
          f"{FG['gry']}expected {rec['cycle']}{RESET}\n")
    print(FG["gry"]+f"EXPORT: symbol={m['symbol']}, low={rec['lo']:.8f}, high={rec['hi']:.8f}, "
          f"levels={rec['grids']}, step={rec['step_pct']:.4f}%, tp={rec['tp_pct']:.2f}%"+RESET)

# -------------------- Main --------------------
def main():
    banner()
    while True:
        results = scan_once()
        if not results:
            print(FG["red"]+"⚠ No data this pass (network/API)."+RESET)
            time.sleep(REFRESH)
            continue

        qualified = [r for r in results if r["qualified"]]
        if qualified:
            top = qualified[:TOPN]
            print_table(top)
            print_pick(top[0])
        else:
            best = results[0]
            print(FG["ylw"] + "⚠ No symbols passed filters — showing best available (relaxed)." + RESET)
            print_table(results[:TOPN])
            print_pick(best)

        time.sleep(REFRESH)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nBye.")
