import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime

# Page Configuration
st.set_page_config(
    page_title="Biotech Stock Screener & Sentiment Dashboard",
    page_icon="📈",
    layout="wide"
)

st.title("🧬 Biotech Stock Screener & Sentiment Dashboard")
st.markdown("Scans live biotech tickers via Yahoo Finance, ranks daily performance, and visualizes market sentiment.")

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

run_scan = st.sidebar.button("Run Screener & Dashboard", type="primary")

@st.cache_data(ttl=300)
def fetch_screener_data(ticker_list):
    import yfinance as yf
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
    st.subheader("📋 Stock Performance Table")
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

    # ---------------------------------------------------------------------------
    # RENDER 4-PANEL SENTIMENT DASHBOARD GRAPHS
    # ---------------------------------------------------------------------------
    st.markdown("---")
    st.subheader("📊 Sector Sentiment & Market Breadth Dashboard")

    # Clean and parse returns for the dashboard
    clean_df = df[df["Status"] == "OK"].copy()
    if not clean_df.empty and "Daily Change (%)" in clean_df.columns:
        returns = pd.to_numeric(clean_df["Daily Change (%)"], errors="coerce").dropna()
        
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

            # Sentiment calculation
            breadth_score = advance_pct - decline_pct
            return_score = float(np.clip(mean_return / 2.0 * 100, -100, 100))
            score = float(np.clip(0.70 * breadth_score + 0.30 * return_score, -100, 100))

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

            # Build Matplotlib figure
            fig = plt.figure(figsize=(16, 10), constrained_layout=True)
            gs = fig.add_gridspec(2, 2, height_ratios=[0.85, 1.15], width_ratios=[1.15, 1.0])

            ax_score = fig.add_subplot(gs[0, 0])
            ax_breadth = fig.add_subplot(gs[0, 1])
            ax_summary = fig.add_subplot(gs[1, 0])
            ax_distribution = fig.add_subplot(gs[1, 1])

            fig.suptitle("BIOTECH SECTOR SENTIMENT DASHBOARD", fontsize=18, fontweight="bold")

            for ax in [ax_score, ax_breadth, ax_summary, ax_distribution]:
                ax.set_facecolor("#ffffff")
                ax.set_axisbelow(True)

            # Panel 1: Sentiment Score
            ax_score.set_title("1. Composite Sentiment Score", fontsize=12, fontweight="bold", loc="left", pad=12)
            zone_colors = [(-100, -60, "#c92a2a"), (-60, -30, "#f08c00"), (-30, 0, "#ffd43b"),
                           (0, 30, "#94d82d"), (30, 60, "#2f9e44"), (60, 100, "#087f5b")]
            ax_score.barh(0, 200, left=-100, height=0.36, color="#f1f3f5", edgecolor="none")
            for left, right, color in zone_colors:
                ax_score.barh(0, right - left, left=left, height=0.36, color=color, alpha=0.22, edgecolor="none")
            ax_score.axvline(score, color=sentiment_color, linewidth=3, ymin=0.28, ymax=0.80)
            ax_score.scatter([score], [0], color=sentiment_color, edgecolor="white", linewidth=1.5, s=130, zorder=5)
            ax_score.axvline(0, color="#343a40", linewidth=1.2, linestyle="--")
            ax_score.set_xlim(-105, 105)
            ax_score.set_ylim(-0.8, 0.85)
            ax_score.set_yticks([])
            ax_score.set_xticks([-100, -60, -30, 0, 30, 60, 100])
            ax_score.set_xlabel(f"Score: {score:+.2f} / 100", fontsize=9, labelpad=8)
            ax_score.text(0.5, 0.94, sentiment, transform=ax_score.transAxes, ha="center", va="top", fontsize=12, fontweight="bold", color=sentiment_color)
            ax_score.grid(axis="x", alpha=0.15)
            for spine in ax_score.spines.values(): spine.set_visible(False)

            # Panel 2: Market Breadth
            ax_breadth.set_title("2. Market Breadth", fontsize=12, fontweight="bold", loc="left", pad=12)
            breadth_labels = ["Advancing", "Declining", "Unchanged"]
            breadth_values = [advancers, decliners, unchanged]
            bars = ax_breadth.bar(breadth_labels, breadth_values, color=["#2f9e44", "#e03131", "#adb5bd"], width=0.58, edgecolor="white", linewidth=1)
            max_val = max(breadth_values) if breadth_values else 1
            ax_breadth.set_ylim(0, max(1, max_val * 1.30))
            for bar, value, percentage in zip(bars, breadth_values, [advance_pct, decline_pct, unchanged_pct]):
                ax_breadth.annotate(f"{value} stocks\n{percentage:.1f}%", xy=(bar.get_x() + bar.get_width() / 2, bar.get_height()),
                                    xytext=(0, 7), textcoords="offset points", ha="center", va="bottom", fontsize=8, fontweight="bold")
            ax_breadth.set_ylabel("Number of stocks", fontsize=9)
            ax_breadth.grid(axis="y", alpha=0.2)
            for spine in ["top", "right"]: ax_breadth.spines[spine].set_visible(False)

            # Panel 3: Sector Summary Info Box
            ax_summary.set_title("3. Sector Summary", fontsize=12, fontweight="bold", loc="left", pad=12)
            ax_summary.set_facecolor("#f8f9fa")
            ax_summary.set_xticks([])
            ax_summary.set_yticks([])
            for spine in ax_summary.spines.values():
                spine.set_visible(True); spine.set_color("#dee2e6"); spine.set_linewidth(1.2)
            ax_summary.text(0.05, 0.88, "SECTOR SENTIMENT", transform=ax_summary.transAxes, fontsize=8, color="#6c757d", fontweight="bold")
            ax_summary.text(0.05, 0.74, sentiment, transform=ax_summary.transAxes, fontsize=15, color=sentiment_color, fontweight="bold")
            ax_summary.text(0.95, 0.75, f"{score:+.1f}/100", transform=ax_summary.transAxes, fontsize=12, color=sentiment_color, fontweight="bold", ha="right")
            ax_summary.axhline(0.58, xmin=0.05, xmax=0.95, color="#dee2e6", linewidth=1)
            ax_summary.text(0.05, 0.48, "KEY STATISTICS", transform=ax_summary.transAxes, fontsize=8, color="#6c757d", fontweight="bold")
            ax_summary.text(0.05, 0.36, f"Stocks analyzed: {total}\nAdvancers: {advancers} ({advance_pct:.1f}%)\nDecliners: {decliners} ({decline_pct:.1f}%)\nMedian return: {median_return:+.2f}%\nMean return: {mean_return:+.2f}%",
                            transform=ax_summary.transAxes, fontsize=9, linespacing=1.4, va="top")

            # Panel 4: Return Distribution
            ax_distribution.set_title("4. Daily Return Distribution", fontsize=12, fontweight="bold", loc="left", pad=12)
            display_returns = returns.clip(lower=-15, upper=15)
            ax_distribution.hist(display_returns, bins=30, color="#4c78a8", edgecolor="white", linewidth=0.7, alpha=0.88)
            ax_distribution.axvline(0, color="#343a40", linestyle="--", linewidth=1.2, label="Zero return")
            ax_distribution.axvline(median_return, color="#e03131", linewidth=1.8, label=f"Median: {median_return:+.2f}%")
            ax_distribution.axvline(mean_return, color="#f08c00", linewidth=1.8, linestyle=":", label=f"Mean: {mean_return:+.2f}%")
            ax_distribution.set_xlabel("Daily change (%)", fontsize=9)
            ax_distribution.set_ylabel("Number of stocks", fontsize=9)
            ax_distribution.legend(loc="upper right", frameon=False, fontsize=8)
            ax_distribution.grid(axis="y", alpha=0.2)
            for spine in ["top", "right"]: ax_distribution.spines[spine].set_visible(False)

            # Display plot in Streamlit
            st.pyplot(fig)
            plt.close(fig)
else:
    st.info("👈 Click **Run Screener & Dashboard** in the sidebar to fetch live data and generate the graphs.")