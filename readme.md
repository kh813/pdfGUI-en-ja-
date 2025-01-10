# Special thanks to the original creator

こちらで公開されていたコードをベースに、日英バイリンガル表示化
Based on the following code, English labels added
https://github.com/jean0enuma/pdfGUI

また以下の説明文は原文に英訳をつけました
I added English translation to the following original readme


# pdfGUI
PDFの結合，分割ができるpythonGUI(Tkinter)
Merge / devide PDF

# 動作条件 / Supported environment
- Windows 11 (x64, arm64) 
- macOS
- Ubuntu(だぶん) ※動作未確認 / Maybe, not tested


# 実行方法 / Running the app
python3で動作しています．必要なライブラリはPyPDF2だけです．
Depeinding on PyPDF2 only
```
pip install PyPDF2
```
もしくは
or 
```
pip install -r requirements.txt
```
実行方法は該当ディレクトリに移動し
For starting the app, go to the directory and run 
```
python pdf_gui.py
```
これでGUIが起動する．
<div align="center">
<img width="1412" alt="gui" src="https://user-images.githubusercontent.com/118164921/216750822-6e194a07-8b29-44f6-be16-ea942ea0c823.png" title="Windows">
Windowsでの画面 
Screenshot on Windows
</div>
<br>
<div align="center">
<img width="1412" alt="gui" src="https://user-images.githubusercontent.com/118164921/216751084-27285c0c-5bb2-47ce-813f-7a1ec31b72f9.png" title="Mac">
Macでの画面
</div>
<br>

また実行ファイルを生成する場合は，
To generate the executable file

```
python generate_exe.py
```

と入力するとdistというディレクトリに実行ファイルが生成される．
You'll find the executable file in dist directory

# できること / Features
* PDFの結合 / Merge PDFs
* PDFの分割 / Devide PDF

どちらの機能もページ範囲の指定により，その範囲のみの結合，分割が可能.


## PDFの結合 / Merge PDFs
* 右のボタンで「Add / 追加」と押しTreeviewにPDFファイルを追加
* ファイルを選択し「Merge / 結合」をクリック
* 好きな場所に保存
  
   ページ範囲を指定していると，範囲ページのみが結合対象となる．

* Click "Add / 追加" on the right menu to add the PDF to the Treeview
* Select files and click "Merge / 結合"
* Save it to the directory of your choice
  
  If you select pages, only the selected pages are merged.


## PDF分割 / Devide PDF
* ページ範囲を指定していない場合  
  1. ファイルを追加
  2. ファイルを選択し下のボタンのpdf分割をクリック
  3. 好きな場所に保存
   ファイルは1ページごとに分割されます．
* ページ範囲を指定している場合  
  1.  ページ範囲のボタンをクリックし最小，最大ページを設定
  2.  Treeviewに表示されていることを確認した後，分割したいpdfをクリック
  3.  好きな場所に保存
   
   ページ範囲が指定されているファイルは，範囲内と範囲外の2ファイルが分割されます．
   また，Treeviewにある選択ファイルをダブルクリックすると，そのPDFファイルを開くことができます．

* When the pages are NOT selected 
  1. Add file
  2. Select files and click "Device PDF / PDF" 
  3. Save it to the directory of your choice
   File is devided per page．

* When the pages are selected 
  1.  Click "Page range" and specify min/max pages
  2.  Make sure it's listed on Treeview, then click "Device PDF / PDF" 
  3.  Save it to the directory of your choice
   
   You'll get in/out range pages for those files with the page range selected.
   You can open teh file by clicking the list in the Treeview


# 注意点 / Remarks
* 重いファイルを開くとTreeviewに表示されるまで時間がかかるときがある．
* 分割する際，ページ範囲をしていしていないとすべてのページが分割されるので，ページ数が多いとたくさんのファイルが生成されます．例えば，100ページあると100枚のpdfが作成されます．
* 動作としてMacとWindows10は確認しているが，Ubuntu等Linuxは動作確認をしていない．
* だいぶ前にpython初心者が書いたコードなので，とっても汚い．自分でも何書いているのかわからない(笑)．でもとりあえず動く．
* 変なテンションで書いたため， エラーメッセージが変．あまり気にしないでください．(たぶん修正します)
* デザインがダサい．Tkinterなので仕方ない部分はあるのか?
* tkinterのバージョンによってはエラーになるかも? 色の設定でエラーになりましたが修正済みです．

* Opening large files may take some time to display in the Treeview.
* If you don't specify a page range when splitting, all pages will be split. For example, a 100-page PDF will be split into 100 individual PDFs.
* The application has been tested on Mac and Windows 10, but not on Ubuntu or other Linux distributions.
* This code was written by a Python beginner a long time ago, so it's quite messy. Even I can't really understand what I wrote (lol). But it works.
* I wrote this with a strange tone, so the error messages might be a bit odd. Please don't mind it too much. (I'll probably fix it later.)
* The design is pretty ugly. Is this unavoidable with Tkinter?
* Depending on the Tkinter version, you might encounter errors. I had an issue with color settings, but I've fixed it.


# 参考
CubePDF Pageはレイアウトなどを参考にしました．リンクを載せておきます．

https://www.cube-soft.jp/cubepdfpage/



    