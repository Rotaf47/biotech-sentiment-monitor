from concurrent.futures import ThreadPoolExecutor
from datetime import datetime
import time

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import streamlit as st

# Page Configuration
st.set_page_config(
    page_title="Biotech Sentiment Monitor & Squeeze Screener",
    page_icon="🧬",
    layout="wide",
)

st.title("🧬 Biotech Sentiment & Squeeze Monitor (BSM)")
st.markdown(
    "Scans live biotech tickers, tracks price action, evaluates **Float &"
    " Short Squeeze Metrics**, and visualizes sector-wide sentiment."
)

# Sidebar controls for Alpaca API Credentials
st.sidebar.header("Alpaca API Settings")
alpaca_api_key = st.sidebar.text_input(
    "Alpaca API Key", value="PKKUDHFXLGCRECNPFHWFINVFZY", type="password"
)
alpaca_secret_key = st.sidebar.text_input(
    "Alpaca Secret Key",
    value="3Lo3FMU1TdEbvYQzAZ5XMLFre7bmzd1Lp9fDJ6PJ2czx",
    type="password",
)

# Expanded Ticker List
DEFAULT_TICKERS = [
    "AAPG",
    "AARD",
    "ABCL",
    "ABEO",
    "ABOS",
    "ABSI",
    "ABTS",
    "ABUS",
    "ABVC",
    "ABVX",
    "ACAD",
    "ACET",
    "ACHV",
    "ACIU",
    "ACLX",
    "ACOG",
    "ACRS",
    "ACRV",
    "ACTU",
    "ADAG",
    "ADMA",
    "ADRX",
    "ADUS",
    "AEMD",
    "AEON",
    "AGEN",
    "AGIO",
    "AGMB",
    "AKTS",
    "AKTX",
    "ALDX",
    "ALEC",
    "ALGS",
    "ALKS",
    "ALLO",
    "ALLR",
    "ALMS",
    "ALNY",
    "ALPS",
    "ALT",
    "ALVO",
    "ALXO",
    "ALZN",
    "AMLX",
    "ANAB",
    "ANIX",
    "ANL",
    "ANNX",
    "ANRO",
    "ANTX",
    "ANVS",
    "APLM",
    "APMD",
    "APRE",
    "APVO",
    "ARCT",
    "ARDX",
    "ARGX",
    "ARMP",
    "ARQT",
    "ARTV",
    "ARVN",
    "ARWR",
    "ASBP",
    "ASMB",
    "ASND",
    "ATHE",
    "ATNM",
    "ATOS",
    "ATRA",
    "ATTO",
    "ATYR",
    "AUPH",
    "AURA",
    "AUTL",
    "AVBP",
    "AVIR",
    "AVLN",
    "AVTX",
    "AVXL",
    "AXSM",
    "AYTU",
    "BBIO",
    "BBLG",
    "BBOT",
    "BCAX",
    "BCDA",
    "BCRX",
    "BCTX",
    "BCYC",
    "BDSX",
    "BDTX",
    "BEAM",
    "BGMS",
    "BHVN",
    "BIIB",
    "BIO",
    "BIOA",
    "BIOX",
    "BJDX",
    "BLRX",
    "BLSM",
    "BLTE",
    "BMEA",
    "BMRN",
    "BNTC",
    "BNTX",
    "BOLD",
    "BRTX",
    "BRVE",
    "BSEM",
    "BYSI",
    "CABA",
    "CADL",
    "CAI",
    "CAMP",
    "CAPR",
    "CBIO",
    "CBUS",
    "CCCC",
    "CDNA",
    "CDXS",
    "CELC",
    "CELU",
    "CELZ",
    "CGEM",
    "CGON",
    "CGTX",
    "CHRS",
    "CING",
    "CLDX",
    "CLNN",
    "CLPT",
    "CLRB",
    "CLRO",
    "CLYM",
    "CMPX",
    "CNSP",
    "CNSY",
    "CNTB",
    "CNTN",
    "CNTX",
    "CNXU",
    "COAG",
    "COCP",
    "CODX",
    "COGT",
    "CORT",
    "COYA",
    "CRBP",
    "CRBU",
    "CRDF",
    "CRIS",
    "CRMD",
    "CRSP",
    "CRVO",
    "CRVS",
    "CSBR",
    "CTKB",
    "CTMX",
    "CTNM",
    "CTOR",
    "CTXR",
    "CUE",
    "CUVL",
    "CVKD",
    "CVM",
    "CYPH",
    "CYRX",
    "CYTK",
    "DARE",
    "DBVT",
    "DFTX",
    "DMAC",
    "DMRA",
    "DNA",
    "DNLI",
    "DNTH",
    "DRTS",
    "DRUG",
    "DSGN",
    "DSTX",
    "DTIL",
    "DWTX",
    "DYAI",
    "DYN",
    "EBS",
    "ECOR",
    "EDIT",
    "EDSA",
    "EIKN",
    "ELOX",
    "ELTX",
    "ELVN",
    "ENGN",
    "ENSC",
    "ENTA",
    "ENTX",
    "EPRX",
    "EQ",
    "ERAS",
    "ERNA",
    "ESLA",
    "ETRA",
    "EVAX",
    "EVMN",
    "EWTX",
    "EXEL",
    "EXOZ",
    "EYPT",
    "FATE",
    "FBIO",
    "FDMT",
    "FDTX",
    "FEMY",
    "FENC",
    "FERA",
    "FHTX",
    "FLNA",
    "FTH",
    "FTRE",
    "FULC",
    "GALT",
    "GANX",
    "GENB",
    "GERN",
    "GHRS",
    "GLSI",
    "GLUE",
    "GMAB",
    "GNLX",
    "GNPX",
    "GOSS",
    "GOVX",
    "GPCR",
    "GRCE",
    "GRDX",
    "GRI",
    "GTBP",
    "GUTS",
    "GYRE",
    "HALO",
    "HBIO",
    "HELP",
    "HIND",
    "HOWL",
    "HRMY",
    "HRTX",
    "HUMA",
    "HURA",
    "HYBX",
    "HYFT",
    "HYPD",
    "IBIO",
    "IBO",
    "IBRX",
    "ICCC",
    "ICU",
    "IDYA",
    "IFRX",
    "IGC",
    "IKT",
    "IMA",
    "IMCR",
    "IMMP",
    "IMMX",
    "IMNM",
    "IMRX",
    "IMTX",
    "IMUX",
    "IMVT",
    "INAB",
    "INBX",
    "INCY",
    "INDP",
    "INKT",
    "INMB",
    "INO",
    "INSM",
    "INTS",
    "INVA",
    "IONS",
    "IOVA",
    "IPHA",
    "IPSC",
    "IRD",
    "IRON",
    "IVA",
    "IVVD",
    "JAGX",
    "JANX",
    "JAZZ",
    "JBIO",
    "JSPR",
    "KARD",
    "KLRA",
    "KLRS",
    "KNSA",
    "KOD",
    "KPRX",
    "KPTI",
    "KROS",
    "KRRO",
    "KRSA",
    "KRYS",
    "KTTA",
    "KURA",
    "KYMR",
    "KYNB",
    "KYTX",
    "KZIA",
    "LBRX",
    "LCTX",
    "LEGN",
    "LENZ",
    "LGND",
    "LGVN",
    "LIMN",
    "LIQT",
    "LITS",
    "LKFT",
    "LNAI",
    "LONA",
    "LPCN",
    "LQDA",
    "LRMR",
    "LTGO",
    "LTRN",
    "LUNG",
    "LXEO",
    "LXRX",
    "LYEL",
    "MAIA",
    "MANE",
    "MAZE",
    "MBIO",
    "MBX",
    "MCRB",
    "MDGL",
    "MDWD",
    "MDXG",
    "MENS",
    "MESO",
    "MGNX",
    "MGRX",
    "MGX",
    "MIRM",
    "MIST",
    "MLYS",
    "MNKD",
    "MNOV",
    "MNPR",
    "MOLN",
    "MREO",
    "MRNA",
    "MRVI",
    "MSLE",
    "MYCN",
    "MYGN",
    "NAMS",
    "NAUT",
    "NBIS",
    "NBIX",
    "NBP",
    "NBTX",
    "NCEL",
    "NCNA",
    "NERV",
    "NEUP",
    "NGEN",
    "NGNE",
    "NKTR",
    "NKTX",
    "NMRA",
    "NNVC",
    "NRIX",
    "NRXP",
    "NRXS",
    "NTHI",
    "NTLA",
    "NTRB",
    "NTRP",
    "NUVB",
    "NVCT",
    "NXTC",
    "OABI",
    "OBIO",
    "OBX",
    "OCGN",
    "OCS",
    "OCUL",
    "ODTX",
    "OKUR",
    "OKYO",
    "OLMA",
    "OMER",
    "ONC",
    "ONCO",
    "ONCY",
    "OPAL",
    "ORGO",
    "ORIC",
    "ORKA",
    "ORMP",
    "OSTX",
    "OTLK",
    "OXBR",
    "PACB",
    "PALI",
    "PBLS",
    "PBYI",
    "PCVX",
    "PDSB",
    "PEPG",
    "PGEN",
    "PHAR",
    "PHAT",
    "PHIO",
    "PHVS",
    "PLRX",
    "PLUR",
    "PLX",
    "PLYX",
    "PMN",
    "PMVP",
    "PRAX",
    "PRFX",
    "PRLD",
    "PRME",
    "PROK",
    "PRQR",
    "PRTA",
    "PTCT",
    "PTGX",
    "PTHS",
    "PTN",
    "PULM",
    "PURR",
    "PVLA",
    "PYPD",
    "PYXS",
    "QCLR",
    "QDEL",
    "QGEN",
    "QNRX",
    "QNTM",
    "QTRX",
    "QTTB",
    "QURE",
    "RADX",
    "RANI",
    "RAPP",
    "RARE",
    "RCEL",
    "RCKT",
    "RCUS",
    "REGN",
    "REPL",
    "REVB",
    "RGEN",
    "RGNX",
    "RGTX",
    "RIGL",
    "RKDA",
    "RLAY",
    "RLMD",
    "RLYB",
    "RNA",
    "RNAC",
    "RNAZ",
    "RNTX",
    "RNXT",
    "ROIV",
    "RPID",
    "RPRX",
    "RTSN",
    "RVMD",
    "RXRX",
    "RYTM",
    "SABS",
    "SANA",
    "SBFM",
    "SCTX",
    "SCYX",
    "SEER",
    "SEPN",
    "SER",
    "SERA",
    "SGMT",
    "SGP",
    "SHPH",
    "SIGA",
    "SILO",
    "SION",
    "SMMT",
    "SMTI",
    "SNDX",
    "SNGX",
    "SNTI",
    "SOPH",
    "SORA",
    "SPRB",
    "SPRX",
    "SPRY",
    "SPTX",
    "SRPT",
    "SRRK",
    "SRZN",
    "STOK",
    "STRO",
    "STTK",
    "SUSB",
    "SVRA",
    "SXTC",
    "SYRE",
    "TARA",
    "TARS",
    "TCRT",
    "TCRX",
    "TECH",
    "TECX",
    "TELO",
    "TENX",
    "TGTX",
    "THRD",
    "TIL",
    "TLSA",
    "TLSI",
    "TLX",
    "TNGX",
    "TNXP",
    "TNYA",
    "TPST",
    "TRAX",
    "TRDA",
    "TRVI",
    "TRXB",
    "TSHA",
    "TTRX",
    "TVGN",
    "TVRD",
    "TVTX",
    "TWST",
    "TXG",
    "TYRA",
    "UNCY",
    "UPB",
    "URGN",
    "VALN",
    "VANI",
    "VCEL",
    "VCRE",
    "VCYT",
    "VERA",
    "VERU",
    "VIGL",
    "VIR",
    "VKTX",
    "VNDA",
    "VOGX",
    "VOR",
    "VRAX",
    "VRCA",
    "VRDN",
    "VRXA",
    "VS",
    "VSTM",
    "VTGN",
    "VTVT",
    "VYGR",
    "WHWK",
    "WVE",
    "XBIO",
    "XBIT",
    "XCUR",
    "XENE",
    "XFOR",
    "XLO",
    "XNCR",
    "XRTX",
    "YARW",
    "YDES",
    "ZBIO",
    "ZGN",
    "ZLAB",
    "ZNTL",
    "ZURA",
    "ZVRA",
    "ZYBT",
    "ZYME",
]

# Sidebar controls
st.sidebar.header("Screener Settings")
tickers_input = st.sidebar.text_area(
    "Edit Tickers (comma separated):",
    value=", ".join(DEFAULT_TICKERS),
    height=200,
)

# Parse tickers
tickers = [t.strip().upper() for t in tickers_input.split(",") if t.strip()]
tickers = list(dict.fromkeys(tickers))  # remove duplicates

run_scan = st.sidebar.button("Run Screener & Dashboard", type="primary")

auto_refresh = st.sidebar.toggle(
    "🔄 Enable 5 min Auto-Refresh",
    value=False,
    help="Automatically re-runs the screener every 5 minutes",
)

refresh_btn = st.sidebar.button(
    "🔄 Refresh Data Now",
    help="Clears cache and fetches fresh live data immediately",
)

if refresh_btn:
  st.cache_data.clear()
  if "df_results" in st.session_state:
    del st.session_state["df_results"]
  st.rerun()

if run_scan:
  st.session_state["is_running"] = True


@st.cache_data(ttl=300, show_spinner=False)
def fetch_alpaca_fallback(missing_tickers, api_key, secret_key):
  """Completions missing regular session data via Alpaca Snapshots."""
  from alpaca.data.enums import DataFeed
  from alpaca.data.historical import StockHistoricalDataClient
  from alpaca.data.requests import StockSnapshotRequest

  alpaca_data = {}
  failed_list = []

  if not missing_tickers or not api_key or not secret_key:
    return alpaca_data, missing_tickers

  try:
    client = StockHistoricalDataClient(api_key, secret_key)
    batch_size = 50

    for i in range(0, len(missing_tickers), batch_size):
      batch = missing_tickers[i : i + batch_size]
      try:
        request_params = StockSnapshotRequest(
            symbol_or_symbols=batch, feed=DataFeed.IEX
        )
        snapshots = client.get_stock_snapshot(request_params)

        for ticker in batch:
          if ticker in snapshots and snapshots[ticker]:
            snap = snapshots[ticker]
            prev_close = (
                snap.previous_daily_bar.close
                if snap.previous_daily_bar
                else None
            )
            latest_price = (
                snap.latest_trade.price
                if snap.latest_trade
                else (
                    snap.daily_bar.close
                    if snap.daily_bar
                    else (
                        snap.minute_bar.close if snap.minute_bar else None
                    )
                )
            )

            if prev_close and latest_price:
              alpaca_data[ticker] = pd.Series([prev_close, latest_price])
            else:
              failed_list.append((ticker, "Incomplete Alpaca snapshot price"))
          else:
            failed_list.append((ticker, "No snapshot data on Alpaca"))
      except Exception as e:
        for ticker in batch:
          failed_list.append((ticker, f"Alpaca batch error: {type(e).__name__}"))
  except Exception as e:
    for ticker in missing_tickers:
      failed_list.append((ticker, f"Alpaca init error: {type(e).__name__}"))

  return alpaca_data, failed_list


@st.cache_data(ttl=300, show_spinner=False)
def fetch_screener_data(ticker_list, api_key, secret_key):
  import yfinance as yf

  price_data = {}
  failed_tickers = []
  missing_tickers = []

  batch_size = 50
  for i in range(0, len(ticker_list), batch_size):
    batch = ticker_list[i : i + batch_size]
    try:
      data = yf.download(
          batch,
          period="5d",
          interval="1d",
          auto_adjust=False,
          group_by="ticker",
          threads=True,
          progress=False,
      )

      for ticker in batch:
        try:
          if len(batch) == 1:
            hist = data
          else:
            if ticker in data.columns.levels[0]:
              hist = data[ticker]
            else:
              missing_tickers.append(ticker)
              continue

          if hist.empty or "Close" not in hist.columns:
            missing_tickers.append(ticker)
            continue

          prices = hist["Close"].dropna()
          if len(prices) < 2:
            missing_tickers.append(ticker)
            continue

          price_data[ticker] = prices
        except Exception:
          missing_tickers.append(ticker)
    except Exception:
      missing_tickers.extend(batch)

  if missing_tickers:
    alpaca_data, alpaca_failed = fetch_alpaca_fallback(
        missing_tickers, api_key, secret_key
    )
    price_data.update(alpaca_data)
    failed_tickers.extend(alpaca_failed)

  return price_data, failed_tickers


@st.cache_data(ttl=3600, show_spinner=False)
def fetch_squeeze_metrics(ticker_list):
  """Multithreaded fetching of Float, Short Interest, and Short Ratio from yfinance."""
  import yfinance as yf

  def get_single_info(ticker):
    try:
      info = yf.Ticker(ticker).info
      float_shares = info.get("floatShares") or info.get("sharesOutstanding")
      short_pct = info.get("shortPercentOfFloat")
      short_ratio = info.get("shortRatio")

      short_pct_val = (short_pct * 100) if short_pct is not None else None
      float_m_val = (
          (float_shares / 1_000_000) if float_shares is not None else None
      )

      return ticker, {
          "Float (M)": float_m_val,
          "Short Int (%)": short_pct_val,
          "Short Ratio": short_ratio,
      }
    except Exception:
      return ticker, {
          "Float (M)": None,
          "Short Int (%)": None,
          "Short Ratio": None,
      }

  metrics = {}
  with ThreadPoolExecutor(max_workers=20) as executor:
    results = executor.map(get_single_info, ticker_list)
    for ticker, res in results:
      metrics[ticker] = res

  return metrics


if st.session_state.get("is_running", False):
  with st.spinner("Fetching live market price action & squeeze data..."):
    price_data, failed_tickers = fetch_screener_data(
        tickers, alpaca_api_key, alpaca_secret_key
    )
    squeeze_data = fetch_squeeze_metrics(tickers)

  results = []
  for ticker in tickers:
    if ticker not in price_data:
      results.append({
          "Ticker": ticker,
          "Previous Close ($)": None,
          "Latest Close ($)": None,
          "Change ($)": None,
          "Daily Change (%)": None,
          "Float (M)": None,
          "Short Int (%)": None,
          "Short Ratio": None,
          "Micro Float": "NO",
          "High Short": "NO",
          "Squeeze Score": 0,
          "Status": "No data / insufficient history",
      })
      continue

    prices = price_data[ticker]
    previous_close = float(prices.iloc[-2])
    latest_close = float(prices.iloc[-1])

    if previous_close == 0:
      results.append({
          "Ticker": ticker,
          "Previous Close ($)": previous_close,
          "Latest Close ($)": latest_close,
          "Change ($)": None,
          "Daily Change (%)": None,
          "Float (M)": None,
          "Short Int (%)": None,
          "Short Ratio": None,
          "Micro Float": "NO",
          "High Short": "NO",
          "Squeeze Score": 0,
          "Status": "Invalid previous close",
      })
      continue

    change = latest_close - previous_close
    pct_change = (change / previous_close) * 100

    # Retreive Float & Squeeze Metrics
    sq_info = squeeze_data.get(
        ticker,
        {"Float (M)": None, "Short Int (%)": None, "Short Ratio": None},
    )
    float_m = sq_info["Float (M)"]
    short_pct = sq_info["Short Int (%)"]
    short_ratio = sq_info["Short Ratio"]

    # Structural Rules Evaluation
    is_low_float = float_m is not None and float_m <= 20.0
    is_high_short = short_pct is not None and short_pct >= 15.0

    # Calculate Custom Squeeze Score (0 to 100)
    squeeze_score = 0
    if pct_change >= 15.0:
      squeeze_score += 40  # Momentum Trigger
    if is_low_float:
      squeeze_score += 30  # Choked Supply
    if is_high_short:
      squeeze_score += 30  # Trapped Shorts

    results.append({
        "Ticker": ticker,
        "Previous Close ($)": previous_close,
        "Latest Close ($)": latest_close,
        "Change ($)": change,
        "Daily Change (%)": pct_change,
        "Float (M)": float_m,
        "Short Int (%)": short_pct,
        "Short Ratio": short_ratio,
        "Micro Float": "⚡ YES" if is_low_float else "NO",
        "High Short": "🔥 YES" if is_high_short else "NO",
        "Squeeze Score": squeeze_score,
        "Status": "OK",
    })

  df = pd.DataFrame(results)

  # Sort primarily by Squeeze Score, then by Daily Change
  df = df.sort_values(
      by=["Squeeze Score", "Daily Change (%)"],
      ascending=[False, False],
      na_position="last",
  ).reset_index(drop=True)
  df.insert(0, "Rank", range(1, len(df) + 1))

  st.session_state["df_results"] = df
  st.session_state["failed_tickers"] = failed_tickers

  df = st.session_state["df_results"]
  failed_tickers = st.session_state["failed_tickers"]

  # Key Metrics Summary
  valid = df[df["Status"] == "OK"]
  col1, col2, col3, col4 = st.columns(4)
  col1.metric("Total Scanned", len(tickers))
  col2.metric("Valid Data", len(valid))
  col3.metric("Errors / Missing", len(failed_tickers))
  top_squeezes = len(valid[valid["Squeeze Score"] >= 70])
  col4.metric("🔥 Squeeze Candidates", top_squeezes)

  if not valid.empty:
    top = valid.iloc[0]
    bottom = valid.iloc[-1]
    st.success(
        f"🚀 **Top Squeeze Target:** {top['Ticker']} (Score:"
        f" {top['Squeeze Score']}/100, Change: {top['Daily Change (%)']:+.2f}%)"
        f" & 📉 **Bottom Performer:** {bottom['Ticker']}"
        f" ({bottom['Daily Change (%)']:+.2f}%)"
    )

  # Enhanced Data Frame Table Display
  st.subheader("📋 Stock Performance & Short Squeeze Screener")

  # Highlight formatting for Squeeze Flags
  def style_flags(val):
    if val == "⚡ YES":
      return "background-color: #d3f9d8; color: #2b8a3e; font-weight: bold;"
    elif val == "🔥 YES":
      return "background-color: #ffe3e3; color: #c92a2a; font-weight: bold;"
    return ""

  st.dataframe(
      df.style.format(
          {
              "Previous Close ($)": "{:.4f}",
              "Latest Close ($)": "{:.4f}",
              "Change ($)": "{:+.4f}",
              "Daily Change (%)": "{:+.2f}%",
              "Float (M)": "{:.2f}M",
              "Short Int (%)": "{:.1f}%",
              "Short Ratio": "{:.1f} days",
              "Squeeze Score": "{:d}/100",
          },
          na_rep="N/A",
      ).map(style_flags, subset=["Micro Float", "High Short"]),
      use_container_width=True,
  )

  # CSV Download
  timestamp = datetime.now().strftime("%Y%m%d_%H%M")
  csv = df.to_csv(index=False).encode("utf-8")
  st.download_button(
      label="📥 Download Results as CSV",
      data=csv,
      file_name=f"biotech_squeeze_screener_{timestamp}.csv",
      mime="text/csv",
  )

  # ---------------------------------------------------------------------------
  # RENDER 4-PANEL SENTIMENT DASHBOARD GRAPHS
  # ---------------------------------------------------------------------------
  st.markdown("---")
  st.subheader("📊 Sector Sentiment & Market Breadth Dashboard")

  clean_df = df[df["Status"] == "OK"].copy()
  if not clean_df.empty and "Daily Change (%)" in clean_df.columns:
    returns = pd.to_numeric(
        clean_df["Daily Change (%)"], errors="coerce"
    ).dropna()

    if not returns.empty:
      total = int(len(returns))
      advancers = int((returns > 0).sum())
      decliners = int((returns < 0).sum())
      unchanged = int((returns == 0).sum())

      advance_pct = advancers / total * 100
      decline_pct = decliners / total * 100
      unchanged_pct = unchanged / total * 100

      median_return = float(returns.median())
      mean_return = float(returns.mean())

      breadth_score = advance_pct - decline_pct
      return_score = float(np.clip(mean_return / 2.0 * 100, -100, 100))
      score = float(
          np.clip(0.70 * breadth_score + 0.30 * return_score, -100, 100)
      )

      if score <= -60:
        sentiment, sentiment_color = "VERY BEARISH", "#c92a2a"
      elif score <= -30:
        sentiment, sentiment_color = "BEARISH", "#f08c00"
      elif score < 0:
        sentiment, sentiment_color = "SLIGHTLY BEARISH", "#e0a800"
      elif score < 30:
        sentiment, sentiment_color = "SLIGHTLY BULLISH", "#74b816"
      elif score < 60:
        sentiment, sentiment_color = "BULLISH", "#2f9e44"
      else:
        sentiment, sentiment_color = "VERY BULLISH", "#087f5b"

      fig = plt.figure(figsize=(16, 10), constrained_layout=True)
      gs = fig.add_gridspec(
          2, 2, height_ratios=[0.85, 1.15], width_ratios=[1.15, 1.0]
      )

      ax_score = fig.add_subplot(gs[0, 0])
      ax_breadth = fig.add_subplot(gs[0, 1])
      ax_summary = fig.add_subplot(gs[1, 0])
      ax_distribution = fig.add_subplot(gs[1, 1])

      fig.suptitle(
          "BIOTECH SECTOR SENTIMENT DASHBOARD", fontsize=18, fontweight="bold"
      )

      for ax in [ax_score, ax_breadth, ax_summary, ax_distribution]:
        ax.set_facecolor("#ffffff")
        ax.set_axisbelow(True)

      # Panel 1
      ax_score.set_title(
          "1. Composite Sentiment Score",
          fontsize=12,
          fontweight="bold",
          loc="left",
          pad=12,
      )
      zone_colors = [
          (-100, -60, "#c92a2a"),
          (-60, -30, "#f08c00"),
          (-30, 0, "#ffd43b"),
          (0, 30, "#94d82d"),
          (30, 60, "#2f9e44"),
          (60, 100, "#087f5b"),
      ]
      ax_score.barh(
          0, 200, left=-100, height=0.36, color="#f1f3f5", edgecolor="none"
      )
      for left, right, color in zone_colors:
        ax_score.barh(
            0,
            right - left,
            left=left,
            height=0.36,
            color=color,
            alpha=0.22,
            edgecolor="none",
        )
      ax_score.axvline(
          score, color=sentiment_color, linewidth=3, ymin=0.28, ymax=0.80
      )
      ax_score.scatter(
          [score],
          [0],
          color=sentiment_color,
          edgecolor="white",
          linewidth=1.5,
          s=130,
          zorder=5,
      )
      ax_score.axvline(0, color="#343a40", linewidth=1.2, linestyle="--")
      ax_score.set_xlim(-105, 105)
      ax_score.set_ylim(-0.8, 0.85)
      ax_score.set_yticks([])
      ax_score.set_xticks([-100, -60, -30, 0, 30, 60, 100])
      ax_score.set_xlabel(f"Score: {score:+.2f} / 100", fontsize=9, labelpad=8)
      ax_score.text(
          0.5,
          0.94,
          sentiment,
          transform=ax_score.transAxes,
          ha="center",
          va="top",
          fontsize=12,
          fontweight="bold",
          color=sentiment_color,
      )
      ax_score.grid(axis="x", alpha=0.15)
      for spine in ax_score.spines.values():
        spine.set_visible(False)

      # Panel 2
      ax_breadth.set_title(
          "2. Market Breadth",
          fontsize=12,
          fontweight="bold",
          loc="left",
          pad=12,
      )
      breadth_labels = ["Advancing", "Declining", "Unchanged"]
      breadth_values = [advancers, decliners, unchanged]
      bars = ax_breadth.bar(
          breadth_labels,
          breadth_values,
          color=["#2f9e44", "#e03131", "#adb5bd"],
          width=0.58,
          edgecolor="white",
          linewidth=1,
      )
      max_val = max(breadth_values) if breadth_values else 1
      ax_breadth.set_ylim(0, max(1, max_val * 1.30))
      for bar, value, percentage in zip(
          bars, breadth_values, [advance_pct, decline_pct, unchanged_pct]
      ):
        ax_breadth.annotate(
            f"{value} stocks\n{percentage:.1f}%",
            xy=(bar.get_x() + bar.get_width() / 2, bar.get_height()),
            xytext=(0, 7),
            textcoords="offset points",
            ha="center",
            va="bottom",
            fontsize=8,
            fontweight="bold",
        )
      ax_breadth.set_ylabel("Number of stocks", fontsize=9)
      ax_breadth.grid(axis="y", alpha=0.2)
      for spine in ["top", "right"]:
        ax_breadth.spines[spine].set_visible(False)

      # Panel 3
      ax_summary.set_title(
          "3. Sector Summary",
          fontsize=12,
          fontweight="bold",
          loc="left",
          pad=12,
      )
      ax_summary.set_facecolor("#f8f9fa")
      ax_summary.set_xticks([])
      ax_summary.set_yticks([])
      for spine in ax_summary.spines.values():
        spine.set_visible(True)
        spine.set_color("#dee2e6")
        spine.set_linewidth(1.2)
      ax_summary.text(
          0.05,
          0.88,
          "SECTOR SENTIMENT",
          transform=ax_summary.transAxes,
          fontsize=8,
          color="#6c757d",
          fontweight="bold",
      )
      ax_summary.text(
          0.05,
          0.74,
          sentiment,
          transform=ax_summary.transAxes,
          fontsize=15,
          color=sentiment_color,
          fontweight="bold",
      )
      ax_summary.text(
          0.95,
          0.75,
          f"{score:+.1f}/100",
          transform=ax_summary.transAxes,
          fontsize=12,
          color=sentiment_color,
          fontweight="bold",
          ha="right",
      )
      ax_summary.axhline(
          0.58, xmin=0.05, xmax=0.95, color="#dee2e6", linewidth=1
      )
      ax_summary.text(
          0.05,
          0.48,
          "KEY STATISTICS",
          transform=ax_summary.transAxes,
          fontsize=8,
          color="#6c757d",
          fontweight="bold",
      )
      ax_summary.text(
          0.05,
          0.36,
          f"Stocks analyzed: {total}\nAdvancers: {advancers}"
          f" ({advance_pct:.1f}%)\nDecliners: {decliners}"
          f" ({decline_pct:.1f}%)\nMedian return: {median_return:+.2f}%\nMean"
          f" return: {mean_return:+.2f}%",
          transform=ax_summary.transAxes,
          fontsize=9,
          linespacing=1.4,
          va="top",
      )

      # Panel 4
      ax_distribution.set_title(
          "4. Daily Return Distribution",
          fontsize=12,
          fontweight="bold",
          loc="left",
          pad=12,
      )
      display_returns = returns.clip(lower=-15, upper=15)
      ax_distribution.hist(
          display_returns,
          bins=30,
          color="#4c78a8",
          edgecolor="white",
          linewidth=0.7,
          alpha=0.88,
      )
      ax_distribution.axvline(
          0,
          color="#343a40",
          linestyle="--",
          linewidth=1.2,
          label="Zero return",
      )
      ax_distribution.axvline(
          median_return,
          color="#e03131",
          linewidth=1.8,
          label=f"Median: {median_return:+.2f}%",
      )
      ax_distribution.axvline(
          mean_return,
          color="#f08c00",
          linewidth=1.8,
          linestyle=":",
          label=f"Mean: {mean_return:+.2f}%",
      )
      ax_distribution.set_xlabel("Daily change (%)", fontsize=9)
      ax_distribution.set_ylabel("Number of stocks", fontsize=9)
      ax_distribution.legend(loc="upper right", frameon=False, fontsize=8)
      ax_distribution.grid(axis="y", alpha=0.2)
      for spine in ["top", "right"]:
        ax_distribution.spines[spine].set_visible(False)

      st.pyplot(fig)
      plt.close(fig)

  if auto_refresh:
    st.info("⏳ Auto-refreshing in 5 minutes...")
    time.sleep(300)
    st.cache_data.clear()
    if "df_results" in st.session_state:
      del st.session_state["df_results"]
    st.rerun()
else:
  st.info(
      "👈 Click Run Screener & Dashboard in the sidebar to fetch live data and"
      " generate the dashboard."
  )