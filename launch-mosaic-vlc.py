import json
import os
from PIL import Image, ImageDraw
#from PIL import Image, ImageDraw, ImageFont

mosaicFilename = 'mosaic-vlm-test.conf'
mosaicImageFilename = 'background.png'
mosaicExecuteFileWin = 'executeMosaicStreaming.bat'
mosaicExecuteFileLinux = 'executeMosaicStreaming'

def createExecuteFile(list):
    dir_path = os.path.dirname(os.path.realpath(__file__))
    fullFilePath = dir_path + '\\' + mosaicExecuteFileWin
    print(fullFilePath)
    try:
        if os.path.exists(fullFilePath):
            os.remove(fullFilePath)
    except Exception as e:
        print("No file exist")
        
    vlcLocation = list['mosaic']['vlc-location']
    executeCmd = "\"" + vlcLocation + "\\vlc.exe\"" +  " --image-duration -1 --vlm-conf " +  mosaicFilename
    file = open(fullFilePath, "a")
    file.write(executeCmd)
    file.close
    

def createImageFile(list):
    dir_path = os.path.dirname(os.path.realpath(__file__))
    fullFilePath = dir_path + "\\" + mosaicImageFilename
    print(fullFilePath)
    try:
        if os.path.exists(fullFilePath):
            os.remove(fullFilePath)
    except Exception as e:
        print("No file exist")
        
    width = list['mosaic']['pixels-horizontal']
    height = list['mosaic']['pixels-vertical']
    
    img = Image.new(mode="RGB", size=(int(width), int(height)), color='#000000')
    img.save(fullFilePath)

def createMosaicConfigFile(list):
    dir_path = os.path.dirname(os.path.realpath(__file__))
    fullFilePath = dir_path + '\\' + mosaicFilename
    print(fullFilePath)
    try:
        if os.path.exists(fullFilePath):
            os.remove(fullFilePath)
    except Exception as e:
        print("No file exist")
    
    print("Opening file")
    #print(list)
    
    
    counter = 1
    order_str = ""
    launch_list = []
    file = open(fullFilePath, "a")
    
    
    file.write("### VLC (VLM) configuration: Tile mosaic IP Camera  ###\r\n")
    
    for item in list['mosaic']['ipcitem']:
    
        print(item)
        
     
        ipcCount = "Channel" + str(counter)
        
        file.write("## " + str(counter) + " ##\r\n")
        file.write("new " + ipcCount + " broadcast enabled\r\n")
        file.write("setup " + ipcCount + " option " + item['protocol'] + "\r\n")
        file.write("setup " + ipcCount + " option rtsp-user=" + item['username'] + "\r\n")
        file.write("setup " + ipcCount + " option rtsp-pwd=" + item['password'] + "\r\n")
        file.write("setup " + ipcCount + " input \"" + item['url'] + "\"\r\n")
        file.write("setup " + ipcCount + " output #duplicate{dst=mosaic-bridge{id=" + str(counter) + "},select=video}\r\n")
        file.write("\r\n\r\n")
        
        if(counter == 1):
            order_str = "order=\"1"
        else:
            order_str = order_str + "," + str(counter)
            
        launch_list.append("control Channel" + str(counter) + " play\r\n")
        
        counter = counter + 1

    order_str = order_str + "\""
    
    file.write("## Background ##\r\n")  
    file.write("new background broadcast enabled\r\n")
    file.write("setup background option image-fps=12/1\r\n")
    file.write("setup background input " + "\"" +  dir_path + "\\background.png\"\r\n")
    file.write("setup background output #transcode{sfilter=mosaic{width=2560,height=1440,rows=3,cols=2,borderw=2,borderh=2,position=1," + order_str + "},vcodec=mp4v}:display\r\n")
    
    file.write("\r\n\r\n")
    file.write("## Control ## \r\n")
    for index in launch_list:
         file.write(index)
    file.write("control background play\r\n")
    
    file.close
        

def main():

    with open('mosaic-settings.json') as json_file:
        json_data = json.load(json_file)
        createMosaicConfigFile(json_data)
        createImageFile(json_data)
        createExecuteFile(json_data)
    
if __name__ == '__main__':
    main()
    
    
