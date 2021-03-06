# 東証業種別強弱チャート(Sector-Strength-Chart-TSE)

<br>

東京証券取引所の各セクターが市場平均であるTOPIXに対してどの程度のパフォーマンスを誇るのかを算出するWebアプリケーションです。

![IMG_0270](https://user-images.githubusercontent.com/74766908/148157962-20b19cf2-7c12-494a-9263-d25775c61e87.jpg)

デモサイト<br>
https://sector-strength.herokuapp.com

<br>

## 開発のきっかけ

このWebアプリはトレーダー歴2年、プログラミング歴8ヶ月の私が最初に作ったプロダクトになります。

今でこそ株価指数CFDやFXを中心にトレードしている私ですが、トレーディングを始めた当初はもっぱら日本株を扱っていました。
株式投資の難しいところはやはり銘柄選定でしょう。何千とある銘柄の中から投資をするに値する銘柄を見つけなければなりません。

投資初心者なりに色々考えた末に思いついたのが「直近で最も買われている業種の最も買われている銘柄を買い、最も売られている業種の最も売られている銘柄を空売りする」
というものでした。この頃から私は順張りが好きなトレンドフォロワーだったようです。

東京証券取引所に上場している企業はいくつかの業種に分けることができ、業種別株価指数のようにパフォーマンスが数値化されています。
あとはこの指標をチャート等で比較すればいいのですが、なんとそのようなチャートがどこにも見当たらないのです！
いくらググっても証券会社や経済誌の過去の分析記事ばかりで、リアルタイムで業種のパフォーマンスを算出しているサイトがどこにもありません。

つまり日本株の投資家は各業種のパフォーマンスを日々の値動きやニュース等でぼんやりとしか把握していない可能性があります。
それで上手くいっているのなら言うことないのですが、やはり客観的な指標を一目で把握したいですよね。ということで作ったのがこのWebアプリになります。

<br>

## Webアプリケーションの説明

「ホーム」の真ん中にデカデカとあるのがお目当てのチャートです。

左上に「1ヶ月」「3ヶ月」「1年」「5年」「最大」とあるように、それぞれの期間で各業種のパフォーマンスが分かります。
縦軸の上に行くほどTOPIXに対して強く、下に行くほど弱いと言えます。
例えば、1年のチャートで食品セクターの最新値が＋20%だった場合、食品セクターの1年間のパフォーマンスはTOPIXと比較して20%良かったことを意味します。

なぜ"TOPIXに対して"という比較にしたかというと、市場平均と比較しなければ全業種の中の相対的なパフォーマンスが測れないからです。


<br>

## 簡単な内部ロジックの説明

#### 1. TOPIXおよびTOPIX-17シリーズの価格データの取得

サードパーティーのライブラリを使ってYahoo FinanceからTOPIXとTOPIX−17シリーズの価格データを取得します。

<br>

#### 2. データ整形を施した後、対TOPIX指数を算出

Pandasのデータフレームを使用してデータの抽出や欠損値・外れ値の対処をした上で、チャートに出力する対TOPIX指数を算出します。

<br>

#### 3. データベースに格納

SQLAlchemyを経由してローカルではSQLite、デプロイ先のHerokuではHeroku Postgresにデータを格納します。

<br>

#### 4. チャートに描画

Google Chart Toolsを使用して対TOPIX指数をチャートに描画します。
WebアプリケーションのフレームワークにはFlaskを使用しています。


<br>
  
## 工夫した点

* 機能を厳選したシンプルなデザインにすることであらゆる層に使いやすいサイトにした。

* 本来Google Chart Toolsは非レスポンシブだが、JavaScriptのコードを工夫することでレスポンシブにした。

* TOPIXとの相対比較とすることでより本質的な業種のパフォーマンスが分かるようにした。

* 「当サイトについて」や「お問い合わせ」のページを作り、ユーザーに親切なサイトにした。

<br>

## 解決出来ること

#### 1. 日本株の投資家に対して定量的な情報を提供できる
投資対象の業種を判断基準に持つ投資家に対して肌感覚ではない定量的な指標を提示することができます。<br>
堅調な銘柄が多いように見えたり、ニュースで話題になっていたりする業種について、TOPIXとの相対比較によって一目で実態が把握できます。

<br>

#### 2. 株価という視点から世の中の産業の趨勢がわかる
「あそこの業界は今アツい」とか「この業界はもう斜陽産業だ」という社会の雰囲気を株価という視点から検証することができます。<br>
客観的には上昇トレンドであっても市場平均であるTOPIXと比較すると全然ダメであれば、その業界は斜陽と言っていいかもしれません。

<br>

## 今後の展望

* 学習コストの点からjQueryを使用した結果、チャートの表示や切り替えに若干時間がかかる。できるだけ早くReactなどのより高速なライブラリに移行したい。

* 本格的なサービスとして運用・保守していくことを見据え、拡張性や耐障害性を意識したリファクタリングを行う。

* より多くのユーザーに届けるためにGoogle Analyticsを導入してSEO対策をする。

* TOPIX-17シリーズだけでなく東証株価指数33業種や各業種内の銘柄についても同様のチャートを作成してパフォーマンスが分かるようにする。

<br>

## 開発技術
#### 言語
* Python
* HTML
* CSS
* JavaScript

#### フレームワーク・ライブラリ
* Flask
* jQuery
* Pandas
* SQLalchemy


#### API・データ
* [yahoo_finance_api2](https://github.com/pkout/yahoo_finance_api2.git)
