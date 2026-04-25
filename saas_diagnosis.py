import os
import streamlit as st
import requests
from dotenv import load_dotenv

load_dotenv()

DISCORD_WEBHOOK = os.getenv("DISCORD_WEBHOOK_URL", "")
GAS_SHEETS_URL  = os.getenv("GAS_SHEETS_URL", "")

st.set_page_config(
    page_title="SaaS管理レベル診断 | 無料",
    page_icon="📊",
    layout="centered",
    initial_sidebar_state="collapsed",
)

st.markdown("""
<style>
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# ── ヘッダー ──────────────────────────────────────────────────────────────────
st.markdown("## 📊 SaaS管理レベル診断（無料）")
st.markdown("**5問・約3分**で、貴社のSaaS支出管理の現状がわかります。")
st.caption("IT部門・情報システム・調達・経営管理のご担当者向け")
st.divider()

# ── フォーム ──────────────────────────────────────────────────────────────────
with st.form("diagnosis"):

    q1 = st.radio(
        "**Q1. 貴社のSaaS・クラウドツールの月額費用、ざっくり把握できていますか？**",
        ["はい、だいたいわかる",
         "なんとなくはわかるが正確ではない",
         "正直、よくわからない",
         "部門ごとにバラバラで全社では把握できていない"],
        index=None,
    )
    st.write("")

    q2 = st.radio(
        "**Q2. 「誰も使っていないのに契約が続いていたツール」の経験はありますか？**",
        ["ある（気づいて解約した）",
         "おそらくあると思うが確認できていない",
         "ない",
         "考えたことがなかった"],
        index=None,
    )
    st.write("")

    q3 = st.multiselect(
        "**Q3. SaaS・ツールの契約状況、今どうやって管理していますか？（複数選択可）**",
        ["ExcelやGoogleスプレッドシートで管理",
         "専用のSaaS管理ツールを使っている",
         "経理・財務部門が管理している",
         "各部門バラバラで全社把握できていない",
         "ほぼ管理できていない",
         "その他"],
    )
    st.write("")

    q4 = st.radio(
        "**Q4. 「使われていないライセンスや重複契約を自動検出して削減提案を出してくれるツール」があれば使いたいですか？**",
        ["ぜひ使いたい",
         "詳しく話を聞いてみたい",
         "コスト・手間次第",
         "あまり使わないと思う"],
        index=None,
    )
    st.write("")

    q5 = st.radio(
        "**Q5. 月額いくらまでなら導入を検討しますか？**",
        ["月3万円以下",
         "月5万円以下",
         "月10万円以下",
         "月30万円以下",
         "削減できた額の一定割合（成果報酬型）なら検討",
         "価格より効果次第"],
        index=None,
    )

    st.divider()

    beta_email = st.text_input(
        "📩 βテスター登録（任意・先着10名）",
        placeholder="メールアドレスまたはLinkedInのURL",
        help="ツール完成後すぐにご連絡します。通常月額5〜10万円相当を無料でご提供します。",
    )

    submitted = st.form_submit_button("▶ 診断する", type="primary", use_container_width=True)

# ── 送信処理 ──────────────────────────────────────────────────────────────────
if submitted:
    # バリデーション
    missing = [f"Q{i}" for i, v in [(1, q1), (2, q2), (4, q4), (5, q5)] if v is None] + \
              (["Q3"] if not q3 else [])
    if missing:
        st.error(f"未回答の質問があります: {', '.join(sorted(missing))}")
        st.stop()

    # スコア計算
    score = 0
    score += {"はい、だいたいわかる": 2,
              "なんとなくはわかるが正確ではない": 1,
              "正直、よくわからない": 0,
              "部門ごとにバラバラで全社では把握できていない": 0}[q1]

    score += {"ある（気づいて解約した）": 1,
              "おそらくあると思うが確認できていない": 0,
              "ない": 2,
              "考えたことがなかった": 0}[q2]

    q3_pts = {"専用のSaaS管理ツールを使っている": 3,
              "経理・財務部門が管理している": 1,
              "ExcelやGoogleスプレッドシートで管理": 1}
    score += max((q3_pts.get(x, 0) for x in q3), default=0)

    # レベル判定
    LEVELS = {
        1: dict(
            name="コスト見えない状態", color="#FF4B4B", badge="🔴",
            waste="20〜30%",
            comment="月額SaaS費用の約20〜30%が無駄になっている可能性があります。",
            details=[
                "全社のSaaS契約を把握している人が誰もいない状態です",
                "シャドーIT（IT部門が知らない契約）が複数存在している可能性が高いです",
                "退職者のライセンスがそのまま課金され続けているケースが多く見られます",
            ],
            actions=[
                "全部門にSaaSアンケートを送り、使っているツールを全部洗い出す",
                "直近3ヶ月のクレジットカード・銀行明細でSaaS系の支払いを確認する",
                "90日以上ログインがないアカウントを各ツールの管理画面でチェックする",
            ],
        ),
        2: dict(
            name="なんとなく管理", color="#FF8C00", badge="🟠",
            waste="10〜20%",
            comment="月額SaaS費用の約10〜20%が無駄になっている可能性があります。",
            details=[
                "スプレッドシートや担当者の記憶に依存していて、リアルタイムな把握ができていません",
                "部門ごとの契約は把握できていても、利用率まで確認できていないケースが多いです",
                "契約更新日の把握が甘く、自動更新でそのまま継続されている契約があります",
            ],
            actions=[
                "全SaaS契約を1つのシートに集約し、月額・更新日・担当者を記録する",
                "四半期に1回、各ツールのアクティブユーザー数をライセンス数と比較する",
                "契約更新の60日前にリマインダーを設定して必ず見直すルールを作る",
            ],
        ),
        3: dict(
            name="管理しているが非効率", color="#DAA520", badge="🟡",
            waste="5〜15%",
            comment="月額SaaS費用の約5〜15%がまだ改善できる可能性があります。",
            details=[
                "管理の仕組みはあるものの、リアルタイムな利用状況の把握までは追いついていません",
                "手作業での管理はコストがかかっており、更新のたびに工数が発生しています",
                "類似機能を持つツールの重複契約が残っている可能性があります",
            ],
            actions=[
                "利用率の低いツールを四半期ごとに洗い出し、プランのダウングレードを検討する",
                "同じ機能を持つツールが複数ある場合、統合または片方の解約を検討する",
                "ベンダーとの次回更新時に利用実績データを持参して値引き交渉を行う",
            ],
        ),
        4: dict(
            name="最適化できている", color="#00C851", badge="🟢",
            waste="5〜10%",
            comment="管理レベルは高い状態です。さらに5〜10%の改善余地がある可能性があります。",
            details=[
                "SaaS管理の仕組みとしては整っている状態です",
                "次のステップは、手作業の自動化と継続的な最適化サイクルの構築です",
                "利用率データの自動収集とAIによる削減提案の自動化が有効です",
            ],
            actions=[
                "利用状況の自動収集とレポート生成を仕組み化して、管理工数をゼロに近づける",
                "ベンダーとの契約条件（割引・フレキシブルプラン）を定期的に再交渉する",
                "全社のSaaS支出をダッシュボードで可視化し、経営陣に定期報告できる体制を作る",
            ],
        ),
    }

    level_num = 1 if score <= 1 else 2 if score <= 3 else 3 if score <= 5 else 4
    lv = LEVELS[level_num]

    # ── 結果表示 ──────────────────────────────────────────────────────────────
    st.divider()
    st.markdown(f"## {lv['badge']} 診断結果")

    st.markdown(
        f'<div style="background:{lv["color"]}22;border-left:5px solid {lv["color"]};'
        f'padding:1.2rem;border-radius:8px;margin:0.5rem 0">'
        f'<h3 style="color:{lv["color"]};margin:0">レベル {level_num}：{lv["name"]}</h3>'
        f'<p style="margin:0.5rem 0 0 0;font-size:1.05rem">{lv["comment"]}</p>'
        f'</div>',
        unsafe_allow_html=True,
    )

    st.markdown("### 📋 現状の分析")
    for d in lv["details"]:
        st.markdown(f"- {d}")

    st.markdown("### ✅ 今すぐできる改善アクション")
    for i, a in enumerate(lv["actions"], 1):
        st.markdown(f"**{i}.** {a}")

    st.markdown(
        '<div style="background:#EBF4FF;border:2px solid #4A90D9;'
        'padding:1.2rem;border-radius:8px;margin:1.5rem 0;text-align:center">'
        '<h4 style="color:#4A90D9;margin:0 0 0.5rem 0">'
        '🚀 このプロセスをすべて自動化するツールを開発中です</h4>'
        '<p style="margin:0;color:#555">'
        'ライセンス利用率の自動収集・重複契約の検出・削減提案レポートを自動生成<br>'
        '<strong>βテスター先着10名に無料でご提供します</strong></p>'
        '</div>',
        unsafe_allow_html=True,
    )

    if beta_email:
        st.success(f"✅ βテスター登録完了（{beta_email}）\nツール完成後、最初にご連絡します！")

    # Google Sheets保存
    if GAS_SHEETS_URL:
        try:
            requests.post(
                GAS_SHEETS_URL,
                json={
                    "q1": q1, "q2": q2, "q3": ", ".join(q3),
                    "q4": q4, "q5": q5,
                    "beta_email": beta_email,
                    "level": level_num, "score": score,
                },
                timeout=5,
            )
        except Exception:
            pass

    # Discord通知
    if DISCORD_WEBHOOK:
        try:
            requests.post(
                DISCORD_WEBHOOK,
                json={"content": (
                    f"**📊 新しい診断回答**\n"
                    f"レベル: {lv['badge']} {level_num}（{lv['name']}）| スコア: {score}点\n\n"
                    f"Q1 費用把握: {q1}\n"
                    f"Q2 無駄経験: {q2}\n"
                    f"Q3 管理方法: {', '.join(q3)}\n"
                    f"Q4 ニーズ: {q4}\n"
                    f"Q5 価格感: {q5}\n"
                    f"βテスター: {beta_email or 'なし'}"
                )},
                timeout=5,
            )
        except Exception:
            pass
