import tkinter as tk
import PyPDF2 as pf2
import tkinter.filedialog as fd
import tkinter.messagebox as msg
import tkinter.ttk as ttk
import re
import os
import subprocess
import platform
#osごとの違い
if platform.system()=="Windows":
    process_name="start"
    shell_flag=True
    button_pad=10
elif platform.system()=="Darwin":
    process_name = "open"
    shell_flag=False
    button_pad=0
elif platform.system()=="Linux":
    process_name = "see"
    shell_flag=False
    button_pad = 0

#関数
#終了ボタンの処理
def exit():
    base.destroy()

#ページ範囲判定初期設定
def judge_flags(ind,max=None,min=None):
    if pg_flags[ind]==False:
        pg_max[ind]=None
        pg_min[ind]=None
    else:
        pg_max[ind]=max
        pg_min[ind]=min
#辞書型要素移動
def change_dict_key(d, old_key, new_key, default_value=None):
    d[new_key] = d.pop(old_key, default_value)

#ページ範囲設定
def judge_flagsT(ind):
    a=tree.item(tree.get_children()[ind],"values")
    if not tree.item(tree.get_children()[ind],"values")[2]:
        pg_flags[ind]=False
        pg_max[ind]=None
        pg_min[ind]=None
    else:
        pg_flags[ind]=True
        m=re.search(r'\d+$',tree.item(tree.get_children()[ind],"values")[2])
        h=re.search(r'\d+',tree.item(tree.get_children()[ind],"values")[2])
        pg_max[ind]=int(m.group())
        pg_min[ind]=int(h.group())


#「選択」ボタン処理
def add_file():
    global i
    global filename
    m=tree.selection()
    
    if m:
        h=tree.index(m[-1])
        filename.insert(h+1,fd.askopenfilename(filetypes=[("PDF","*.pdf")]))
        if filename[h+1]=="":
            del filename[h+1]
            return
        elif len(filename)!=len(set(filename)):
            del filename[h+1]
            error_same=msg.showerror("同一名エラー","名前が同じだ　やり直せ")
            return
        try:
            reader=pf2.PdfFileReader(filename[h+1])
            tree.insert("",h+1,values=(os.path.basename(filename[h+1]),reader.numPages,"",filename[h+1]))
            for n in reversed(range(len(filename))[h+2:]):
                change_dict_key(pg_flags,n-1,n)
            pg_flags[h+1]=False
            judge_flags(i)
            for n in reversed(range(len(pg_flags))[h+1:]):
                judge_flags(n,pg_max[n-1],pg_min[n-1])
            i+=1
        except pf2.utils.PdfReadError as e:
            del filename[h+1]
            msg.showerror("pdf破損","pdfが正しくありません。")
    else:
        tmp=fd.askopenfilename(filetypes=[("PDF","*.pdf")])
        filename.append(tmp)
        if filename[i]=="":
            del filename[i]
            return
        elif len(filename)!=len(set(filename)):
            del filename[i]
            error_same=msg.showerror("同一名エラー","名前が同じだ　やり直せ")
            return
        try :
            reader=pf2.PdfFileReader(filename[i])
            tree.insert("","end",values=(os.path.basename(filename[i]),reader.numPages,"",filename[i]))
            pg_flags[i]=False
            judge_flags(i)
            i+=1
        except pf2.utils.PdfReadError:
            del filename[i]
            msg.showerror("pdf破損","pdfが正しくありません。")
    remove_tree()



       
#pdf結合処理
def connect():
    if i<=1:
        return
    else:
        merger=pf2.PdfFileMerger()
        m=tree.selection()
        if len(m)==0:
            for n in range(i):
                if pg_flags[n]==True:
                    merger.append(filename[n],pages=(pg_min[n]-1,pg_max[n]))
                else:
                    merger.append(filename[n])
        else:
            for n in m:
                if pg_flags[tree.index(n)]==True:
                    merger.append(filename[tree.index(n)],pages=(pg_min[tree.index(n)]-1,pg_max[tree.index(n)]))
                else:
                    merger.append(filename[tree.index(n)])
    s=re.sub(r".pdf$",r"_connected.pdf",filename[0])
    h=os.path.basename(s)
    pdfname=fd.asksaveasfilename(initialfile=h,filetypes=[("PDF","*.pdf")])
    if pdfname=="":
        return
    else:
        try:
            merger.write(pdfname)
        except PermissionError:
            msg.showerror("","ファイルが使われています。")
            return
        else:
            subprocess.Popen([process_name,pdfname],shell=shell_flag)
    merger.close()

    
    #pdf分割
def pdf_split():
    if i==0:
        return
    sc=tree.selection()
    dir=fd.askdirectory()
    if dir=="":
            return
    response=msg.askyesno("確認","pdfを開きますか？")
    if len(sc)==0:
        for m in range(i):
            reader=pf2.PdfFileReader(filename[m])
            merger=pf2.PdfFileMerger()
            merger2=pf2.PdfFileMerger()
            if pg_flags[m]==True:
                s=re.sub(r".pdf$",r"_extract1.pdf",filename[m])
                h=os.path.basename(s)
                merger.append(filename[m],pages=(pg_min[m]-1,pg_max[m]))
                try:
                    if os.path.exists("{}/{}".format(dir,h)):
                        n=1
                        s2=re.sub(r".pdf$",r"_extract1(1).pdf",filename[m])
                        h=os.path.basename(s2)
                        while os.path.exists("{}/{}".format(dir,h)):
                            n+=1
                            s2=re.sub(r".pdf$",r"_extract1({}).pdf".format(n),filename[m])
                            h=os.path.basename(s2)
                        merger.write("{}/{}".format(dir,h))
                    else:
                        merger.write("{}/{}".format(dir,h))
                    merger.close()
                    if response==True:
                        subprocess.Popen([process_name,"{}/{}".format(dir,h)],shell=shell_flag)
                except PermissionError:
                    msg.showerror("","ファイルが使われています。")
                    return
                s=re.sub(r".pdf$",r"_extract2.pdf",filename[m])
                h=os.path.basename(s)
                if pg_min[m]==1 and pg_max[m]==reader.numPages:
                    return
                elif pg_min[m]==1:
                    merger2.append(filename[m],pages=(pg_max[m],reader.numPages))
                elif pg_max[m]==reader.numPages:
                    merger2.append(filename[m],pages=(0,pg_min[m]-1))
                else:
                    merger2.append(filename[m],pages=(0,pg_min[m]-1))
                    merger2.append(filename[m],pages=(pg_max[m],reader.numPages))
                try:
                    if os.path.exists("{}/{}".format(dir,h)):
                        n=1
                        s2=re.sub(r".pdf$",r"_extract2(1).pdf",filename[m])
                        h=os.path.basename(s2)
                        while os.path.exists("{}/{}".format(dir,h)):
                            n+=1
                            s2=re.sub(r".pdf$",r"_extract2({}).pdf".format(n),filename[m])
                            h=os.path.basename(s2)
                        merger2.write("{}/{}".format(dir,h))
                        if response==True:
                            subprocess.Popen([process_name,"{}/{}".format(dir,h)],shell=shell_flag)
                    else:
                        merger2.write("{}/{}".format(dir,h))
                        if response==True:
                            subprocess.Popen([process_name,"{}/{}".format(dir,h)],shell=shell_flag)
                except PermissionError:
                    msg.showerror("","ファイルが使われています。")
                    return
                merger2.close()
                
            else:
                reader=pf2.PdfFileReader(filename[m])
                for n in range(reader.numPages):
                    writer=pf2.PdfFileWriter()
                    writer.addPage(reader.getPage(n))
                    s=re.sub(r".pdf$",r"_{}.pdf".format(n+1),filename[m])
                    h=os.path.basename(s)
                    try:
                        if os.path.exists("{}/{}".format(dir,h)):
                            l=1
                            s2=re.sub(r".pdf$",r"_{}(1).pdf".format(n+1),filename[m])
                            h=os.path.basename(s2)
                            while os.path.exists("{}/{}".format(dir,h)):
                                l+=1
                                s2=re.sub(r".pdf$",r"_{}({}).pdf".format(n+1,l),filename[m])
                                h=os.path.basename(s2)
                            with open("{}/{}".format(dir,h),"wb") as f:
                                writer.write(f)
                        else:
                            with open("{}/{}".format(dir,h),"wb") as f:
                                writer.write(f)
                    except PermissionError:
                        msg.showerror("","ファイルが使われています。")
                        return
                    if response==True:
                        subprocess.Popen([process_name,"{}/{}".format(dir,h)],shell=shell_flag)
    else:
        sel_ind=[]
        for n in range(len(sc)):
            sel_ind.append(tree.index(sc[n]))

        for n in sel_ind:
            reader=pf2.PdfFileReader(filename[n])
            merger=pf2.PdfFileMerger()
            merger2=pf2.PdfFileMerger()
            if pg_flags[n]==True:
                s=re.sub(r".pdf$",r"_extract1.pdf",filename[n])
                h=os.path.basename(s)
                merger.append(filename[n],pages=(pg_min[n]-1,pg_max[n]))
                try:
                    if os.path.exists("{}/{}".format(dir,h)):
                        m=1
                        s2=re.sub(r".pdf$",r"_extract1(1).pdf",filename[n])
                        h=os.path.basename(s2)
                        while os.path.exists("{}/{}".format(dir,h)):
                            m+=1
                            s2=re.sub(r".pdf$",r"_extract1({}).pdf".format(m),filename[n])
                            h=os.path.basename(s2)
                        merger.write("{}/{}".format(dir,h))
                        if response==True:
                            subprocess.Popen([process_name,"{}/{}".format(dir,h)],shell=shell_flag)
                    else:
                        merger.write("{}/{}".format(dir,h))
                        if response==True:
                            subprocess.Popen([process_name,"{}/{}".format(dir,h)],shell=shell_flag)
                except PermissionError:
                    msg.showerror("","ファイルが使われています。")
                    return
                merger.close()
                if response==True:
                    subprocess.Popen([process_name,"{}/{}".format(dir,h)],shell=shell_flag)
                s=re.sub(r".pdf$",r"_extract2.pdf",filename[n])
                h=os.path.basename(s)
                if pg_min[n]==1 and pg_max[n]==reader.numPages:
                    return
                elif pg_min[n]==1:
                    merger2.append(filename[n],pages=(pg_max[n],reader.numPages))
                elif pg_max[n]==reader.numPages:
                    merger2.append(filename[n],pages=(0,pg_min[n]-1))
                else:
                    merger2.append(filename[n],pages=(0,pg_min[n]-1))
                    merger2.append(filename[n],pages=(pg_max[n],reader.numPages))
                try:
                    if os.path.exists("{}/{}".format(dir,h)):
                        m=1
                        s2=re.sub(r".pdf$",r"_{}(1).pdf",filename[n])
                        h=os.path.basename(s2)
                        while os.path.exists("{}/{}".format(dir,h)):
                            m+=1
                            s2=re.sub(r".pdf$",r"_extract2({}).pdf".format(m),filename[n])
                            h=os.path.basename(s2)
                        merger2.write("{}/{}".format(dir,h,m))
                        if response==True:
                            subprocess.Popen([process_name,"{}/{}".format(dir,h,m)],shell=shell_flag)
                    else:
                        merger2.write("{}/{}".format(dir,h))
                        if response==True:
                            subprocess.Popen([process_name,"{}/{}".format(dir,h)],shell=shell_flag)
                except PermissionError:
                    msg.showerror("","ファイルが使われています。")
                    return
                merger.close()
            else:
                reader=pf2.PdfFileReader(filename[n])
                for m in range(reader.numPages):
                    writer=pf2.PdfFileWriter()
                    writer.addPage(reader.getPage(m))
                    s=re.sub(r".pdf$",r"_{}.pdf".format(m+1),filename[n])
                    h=os.path.basename(s)
                    try:
                        if os.path.exists("{}/{}".format(dir,h)):
                            l=1
                            s2=re.sub(r".pdf$",r"_{}(1).pdf".format(m+1),filename[n])
                            h=os.path.basename(s2)
                            while os.path.exists("{}/{}".format(dir,h)):
                                l+=1
                                s2=re.sub(r".pdf$",r"_{}({}).pdf".format(m+1,l),filename[n])
                                h=os.path.basename(s2)
                            with open("{}/{}".format(dir,h),"wb") as f:
                                writer.write(f)
                        else:
                            with open("{}/{}".format(dir,h),"wb") as f:
                                writer.write(f)
                    except PermissionError:
                        msg.showerror("","ファイルが使われています。")
                        return
                    if response==True:
                        subprocess.Popen([process_name,"{}/{}".format(dir,h)],shell=shell_flag)
#置換
def pdf_replace():
    global i
    global filename
    m=tree.selection()
    dust=[]
    pg_dust=[]
    #ファイル選択時
    if tree.selection():
        sct_ind=[] #選択インデックス
        for n in range(len(m)):
            sct_ind.append(tree.index(m[n]))
        filename.insert(sct_ind[0],fd.askopenfilename(filetypes=[("PDF","*.pdf")]))
        i+=1
        #キャンセル時
        if not filename[sct_ind[0]]:
            del filename[sct_ind[0]]
            i-=1
            return
        reader=pf2.PdfFileReader(filename[sct_ind[0]])
        tree.insert("",sct_ind[0],values=(os.path.basename(filename[sct_ind[0]]),reader.numPages,"",filename[sct_ind[0]]))
        #選んだファイルを削除
        for n in reversed(sct_ind):
            pg_dust.append(tree.item(tree.get_children()[n+1],"values")[2])
            tree.delete(tree.get_children()[n+1])
            dust.append(filename.pop(n+1))
            i-=1
        pg_dust.reverse()
        dust.reverse()
        #ファイルパスが同じ場合
        if len(filename)!=len(set(filename)):
            tree.delete(tree.get_children()[sct_ind[0]])
            del filename[sct_ind[0]]
            i-=1
            for n in range(len(dust)):
                reader=pf2.PdfFileReader(dust[n])
                tree.insert("",sct_ind[n],values=(os.path.basename(dust[n]),reader.numPages,pg_dust[n],dust[n]))
                filename.insert(sct_ind[n],dust[n])
                i+=1
            msg.showerror("同一名エラー","名前が同じだ　やり直せ")
            return
        #ページ範囲設定
        pg_flags[sct_ind[0]]=False
        pg_min[sct_ind[0]]=None
        pg_max[sct_ind[0]]=None
        for n in range(len(pg_flags))[len(filename):]:
            del pg_flags[n]
            del pg_min[n]
            del pg_max[n]
        for n in range(len(filename)):
            judge_flagsT(n)
#削除処理    
def Delete_pdf():
    global i
    m=tree.selection()
    if i==0:
        return
    if len(m)==0:
        i-=1
        del filename[i]
        del pg_flags[i]
        del pg_min[i]
        del pg_max[i]
        tree.delete(tree.get_children()[i])
       
        return
    else:
        for n in range(len(m)):
            del filename[tree.index(m[n])]
            del pg_flags[i-n-1]
            del pg_min[i-n-1]
            del pg_max[i-n-1]
            tree.delete(m[n])
        i-=len(m)
        for n in range(len(filename)):
            judge_flagsT(n)
#選択ファイルを上に移動
def move_up():
    m=tree.selection()
    dust=[]
    if len(m)==0:
        return
    for n in range(len(m)):
        if tree.index(m[0])==0:
           if tree.index(m[n])==0+n:
                continue
        ind=tree.index(m[n])
        dust.append(filename.pop(ind))
        filename.insert(ind-1,dust.pop(0))
        tree.move(m[n],"",tree.index(m[n])-1)
    for n in range(len(filename)):
        judge_flagsT(n)

    
def move_down():
    m=tree.selection()
    dust=[]
    a=0
    if len(m)==0:
        return
            
    for n in reversed(range(len(m))):
        if tree.index(m[len(m)-1])==i-1:
           if tree.index(m[n])==i-a-1:
                a+=1
                continue
        ind=tree.index(m[n])
        dust.append(filename.pop(ind))
        filename.insert(ind+1,dust.pop(0))
        tree.move(m[n],"",tree.index(m[n])+1)
    for n in range(len(filename)):
        judge_flagsT(n)
#ページ範囲指定ウィンドウ表示
def page_assgn():
    bx=base.winfo_x()
    by=base.winfo_y()
    wb=base.winfo_width()
    hb=base.winfo_height()
    global pw
    global pg_min
    global pg_max
    def validation(afterword):
        return (afterword.isdecimal() and len(afterword)<=2 or len(afterword)==0)
    def print_pg():
            global pg_min,pg_max
            m=tree.selection()
            if entry1.get() or entry2.get():
                if  entry1.get() and not entry2.get():
                    for n in range(len(m)):
                        if int(entry1.get()) > int(tree.item(m[n],"values")[1]) or int(entry1.get())==0:
                            pw.destroy()
                            msg.showerror("","範囲にありません")
                            return
                        pg_flags[tree.index(m[n])]=True
                        judge_flags(tree.index(m[n]),int(entry1.get()),int(entry1.get()))
                        tree.set(m[n],column=3,value="{}".format(pg_min[tree.index(m[n])]))
                elif entry2.get() and not entry1.get():
                    for n in range(len(m)):
                        if int(entry2.get()) > int(tree.item(m[n],"values")[1]) or int(entry2.get())==0:
                            pw.destroy()
                            msg.showerror("","範囲にありません")
                            return
                        pg_flags[tree.index(m[n])]=True
                        judge_flags(tree.index(m[n]),int(entry2.get()),int(entry2.get()))
                        tree.set(m[n],column=3,value="{}".format(pg_max[tree.index(m[n])]))

                else:
                    for n in range(len(m)):
                        if int(entry1.get()) > int(tree.item(m[n],"values")[1]) or int(entry2.get()) > int(tree.item(m[n],"values")[1]) or int(entry1.get())==0 or int(entry2.get())<=1 or int(entry1.get())>int(entry2.get()):
                            pw.destroy()
                            msg.showerror("","範囲にありません")
                            return
                        pg_flags[tree.index(m[n])]=True
                        judge_flags(tree.index(m[n]),int(entry2.get()),int(entry1.get()))
                        tree.set(m[n],column=3,value="{}~{}".format(pg_min[tree.index(m[n])],pg_max[tree.index(m[n])]))
                       
            else:
                for n in range(len(m)):
                    tree.set(m[n],column=3,value="")
                    pg_min[tree.index(m[n])]=None
                    pg_max[tree.index(m[n])]=None
                    pg_flags[tree.index(m[n])]=False
            
            pw.destroy()
    if pw is None or not pw.winfo_exists():

        #ウィンドウ初期設定
        pw=tk.Toplevel(base)
        pw.title("ページ指定")
        px=int(bx+wb/2-125)
        py=int(by+hb/2-100)
        pw.geometry("250x200+{}+{}".format(px,py))
        pw.resizable(width=False,height=False)
        pw.grab_set()
        pw.grid_columnconfigure(0,weight=1)
        pw.grid_columnconfigure(1,weight=2)
        pw.bind("<Return>", lambda event: print_pg())
        pw.attributes("-topmost", True)
        pw.lift()
        pw.focus_force()
        base.attributes("-topmost",False)


        #validatecommand
        intvc=(pw.register(validation),"%P")

        #ラベル
        tk.Label(pw,text="ページ範囲指定",font=("",15,"bold")).grid(column=0,row=0,padx=5,pady=5,columnspan=2)
        tk.Label(pw,text="(数字のみ)").grid(column=0,row=1,padx=5,pady=5,columnspan=2)
        tk.Label(pw,text="最小値",font=("",10,"")).grid(column=0,row=2,padx=5,pady=5)
        tk.Label(pw,text="最大値",font=("",10,"")).grid(column=0,row=3,padx=5,pady=5)

        #テキストボックス
        entry1=tk.Entry(pw,width=20,validate="key",validatecommand=intvc,takefocus=True)
        entry1.focus_set()
        entry2=tk.Entry(pw,width=20,validate="key",validatecommand=intvc,takefocus=True)

        #テキストボックス位置
        entry1.grid(column=1,row=2,padx=5,pady=5)
        entry2.grid(column=1,row=3,padx=5,pady=5)

        
        dec=ttk.Button(pw,text="決定",command=print_pg).grid(column=0,row=4,columnspan=2)

        
        pw.mainloop()
#選択解除
def remove_tree():
    tree.selection_remove(tree.selection())
#選択解除(treeviwのファイル部分以外を選択した場合)
def remove_treeE(event):
    if not tree.identify_row(event.y):
         remove_tree()
#全選択
def select_all():
    tree.selection_add(tree.get_children())
#不明(デバッグ用?)
def select_allE():
    select_all()
#pdfを既定アプリで開く
def open_pdf(event):
    m=tree.selection()
    if len(m)>0:
        for n in range(len(m)):
            pdf=filename[tree.index(m[n])]
            subprocess.Popen([process_name,pdf],shell=shell_flag)
        remove_tree()
#デバッグ用
def print_dict():
    print(filename)
    print("id:",tree.get_children())
    print("select:",tree.selection()) 
    print("i:",i)
    print(base.winfo_geometry())
    print(tree.get_children())
    print("pgflags",pg_flags)
    print("最小値：",pg_min)
    print("最大値：",pg_max)
    #print(tree.item(tree.get_children()[i-1],"values")[2])
    m=re.search(r'\d+$',tree.item(tree.get_children()[i-1],"values")[2])
    print(m.group())
#グローバル変数
filename=[]
#ファイル最後尾インデックス?
i=0
pw=None
pg_min={}
pg_max={}
pg_flags={}
#関数
#ここより下はUI
#Window & Frame初期設定
base=tk.Tk()
base.title("pdf操作")
base.geometry("1300x600+200+200")


base.minsize(1300,600)
base.resizable(width=True,height=True)
base.configure(bg=None)

style=ttk.Style()
style.configure("Treeview.Heading",font=("",10,"normal","italic"))
style.configure("MyButton.TButton",backgroud="red",foreground="black")
style.map("MyButton.TButton",foreground=[("pressed","red"),("active","black")])
#treeview
frame1=tk.Frame(base)
#frame1.configure(background="skyblue")
tree=ttk.Treeview(frame1,show="headings",columns=(1,2,3,4),selectmode="extended")
tree.heading(1,text="ファイル名",command=select_all)
tree.heading(2,text="ページ数",command=select_all)
tree.heading(3,text="ページ範囲",command=select_all)
tree.heading(4,text="ファイルパス",command=select_all)

tree.column(1,width=175)
tree.column(2,width=25,anchor=tk.CENTER)
tree.column(3,width=25,anchor=tk.CENTER)
tree.column(4,width=600,minwidth=250)


tree.pack(padx=10,pady=10,expand=1,fill="both",side=tk.LEFT)
scrollbar=tk.Scrollbar(frame1,orient=tk.VERTICAL,command=tree.yview)
scrollbar.pack(side=tk.RIGHT,fill="both")
tree.configure(yscrollcommand=scrollbar.set)

#bind
tree.bind("<1>",remove_treeE)
tree.bind("<Double-1>",open_pdf)

#各種ボタン設定
#frame2

frame2=tk.Frame(base,width=450,bg="teal")
add=ttk.Button(text="追加",style="MyButton.TButton",padding=[45,button_pad],command=add_file)
up=ttk.Button(text="上移動",style="MyButton.TButton",padding=[45,button_pad],command=move_up)
down=ttk.Button(text="下移動",style="MyButton.TButton",padding=[45,button_pad],command=move_down)
release=ttk.Button(text="選択解除",style="MyButton.TButton",padding=[45,button_pad],command=remove_tree)
delete=ttk.Button(text="削除",style="MyButton.TButton",padding=[45,button_pad],command=Delete_pdf)
allselect=ttk.Button(text="ALL選択",style="MyButton.TButton",padding=[45,button_pad],command=select_all)
replace=ttk.Button(text="置換",style="MyButton.TButton",padding=[45,button_pad],command=pdf_replace)
#frame3
frame3=tk.Frame(base,bg="indianred")
pdf_connect=ttk.Button(text="pdf結合",style="MyButton.TButton",padding=[35,button_pad],command=connect)
show=ttk.Button(text="表示",style="MyButton.TButton",padding=[35,button_pad],command=print_dict)
end=ttk.Button(text="終了",style="MyButton.TButton",padding=[35,button_pad],command=exit)
split=ttk.Button(text="pdf分割",style="MyButton.TButton",padding=[35,button_pad],command=pdf_split)
assign=ttk.Button(text="ページ指定",style="MyButton.TButton",padding=[35,button_pad],command=page_assgn)

#frame設置
frame1.pack(side=tk.LEFT,anchor=tk.NW,in_=base,expand=1,fill="both")
frame2.pack()
frame3.pack(side=tk.BOTTOM,anchor=tk.SE,before=frame1)


#ボタン配置
#frame2

add.pack(anchor=tk.E,padx=10,pady=10,in_=frame2)
replace.pack(anchor=tk.E,padx=10,pady=10,in_=frame2)
up.pack(anchor=tk.E,padx=10,pady=10,in_=frame2)
down.pack(anchor=tk.E,padx=10,pady=10,in_=frame2)
release.pack(anchor=tk.E,padx=10,pady=10,in_=frame2)
allselect.pack(anchor=tk.E,padx=10,pady=10,in_=frame2)
delete.pack(anchor=tk.E,padx=10,pady=10,in_=frame2)
#frame3
split.pack(side=tk.LEFT,anchor=tk.E,padx=10,pady=10,in_=frame3)
pdf_connect.pack(side=tk.LEFT,anchor=tk.E,padx=10,pady=10,in_=frame3)
assign.pack(side=tk.LEFT,anchor=tk.E,padx=10,pady=10,in_=frame3)
#show.pack(side=tk.LEFT,anchor=tk.E,padx=10,pady=10,in_=frame3)
end.pack(side=tk.LEFT,anchor=tk.E,padx=10,pady=10,in_=frame3)

base.mainloop()
