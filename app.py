import streamlit as st
import datetime
import json
import os
from collections import defaultdict
from fractions import Fraction

# --- パスワード認証 ---
PASSWORD = "k1122"
password = st.text_input("パスワードを入力してください", type="password")
if password != PASSWORD:
    st.warning("正しいパスワードを入力してください。")
    st.stop()

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
        "麻婆豆腐": {
            "ingredients": {"豆腐": "1丁", "豚挽き肉": "150g", "にんにく": "少々", "しょうが": "少々", "豆板醤": "小さじ0.5"},
            "link": "https://www.instagram.com/reel/C9KRBhVS9E8/?igsh=MWc1YWUyeTd3MG9qcQ=="
        },
        "サバの味噌煮": {
            "ingredients": {"サバ": "2切れg", "しょうがチューブ": "適量"},
            "link": "https://delishkitchen.tv/recipes/449561114036929616"
        },
        "白身魚のマヨ醤油": {
            "ingredients": {"タラ": "3切れ"},
            "link": "https://www.instagram.com/p/DINcp4Mp7sS/?igsh=azd2b3k2ZDVjMGtp&img_index=1"
        },
        "タラのホイル焼き": {
            "ingredients": {"タラ": "2切れ", "しめじ": "1個", "玉ねぎ": "1/4個", "しょうがチューブ": "適量",},
            "link": "https://www.instagram.com/p/CHuF6x_JQUj/?igsh=Zm5ibDRycWM4enp5&img_index=1"
        },
        "からあげ": {
            "ingredients": {"鶏もも肉": "1枚", "にんにく": "少々", "しょうが": "少々", "鶏がらのもと": "小さじ1/2", "片栗粉": "適量"},
            "link": "https://cookpad.com/jp/recipes/19108352-%E7%B5%B6%E5%93%81-%E3%81%8B%E3%82%89%E6%8F%9A%E3%81%92"
        },
        "ミルフィーユかつ": {
            "ingredients": {"豚ばら肉": "400g", "卵": "1個", "小麦粉": "大さじ2", "パン粉": "適量"},
            "link": "https://www.instagram.com/p/Cn3PIDuPdUp/?img_index=5&igsh=dGdpdjFuZmg1MHBs"
        },        
        "エビカツ": {
            "ingredients": {"むき海老": "200g", "はんぺん": "1枚", "パン粉": "大さじ3", "片栗粉": "大さじ1", "鶏がらのもと": "小さじ1", "にんにくチューブ": "適量"},
            "link": "https://www.instagram.com/p/Cv9qonmJvDD/?img_index=5&igsh=MWFzMXU1aDlyMG5mcQ%3D%3D"
        },
        "タルタル鮭フライ": {
            "ingredients": {"鮭": "2切れ", "薄力粉": "大さじ2", "パン粉": "適量", "卵": "1個", "玉ねぎ": "1/8個", "マヨネーズ": "大さじ3"},
            "link": "https://www.instagram.com/p/C4wG1VDBfJE/?igsh=MXNoaGxxbnFicWVwdw%3D%3D&img_index=1"
        }
    },
    "副菜": {
        "基本サラダ": {
            "ingredients": {"レタス": "1玉", "トマト": "2個", "きゅうり": "1本", "アボカド": "1個"},
            "link": ""
        },
        "やみつき甘辛れんこん": {
            "ingredients": {"れんこん": "150g"},
            "link": "https://www.instagram.com/p/CJsa_I9JQr7/?igsh=MXA3Y2pqaDVrYmkxMg=="
        }
    },
    "汁": {
        "どさんこ汁": {
            "ingredients": {"じゃがいも": "2個", "にんじん": "1/2個", "玉ねぎ": "1/2個",
                "豚こま肉": "150g", "コーン": "50g", "乾燥わかめ": "大さじ1.5"},
             "link": "https://www.instagram.com/p/DH5eKCGzT5c/?img_index=5&igsh=MWxweW4zZGM3aW1qdA=="
        },
        "春キャベツの味噌スープ": {
            "ingredients": {"キャベツ": "1/8個", "にんじん": "1/2本", "ウインナー": "5本", "コーン": "大さじ4", "豆乳": "300ml", "コンソメ": "1個", "しょうがチューブ": "少々"},
            "link": "https://www.instagram.com/reel/DIVoFpUBxQj/?igsh=MWN3bmI4ZGtzdW5uaw%3D%3D"
        },
        }
    }
}

category_map = {
    "玉ねぎ": "野菜", "レタス": "野菜", "トマト": "野菜", "きゅうり": "野菜",
    "じゃがいも": "野菜", "にんじん": "野菜", "コーン": "野菜", "アボカド": "野菜", "れんこん": "野菜",
    "鮭": "魚", "むき海老": "魚", "サバ": "魚", "タラ": "魚",
    "豚挽き肉": "肉", "豚こま肉": "肉", "豚ばら肉": "肉", "鶏もも肉": "肉", "ウインナー": "肉",
    "パン粉": "その他", "小麦粉": "その他", "卵": "その他", "豆腐": "その他",
    "乾燥わかめ": "その他", "にんにく": "その他", "しょうが": "その他", "豆乳": "その他",
    "豆板醤": "調味料", "味噌": "調味料", "塩": "調味料", "鶏がらのもと": "調味料", "片栗粉": "調味料", "マヨネーズ": "調味料", "にんにくチューブ": "調味料", "しょうがチューブ": "調味料", "コンソメ": "調味料"

}

DATA_FILE = "kondate_data.json"

# ------------------------------
# データ保存・読み込み
# ------------------------------
def save_menu_to_json(date_str, menu):
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
    else:
        data = {}
    data[date_str] = menu
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def load_menu_from_json(date_str):
    if not os.path.exists(DATA_FILE):
        return None
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)
    return data.get(date_str)

# ------------------------------
# 材料の数値を合算する関数
# ------------------------------
def sum_ingredients(qty_list):
    total = defaultdict(Fraction)
    for qty in qty_list:
        for unit in ["個", "枚", "本", "g", "ml", "玉", "丁", "切れ", "大さじ", "小さじ", "少々", "適量"]:
            if unit in qty:
                num_part = qty.replace(unit, "").strip()
                try:
                    number = Fraction(num_part)
                    total[unit] += number
                except:
                    pass
                break
        else:
            total[""] += 1
    return "、".join([f"{float(num):g}{unit}" if unit else str(float(num)) for unit, num in total.items()])

# ------------------------------
# アプリUI
# ------------------------------
if "initialized" not in st.session_state:
    st.session_state.initialized = True
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
# まとめボタン処理
# ------------------------------
if st.button("買い物リストをまとめる"):
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
            if dish_name != "無し":
                ingredients = menu_data[dish_type][dish_name]["ingredients"]
                for item, qty in ingredients.items():
                    ingredient_totals[item].append(qty)

    # カテゴリごとに集計表示
    categorized = defaultdict(dict)
    for item, qtys in ingredient_totals.items():
        category = category_map.get(item, "その他")
        categorized[category][item] = sum_ingredients(qtys)

    # ✅ 一度だけ表示される「買い物リスト」
    st.header("🛒 買い物リスト")
    categorized = defaultdict(dict)
    for item, qtys in ingredient_totals.items():
        category = category_map.get(item, "その他")
        categorized[category][item] = sum_ingredients(qtys)

    for category in ["野菜", "肉", "魚", "調味料", "その他"]:
        if category in categorized:
            st.subheader(f"【{category}】")
            for item, total in categorized[category].items():
                st.write(f"- {item}：{total}")

    # ✅ 一度だけ表示される「作り方リンク」
    st.header("📖 作り方リンク")
    for menu in selected_menus:
        st.subheader(f"{menu['date']} の献立")
        for dish_type in ["主菜", "副菜", "汁"]:
            dish_key = dish_key_map[dish_type]
            dish_name = menu[dish_key]
            if dish_name != "無し":
                link = menu_data[dish_type][dish_name]["link"]
                if link:
                    st.markdown(f"- [{dish_type}：{dish_name}]({link})")
                else:
                    st.write(f"- {dish_type}：{dish_name}（リンクなし）")

# ------------------------------
# 過去の献立をカレンダーから表示
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
