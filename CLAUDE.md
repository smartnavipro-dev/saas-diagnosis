# SaaS管理診断ツール — プロジェクトコンテキスト

## プロジェクト概要
SaaS管理レベル診断ツール（Streamlit製）をリードジェネレーション装置として活用し、
「個別削減提案レポート」のコンサル販売につなげるソロビジネス。

ツール自体は補助手段。主軸は「個別レポート販売（コンサル）」。
外販・SaaS化は将来検討しない（自分の作業効率化のためのみ）。

## ビジネスモデルと価格
- **中小企業向けレポート**: 15万円〜（サービス立ち上げ期につき通常の2割引）
- **中堅企業向けレポート**: 45万円〜
- CTAは記事の最後に1段落だけ自然に紹介。前面には出さない構造。
- 本気で困っている層だけが個別レポートに進む導線設計。

## 収益ロードマップ — ⚠️ 2026-09-02 取り下げ
旧: 月50万→100万→300万の12ヶ月目標。**根拠となる実測（問い合わせ数・成約数）が1件も無いため取り下げ。**
代わりの判断日: **2026-12-01**（それまでに 問い合わせ件数・note PV・Streamlit閲覧数 を実測してから、コンサル継続か縮小かを決める）。
詳細: `ObsidianVault/Projects/CW_Hunter/2026-09-02_収入戦略の再考.md`
<!-- 旧記載（参考）: 1〜3ヶ月 月50万 / 3〜6ヶ月 月100万 / 6〜12ヶ月 月300万 -->

---

## ファイル構成

```
C:\Users\chanc\saas_diagnosis\          ← このディレクトリ（git管理）
  saas_diagnosis.py                     ← メインアプリ（デプロイ済み・最新版）
  saas_diagnosis_additional_questions.py← 追加3問コード（未統合）
  note_article_final.md                 ← 投稿用note記事（最終版）
  requirements.txt
  .gitignore
  CLAUDE.md                             ← このファイル

C:\Users\chanc\saas_diagnosis.py        ← 旧版（GAS未対応）。削除候補。
C:\Users\chanc\Downloads\saas_diagnosis_additional_questions.py  ← 上記のコピー×2
```

**デプロイ先**: https://saas-diagnosis-4u2z3uxxgtmjrsvqzdqjzn.streamlit.app

---

## 現状の診断アプリ仕様（saas_diagnosis.py）

### 構成
- 5問 + メールアドレス（任意）で3〜4分
- スコア計算→4レベルの診断結果→アクション提示→βテスター登録

### 5問の内容
| | 質問 | スコア |
|---|---|---|
| Q1 | SaaS月額費用の把握度 | 0〜2点 |
| Q2 | 使われていないツール経験 | 0〜2点 |
| Q3 | 管理方法（複数選択） | 0〜3点（最大値を採用） |
| Q4 | ニーズ確認（スコアに未使用） | - |
| Q5 | 価格感（スコアに未使用） | - |

### 4段階診断レベル
| スコア | レベル | 無駄率目安 |
|---|---|---|
| 0〜1点 | コスト見えない状態 🔴 | 20〜30% |
| 2〜3点 | なんとなく管理 🟠 | 10〜20% |
| 4〜5点 | 管理しているが非効率 🟡 | 5〜15% |
| 6点〜 | 最適化できている 🟢 | 5〜10% |

### データ保存
- **Discord webhook**: 全回答をDiscordに通知（`DISCORD_WEBHOOK_URL`）
- **Google Sheets**: GASエンドポイント経由（`GAS_SHEETS_URL`）
- `.env`で管理。Streamlit CloudではSecrets設定が必要。

---

## ✅ 本番のDiscord通知が飛んでいなかった問題（2026-09-04 修正・要確認）
- 症状: 8/30に本番アプリからテスト回答を送ったのに、Discord（Captain Hook）に「📊 新しい診断回答」が出なかった。curlで送った2件（test / webhook test 2）は届いていた＝**Webhookは生きているがアプリから飛んでいない**
- 原因: `saas_diagnosis.py` が鍵を `os.getenv()` だけで読んでいた。Streamlit Cloud の Secrets は `st.secrets` 側に入るため、本番では DISCORD_WEBHOOK_URL / GAS_SHEETS_URL が空文字のまま → `if DISCORD_WEBHOOK:` が偽で通知処理を丸ごとスキップしていた（Googleスプレッドシート保存も同じ理由で動いていなかったはず）
- 修正: `_secret()` を追加し **st.secrets → 環境変数(.env)** の順に読む。commit b73f8a1・push済み（Streamlit Cloudが自動反映）
- 9/4のテストは**届かなかった**（9/5ユーザー確認）。追加調査で**真の原因**判明: Streamlit Cloud の Secrets に貼った DISCORD_WEBHOOK_URL の途中（95〜96文字目）に**空白が2つ混入**していた（.envより2文字長い）。URLに空白があると requests.post が失敗し、`except: pass` で握りつぶされて無音だった。GAS_SHEETS_URL は空白なし
- 修正2（commit a97537c）: `_secret()` で読んだ値から空白類を全て除去。Streamlit Cloud をリブートして反映。9/5 20時台に本番から再テスト送信（Q5その他＝「2026-09-05 再テスト（空白除去修正後）」）→ 結果画面まで正常。**Discord到着はユーザー確認待ち**。届かなければ次は Streamlit の Manage app ログを見る
- 教訓: 通知の失敗を `except Exception: pass` で黙らせない。少なくとも st.session_state か標準出力に理由を残す（次の改修で入れる）

## 🚨 本番デプロイが古い問題（2026-08-27発見・未解決）
本番URL（saas-diagnosis-4u2z3uxxgtmjrsvqzdqjzn.streamlit.app）は**「5問・約3分」の4月以前の旧版**を配信している。
- GitHub origin/master は正しい（8問版＋問い合わせCTA・421行・コミットe5b3c9d）
- つまり**Streamlit Cloud側がこのリポジトリのmasterを追従していない**（古いビルドのまま眠り→起床でも更新されず）
- アプリは「Zzzz（居眠り）」状態だった＝**note記事からの訪問がほぼ無い**ことも判明
- 対処（ユーザー本人の操作が必要）: share.streamlit.io にサインイン → 該当アプリの Manage app →
  ①まず「Reboot」で直るか確認 ②直らなければソース設定（リポジトリ/ブランチ/メインファイル）を確認。
  smartnavipro-dev/saas-diagnosis の master / saas_diagnosis.py を指しているべき
- ⚠️アプリを作り直すとURLが変わり、**note記事内のリンクが切れる**。カスタムサブドメインに同じ文字列を指定すれば維持できる

## 追加3問 — ✅統合済み（2026-04-29のpure-give改修で本体に組込済。8問構成で公開中）

### 追加内容と配置位置
| 追加問 | 内容 | 配置 |
|---|---|---|
| 追加Q1 | 企業規模（従業員数）+ 業種（任意） | 既存Q1の前 |
| 追加Q2 | 最も気になる無駄パターン（7択） | 既存Q3とQ4の間 |
| 追加Q3 | SaaS管理ツールの利用状況 | 既存Q5とメアドの間 |

### 追加Q2の選択肢（7パターン）
note記事の7パターンとの対応：
1. 退職者のライセンスが残ったまま課金されている ← 記事パターン1
2. 部門ごとに似た機能のツールが重複契約されている ← 記事パターン2
3. 機能の半分も使っていないのに上位プランを契約している ← 記事パターン3
4. 契約更新日を把握できておらず、気づいたら自動更新されている ← 記事パターン4
5. 一部の人しか使っていないツールに全員分払っている ← 記事パターン6
6. トライアルや個別契約のツールが管理外で動いている ← 記事パターン7
7. そもそも何が無駄かわからない（可視化できていない） ← キャッチオール
⚠️ **記事パターン5（「導入しただけ」放置）が選択肢に欠落。統合時に追加要。**

---

## 統合時に修正が必要な技術的問題

### 問題1: フォームコンテキストの衝突（最重要）
既存アプリは`with st.form("diagnosis"):`を使っている。
追加コードは`st.radio()`をフォーム外で使い、`st.button()`を持つ。

**修正方法:**
- 追加のウィジェットをすべて`with st.form("diagnosis"):`ブロック内に移動
- `st.button("診断結果を見る")`と`save_response_to_csv()`は削除
- 送信は既存の`st.form_submit_button("▶ 診断する")`で統一

### 問題2: GASペイロードに新フィールドを追加
既存のGAS送信コードに`company_size`, `industry`, `most_painful_pattern`, `current_tool_status`を追加:
```python
requests.post(GAS_SHEETS_URL, json={
    "q1": q1, "q2": q2, "q3": ", ".join(q3),
    "q4": q4, "q5": q5,
    "company_size": company_size,       # 追加
    "industry": industry,               # 追加
    "most_painful_pattern": most_painful_pattern,  # 追加
    "current_tool_status": current_tool_status,    # 追加
    "beta_email": beta_email, "level": level_num, "score": score,
})
```

### 問題3: Discordペイロードにも新フィールドを追加
```python
f"企業規模: {company_size}\n"
f"業種: {industry}\n"
f"最も気になるパターン: {most_painful_pattern}\n"
f"既存管理ツール: {current_tool_status}\n"
```

### 問題4: 個別レポートCTAが診断完了画面に未実装
引き継ぎメモで「診断完了画面にも問い合わせリンク追加」と計画済み。
βテスター登録の下に追加する（Google FormかメールURLで）。

---

## 次のアクション（優先順位順）

### 1. 診断ツールの改修 — ✅完了（追加3問は統合済み・8問構成で公開中）

### 2. データ保存先の確認
- 現状: GASエンドポイント（`GAS_SHEETS_URL`）がすでに動いている
- 引き継ぎメモでは「Supabaseが必須」と書いたが、GASが機能しているならそのままでOK
- Supabase化は必要に応じて（回答数が増えてGASが遅くなった時）

### 3. 個別レポート問い合わせ窓口 — ✅実装済み（2026-08-26）
- 診断結果画面の最下部にCTAボックスを追加（Xシェアボタンの下）
- mailto: smartnavipro@gmail.com。件名・本文に診断結果（レベル/スコア/削減見込み/規模）が自動で入る
- 文言: 個別削減提案レポート（PDF・約10ページ／150,000円〜・規模による）・見積まで無料
- AppTestで8項目の表示検証済み。デプロイはgit push後にStreamlit Cloudが自動反映

### 4. note記事の投稿 — ✅ 完了（2026-08-13 18:25 投稿済み）
→ https://note.com/royal_zephyr5395/n/n5e21f3299bca 。`note_article_final.md` は投稿済みの原稿。**再投稿しないこと**（同名記事が既に2本ある: 4か月前 n6753fe3700c0 と 8/13 n5e21f3299bca）。
✅ 記事末尾の「2割引」表記は 2026-09-05 に「15万円〜でご提供しています。」へ修正して公開済み（値引き政策の取り下げに合わせた）。
✅ 同名の古い記事（4/29版 n6753fe3700c0）は 2026-09-04 に**下書きに戻した**（非公開・削除はしていない）。

### 5. レポートテンプレートの準備（10ページ）
- 表紙 / 現状分析 / 7パターン該当チェック / 削減見込み額試算
- 削減ロードマップ / 優先順位 / まとめ

---

## 検証済みの数字（note記事・レポートに使用）

| データ | 出典 |
|---|---|
| SaaSライセンス利用率54%（46%が未使用） | Zylo 2026年版調査 |
| 大企業の60.7%が「使いこなせていないSaaSがある」 | テックタッチ2024年調査 |
| 10個以上のSaaS使用企業の64.07%が意図せず契約更新の経験 | Money Forward Admina調査 |
| Salesforce Sales Cloud Enterprise 月21,000円/ユーザー | Salesforce公式 2026年8月13日実測（旧19,800円から改定） |
| Salesforce 現行プラン: Starter Suite 3,000 / Pro Suite 12,000 / Enterprise 21,000 / Unlimited 42,000 / Agentforce 1 Sales 66,000（月/ユーザー） | Salesforce公式 2026年8月13日実測。旧Professional 9,600はPro Suite 12,000に改定 |
| Salesforceは契約後ダウングレード不可 | Salesforce公式 |
| HubSpotは2024年3月以降シート単位の課金体系 | HubSpot公式 2026年4月時点 |

⚠️ 価格・プラン情報は頻繁に改定されるため、使用前に必ず公式サイトで確認すること。

---

## note記事について

### 投稿済み記事
- 第1弾: 「SaaSレビュー500件を分析した話」（投稿済み・反響あり）

### 第2弾: 投稿済み（2026-08-13 18:25）
- タイトル:「SaaS予算の40%は"気づかれずに"無駄になっている。500件のレビュー分析と日本企業に効く7つのチェックポイント」
- URL: https://note.com/royal_zephyr5395/n/n5e21f3299bca
- ファイル: `note_article_final.md`（投稿直前にSalesforce価格を2026年8月実測値に更新して投稿）
- CTA: 診断ツールへの誘導 + 個別レポートの簡潔な紹介（15万円〜）
- ハッシュタグ: #SaaS #コスト削減 #業務効率化 #情報システム #DX ・無料記事・タイトルは40%のまま（46%はライセンス比率でありタイトル主語「予算」と不整合のため）
- 未設定: 見出し画像（あとから設定可）

### ⚠️ 記事の軽微な不整合（投稿前に確認）
- タイトル「40%は無駄」← 本文中の「40%前後」← Zylo実データ「46%が未使用」
- 46%の方が強く・根拠もある。タイトルを「46%」に変更するか要検討。

### 続編記事のアイデア
- 1〜2週間後: アンケート中間報告
- 1ヶ月後: 実際のSaaS棚卸しでわかった意外な無駄（匿名実例）
- 3ヶ月後: ソロでSaaS診断サービス立ち上げて見えたこと

---

## よく使うコマンド

### ローカル起動
```
cd C:\Users\chanc\saas_diagnosis
streamlit run saas_diagnosis.py
```

### デプロイ
Streamlit Cloudと連携済み。mainブランチにpushすると自動デプロイ。


---

## 居眠り防止ピン（2026-08-29 導入）
Streamlit Community Cloudはアクセスが途絶えるとアプリを休眠させ、訪問者に「起こすボタン」を見せてしまう（離脱要因）。
対策として、Playwrightでページを開き寝ていたら起こすピンを1日3回自動実行している。

- スクリプト: `keep_awake.py`（休眠画面なら「get this app back up」をクリック→タイトルが「SaaS管理レベル診断」になるまで待つ）
- 実行: `run_keep_awake.bat` → ログは `keep_awake.log`（status=awake / woke+ok / ERROR）
- タスクスケジューラ: `SaaS_Diagnosis_KeepAwake_0945` / `_1545` / `_2115`（毎日9:45・15:45・21:15、PC起動時のみ）
- 削除するとき: `schtasks /Delete /TN "SaaS_Diagnosis_KeepAwake_0945" /F`（3つとも同様）
- 限界: PCが点いていない夜間は打てないため、翌朝9:45の便で起こす設計。朝9:45以前の訪問者には休眠画面が出ることがある
