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
st.markdown("**8問・約4分**で、貴社のSaaS支出管理の現状がわかります。")
st.caption("IT部門・情報システム・調達・経営管理のご担当者向け")
st.divider()

# ── フォーム ──────────────────────────────────────────────────────────────────
with st.form("diagnosis"):

    # ── 企業属性 ──────────────────────────────────────────────────────────────
    company_size = st.radio(
        "**Q1. 貴社の従業員数を教えてください**",
        ["〜50名（スタートアップ・小規模）",
         "51〜300名（中小企業）",
         "301〜1,000名（中堅企業）",
         "1,001〜5,000名（大企業）",
         "5,001名〜（エンタープライズ）"],
        index=None,
    )

    industry = st.selectbox(
        "業種（任意）",
        ["選択しない", "IT・ソフトウェア", "製造業", "金融・保険", "小売・EC",
         "サービス業", "メディア・広告", "医療・ヘルスケア", "建設・不動産", "教育", "その他"],
    )
    st.write("")

    # ── SaaS管理の現状 ────────────────────────────────────────────────────────
    q1 = st.radio(
        "**Q2. 貴社のSaaS・クラウドツールの月額費用、ざっくり把握できていますか？**",
        ["はい、だいたいわかる",
         "なんとなくはわかるが正確ではない",
         "正直、よくわからない",
         "部門ごとにバラバラで全社では把握できていない"],
        index=None,
    )
    st.write("")

    q2 = st.radio(
        "**Q3. 「誰も使っていないのに契約が続いていたツール」の経験はありますか？**",
        ["ある（気づいて解約した）",
         "おそらくあると思うが確認できていない",
         "ない",
         "考えたことがなかった"],
        index=None,
    )
    st.write("")

    q3 = st.multiselect(
        "**Q4. SaaS・ツールの契約状況、今どうやって管理していますか？（複数選択可）**",
        ["ExcelやGoogleスプレッドシートで管理",
         "専用のSaaS管理ツールを使っている",
         "経理・財務部門が管理している",
         "各部門バラバラで全社把握できていない",
         "ほぼ管理できていない",
         "その他"],
    )
    st.write("")

    most_painful_pattern = st.radio(
        "**Q5. 以下のうち、最も「もったいない」と感じる状況はどれですか？**",
        ["退職者のライセンスが残ったまま課金されている",
         "部門ごとに似た機能のツールが重複契約されている",
         "機能の半分も使っていないのに上位プランを契約している",
         "契約更新日を把握できておらず、気づいたら自動更新されている",
         "導入したが使いこなせていないツールに費用を払い続けている",
         "一部の人しか使っていないツールに全員分払っている",
         "トライアルや個別契約のツールが管理外で動いている",
         "そもそも何が無駄かわからない（可視化できていない）",
         "その他"],
        index=None,
    )

    other_pattern = st.text_input(
        "「その他」を選択の場合、具体的に教えてください（任意）",
        placeholder="例：ベンダーとの交渉機会を逃している　など",
    )
    st.write("")

    q4 = st.radio(
        "**Q6. 「使われていないライセンスや重複契約を自動検出して削減提案を出してくれるツール」があれば使いたいですか？**",
        ["ぜひ使いたい",
         "詳しく話を聞いてみたい",
         "コスト・手間次第",
         "あまり使わないと思う"],
        index=None,
    )
    st.write("")

    q5 = st.radio(
        "**Q7. 月額いくらまでなら導入を検討しますか？**",
        ["月3万円以下",
         "月5万円以下",
         "月10万円以下",
         "月30万円以下",
         "削減できた額の一定割合（成果報酬型）なら検討",
         "価格より効果次第"],
        index=None,
    )
    st.write("")

    current_tool_status = st.radio(
        "**Q8. 現在、SaaS管理ツール（Admina・Josys等）を使っていますか？**",
        ["現在使っている",
         "過去に検討したが導入していない",
         "検討したことはない",
         "そもそもそういうツールがあることを知らなかった"],
        index=None,
    )

    current_tool_name = st.text_input(
        "現在使っているツール名（任意・「現在使っている」を選択の場合）",
        placeholder="例：Admina、Josys、HENNGE One　など",
    )

    st.divider()

    st.markdown(
        '<div style="background:#EBF4FF;border:2px solid #4A90D9;'
        'padding:1.2rem;border-radius:8px;margin:0.5rem 0;text-align:center">'
        '<h4 style="color:#4A90D9;margin:0 0 0.5rem 0">'
        '🚀 このプロセスをすべて自動化するツールを開発中です</h4>'
        '<p style="margin:0;color:#555">'
        'ライセンス利用率の自動収集・重複契約の検出・削減提案レポートを自動生成。<br>'
        'βテスター<strong>先着10名</strong>に通常月額5〜10万円相当を<strong>無料</strong>でご提供します。<br>'
        '<span style="font-size:0.9rem;color:#777">参加ご希望の方は下のメールアドレス欄にご入力ください</span>'
        '</p>'
        '</div>',
        unsafe_allow_html=True,
    )

    st.info("📌 **個人情報について**　メールアドレスの入力は任意です。入力しない場合、個人情報は一切収集されません。回答データは統計目的のみに使用します。")

    beta_email = st.text_input(
        "📩 βテスター登録（任意・先着10名）",
        placeholder="メールアドレスまたはLinkedInのURL",
        help="ツール完成後すぐにご連絡します。通常月額5〜10万円相当を無料でご提供します。",
    )

    submitted = st.form_submit_button("▶ 診断する", type="primary", use_container_width=True)

# ── 送信処理 ──────────────────────────────────────────────────────────────────
if submitted:
    # バリデーション
    missing = (
        (["Q1"] if company_size is None else []) +
        ([f"Q{i}" for i, v in [(2, q1), (3, q2), (6, q4), (7, q5)] if v is None]) +
        (["Q4"] if not q3 else []) +
        (["Q5"] if most_painful_pattern is None else []) +
        (["Q8"] if current_tool_status is None else [])
    )
    if missing:
        st.error(f"未回答の質問があります: {', '.join(sorted(missing))}")
        st.stop()

    # スコア計算（Q2・Q3・Q4 = 旧Q1・Q2・Q3 がスコア対象）
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

    if beta_email:
        st.success(f"✅ βテスター登録完了（{beta_email}）\nツール完成後、最初にご連絡します！")

    st.markdown(
        '<div style="background:#FFF9E6;border:2px solid #E8A000;'
        'padding:1.2rem;border-radius:8px;margin:1rem 0">'
        '<h4 style="color:#B8730A;margin:0 0 0.5rem 0">'
        '📋 自社のSaaS削減余地を具体的な数字で知りたい方へ</h4>'
        '<p style="margin:0;color:#555">'
        '診断結果をもとに、<strong>個別の削減提案レポート</strong>（PDF・10ページ程度）を作成します。<br>'
        '削減見込み額の試算・優先順位・交渉ポイントまでお届けします。<br>'
        'サービス立ち上げ期につき、<strong>初期価格15万円〜（通常の2割引）</strong>でご提供中。<br><br>'
        '<a href="mailto:smartnavipro@gmail.com" '
        'style="background:#E8A000;color:white;padding:0.4rem 1rem;'
        'border-radius:4px;text-decoration:none;font-weight:bold">'
        '📩 お問い合わせ（メール）</a>'
        '</p>'
        '</div>',
        unsafe_allow_html=True,
    )

    # Google Sheets保存
    if GAS_SHEETS_URL:
        try:
            requests.post(
                GAS_SHEETS_URL,
                json={
                    "company_size": company_size,
                    "industry": industry,
                    "q1": q1, "q2": q2, "q3": ", ".join(q3),
                    "most_painful_pattern": most_painful_pattern,
                    "other_pattern": other_pattern,
                    "q4": q4, "q5": q5,
                    "current_tool_status": current_tool_status,
                    "current_tool_name": current_tool_name,
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
                    f"Q1 企業規模: {company_size}\n"
                    f"　　業種: {industry}\n"
                    f"Q2 費用把握: {q1}\n"
                    f"Q3 無駄経験: {q2}\n"
                    f"Q4 管理方法: {', '.join(q3)}\n"
                    f"Q5 気になるパターン: {most_painful_pattern}"
                    + (f"（{other_pattern}）" if other_pattern else "") + "\n"
                    f"Q6 ニーズ: {q4}\n"
                    f"Q7 価格感: {q5}\n"
                    f"Q8 管理ツール: {current_tool_status}"
                    + (f"（{current_tool_name}）" if current_tool_name else "") + "\n"
                    f"βテスター: {beta_email or 'なし'}"
                )},
                timeout=5,
            )
        except Exception:
            pass
