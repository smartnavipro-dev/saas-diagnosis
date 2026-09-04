import os
import streamlit as st
import requests
from dotenv import load_dotenv

load_dotenv()



def _secret(name: str, default: str = "") -> str:
    """Streamlit Cloud の Secrets → 環境変数(.env) の順に鍵を読む。

    2026-09-04 修正: 以前は os.getenv だけだった。Streamlit Cloud に置いた
    Secrets（DISCORD_WEBHOOK_URL / GAS_SHEETS_URL）は st.secrets 側に入るため、
    本番アプリからは鍵が空のままで、診断回答の Discord 通知が一度も飛んでいなかった
    （8/30 に本番から送ったテスト回答が Discord に出なかったことで判明）。
    ローカルには secrets.toml が無く st.secrets が例外を出すので握りつぶす。
    """
    try:
        value = st.secrets.get(name)
        if value:
            return str(value)
    except Exception:
        pass
    return os.getenv(name, default)


DISCORD_WEBHOOK = _secret("DISCORD_WEBHOOK_URL")
GAS_SHEETS_URL  = _secret("GAS_SHEETS_URL")

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

    # 削減見込み額の試算
    SIZE_ANNUAL_BUDGET = {
        "〜50名（スタートアップ・小規模）":   5_000_000,
        "51〜300名（中小企業）":            20_000_000,
        "301〜1,000名（中堅企業）":         80_000_000,
        "1,001〜5,000名（大企業）":        300_000_000,
        "5,001名〜（エンタープライズ）":    800_000_000,
    }
    WASTE_RATE_MID = {1: 0.25, 2: 0.15, 3: 0.10, 4: 0.075}
    annual_budget = SIZE_ANNUAL_BUDGET.get(company_size, 20_000_000)
    estimated_savings = int(annual_budget * WASTE_RATE_MID[level_num] * 0.6)
    savings_man = estimated_savings // 10_000

    # Q5別コメント（検証済みデータのみ使用）
    Q5_COMMENTS = {
        "退職者のライセンスが残ったまま課金されている":
            "Salesforce Enterprise（月19,800円/ユーザー）で退職者が10名いれば、年間約238万円が無駄になります。退職フローにSaaSアカウント削除の手順がない企業では、気づかず半年・1年と課金が続くケースが多いです。",
        "部門ごとに似た機能のツールが重複契約されている":
            "海外調査では42〜48%の企業でIT部門が把握していない「シャドーIT」が確認されています。チャットツール・プロジェクト管理ツールが部門ごとに乱立しているケースは珍しくありません。",
        "機能の半分も使っていないのに上位プランを契約している":
            "Salesforceはプロフェッショナルからエンタープライズへのアップグレードでユーザーあたり月10,200円増加しますが、追加機能の多くが使われていないことがあります。なおSalesforceは契約後のダウングレードができないため、プラン選定の段階で慎重な判断が必要です。",
        "契約更新日を把握できておらず、気づいたら自動更新されている":
            "Money Forward Admina調査によると、10個以上のSaaSを使っている企業の64.07%が「意図せずSaaSを自動更新した経験がある」と回答しています。更新通知メールを見逃すだけで、年単位の無駄が生まれます。",
        "導入したが使いこなせていないツールに費用を払い続けている":
            "テックタッチ2024年調査では、大企業の60.7%が「使いこなせていないSaaSがある」と回答。HubSpotは2024年3月以降シート単位の課金体系に変わっており、使っていないユーザー分のコストが見えやすくなっています。",
        "一部の人しか使っていないツールに全員分払っている":
            "Zylo 2026年版調査では、企業が保有するSaaSライセンスの平均利用率は54%（46%が未使用）。100席契約して46席が使われていないなら、その分は丸ごと削減対象です。",
        "トライアルや個別契約のツールが管理外で動いている":
            "海外調査では42〜48%の企業でIT部門が把握していないシャドーITが存在しています。法人カードの明細を確認すると、トライアルのつもりが継続課金になっているサービスが見つかることがあります。",
        "そもそも何が無駄かわからない（可視化できていない）":
            "支出が見えていない状態は問題を認識できず、最も多くの無駄が放置されやすい状態です。まず全部門にSaaS利用状況のアンケートを実施し、何があるかを洗い出すことが最初の一手です。",
        "その他":
            "SaaSコストの無駄は会社ごとに異なります。まずは全SaaS契約の費用・利用率・更新日を1つのシートに集約することから始めましょう。",
    }
    q5_comment = Q5_COMMENTS.get(most_painful_pattern, "")

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

    # 削減見込み額の表示
    st.markdown(
        f'<div style="background:#F0FFF4;border:2px solid #00C851;'
        f'padding:1rem;border-radius:8px;margin:0.8rem 0;text-align:center">'
        f'<p style="margin:0 0 0.2rem 0;color:#00713A;font-weight:bold">💰 削減見込み額（試算）</p>'
        f'<p style="font-size:1.8rem;font-weight:bold;color:#00713A;margin:0">約{savings_man:,}万円 / 年</p>'
        f'<p style="font-size:0.82rem;color:#666;margin:0.3rem 0 0 0">'
        f'貴社規模のSaaS年間支出 × 無駄率{int(WASTE_RATE_MID[level_num]*100)}%（診断結果）× 回収率60%で試算</p>'
        f'</div>',
        unsafe_allow_html=True,
    )

    # Q5別コメント
    if q5_comment:
        st.markdown(
            f'<div style="background:#FFFBEA;border-left:4px solid #DAA520;'
            f'padding:0.8rem 1rem;border-radius:4px;margin:0.8rem 0">'
            f'<p style="margin:0;font-size:0.9rem;color:#555">'
            f'💡 <strong>「{most_painful_pattern}」について</strong>：{q5_comment}'
            f'</p></div>',
            unsafe_allow_html=True,
        )

    st.markdown("### 📋 現状の分析")
    for d in lv["details"]:
        st.markdown(f"- {d}")

    st.markdown("### ✅ 今すぐできる改善アクション")
    for i, a in enumerate(lv["actions"], 1):
        st.markdown(f"**{i}.** {a}")

    # Xシェアボタン
    import urllib.parse
    _app_url = "https://saas-diagnosis-4u2z3uxxgtmjrsvqzdqjzn.streamlit.app"
    _tweet = (
        f"SaaS管理レベルを診断してみた。\n"
        f"結果：「{lv['name']}」（スコア{score}/7点）\n"
        f"削減見込み：年間約{savings_man:,}万円\n\n"
        f"自社のSaaS無駄が気になる方はこちら👇\n"
        f"#SaaS管理 #情シス #コスト削減"
    )
    _tweet_url = f"https://twitter.com/intent/tweet?text={urllib.parse.quote(_tweet)}&url={urllib.parse.quote(_app_url)}"
    st.markdown(
        f'<div style="text-align:center;margin:0.8rem 0">'
        f'<p style="color:#555;font-size:0.9rem;margin:0 0 0.5rem 0">役に立ったら、ぜひシェアをお願いします🙏</p>'
        f'<a href="{_tweet_url}" target="_blank" '
        f'style="background:#000;color:white;padding:0.5rem 1.4rem;'
        f'border-radius:6px;text-decoration:none;font-weight:bold;font-size:0.95rem">'
        f'𝕏 診断結果をポストする</a></div>',
        unsafe_allow_html=True,
    )

    # 個別レポートの問い合わせ窓口
    _mail_addr = "smartnavipro@gmail.com"
    _mail_subject = urllib.parse.quote("【個別レポート相談】SaaS管理診断より")
    _mail_body = urllib.parse.quote(
        "SaaS管理レベル診断の結果を見てご連絡しました。\n\n"
        f"・診断結果: レベル{level_num}（{lv['name']}）/ スコア{score}点\n"
        f"・削減見込み（試算）: 約{savings_man:,}万円/年\n"
        f"・従業員規模: {company_size}\n\n"
        "会社名:\n"
        "お名前:\n"
        "ご相談内容（任意）:\n"
    )
    st.divider()
    st.markdown(
        f'<div style="background:#F7F9FC;border:1px solid #D5DCE6;'
        f'padding:1rem 1.2rem;border-radius:8px;margin:0.5rem 0">'
        f'<p style="margin:0 0 0.4rem 0;font-weight:bold;color:#1a3d6e">📄 貴社の実データで詳しく知りたい方へ</p>'
        f'<p style="margin:0 0 0.7rem 0;font-size:0.9rem;color:#444">'
        f'この診断は一般的な傾向にもとづく試算です。貴社の実際の契約内容をもとに、'
        f'「どの契約を・どの順番で・いくら削れるか」をまとめた'
        f'<strong>個別削減提案レポート（PDF・約10ページ／150,000円〜・規模による）</strong>を作成しています。'
        f'ご興味のある方は、下のボタンからお気軽にご連絡ください（見積まで無料）。</p>'
        f'<p style="text-align:center;margin:0">'
        f'<a href="mailto:{_mail_addr}?subject={_mail_subject}&body={_mail_body}" '
        f'style="background:#1a3d6e;color:white;padding:0.5rem 1.4rem;'
        f'border-radius:6px;text-decoration:none;font-weight:bold;font-size:0.95rem">'
        f'📩 メールで相談する（無料）</a></p>'
        f'<p style="text-align:center;font-size:0.78rem;color:#888;margin:0.5rem 0 0 0">'
        f'宛先: {_mail_addr}（診断結果が自動で本文に入ります）</p>'
        f'</div>',
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
                    + (f"（{current_tool_name}）" if current_tool_name else "")
                )},
                timeout=5,
            )
        except Exception:
            pass
