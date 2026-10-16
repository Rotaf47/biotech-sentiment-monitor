import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime
import time

# Page Configuration
st.set_page_config(
    page_title="Biotech Sentiment Monitor",
    page_icon="📈",
    layout="wide"
)

st.title("🧬 BSM")
st.markdown("Scans live biotech tickers via Yahoo Finance, ranks daily performance, and visualizes market sentiment.")

# Expanded Ticker List
DEFAULT_TICKERS = [
    "AAPG", "AARD", "ABCL", "ABEO", "ABOS", "ABSI", "ABTS", "ABUS", "ABVC", "ABVX", "ACAD", "ACET", "ACHV", "ACIU", "ACLX", "ACOG", "ACRS", "ACRV", "ACTU", "ADAG", "ADMA", "ADRX", "ADUS", "AEMD", "AEON", "AGEN", "AGIO", "AGMB", "AKTS", "AKTX", "ALDX", "ALEC", "ALGS", "ALKS", "ALLO", "ALLR", "ALMS", "ALNY", "ALPS", "ALT", "ALVO", "ALXO", "ALZN", "AMLX", "ANAB", "ANIX", "ANL", "ANNX", "ANRO", "ANTX", "ANVS", "APLM", "APMD", "APRE", "APVO", "ARCT", "ARDX", "ARGX", "ARMP", "ARQT", "ARTV", "ARVN", "ARWR", "ASBP", "ASMB", "ASND", "ATHE", "ATNM", "ATOS", "ATRA", "ATTO", "ATYR", "AUPH", "AURA", "AUTL", "AVBP", "AVIR", "AVLN", "AVTX", "AVXL", "AXSM", "AYTU", "BBIO", "BBLG", "BBOT", "BCAX", "BCDA", "BCRX", "BCTX", "BCYC", "BDSX", "BDTX", "BEAM", "BGMS", "BHVN", "BIIB", "BIO", "BIOA", "BIOX", "BJDX", "BLRX", "BLSM", "BLTE", "BMEA", "BMRN", "BNTC", "BNTX", "BOLD", "BRTX", "BRVE", "BSEM", "BYSI", "CABA", "CADL", "CAI", "CAMP", "CAPR", "CBIO", "CBUS", "CCCC", "CDNA", "CDXS", "CELC", "CELU", "CELZ", "CGEM", "CGON", "CGTX", "CHRS", "CING", "CLDX", "CLNN", "CLPT", "CLRB", "CLRO", "CLYM", "CMPX", "CNSP", "CNSY", "CNTB", "CNTN", "CNTX", "CNXU", "COAG", "COCP", "CODX", "COGT", "CORT", "COYA", "CRBP", "CRBU", "CRDF", "CRIS", "CRMD", "CRSP", "CRVO", "CRVS", "CSBR", "CTKB", "CTMX", "CTNM", "CTOR", "CTXR", "CUE", "CUVL", "CVKD", "CVM", "CYPH", "CYRX", "CYTK", "DARE", "DBVT", "DFTX", "DMAC", "DMRA", "DNA", "DNLI", "DNTH", "DRTS", "DRUG", "DSGN", "DSTX", "DTIL", "DWTX", "DYAI", "DYN", "EBS", "ECOR", "EDIT", "EDSA", "EIKN", "ELOX", "ELTX", "ELVN", "ENGN", "ENSC", "ENTA", "ENTX", "EPRX", "EQ", "ERAS", "ERNA", "ESLA", "ETRA", "EVAX", "EVMN", "EWTX", "EXEL", "EXOZ", "EYPT", "FATE", "FBIO", "FDMT", "FDTX", "FEMY", "FENC", "FERA", "FHTX", "FLNA", "FTH", "FTRE", "FULC", "GALT", "GANX", "GENB", "GERN", "GHRS", "GLSI", "GLUE", "GMAB", "GNLX", "GNPX", "GOSS", "GOVX", "GPCR", "GRCE", "GRDX", "GRI", "GTBP", "GUTS", "GYRE", "HALO", "HBIO", "HELP", "HIND", "HOWL", "HRMY", "HRTX", "HUMA", "HURA", "HYBX", "HYFT", "HYPD", "IBIO", "IBO", "IBRX", "ICCC", "ICU", "IDYA", "IFRX", "IGC", "IKT", "IMA", "IMCR", "IMMP", "IMMX", "IMNM", "IMRX", "IMTX", "IMUX", "IMVT", "INAB", "INBX", "INCY", "INDP", "INKT", "INMB", "INO", "INSM", "INTS", "INVA", "IONS", "IOVA", "IPHA", "IPSC", "IRD", "IRON", "IVA", "IVVD", "JAGX", "JANX", "JAZZ", "JBIO", "JSPR", "KARD", "KLRA", "KLRS", "KNSA", "KOD", "KPRX", "KPTI", "KROS", "KRRO", "KRSA", "KRYS", "KTTA", "KURA", "KYMR", "KYNB", "KYTX", "KZIA", "LBRX", "LCTX", "LEGN", "LENZ", "LGND", "LGVN", "LIMN", "LIQT", "LITS", "LKFT", "LNAI", "LONA", "LPCN", "LQDA", "LRMR", "LTGO", "LTRN", "LUNG", "LXEO", "LXRX", "LYEL", "MAIA", "MANE", "MAZE", "MBIO", "MBX", "MCRB", "MDGL", "MDWD", "MDXG", "MENS", "MESO", "MGNX", "MGRX", "MGX", "MIRM", "MIST", "MLYS", "MNKD", "MNOV", "MNPR", "MOLN", "MREO", "MRNA", "MRVI", "MSLE", "MYCN", "MYGN", "NAMS", "NAUT", "NBIS", "NBIX", "NBP", "NBTX", "NCEL", "NCNA", "NERV", "NEUP", "NGEN", "NGNE", "NKTR", "NKTX", "NMRA", "NNVC", "NRIX", "NRXP", "NRXS", "NTHI", "NTLA", "NTRB", "NTRP", "NUVB", "NVCT", "NXTC", "OABI", "OBIO", "OBX", "OCGN", "OCS", "OCUL", "ODTX", "OKUR", "OKYO", "OLMA", "OMER", "ONC", "ONCO", "ONCY", "OPAL", "ORGO", "ORIC", "ORKA", "ORMP", "OSTX", "OTLK", "OXBR", "PACB", "PALI", "PBLS", "PBYI", "PCVX", "PDSB", "PEPG", "PGEN", "PHAR", "PHAT", "PHIO", "PHVS", "PLRX", "PLUR", "PLX", "PLYX", "PMN", "PMVP", "PRAX", "PRFX", "PRLD", "PRME", "PROK", "PRQR", "PRTA", "PTCT", "PTGX", "PTHS", "PTN", "PULM", "PURR", "PVLA", "PYPD", "PYXS", "QCLR", "QDEL", "QGEN", "QNRX", "QNTM", "QTRX", "QTTB", "QURE", "RADX", "RANI", "RAPP", "RARE", "RCEL", "RCKT", "RCUS", "REGN", "REPL", "REVB", "RGEN", "RGNX", "RGTX", "RIGL", "RKDA", "RLAY", "RLMD", "RLYB", "RNA", "RNAC", "RNAZ", "RNTX", "RNXT", "ROIV", "RPID", "RPRX", "RTSN", "RVMD", "RXRX", "RYTM", "SABS", "SANA", "SBFM", "SCTX", "SCYX", "SEER", "SEPN", "SER", "SERA", "SGMT", "SGP", "SHPH", "SIGA", "SILO", "SION", "SMMT", "SMTI", "SNDX", "SNGX", "SNTI", "SOPH", "SORA", "SPRB", "SPRX", "SPRY", "SPTX", "SRPT", "SRRK", "SRZN", "STOK", "STRO", "STTK", "SUSB", "SVRA", "SXTC", "SYRE", "TARA", "TARS", "TCRT", "TCRX", "TECH", "TECX", "TELO", "TENX", "TGTX", "THRD", "TIL", "TLSA", "TLSI", "TLX", "TNGX", "TNXP", "TNYA", "TPST", "TRAX", "TRDA", "TRVI", "TRXB", "TSHA", "TTRX", "TVGN", "TVRD", "TVTX", "TWST", "TXG", "TYRA", "UNCY", "UPB", "URGN", "VALN", "VANI", "VCEL", "VCRE", "VCYT", "VERA", "VERU", "VIGL", "VIR", "VKTX", "VNDA", "VOGX", "VOR", "VRAX", "VRCA", "VRDN", "VRXA", "VS", "VSTM", "VTGN", "VTVT", "VYGR", "WHWK", "WVE", "XBIO", "XBIT", "XCUR", "XENE", "XFOR", "XLO", "XNCR", "XRTX", "YARW", "YDES", "ZBIO", "ZGN", "ZLAB", "ZNTL", "ZURA", "ZVRA", "ZYBT", "ZYME"
]

# Sidebar controls
st.sidebar.header("Screener Settings")
tickers_input = st.sidebar.text_area(
    "Edit Tickers (comma separated):",
    value=", ".join(DEFAULT_TICKERS),
    height=250
)

# Parse tickers
tickers = [t.strip().upper() for t in tickers_input.split(",") if t.strip()]
tickers = list(dict.fromkeys(tickers)) # remove duplicates

run_scan = st.sidebar.button("Run Screener & Dashboard", type="primary")

# Touch-friendly toggle switch (5 min refresh)
auto_refresh = st.sidebar.toggle("🔄 Enable 5 min Auto-Refresh", value=False, help="Automatically re-runs the screener every 5 minutes")

# Refresh Data button
refresh_btn = st.sidebar.button("🔄 Refresh Data Now", help="Clears cache and fetches fresh live data immediately")

if refresh_btn:
    st.cache_data.clear()
    if "df_results" in st.session_state:
        del st.session_state["df_results"]
    st.rerun()

# Maintain execution state
if run_scan:
    st.session_state["is_running"] = True

@st.cache_data(ttl=300, show_spinner=False)
def fetch_screener_data(ticker_list):
    import yfinance as yf
    price_data = {}
    failed_tickers = []
    
    # Process in optimized batches of 50 to prevent memory spikes and timeouts
    batch_size = 50
    for i in range(0, len(ticker_list), batch_size):
        batch = ticker_list[i:i + batch_size]
        try:
            data = yf.download(
                batch,
                period="5d",
                interval="1d",
                auto_adjust=False,
                group_by="ticker",
                threads=True,
                progress=False
            )
            
            for ticker in batch:
                try:
                    if len(batch) == 1:
                        hist = data
                    else:
                        if ticker in data.columns.levels[0]:
                            hist = data[ticker]
                        else:
                            failed_tickers.append((ticker, "No data returned"))
                            continue
                    
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
        except Exception as e:
            for ticker in batch:
                failed_tickers.append((ticker, type(e).__name__))
            
    return price_data, failed_tickers

if st.session_state.get("is_running", False):
    with st.spinner("Fetching live market data..."):
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
        st.success(f"🚀 **Top Gainer:** {top['Ticker']} ({top['Daily Change (%)']:+.2f}%) & 📉 **Bottom Performer:** {bottom['Ticker']} ({bottom['Daily Change (%)']:+.2f}%)")

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

            # Panel 1
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

            # Panel 2
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

            # Panel 3
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

            # Panel 4
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

            st.pyplot(fig)
            plt.close(fig)

    # If auto-refresh toggle is active, sleep for 300 seconds (5 min) and trigger rerun
    if auto_refresh:
        st.info("⏳ Auto-refreshing in 5 minutes...")
        time.sleep(300)
        st.cache_data.clear()
        if "df_results" in st.session_state:
            del st.session_state["df_results"]
        st.rerun()
else:
    st.info("👈 Click **Run Screener & Dashboard** in the sidebar to fetch live data and generate the graphs.")