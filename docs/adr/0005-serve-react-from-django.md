# 0005. React の画面は Django から配信する

## ステータス

承認（2026-11-16）

## コンテキスト

ユーザー登録を、Django のフォームの画面（MPA）、React の画面（SPA）、API の 3 つの形で提供する。SPA を普段の入口とし、JavaScript が使えない人は MPA に案内する。SPA は API で登録し、API の POST には CSRF のチェックがかかる。

React の画面の配信のしかたとして、次の 2 つを比べた。

- 別に配信する: Django と React は API だけでつながり、関係が単純になる。ただし、CSRF のトークンを SPA に渡す API が要る。MPA と同じレイアウトや CSS を使うにも、別の仕組みが要る。
- Django から配信する: 同じオリジンなので、React を読み込む HTML を返すときに CSRF のトークンを cookie で渡せる。MPA と同じレイアウトと CSS をそのまま使え、JavaScript が使えない人を同じサーバーの MPA に案内できる。Django と Vite をつなぐ設定が要る。

SPA の URL の置き場所も比べた。サイトの直下に置くと、リロードしたときにも SPA を返すために、存在しない URL まで SPA の HTML を返すか、画面を足すたびに Django 側にも URL を足すことになる。専用の URL の配下に置けば、その配下だけを SPA に返せばよい。

## 決定

React の画面は、Django が返す HTML の上で動かし、Vite でビルドした結果を Django から配信する。SPA は専用の URL の配下に置き、その配下だけをすべて SPA の HTML に返す。

## 結果

- ビルドしたあとは、Django だけで MPA・SPA・API が動く。
- 開発中は、Django と Vite の開発サーバーの両方を起動する。
- SPA に画面を足しても、Django 側は変わらない。
- React を Django から切り離して配信したくなった場合は、CSRF のトークンの渡し方と、共通の CSS の読み込み方を作り直すことになる。
