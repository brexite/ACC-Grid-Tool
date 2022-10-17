from PIL import Image, ImageFont, ImageDraw
import json

def modelToCar(number):
        res = ""
        cf = open('./cars.json', 'rb')
        cars = json.load(cf)

        for car in cars["cars"]:
            if car["value"] == number:
                return str(car["model"] + " " + car["key"])
        return "NaN"
    
def trackCodeToName(track: str):
    cf = open ('./tracks.json', 'rb')
    tracks = json.load(cf)
    return tracks[track]
    
def msToFormattedTime(number):
    if (number == 2147483647):
        return "NO TIME SET"
    millis = (number)%1000
    seconds = int((number/1000)%60)
    minutes = int((number/(1000*60))%60)
    return ('{}:{}.{}'.format(minutes,str(seconds).zfill(2),str(millis).zfill(3)))

with open(r'./config.json', 'rb') as config:
    params = json.load(config)
with open(r'./220808_191738_Q.json', 'rb') as rawData:
    qualiData = json.load(rawData)
print(params["fonts"]["fontLarge"])
startPos = 1
cX = params["startX"]
cY = params["startY"]
spacing = params["spacing"]
maxSize = params["maxSize"]

BannerFont = ImageFont.truetype(str(params["fonts"]["fontLarge"]), 34)
DriverFont = ImageFont.truetype(str(params["fonts"]["fontNorm"]), 38)
table = Image.open(params["table"], 'r')

editImg = ImageDraw.Draw(table)
   
#print(qualiData["sessionResult"]["leaderBoardLines"][0]["timing"])


editImg.text((704,129), qualiData["serverName"], font = BannerFont)
BannerFont = ImageFont.truetype(str(params["fonts"]["fontLarge"]), 26)
editImg.text((681,183), trackCodeToName(qualiData["trackName"]), font = BannerFont, fill='black')

for driver in qualiData["sessionResult"]["leaderBoardLines"]:
    driverName = (str(driver["currentDriver"]["firstName"])[0] + '. ' + driver["currentDriver"]["lastName"])
    lapTime = msToFormattedTime(driver["timing"]["bestLap"])
    editImg.text((cX,cY), str(startPos), font = DriverFont, anchor="mm")
    startPos += 1
    editImg.text((cX+110, cY), driverName, font = DriverFont, anchor="lm")
    editImg.text((cX+1239, cY), str(driver["car"]["raceNumber"]), font = DriverFont, anchor="mm", fill='black')
    editImg.text((cX+1156, cY), str(lapTime), font = DriverFont, anchor="rm")
    print(driverName)
    print(modelToCar(driver["car"]["carModel"]))
    print(lapTime)
    #print(driver["timing"]["bestLap"])
    print('-----------------------------')
    cY += 44
    if startPos >= 16:
        break

table.save("./output/result.png")

table.show()