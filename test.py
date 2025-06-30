import streamlit as st
from itertools import combinations_with_replacement
from collections import Counter

# キャラクターごとの技データ
character_moves = {
    "ルーク": {
        "立ち弱ｐ": {"normal": 22, "cancel": 22, "is_chain": False, "last_additional": 0},
        "立ち弱ｋ": {"normal": 18, "cancel": 18, "is_chain": False, "last_additional": 0},
        "立ち中P": {"normal": 28, "cancel": 28, "is_chain": False, "last_additional": 0},
        "立ち中ｋ": {"normal": 29, "cancel": 29, "is_chain": False, "last_additional": 0},
        "立ち強ｐ": {"normal": 35, "cancel": 35, "is_chain": False, "last_additional": 0},
        "立ち強ｋ": {"normal": 32, "cancel": 32, "is_chain": False, "last_additional": 0},
        "屈弱ｐ": {"normal": 15, "cancel": 12, "is_chain": True, "last_additional": 2},
        "屈弱ｋ": {"normal": 18, "cancel": 14, "is_chain": True, "last_additional": 1},
        "屈中ｐ": {"normal": 24, "cancel": 24, "is_chain": False, "last_additional": 0},
        "屈中ｋ": {"normal": 29, "cancel": 29, "is_chain": False, "last_additional": 0},
        "屈強ｐ": {"normal": 35, "cancel": 35, "is_chain": False, "last_additional": 0},
        "前中ｐ": {"normal": 43, "cancel": 43, "is_chain": False, "last_additional": 0},
        "前強ｐ": {"normal": 37, "cancel": 37, "is_chain": False, "last_additional": 0},
        "引き強ｐ": {"normal": 48, "cancel": 48, "is_chain": False, "last_additional": 0},
        "引き強ｋ": {"normal": 39, "cancel": 39, "is_chain": False, "last_additional": 0},
    },
    "ジェイミー": {
        "立ち弱ｐ(酔いレベル0)": {"normal": 13, "cancel": 13, "is_chain": False, "last_additional": 0},
        "立ち弱ｐ(酔いレベル1以上)": {"normal": 16, "cancel": 16, "is_chain": False, "last_additional": 0},
        "立ち弱ｋ": {"normal": 17, "cancel": 13, "is_chain": True, "last_additional": 0},
        "立ち中P": {"normal": 25, "cancel": 25, "is_chain": False, "last_additional": 0},
        "立ち中ｋ": {"normal": 29, "cancel": 29, "is_chain": False, "last_additional": 0},
        "立ち強ｐ": {"normal": 34, "cancel": 34, "is_chain": False, "last_additional": 0},
        "立ち強ｋ": {"normal": 38, "cancel": 38, "is_chain": False, "last_additional": 0},
        "屈弱ｐ": {"normal": 14, "cancel": 11, "is_chain": True, "last_additional": 1},
        "屈弱ｋ": {"normal": 17, "cancel": 13, "is_chain": True, "last_additional": 0},
        "屈中ｐ": {"normal": 23, "cancel": 23, "is_chain": False, "last_additional": 0},
        "屈中ｋ": {"normal": 27, "cancel": 27, "is_chain": False, "last_additional": 0},
        "屈強ｐ": {"normal": 35, "cancel": 35, "is_chain": False, "last_additional": 0},
        "屈強ｋ": {"normal": 43, "cancel": 43, "is_chain": False, "last_additional": 0},
        "前中ｋ": {"normal": 44, "cancel": 44, "is_chain": False, "last_additional": 0},
        "引き強ｐ": {"normal": 41, "cancel": 41, "is_chain": False, "last_additional": 0},
        "引き強ｐ(酔いレベル3以上)": {"normal": 42, "cancel": 42, "is_chain": False, "last_additional": 0},
        "前強ｋ": {"normal": 38, "cancel": 38, "is_chain": False, "last_additional": 0},
        "天晴脚(↓+ K同時押し)": {"normal": 33, "cancel": 33, "is_chain": False, "last_additional": 0},
    },
    "リュウ": {
        "立ち弱ｐ": {"normal": 13, "cancel": 9, "is_chain": True, "last_additional": 1},
        "立ち弱ｋ": {"normal": 18, "cancel": 18, "is_chain": False, "last_additional": 0},
        "立ち中P": {"normal": 20, "cancel": 20, "is_chain": False, "last_additional": 0},
        "立ち中ｋ": {"normal": 29, "cancel": 29, "is_chain": False, "last_additional": 0},
        "立ち強ｐ": {"normal": 32, "cancel": 32, "is_chain": False, "last_additional": 0},
        "立ち強ｋ": {"normal": 35, "cancel": 35, "is_chain": False, "last_additional": 0},
        "屈弱ｐ": {"normal": 14, "cancel": 12, "is_chain": True, "last_additional": 1},
        "屈弱ｋ": {"normal": 16, "cancel": 12, "is_chain": False, "last_additional": 0},
        "屈中ｐ": {"normal": 22, "cancel": 22, "is_chain": False, "last_additional": 0},
        "屈中ｋ": {"normal": 29, "cancel": 29, "is_chain": False, "last_additional": 0},
        "屈強ｐ": {"normal": 36, "cancel": 36, "is_chain": False, "last_additional": 0},
        "屈強ｋ": {"normal": 34, "cancel": 34, "is_chain": False, "last_additional": 0},
        "前中ｐ": {"normal": 42, "cancel": 42, "is_chain": False, "last_additional": 0},
        "前強ｐ": {"normal": 40, "cancel": 40, "is_chain": False, "last_additional": 0},
        "前強ｋ": {"normal": 39, "cancel": 39, "is_chain": False, "last_additional": 0},
        "引き強ｐ": {"normal": 36, "cancel": 36, "is_chain": False, "last_additional": 0},
        "引き強ｋ": {"normal": 44, "cancel": 44, "is_chain": False, "last_additional": 0},
    },
    "春麗": {
        "立ち弱ｐ": {"normal": 13, "cancel": 9, "is_chain": True, "last_additional": 1},
        "立ち弱ｋ": {"normal": 17, "cancel": 17, "is_chain": False, "last_additional": 0},
        "立ち中P": {"normal": 18, "cancel": 18, "is_chain": False, "last_additional": 0},
        "立ち中ｋ": {"normal": 26, "cancel": 26, "is_chain": False, "last_additional": 0},
        "立ち強ｐ": {"normal": 35, "cancel": 35, "is_chain": False, "last_additional": 0},
        "立ち強ｋ": {"normal": 34, "cancel": 34, "is_chain": False, "last_additional": 0},
        "屈弱ｐ": {"normal": 13, "cancel": 10, "is_chain": True, "last_additional": 0},
        "屈弱ｋ": {"normal": 15, "cancel": 12, "is_chain": False, "last_additional": 1},
        "屈中ｐ": {"normal": 23, "cancel": 23, "is_chain": False, "last_additional": 0},
        "屈中ｋ": {"normal": 28, "cancel": 28, "is_chain": False, "last_additional": 0},
        "屈強ｐ": {"normal": 41, "cancel": 41, "is_chain": False, "last_additional": 0},
        "屈強ｋ": {"normal": 33, "cancel": 33, "is_chain": False, "last_additional": 0},
        "前または引き中ｐ": {"normal": 24, "cancel": 24, "is_chain": False, "last_additional": 0},
        "前斜め強ｐ": {"normal": 36, "cancel": 36, "is_chain": False, "last_additional": 0},
        "前強ｋ": {"normal": 40, "cancel": 40, "is_chain": False, "last_additional": 0},
        "前斜め強ｋ": {"normal": 51, "cancel": 51, "is_chain": False, "last_additional": 0},
        "引き強ｐ": {"normal": 27, "cancel": 27, "is_chain": False, "last_additional": 0},
    },
    "テリー": {
        "立ち弱ｐ": {"normal": 13, "cancel": 9, "is_chain": True, "last_additional": 1},
        "立ち弱ｋ": {"normal": 18, "cancel": 18, "is_chain": False, "last_additional": 0},
        "立ち中P": {"normal": 25, "cancel": 25, "is_chain": False, "last_additional": 0},
        "立ち中ｋ": {"normal": 29, "cancel": 29, "is_chain": False, "last_additional": 0},
        "立ち強ｐ": {"normal": 30, "cancel": 30, "is_chain": False, "last_additional": 0},
        "立ち強ｋ": {"normal": 36, "cancel": 36, "is_chain": False, "last_additional": 0},
        "屈弱ｐ": {"normal": 14, "cancel": 10, "is_chain": True, "last_additional": 1},
        "屈弱ｋ": {"normal": 17, "cancel": 13, "is_chain": False, "last_additional": 0},
        "屈中ｐ": {"normal": 23, "cancel": 23, "is_chain": False, "last_additional": 0},
        "屈中ｋ": {"normal": 29, "cancel": 29, "is_chain": False, "last_additional": 0},
        "屈強ｐ": {"normal": 35, "cancel": 35, "is_chain": False, "last_additional": 0},
        "前強ｐ": {"normal": 43, "cancel": 43, "is_chain": False, "last_additional": 0},
    }
}

# 技フレーム計算ロジック
def compute_combo_total(combo, move_data):
    usage_tracker = Counter()
    total = 0
    detail = []

    for move in combo:
        usage_tracker[move] += 1
        count = usage_tracker[move]
        move_info = move_data[move]

        if move_info["is_chain"]:
            total_count = combo.count(move)
            if total_count == 1:
                frame = move_info["normal"]
                label = "N"
            else:
                if count == 1:
                    frame = move_info["normal"]
                    label = "N"
                elif count < total_count:
                    frame = move_info["cancel"]
                    label = "C"
                else:
                    frame = move_info["cancel"] + move_info["last_additional"]
                    label = f"C+{move_info['last_additional']}"
        else:
            frame = move_info["normal"]
            label = "N"

        total += frame
        detail.append((move, label))

    return total, detail

# コンボ検索
def find_frame_combos(move_data, target, tolerance=1):
    move_names = list(move_data.keys())
    results = []

    for r in range(1, 4):
        for combo in combinations_with_replacement(move_names, r):
            total, detail = compute_combo_total(combo, move_data)

            invalid = False
            for move in set(combo):
                if move_data[move]["is_chain"] and combo.count(move) > 1:
                    tags = [t for m, t in detail if m == move]
                    if all(t == "N" for t in tags):
                        invalid = True
                        break
            if invalid:
                continue

            if abs(total - target) <= tolerance:
                formatted = [f"{m}({t})" for m, t in detail]
                results.append((formatted, total))

    return sorted(results, key=lambda x: abs(x[1] - target))

# ==== Streamlit GUI ====

st.title("ストリートファイター6 技フレーム消費検索")
selected_char = st.selectbox("キャラクターを選択", list(character_moves.keys()))
target_frame = st.number_input(f"{selected_char}で消費したいフレーム数を入力", min_value=1, max_value=300, step=1)

if st.button("検索"):
    results = find_frame_combos(character_moves[selected_char], target_frame)
    if results:
        st.success(f"見つかった組み合わせ（上位5件）:")
        for detail, total in results[:5]:
            st.write(f"{' + '.join(detail)} = {total}F")
    else:
        st.warning("該当する技の組み合わせが見つかりませんでした。")
