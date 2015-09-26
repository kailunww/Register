# -*- coding: UTF-8 -*-  
# 全部函數列表：http://dll.uuwise.com/index.php?n=ApiDoc.AllFunc
# 技術QQ:87280085

from ctypes import *
import sys
import os
import hashlib
import binascii
import random

#reload(sys)						#必須，不弄的話漢字有問題
#sys.setdefaultencoding('utf8')	#必須，不弄的話漢字有問題


#得到文件的MD5值函數
def getFileMd5(strFile):  
    file = None;  
    bRet = False;  
    strMd5 = "";  
    try:  
        file = open(strFile, "rb");  
        md5 = hashlib.md5();  
        strRead = "";  
          
        while True:  
            strRead = file.read(8096);  
            if not strRead:  
                break;  
            md5.update(strRead);  
        #read file finish  
        bRet = True;  
        strMd5 = md5.hexdigest();  
    except:  
        bRet = False;  
    finally:  
        if file:  
            file.close()  
  
    return [bRet, strMd5]; 

#獲取文件CRC32碼
def getFileCRC(filename):
    f = None;  
    bRet = False;
    crc = 0;
    blocksize = 1024 * 64
    try:
                f = open(filename, "rb")
                str = f.read(blocksize)
                while len(str) != 0:
                        crc = binascii.crc32(str,crc) & 0xffffffff
                        str = f.read(blocksize)
                f.close()
                bRet = True; 
    except:
        print "compute file crc failed!"+filename
        return 0
    return [bRet, '%x' % crc];

#對服務器返回的識別結果進行校驗
def checkResult(dllResult, s_id, softVerifyKey, codeid):
    bRet = False;
    #服務器返回的是錯誤代碼
    #print(dllResult);
    #print(len(dllResult));
    if(len(dllResult) < 0):
        return [bRet, dllResult];
    #截取出校驗值和識別結果
    items=dllResult.split('_')
    verify=items[0]
    code=items[1]

    localMd5=hashlib.md5('%d%s%d%s'%(s_id, softVerifyKey, codeid, (code.upper()))).hexdigest().upper()
    if(verify == localMd5):
        bRet = True;
        return [bRet, code];
    return [bRet, "校驗結果失敗"]


def getCapcha(pic_file_path):
    code = ""
    result=c_wchar_p("                                              ")	
    code_id = recognizeByCodeTypeAndPath(c_wchar_p(pic_file_path),c_int(2002),result)
    if code_id <= 0:
        print('get result error ,ErrorCode: %d' % code_id)
        code = ""
    else:
        checkedRes=checkResult(result.value, s_id, softVerifyKey, code_id);
        print("the resultID is :%d result is %s" % (code_id,checkedRes[1]))  #識別結果為寬字符類型 c_wchar_p,運用的時候注意轉換一下
        code = checkedRes[1]
    if "timeout" in code.lower() :
        code = ""
    return code
    
UUDLL=os.path.join(os.path.dirname(__file__), 'UUWiseHelper.dll')                   #當前目錄下的優優API接口文件 
#pic_file_path = os.path.join(os.path.dirname(__file__), 'test_pics', 'test1.jpg')   #測試圖片文件
#此處指的當前腳本同目錄中test_pics文件夾下面的test.jpg
#可以修改成你想要的文件路徑
s_id  = 2097                                # 軟件ID
s_key = "b7ee76f547e34516bc30f6eb6c67c7db"  # 軟件Key 獲取方式：http://dll.uuwise.com/index.php?n=ApiDoc.GetSoftIDandKEY
# 加載動態鏈接庫, 需要放在System 的path裡，或者當前目錄下
UU = windll.LoadLibrary(UUDLL)
# 初始化函數調用
#global setSoftInfo, recognizeByCodeTypeAndPath, getResult, uploadFile
setSoftInfo = UU.uu_setSoftInfoW
recognizeByCodeTypeAndPath = UU.uu_recognizeByCodeTypeAndPathW
getResult = UU.uu_getResultW
# For login
uploadFile = UU.uu_UploadFileW
login = UU.uu_loginW
getScore = UU.uu_getScoreW
checkAPi=UU.uu_CheckApiSignW	#api文件校驗函數，調用後返回：MD5（軟件ID+大寫DLL校驗KEY+大寫隨機值參數+優優API文件的MD5值+大寫的優優API文件的CRC32值）
# 初始化函數調用
#優優雲DLL 文件MD5值校驗
#用處：近期有不法份子採用替換優優雲官方dll文件的方式，極大的破壞了開發者的利益
#用戶使用替換過的DLL打碼，導致開發者分成變成別人的，利益受損，
#所以建議所有開發者在軟件裡面增加校驗官方MD5值的函數
#成功集成API文件校驗的作者可免費聯繫客服獲取100元充值卡
dllMd5=getFileMd5(UUDLL);	#api文件的MD5值
dllCRC32=getFileCRC(UUDLL);	#API文件的CRC32值
randChar=hashlib.md5(random.choice('abcdefghijklmnopqrstuvwxyz!@#$%^&*()')).hexdigest();	#隨機字符串，用於讓返回來的結果隨機
softVerifyKey="32F1C86B-E64C-4EAF-8BC1-C142570008BC";	#在開發者後台軟件列表內獲取，請勿洩露此KEY。圖例：http://dll.uuwise.com/index.php?n=ApiDoc.GetSoftIDandKEY
checkStatus=hashlib.md5('%d%s%s%s%s'%(s_id,(softVerifyKey.upper()),(randChar.upper()),(dllMd5[1].upper()),(dllCRC32[1].upper()))).hexdigest();		#服務器返回來的值與此值對應一至則表示成功
#debugPoint = raw_input("Pleas input you user name and press enter:")
serverStatus=c_wchar_p("");	#服務器返回來的結果,serverStatus和checkStatus值一樣的話，就OK
checkAPi(c_int(s_id), c_wchar_p(s_key.upper()),c_wchar_p(randChar.upper()),c_wchar_p(dllMd5[1].upper()),c_wchar_p(dllCRC32[1].upper()),serverStatus);  #調用檢查函數,僅需要調用一次即可，不需要每次上傳圖片都調用一次
#檢查API文件是否被修改
if not (checkStatus == serverStatus.value):
	print("sorry, api file is modified")	#如果API文件被修改，則終止程序
	sys.exit(0)    #終止程序
user_i = 'tomtomtomt12345'
passwd_i = 'HKpaiwei666666'
user = c_wchar_p(user_i)  # 授權用戶名
passwd = c_wchar_p(passwd_i)  # 授權密碼
#setSoftInfo(c_int(s_id), c_wchar_p(s_key))		#設置軟件ID和KEY，僅需要調用一次即可，使用了checkAPi函數的話，就不用使用此函數了
ret = login(user, passwd)		                #用戶登錄，僅需要調用一次即可，不需要每次上傳圖片都調用一次，特殊情況除外，比如當成腳本執行的話
if ret > 0:
    print('login ok, user_id:%d' % ret)                 #登錄成功返回用戶ID
else:
    print('login error,errorCode:%d' %ret )
    sys.exit(0)
ret = getScore(user, passwd)                            #獲取用戶當前剩餘積分
print('The Score of User : %s  is :%d' % (user.value, ret))