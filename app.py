from datetime import datetime
import time
import feedparser
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import streamlit as st
import yfinance as yf


# Page Configuration

st.set_page_config(
    page_title="Biotech Sentiment Monitor", page_icon="📈", layout="wide"
)


st.title("🧬 BSM")

st.markdown(
    "Scans live biotech tickers via Yahoo Finance, ranks daily performance, and"
    " visualizes market sentiment."
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


# Expanded Ticker List (593 Tickers from PDF, ordered alphabetically and placed horizontally)

DEFAULT_TICKERS = [
    "AAPG",
    "AARD",
    "ABCL",
    "ABEO",
    "ABOS",
    "ABSI",
    "ABUS",
    "ABVC",
    "ABVX",
    "ACAD",
    "ACET",
    "ACHV",
    "ACIU",
    "ACOG",
    "ACRS",
    "ACRV",
    "ACTU",
    "ACXP",
    "ADAG",
    "ADIL",
    "ADMA",
    "ADRX",
    "ADXN",
    "AEON",
    "AGEN",
    "AGIO",
    "AGMB",
    "AIM",
    "AKTS",
    "AKTX",
    "ALDX",
    "ALEC",
    "ALGS",
    "ALLO",
    "ALLR",
    "ALMS",
    "ALNY",
    "ALPS",
    "ALT",
    "ALXO",
    "ALZN",
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
    "ARTL",
    "ARTV",
    "ARVN",
    "ARWR",
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
    "AZTR",
    "BBIO",
    "BBLG",
    "BBOT",
    "BCAX",
    "BCDA",
    "BCTX",
    "BCYC",
    "BDRX",
    "BDTX",
    "BEAM",
    "BHVN",
    "BIVI",
    "BLRX",
    "BLSM",
    "BLTE",
    "BMEA",
    "BMRN",
    "BNTC",
    "BNTX",
    "BOLD",
    "BOLT",
    "BRTX",
    "BRVE",
    "BSEM",
    "BYSI",
    "CABA",
    "CADL",
    "CAI",
    "CALC",
    "CAMP",
    "CANF",
    "CAPR",
    "CBIO",
    "CBUS",
    "CCCC",
    "CDIO",
    "CDT",
    "CDXS",
    "CELC",
    "CELU",
    "CELZ",
    "CGEM",
    "CGEN",
    "CGON",
    "CGTX",
    "CHRS",
    "CING",
    "CLDI",
    "CLDX",
    "CLGN",
    "CLLS",
    "CLNN",
    "CLRB",
    "CLYM",
    "CMMB",
    "CMND",
    "CMPX",
    "CNSP",
    "CNSY",
    "CNTB",
    "CNTN",
    "CNTX",
    "CNXU",
    "COAG",
    "COCP",
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
    "CTMX",
    "CTNM",
    "CTXR",
    "CTY",
    "CUE",
    "CUVL",
    "CVKD",
    "CVM",
    "CYTK",
    "DARE",
    "DBVT",
    "DCOY",
    "DFTX",
    "DMAC",
    "DMRA",
    "DNA",
    "DNLI",
    "DNTH",
    "DRMA",
    "DRTS",
    "DRUG",
    "DSGN",
    "DTIL",
    "DWTX",
    "DYAI",
    "DYN",
    "EDIT",
    "EDSA",
    "EDVA",
    "EIKN",
    "ELAB",
    "ELDN",
    "ELOX",
    "ELTX",
    "ELVN",
    "ENGN",
    "ENLV",
    "ENSC",
    "ENTA",
    "ENTX",
    "ENVB",
    "EOCN",
    "EPRX",
    "EQ",
    "ERAS",
    "ERNA",
    "ESLA",
    "ETRA",
    "EVAX",
    "EVGN",
    "EVMN",
    "EWTX",
    "EXEL",
    "EXOZ",
    "EYPT",
    "FATE",
    "FBIO",
    "FBLG",
    "FDMT",
    "FENC",
    "FHTX",
    "FLNA",
    "FTH",
    "FTRE",
    "FULC",
    "GALT",
    "GANX",
    "GDTC",
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
    "HCWB",
    "HELP",
    "HIND",
    "HOWL",
    "HRMY",
    "HRTX",
    "HUMA",
    "HURA",
    "HYFT",
    "HYPD",
    "IAM",
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
    "IMNN",
    "IMRN",
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
    "IRLA",
    "IRON",
    "IVA",
    "IVVD",
    "JAGX",
    "JANX",
    "JAZZ",
    "JBIO",
    "JSPR",
    "JUNS",
    "KALA",
    "KAPA",
    "KARD",
    "KLRA",
    "KLRS",
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
    "LABT",
    "LBRX",
    "LCTX",
    "LEGN",
    "LENZ",
    "LEXX",
    "LGND",
    "LGVN",
    "LIMN",
    "LITS",
    "LKFT",
    "LNAI",
    "LONA",
    "LPCN",
    "LRMR",
    "LSTA",
    "LTGO",
    "LTRN",
    "LXEO",
    "LXRX",
    "LYEL",
    "MAIA",
    "MANE",
    "MAZE",
    "MBIO",
    "MBRX",
    "MBX",
    "MCRB",
    "MDGL",
    "MDWD",
    "MDXG",
    "MENS",
    "MESO",
    "MGNX",
    "MGTX",
    "MGX",
    "MIRM",
    "MIST",
    "MLEC",
    "MLTX",
    "MLYS",
    "MNKD",
    "MNOV",
    "MNPR",
    "MOLN",
    "MPLT",
    "MREO",
    "MRKR",
    "MRNA",
    "MRVI",
    "MSLE",
    "MTNB",
    "MTVA",
    "NAMS",
    "NAUT",
    "NBP",
    "NBTX",
    "NCEL",
    "NCNA",
    "NERV",
    "NEUP",
    "NGEN",
    "NGNE",
    "NIKI",
    "NKTR",
    "NKTX",
    "NMRA",
    "NNVC",
    "NRIX",
    "NRSN",
    "NRXP",
    "NRXS",
    "NTHI",
    "NTLA",
    "NTRB",
    "NUVB",
    "NVAX",
    "NVCT",
    "NXTC",
    "OABI",
    "OBIO",
    "OBX",
    "OCGN",
    "OCS",
    "OCUL",
    "ODTX",
    "OGEN",
    "OKUR",
    "OKYO",
    "OLMA",
    "OMER",
    "ONC",
    "ONCO",
    "ONCY",
    "ORIC",
    "ORKA",
    "ORMP",
    "OSTX",
    "OTLK",
    "OVID",
    "PALI",
    "PASG",
    "PBLS",
    "PBM",
    "PBYI",
    "PCSA",
    "PCVX",
    "PDSB",
    "PEPG",
    "PGEN",
    "PHAR",
    "PHAT",
    "PHIO",
    "PHVS",
    "PLRX",
    "PLRZ",
    "PLUR",
    "PLX",
    "PLYX",
    "PMCB",
    "PMN",
    "PMVP",
    "PPBT",
    "PPCB",
    "PRAX",
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
    "PVLA",
    "PYPD",
    "PYXS",
    "QNRX",
    "QNTM",
    "QTTB",
    "QURE",
    "RADX",
    "RANI",
    "RAPP",
    "RARE",
    "RCKT",
    "RCUS",
    "REGN",
    "REPL",
    "REVB",
    "RGNX",
    "RIGL",
    "RLAY",
    "RLMD",
    "RLYB",
    "RNA",
    "RNAC",
    "RNAZ",
    "RNTX",
    "RNXT",
    "ROIV",
    "RPRX",
    "RTSN",
    "RVMD",
    "RXRX",
    "RYTM",
    "RZLT",
    "SABS",
    "SANA",
    "SCNI",
    "SCTX",
    "SEER",
    "SEPN",
    "SER",
    "SGMT",
    "SGP",
    "SILO",
    "SION",
    "SKYE",
    "SLBT",
    "SLDB",
    "SLGL",
    "SLN",
    "SXTP",
    "TCRT",
    "SPRY",
    "TECH",
    "TRDA",
    "XCUR",
    "TRAX",
    "TIL",
    "TARA",
    "SRPT",
    "SVRA",
    "SRRK",
    "SPRC",
    "SPTX",
    "SLS",
    "SNTI",
    "STTK",
    "SLXN",
    "SNGX",
    "SPRO",
    "SPRB",
    "SYRE",
    "STOK",
    "SMMT",
    "SRZN",
    "STRO",
    "SNDX",
    "TNGX",
    "TARS",
    "TSHA",
    "TECX",
    "TLX",
    "TELO",
    "TPST",
    "TENX",
    "TNYA",
    "TVGN",
    "TGTX",
    "TOVX",
    "TLSA",
    "TNXP",
    "TVTX",
    "TRAW",
    "TRVI",
    "TRXB",
    "TCRX",
    "TTRX",
    "TVRD",
    "TWST",
    "TYRA",
    "UNCY",
    "UPB",
    "URGN",
    "VBIO",
    "VALN",
    "VNDA",
    "VERA",
    "VSTM",
    "VRXA",
    "VCEL",
    "VRCA",
    "VRTX",
    "VERU",
    "VCRE",
    "VKTX",
    "VIR",
    "VRAX",
    "VRDN",
    "VTGN",
    "VANI",
    "VIVS",
    "VOGX",
    "VOR",
    "VYGR",
    "VTVT",
    "WVE",
    "WHWK",
    "XFOR",
    "XBIT",
    "XNCR",
    "XBIO",
    "XENE",
    "XLO",
    "XRTX",
    "XTLB",
    "YARW",
    "YDES",
    "ZLAB",
    "ZBIO",
    "ZNTL",
    "ZVRA",
    "ZURA",
    "ZYME",
]


# Sidebar controls

st.sidebar.header("Screener Settings")

tickers_input = st.sidebar.text_area(
    "Edit Tickers (comma separated):",
    value=", ".join(DEFAULT_TICKERS),
    height=250,
)


# Parse tickers

tickers = [t.strip().upper() for t in tickers_input.split(",") if t.strip()]

tickers = list(dict.fromkeys(tickers))  # remove duplicates


run_scan = st.sidebar.button("Run Screener & Dashboard", type="primary")


# Touch-friendly toggle switch (3 min refresh)

auto_refresh = st.sidebar.toggle(
    "🔄 Enable 3 min Auto-Refresh",
    value=False,
    help="Automatically re-runs the screener every 3 minutes",
)


# Refresh Data button

refresh_btn = st.sidebar.button(
    "🔄 Refresh Data Now",
    help="Clears cache and fetches fresh live data immediately",
)


if refresh_btn:
  st.cache_data.clear()
  if "df_results" in st.session_state:
    del st.session_state["df_results"]
  st.rerun()


# Maintain execution state

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
            latest_volume = (
                snap.daily_bar.volume
                if snap.daily_bar
                else (snap.minute_bar.volume if snap.minute_bar else 0)
            )

            if prev_close and latest_price:
              alpaca_data[ticker] = pd.DataFrame({
                  "Close": [prev_close, latest_price],
                  "Volume": [latest_volume, latest_volume],
              })
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
  price_data = {}
  failed_tickers = []
  missing_tickers = []

  batch_size = 50
  for i in range(0, len(ticker_list), batch_size):
    batch = ticker_list[i : i + batch_size]
    try:
      data = yf.download(
          batch,
          period="3mo",
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

          if (
              hist.empty
              or "Close" not in hist.columns
              or "Volume" not in hist.columns
          ):
            missing_tickers.append(ticker)
            continue

          clean_hist = hist[["Close", "Volume"]].dropna(subset=["Close"])
          if len(clean_hist) < 2:
            missing_tickers.append(ticker)
            continue

          price_data[ticker] = clean_hist
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


@st.cache_data(ttl=300, show_spinner=False)
def fetch_ibb_data():
  try:
    ibb = yf.Ticker("IBB")
    hist = ibb.history(period="1mo")
    if len(hist) >= 5:
      prev_close = float(hist["Close"].iloc[-2])
      latest_close = float(hist["Close"].iloc[-1])
      change = latest_close - prev_close
      pct_change = (change / prev_close) * 100

      high = hist["High"]
      low = hist["Low"]
      close = hist["Close"]
      vol = hist["Volume"]

      range_hl = high - low
      multiplier = ((close - low) - (high - close)) / range_hl.replace(0, np.nan)
      multiplier = multiplier.fillna(0)

      mf_volume = multiplier * vol
      cmf_5 = float(mf_volume.tail(5).sum() / vol.tail(5).sum())

      price_5d_change = float(
          ((hist["Close"].iloc[-1] - hist["Close"].iloc[-5]) / hist["Close"].iloc[-5]) * 100
      )

      if price_5d_change < 0 and cmf_5 >= 0:
        divergence_info = "Bullish Div"
      elif price_5d_change > 0 and cmf_5 < 0:
        divergence_info = "Bearish Div"
      else:
        divergence_info = "Neutral"

      return {
          "price": latest_close,
          "change": change,
          "pct_change": pct_change,
          "cmf": cmf_5,
          "price_5d_change": price_5d_change,
          "divergence_info": divergence_info,
          "status": "OK",
      }
  except Exception:
    pass
  return {"status": "Error"}


@st.cache_data(ttl=300, show_spinner=False)
def fetch_vxn_data():
  try:
    vxn = yf.Ticker("^VXN")
    hist = vxn.history(period="1mo")
    if len(hist) >= 2:
      prev_close = float(hist["Close"].iloc[-2])
      latest_close = float(hist["Close"].iloc[-1])
      change = latest_close - prev_close
      pct_change = (change / prev_close) * 100

      return {
          "price": latest_close,
          "change": change,
          "pct_change": pct_change,
          "status": "OK",
      }
  except Exception:
    pass
  return {"status": "Error"}


@st.cache_data(ttl=300, show_spinner=False)
def fetch_stocktitan_combined_rss():
  """Fetches entries from both StockTitan Clinical Trials and FDA Approval RSS feeds, extracts tickers, and combines them."""
  rss_urls = [
      ("https://www.stocktitan.net/rss-clinical-trials", "CLINICAL TRIAL"),
      ("https://www.stocktitan.net/rss-fda-approvals", "FDA APPROVAL")
  ]
  entries_list = []
  
  for rss_url, feed_tag in rss_urls:
    try:
      feed = feedparser.parse(rss_url)
      for entry in feed.entries:
        title = entry.get("title", "No Title")
        link = entry.get("link", "#")
        published = entry.get("published", "")
        published_parsed = entry.get("published_parsed", None)
        
        # Convert published_parsed to timestamp for proper sorting if available
        timestamp = time.mktime(published_parsed) if published_parsed else 0
        
        ticker = "MARKET"
        desc_part = title
        
        if "|" in title:
          parts = title.rsplit("|", 1)
          desc_part = parts[0].strip()
          right_part = parts[1].strip()
          tokens = right_part.split()
          if tokens:
            potential_ticker = tokens[0].strip().upper()
            if 1 <= len(potential_ticker) <= 6 and potential_ticker.isalnum():
              ticker = potential_ticker
        elif ":" in title:
          parts = title.split(":", 1)
          potential_ticker = parts[0].strip().upper()
          if 1 <= len(potential_ticker) <= 6 and potential_ticker.isalnum():
            ticker = potential_ticker
            desc_part = parts[1].strip()

        entries_list.append({
            "ticker": ticker,
            "description": desc_part,
            "link": link,
            "published": published,
            "timestamp": timestamp,
            "feed_tag": feed_tag
        })
    except Exception:
      pass

  # Sort combined entries by timestamp descending (newest first)
  entries_list = sorted(entries_list, key=lambda x: x["timestamp"], reverse=True)
  return entries_list


if st.session_state.get("is_running", False):
  with st.spinner("Fetching live market data..."):
    price_data, failed_tickers = fetch_screener_data(
        tickers, alpaca_api_key, alpaca_secret_key
    )
    ibb_info = fetch_ibb_data()
    vxn_info = fetch_vxn_data()
    clinical_rss_entries = fetch_stocktitan_combined_rss()

  results = []
  for ticker in tickers:
    overview_url = f"https://www.stocktitan.net/overview/{ticker}/"
    
    if ticker not in price_data:
      results.append({
          "Ticker": ticker,
          "Previous Close ($)": None,
          "Latest Close ($)": None,
          "Change ($)": None,
          "Daily Change (%)": None,
          "RVOL": None,
          "Overview": overview_url,
          "Status": "No data / insufficient history",
      })
      continue

    df_hist = price_data[ticker]
    prices = df_hist["Close"].dropna()
    volumes = df_hist["Volume"].fillna(0)

    if len(prices) < 2:
      results.append({
          "Ticker": ticker,
          "Previous Close ($)": None,
          "Latest Close ($)": None,
          "Change ($)": None,
          "Daily Change (%)": None,
          "RVOL": None,
          "Overview": overview_url,
          "Status": "Insufficient history",
      })
      continue

    previous_close = float(prices.iloc[-2])
    latest_close = float(prices.iloc[-1])
    latest_volume = float(volumes.iloc[-1])

    if len(volumes) > 1:
      avg_volume = float(volumes.iloc[:-1].tail(63).mean())
    else:
      avg_volume = 0

    rvol = (
        (latest_volume / avg_volume) if avg_volume > 0 else float("nan")
    )

    if previous_close == 0:
      results.append({
          "Ticker": ticker,
          "Previous Close ($)": previous_close,
          "Latest Close ($)": latest_close,
          "Change ($)": None,
          "Daily Change (%)": None,
          "RVOL": rvol,
          "Overview": overview_url,
          "Status": "Invalid previous close",
      })
      continue

    change = latest_close - previous_close
    pct_change = (change / previous_close) * 100

    results.append({
        "Ticker": ticker,
        "Previous Close ($)": previous_close,
        "Latest Close ($)": latest_close,
        "Change ($)": change,
        "Daily Change (%)": pct_change,
        "RVOL": rvol,
        "Overview": overview_url,
        "Status": "OK",
    })

  df = pd.DataFrame(results)
  df = df.sort_values(
      by="Daily Change (%)", ascending=False, na_position="last"
  ).reset_index(drop=True)
  df.insert(0, "Rank", range(1, len(df) + 1))

  st.session_state["df_results"] = df
  st.session_state["failed_tickers"] = failed_tickers
  st.session_state["ibb_info"] = ibb_info
  st.session_state["vxn_info"] = vxn_info
  st.session_state["clinical_rss_entries"] = clinical_rss_entries

  df = st.session_state["df_results"]
  failed_tickers = st.session_state["failed_tickers"]
  ibb_info = st.session_state.get("ibb_info", {"status": "Error"})
  vxn_info = st.session_state.get("vxn_info", {"status": "Error"})
  clinical_rss_entries = st.session_state.get("clinical_rss_entries", [])

  # Metrics summary

  valid = df[df["Status"] == "OK"]

  col1, col2, col3 = st.columns(3)

  col1.metric("Total Scanned", len(tickers))

  col2.metric("Valid Data", len(valid))

  col3.metric("Errors / Missing", len(failed_tickers))


  if not valid.empty:
    top = valid.iloc[0]
    bottom = valid.iloc[-1]
    st.success(
        f"🚀 **Top Gainer:** {top['Ticker']} ({top['Daily Change (%)']:+.2f}%) &"
        f" 📉 **Bottom Performer:** {bottom['Ticker']}"
        f" ({bottom['Daily Change (%)']:+.2f}%)"
    )


  # Display interactive dataframe (with index hidden)

  st.subheader("📋 Stock Performance Table")

  st.dataframe(
      df.style.format(
          {
              "Previous Close ($)": "{:.4f}",
              "Latest Close ($)": "{:.4f}",
              "Change ($)": "{:+.4f}",
              "Daily Change (%)": "{:+.2f}%",
              "RVOL": "{:.2f}x",
          },
          na_rep="N/A",
      ),
      column_config={
          "Overview": st.column_config.LinkColumn(
              "Overview",
              help="Click to view StockTitan overview",
              max_chars=100,
              display_text="Click here",
          )
      },
      use_container_width=True,
      hide_index=True,
  )


  # CSV Download Button

  timestamp = datetime.now().strftime("%Y%m%d_%H%M")

  csv = df.to_csv(index=False).encode("utf-8")

  st.download_button(
      label="📥 Download Results as CSV",
      data=csv,
      file_name=f"biotech_daily_screener_{timestamp}.csv",
      mime="text/csv",
  )


  st.markdown("---")

  # ---------------------------------------------------------------------------
  # NATIVE SCROLLABLE CONTAINER FOR COMBINED STOCKTITAN RSS FEEDS
  # ---------------------------------------------------------------------------
  st.markdown("### 🔬 StockTitan Clinical Trials & FDA Approvals RSS Feed")
  st.markdown(
      "<p style='font-size:12px; color:#6c757d; margin-bottom:15px;'>"
      "Combined live feed tracking real-time clinical trial announcements and FDA approval updates."
      "</p>",
      unsafe_allow_html=True
  )
  
  # Check for new items compared to previously stored session entries and trigger the jingle bells sound alert once
  current_entry_links = {entry['link'] for entry in clinical_rss_entries}
  if "last_seen_rss_links" not in st.session_state:
    st.session_state["last_seen_rss_links"] = current_entry_links
    has_new_rss_cards = False
  else:
    new_links = current_entry_links - st.session_state["last_seen_rss_links"]
    has_new_rss_cards = len(new_links) > 0
    if has_new_rss_cards:
      st.session_state["last_seen_rss_links"] = current_entry_links

  if has_new_rss_cards:
    audio_html = """
    <audio autoplay>
      <source src="https://actions.google.com/sounds/v1/cartoon/jingle_bells.ogg" type="audio/ogg">
    </audio>
    """
    st.markdown(audio_html, unsafe_allow_html=True)

  # Map advancing stock tickers with daily change > 5% to their change percentage
  advancing_tickers_pct = df[
      (df["Status"] == "OK") & (df["Daily Change (%)"] > 5.0)
  ].set_index("Ticker")["Daily Change (%)"].to_dict()

  with st.container(height=400):
    if clinical_rss_entries:
      for entry in clinical_rss_entries:
        ticker = entry['ticker']
        description = entry['description']
        link = entry['link']
        published = entry['published']
        feed_tag = entry['feed_tag']
        
        # Determine background color gradient: the higher above 5%, the deeper green the card
        if ticker in advancing_tickers_pct:
          change_pct = advancing_tickers_pct[ticker]
          if change_pct >= 20.0:
            card_bg = "#6ee7b7"  # Deep vivid green (20%+)
          elif change_pct >= 15.0:
            card_bg = "#86efac"  # Medium-dark green (15% - 20%)
          elif change_pct >= 10.0:
            card_bg = "#a7f3d0"  # Medium green (10% - 15%)
          else:
            card_bg = "#d1fae5"  # Soft light green (5% - 10%)
        else:
          card_bg = "#ffffff"     # Default white body background
        
        border_color = "#10b981" if feed_tag == "FDA APPROVAL" else "#3b82f6"    # Green accent for FDA, Blue for Clinical
        
        pub_badge = f"<span style='background-color: #f1f3f5; color: #495057; padding: 2px 6px; border-radius: 4px; font-size: 9px; float: right;'>🕒 {published}</span>" if published else ""
        
        card_html = f"""
        <div style="
            background-color: {card_bg}; 
            border: 1px solid #e2e8f0; 
            border-left: 4px solid {border_color}; 
            padding: 12px 14px; 
            margin-bottom: 12px; 
            border-radius: 6px; 
            box-shadow: 0 1px 2px rgba(0,0,0,0.03);
        ">
            <div style="margin-bottom: 6px;">
                {pub_badge}
                <span style="font-size: 11px; font-weight: 700; color: #1e40af; letter-spacing: 0.5px;">[{ticker}] {feed_tag}</span>
            </div>
            <div style="font-size: 12px; font-weight: 500; line-height: 1.4;">
                <a href="{link}" target="_blank" style="text-decoration: none; color: #1f2937;">{description}</a>
            </div>
        </div>
        """
        st.markdown(card_html, unsafe_allow_html=True)
    else:
      st.markdown(
          "<p style='font-size: 11px; color: #6c757d;'>No entries found or unable to fetch the RSS feeds.</p>",
          unsafe_allow_html=True
      )

  st.markdown("---")

  # ---------------------------------------------------------------------------

  # HORIZONTAL SWIPE TAB CONTAINER (MACRO INFOS VS DASHBOARD IMAGE SIDE-BY-SIDE)

  # ---------------------------------------------------------------------------

  tab_macro_info, tab_dashboard = st.tabs([
      "📈 Macro & Sector Indicators",
      "📊 Sentiment Dashboard Visuals",
  ])


  # SLIDE 1: MACRO INFOS SECTION AS IT WAS ORIGINALLY

  with tab_macro_info:
    if ibb_info.get("status") == "OK":
      st.metric(
          "IBB (iShares Biotechnology ETF)",
          f"${ibb_info['price']:.2f}",
          f"{ibb_info['change']:+.2f} ({ibb_info['pct_change']:+.2f}%)",
      )

      # 5D CMF and Price / CMF Divergence Info Side-by-Side metrics

      ind_col1, ind_col2 = st.columns(2)

      cmf_val = ibb_info["cmf"]
      divergence_info = ibb_info["divergence_info"]

      cmf_status = (
          "Buying Pressure" if cmf_val >= 0 else "Selling Pressure"
      )
      cmf_delta_color = "normal" if cmf_val >= 0 else "inverse"

      with ind_col1:
        st.metric(
            "Chaikin Money Flow (5D)",
            f"{cmf_val:+.3f}",
            delta=cmf_status,
            delta_color=cmf_delta_color,
        )

      with ind_col2:
        if "Bullish" in divergence_info:
          div_delta_color = "normal"
        elif "Bearish" in divergence_info:
          div_delta_color = "inverse"
        else:
          div_delta_color = "off"

        st.metric(
            "IBB Price / CMF 5D Divergence",
            divergence_info,
            delta=f"5D Price: {ibb_info['price_5d_change']:+.2f}%",
            delta_color=div_delta_color,
        )

      # VXN Info Display under Divergence

      if vxn_info.get("status") == "OK":
        vxn_val = vxn_info["price"]
        vxn_change = vxn_info["change"]
        vxn_pct = vxn_info["pct_change"]

        vxn_delta_color = "inverse" if vxn_change > 0 else "normal"

        st.metric(
            "CBOE NASDAQ Volatility Index (^VXN)",
            f"{vxn_val:.2f}",
            f"{vxn_change:+.2f} ({vxn_pct:+.2f}%)",
            delta_color=vxn_delta_color,
        )
      else:
        st.warning(
            "Could not fetch live CBOE NASDAQ Volatility (^VXN) data from Yahoo"
            " Finance."
        )

      # Rewritten Strategy Logic explanatory text

      st.markdown(
          "<p style='font-size:11px; color:#6c757d; margin-top:-5px;"
          " margin-bottom:15px;'>💡 <b>Strategy Logic:</b> Dynamic"
          " multi-factor regime filter leveraging IBB sector momentum,"
          " institutional liquidity via CMF flow, and ^VXN volatility"
          " boundaries. <b>Long Bias:</b> Activated during positive"
          " institutional accumulation (CMF > 0 or Bullish Divergence) combined"
          " with subdued or downward-trending volatility (^VXN), favoring"
          " aggressive small-to-mid cap biotech momentum plays."
          " <b>Short/Hedge Bias:</b> Triggered under heavy distribution (CMF <"
          " 0 or Bearish Divergence) paired with expanding ^VXN volatility,"
          " indicating macro risk-off pressure and favoring defensive capital"
          " preservation or tactical short exposure. <b>Execution Filter:</b>"
          " The composite sentiment score and breadth metrics below act as the"
          " final mandatory gateway to filter out false breakouts before order"
          " routing.</p>",
          unsafe_allow_html=True,
      )
    else:
      st.warning("Could not fetch live IBB ETF data from Yahoo Finance.")


  # SLIDE 2: SECTOR SENTIMENT DASHBOARD IMAGE / VISUALS

  with tab_dashboard:
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
        ax_score.set_xlabel(
            f"Score: {score:+.2f} / 100", fontsize=9, labelpad=8
        )
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


  # Auto-refresh logic

  if auto_refresh:
    st.info("⏳ Auto-refreshing in 3 minute...")
    time.sleep(180)
    st.cache_data.clear()
    if "df_results" in st.session_state:
      del st.session_state["df_results"]
    st.rerun()

else:
  st.info(
      "👈 Click Run Screener & Dashboard in the sidebar to fetch live data and"
      " generate the graphs."
  )