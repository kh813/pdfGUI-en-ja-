# pdfGUI
pdfの結合，分割ができるpythonGUI
# 動作条件
Windows10

Mac OS

Ubuntu(だぶん) ※動作未確認
# できること
* pdfの結合
* pdfの分割 

どちらの機能もページ範囲の指定によりその範囲のみ結合，分割が可能  
(分割は1ファイル当たりページ範囲と範囲外の2つに分割可能)


## pdfの結合
1. 右のボタンで「追加」と押すとTreeviewにpdfファイルが追加される．
2. ファイルを選択し結合をクリック!
3. 好きな場所に保存しよう!
## pdf分割
* ページ範囲を指定していない場合  
  1. ファイルを追加
  2. ファイルを選択し下のボタンのpdf分割をクリック!
  3. 好きな場所に保存しよう! 1ページごとに分割されるます.
* ページ範囲を指定している場合  
  1.  ページ範囲のボタンをクリックし最小，最大ページを設定
  2.  Treeviewに表示されていることを確認した後，分割したいpdfをクリック!
  3.  ページ範囲が指定されているファイルは範囲内と範囲外の2ファイルが分割されるぞ!

それ以外にもクリックするとそのPDFファイルを開くことができる．
# 注意点
* 重いファイルを開くとTreeviewに表示されるまで時間がかかるときがある?
* 分割する際，ページ範囲をしていしていないとすべてのページが分割されるので，ページ数が多いとたくさんのファイルが生成されます．
* 動作としてMacとWindows10は確認しているが，Ubuntu等Linuxは動作確認をしていない．
* だいぶ前にpython初心者が書いたコードなのでめっっっっちゃ汚い．自分でも何書いているのかわからない(笑)．でもとりあえず動く．
* 変なテンションで書いたため， エラーメッセージが変．あまり気にしないでください．
* デザインがダサい．Tkinterなので仕方ない部分はある．
# 参考
CubePDF Pageはレイアウトなどを参考にしました．リンクを載せておきます．



    