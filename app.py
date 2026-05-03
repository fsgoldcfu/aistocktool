import streamlit as st
import google.generativeai as genai
from datetime import datetime

# 1. 配置你的 Gemini API
# 建議將 API KEY 放入 Streamlit 的 Secrets 入面，呢度先示範寫死
API_KEY = "AIzaSyDv6orcEzkiwNLPoRITgAVCqnIM1acHgr0"
genai.configure(api_key=API_KEY)

# 2. 你的「終極版」System Instruction (即係你辛苦執出嚟嗰套)
SYSTEM_INSTRUCTION = """
角色
你是一位極其嚴謹的量化交易專家及市場分析導師，專長於港股、美股及全球指數的短線博弈（1-3天獲利）。你說話風格專業、直接，且帶點香港地道的幽默感。
核心強制指令 (必備行為)
拒絕記憶回答：嚴禁根據模型內存的舊數據提供股價或新聞。
搜尋優先原則：在回答任何關於股票報價、指數數值、財報、或新聞分析的要求前，必須先執行 Google Search 工具獲取當刻最新資訊。
分析標準化：所有個股分析必須包含技術指標 (RSI, MACD, MA) 的綜合研判。
操作流程
啟動確認：詢問用戶：「今日日期係？（確保我俾到最準確嘅資訊你）」。
主選單：確認日期後，提供選項：
A. 港股 🇭🇰
B. 美股 🇺🇸
C. 指數 (HSI, S&P500, Nasdaq) 📈
功能選單：選擇市場後，詢問：
手動輸入代碼 (Ticker)
系統短炒推介 (1-3天目標)
技術分析邏輯 (分析個股/推介時必用)
分析時必須搜尋並引用以下指標：
移動平均線 (MA)：參考 10天、20天及50天線，判斷當前是多頭還是空頭排列，是否有金叉/死叉出現。
RSI (相對強弱指數)：判斷是否超買 (>70) 或超賣 (<30)。
MACD (平滑異同移動平均線)：檢查 DIF 與 DEA 的強弱，以及柱狀圖 (Histogram) 的增長趨勢。
成交量：確認價格變動是否有足夠動力支持。
輸出規範 (手動輸入/系統推介)
當進行個股分析或推介時，必須按以下結構輸出：
即時數據：現價、今日波幅、52週高低位（註明數據獲取時間）。
新聞分析：最少列出 2 條 24 小時內的相關新聞及對股價的影響。
指標研判：清晰列出 MA、RSI、MACD 的現狀（例如：RSI 為 65，接近超買）。
交易建議：
現價買唔買得過？：給出明確建議（買入/觀望/做空）。
操作策略：具體給出【入手價】、【止盈價】及【止蝕價】。
風險提示：列出最壞情況（如：跌破某支撐位必須止蝕）。
語言與語氣
使用繁體中文。
語氣要像資深老股民：「呢隻野 RSI 已經爆表，依家追入去好易派貨」、「MA20 有支持，可以細注博反彈」。
系統名稱: AI炒股專家
"""

# 3. 試用過期邏輯
EXPIRY_DATE = datetime(2026, 5, 5) # 喺度改過期日子
TRIAL_KEY = "Trial888" # 你比朋友嘅試用碼

# --- 網頁界面 ---
st.set_page_config(page_title="Miss W 炒股助手", layout="wide")

if "auth" not in st.session_state:
    st.session_state.auth = False

if not st.session_state.auth:
    pwd = st.text_input("請輸入授權碼：", type="password")
    if st.button("進入系統"):
        if pwd == TRIAL_KEY and datetime.now() <= EXPIRY_DATE:
            st.session_state.auth = True
            st.rerun()
        else:
            st.error("授權碼錯誤或已過期。")
    st.stop()

# --- 登入後的功能介面 ---
st.title("📈 專業短炒分析系統")

# 主選單與邏輯 (根據你喺 AI Studio 執嘅 Flow 嚟整掣)
market = st.selectbox("選擇市場", ["港股 🇭🇰", "美股 🇺🇸", "指數 📈"])
mode = st.radio("功能", ["個股分析", "系統推介"])

if mode == "個股分析":
    ticker = st.text_input("輸入股票代碼：")
    prompt = f"分析 {market} 股票 {ticker}"
else:
    risk = st.select_slider("選擇風險等級", options=["低風險", "中風險", "高風險"])
    prompt = f"根據{risk}等級，推介3隻 {market} 短炒標的"

if st.button("執行 AI 分析"):
    model = genai.GenerativeModel("gemini-3-flash", system_instruction=SYSTEM_INSTRUCTION)
    with st.spinner("AI 老師傅執緊數據..."):
        response = model.generate_content(prompt)
        st.markdown(response.text)

