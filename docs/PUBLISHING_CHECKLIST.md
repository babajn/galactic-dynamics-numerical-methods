# 公開状況と確認事項

## 配布版 v1.3（2026年11月11日）

- [x] 第1〜3章・付録A〜FのLaTeXソースを公開
- [x] XeLaTeXの3回実行によるA4・115ページのPDFを公開（`docs/galactic_dynamics_numerical_methods_v1.3.pdf`）
- [x] GitHub ActionsによるPDFの組版・ページ数検証が成功
- [x] 本文で使用する図45点と、数値マクロ・生成数値を公開
- [x] `notebooks/student/` にコード入力版Notebook 6冊を配置
- [x] `notebooks/complete/` に完全実装版Notebook 6冊を配置（添付原本とのSHA-1一致を確認）
- [x] 学生用Notebookの54か所のPDFリンクをv1.3へ変更（コードセルは変更なし）
- [x] 完全実装版6冊をPython 3.13.5とnbclient 0.10.4で全セル再実行し、すべて成功
- [x] 図生成スクリプトの入力先を `notebooks/complete/` に変更
- [x] 配布版v1.2のPDFを旧版として保持

## 追加の確認事項

- [ ] `python scripts/generate_all_figures.py` を実行し、図45点・生成数値の再生成結果を照合する
- [ ] GitHub Actionsで生成されたPDFとローカル組版PDFの表示差を比較する（ページ数115は確認済み）
- [ ] 第三者由来の図・コード・データの権利を最終確認する
- [ ] 正式な教材・ソフトウェアの再利用ライセンスを決定して配置する
- [ ] 公開資料に学内限定情報や公開不要な記載が残っていないか最終レビューする

## 配布版 v1.2（2026年10月16日）の履歴

- [x] 教科書PDF（104ページ）
- [x] 本編3章・付録A〜D、前付・参考文献のLaTeXソース
- [x] 本文で使用する図45点（PDF）
- [x] 学生用コード入力版Notebook 6冊、入力欄対応表、図生成関連スクリプト
- [x] 元のZIPとのGit blob SHA-1一致を確認
- [x] 当時は完全実装版Notebookを公開せず、v1.3から公開
