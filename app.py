import streamlit as st
import pandas as pd
from datetime import datetime
import plotly.express as px

# --- 設定頁面資訊 ---
st.set_page_config(
    page_title="2025 Canada Trip",
    page_icon="🍁",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# --- 資料準備 ---
# 定義日期與城市的對應關係，用來切換背景
date_city_map = {
    "2025-12-23": "Vancouver",
    "2025-12-24": "Whitehorse",
    "2025-12-25": "Whitehorse",
    "2025-12-26": "Whitehorse",
    "2025-12-27": "Whitehorse", # 下午回溫哥華，但早上還在白馬，暫定白馬
    "2025-12-28": "Vancouver",
    "2025-12-29": "Vancouver",
    "2025-12-30": "Vancouver",
    "2025-12-31": "Vancouver",
    "2026-01-01": "Vancouver",
    "2026-01-02": "Richmond", # 算在大溫哥華區
    "2026-01-03": "Vancouver"
}

# 背景圖片連結 (可替換成你自己的圖檔路徑，如 "app/my_photo.jpg")
backgrounds = {
    "Vancouver": "https://images.unsplash.com/photo-1560275619-4662e36fa65c?q=80&w=2000&auto=format&fit=crop", # 溫哥華城市
    "Richmond": "https://images.unsplash.com/photo-1560275619-4662e36fa65c?q=80&w=2000&auto=format&fit=crop",  # 共用溫哥華
    "Whitehorse": "https://images.unsplash.com/photo-1531366936337-7c912a4589a7?q=80&w=2000&auto=format&fit=crop", # 極光/雪地
    "Default": "https://images.unsplash.com/photo-1476514525535-07fb3b4ae5f1?q=80&w=2000&auto=format&fit=crop"
}

# 詳細行程資料
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
            {"time": "10:45", "title": "City Tour & Wildlife", "type": "spot", "desc": "野生動物保護區 & 溫泉", "loc": "Yukon Wildlife Preserve", "tips": "必拍：雪地裡的動物"},
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

# --- CSS 樣式與動態背景 ---
def set_bg(url):
    st.markdown(f"""
    <style>
        .stApp {{
            background-image: url("{url}");
            background-size: cover;
            background-position: center;
            background-repeat: no-repeat;
            background-attachment: fixed;
        }}
        /* 讓內容區域有玻璃擬態效果，增加文字可讀性 */
        .main .block-container {{
            background-color: rgba(255, 255, 255, 0.85);
            border-radius: 20px;
            padding: 2rem;
            margin-top: 2rem;
            backdrop-filter: blur(10px);
            box-shadow: 0 4px 30px rgba(0, 0, 0, 0.1);
        }}
        
        /* 卡片樣式優化 */
        .travel-card {{
            background-color: #FFFFFF;
            border-radius: 16px;
            padding: 18px;
            margin-bottom: 12px;
            border-left: 5px solid #0984E3; /* 裝飾線 */
            box-shadow: 0 2px 8px rgba(0,0,0,0.08);
        }}
        
        .tag {{
            display: inline-block;
            padding: 3px 8px;
            border-radius: 6px;
            font-size: 12px;
            font-weight: 600;
            margin-right: 5px;
        }}
        .tag-food {{ background-color: #ffeaa7; color: #d35400; }}
        .tag-spot {{ background-color: #74b9ff; color: #0984e3; }}
        .tag-buy {{ background-color: #ffcccc; color: #d63031; }}
        .tag-transport {{ background-color: #dfe6e9; color: #2d3436; }}
        .tag-stay {{ background-color: #a29bfe; color: #6c5ce7; }}

        /* 隱藏預設的主選單漢堡按鈕，讓畫面更乾淨 */
        #MainMenu {{visibility: hidden;}}
        footer {{visibility: hidden;}}
        
    </style>
    """, unsafe_allow_html=True)

# --- App 主邏輯 ---

# 1. 日期滑動選擇器
# 製作日期列表
date_list = list(itinerary_data.keys())
# 將日期格式化為較好讀的字串 (e.g. "12/23") 供滑桿顯示
date_labels = {d: d[5:].replace("-", "/") for d in date_list}

# 使用 select_slider
selected_date = st.select_slider(
    "請滑動選擇日期 🗓️",
    options=date_list,
    format_func=lambda x: date_labels[x]
)

# 2. 根據日期設定背景
current_city = date_city_map.get(selected_date, "Default")
bg_url = backgrounds.get(current_city, backgrounds["Default"])
set_bg(bg_url)

st.image("你的照片檔名.jpg", use_container_width=True) 


st.title(f"📅 {date_labels[selected_date]} {current_city}")
# 3. 顯示內容
st.title(f"📅 {date_labels[selected_date]} {current_city}")

tab1, tab2, tab3 = st.tabs(["行程", "資訊", "記帳"])

with tab1:
    day_data = itinerary_data.get(selected_date)
    if day_data:
        # 天氣小卡
        weather_icon = "❄️" if "Whitehorse" in current_city else "🌧️"
        temp = "-15°C" if "Whitehorse" in current_city else "6°C"
        st.info(f"{weather_icon} {current_city} 天氣預報: {temp}")

        for event in day_data['events']:
            # 準備 HTML 內容
            tag_type = event.get('type', 'spot')
            tips_html = ""
            
            # 如果有 Tips，先組合成 HTML 字串
            if 'tips' in event:
                tips_html = f"""
                <div style="background-color: #FFF9C4; padding: 10px; border-radius: 8px; font-size: 14px; color: #5D4037; margin-top:8px; border: 1px dashed #FBC02D;">
                    💡 <b>小撇步：</b> {event['tips']}
                </div>
                """
            
            # 完整的卡片 HTML
            card_html = f"""
            <div class="travel-card">
                <div style="display:flex; justify-content:space-between; align-items:center;">
                    <span style="font-weight:bold; font-size:18px; color:#2d3436;">{event['title']}</span>
                    <span style="font-size:14px; color:#636e72; font-family:monospace;">{event['time']}</span>
                </div>
                <div style="margin: 5px 0;">
                    <span class="tag tag-{tag_type}">{tag_type.upper()}</span>
                    <span style="font-size:14px; color:#636e72;">📍 {event['loc']}</span>
                </div>
                <div style="color: #4A4A4A; font-size: 15px; line-height:1.5;">
                    {event['desc']}
                </div>
                {tips_html}
            </div>
            """
            
            # 重要：一定要用 unsafe_allow_html=True 渲染
            st.markdown(card_html, unsafe_allow_html=True)
            
            # 導航按鈕 (Streamlit 原生按鈕無法放在 HTML 裡，所以分開寫)
            if st.button(f"🗺️ 導航去: {event['title']}", key=event['title']):
                st.link_button("開啟 Google Maps", f"https://www.google.com/maps/search/?api=1&query={event['loc']}")
    else:
        st.write("查無資料")

with tab2:
    st.markdown("### ✈️ 航班 & 住宿")
    st.success("去程: BR10 | 回程: BR09")
    st.info("住宿: Raven Inn (Whitehorse)")
    
    st.markdown("### 🛍️ 購物清單")
    st.checkbox("CK 內衣褲")
    st.checkbox("Saje 精油")
    st.checkbox("楓糖漿")
    st.checkbox("Anto Yukon 香皂")

with tab3:
    st.markdown("### 💸 記帳本")
    if 'expenses' not in st.session_state:
        st.session_state.expenses = pd.DataFrame(columns=["項目", "金額", "分類"])
        
    with st.form("accounting"):
        item = st.text_input("項目")
        cost = st.number_input("金額", min_value=0.0)
        category = st.selectbox("分類", ["食", "衣", "住", "行", "樂"])
        if st.form_submit_button("新增"):
            new_data = pd.DataFrame({"項目": [item], "金額": [cost], "分類": [category]})
            st.session_state.expenses = pd.concat([st.session_state.expenses, new_data], ignore_index=True)
            st.rerun()
            
    if not st.session_state.expenses.empty:
        st.dataframe(st.session_state.expenses)
        fig = px.pie(st.session_state.expenses, values='金額', names='分類', title="花費比例")
        st.plotly_chart(fig)
