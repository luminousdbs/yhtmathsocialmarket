import html
from datetime import datetime

import streamlit as st


BUDGET = 20_000
CASH_TO_PAY = 20_000
ITEMS = [
    {"id": "apple", "name": "사과", "price": 700, "bundle_size": 6, "emoji": "🍎", "color": "#ffe0dc"},
    {"id": "banana", "name": "바나나", "price": 500, "bundle_size": 8, "emoji": "🍌", "color": "#fff2bd"},
    {"id": "bread", "name": "빵", "price": 1_200, "bundle_size": 3, "emoji": "🥐", "color": "#ffe5bf"},
    {"id": "milk", "name": "우유", "price": 900, "bundle_size": 4, "emoji": "🥛", "color": "#e4f2ff"},
    {"id": "juice", "name": "주스", "price": 800, "bundle_size": 5, "emoji": "🧃", "color": "#ffebc2"},
    {"id": "pencil", "name": "연필", "price": 500, "bundle_size": 8, "emoji": "✏️", "color": "#fff1bd"},
    {"id": "notebook", "name": "공책", "price": 1_000, "bundle_size": 4, "emoji": "📒", "color": "#e1f3df"},
    {"id": "crayons", "name": "색연필", "price": 1_500, "bundle_size": 3, "emoji": "🖍️", "color": "#f8e2ff"},
    {"id": "rope", "name": "줄넘기", "price": 2_500, "bundle_size": 2, "emoji": "🪢", "color": "#e3e7ff"},
    {"id": "ball", "name": "공", "price": 3_000, "bundle_size": 2, "emoji": "⚽", "color": "#e4f4ff"},
    {"id": "stickers", "name": "스티커", "price": 300, "bundle_size": 10, "emoji": "⭐", "color": "#fff1d6"},
    {"id": "cards", "name": "카드 게임", "price": 2_000, "bundle_size": 2, "emoji": "🃏", "color": "#ffe4ec"},
    {"id": "cap", "name": "야구 모자", "price": 2_500, "bundle_size": 2, "emoji": "🧢", "color": "#e1efff"},
    {"id": "flower", "name": "꽃씨", "price": 600, "bundle_size": 6, "emoji": "🌷", "color": "#fce4f2"},
    {"id": "console", "name": "휴대용 게임기", "price": 8_000, "bundle_size": 2, "emoji": "🎮", "color": "#e5e3ff"},
    {"id": "game_cartridge", "name": "게임 칩", "price": 4_000, "bundle_size": 2, "emoji": "🕹️", "color": "#e4f4ff"},
    {"id": "headphones", "name": "유선 헤드폰", "price": 5_000, "bundle_size": 2, "emoji": "🎧", "color": "#ffe4ec"},
    {"id": "robot", "name": "로봇 장난감", "price": 6_000, "bundle_size": 2, "emoji": "🤖", "color": "#e1f3df"},
]
ITEMS_BY_ID = {item["id"]: item for item in ITEMS}
ITEMS_BY_NAME = {item["name"]: item for item in ITEMS}

st.set_page_config(page_title="나만의 돈 관리 시장 게임", page_icon="🛍️", layout="wide")
st.markdown(
    """
    <style>
      .stApp {
        background: linear-gradient(145deg, #fff9e8 0%, #fff1df 55%, #ffe9e8 100%);
      }
      .main .block-container { max-width: 1400px; padding-top: 2rem; }
      .market-banner {
        padding: 1.15rem 1.4rem; margin-bottom: 1rem; border-radius: 20px;
        color: #5a3518; background: linear-gradient(100deg, #ffd36e, #ffae75);
        border: 2px solid #f59b4a; box-shadow: 0 5px 14px #b26a3020;
      }
      .product-photo {
        display: grid; place-items: center; height: 110px; margin: .25rem 0 .7rem;
        border: 2px solid #ffffff; border-radius: 18px; font-size: 4.3rem;
        box-shadow: inset 0 0 0 1px #70421b18;
      }
      div[data-testid="stVerticalBlockBorderWrapper"] {
        background-color: #fffdf8;
        border-color: #f3d9b8;
      }
      div.stButton > button {
        border-radius: 12px; border: 1px solid #edbd79; color: #573616;
        background: #fff2d6; font-weight: 650;
      }
      div.stButton > button:hover { border-color: #e88c38; color: #713e16; }
    </style>
    """,
    unsafe_allow_html=True,
)

if "game_phase" not in st.session_state:
    st.session_state.game_phase = "shopping"
if "cart" not in st.session_state:
    st.session_state.cart = {
        item["id"]: {"single": 0, "bundle": 0} for item in ITEMS
    }
if "opportunity_cost_choice" not in st.session_state:
    st.session_state.opportunity_cost_choice = "선택해 주세요"


def won(amount):
    return f"{amount:,}원"


def item_units(item, counts):
    return counts["single"] + counts["bundle"] * item["bundle_size"]


def cart_total(cart):
    return sum(
        item["price"] * item_units(item, cart[item["id"]])
        for item in ITEMS
    )


def add_to_cart(item_id, kind):
    updated_cart = {
        key: counts.copy() for key, counts in st.session_state.cart.items()
    }
    updated_cart[item_id][kind] += 1
    st.session_state.cart = updated_cart


def remove_from_cart(item_id, kind):
    updated_cart = {
        key: counts.copy() for key, counts in st.session_state.cart.items()
    }
    updated_cart[item_id][kind] = max(0, updated_cart[item_id][kind] - 1)
    st.session_state.cart = updated_cart


def make_receipt(cart, total, opportunity_cost):
    lines = [
        "나만의 돈 관리 시장 게임 영수증",
        f"구매 시각: {datetime.now().strftime('%Y-%m-%d %H:%M')}",
        "-" * 30,
    ]
    for item in ITEMS:
        counts = cart[item["id"]]
        units = item_units(item, counts)
        if units:
            choices = []
            if counts["single"]:
                choices.append(f"낱개 {counts['single']}개")
            if counts["bundle"]:
                choices.append(
                    f"묶음 {counts['bundle']}개 "
                    f"({item['bundle_size']}개씩)"
                )
            lines.append(
                f"{item['name']} {', '.join(choices)} = {units}개, "
                f"{won(item['price'] * units)}"
            )
    lines.extend(
        [
            "-" * 30,
            f"구매한 물건 합계: {won(total)}",
            f"처음 예산: {won(BUDGET)}",
            f"남은 예산: {won(BUDGET - total)}",
            f"낸 돈: {won(CASH_TO_PAY)}",
            f"거스름돈: {won(CASH_TO_PAY - total)}",
        ]
    )
    if opportunity_cost:
        item = ITEMS_BY_NAME[opportunity_cost]
        lines.append(
            f"이번에 포기한 대안: {opportunity_cost} ({won(item['price'])} / 개)"
        )
    lines.extend(["-" * 30, "오늘의 배움: 필요한 것과 원하는 것을 생각해 돈을 써요!"])
    return "\n".join(lines)


def make_printable_receipt(receipt):
    escaped_lines = "".join(
        f"<p>{html.escape(line)}</p>" for line in receipt.splitlines()
    )
    return f"""<!doctype html>
<html lang="ko">
<meta charset="utf-8">
<title>시장 게임 영수증</title>
<style>
  body {{ max-width: 560px; margin: 40px auto; padding: 24px; font-family: sans-serif; }}
  h1 {{ font-size: 1.4rem; }}
  p {{ margin: 8px 0; }}
  @media print {{ body {{ margin: 0 auto; }} }}
</style>
<h1>🛍️ 시장 게임 영수증</h1>
{escaped_lines}
</html>"""


def render_cart(cart, editable=True):
    st.subheader("🧺 내 장바구니")
    has_items = False
    for item in ITEMS:
        counts = cart[item["id"]]
        units = item_units(item, counts)
        if not units:
            continue
        has_items = True
        with st.container(border=True):
            st.markdown(f"**{item['emoji']} {item['name']}**")
            st.caption(
                f"낱개 {counts['single']}개 + 묶음 {counts['bundle']}개 "
                f"({item['bundle_size']}개씩) = {units}개"
            )
            st.write(won(item["price"] * units))
            if editable:
                remove_cols = st.columns(2)
                if counts["single"]:
                    remove_cols[0].button(
                        "− 낱개",
                        key=f"remove_single_{item['id']}",
                        on_click=remove_from_cart,
                        args=(item["id"], "single"),
                        use_container_width=True,
                    )
                if counts["bundle"]:
                    remove_cols[1].button(
                        "− 묶음",
                        key=f"remove_bundle_{item['id']}",
                        on_click=remove_from_cart,
                        args=(item["id"], "bundle"),
                        use_container_width=True,
                    )
    if not has_items:
        st.info("아직 담은 상품이 없어요. 왼쪽 가게에서 골라 보세요!")


st.markdown(
    """
    <div class="market-banner">
      <h1>🎪 알뜰살뜰 우리 동네 시장</h1>
      <b>상품 그림을 보고 낱개나 묶음을 골라 담아 보세요!</b>
    </div>
    """,
    unsafe_allow_html=True,
)
st.title("🛍️ 나만의 돈 관리 시장 게임")
st.subheader("초등 4학년 경제 | 사고 싶은 물건을 고르고 똑똑하게 계산해요!")
st.progress(
    {"shopping": 0.33, "change": 0.66, "complete": 1.0}[
        st.session_state.game_phase
    ],
    text="장바구니 담기 → 합계 계산 → 거스름돈 계산",
)

with st.container(border=True):
    st.markdown("### 📣 오늘의 시장 미션")
    st.write(
        "학교 축제에서 쓸 물건을 사러 왔어요. "
        f"쓸 수 있는 돈은 **{won(BUDGET)}**이고, 계산대에 "
        f"**{won(CASH_TO_PAY)}**을 낼 거예요."
    )
    st.info("예산을 확인하고 필요한 물건을 골라요. 묶음은 낱개 가격으로 직접 계산해요!")

if st.session_state.game_phase == "shopping":
    st.header("1단계: 상품을 골라 장바구니에 담아요")
    market_col, cart_col = st.columns([1.8, 1])
    cart = st.session_state.cart

    with market_col:
        st.markdown(
            '<div class="market-banner"><b>🏪 싱싱가게 · 문구가게 · 놀이가게</b>'
            "</div>",
            unsafe_allow_html=True,
        )
        product_columns = st.columns(2)
        for index, item in enumerate(ITEMS):
            with product_columns[index % 2]:
                with st.container(border=True):
                    st.markdown(
                        f'<div class="product-photo" style="background:{item["color"]}" '
                        f'role="img" aria-label="{item["name"]} 그림">'
                        f'{item["emoji"]}</div>',
                        unsafe_allow_html=True,
                    )
                    st.markdown(f"#### {item['name']}")
                    st.write(f"낱개 가격: **{won(item['price'])} / 개**")
                    st.caption(
                        f"묶음: {item['bundle_size']}개 "
                        "(묶음 가격은 직접 계산해요!)"
                    )
                    single_col, bundle_col = st.columns(2)
                    single_col.button(
                        f"{item['emoji']} 낱개 담기",
                        key=f"add_single_{item['id']}",
                        on_click=add_to_cart,
                        args=(item["id"], "single"),
                        use_container_width=True,
                    )
                    bundle_col.button(
                        f"📦 묶음 담기",
                        key=f"add_bundle_{item['id']}",
                        on_click=add_to_cart,
                        args=(item["id"], "bundle"),
                        use_container_width=True,
                    )

    with cart_col:
        render_cart(cart)
        total = cart_total(cart)
        remaining = BUDGET - total
        st.metric("장바구니 합계", won(total))
        st.metric("남은 예산", won(remaining))

        selected_items = [
            item for item in ITEMS if item_units(item, cart[item["id"]]) > 0
        ]
        unselected_items = [
            item for item in ITEMS if item_units(item, cart[item["id"]]) == 0
        ]

        if total > BUDGET:
            st.warning("예산을 넘었어요. 장바구니에서 상품을 빼 주세요.")
        elif selected_items:
            st.markdown("#### 💭 이번에 포기한 대안")
            st.caption("사지 않은 물건 중 가장 아쉬운 것을 골라 보세요.")
            opportunity_options = [
                "선택해 주세요",
                *[item["name"] for item in unselected_items],
            ]
            if (
                st.session_state.opportunity_cost_choice
                not in opportunity_options
            ):
                st.session_state.opportunity_cost_choice = "선택해 주세요"
            opportunity_cost = st.selectbox(
                "포기한 물건",
                opportunity_options,
                key="opportunity_cost_choice",
            )
            with st.form("total_form"):
                total_answer = st.number_input(
                    "계산한 물건값 합계 (원)",
                    min_value=0,
                    max_value=BUDGET * 10,
                    step=100,
                    key="total_answer",
                )
                total_submitted = st.form_submit_button("합계 확인하기")

            if total_submitted:
                if opportunity_cost == "선택해 주세요":
                    st.warning("포기한 대안도 하나 골라 주세요.")
                elif total_answer != total:
                    st.error(f"다시 계산해 봐요. 합계는 {won(total)}이에요.")
                else:
                    st.session_state.saved_cart = {
                        item["id"]: cart[item["id"]].copy() for item in ITEMS
                    }
                    st.session_state.saved_opportunity_cost = opportunity_cost
                    st.session_state.game_phase = "change"
                    st.rerun()
        else:
            st.caption("상품을 담으면 합계를 확인하고 계산 퀴즈를 시작할 수 있어요.")

elif st.session_state.game_phase == "change":
    cart = st.session_state.saved_cart
    total = cart_total(cart)
    st.header("2단계: 거스름돈을 계산해요")
    st.write(
        f"물건값은 **{won(total)}**이고, 계산대에 **{won(CASH_TO_PAY)}**을 냈어요. "
        "거스름돈은 얼마일까요?"
    )
    st.caption("낸 돈에서 물건값을 빼면 거스름돈을 알 수 있어요.")
    with st.form("change_form"):
        change_answer = st.number_input(
            "내가 계산한 거스름돈 (원)",
            min_value=0,
            max_value=CASH_TO_PAY,
            step=100,
        )
        change_submitted = st.form_submit_button("거스름돈 확인하고 구매 완료")

    if change_submitted:
        correct_change = CASH_TO_PAY - total
        if change_answer != correct_change:
            st.error(f"다시 계산해 봐요. 거스름돈은 {won(correct_change)}이에요.")
        else:
            st.session_state.game_phase = "complete"
            st.rerun()

else:
    cart = st.session_state.saved_cart
    total = cart_total(cart)
    opportunity_cost = st.session_state.get("saved_opportunity_cost", "")
    receipt = make_receipt(cart, total, opportunity_cost)

    st.header("🎉 구매 완료! 소비를 돌아봐요")
    st.success(
        f"합계 {won(total)}과 거스름돈 {won(CASH_TO_PAY - total)}을 "
        "모두 맞혔어요!"
    )
    st.markdown("### 🧺 나의 장바구니")
    render_cart(cart, editable=False)
    st.markdown("### 🔎 나의 소비 분석")
    st.write(f"- 처음 예산 {won(BUDGET)} 중 {won(total)}을 썼어요.")
    st.write(f"- 사고 남은 예산은 **{won(BUDGET - total)}**이에요.")
    if opportunity_cost:
        forgone_item = ITEMS_BY_NAME[opportunity_cost]
        st.write(
            f"- 이번에 가장 아쉬워하며 포기한 대안은 "
            f"**{opportunity_cost}**({won(forgone_item['price'])} / 개)예요."
        )
    st.info(
        "**기회비용**은 하나를 선택해서 다른 것을 포기할 때, "
        "포기한 것 중 가장 아쉬운 대안이에요. "
        "예산이 한정되어 있어서 무엇을 살지 고르는 순간 기회비용이 생겨요."
    )
    st.markdown("### 🧾 영수증")
    st.caption("아래 영수증을 복사해 공유하거나 파일로 내려받아 인쇄할 수 있어요.")
    st.text_area("복사해서 공유할 영수증", value=receipt, height=280)

    text_col, print_col = st.columns(2)
    text_col.download_button(
        "영수증 내려받기 (공유용)",
        data=receipt,
        file_name="시장_게임_영수증.txt",
        mime="text/plain",
        use_container_width=True,
    )
    print_col.download_button(
        "인쇄용 영수증 내려받기",
        data=make_printable_receipt(receipt),
        file_name="시장_게임_영수증.html",
        mime="text/html",
        use_container_width=True,
    )
    st.caption("인쇄용 파일을 열고 브라우저에서 인쇄를 선택하세요.")
    if st.button("새 게임 시작"):
        for key in ("total_answer", "saved_cart", "saved_opportunity_cost"):
            st.session_state.pop(key, None)
        st.session_state.cart = {
            item["id"]: {"single": 0, "bundle": 0} for item in ITEMS
        }
        st.session_state.opportunity_cost_choice = "선택해 주세요"
        st.session_state.game_phase = "shopping"
        st.rerun()
