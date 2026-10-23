import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go

st.set_page_config(page_title="SANU AI", page_icon="🤖", layout="wide")
st.title("🤖 SANU AI")
st.caption("Personal AI • Trading research • Backtesting • Paper-trading demo")

section = st.sidebar.radio("Menu", ["AI Chat", "Trading Dashboard", "Strategy Backtest", "About & Safety"])

if section == "AI Chat":
    st.subheader("💬 AI Chat")
    st.info("Real AI answers require OPENAI_API_KEY in your app host's Secrets. Never put an API key in public code.")
    if "messages" not in st.session_state:
        st.session_state.messages = [{"role":"assistant","content":"नमस्कार! मी तुमचा AI Assistant आहे. AI API key जोडल्यावर प्रत्यक्ष उत्तरे मिळतील."}]
    for m in st.session_state.messages:
        with st.chat_message(m["role"]):
            st.markdown(m["content"])
    prompt = st.chat_input("तुमचा प्रश्न लिहा...")
    if prompt:
        st.session_state.messages.append({"role":"user","content":prompt})
        with st.chat_message("user"):
            st.markdown(prompt)
        answer = None
        try:
            key = st.secrets.get("OPENAI_API_KEY", "")
            if key:
                from openai import OpenAI
                client = OpenAI(api_key=key)
                msgs = [{"role":"system","content":"Answer helpfully in the user's language, especially Marathi or Hindi. Trading answers are educational and must not promise profits."}]
                msgs += [{"role":m["role"],"content":m["content"]} for m in st.session_state.messages[-12:]]
                answer = client.chat.completions.create(model="gpt-4.1-mini", messages=msgs).choices[0].message.content
        except Exception:
            answer = None
        if not answer:
            answer = "हा डेमो मोड आहे. प्रत्यक्ष AI उत्तरे सुरू करण्यासाठी hosting Secrets मध्ये OPENAI_API_KEY सुरक्षितपणे सेट करावी लागेल."
        st.session_state.messages.append({"role":"assistant","content":answer})
        with st.chat_message("assistant"):
            st.markdown(answer)

elif section == "Trading Dashboard":
    st.subheader("📈 Trading Dashboard")
    st.warning("हा synthetic demo data आहे; live market data किंवा CE/PE खरेदी-विक्रीचा सिग्नल नाही.")
    c1,c2,c3 = st.columns(3)
    c1.metric("Market data","Demo only")
    c2.metric("Paper balance","₹1,00,000")
    c3.metric("Broker connected","No")
    dates = pd.date_range(end=pd.Timestamp.today().normalize(), periods=90, freq="D")
    rng = np.random.default_rng(7)
    close = 22000 + np.cumsum(rng.normal(0,95,len(dates)))
    st.plotly_chart(go.Figure(go.Scatter(x=dates,y=close,mode="lines",name="Illustrative index")).update_layout(title="Synthetic example chart"), use_container_width=True)
    st.write("पुढील टप्प्यात historical data, options chain आणि broker API जोडता येईल.")

elif section == "Strategy Backtest":
    st.subheader("🧪 Simple EMA Backtest")
    st.write("CSV मध्ये `Close` column असलेला historical price data अपलोड करा. हा underlying-price demo आहे, options premium backtest नाही.")
    file = st.file_uploader("CSV अपलोड करा", type=["csv"])
    if file:
        try:
            df = pd.read_csv(file)
            if "Close" not in df.columns:
                st.error("CSV मध्ये Close column आवश्यक आहे.")
            else:
                df["Close"] = pd.to_numeric(df["Close"], errors="coerce")
                df = df.dropna(subset=["Close"]).copy()
                df["EMA20"] = df["Close"].ewm(span=20, adjust=False).mean()
                df["EMA50"] = df["Close"].ewm(span=50, adjust=False).mean()
                df["Signal"] = (df["EMA20"] > df["EMA50"]).astype(int)
                df["Return"] = df["Close"].pct_change().fillna(0)
                df["Strategy"] = df["Signal"].shift(1).fillna(0) * df["Return"]
                equity = (1 + df["Strategy"]).cumprod()
                total = (equity.iloc[-1]-1)*100 if len(equity) else 0
                st.metric("Demo strategy return (costs excluded)", f"{total:.2f}%")
                st.plotly_chart(go.Figure([go.Scatter(y=df["Close"],name="Close"),go.Scatter(y=df["EMA20"],name="EMA20"),go.Scatter(y=df["EMA50"],name="EMA50")]).update_layout(title="Price and EMA"), use_container_width=True)
                st.line_chart(equity.rename("Growth of ₹1"))
                st.caption("Brokerage, taxes, slippage, option premium, expiry, strike आणि liquidity यांचे वास्तववादी मॉडेल यात नाही.")
        except Exception as e:
            st.error(f"CSV वाचताना त्रुटी: {e}")
    else:
        st.info("Historical CSV अपलोड केल्यावर backtest चालेल. Live data आपोआप येत नाही.")

else:
    st.subheader("ℹ️ About & Safety")
    st.markdown("""
- हा starter demo आहे, पूर्ण production-ready system नाही.
- AI Chat साठी hosting Secrets मध्ये `OPENAI_API_KEY` आवश्यक आहे.
- Broker integration आणि live orders सध्या नाहीत.
- आधी paper trading आणि historical testing करा.
- API key, broker password, PIN किंवा OTP कोणालाही पाठवू नका.
- नफा हमखास मिळेल अशी रणनीती नसते.
""")
