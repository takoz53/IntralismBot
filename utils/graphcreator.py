from utils.playerinfo import PlayerInfo
from utils.rank_scraper import scrapeTop
import plotly.graph_objs as go
import plotly.io as pio
import numpy as np
import cv2

def removeWhitespace(image):
    #Crop image whitespace
    img = cv2.imread(image)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    th, threshed = cv2.threshold(gray, 240, 255, cv2.THRESH_BINARY_INV)
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (11,11))
    morphed = cv2.morphologyEx(threshed, cv2.MORPH_CLOSE, kernel)
    cnts = cv2.findContours(morphed, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[-2]
    cnt = sorted(cnts, key=cv2.contourArea)[-1]
    x,y,w,h = cv2.boundingRect(cnt)
    dst = img[y:y+h, x:x+w]
    cv2.imwrite(image, dst)

def createGraph(players):
    values = []
    rank = []
    username = []
    country = []
    score = []
    accuracy = []
    misses = []
    
    curRank = 1

    for player in players:
        rank.append(curRank)
        username.append(player.userName)
        country.append(player.country)
        score.append(player.points)
        accuracy.append(player.accuracy)
        misses.append(player.misses)
        curRank += 1

    #Add Everything into the Table
    values.append(rank)
    values.append(username)
    values.append(country)
    values.append(score)
    values.append(accuracy)
    values.append(misses)
        
    trace = go.Table(
        #columnwidth = [1, 2, 2, 2, 2, 2],
        header = dict(height = 160,
            values = [['<b>Rank</b>'],['<b>Username</b>'],['<b>Country<b>'],
            ['<b>Score</b>'], ['<b>Avg Accuracy</b>'], ['<b>Avg Misses</b>']],
            line = dict(color='rgb(50, 50, 50)'),
            align = ['center'],
            font = dict(color=['rgb(45, 45, 45)'] * 5, size=100),
            fill = dict(color='#ffda44')),
        cells = dict(values = values,
            line = dict(color='#506784'),
            align = ['left'],
            font = dict(color=['rgb(40, 40, 40)'] * 5, size=96),
            height = 160,
            fill = dict(color=['rgb(228, 222, 249)'])))

    data = [trace]
    fig = go.Figure(data=data)
    pio.write_image(fig, 'top.png', width=5000, height=2500)
    removeWhitespace('top.png')