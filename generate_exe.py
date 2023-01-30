"""
exe,appファイルの作成
"""
import subprocess

def Generate_exe():
    result = subprocess.run("pyinstaller pdf_gui.py --onefile --noconsole", shell=True, stdout=subprocess.PIPE, universal_newlines=True)

if __name__=="__main__":
    Generate_exe()