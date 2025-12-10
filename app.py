import streamlit as st
import pandas as pd
from datetime import datetime
import plotly.express as px

# --- 1. 設定與狀態初始化 ---
st.set_page_config(
    page_title="Brian & Tanya's Trip",
    page_icon="🍁",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# 初始化 Session State 來控制頁面跳轉
if 'current_page' not in st.session_state:
    st.session_state['current_page'] = 'welcome'

# --- 2. 資料定義區域 ---

# 日期與城市對應
date_city_map = {
    "2025-12-23": "Vancouver",
    "2025-12-24": "Whitehorse",
    "2025-12-25": "Whitehorse",
    "2025-12-26": "Whitehorse",
    "2025-12-27": "Whitehorse",
    "2025-12-28": "Vancouver",
    "2025-12-29": "Vancouver",
    "2025-12-30": "Vancouver",
    "2025-12-31": "Vancouver",
    "2026-01-01": "Vancouver",
    "2026-01-02": "Richmond",
    "2026-01-03": "Vancouver"
}

# 背景圖片連結 (已更新溫哥華為指標性臨海圖片)
backgrounds = {
    # 替換成更有指標性的溫哥華臨海市景 (Canada Place/Coal Harbour area)
    "Vancouver": "https://images.unsplash.com/photo-1559511260-66a654ae982a?q=80&w=2000&auto=format&fit=crop", 
    "Richmond": "https://images.unsplash.com/photo-1559511260-66a654ae982a?q=80&w=2000&auto=format&fit=crop",
    "Whitehorse": "https://images.unsplash.com/photo-1531366936337-7c912a4589a7?q=80&w=2000&auto=format&fit=crop",
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

# --- 3. CSS 樣式函數 (深色模式) ---
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
        .stApp, .stMarkdown, h1, h2, h3, h4, h5, h6, p, span, div {{
            color: #FFFFFF !important;
        }}
        /* 主內容容器 - 深色毛玻璃 */
        .main .block-container {{
            background-color: rgba(0, 0, 0, 0.65);
            border-radius: 20px;
            padding: 2rem;
            margin-top: 2rem;
            backdrop-filter: blur(10px);
            box-shadow: 0 4px 30px rgba(0, 0, 0, 0.5);
        }}
        /* 行程卡片 - 深灰色 */
        .travel-card {{
            background-color: rgba(60, 60, 60, 0.9);
            border-radius: 16px;
            padding: 18px;
            margin-bottom: 12px;
            border-left: 5px solid #74b9ff;
            box-shadow: 0 4px 6px rgba(0,0,0,0.3);
            color: #FFFFFF;
        }}
        .travel-card .card-title {{
            color: #ffffff !important;
            font-weight: bold;
        }}
        /* 標籤樣式 */
        .tag {{
            display: inline-block;
            padding: 3px 8px;
            border-radius: 6px;
            font-size: 12px;
            font-weight: 600;
            margin-right: 5px;
            color: #2d3436 !important;
        }}
        .tag-food {{ background-color: #ffeaa7; }}
        .tag-spot {{ background-color: #74b9ff; }}
        .tag-buy {{ background-color: #ffcccc; }}
        .tag-transport {{ background-color: #dfe6e9; }}
        
        #MainMenu {{visibility: hidden;}}
        footer {{visibility: hidden;}}
        .stSlider label {{ color: white !important; }}
        
        /* 歡迎頁面專用樣式 */
        .welcome-title {{
            text-align: center;
            font-size: 2.5rem;
            font-weight: 800;
            margin-top: 20px;
            margin-bottom: 30px;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.5);
        }}
        .stButton button {{
            width: 100%;
            border-radius: 12px;
            height: 50px;
            font-size: 18px;
            font-weight: bold;
        }}
    </style>
    """, unsafe_allow_html=True)

# --- 4. 頁面函數定義 ---

def show_welcome_page():
    """顯示歡迎首頁"""
    # 這裡設定一個預設的漂亮背景，或者你可以用空白背景
    set_bg("https://images.unsplash.com/photo-1469854523086-cc02fe5d8800?q=80&w=2000&auto=format&fit=crop")
    
    # 顯示 header.jpg (請確保檔案在同目錄下)
    # 這裡使用 columns 來稍微置中圖片
    col1, col2, col3 = st.columns([1, 8, 1])
    with col2:
        try:
            st.image("header.jpg", use_container_width=True)
        except:
            st.warning("請確認 header.jpg 已上傳至專案目錄")

    # 顯示大標題 (使用 HTML 置中)
    st.markdown('<div class="welcome-title">Brian & Tanya\'s<br>trip to Vancouver 🇨🇦</div>', unsafe_allow_html=True)
    
    # 進入按鈕
    # 使用 columns 讓按鈕不要太寬
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("開始旅程 ✨"):
            # 按下後切換狀態，並重新執行
            st.session_state['current_page'] = 'main'
            st.rerun()

def show_main_app():
    """顯示主要的旅遊行程 App 內容"""
    
    # 日期滑動選擇器
    date_list = list(itinerary_data.keys())
    date_labels = {d: d[5:].replace("-", "/") for d in date_list}

    selected_date = st.select_slider(
        "請滑動選擇日期 🗓️",
        options=date_list,
        format_func=lambda x: date_labels[x]
    )

    # 根據日期設定背景
    current_city = date_city_map.get(selected_date, "Default")
    bg_url = backgrounds.get(current_city, backgrounds["Default"])
    set_bg(bg_url)

    # 顯示內容標題
    st.title(f"📅 {date_labels[selected_date]} {current_city}")

    tab1, tab2, tab3 = st.tabs(["行程", "資訊", "記帳"])

    with tab1:
        day_data = itinerary_data.get(selected_date)
        if day_data:
            weather_icon = "❄️" if "Whitehorse" in current_city else "🌧️"
            temp = "-15°C" if "Whitehorse" in current_city else "6°C"
            st.info(f"{weather_icon} {current_city} 天氣預報: {temp}")

            for event in day_data['events']:
                tag_type = event.get('type', 'spot')
                tips_html = ""
                if 'tips' in event:
                    tips_html = f"""
                    <div style="background-color: rgba(255, 249, 196, 0.15); padding: 10px; border-radius: 8px; font-size: 14px; color: #ececec; margin-top:8px; border: 1px dashed #ffeaa7;">
                        💡 <b>小撇步：</b> {event['tips']}
                    </div>
                    """
                
                card_html = f"""
                <div class="travel-card">
                    <div style="display:flex; justify-content:space-between; align-items:center;">
                        <span class="card-title" style="font-size:18px;">{event['title']}</span>
                        <span style="font-size:14px; color:#b2bec3; font-family:monospace;">{event['time']}</span>
                    </div>
                    <div style="margin: 5px 0;">
                        <span class="tag tag-{tag_type}">{tag_type.upper()}</span>
                        <span style="font-size:14px; color:#dfe6e9;">📍 {event['loc']}</span>
                    </div>
                    <div style="color: #ecf0f1; font-size: 15px; line-height:1.5;">
                        {event['desc']}
                    </div>
                    {tips_html}
                </div>
                """
                st.markdown(card_html, unsafe_allow_html=True)
                
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

# --- 5. 主程式執行邏輯 ---

if st.session_state['current_page'] == 'welcome':
    show_welcome_page()
else:
    show_main_app()
