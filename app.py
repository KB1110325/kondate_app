import streamlit as st
import datetime
import json
import os
from collections import defaultdict
from fractions import Fraction


# --- パスワード認証 ---
PASSWORD = "0524"
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
            "ingredients": {"豆腐": "1丁", "豚ひき肉": "150g", "にんにく": "少々", "しょうが": "少々", "豆板醤": "小さじ0.5"},
            "link": "https://www.instagram.com/reel/C9KRBhVS9E8/?igsh=MWc1YWUyeTd3MG9qcQ=="
        },
        "サバの味噌煮": {
            "ingredients": {"サバ": "2切れ", "しょうがチューブ": "適量"},
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
            "ingredients": {"むき海老": "200g", "はんぺん": "1枚", "パン粉": "大さじ3", "片栗粉": "大さじ1", "鶏がらのもと": "小さじ1", 
            "にんにくチューブ": "適量"},
            "link": "https://www.instagram.com/p/Cv9qonmJvDD/?img_index=5&igsh=MWFzMXU1aDlyMG5mcQ%3D%3D"
        },
        "タルタル鮭フライ": {
            "ingredients": {"鮭": "2切れ", "薄力粉": "大さじ2", "パン粉": "適量", "卵": "1個", "玉ねぎ": "1/8個", "マヨネーズ": "大さじ3"},
            "link": "https://www.instagram.com/p/C4wG1VDBfJE/?igsh=MXNoaGxxbnFicWVwdw%3D%3D&img_index=1"
        },        
        "豚バラコーンペッパーライス": {
            "ingredients": {"豚ばら肉": "150g", "コーン": "120g", "バター": "10g", "にんにくチューブ": "小さじ1", "鶏がらのもと": "小さじ1"},
            "link": "https://www.instagram.com/p/DIEKhwZTAk4/?igsh=MWo1ZTVocmt4OGYwMg%3D%3D&img_index=1"
        },        
        "ミートパスタ": {
            "ingredients": {"豚ひき肉": "200g", "玉ねぎ": "1個", "ホールトマト": "1缶", "にんにく": "2片", "にんじん": "1本", 
            "ウスターソース": "大さじ1", "コンソメ": "大さじ1/2", "小麦粉": "大さじ1", "しいたけ": "3個"},
            "link": "https://cookpad.com/jp/recipes/17509648-%E7%B0%A1%E5%8D%98%E3%83%9F%E3%83%BC%E3%83%88%E3%82%BD%E3%83%BC%E3%82%B9"
        },
        "ツナ塩昆布バターパスタ": {
            "ingredients": {"ツナ缶": "1缶", "しめじ": "1袋", "塩昆布": "15g", "バター": "15g"},
            "link": "https://www.instagram.com/p/C6Pe_3vBXXa/?igsh=bW1nczZoMnF4cjhr&img_index=1"
        }

    },
    "副菜": {
        "基本サラダ": {
            "ingredients": {"レタス": "1玉", "トマト": "2個", "きゅうり": "1本", "アボカド": "1個"},
            "link": ""
        },
        "ひじきの煮物": {
            "ingredients": {"乾燥ひじき": "15g", "にんじん": "1/2本", "油揚げ": "1枚"},
            "link": "https://cookpad.com/jp/recipes/19415522-%E3%81%B2%E3%81%98%E3%81%8D%E3%81%AE%E7%85%AE%E7%89%A9"
        },
        "れんこんゆかり和え": {
            "ingredients": {"れんこん": "200g", "ゆかり": "小さじ2"},
            "link": "https://www.kurashiru.com/recipes/536d89bc-2a89-4197-a9fb-09bb5a9a8abc"
        },
        "なすの揚げびたし": {
            "ingredients": {"なす": "2本", "しょうがチューブ": "少々", "かつお節": "1袋", "白だし": "大さじ1/2"},
            "link": "https://cookien.com/recipe/2690/"
        },
        "こんにゃくの田楽風": {
            "ingredients": {"こんにゃく": "200g"},
            "link": "https://cookpad.com/jp/recipes/21538189-%E5%B0%8F%E3%81%95%E3%81%AA%E3%81%93%E3%82%93%E3%81%AB%E3%82%83%E3%81%8F%E3%81%AE%E3%81%94%E3%81%BE%E5%91%B3%E5%99%8C%E7%94%B0%E6%A5%BD%E9%A2%A8"
        },
        "青菜炒め": {
            "ingredients": {"ほうれん草": "1袋", "鶏がらのもと": "小さじ1", "にんにく": "1片"},
            "link": "https://cookpad.com/jp/recipes/18563383-%E7%B0%A1%E5%8D%98%E3%82%B7%E3%83%B3%E3%83%97%E3%83%AB%E9%9D%92%E8%8F%9C%E7%82%92%E3%82%81"
        },
        "やみつき甘辛れんこん": {
            "ingredients": {"れんこん": "150g"},
            "link": "https://www.instagram.com/p/CJsa_I9JQr7/?igsh=MXA3Y2pqaDVrYmkxMg=="
        }
    },
    "汁": {
        "どさんこ汁": {
            "ingredients": {"じゃがいも": "2個", "にんじん": "1/2本", "玉ねぎ": "1/2個",
                "豚こま肉": "150g", "コーン": "50g", "乾燥わかめ": "大さじ1.5"},
             "link": "https://www.instagram.com/p/DH5eKCGzT5c/?img_index=5&igsh=MWxweW4zZGM3aW1qdA=="
        },
        "ポトフ": {
            "ingredients": {"じゃがいも": "2個", "にんじん": "1本", "玉ねぎ": "1個",
                "キャベツ": "1/4個", "ウインナー": "5本",  "コンソメ": "1個","にんにく": "1片"},
             "link": "https://www.instagram.com/reel/C5uCWZDSIUo/?igsh=cWVtbjlmc2xvY3Qy"
        },
        "豆乳コーンスープ": {
            "ingredients": {"豆乳": "200ml", "コーンクリーム缶": "1個", "コンソメ": "1個"},
             "link": "https://www.kurashiru.com/recipes/72fa81fb-b412-4017-82ba-2b96cd3aba8a"
        },
        "春キャベツの味噌スープ": {
            "ingredients": {"キャベツ": "1/8個", "にんじん": "1/2本", "ウインナー": "5本", "コーン": "大さじ4", "豆乳": "300ml", 
             "コンソメ": "1個", "しょうがチューブ": "少々"},
            "link": "https://www.instagram.com/reel/DIVoFpUBxQj/?igsh=MWN3bmI4ZGtzdW5uaw%3D%3D"
        }
    }
}

category_map = {
    "玉ねぎ": "野菜", "レタス": "野菜", "トマト": "野菜", "きゅうり": "野菜", "キャベツ": "野菜", "しいたけ": "野菜",
    "じゃがいも": "野菜", "にんじん": "野菜", "コーン": "野菜", "アボカド": "野菜", "れんこん": "野菜", "しめじ": "野菜", "ほうれん草": "野菜",
    "鮭": "魚", "むき海老": "魚", "サバ": "魚", "タラ": "魚",
    "豚ひき肉": "肉", "豚こま肉": "肉", "豚ばら肉": "肉", "鶏もも肉": "肉", "ウインナー": "肉",
    "パン粉": "その他", "小麦粉": "その他", "卵": "その他", "豆腐": "その他", "油揚げ": "その他", "こんにゃく": "その他",
    "乾燥わかめ": "その他", "にんにく": "その他", "しょうが": "その他", "豆乳": "その他", "ツナ缶": "その他", "塩昆布": "その他", 
    "バター": "その他", "ホールトマト": "その他", "コーンクリーム缶": "その他", "乾燥ひじき": "その他", "ゆかり": "その他",
    "豆板醤": "調味料", "味噌": "調味料", "塩": "調味料", "鶏がらのもと": "調味料", "小麦粉": "調味料", "片栗粉": "調味料", 
    "マヨネーズ": "調味料", "にんにくチューブ": "調味料", "しょうがチューブ": "調味料", "コンソメ": "調味料", "ウスターソース": "調味料"

}

# ---- JSON保存ファイル ----
DATA_FILE = "kondate_data.json"

# ---- データ保存・読み込み ----
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
        for unit in ["個", "枚", "本", "g", "ml", "玉", "丁", "切れ", "大さじ", "小さじ", "少々", "片", "袋", "缶", "適量"]:
            if unit in qty:
                num_part = qty.replace(unit, "").strip()
                try:
                    number = Fraction(num_part)
                    total[unit] += number
                except:
                    total[unit] += 1  # 単位はあるが数値として変換できない → 1つと仮定
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
    date = st.date_input(f"日付を選択（{i+1}日目）", value=start_date + datetime.timedelta(days=i), key=f"date_{i}")

    st.subheader("主菜の選択")
    main_dishes = list(menu_data["主菜"].keys())
    selected_main_dishes = st.multiselect("主菜を選んでください（最大3つ）", main_dishes, key=f"main_{i}")
    if len(selected_main_dishes) > 3:
        st.warning("主菜は最大3つまで選択できます。")
    selected_main_dishes = selected_main_dishes[:3]

    st.subheader("副菜の選択")
    side_dishes = list(menu_data["副菜"].keys())
    selected_side_dishes = st.multiselect("副菜を選んでください（最大3つ）", side_dishes, key=f"side_{i}")
    if len(selected_side_dishes) > 3:
        st.warning("副菜は最大3つまで選択できます。")
    selected_side_dishes = selected_side_dishes[:3]

    st.subheader("汁の選択")
    soups = list(menu_data["汁"].keys())
    selected_soups = st.multiselect("汁を選んでください（最大3つ）", soups, key=f"soup_{i}")
    if len(selected_soups) > 3:
        st.warning("汁物は最大3つまで選択できます。")
    selected_soups = selected_soups[:3]

    selected_menus.append({
        "date": str(date),
        "main": selected_main_dishes,
        "side": selected_side_dishes,
        "soup": selected_soups
    })

# ---- 保存ボタン ----
if st.button("この献立を保存する"):
    for menu in selected_menus:
        save_menu_to_json(menu["date"], menu)
    st.success("献立を保存しました！")

# ---- 買い物リストまとめ ----
if st.button("買い物リストをまとめる"):
    ingredient_totals = defaultdict(list)
    recipe_links_by_date = defaultdict(list)  # ← 作り方リンク用に初期化

    for menu in selected_menus:
        date = menu["date"]

        for dish_name in menu["main"]:
            ingredients = menu_data["主菜"][dish_name]["ingredients"]
            for item, qty in ingredients.items():
                ingredient_totals[item].append(qty)

            link = menu_data["主菜"][dish_name]["link"]
            recipe_links_by_date[date].append(("主菜", dish_name, link))

        for dish_name in menu["side"]:
            ingredients = menu_data["副菜"][dish_name]["ingredients"]
            for item, qty in ingredients.items():
                ingredient_totals[item].append(qty)

            link = menu_data["副菜"][dish_name]["link"]
            recipe_links_by_date[date].append(("副菜", dish_name, link))

        for dish_name in menu["soup"]:
            ingredients = menu_data["汁"][dish_name]["ingredients"]
            for item, qty in ingredients.items():
                ingredient_totals[item].append(qty)

            link = menu_data["汁"][dish_name]["link"]
            recipe_links_by_date[date].append(("汁", dish_name, link))

    # --- カテゴリごとにまとめて表示 ---
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

    # --- コピー用：買い物リスト ---
    shopping_text = ""
    for category in ["野菜", "肉", "魚", "調味料", "その他"]:
        if category in categorized:
            shopping_text += f"【{category}】\n"
            for item, total in categorized[category].items():
                shopping_text += f"- {item}：{total}\n"
            shopping_text += "\n"
    st.text_area("📋 コピー用：買い物リスト", shopping_text.strip(), height=250)
    
    # --- 作り方リンク表示 ---
    st.header("📖 作り方リンク")
    for date, recipes in recipe_links_by_date.items():
        st.subheader(f"{date} の献立")
        for category, name, link in recipes:
            if link:
                st.markdown(f"- {category}：[{name}]({link})")
            else:
                st.write(f"- {category}：{name}（リンクなし）")

    # --- コピー用：作り方リンク ---
    recipe_links_text = ""
    for date, recipes in recipe_links_by_date.items():
        recipe_links_text += f"[{date}]\n"
        for category, name, link in recipes:
            if link:
                recipe_links_text += f"・{category}：{name} → {link}\n"
            else:
                recipe_links_text += f"・{category}：{name}（リンクなし）\n"
        recipe_links_text += "\n"
    st.text_area("📋 コピー用：作り方リンク", recipe_links_text.strip(), height=300)

# ---- 過去の献立表示 ----
st.header("📅 カレンダーから過去の献立を確認")
selected_date = st.date_input("日付を選んで献立を表示", key="calendar_lookup")
menu = load_menu_from_json(str(selected_date))

if menu:
    st.subheader(f"{selected_date} の献立")
    st.write(f"- 主菜: {[dish for _, dish in menu['main']]}")
    st.write(f"- 副菜: {menu['side']}")
    st.write(f"- 汁物: {menu['soup']}")
else:
    st.info("この日には献立が登録されていません。")