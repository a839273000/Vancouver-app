import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import plotly.express as px

# --- 設定頁面資訊 ---
st.set_page_config(
    page_title="2025 Canada Trip",
    page_icon="🍁",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# --- 客製化 CSS (極簡 iPhone 風格) ---
st.markdown("""
<style>
    /* 全局字體與背景 */
    .stApp {
        background-color: #F2F2F7; /* iOS 淺灰色背景 */
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
    }
    
    /* 卡片樣式 */
    .travel-card {
        background-color: #FFFFFF;
        border-radius: 16px;
        padding: 20px;
        margin-bottom: 16px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.05);
        border: 1px solid #E5E5EA;
    }
    
    /* 標題樣式 */
    .card-title {
        font-size: 18px;
        font-weight: 700;
        color: #1C1C1E;
        margin-bottom: 8px;
    }
    
    .card-time {
        font-size: 14px;
        color: #8E8E93;
        font-weight: 600;
        margin-bottom: 8px;
        display: block;
    }
    
    /* 標籤樣式 */
    .tag {
        display: inline-block;
        padding: 4px 10px;
        border-radius: 12px;
        font-size: 12px;
        font-weight: 600;
        margin-right: 6px;
        margin-top: 6px;
    }
    .tag-food { background-color: #FFE5E5; color: #D63031; }
    .tag-spot { background-color: #E5F6FF; color: #0984E3; }
    .tag-buy { background-color: #FFF4E5; color: #E17055; }
    .tag-transport { background-color: #F0F2F5; color: #636E72; }
    .tag-tips { background-color: #FFF9C4; color: #FBC02D; border: 1px solid #FBC02D; }

    /* 重點亮顯 */
    .highlight-text {
        font-weight: bold;
        color: #007AFF; /* iOS Blue */
    }

    /* 天氣 Widget */
    .weather-widget {
        background: linear-gradient(135deg, #74b9ff, #0984e3);
        color: white;
        padding: 15px;
        border-radius: 16px;
        margin-bottom: 20px;
        display: flex;
        justify-content: space-between;
        align-items: center;
    }
</style>
""", unsafe_allow_html=True)

# --- 資料準備 (根據你的上傳檔案整合) ---
# 這裡將檔案內容轉化為結構化數據
itinerary_data = {
    "2025-12-23": {
        "city": "Vancouver",
        "events": [
            {"time": "23:55 (TPE)", "title": "長榮 BR10 出發", "type": "transport", "desc": "前往溫哥華", "loc": "Taoyuan Airport"},
            {"time": "18:35 (YVR)", "title": "抵達溫哥華", "type": "transport", "desc": "入境、領行李", "loc": "YVR Airport"},
            {"time": "20:30", "title": "春秋火鍋", "type": "food", "desc": "抵達後晚餐", "loc": "Landmark Hotpot House"}
        ]
    },
    "2025-12-24": {
        "city": "Whitehorse",
        "events": [
            {"time": "09:25", "title": "飛往白馬鎮 (AC)", "type": "transport", "desc": "YVR -> YXY (12:54 抵達)", "loc": "YVR Airport"},
            {"time": "14:00", "title": "入住 Raven Inn", "type": "stay", "desc": "Check-in 休息", "loc": "Raven Inn Whitehorse"},
            {"time": "23:10", "title": "Aurora Viewing Tour", "type": "spot", "desc": "極光中心觀賞 (約5小時)", "loc": "Aurora Centre Whitehorse", "tips": "記得穿戴極地裝備，攜帶備用電池"}
        ]
    },
    "2025-12-25": {
        "city": "Whitehorse",
        "events": [
            {"time": "13:05", "title": "Dog Sledding Tour", "type": "spot", "desc": "半日狗拉雪橇 (4HR)", "loc": "Whitehorse Dog Sledding", "tips": "保護好相機，狗狗很熱情"},
            {"time": "23:10", "title": "Aurora Viewing Tour (D2)", "type": "spot", "desc": "第二次極光觀賞", "loc": "Aurora Centre Whitehorse"}
        ]
    },
    "2025-12-26": {
        "city": "Whitehorse",
        "events": [
            {"time": "10:45", "title": "City Tour & Wildlife", "type": "spot", "desc": "野生動物保護區 & 溫泉 (Hot Springs)", "loc": "Yukon Wildlife Preserve", "tips": "必拍：雪地裡的動物"},
            {"time": "23:10", "title": "Aurora Viewing Tour (D3)", "type": "spot", "desc": "最後一晚極光", "loc": "Aurora Centre Whitehorse"}
        ]
    },
    "2025-12-27": {
        "city": "Whitehorse/Vancouver",
        "events": [
            {"time": "Morning", "title": "市區採買", "type": "buy", "desc": "Two Brewers (威士忌), Anto Yukon (香皂)", "loc": "Whitehorse Main Street", "tips": "必買：Anto Yukon香皂"},
            {"time": "13:35", "title": "飛回溫哥華", "type": "transport", "desc": "YXY -> YVR (15:05 抵達)", "loc": "Erik Nielsen Whitehorse International Airport"}
        ]
    },
    "2025-12-28": {
        "city": "Vancouver",
        "events": [
            {"time": "11:30", "title": "金閣海鮮酒家", "type": "food", "desc": "與戴仕軒早午餐", "loc": "Golden Ocean Seafood Restaurant"},
            {"time": "Afternoon", "title": "Queen Elizabeth Park", "type": "spot", "desc": "Bloedel Conservatory, Hillcrest Community Centre", "loc": "Queen Elizabeth Park"},
            {"time": "17:30", "title": "Seasons in the Park", "type": "food", "desc": "晚餐", "loc": "Seasons in the Park"}
        ]
    },
    "2025-12-29": {
        "city": "Vancouver",
        "events": [
            {"time": "Morning", "title": "Angus T Bakery & Café", "type": "food", "desc": "Downtown 早餐", "loc": "Angus T Bakery & Café"},
            {"time": "Daytime", "title": "Granville Island", "type": "spot", "desc": "公眾市場、逛畫廊", "loc": "Granville Island", "tips": "必吃：Chowder, La Bise Bakery, Lee's Donuts"},
            {"time": "Evening", "title": "桑拿放鬆", "type": "spot", "desc": "AetherHaus 或 Circle Wellness", "loc": "Circle Wellness Granville Island"}
        ]
    },
    "2025-12-30": {
        "city": "Vancouver",
        "events": [
            {"time": "11:00", "title": "Mt. Seymour 滑雪", "type": "spot", "desc": "Snowboard lesson (11:00-13:00)", "loc": "Mt Seymour Resort", "tips": "Shuttle: Rupert Skytrain Station"},
            {"time": "Afternoon", "title": "Slo Coffee", "type": "food", "desc": "休息喝咖啡", "loc": "Slo Coffee"},
            {"time": "Evening", "title": "Earnest Ice Cream", "type": "food", "desc": "Fraser St 分店", "loc": "Earnest Ice Cream Fraser", "tips": "路人推薦：Cream Cheese, London Fog, Whiskey Hazelnut"}
        ]
    },
    "2025-12-31": {
        "city": "Vancouver",
        "events": [
            {"time": "10:00", "title": "北溫 Lower Lonsdale", "type": "spot", "desc": "The Polygon Gallery, Lonsdale Quay Market", "loc": "The Polygon Gallery", "tips": "參觀 Shipyards 歷史地圖"},
            {"time": "Afternoon", "title": "Lighthouse Park", "type": "spot", "desc": "戶外健行 (1hr)", "loc": "Lighthouse Park"}
        ]
    },
    "2026-01-01": {
        "city": "Vancouver",
        "events": [
            {"time": "Morning", "title": "Capilano Suspension Bridge", "type": "spot", "desc": "吊橋公園、鮭魚孵化場", "loc": "Capilano Suspension Bridge Park", "tips": "順路看 Cleveland Dam"},
            {"time": "Afternoon", "title": "Stanley Park?", "type": "spot", "desc": "討論：是否有車去水族館", "loc": "Vancouver Aquarium"}
        ]
    },
    "2026-01-02": {
        "city": "Richmond",
        "events": [
            {"time": "All Day", "title": "Richmond 逛街", "type": "buy", "desc": "阿搜比、最後採買", "loc": "Richmond Centre"},
             {"time": "Tip", "title": "購物清單檢查", "type": "buy", "desc": "CK, Saje (睡前塗腳底精油), 楓糖漿", "loc": "CF Richmond Centre", "tips": "Saje 據說塗腳底可一覺到天亮"}
        ]
    },
    "2026-01-03": {
        "city": "Vancouver",
        "events": [
            {"time": "16:15", "title": "返程航班 BR09", "type": "transport", "desc": "YVR -> TPE (05:15+1)", "loc": "YVR Airport"}
        ]
    }
}

# --- 功能函數 ---

def get_weather(city, date):
    # 這裡未來可以接真實 API，目前做模擬顯示
    if city == "Whitehorse":
        return "❄️ -15°C | 降雪機率 40%"
    return "🌧️ 6°C | 溫哥華冬季多雨"

def google_maps_link(location):
    base_url = "https://www.google.com/maps/search/?api=1&query="
    return base_url + location.replace(" ", "+")

# --- App 介面 ---

# 底部導航模擬 (使用 Tabs)
tab1, tab2, tab3 = st.tabs(["📅 行程", "🧳 資訊/工具", "💰 記帳"])

# === Tab 1: 行程 ===
with tab1:
    # 日期選擇器
    selected_date_obj = st.date_input(
        "選擇日期",
        min_value=datetime(2025, 12, 23),
        max_value=datetime(2026, 1, 3),
        value=datetime(2025, 12, 23)
    )
    selected_date = selected_date_obj.strftime("%Y-%m-%d")

    if selected_date in itinerary_data:
        day_data = itinerary_data[selected_date]
        
        # 1. 天氣預報 Widget
        st.markdown(f"""
        <div class="weather-widget">
            <div>
                <h3 style="margin:0; color:white;">{day_data['city']}</h3>
                <p style="margin:0; font-size:14px;">{selected_date}</p>
            </div>
            <div style="font-size: 20px; font-weight:bold;">
                {get_weather(day_data['city'], selected_date)}
            </div>
        </div>
        """, unsafe_allow_html=True)

        # 2. 行程卡片
        for event in day_data['events']:
            # 決定標籤顏色
            tag_class = f"tag-{event['type']}"
            tag_label = event['type'].upper()
            
            # 卡片 HTML
            card_html = f"""
            <div class="travel-card">
                <span class="card-time">{event['time']}</span>
                <div class="card-title">{event['title']}</div>
                <div style="margin-bottom:8px;">
                    <span class="tag {tag_class}">{tag_label}</span>
                </div>
                <div style="color: #4A4A4A; font-size: 15px; margin-bottom: 12px;">
                    {event['desc']}
                </div>
            """
            
            # 如果有 Tips (導遊職責)
            if 'tips' in event:
                card_html += f"""
                <div style="background-color: #FFF9C4; padding: 8px; border-radius: 8px; font-size: 13px; color: #5D4037; margin-bottom:10px;">
                    💡 <b>小撇步：</b> {event['tips']}
                </div>
                """
            
            card_html += "</div>"
            st.markdown(card_html, unsafe_allow_html=True)
            
            # 導航按鈕 (Streamlit 原生按鈕以支援 Python 邏輯)
            if st.button(f"📍 導航至 {event['title']}", key=event['title']):
                st.link_button("開啟 Google Maps", google_maps_link(event['loc']))

    else:
        st.info("今天沒有安排特定行程，好好休息！")

# === Tab 2: 資訊與工具 ===
with tab2:
    st.markdown("### ✈️ 航班資訊")
    st.info("**去程 (BR10):** 12/23 TPE 23:55 -> YVR 18:35")
    st.info("**國內線 (AC):** 12/24 YVR 09:25 -> YXY 12:54")
    st.info("**回程 (BR09):** 01/03 YVR 16:15 -> TPE 05:15(+1)")

    st.markdown("---")
    st.markdown("### 🏨 住宿")
    st.write("📍 **Whitehorse:** Raven Inn")
    st.write("📍 **Vancouver:** (填寫溫哥華住宿地址)")

    st.markdown("---")
    st.markdown("### 🛍️ 必買清單 Check")
    checklist = {
        "CK 內衣褲": False,
        "Saje 精油 (腳底/耳後睡眠用)": False,
        "楓糖漿 (給張憶庭)": False,
        "Anto Yukon 香皂": False
    }
    
    for item, checked in checklist.items():
        st.checkbox(item, value=checked)

# === Tab 3: 記帳分帳 ===
with tab3:
    st.markdown("### 💸 快速記帳")
    
    # 初始化 Session State
    if 'expenses' not in st.session_state:
        st.session_state.expenses = pd.DataFrame(columns=["日期", "項目", "金額", "分類", "付款人"])

    with st.form("expense_form"):
        col1, col2 = st.columns(2)
        with col1:
            ex_item = st.text_input("項目 (如: 晚餐)")
            ex_amount = st.number_input("金額 (CAD)", min_value=0.0)
        with col2:
            ex_cat = st.selectbox("分類", ["食物", "交通", "購物", "娛樂", "住宿"])
            ex_payer = st.selectbox("付款人", ["本人", "旅伴A", "旅伴B"]) # 可修改名字
            
        submitted = st.form_submit_button("➕ 新增支出")
        
        if submitted:
            new_row = pd.DataFrame({
                "日期": [datetime.now().strftime("%Y-%m-%d")],
                "項目": [ex_item],
                "金額": [ex_amount],
                "分類": [ex_cat],
                "付款人": [ex_payer]
            })
            st.session_state.expenses = pd.concat([st.session_state.expenses, new_row], ignore_index=True)
            st.success("已儲存！")

    # 顯示統計
    if not st.session_state.expenses.empty:
        st.markdown("#### 支出明細")
        st.dataframe(st.session_state.expenses)
        
        st.markdown("#### 分類統計")
        fig = px.pie(st.session_state.expenses, values='金額', names='分類', hole=0.4)
        fig.update_layout(margin=dict(t=0, b=0, l=0, r=0), height=250)
        st.plotly_chart(fig, use_container_width=True)
