import os
import zipfile
class UnzipBhav:
    def  __init__(_self,sourceFolder, unzipDestFolder):
        entries = os.listdir(sourceFolder)
        for entry in entries:
            absPath=sourceFolder+ '\\'+entry
            fileSize=os.path.getsize(absPath)
            print(entry + ":" + str( fileSize))
            if(fileSize>10 and entry.endswith(".zip")):
                with zipfile.ZipFile(sourceFolder + '\\'+entry, 'r') as zip_ref:
                    zip_ref.extractall(unzipDestFolder)




# with zipfile.ZipFile("E:\\data\\01JUL2020.zip", 'r') as zip_ref:
#     zip_ref.extractall("E:\\data\\\extrac")


# UnzipBhav('C:\\my_data\\bhav','C:\\my_data\\bhav\\fno-data')
UnzipBhav('C:\\my_data\\fno','C:\\my_data\\fno\\fno-data')