#!/usr/bin/env python
import sys
from asterisk.agi import *
import mysql.connector
import requests
import time

config = {
  'user': 'asterisk',  #enter your username 
  'password': '************', # enter your password
  'host': '127.0.0.1',
  'database': 'asterisk', #enter your database name =)
  'raise_on_warnings': True
}
#apiKey for weather API
apiKey="CTPWSS4615D4KBMI8LL4PLP77" #this is my api KEY, you can use it or create the new one on weatehr.visualcrossing.com
loc = ""
#Url for weather API
url = "https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/weatherdata/forecast?locations=%s&aggregateHours=24&unitGroup=metric&shortColumnNames=false&contentType=json&key="+apiKey

agi = AGI()
agi.answer()

agi.stream_file("welcome")
agi.stream_file("enter-password")
agi.stream_file("beep")
enterPassword =""
while True:
  result = agi.wait_for_digit(-1)
  if result.isdigit():
    enterPassword = enterPassword+result
  else:
    break

try:
   cnx = mysql.connector.connect(**config)
   cursor = cnx.cursor()
   query = "select password, location from ps_auths p LEFT JOIN UserDetail u ON p.id=u.userID where p.id='%s'" %agi.env["agi_callerid"].strip()
   cursor.execute(query)
   v1 = ""
   for (password,location) in cursor:
      v1 = password
      url = url %location
      loc = location

   cursor.close()
   cnx.close()
except:
    agi.stream_file("goodbye")
    agi.hangup()
 
if enterPassword != v1:
    agi.stream_file("vm-incorrect")
    agi.stream_file("goodbye")
    agi.hangup()

#to change password, didnt find the right wav
agi.stream_file("to-change-your-pin-number")
agi.stream_file("press-1")
agi.stream_file("for-no-press")
agi.say_phonetic(2)
agi.stream_file("beep")

option = ""
while True:
  result = agi.wait_for_digit(-1)
  if result.isdigit() and int(result) <3:
    option = result
    break
  else:
    continue

if option == '1':
    try:
        agi.stream_file("pls-enter-vm-password")
        agi.stream_file("beep")
        number =""
        while True:
            result = agi.wait_for_digit(-1)
            if result.isdigit():
                number += result
            else:
                break

        cnx = mysql.connector.connect(**config)
        cursor = cnx.cursor()
        sqlUpdate = "UPDATE ps_auths SET password = '%s' WHERE id = '%s'" % (number ,agi.env['agi_callerid'].strip())
        agi.verbose(sqlUpdate,1)
        cursor.execute(sqlUpdate)
        cnx.commit()
        cursor.close()
        cnx.close()
        agi.stream_file("your")
        agi.stream_file("vm-password")
        agi.stream_file("T-changed-to")
        agi.say_digits(number,"")
    except:
        agi.stream_file("goodbye")
        agi.hangup()


agi.stream_file("what-time-it-is")
agi.stream_file("press-1")
agi.stream_file("for")
agi.stream_file("date")
agi.stream_file("press-2")
agi.stream_file("for-no-press")
agi.say_number(3,"")
option = ""

while True:
  result = agi.wait_for_digit(-1)
  if result.isdigit():
    if int(result) <4:  
        option = result
        break
  else:
    continue

if option == '1':
    agi.stream_file("current-time-is")
    agi.say_time(int(time.time()),"")
elif option=='2':
    agi.say_date(int(time.time()),"")


if loc!="":
    agi.stream_file("for-the-weather")
    agi.stream_file("press-1")
    agi.stream_file("for-no-press")
    agi.say_number(2,"")
    agi.stream_file("beep")
    option = ""
    while True:
      result = agi.wait_for_digit(-1)
      if result.isdigit():
          if int(result) <3:  
              option = result
              break
      else:
          continue

    if option=='1':
        temp = requests.get(url).json()["locations"][loc]["values"][0]["temp"]
        agi.stream_file("temperature")
        agi.stream_file("in-your-city")
        agi.stream_file("is")
        agi.say_number(temp)
        agi.stream_file("degrees")

agi.stream_file("goodbye")
agi.hangup()
