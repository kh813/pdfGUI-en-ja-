# pdfGUI
pdfの結合，分割ができるpythonGUI(Tkinter)
# 動作条件
Windows10

Mac OS

Ubuntu(だぶん) ※動作未確認
# 実行方法
python3で動作しています．必要なライブラリはPyPDF2だけです．
```
pip install PyPDF2
```
もしくは
```
pip install -r requirements.txt
```
実行方法は該当ディレクトリに移動し
```
python pdf_gui.py
```
これでGUIが起動する．
<div align="center">
<img width="1412" alt="gui" src="https://user-images.githubusercontent.com/118164921/214738576-624c729d-28c4-48e3-bba1-24907787d6c5.png" title="Mac">
Macでの画面
</div>
<div align="center">
<img width="1412" alt="gui" src="https://user-images.githubusercontent.com/118164921/214738576-624c729d-28c4-48e3-bba1-24907787d6c5.png" title="Mac">
Windowsでの画面
</div>

# できること
* pdfの結合 
* pdfの分割 

どちらの機能もページ範囲の指定によりその範囲のみ結合，分割が可能  
(分割は1ファイル当たりページ範囲と範囲外の2つに分割可能)


## pdfの結合
1. 右のボタンで「追加」と押しTreeviewにpdfファイルを追加
2. ファイルを選択し結合をクリック
3. 好きな場所に保存
## pdf分割
* ページ範囲を指定していない場合  
  1. ファイルを追加
  2. ファイルを選択し下のボタンのpdf分割をクリック
  3. 好きな場所に保存
   
   ファイルは1ページごとに分割されます．
* ページ範囲を指定している場合  
  1.  ページ範囲のボタンをクリックし最小，最大ページを設定
  2.  Treeviewに表示されていることを確認した後，分割したいpdfをクリック
  3.  好きな場所に保存
   
   ページ範囲が指定されているファイルは範囲内と範囲外の2ファイルが分割されます．

それ以外にもTreeviewにある選択ファイルをダブルクリックするとそのPDFファイルを開くことができます．
# 注意点
* 重いファイルを開くとTreeviewに表示されるまで時間がかかるときがある．
* 分割する際，ページ範囲をしていしていないとすべてのページが分割されるので，ページ数が多いとたくさんのファイルが生成されます．例えば，100ページあると100枚のpdfが作成されます．
* 動作としてMacとWindows10は確認しているが，Ubuntu等Linuxは動作確認をしていない．
* だいぶ前にpython初心者が書いたコードなのでめっっっっちゃ汚い．自分でも何書いているのかわからない(笑)．でもとりあえず動く．
* 変なテンションで書いたため， エラーメッセージが変．あまり気にしないでください．(たぶん修正します)
* デザインがダサい．Tkinterなので仕方ない部分はあるのか?
* tkinterのバージョンによってはエラーになるかも? 色の設定でエラーになりｍしたが修正済みです．
# 参考
CubePDF Pageはレイアウトなどを参考にしました．リンクを載せておきます．

https://www.cube-soft.jp/cubepdfpage/



    