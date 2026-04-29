"""
SaaS管理レベル診断ツール - 追加3問のサンプルコード
既存の5問構成に追加することで、ツール開発に必要な実態データを取得可能にする。

配置位置:
- 追加Q1: 最初（既存Q1の前）に配置
- 追加Q2: 既存Q3とQ4の間に配置
- 追加Q3: 既存Q5の後、メールアドレス入力の前に配置
"""

import streamlit as st


# =============================================================================
# 追加Q1: 企業規模（最初に配置）
# =============================================================================
st.markdown("### Q. 貴社の規模を教えてください")
company_size = st.radio(
    "従業員数",
    options=[
        "〜50名（スタートアップ・小規模）",
        "51〜300名（中小企業）",
        "301〜1,000名（中堅企業）",
        "1,001〜5,000名（大企業）",
        "5,001名〜（エンタープライズ）",
    ],
    key="company_size",
    label_visibility="collapsed",
)

# 任意項目: 業種
industry = st.selectbox(
    "業種（任意）",
    options=[
        "選択しない",
        "IT・ソフトウェア",
        "製造業",
        "金融・保険",
        "小売・EC",
        "サービス業",
        "メディア・広告",
        "医療・ヘルスケア",
        "建設・不動産",
        "教育",
        "その他",
    ],
    key="industry",
)


# =============================================================================
# 追加Q2: 最も気になる無駄パターン（既存Q3の後に配置）
# =============================================================================
st.markdown("### Q. 以下のうち、最も「もったいない」と感じる状況はどれですか？")
st.caption("最も気になるもの1つを選んでください")

most_painful_pattern = st.radio(
    "気になる無駄",
    options=[
        "退職者のライセンスが残ったまま課金されている",
        "部門ごとに似た機能のツールが重複契約されている",
        "機能の半分も使っていないのに上位プランを契約している",
        "契約更新日を把握できておらず、気づいたら自動更新されている",
        "一部の人しか使っていないツールに全員分払っている",
        "トライアルや個別契約のツールが管理外で動いている",
        "そもそも何が無駄かわからない（可視化できていない）",
        "その他",
    ],
    key="most_painful_pattern",
    label_visibility="collapsed",
)

# 「その他」を選んだ場合の自由記述
if most_painful_pattern == "その他":
    other_pattern = st.text_input(
        "具体的にどのような状況ですか？（任意）",
        key="other_pattern",
    )


# =============================================================================
# 追加Q3: 既存SaaS管理ツールの利用状況（既存Q5の後、メアド入力の前）
# =============================================================================
st.markdown("### Q. 現在、SaaS管理ツールを使っていますか？")

current_tool_status = st.radio(
    "管理ツールの利用状況",
    options=[
        "現在使っている",
        "過去に検討したが導入していない",
        "検討したことはない",
        "そもそもそういうツールがあることを知らなかった",
    ],
    key="current_tool_status",
    label_visibility="collapsed",
)

# 「使っている」を選んだ場合のみ、ツール名を任意記述
if current_tool_status == "現在使っている":
    current_tool_name = st.text_input(
        "差し支えなければツール名を教えてください（任意）",
        placeholder="例: Admina, Josys, HENNGE One など",
        key="current_tool_name",
    )


# =============================================================================
# 回答データの保存（CSVまたはGoogleスプレッドシート連携を想定）
# =============================================================================
def save_response_to_csv(response_data: dict, filepath: str = "responses.csv"):
    """
    回答データをCSVに追記保存する関数。
    Streamlit Cloudの場合、永続化にはst.secretsでGoogleスプレッドシートAPIを
    使う、またはSupabase等のDBに保存する方法を推奨。
    """
    import csv
    from datetime import datetime
    from pathlib import Path

    response_data["timestamp"] = datetime.now().isoformat()

    file_exists = Path(filepath).exists()
    with open(filepath, "a", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=response_data.keys())
        if not file_exists:
            writer.writeheader()
        writer.writerow(response_data)


# 送信ボタン押下時の処理例
if st.button("診断結果を見る"):
    response = {
        "company_size": company_size,
        "industry": industry,
        "most_painful_pattern": most_painful_pattern,
        "current_tool_status": current_tool_status,
        # 既存のQ1〜Q5の回答もここに含める
    }
    save_response_to_csv(response)
    st.success("ご回答ありがとうございました！")
