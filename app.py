import streamlit as st
import pandas as pd
import yfinance as yf
from datetime import datetime

# Page Configuration
st.set_page_config(
    page_title="Biotech Stock Screener",
    page_icon="📈",
    layout="wide"
)

st.title("🧬 Biotech Stock Screener — Daily % Change")
st.markdown("Scans a curated list of biotech tickers via Yahoo Finance, ranks them from biggest gainer to biggest loser, and lets you download the results.")

# Default Ticker List
DEFAULT_TICKERS = [
    "ACAD", "ACHV", "ACRS", "ADMA", "AGIO", "ALKS", "ALMS",
    "ALNY", "ALT", "ALVO", "ALXO", "ANVS", "ARDX", "ARQT",
    "ASMB", "ASND", "BEAM", "BHVN", "BIIB", "BNTX", "CADL",
    "CAI", "CCCC", "CGON", "COGT", "CORT", "CRBU", "CRSP",
    "CRVS", "CTMX", "CUE", "CYTK", "DFTX", "DNA", "DNLI",
    "DRUG", "DTIL", "DYN", "ELTX", "ELVN", "ENTA", "ERAS",
    "FDMT", "FTRE", "GHRS", "GLSI", "GYRE", "HALO", "IBRX",
    "IKT", "IMCR", "IMRX", "INBX", "INO", "INVA", "IOVA",
    "IRD", "IVVD", "KYMR", "KYTX", "LENZ", "MAZE", "MIRM",
    "MLYS", "MRK", "NBIX", "NMRA", "NTLA", "NTRB", "NUVL",
    "NVS", "OABI", "OMER", "OTLK", "OVID", "PDSB", "PEPG",
    "PGEN", "PRME", "PRTA", "PTCT", "PTGX", "PVLA", "RAPP",
    "RARE", "REPL", "RLMD", "ROIV", "RVMD", "RXRX", "SANA",
    "SEPN", "SLDB", "SLN", "SLS", "SRPT", "STTK", "TARA",
    "TENX", "TNGX", "TRDA", "TRVI", "UPB", "VIR", "VOR",
    "VRTX", "XENE", "ZBIO", "ZNTL"
]

# Sidebar controls
st.sidebar.header("Screener Settings")
tickers_input = st.sidebar.text_area(
    "Edit Tickers (comma separated):",
    value=", ".join(DEFAULT_TICKERS),
    height=300
)

# Parse tickers
tickers = [t.strip().upper() for t in tickers_input.split(",") if t.strip()]
tickers = list(dict.fromkeys(tickers)) # remove duplicates

run_scan = st.sidebar.button("Run Screener", type="primary")

@st.cache_data(ttl=300) # Cache data for 5 minutes to avoid rate limits
def fetch_screener_data(ticker_list):
    price_data = {}
    failed_tickers = []

    for ticker in ticker_list:
        try:
            hist = yf.Ticker(ticker).history(
                period="5d",
                interval="1d",
                auto_adjust=False,
                raise_errors=True
            )

            if hist.empty or "Close" not in hist.columns:
                failed_tickers.append((ticker, "No data returned"))
                continue

            prices = hist["Close"].dropna()
            if len(prices) < 2:
                failed_tickers.append((ticker, "Insufficient daily price history"))
                continue

            price_data[ticker] = prices
        except Exception as e:
            failed_tickers.append((ticker, type(e).__name__))
            
    return price_data, failed_tickers

if run_scan or "df_results" in st.session_state:
    if run_scan:
        with st.spinner(f"Scanning {len(tickers)} unique tickers from Yahoo Finance..."):
            price_data, failed_tickers = fetch_screener_data(tickers)

            results = []
            for ticker in tickers:
                if ticker not in price_data:
                    results.append({
                        "Ticker": ticker,
                        "Previous Close ($)": None,
                        "Latest Close ($)": None,
                        "Change ($)": None,
                        "Daily Change (%)": None,
                        "Status": "No data / insufficient history"
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
                        "Status": "Invalid previous close"
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
                    "Status": "OK"
                })

            df = pd.DataFrame(results)
            df = df.sort_values(by="Daily Change (%)", ascending=False, na_position="last").reset_index(drop=True)
            df.insert(0, "Rank", range(1, len(df) + 1))
            
            st.session_state["df_results"] = df
            st.session_state["failed_tickers"] = failed_tickers

    df = st.session_state["df_results"]
    failed_tickers = st.session_state["failed_tickers"]

    # Metrics summary
    valid = df[df["Status"] == "OK"]
    col1, col2, col3 = st.columns(3)
    col1.metric("Total Scanned", len(tickers))
    col2.metric("Valid Data", len(valid))
    col3.metric("Errors / Missing", len(failed_tickers))

    if not valid.empty:
        top = valid.iloc[0]
        bottom = valid.iloc[-1]
        st.success(f"🚀 **Top Gainer:** {top['Ticker']} ({top['Daily Change (%)']:+.2f}%) | 📉 **Bottom Performer:** {bottom['Ticker']} ({bottom['Daily Change (%)']:+.2f}%)")

    # Display interactive dataframe
    st.dataframe(
        df.style.format({
            "Previous Close ($)": "{:.4f}",
            "Latest Close ($)": "{:.4f}",
            "Change ($)": "{:+.4f}",
            "Daily Change (%)": "{:+.2f}%"
        }, na_rep="N/A"),
        use_container_width=True
    )

    # CSV Download Button
    timestamp = datetime.now().strftime("%Y%m%d_%H%M")
    csv = df.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="📥 Download Results as CSV",
        data=csv,
        file_name=f"biotech_daily_screener_{timestamp}.csv",
        mime="text/csv",
    )
else:
    st.info("👈 Click **Run Screener** in the sidebar to fetch live data.")