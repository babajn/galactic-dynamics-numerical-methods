# 銀河力学で学ぶ数値計算法

**Numerical Methods for Galactic Dynamics**

銀河力学の具体的な問題を通して、数値積分、有限差分法、常微分方程式の時間積分法を学ぶための教材です。解析解との比較、保存量の診断、格子幅や時間刻みを変えた収束試験を重視します。

- **著者：** 馬場淳一（鹿児島大学・国立天文台）
- **公開PDF・LaTeXソース：** 配布版 v1.3（A4・115ページ）
- **Jupyter Notebook：** 学生用（コード入力版）6冊と完全実装版6冊
- **対象：** 宇宙流体・重力多体系シミュレーションを学び始める学部生・大学院生
- **関連する輪講テキスト：** Barbara Ryden, *Celestial and Stellar Dynamics* (2025)

## 教科書PDF

**[銀河力学で学ぶ数値計算法 — 配布版 v1.3（PDF）](docs/galactic_dynamics_numerical_methods_v1.3.pdf)**

PDFは全115ページ。本編3章と付録A〜Fから構成されます。

## 目次・Jupyter Notebook

Notebookには**学生用のコード入力版**と、コード・実行結果を含む**完全実装版**を収録しています。対応するコードの掲載ページは [INPUT_MAP.md](docs/INPUT_MAP.md) を参照してください。

| 教材 | 主な内容 | 学生用Notebook | 完全実装版Notebook |
| --- | --- | --- | --- |
| 第1章 球対称質量モデルと数値積分 | Plummer・Hernquist・NFWモデル、数値積分、誤差、収束次数 | [Notebook 1](notebooks/student/ryden_ch6_notebook1_spherical_mass_models.ipynb) | [完全版](notebooks/complete/ryden_ch6_notebook1_spherical_mass_models.ipynb) |
| 第2章 Poisson方程式と有限差分法 | 球対称Poisson方程式、境界条件、有限差分、数値微分 | [Notebook 2](notebooks/student/ryden_ch6_notebook2_poisson_equation_and_gravity.ipynb) | [完全版](notebooks/complete/ryden_ch6_notebook2_poisson_equation_and_gravity.ipynb) |
| 第3章 球対称ポテンシャルと時間積分法 | Euler法、RK4、リープフロッグ法、保存量 | [Notebook 3](notebooks/student/ryden_ch7_notebook3_spherical_orbits.ipynb) | [完全版](notebooks/complete/ryden_ch7_notebook3_spherical_orbits.ipynb) |
| 付録A 軸対称円盤の質量積分と回転曲線 | 指数円盤、Mestel円盤、累積積分 | [Notebook A](notebooks/student/ryden_notebookA_exponential_disks.ipynb) | [完全版](notebooks/complete/ryden_notebookA_exponential_disks.ipynb) |
| 付録B 軸対称Poisson方程式の数値解法 | 2次元有限差分、疎行列、格子収束 | [Notebook B](notebooks/student/ryden_notebookB_axisymmetric_poisson.ipynb) | [完全版](notebooks/complete/ryden_notebookB_axisymmetric_poisson.ipynb) |
| 付録C 軸対称・非軸対称ポテンシャル中の軌道 | エピサイクル運動、軌道積分 | [Notebook C](notebooks/student/ryden_notebookC_axisymmetric_nonaxisymmetric_orbits.ipynb) | [完全版](notebooks/complete/ryden_notebookC_axisymmetric_nonaxisymmetric_orbits.ipynb) |
| 付録D 連立一次方程式の解法 | Gauss消去法、LU分解、Jacobi法 | — | — |
| 付録E 数学公式集 | 数学公式の参照 | — | — |
| 付録F 単位換算と物理定数 | SI・cgs単位系、物理・天文定数 | — | — |

**注意：** `notebooks/student/` はコード入力欄を残した演習版です。未入力セルの `raise NotImplementedError(...)` による停止は仕様です。解答例・保存済み出力を確認したい場合は `notebooks/complete/` を利用してください。

## Notebookの実行環境

Python 3とJupyterLabを使用します。

```sh
git clone https://github.com/babajn/galactic-dynamics-numerical-methods.git
cd galactic-dynamics-numerical-methods
python -m pip install -r requirements-student.txt
jupyter lab
```

必要なパッケージは主にNumPy、SciPy、Matplotlibです。学生用の環境では [requirements-student.txt](requirements-student.txt) を使用してください。完全実装版の実行環境は [requirements.txt](requirements.txt) を参照してください。

## LaTeXソース

教科書を編集・組版するためのソースファイルも公開しています。

- [main.tex](textbook/main.tex)、[preamble.tex](textbook/preamble.tex)：書籍の構成と設定
- [chapters/](textbook/chapters/)：第1〜3章
- [appendices/](textbook/appendices/)：付録A〜F
- [frontmatter/](textbook/frontmatter/)、[backmatter/](textbook/backmatter/)：前付と参考文献
- [figures/](textbook/figures/)：本文に用いる図45点（PDF）
- [generated/](textbook/generated/)：数値結果とLaTeXマクロ
- [scripts/](scripts/)：図生成の関連スクリプト（リポジトリのルートに配置）

XeLaTeXで組版します。ソースのディレクトリ構成を維持した状態で、`textbook/` を作業ディレクトリとして `xelatex main.tex` を実行してください。目次と参照を確定するには複数回の実行が必要です。

図生成スクリプトは `notebooks/complete/` の完全実装版を参照します。図・数値マクロの一括再生成コマンドは `python scripts/generate_all_figures.py` です。実行環境が異なる場合は計算結果や図の差異を検証してください。

## ライセンス

**再利用ライセンスは現在未設定です。** Publicリポジトリであることだけでは、第三者による複製・改変・再配布を許諾するものではありません。教材とプログラムのライセンスについては [LICENSE_DECISION.md](LICENSE_DECISION.md) を参照してください。

## お問い合わせ

内容の誤りや改善提案は、GitHubのIssuesをご利用ください。
