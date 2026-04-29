/**
 * SaaS管理ヒアリングフォーム 自動生成スクリプト
 *
 * 【実行方法】
 * 1. smartnavipro@gmail.com でログインした状態で script.google.com を開く
 * 2. 「新しいプロジェクト」→ このコードを全選択して貼り付け
 * 3. 上部の「実行する関数」が createHearingForm になっていることを確認
 * 4. ▶ 実行ボタンをクリック（初回は権限許可が必要）
 * 5. 「ログ」（表示 → ログ）にフォームURLが出力される
 */

function createHearingForm() {

  // ── フォーム作成 ──────────────────────────────
  var form = FormApp.create('SaaS管理ヒアリングシート');

  form.setDescription(
    '個別削減提案レポート作成に必要な情報をご記入ください。\n' +
    'ご入力内容はレポート作成にのみ使用し、第三者に共有しません。\n' +
    '（所要時間：約10〜15分）'
  );

  form.setConfirmationMessage(
    'ご回答ありがとうございます。\n' +
    '通常3営業日以内にレポートの完成目安をご連絡します。\n' +
    'ご不明な点は smartnavipro@gmail.com までお問い合わせください。'
  );

  form.setCollectEmail(false);
  form.setAllowResponseEdits(false);
  form.setLimitOneResponsePerUser(false);


  // ── セクション1：基本情報 ──────────────────────────────
  form.addSectionHeaderItem()
    .setTitle('1. 基本情報')
    .setHelpText('まず、基本情報をご記入ください。いただいた情報はレポートの宛名・文中に使用します。');

  form.addTextItem()
    .setTitle('会社名（正式名称）')
    .setHelpText('例：株式会社〇〇')
    .setRequired(true);

  form.addTextItem()
    .setTitle('ご担当者名')
    .setRequired(true);

  form.addTextItem()
    .setTitle('ご役職')
    .setHelpText('例：情報システム部 マネージャー')
    .setRequired(false);

  form.addTextItem()
    .setTitle('ご返送先メールアドレス')
    .setHelpText('レポートをお送りするメールアドレスをご記入ください')
    .setRequired(true);


  // ── セクション2：SaaS全体の把握 ──────────────────────────────
  form.addPageBreakItem()
    .setTitle('2. SaaS全体の把握')
    .setHelpText('貴社のSaaSコスト全体感を把握するための質問です。概算・推定で構いません。');

  form.addMultipleChoiceItem()
    .setTitle('現在、会社として契約しているSaaSの総数（概算）')
    .setChoiceValues([
      '5個未満',
      '5〜10個',
      '11〜20個',
      '21〜50個',
      '51個以上',
      'わからない'
    ])
    .setRequired(true);

  form.addMultipleChoiceItem()
    .setTitle('年間SaaS関連費用の合計（概算・税抜）')
    .setChoiceValues([
      '500万円未満',
      '500万〜1,000万円',
      '1,000万〜3,000万円',
      '3,000万〜5,000万円',
      '5,000万〜1億円',
      '1億円以上',
      '把握していない'
    ])
    .setRequired(true);

  form.addCheckboxItem()
    .setTitle('SaaSの契約・支払いはどのように管理されていますか？（複数選択可）')
    .setChoiceValues([
      '情報システム部門が一元管理している',
      '経理・財務部門が把握している',
      '部門ごとに各担当者が管理している',
      '法人カードで部門・個人が個別に契約しているものがある',
      '管理が明確でなく、誰が把握しているかわからない'
    ])
    .setRequired(true);

  form.addMultipleChoiceItem()
    .setTitle('IT部門の管轄外（部門・個人の独自契約）でSaaSが導入されているケースはありますか？')
    .setChoiceValues([
      'はい、把握しています',
      'はい、おそらくありますが全容は不明です',
      'ないと思いますが、確認はしていません',
      'ありません'
    ])
    .setRequired(true);


  // ── セクション3：主要SaaS一覧（最重要） ──────────────────────────────
  form.addPageBreakItem()
    .setTitle('3. 主要SaaS一覧（最重要）')
    .setHelpText(
      'このセクションが削減見込み額の試算で最も重要です。\n' +
      '把握している範囲で構いません。わからない欄は「不明」とご記入ください。'
    );

  form.addParagraphTextItem()
    .setTitle('主要SaaSを上位5〜10件、以下の形式でご記入ください')
    .setHelpText(
      '【形式】ツール名 ／ 月額費用（税抜）／ 契約席数 ／ 月間アクティブ数（概算）／ 契約更新月\n\n' +
      '【例】\n' +
      'Salesforce ／ 198,000円 ／ 10席 ／ 8名 ／ 2026年9月\n' +
      'Slack ／ 45,000円 ／ 30席 ／ 22名 ／ 2026年12月\n\n' +
      'わからない欄は「不明」とご記入ください。'
    )
    .setRequired(true);

  form.addParagraphTextItem()
    .setTitle('上記以外で、定期的に支払いが発生しているSaaSや月額サービスがあればご記入ください（任意）')
    .setHelpText(
      '法人カードの明細にあるが台帳に載っていないもの、' +
      'トライアルのつもりが継続しているものなど。'
    )
    .setRequired(false);


  // ── セクション4：パターン別確認 ──────────────────────────────
  form.addPageBreakItem()
    .setTitle('4. パターン別確認')
    .setHelpText('7つの無駄パターンに対して、貴社の状況をお聞きします。');

  form.addMultipleChoiceItem()
    .setTitle('直近1年間での退職・異動者数（概算）')
    .setChoiceValues([
      '0名',
      '1〜5名',
      '6〜20名',
      '21〜50名',
      '51名以上',
      'わからない'
    ])
    .setRequired(true);

  form.addMultipleChoiceItem()
    .setTitle('退職・異動が発生した際のSaaSアカウント削除フローはありますか？')
    .setChoiceValues([
      'はい、人事システムと連携して自動的に対応されています',
      'はい、ただし手動対応のためもれることがあります',
      '明確なフローがなく、担当者任せです',
      '対応できていないと思います'
    ])
    .setRequired(true);

  form.addMultipleChoiceItem()
    .setTitle('過去に、意図せずSaaSが自動更新されてしまったことはありますか？')
    .setChoiceValues([
      'はい、複数回あります',
      'はい、1〜2回あります',
      'ないと思いますが、更新日は管理できていません',
      'しっかり管理できており、意図しない更新はありません'
    ])
    .setRequired(true);

  form.addMultipleChoiceItem()
    .setTitle('「導入したが、ほとんど使われていない」と感じているSaaSはありますか？')
    .setChoiceValues([
      'はい、1つ以上あります',
      'おそらくありますが、把握できていません',
      '定期的に利用状況を確認しており、問題ありません',
      'ありません'
    ])
    .setRequired(true);

  form.addParagraphTextItem()
    .setTitle('使われていないと感じているSaaS名と、その状況を教えてください（任意）')
    .setHelpText(
      '「はい、1つ以上あります」と答えた方のみご記入ください。\n' +
      '例：HubSpot Marketing Hub — 導入後1年、設定が複雑でメール配信だけしか使っていない。月45万円。'
    )
    .setRequired(false);

  form.addMultipleChoiceItem()
    .setTitle('部門ごとに類似した機能のSaaSが重複して契約されている可能性はありますか？')
    .setChoiceValues([
      'はい、把握している重複があります',
      'おそらくありますが、全容は把握していません',
      'ないと思います',
      'わかりません'
    ])
    .setRequired(true);

  form.addMultipleChoiceItem()
    .setTitle('各SaaSの「契約席数」と「実際に使っているユーザー数」のギャップを把握していますか？')
    .setChoiceValues([
      '主要ツールは把握できています',
      '一部のツールは把握していますが、全体は不明です',
      'ほとんど把握できていません'
    ])
    .setRequired(true);


  // ── セクション5：管理体制 ──────────────────────────────
  form.addPageBreakItem()
    .setTitle('5. 管理体制')
    .setHelpText('現在のSaaS管理体制を確認します。');

  form.addMultipleChoiceItem()
    .setTitle('法人カードの明細とIT資産台帳を定期的に突き合わせていますか？')
    .setChoiceValues([
      'はい、定期的に実施しています（年1回以上）',
      '不定期ですが実施しています',
      '実施したことがありません',
      'IT資産台帳そのものがありません'
    ])
    .setRequired(true);

  form.addCheckboxItem()
    .setTitle('SaaS管理の課題として最も大きいと感じるものを教えてください（複数選択可・任意）')
    .setChoiceValues([
      '何に・いくら払っているか全体像が見えない',
      '更新日・解約期限の管理ができていない',
      '部門ごとの個別契約を把握できていない',
      'ツールの利用状況（誰が使っているか）が見えない',
      '社内の合意形成・稟議が難しい',
      'ベンダーとの交渉経験・知識がない',
      '担当者がいない（兼務・片手間）',
      'その他'
    ])
    .setRequired(false);


  // ── セクション6：ご要望・備考 ──────────────────────────────
  form.addPageBreakItem()
    .setTitle('6. ご要望・備考');

  form.addParagraphTextItem()
    .setTitle('本レポートで特に重点的に分析・確認してほしい内容があれば教えてください（任意）')
    .setHelpText(
      '例：「Salesforceのプラン見直しを最優先で確認してほしい」' +
      '「退職者ライセンスの棚卸し方法を詳しく知りたい」など'
    )
    .setRequired(false);

  form.addParagraphTextItem()
    .setTitle('社内で改善を進めるうえで想定される障壁があれば教えてください（任意）')
    .setHelpText(
      '例：「稟議プロセスが長い」「ベンダーとの関係を壊したくない」「担当者の工数がない」など'
    )
    .setRequired(false);


  // ── URL出力 ──────────────────────────────
  var publishedUrl = form.getPublishedUrl();
  var editUrl      = form.getEditUrl();

  Logger.log('');
  Logger.log('╔══════════════════════════════════════════════╗');
  Logger.log('  フォーム作成完了');
  Logger.log('╠══════════════════════════════════════════════╣');
  Logger.log('  回答URL（クライアントに送るURL）:');
  Logger.log('  ' + publishedUrl);
  Logger.log('');
  Logger.log('  編集URL（自分の管理用）:');
  Logger.log('  ' + editUrl);
  Logger.log('╚══════════════════════════════════════════════╝');
  Logger.log('');
  Logger.log('【次の手順】');
  Logger.log('1. 上の「回答URL」をコピーして hearing_sheet_form.md に記録する');
  Logger.log('2. フォームを開く → 設定 → 回答 → メール通知を有効化');
  Logger.log('   通知先: smartnavipro@gmail.com');
  Logger.log('3. 「回答」タブ → スプレッドシートにリンク → 新しいスプレッドシートを作成');
  Logger.log('   （回答が自動でスプレッドシートに蓄積される）');
}
