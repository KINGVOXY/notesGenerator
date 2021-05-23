import json
import sys

__author__  = "Daruo"
__version__ = "1.0.0"
__date__    = "2021-05-23 16:08:46"

class Generator:
    """
    Notesデータを変換するクラス
    もはやクラスである必要はない
    """

    def __init__(self, fname):
        """コンストラクタ

        Args:
            fname (str): ファイル名(.json)
        """
        self.fname = fname
        self.notes = []

    def loadJson(self):
        """Jsonを読み込む

        Returns:
            Any: 読み込んだJsonの配列
        """
        json_open = open(self.fname, 'r', encoding="utf_8_sig")
        json_load = json.load(json_open, strict=False)
        self.json = json_load
        return self.json

    def setDataName(self):
        """曲名のセット
        self追加
        """
        self.dataname = self.json['name']
        print("[設定]曲名: "+ self.dataname)
    
    def setBPM(self):
        """BPMのセット
        self追加
        """
        self.BPM = self.json['BPM']
        print("[設定]BPM: "+ str(self.BPM))

    def setComposer(self,*composer):
        """作曲者のセット
        self追加
        """
        if composer:
            self.composer = composer[0]
            print("[設定]作曲者: "+ self.composer)
        else:
            self.composer = "unknown"
            print("[警告]作曲者: 指定されませんでした")

    def setMul(self,*mul):
        """mul追加
        デフォルトは4
        self追加
        """
        if mul:
            self.mul = mul[0]
            print("[設定]mul: "+str(self.mul))
        else:
            self.mul = 4
            print("[警告]mul: デフォルト値4が設定されます")

    def setNumOfNotes(self):
        """返すノーツセット数を決定する
        """
        self.notes = self.json['notes']
        notes_length = len(self.notes)
        self.num_of_make = int((self.notes[notes_length-1]['num'] - self.notes[0]['num'])/self.mul + 1) # ノーツ数
        print("[設定]全ノーツ数: "+str(self.num_of_make))

    def getPickUpNum(self):
        """ノーツのダブり計測

        Returns:
            list: 各ノーツ番号に含まれるノーツ数
        """
        notes_length = len(self.notes)
        # print(self.notes)
        # numピックアップ
        tmp = []
        num_tmp=[]
        for i in range(notes_length):
            tmp.append(int(self.notes[i]['num']/self.mul))
        for i in range(self.num_of_make):
            num_tmp.append(tmp.count(i))

        return num_tmp
    
    def makeNotesDict(self, pn):
        """返すデータに合わせたノーツ番号を生成
        ここで2と3の同時押しなどを23に変換したりしている。

        Args:
            pn (list): ダブり数(0は休符)

        Returns:
            list: ノーツ番号配列
        """
        data = []
        soeji = 0
        for i in range(len(pn)):
            tmp=""
            if pn[i] != 0:
                for j in range(pn[i]):
                    tmp+=str(self.notes[soeji+j]['block']+1)
            else:
                tmp="-1"

            data.append(int(tmp))
            soeji+=pn[i]
        return data

    def makeTiming(self):
        """タイミングを計測し、配列で返す

        Returns:
            list: タイミング配列
        """
        gap = 60.0/self.BPM
        timing=0
        tmp=[]
        for i in range(self.num_of_make):
            tmp.append(timing)
            timing+=gap
        return tmp

    def makeJson(self):
        """Jsonデータの生成

        Returns:
            Any: Jsonデータ
        """
        pick_num = self.getPickUpNum()
        # print(pick_num)
        linenum_arr = self.makeNotesDict(pick_num)
        timing_arr  = self.makeTiming()
        name = "  \"name\": \""+self.dataname+"\",\n"
        mul = "  \"mul\": "+str(self.mul)+",\n"

        composer = "  \"composer\": \""+ self.composer +"\",\n"

        notes = "  \"notes\": [\n"
        for i in range(self.num_of_make):
            tmp = "    "+str({"line":linenum_arr[i], "type":self.notes[i]['type'], "timing":timing_arr[i]})
            if i<self.num_of_make-1: tmp+=",\n"
            else: tmp+="\n  ]\n"
            notes+=tmp
        
        notes = notes.replace("\'","\"")

        rtn_json = "{\n" + name + mul + composer + notes + "}\n"
        return rtn_json

    def saveJson(self, saveName, madeJson):
        """出来上がったデータの保存

        Args:
            saveName (str): 保存するファイル名
            madeJson (Any): 保存するJsonデータ
        """
        f = open(saveName, "w")
        f.write(madeJson)
        f.close()
        


if __name__=="__main__":
    args = sys.argv
    if len(args)==1: exit()
    gen = Generator("./json/"+args[1])

    print("######################### 読み込み #########################")
    loaded = gen.loadJson()
    loaded = str(loaded).replace("},","},\n").replace("'name'","\n'name'").replace("'maxBlock'","\n'maxBlock'").replace("'BPM'","\n'BPM'").replace("'offset'","\n'offset'").replace("'notes': [{","\n'notes': [\n {").replace("[]}]}","[]}\n]\n}")
    print(loaded)
    print("######################### セッティング #########################")

    gen.setDataName()
    gen.setBPM()
    gen.setMul(4)           # 4以外の時は引数に指定する
    gen.setComposer("")     # 引数に名前を指定する
    gen.setNumOfNotes()

    print("######################### メイク #########################")
    made_json = gen.makeJson()
    print(made_json)

    gen.saveJson("./output/"+args[1], made_json)