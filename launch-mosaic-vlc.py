import json
import os
from PIL import Image, ImageDraw
from sys import platform
from datetime import date

### Globals ###
writeToLogBoolean = False
mosaicConfFilename = 'mosaic-vlm.conf'
mosaicImageFilename = 'background.png'
mosaicExecuteFileWin = 'executeMosaicStreaming.bat'
mosaicExecuteFileLin = 'executeMosaicStreaming'
mosaicExecuteFileLinux = 'executeMosaicStreaming'
osPlatform = 'WIN'
fullFilePath = ''
dir_path = os.path.dirname(os.path.realpath(__file__))
fullFilePath = dir_path + "\\" + mosaicImageFilename
LogFilePath = dir_path + "\\log.info"
mosaicImageFullFilePath = ''
mosaicConfFullFilePath = ''
### Globals ###

if platform == "linux" or platform == "linux2":
    osPlatform = 'LIN'
    fullFilePath = dir_path + '/' + mosaicExecuteFileLin
    mosaicImageFullFilePath = dir_path + '/' + mosaicImageFilename
    mosaicConfFullFilePath = dir_path + '/' + mosaicConfFilename

elif platform == "darwin":
    osPlatform = 'LIN'
    fullFilePath = dir_path + '/' + mosaicExecuteFileLin
    mosaicImageFullFilePath = dir_path + '/' + mosaicImageFilename
    mosaicConfFullFilePath = dir_path + '/' + mosaicConfFilename
elif platform == "win32":
    osPlatform = 'WIN'
    fullFilePath = dir_path + '\\' + mosaicExecuteFileWin
    mosaicImageFullFilePath = dir_path + '\\' + mosaicImageFilename
    mosaicConfFullFilePath = dir_path + '\\' + mosaicConfFilename
        
def createExecuteFile(list):
    if(osPlatform == 'WIN'):
        print(fullFilePath)
        try:
            if os.path.exists(fullFilePath):
                os.remove(fullFilePath)
        except Exception as e:
            print("No file exist")
            
        vlcLocation = list['mosaic']['vlc-location']
        executeCmd = "\"" + vlcLocation + "\\vlc.exe\"" +  " --image-duration -1 --vlm-conf " +  mosaicConfFilename   
    elif(osPlatform == 'LIN'):
        print(fullFilePath)
        try:
            if os.path.exists(fullFilePath):
                os.remove(fullFilePath)
        except Exception as e:
            print("No file exist")
            
        vlcLocation = list['mosaic']['vlc-location']
        executeCmd = "\"" + vlcLocation + "/vlc\"" +  " --image-duration -1 --vlm-conf " +  mosaicConfFilename   
    else:
        print("Error: Cannot determine OS")
        
    file = open(fullFilePath, "a")
    file.write(executeCmd)
    file.close    
    

def createImageFile(list):
    print(mosaicImageFullFilePath)
    try:
        if os.path.exists(mosaicImageFullFilePath):
            os.remove(mosaicImageFullFilePath)
    except Exception as e:
        print("No file exist")
        
    width = list['mosaic']['pixels-horizontal']
    height = list['mosaic']['pixels-vertical']
    
    img = Image.new(mode="RGB", size=(int(width), int(height)), color='#000000')
    img.save(mosaicImageFullFilePath)

def createMosaicConfigFile(list):
    print(mosaicConfFullFilePath)
	
    horizontal = list['mosaic']['pixels-horizontal']
    vertical = list['mosaic']['pixels-vertical']
    videoCodec = list['mosaic']['videoCodec']
    audioCodec = list['mosaic']['audioCodec']
    fps = list['mosaic']['fps']
    delay = fps = list['mosaic']['delay']
	
    if(horizontal == ""):
	    horizontal = '1280'
    if(vertical == ""):
	    vertical = '720'
		
    if(videoCodec == ""):
	    videoCodec = 'mp4v'
    if(audioCodec == ""):
	    audioCodec = 'mp4v'
	
    if(fps == ""):
	    fps = '12/1'
		
    try:
        if os.path.exists(mosaicConfFullFilePath):
            os.remove(mosaicConfFullFilePath)
    except Exception as e:
        print("No file exist")
        writeToLog("No file exist")
    
    print("Opening file")
    writeToLog("Opening file")
    
    counter = 1
    order_str = ""
    launch_list = []
    file = open(mosaicConfFullFilePath, "a")
    
    file.write("### VLC (VLM) configuration: Tile mosaic IP Camera  ###\r\n")
    writeToLog("### VLC (VLM) configuration: Tile mosaic IP Camera  ###\r\n")
    
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
        
        # Build ordering command
        if(counter == 1):
            order_str = "order=\"1"
        else:
            order_str = order_str + "," + str(counter)
            
        launch_list.append("control Channel" + str(counter) + " play\r\n")
        
        counter = counter + 1
    
    # Close quotations for ordering command
    order_str = order_str + "\""

    if(list['mosaic']['order'] != "-1"):
        order_str = "order=\""
        order_str = order_str + list['mosaic']['order']
        order_str = order_str + "\""
        print(order_str)

    file.write("## Background ##\r\n")  
    file.write("new background broadcast enabled\r\n")
    file.write("setup background option image-fps=" + fps + "\r\n")
    if(osPlatform == 'WIN'):
        file.write("setup background input " + "\"" +  dir_path + "\\background.png\"\r\n")
    if(osPlatform == 'LIN'):
        file.write("setup background input " + "\"" +  dir_path + "/background.png\"\r\n")

    file.write("setup background output #transcode{sfilter=mosaic{width=" + horizontal + ",height=" + vertical + 
	",rows=3,cols=2,borderw=2,borderh=2,position=1," + order_str + ",delay=" + delay + "},vcodec=" + videoCodec + ",acodec=" + audioCodec + 
	"}:display\r\n")
    
    file.write("\r\n\r\n")
    file.write("## Control ## \r\n")
    for index in launch_list:
         file.write(index)
    file.write("control background play\r\n")
    
    file.close
        
def writeToLog(log):
    today = date.today()
    file = open(LogFilePath, "a")
    file.write(str(today) + " : " + log + "\r\n")
    file.close
    
def main():
    with open('mosaic-settings.json') as json_file:
        json_data = json.load(json_file)
        writeToLogBoolean = json_data['app']['debug']
        for item in json_data['mosaic']['ipcitem']:
            if not item:
                writeToLog("No protocols are present")
                sys.exit()
        createMosaicConfigFile(json_data)
        createImageFile(json_data)
        createExecuteFile(json_data)
    
if __name__ == '__main__':
    main()
    
    
