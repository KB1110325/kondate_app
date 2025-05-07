import streamlit as st
import datetime
import json
import os
from collections import defaultdict

# ------------------------------
# データ定義
# ------------------------------
dish_key_map = {
    "主菜": "main",
    "副菜": "side",
    "汁": "soup"
}

menu_data = {
    "主菜": {
        "ハンバーグ": {
            "ingredients": {"玉ねぎ": "1個", "合挽き肉": "300g", "パン粉": "50g"},
            "link": "https://example.com/hamburg"
        },
        "焼き魚": {
            "ingredients": {"鮭": "2切れ", "塩": "少々"},
            "link": "https://example.com/grilled_fish"
        }
    },
    "副菜": {
        "サラダ": {
            "ingredients": {"レタス": "1玉", "トマト": "2個", "きゅうり": "1本"},
            "link": "https://example.com/salad"
        },
        "味噌汁": {
            "ingredients": {"豆腐": "1丁", "わかめ": "適量", "味噌": "大さじ2"},
            "link": "https://example.com/misosoup"
        }
    },
    "汁": {
        "どさんこ汁": {
            "ingredients": {
                "じゃがいも": "2個",
                "にんじん": "1/2個",
                "玉ねぎ": "1/2個",
                "豚こま肉": "150g",
                "コーン": "50g",
                "乾燥わかめ": "大さじ1.5"
            },
            "link": "https://www.instagram.com/p/DH5eKCGzT5c/?img_index=5&igsh=MWxweW4zZGM3aW1qdA=="
        }
    }
}

category_map = {
    "玉ねぎ": "野菜",
    "レタス": "野菜",
    "トマト": "野菜",
    "きゅうり": "野菜",
    "じゃがいも": "野菜",
    "にんじん": "野菜",
    "コーン": "野菜",
    "豆腐": "その他",
    "乾燥わかめ": "その他",
    "味噌": "調味料",
    "鮭": "魚",
    "合挽き肉": "肉",
    "豚こま肉": "肉",
    "パン粉": "その他",
    "塩": "調味料"
}

# 保存ファイル名
DATA_FILE = "kondate_data.json"

# 保存処理

def save_menu_to_json(date_str, menu):
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
    else:
        data = {}
    data[date_str] = menu
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

# 読み込み処理

def load_menu_from_json(date_str):
    if not os.path.exists(DATA_FILE):
        return None
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)
    return data.get(date_str)

# ------------------------------
# アプリ本体
# ------------------------------
st.title("献立アプリ")

st.sidebar.header("設定")
start_date = st.sidebar.date_input("献立の起点日を選択", value=datetime.date.today())
day_count = st.sidebar.number_input("献立を作成する日数", min_value=1, max_value=7, value=3)

selected_menus = []

for i in range(day_count):
    st.header(f"{i+1}日目の献立")
    date = st.date_input(f"日付を選択（{i+1}日目）", value=start_date + datetime.timedelta(days=i))

    main_dish = st.selectbox(f"主菜を選んでください（{i+1}日目）", ["無し"] + list(menu_data["主菜"].keys()), key=f"main_{i}")
    side_dish = st.selectbox(f"副菜を選んでください（{i+1}日目）", ["無し"] + list(menu_data["副菜"].keys()), key=f"side_{i}")
    soup_dish = st.selectbox(f"汁を選んでください（{i+1}日目）", ["無し"] + list(menu_data["汁"].keys()), key=f"soup_{i}")

    selected_menus.append({"date": date, "main": main_dish, "side": side_dish, "soup": soup_dish})

# ------------------------------
# 買い物リスト作成＆保存
# ------------------------------
if st.button("買い物リストをまとめる"):
    st.header("買い物リスト")
    ingredient_totals = defaultdict(list)

    for menu in selected_menus:
        date_str = str(menu["date"])
        save_menu_to_json(date_str, {
            "main": menu["main"],
            "side": menu["side"],
            "soup": menu["soup"]
        })

        for dish_type in ["主菜", "副菜", "汁"]:
            dish_key = dish_key_map[dish_type]
            dish_name = menu[dish_key]
            if dish_name == "無し":
                continue
            ingredients = menu_data[dish_type][dish_name]["ingredients"]
            for item, qty in ingredients.items():
                ingredient_totals[item].append(qty)

    def sum_ingredients(qty_list):
        total = defaultdict(float)
        for qty in qty_list:
            for unit in ["個", "本", "g", "玉", "丁", "切れ", "大さじ", "少々", "適量"]:
                if unit in qty:
                    try:
                        number = float(qty.replace(unit, "").strip())
                        total[unit] += number
                    except:
                        total[unit] += 0
                    break
            else:
                total[""] += 1
        return "、".join([f"{round(num)}{unit}" if unit else str(round(num)) for unit, num in total.items()])

    categorized = defaultdict(dict)
    for item, qtys in ingredient_totals.items():
        category = category_map.get(item, "その他")
        categorized[category][item] = sum_ingredients(qtys)

    for category in ["野菜", "肉", "魚", "調味料", "その他"]:
        if category in categorized:
            st.subheader(f"【{category}】")
            for item, total in categorized[category].items():
                st.write(f"- {item}：{total}")

    st.header("作り方リンク")
    for menu in selected_menus:
        st.subheader(f"{menu['date']}の献立")
        for dish_type in ["主菜", "副菜", "汁"]:
            dish_key = dish_key_map[dish_type]
            dish_name = menu[dish_key]
            if dish_name != "無し":
                link = menu_data[dish_type][dish_name]["link"]
                st.markdown(f"- [{dish_type}：{dish_name}]({link})")

# ------------------------------
# カレンダーから過去の献立を表示
# ------------------------------
st.header("📅 カレンダーから過去の献立を確認")
selected_date = st.date_input("日付を選んで献立を表示", key="calendar_lookup")
menu = load_menu_from_json(str(selected_date))

if menu:
    st.subheader(f"{selected_date} の献立")
    st.write(f"- 主菜: {menu['main']}")
    st.write(f"- 副菜: {menu['side']}")
    st.write(f"- 汁物: {menu['soup']}")
else:
    st.info("この日には献立が登録されていません。")
