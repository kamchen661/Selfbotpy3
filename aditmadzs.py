# -*- coding: utf-8 -*-

from LineAPI.linepy import *
from gtts import gTTS
from bs4 import BeautifulSoup
from datetime import datetime
from googletrans import Translator
import ast, codecs, json, os, pytz, re, random, requests, sys, time, urllib.parse

listApp = ["CHROMEOS", "DESKTOPWIN", "DESKTOPMAC", "IOSIPAD", "WIN10"]
try:
	for app in listApp:
		try:
			try:
				with open("authToken.txt", "r") as token:
					authToken = token.read()
					if not authToken:
						client = LINE()
						with open("authToken.txt","w") as token:
							token.write(client.authToken)
						continue
					client = LINE(authToken, speedThrift=False, appName="{}\t2.1.5\tAditmadzs\t11.2.5".format(app))
				break
			except Exception as error:
				print(error)
				if error == "REVOKE":
					exit()
				elif "auth" in error:
					continue
				else:
					exit()
		except Exception as error:
			print(error)
except Exception as error:
	print(error)
with open("authToken.txt", "w") as token:
    token.write(str(client.authToken))
clientMid = client.profile.mid
clientStart = time.time()
clientPoll = OEPoll(client)

languageOpen = codecs.open("language.json","r","utf-8")
readOpen = codecs.open("read.json","r","utf-8")
settingsOpen = codecs.open("setting.json","r","utf-8")
unsendOpen = codecs.open("unsend.json","r","utf-8")

language = json.load(languageOpen)
read = json.load(readOpen)
settings = json.load(settingsOpen)
unsend = json.load(unsendOpen)

def restartBot():
	print ("[ 訊息 ] BOT 重啟")
	python = sys.executable
	os.execl(python, python, *sys.argv)

def logError(text):
    client.log("[ 錯誤 ] {}".format(str(text)))
    tz = pytz.timezone("Asia/Makassar")
    timeNow = datetime.now(tz=tz)
    timeHours = datetime.strftime(timeNow,"(%H:%M)")
    day = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday","Friday", "Saturday"]
    hari = ["minggu", "Senin", "Selasa", "rabu", "Kamis", "Jumat", "Sabtu"]
    bulan = ["Januari", "Februari", "Maret", "April", "Mei", "Juni", "Juli", "Agustus", "September", "Oktober", "November", "Desember"]
    inihari = datetime.now(tz=tz)
    hr = inihari.strftime('%A')
    bln = inihari.strftime('%m')
    for i in range(len(day)):
        if hr == day[i]: hasil = hari[i]
    for k in range(0, len(bulan)):
        if bln == str(k): bln = bulan[k-1]
    time = "{}, {} - {} - {} | {}".format(str(hasil), str(inihari.strftime('%d')), str(bln), str(inihari.strftime('%Y')), str(inihari.strftime('%H:%M:%S')))
    with open("errorLog.txt","a") as error:
        error.write("\n[{}] {}".format(str(time), text))

def timeChange(secs):
	mins, secs = divmod(secs,60)
	hours, mins = divmod(mins,60)
	days, hours = divmod(hours,24)
	weeks, days = divmod(days,7)
	months, weeks = divmod(weeks,4)
	text = ""
	if months != 0: text += "%02d 月" % (months)
	if weeks != 0: text += " %02d 禮拜" % (weeks)
	if days != 0: text += " %02d 天" % (days)
	if hours !=  0: text +=  " %02d 小時" % (hours)
	if mins != 0: text += " %02d 分鐘" % (mins)
	if secs != 0: text += " %02d 秒" % (secs)
	if text[0] == " ":
		text = text[1:]
	return text

def command(text):
	pesan = text.lower()
	if settings["setKey"] == True:
		if pesan.startswith(settings["keyCommand"]):
			cmd = pesan.replace(settings["keyCommand"],"")
		else:
			cmd = "Undefined command"
	else:
		cmd = text.lower()
	return cmd

def backupData():
	try:
		backup = read
		f = codecs.open('read.json','w','utf-8')
		json.dump(backup, f, sort_keys=True, indent=4, ensure_ascii=False)
		backup = settings
		f = codecs.open('setting.json','w','utf-8')
		json.dump(backup, f, sort_keys=True, indent=4, ensure_ascii=False)
		backup = unsend
		f = codecs.open('unsend.json','w','utf-8')
		json.dump(backup, f, sort_keys=True, indent=4, ensure_ascii=False)
		return True
	except Exception as error:
		logError(error)
		return False

def menuHelp():
	if settings['setKey'] == True:
		key = settings['keyCommand']
	else:
		key = ''
	menuHelp =   "╭━━━━━━━━━━━━━━━━━━━━━" + "\n" + \
                "┃〔 單體半垢 〕" + "\n" + \
                "┃〔 Help Message 〕━━" + "\n" + \
                "┃〔 Meun  〕━━━" + "\n" + \
		        "┃" + key + "Help 幫助\n" +\
		        "┃〔 Status Command 〕━━" + "\n" + \
		        "┃MyKey 我的鑰匙" + "\n" + \
		        "┃" + key + "登出" + "\n" + \
		        "┃" + key + "重啟" + "\n" + \
		        "┃" + key + "運行時間" + "\n" + \
		        "┃" + key + "速度" + "\n" + \
		        "┃" + key + "狀態" + "\n" + \
		        "┃〔 Settings Command 〕━" + "\n" + \
                "┃SetKey 「On/Off」 " + "\n" + \
                "┃" + key + "自動添加 「開/關」" + "\n" + \
                "┃" + key + "自動入群 「開/關」" + "\n" + \
                "┃" + key + "自動加入票卷 「開/關」" + "\n" + \
                "┃" + key + "自動已讀 「開/關」" + "\n" + \
                "┃" + key + "自動回覆 「開/關」" + "\n" + \
                "┃" + key + "查看友資 「開/關」" + "\n" + \
                "┃" + key + "查看貼文 「開/關」" + "\n" + \
                "┃" + key + "查看貼圖 「開/關」" + "\n" + \
                "┃" + key + "查看收回 「開/關」" + "\n" + \
                "┃" + key + "SetKey: 「text」" + "\n" + \
                "┃" + key + "自動添加消息 「開/關」" + "\n" + \
                "┃" + key + "設置自動回覆消息 「開/關」" + "\n" + \
                "┃" + key + "設置自動加入消息 「開/關」" + "\n" + \
		        "┃〔 Self Command 〕━━" + "\n" + \
                "┃" + key + "更改名稱: 「Text」" + "\n" + \
                "┃" + key + "更改個簽: 「Text」" + "\n" + \
                "┃" + key + "Me" + "\n" + \
                "┃" + key + "我的mid" + "\n" + \
                "┃" + key + "我的名稱" + "\n" + \
                "┃" + key + "我的個簽" + "\n" + \
                "┃" + key + "我的頭貼" + "\n" + \
                "┃" + key + "我的影片" + "\n" + \
                "┃" + key + "我的封面" + "\n" + \
                "┃" + key + "我的個人資料" + "\n" + \
                "┃" + key + "Mid @Mention" + "\n" + \
                "┣" + key + "名稱 @Mention" + "\n" + \
                "┃" + key + "個簽 @Mention" + "\n" + \
                "┃" + key + "頭貼 @Mention" + "\n" + \
                "┃" + key + "個人影片 @Mention 個人影片" + "\n" + \
                "┃" + key + "封面 @Mention" + "\n" + \
                "┃" + key + "複製個人資料 @Mention" + "\n" + \
                "┃" + key + "恢復個人資料" + "\n" + \
                "┃" + key + "備份個人資料" + "\n" + \
                "┃" + key + "朋友列表" + "\n" + \
                "┃" + key + "朋友資料 「Number」" + "\n" + \
                "┃" + key + "封鎖名單" + "\n" + \
                "┃" + key + "朋友廣播" + "\n" + \
                "┃" + key + "更改頭貼" + "\n" + \
		        "┃〔 Group Command 〕━━" + "\n" + \
                "┃" + key + "更改群組名「Text」" + "\n" + \
                "┃" + key + "群組創建者" + "\n" + \
                "┃" + key + "群組ID" + "\n" + \
                "┃" + key + "群組名稱" + "\n" + \
                "┃" + key + "群組圖片" + "\n" + \
                "┃" + key + "開啟網址" + "\n" + \
                "┃" + key + "關閉網址" + "\n" + \
                "┃" + key + "群組列表" + "\n" + \
                "┃" + key + "成員名單" + "\n" + \
                "┃" + key + "待定名單" + "\n" + \
                "┃" + key + "群組資訊" + "\n" + \
                "┣" + key + "群組廣播「Text」" + "\n" + \
                "┃" + key + "更改群組圖片" + "\n" + \
		        "┃〔 Special Command 〕━━" + "\n" + \
                "┃" + key + "模仿 「開/關」" + "\n" + \
                "┃" + key + "模仿名單" + "\n" + \
                "┃" + key + "模仿添加 @Mention" + "\n" + \
                "┃" + key + "模仿刪除 @Mention" + "\n" + \
                "┃" + key + "標記全部" + "\n" + \
                "┃" + key + "已讀點 「開/關」" + "\n" + \
                "┃" + key + "查看已讀" + "\n" + \
		        "┃〔 Media Command 〕━━" + "\n" + \
                "┃" + key + "IG資訊 「Username」" + "\n" + \
                "┃" + key + "搜尋音樂 「Search」" + "\n" + \
                "┃" + key + "從YouTube搜尋 「Search」" + "\n" + \
		        "╰━━━〔 製作者 : ©楓糖™  〕"
	return menuHelp

def menuTextToSpeech():
	if settings['setKey'] == True:
		key = settings['keyCommand']
	else:
		key = ''
	menuTextToSpeech =	"╔══[ Text To Speech ]" + "\n" + \
				"╠ " + key + "af : Afrikaans" + "\n" + \
				"╠ " + key + "sq : Albanian" + "\n" + \
				"╠ " + key + "ar : Arabic" + "\n" + \
				"╠ " + key + "hy : Armenian" + "\n" + \
				"╠ " + key + "bn : Bengali" + "\n" + \
				"╠ " + key + "ca : Catalan" + "\n" + \
				"╠ " + key + "zh : Chinese" + "\n" + \
				"╠ " + key + "zh-cn : Chinese (Mandarin/China)" + "\n" + \
				"╠ " + key + "zh-tw : Chinese (Mandarin/Taiwan)" + "\n" + \
				"╠ " + key + "zh-yue : Chinese (Cantonese)" + "\n" + \
				"╠ " + key + "hr : Croatian" + "\n" + \
				"╠ " + key + "cs : Czech" + "\n" + \
				"╠ " + key + "da : Danish" + "\n" + \
				"╠ " + key + "nl : Dutch" + "\n" + \
				"╠ " + key + "en : English" + "\n" + \
				"╠ " + key + "en-au : English (Australia)" + "\n" + \
				"╠ " + key + "en-uk : English (United Kingdom)" + "\n" + \
				"╠ " + key + "en-us : English (United States)" + "\n" + \
				"╠ " + key + "eo : Esperanto" + "\n" + \
				"╠ " + key + "fi : Finnish" + "\n" + \
				"╠ " + key + "fr : French" + "\n" + \
				"╠ " + key + "de : German" + "\n" + \
				"╠ " + key + "el : Greek" + "\n" + \
				"╠ " + key + "hi : Hindi" + "\n" + \
				"╠ " + key + "hu : Hungarian" + "\n" + \
				"╠ " + key + "is : Icelandic" + "\n" + \
				"╠ " + key + "id : Indonesian" + "\n" + \
				"╠ " + key + "it : Italian" + "\n" + \
				"╠ " + key + "ja : Japanese" + "\n" + \
				"╠ " + key + "km : Khmer (Cambodian)" + "\n" + \
				"╠ " + key + "ko : Korean" + "\n" + \
				"╠ " + key + "la : Latin" + "\n" + \
				"╠ " + key + "lv : Latvian" + "\n" + \
				"╠ " + key + "mk : Macedonian" + "\n" + \
				"╠ " + key + "no : Norwegian" + "\n" + \
				"╠ " + key + "pl : Polish" + "\n" + \
				"╠ " + key + "pt : Portuguese" + "\n" + \
				"╠ " + key + "ro : Romanian" + "\n" + \
				"╠ " + key + "ru : Russian" + "\n" + \
				"╠ " + key + "sr : Serbian" + "\n" + \
				"╠ " + key + "si : Sinhala" + "\n" + \
				"╠ " + key + "sk : Slovak" + "\n" + \
				"╠ " + key + "es : Spanish" + "\n" + \
				"╠ " + key + "es-es : Spanish (Spain)" + "\n" + \
				"╠ " + key + "es-us : Spanish (United States)" + "\n" + \
				"╠ " + key + "sw : Swahili" + "\n" + \
				"╠ " + key + "sv : Swedish" + "\n" + \
				"╠ " + key + "ta : Tamil" + "\n" + \
				"╠ " + key + "th : Thai" + "\n" + \
				"╠ " + key + "tr : Turkish" + "\n" + \
				"╠ " + key + "uk : Ukrainian" + "\n" + \
				"╠ " + key + "vi : Vietnamese" + "\n" + \
				"╠ " + key + "cy : Welsh" + "\n" + \
				"╚══[ Jangan Typo ]" + "\n" + "\n\n" + \
				"Contoh : " + key + "say-id Aditmadzs"
	return menuTextToSpeech

def menuTranslate():
	if settings['setKey'] == True:
		key = settings['keyCommand']
	else:
		key = ''
	menuTranslate =	"╭━━〔 T R A N S L A T E 〕" + "\n" + \
                       "┃🇮🇩┃ af : afrikaans" + "\n" + \
                       "┃🇮🇩┃ sq : albanian" + "\n" + \
                       "┃🇮🇩┃ am : amharic" + "\n" + \
                       "┃🇮🇩┃ ar : arabic" + "\n" + \
                       "┃🇮🇩┃ hy : armenian" + "\n" + \
                       "┃🇮🇩┃ az : azerbaijani" + "\n" + \
                       "┃🇮🇩┃ eu : basque" + "\n" + \
                       "┃🇮🇩┃ be : belarusian" + "\n" + \
                       "┃🇮🇩┃ bn : bengali" + "\n" + \
                       "┃🇮🇩┃ bs : bosnian" + "\n" + \
                       "┃🇮🇩┃ bg : bulgarian" + "\n" + \
                       "┃🇮🇩┃ ca : catalan" + "\n" + \
                       "┃🇮🇩┃ ceb : cebuano" + "\n" + \
                       "┃🇮🇩┃ ny : chichewa" + "\n" + \
                       "┃🇮🇩┃ zh-cn : chinese (simplified)" + "\n" + \
                       "┃🇮🇩┃ zh-tw : chinese (traditional)" + "\n" + \
                       "┃🇮🇩┃ co : corsican" + "\n" + \
                       "┃🇮🇩┃ hr : croatian" + "\n" + \
                       "┃🇮🇩┃ cs : czech" + "\n" + \
                       "┃🇮🇩┃ da : danish" + "\n" + \
                       "┃🇮🇩┃ nl : dutch" + "\n" + \
                       "┃🇮🇩┃ en : english" + "\n" + \
                       "┃🇮🇩┃ eo : esperanto" + "\n" + \
                       "┃🇮🇩┃ et : estonian" + "\n" + \
                       "┃🇮🇩┃ tl : filipino" + "\n" + \
                       "┃🇮🇩┃ fi : finnish" + "\n" + \
                       "┃🇮🇩┃ fr : french" + "\n" + \
                       "┃🇮🇩┃ fy : frisian" + "\n" + \
                       "┃🇮🇩┃ gl : galician" + "\n" + \
                       "┃🇮🇩┃ ka : georgian" + "\n" + \
                       "┃🇮🇩┃ de : german" + "\n" + \
                       "┃🇮🇩┃ el : greek" + "\n" + \
                       "┃🇮🇩┃ gu : gujarati" + "\n" + \
                       "┃🇮🇩┃ ht : haitian creole" + "\n" + \
                       "┃🇮🇩┃ ha : hausa" + "\n" + \
                       "┃🇮🇩┃ haw : hawaiian" + "\n" + \
                       "┃🇮🇩┃ iw : hebrew" + "\n" + \
                       "┃🇮🇩┃ hi : hindi" + "\n" + \
                       "┃🇮🇩┃ hmn : hmong" + "\n" + \
                       "┃🇮🇩┃ hu : hungarian" + "\n" + \
                       "┃🇮🇩┃ is : icelandic" + "\n" + \
                       "┃🇮🇩┃ ig : igbo" + "\n" + \
                       "┃🇮🇩┃ id : indonesian" + "\n" + \
                       "┃🇮🇩┃ ga : irish" + "\n" + \
                       "┃🇮🇩┃ it : italian" + "\n" + \
                       "┃🇮🇩┃ ja : japanese" + "\n" + \
                       "┃🇮🇩┃ jw : javanese" + "\n" + \
                       "┃🇮🇩┃ kn : kannada" + "\n" + \
                       "┃🇮🇩┃ kk : kazakh" + "\n" + \
                       "┃🇮🇩┃ km : khmer" + "\n" + \
                       "┃🇮🇩┃ ko : korean" + "\n" + \
                       "┃🇮🇩┃ ku : kurdish (kurmanji)" + "\n" + \
                       "┃🇮🇩┃ ky : kyrgyz" + "\n" + \
                       "┃🇮🇩┃ lo : lao" + "\n" + \
                       "┃🇮🇩┃ la : latin" + "\n" + \
                       "┃🇮🇩┃ lv : latvian" + "\n" + \
                       "┃🇮🇩┃ lt : lithuanian" + "\n" + \
                       "┃🇮🇩┃ lb : luxembourgish" + "\n" + \
                       "┃🇮🇩┃ mk : macedonian" + "\n" + \
                       "┃🇮🇩┃ mg : malagasy" + "\n" + \
                       "┃🇮🇩┃ ms : malay" + "\n" + \
                       "┃🇮🇩┃ ml : malayalam" + "\n" + \
                       "┃🇮🇩┃ mt : maltese" + "\n" + \
                       "┃🇮🇩┃ mi : maori" + "\n" + \
                       "┃🇮🇩┃ mr : marathi" + "\n" + \
                       "┃🇮🇩┃ mn : mongolian" + "\n" + \
                       "┃🇮🇩┃ my : myanmar (burmese)" + "\n" + \
                       "┃🇮🇩┃ ne : nepali" + "\n" + \
                       "┃🇮🇩┃ no : norwegian" + "\n" + \
                       "┃🇮🇩┃ ps : pashto" + "\n" + \
                       "┃🇮🇩┃ fa : persian" + "\n" + \
                       "┃🇮🇩┃ pl : polish" + "\n" + \
                       "┃🇮🇩┃ pt : portuguese" + "\n" + \
                       "┃🇮🇩┃ pa : punjabi" + "\n" + \
                       "┃🇮🇩┃ ro : romanian" + "\n" + \
                       "┃🇮🇩┃ ru : russian" + "\n" + \
                       "┃🇮🇩┃ sm : samoan" + "\n" + \
                       "┃🇮🇩┃ gd : scots gaelic" + "\n" + \
                       "┃🇮🇩┃ sr : serbian" + "\n" + \
                       "┃🇮🇩┃ st : sesotho" + "\n" + \
                       "┃🇮🇩┃ sn : shona" + "\n" + \
                       "┃🇮🇩┃ sd : sindhi" + "\n" + \
                       "┃🇮🇩┃ si : sinhala" + "\n" + \
                       "┃🇮🇩┃ sk : slovak" + "\n" + \
                       "┃🇮🇩┃ sl : slovenian" + "\n" + \
                       "┃🇮🇩┃ so : somali" + "\n" + \
                       "┃🇮🇩┃ es : spanish" + "\n" + \
                       "┃🇮🇩┃ su : sundanese" + "\n" + \
                       "┃🇮🇩┃ sw : swahili" + "\n" + \
                       "┃🇮🇩┃ sv : swedish" + "\n" + \
                       "┃🇮🇩┃ tg : tajik" + "\n" + \
                       "┃🇮🇩┃ ta : tamil" + "\n" + \
                       "┃🇮🇩┃ te : telugu" + "\n" + \
                       "┃🇮🇩┃ th : thai" + "\n" + \
                       "┃🇮🇩┃ tr : turkish" + "\n" + \
                       "┃🇮🇩┃ uk : ukrainian" + "\n" + \
                       "┃🇮🇩┃ ur : urdu" + "\n" + \
                       "┃🇮🇩┃ uz : uzbek" + "\n" + \
                       "┃🇮🇩┃ vi : vietnamese" + "\n" + \
                       "┃🇮🇩┃ cy : welsh" + "\n" + \
                       "┃🇮🇩┃ xh : xhosa" + "\n" + \
                       "┃🇮🇩┃ yi : yiddish" + "\n" + \
                       "┃🇮🇩┃ yo : yoruba" + "\n" + \
                       "┃🇮🇩┃ zu : zulu" + "\n" + \
                       "┃🇮🇩┃ fil : Filipino" + "\n" + \
                       "┃🇮🇩┃ he : Hebrew" + "\n" + \
                       "╰━━〔 Jangan Typo 〕" + "\n" + "\n\n" + \
		               "Contoh : " + key + "tr-id Aditmadzs"
	return menuTranslate

def clientBot(op):
	try:
		if op.type == 0:
			print ("[ 0 ] 運行結束")
			return

		if op.type == 5:
			print ("[ 5 ] 通知添加聯繫人")
			if settings["autoAdd"] == True:
				client.findAndAddContactsByMid(op.param1)
			client.sendMention(op.param1, settings["autoAddMessage"], [op.param1])

		if op.type == 13:
			print ("[ 13 ] 通知邀請進入群組")
			if settings["autoJoin"] and clientMid in op.param3:
				client.acceptGroupInvitation(op.param1)
				client.sendMention(op.param1, settings["autoJoinMessage"], [op.param2])

		if op.type == 25:
			try:
				print("[ 25 ] 傳送訊息")
				msg = op.message
				text = str(msg.text)
				msg_id = msg.id
				receiver = msg.to
				sender = msg._from
				cmd = command(text)
				setKey = settings["keyCommand"].title()
				if settings["setKey"] == False:
					setKey = ''
				if msg.toType == 0 or msg.toType == 1 or msg.toType == 2:
					if msg.toType == 0:
						if sender != client.profile.mid:
							to = sender
						else:
							to = receiver
					elif msg.toType == 1:
						to = receiver
					elif msg.toType == 2:
						to = receiver
					if msg.contentType == 0:
						if cmd == "登出":
							client.sendMessage(to, "成功關閉BOT")
							sys.exit("[　訊息　] 機器關閉")
							return
						elif cmd == "重啟":
							client.sendMessage(to, "成功重置機器人")
							restartBot()
						elif cmd == "速度":
							start = time.time()
							client.sendMessage(to, "拼命測速中......")
							elapsed_time = time.time() - start
							client.sendMessage(to, "訊息反應速度 {} 秒".format(str(elapsed_time)))
						elif cmd == "運行時間":
							timeNow = time.time()
							runtime = timeNow - clientStart
							runtime = timeChange(runtime)
							client.sendMessage(to, "BOT已運行 {}".format(str(runtime)))
						elif cmd.startswith("setkey: "):
							sep = text.split(" ")
							key = text.replace(sep[0] + " ","")
							if " " in key:
								client.sendMessage(to, "密鑰不能使用空格")
							else:
								settings["keyCommand"] = str(key).lower()
								client.sendMessage(to, "成功將命令鍵設置為 : 「{}」".format(str(key).lower()))
						elif cmd == "help":
							helpMessage = menuHelp()
							contact = client.getContact(sender)
							icon = "http://dl.profile.line-cdn.net/{}".format(contact.pictureStatus)
							name = contact.displayName
							link = "https://pa1.narvii.com/6547/d29a5e4bb3405d83fc15cf50ec057f41640618a8_hq.gif"
							client.sendFooter(to, helpMessage, icon, name, link)
							client.sendContact(to, "uec6d62c3e4a61f033332bc1d86133e49")
						elif cmd == "texttospeech":
							helpTextToSpeech = menuTextToSpeech()
							contact = client.getContact(sender)
							icon = "http://dl.profile.line-cdn.net/{}".format(contact.pictureStatus)
							name = contact.displayName
							link = "https://pa1.narvii.com/6547/d29a5e4bb3405d83fc15cf50ec057f41640618a8_hq.gif"
							client.sendFooter(to, helpTextToSpeech, icon, name, link)
						elif cmd == "translate":
							helpTranslate = menuTranslate()
							contact = client.getContact(sender)
							icon = "http://dl.profile.line-cdn.net/{}".format(contact.pictureStatus)
							name = contact.displayName
							link = "https://pa1.narvii.com/6547/d29a5e4bb3405d83fc15cf50ec057f41640618a8_hq.gif"
							client.sendFooter(to, helpTranslate, icon, name, link)
						elif cmd == "誰最可愛"
					                client.sendContact(to, "uec6d62c3e4a61f033332bc1d86133e49")
							client.sendMessage(to, "他最可愛:3")
						
							


						elif cmd == "狀態":
							try:
								ret_ = "╔══[ 目前狀態 ]"
								if settings["autoAdd"] == True: ret_ += "\n╠ 自動添加 : 開"
								else: ret_ += "\n╠ 自動添加 : 關"
								if settings["autoJoin"] == True: ret_ += "\n╠ 自動入群 : 開"
								else: ret_ += "\n╠ 自動入群 : 關"
								if settings["autoJoin"] == True: ret_ += "\n╠ 自動加入票卷 : 開"
								else: ret_ += "\n╠ 自動加入票卷 : 關"
								if settings["autoRead"] == True: ret_ += "\n╠ 自動已讀 : 開"
								else: ret_ += "\n╠ 自動已讀 : 關"
								if settings["autoRespon"] == True: ret_ += "\n╠ 自動回覆 : 開"
								else: ret_ += "\n╠ 自動回覆 : 關"
								if settings["checkContact"] == True: ret_ += "\n╠ 查看友資 : 開"
								else: ret_ += "\n╠ 檢查友資 : 關"
								if settings["checkPost"] == True: ret_ += "\n╠ 查看貼文 : 開"
								else: ret_ += "\n╠ 查看貼文 : 關"
								if settings["checkSticker"] == True: ret_ += "\n╠ 查看貼圖 : 開"
								else: ret_ += "\n╠ 檢查貼圖 : 關"
								if settings["detectUnsend"] == True: ret_ += "\n╠ 查看收回 : 開"
								else: ret_ += "\n╠ 查看收回 : 關"
								if settings["setKey"] == True: ret_ += "\n╠ Set Key : 開"
								else: ret_ += "\n╠ Set Key : 關"
								ret_ +="\n╠ 自動添加消息 : {}".format(settings["AutoAddMessage"])
								ret_ +="\n╠ 自動加入消息 : {}".format(settings["AutoJoinMessage"])
								ret_ +="\n╠ 自動回覆消息 : {}".format(settings["AutoResponMessage"])
								ret_ += "\n╚══[ Status ]"
								client.sendMessage(to, str(ret_))
							except Exception as error:
								logError(error)
						elif cmd == "自動添加 開":
							if settings["autoAdd"] == True:
								client.sendMessage(to, "自動添加已開啟")
							else:
								settings["autoAdd"] = True
								client.sendMessage(to, "成功開啟自動添加")
						elif cmd == "自動添加 關":
							if settings["autoAdd"] == False:
								client.sendMessage(to, "自動添加已關閉")
							else:
								settings["autoAdd"] = False
								client.sendMessage(to, "成功關閉自動添加")
						elif cmd == "自動入群 開":
							if settings["autoJoin"] == True:
								client.sendMessage(to, "自動入群已開啟")
							else:
								settings["autoJoin"] = True
								client.sendMessage(to, "成功開啟自動入群")
						elif cmd == "自動入群 關":
							if settings["autoJoin"] == False:
								client.sendMessage(to, "自動入群已關閉")
							else:
								settings["autoJoin"] = False
								client.sendMessage(to, "成功關閉自動入群")
						elif cmd == "自動加入票卷　關":
							if settings["autoJoinTicket"] == True:
								client.sendMessage(to, "自動加入票卷已開啟")
							else:
								settings["autoJoinTicket"] = True
								client.sendMessage(to, "成功開啟自動加入票卷")
						elif cmd == "自動加入票卷 關":
							if settings["autoJoinTicket"] == False:
								client.sendMessage(to, "自動加入票卷已關閉")
							else:
								settings["autoJoinTicket"] = False
								client.sendMessage(to, "成功關閉自動加入票卷")
						elif cmd == "自動已讀 開":
							if settings["autoRead"] == True:
								client.sendMessage(to, "自動已讀已開啟")
							else:
								settings["autoRead"] = True
								client.sendMessage(to, "成功開啟自動已讀")
						elif cmd == "自動已讀 關":
							if settings["autoRead"] == False:
								client.sendMessage(to, "自動已讀已被關閉")
							else:
								settings["autoRead"] = False
								client.sendMessage(to, "成功關閉自動已讀")
						elif cmd == "自動回覆 開":
							if settings["autoRespon"] == True:
								client.sendMessage(to, "自動回覆已開啟")
							else:
								settings["autoRespon"] = True
								client.sendMessage(to, "成功開啟自動回覆")
						elif cmd == "自動回覆 關":
							if settings["autoRespon"] == False:
								client.sendMessage(to, "自動回覆已關閉")
							else:
								settings["autoRespon"] = False
								client.sendMessage(to, "成功關閉自動回覆")
						elif cmd == "查看友資 開":
							if settings["checkContact"] == True:
								client.sendMessage(to, "查看友資已開啟")
							else:
								settings["checkContact"] = True
								client.sendMessage(to, "成功開啟查看友資")
						elif cmd == "查看友資 關":
							if settings["checkContact"] == False:
								client.sendMessage(to, "查看友資已關閉")
							else:
								settings["checkContact"] = False
								client.sendMessage(to, "成功關閉查看友資")
						elif cmd == "查看貼文 開":
							if settings["checkPost"] == True:
								client.sendMessage(to, "查看貼文已開啟")
							else:
								settings["checkPost"] = True
								client.sendMessage(to, "成功開啟查看貼文")
						elif cmd == "查看貼文 關":
							if settings["checkPost"] == False:
								client.sendMessage(to, "查看貼文已關閉")
							else:
								settings["checkPost"] = False
								client.sendMessage(to, "成功關閉查看貼文")
						elif cmd == "查看貼圖 開":
							if settings["checkSticker"] == True:
								client.sendMessage(to, "查看貼圖已開啟")
							else:
								settings["checkSticker"] = True
								client.sendMessage(to, "成功開啟查看貼圖")
						elif cmd == "查看貼圖 關":
							if settings["checkSticker"] == False:
								client.sendMessage(to, "查看貼圖已關閉")
							else:
								settings["checkSticker"] = False
								client.sendMessage(to, "成功關閉查看貼圖")
						elif cmd == "查看收回 開":
							if settings["detectUnsend"] == True:
								client.sendMessage(to, "查看收回已開啟")
							else:
								settings["detectUnsend"] = True
								client.sendMessage(to, "成功開啟查看回收")
						elif cmd == "查看收回 關":
							if settings["detectUnsend"] == False:
								client.sendMessage(to, "查看收回已關閉")
							else:
								settings["detectUnsend"] = False
								client.sendMessage(to, "成功關閉查看收回")
						elif cmd.startswith("自動添加消息: "):
							sep = text.split(" ")
							txt = text.replace(sep[0] + " ","")
							try:
								settings["AutoAddMessage"] = txt
								client.sendMessage(to, "成功將自動添加消息更改為 : 「{}」".format(txt))
							except:
								client.sendMessage(to, "無法更改自動添加消息")
						elif cmd.startswith("自動回覆消息: "):
							sep = text.split(" ")
							txt = text.replace(sep[0] + " ","")
							try:
								settings["AutoResponMessage"] = txt
								client.sendMessage(to, "成功將自動回覆消息更改為 : 「{}」".format(txt))
							except:
								client.sendMessage(to, "無法更改自動回覆消息")
						elif cmd.startswith("自動加入消息: "):
							sep = text.split(" ")
							txt = text.replace(sep[0] + " ","")
							try:
								settings["AutoJoinMessage"] = txt
								client.sendMessage(to, "成功將自動入群消息更改為 : 「{}」".format(txt))
							except:
								client.sendMessage(to, "無法更改自動入群消息")


						elif cmd.startswith("更改名稱: "):
							sep = text.split(" ")
							name = text.replace(sep[0] + " ","")
							if len(name) <= 20:
								profile = client.getProfile()
								profile.displayName = name
								client.updateProfile(profile)
								client.sendMessage(to, "成功將名稱更改為 : {}".format(name))
						elif cmd.startswith("更改個簽: "):
							sep = text.split(" ")
							bio = text.replace(sep[0] + " ","")
							if len(bio) <= 500:
								profile = client.getProfile()
								profile.displayName = bio
								client.updateProfile(profile)
								client.sendMessage(to, "成功改變個簽 : {}".format(bio))
						elif cmd == "me":
							client.sendMention(to, "@!", [sender])
							client.sendContact(to, sender)
						elif cmd == "我的個人資料":
							contact = client.getContact(sender)
							cover = client.getProfileCoverURL(sender)
							result = "╔══[ 資料詳情 ]"
							result += "\n╠ 名稱 : @!"
							result += "\n╠ Mid : {}".format(contact.mid)
							result += "\n╠ 個簽 : {}".format(contact.statusMessage)
							result += "\n╠ 頭貼 : http://dl.profile.line-cdn.net/{}".format(contact.pictureStatus)
							result += "\n╠ 封面 : {}".format(str(cover))
							result += "\n╚══[ 結束 ]"
							client.sendImageWithURL(to, "http://dl.profile.line-cdn.net/{}".format(contact.pictureStatus))
							client.sendMention(to, result, [sender])
						elif cmd == "我的mid":
							contact = client.getContact(sender)
							client.sendMention(to, "@!: {}".format(contact.mid), [sender])
						elif cmd == "我的名稱":
							contact = client.getContact(sender)
							client.sendMention(to, "@!: {}".format(contact.displayName), [sender])
						elif cmd == "我的個簽":
							contact = client.getContact(sender)
							client.sendMention(to, "@!: {}".format(contact.statusMessage), [sender])
						elif cmd == "我的頭貼":
							contact = client.getContact(sender)
							client.sendImageWithURL(to, "http://dl.profile.line-cdn.net/{}".format(contact.pictureStatus))
						elif cmd == "我的影片":
							contact = client.getContact(sender)
							if contact.videoProfile == None:
								return client.sendMessage(to, "沒有個人影片")
							client.sendVideoWithURL(to, "http://dl.profile.line-cdn.net/{}/vp".format(contact.pictureStatus))
						elif cmd == "我的封面":
							cover = client.getProfileCoverURL(sender)
							client.sendImageWithURL(to, str(cover))
						elif cmd.startswith("Mid "):
							if 'MENTION' in msg.contentMetadata.keys()!= None:
								names = re.findall(r'@(\w+)', text)
								mention = ast.literal_eval(msg.contentMetadata['MENTION'])
								mentionees = mention['MENTIONEES']
								lists = []
								for mention in mentionees:
									if mention["M"] not in lists:
										lists.append(mention["M"])
								for ls in lists:
									client.sendMention(to, "@!: {}".format(ls), [ls])
						elif cmd.startswith("名稱 "):
							if 'MENTION' in msg.contentMetadata.keys()!= None:
								names = re.findall(r'@(\w+)', text)
								mention = ast.literal_eval(msg.contentMetadata['MENTION'])
								mentionees = mention['MENTIONEES']
								lists = []
								for mention in mentionees:
									if mention["M"] not in lists:
										lists.append(mention["M"])
								for ls in lists:
									contact = client.getContact(ls)
									client.sendMention(to, "@!: {}".format(contact.displayName), [ls])
						elif cmd.startswith("個簽 "):
							if 'MENTION' in msg.contentMetadata.keys()!= None:
								names = re.findall(r'@(\w+)', text)
								mention = ast.literal_eval(msg.contentMetadata['MENTION'])
								mentionees = mention['MENTIONEES']
								lists = []
								for mention in mentionees:
									if mention["M"] not in lists:
										lists.append(mention["M"])
								for ls in lists:
									contact = client.getContact(ls)
									client.sendMention(to, "@!: {}".format(contact.statusMessage), [ls])
						elif cmd.startswith("頭貼 "):
							if 'MENTION' in msg.contentMetadata.keys()!= None:
								names = re.findall(r'@(\w+)', text)
								mention = ast.literal_eval(msg.contentMetadata['MENTION'])
								mentionees = mention['MENTIONEES']
								lists = []
								for mention in mentionees:
									if mention["M"] not in lists:
										lists.append(mention["M"])
								for ls in lists:
									contact = client.getContact(ls)
									client.sendImageWithURL(to, "http://dl.profile.line-cdn.net/{}".format(contact.pictureStatus))
						elif cmd.startswith("個人影片 "):
							if 'MENTION' in msg.contentMetadata.keys()!= None:
								names = re.findall(r'@(\w+)', text)
								mention = ast.literal_eval(msg.contentMetadata['MENTION'])
								mentionees = mention['MENTIONEES']
								lists = []
								for mention in mentionees:
									if mention["M"] not in lists:
										lists.append(mention["M"])
								for ls in lists:
									contact = client.getContact(ls)
									if contact.videoProfile == None:
										return client.sendMention(to, "@!沒有個人影片", [ls])
									client.sendVideoWithURL(to, "http://dl.profile.line-cdn.net/{}/vp".format(contact.pictureStatus))
						elif cmd.startswith("封面 "):
							if 'MENTION' in msg.contentMetadata.keys()!= None:
								names = re.findall(r'@(\w+)', text)
								mention = ast.literal_eval(msg.contentMetadata['MENTION'])
								mentionees = mention['MENTIONEES']
								lists = []
								for mention in mentionees:
									if mention["M"] not in lists:
										lists.append(mention["M"])
								for ls in lists:
									cover = client.getProfileCoverURL(ls)
									client.sendImageWithURL(to, str(cover))
						elif cmd.startswith("複製個人資料 "):
							if 'MENTION' in msg.contentMetadata.keys()!= None:
								names = re.findall(r'@(\w+)', text)
								mention = ast.literal_eval(msg.contentMetadata['MENTION'])
								mentionees = mention['MENTIONEES']
								lists = []
								for mention in mentionees:
									if mention["M"] not in lists:
										lists.append(mention["M"])
								for ls in lists:
									client.cloneContactProfile(ls)
									client.sendContact(to, sender)
									client.sendMessage(to, "複製個人資料已成功")
						elif cmd == "恢復個人資料":
							try:
								clientProfile = client.getProfile()
								clientProfile.displayName = str(settings["myProfile"]["displayName"])
								clientProfile.statusMessage = str(settings["myProfile"]["statusMessage"])
								clientPictureStatus = client.downloadFileURL("http://dl.profile.line-cdn.net/{}".format(str(settings["myProfile"]["pictureStatus"])), saveAs="LineAPI/tmp/backupPicture.bin")
								coverId = str(settings["myProfile"]["coverId"])
								client.updateProfile(clientProfile)
								client.updateProfileCoverById(coverId)
								client.updateProfilePicture(clientPictureStatus)
								client.sendMessage(to, "Berhasil restore profile")
								client.sendContact(to, sender)
								client.deleteFile(clientPictureStatus)
							except Exception as error:
								logError(error)
								client.sendMessage(to, "恢復配置文件失敗")
						elif cmd == "備份個人資料":
							try:
								clientProfile = client.getProfile()
								settings["myProfile"]["displayName"] = str(clientProfile.displayName)
								settings["myProfile"]["statusMessage"] = str(clientProfile.statusMessage)
								settings["myProfile"]["pictureStatus"] = str(clientProfile.pictureStatus)
								coverId = client.getProfileDetail()["result"]["objectId"]
								settings["myProfile"]["coverId"] = str(coverId)
								client.sendMessage(to, "成功的配置備份")
							except Exception as error:
								logError(error)
								client.sendMessage(to, "配置文件備份失敗")
						elif cmd == "朋友列表":
							contacts = client.getAllContactIds()
							num = 0
							result = "╔══[ 朋友列表 ]"
							for listContact in contacts:
								contact = client.getContact(listContact)
								num += 1
								result += "\n╠ {}. {}".format(num, contact.displayName)
							result += "\n╚══[ 全部 {} 個好友 ]".format(len(contacts))
							client.sendMessage(to, result)
						elif cmd.startswith("朋友資料 "):
							sep = text.split(" ")
							query = text.replace(sep[0] + " ","")
							contacts = client.getAllContactIds()
							try:
								listContact = contacts[int(query)-1]
								contact = client.getContact(listContact)
								cover = client.getProfileCoverURL(listContact)
								result = "╔══[ 資料詳情 ]"
								result += "\n╠ 名稱 : @!"
								result += "\n╠ Mid : {}".format(contact.mid)
								result += "\n╠ 個簽 : {}".format(contact.statusMessage)
								result += "\n╠ 頭貼 : http://dl.profile.line-cdn.net/{}".format(contact.pictureStatus)
								result += "\n╠ 封面 : {}".format(str(cover))
								result += "\n╚══[ 結束 ]"
								client.sendImageWithURL(to, "http://dl.profile.line-cdn.net/{}".format(contact.pictureStatus))
								client.sendMention(to, result, [contact.mid])
							except Exception as error:
								logError(error)
						elif cmd == "封鎖名單":
							blockeds = client.getBlockedContactIds()
							num = 0
							result = "╔══[ 封鎖名單 ]"
							for listBlocked in blockeds:
								contact = client.getContact(listBlocked)
								num += 1
								result += "\n╠ {}. {}".format(num, contact.displayName)
							result += "\n╚══[ 一共 {} 個人 ]".format(len(blockeds))
							client.sendMessage(to, result)
						elif cmd.startswith("朋友廣播: "):
							sep = text.split(" ")
							txt = text.replace(sep[0] + " ","")
							contacts = client.getAllContactIds()
							for contact in contacts:
								client.sendMessage(contact, "[ 廣播 ]\n{}".format(str(txt)))
							client.sendMessage(to, "成功轉播到 {} 個朋友".format(str(len(contacts))))


						elif cmd.startswith("更改群組名: "):
							if msg.toType == 2:
								sep = text.split(" ")
								groupname = text.replace(sep[0] + " ","")
								if len(groupname) <= 20:
									group = client.getGroup(to)
									group.name = groupname
									client.updateGroup(group)
									client.sendMessage(to, "成功將組名更改為 : {}".format(groupname))
						elif cmd == "開啟網址":
							if msg.toType == 2:
								group = client.getGroup(to)
								group.preventedJoinByTicket = False
								client.updateGroup(group)
								groupUrl = client.reissueGroupTicket(to)
								client.sendMessage(to, "成功開啟群組QR\n\nGroupURL : line://ti/g/{}".format(groupUrl))
						elif cmd == "關閉網址":
							if msg.toType == 2:
								group = client.getGroup(to)
								group.preventedJoinByTicket = True
								client.updateGroup(group)
								client.sendMessage(to, "成功關閉群組QR")
						elif cmd == "群組圖片":
							if msg.toType == 2:
								group = client.getGroup(to)
								groupPicture = "http://dl.profile.line-cdn.net/{}".format(group.pictureStatus)
								client.sendImageWithURL(to, groupPicture)
						elif cmd == "群組名稱":
							if msg.toType == 2:
								group = client.getGroup(to)
								client.sendMessage(to, "群組名稱 : {}".format(group.name))
						elif cmd == "群組ID":
							if msg.toType == 2:
								group = client.getGroup(to)
								client.sendMessage(to, "群組ID : {}".format(group.id))
						elif cmd == "群組列表":
							groups = client.getGroupIdsJoined()
							ret_ = "╔══[ 群組列表 ]"
							no = 0
							for gid in groups:
								group = client.getGroup(gid)
								no += 1
								ret_ += "\n╠ {}. {} | {}".format(str(no), str(group.name), str(len(group.members)))
							ret_ += "\n╚══[ 一共 {} 個群組 ]".format(str(len(groups)))
							client.sendMessage(to, str(ret_))
						elif cmd == "成員名單":
							if msg.toType == 2:
								group = client.getGroup(to)
								num = 0
								ret_ = "╔══[ 成員名單 ]"
								for contact in group.members:
									num += 1
									ret_ += "\n╠ {}. {}".format(num, contact.displayName)
								ret_ += "\n╚══[ 一共 {} 個成員]".format(len(group.members))
								client.sendMessage(to, ret_)
						elif cmd == "待定名單":
							if msg.toType == 2:
								group = client.getGroup(to)
								ret_ = "╔══[ 待定名單 ]"
								no = 0
								if group.invitee is None or group.invitee == []:
									return client.sendMessage(to, "沒有冷卻")
								else:
									for pending in group.invitee:
										no += 1
										ret_ += "\n╠ {}. {}".format(str(no), str(pending.displayName))
									ret_ += "\n╚══[ 一共 {} 個人]".format(str(len(group.invitee)))
									client.sendMessage(to, str(ret_))
						elif cmd == "群組資訊":
							group = client.getGroup(to)
							try:
								try:
									groupCreator = group.creator.mid
								except:
									groupCreator = "找不到"
								if group.invitee is None:
									groupPending = "0"
								else:
									groupPending = str(len(group.invitee))
								if group.preventedJoinByTicket == True:
									groupQr = "關閉"
									groupTicket = "沒有"
								else:
									groupQr = "Terbuka"
									groupTicket = "https://line.me/R/ti/g/{}".format(str(client.reissueGroupTicket(group.id)))
								ret_ = "╔══[ 群組資訊 ]"
								ret_ += "\n╠ 名稱 : {}".format(group.name)
								ret_ += "\n╠ 群組ID : {}".format(group.id)
								ret_ += "\n╠ 創造者 : @!"
								ret_ += "\n╠ 成員數量 : {}".format(str(len(group.members)))
								ret_ += "\n╠ 待定人數 : {}".format(groupPending)
								ret_ += "\n╠ 群組QR : {}".format(groupQr)
								ret_ += "\n╠ 群組票卷 : {}".format(groupTicket)
								ret_ += "\n╚══[ 結束 ]"
								client.sendImageWithURL(to, "http://dl.profile.line-cdn.net/{}".format(group.pictureStatus))
								client.sendMention(to, str(ret_), [groupCreator])
							except:
								ret_ = "╔══[ 群組資訊 ]"
								ret_ += "\n╠ 名稱 : {}".format(group.name)
								ret_ += "\n╠ 群組ID : {}".format(group.id)
								ret_ += "\n╠ 創造者 : {}".format(groupCreator)
								ret_ += "\n╠ 成員數量 : {}".format(str(len(group.members)))
								ret_ += "\n╠ 待定人數 : {}".format(groupPending)
								ret_ += "\n╠ 群組QR : {}".format(groupQr)
								ret_ += "\n╠ 群組票卷t : {}".format(groupTicket)
								ret_ += "\n╚══[ 結束 ]"
								client.sendImageWithURL(to, "http://dl.profile.line-cdn.net/{}".format(group.pictureStatus))
								client.sendMessage(to, str(ret_))
						elif cmd.startswith("群組廣播: "):
							sep = text.split(" ")
							txt = text.replace(sep[0] + " ","")
							groups = client.getGroupIdsJoined()
							for group in groups:
								client.sendMessage(group, "[ 廣播 ]\n{}".format(str(txt)))
							client.sendMessage(to, "成功轉播到 {} 個群組".format(str(len(groups))))


						elif cmd == '標記成員':
							group = client.getGroup(to)
							midMembers = [contact.mid for contact in group.members]
							midSelect = len(midMembers)//100
							for mentionMembers in range(midSelect+1):
								no = 0
								ret_ = "╔══[ 標記成員 ]"
								dataMid = []
								for dataMention in group.members[mentionMembers*100 : (mentionMembers+1)*100]:
									dataMid.append(dataMention.mid)
									no += 1
									ret_ += "\n╠ {}. @!".format(str(no))
								ret_ += "\n╚══[ 一共 {} 個成員]".format(str(len(dataMid)))
								client.sendMention(to, ret_, dataMid)
						elif cmd == "已讀點 開":
							tz = pytz.timezone("Asia/Makassar")
							timeNow = datetime.now(tz=tz)
							day = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday","Friday", "Saturday"]
							hari = ["Minggu", "Senin", "Selasa", "Rabu", "Kamis", "Jumat", "Sabtu"]
							bulan = ["Januari", "Februari", "Maret", "April", "Mei", "Juni", "Juli", "Agustus", "September", "Oktober", "November", "Desember"]
							hr = timeNow.strftime("%A")
							bln = timeNow.strftime("%m")
							for i in range(len(day)):
								if hr == day[i]: hasil = hari[i]
							for k in range(0, len(bulan)):
								if bln == str(k): bln = bulan[k-1]
							readTime = hasil + ", " + timeNow.strftime('%d') + " - " + bln + " - " + timeNow.strftime('%Y') + "\nJam : [ " + timeNow.strftime('%H:%M:%S') + " ]"
							if to in read['readPoint']:
								try:
									del read['readPoint'][to]
									del read['readMember'][to]
								except:
									pass
								read['readPoint'][to] = msg_id
								read['readMember'][to] = []
								client.sendMessage(to, "設置點已開啟")
							else:
								try:
									del read['readPoint'][to]
									del read['readMember'][to]
								except:
									pass
								read['readPoint'][to] = msg_id
								read['readMember'][to] = []
								client.sendMessage(to, "設置已讀點 : \n{}".format(readTime))
						elif cmd == "已讀點 關":
							tz = pytz.timezone("Asia/Makassar")
							timeNow = datetime.now(tz=tz)
							day = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday","Friday", "Saturday"]
							hari = ["Minggu", "Senin", "Selasa", "Rabu", "Kamis", "Jumat", "Sabtu"]
							bulan = ["Januari", "Februari", "Maret", "April", "Mei", "Juni", "Juli", "Agustus", "September", "Oktober", "November", "Desember"]
							hr = timeNow.strftime("%A")
							bln = timeNow.strftime("%m")
							for i in range(len(day)):
								if hr == day[i]: hasil = hari[i]
							for k in range(0, len(bulan)):
								if bln == str(k): bln = bulan[k-1]
							readTime = hasil + ", " + timeNow.strftime('%d') + " - " + bln + " - " + timeNow.strftime('%Y') + "\nJam : [ " + timeNow.strftime('%H:%M:%S') + " ]"
							if to not in read['readPoint']:
								client.sendMessage(to,"已讀點已關閉")
							else:
								try:
									del read['readPoint'][to]
									del read['readMember'][to]
								except:
									pass
								client.sendMessage(to, "刪除已讀點 : \n{}".format(readTime))
						elif cmd == "查看已讀":
							if to in read['readPoint']:
								if read["readMember"][to] == []:
									return client.sendMessage(to, "沒有已讀者")
								else:
									no = 0
									result = "╔══[ 已讀者 ]"
									for dataRead in read["readMember"][to]:
										no += 1
										result += "\n╠ {}. @!".format(str(no))
									result += "\n╚══[ 一共 {} 個已讀 ]".format(str(len(read["readMember"][to])))
									client.sendMention(to, result, read["readMember"][to])
									read['readMember'][to] = []
						elif cmd == "更改頭貼":
							settings["changePictureProfile"] = True
							client.sendMessage(to, "請發送圖片")
						elif cmd == "更改組圖片":
							if msg.toType == 2:
								if to not in settings["changeGroupPicture"]:
									settings["changeGroupPicture"].append(to)
								client.sendMessage(to, "請發送圖片")
						elif cmd == "模仿 開":
							if settings["mimic"]["status"] == True:
								client.sendMessage(to, "模仿已開啟")
							else:
								settings["mimic"]["status"] = True
								client.sendMessage(to, "成功開啟模仿")
						elif cmd == "模仿 關":
							if settings["mimic"]["status"] == False:
								client.sendMessage(to, "模仿已被禁用")
							else:
								settings["mimic"]["status"] = False
								client.sendMessage(to, "成功關閉模仿")
						elif cmd == "模仿列表":
							if settings["mimic"]["target"] == {}:
								client.sendMessage(to, "沒有目標")
							else:
								no = 0
								result = "╔══[ 模仿列表 ]"
								target = []
								for mid in settings["mimic"]["target"]:
									target.append(mid)
									no += 1
									result += "\n╠ {}. @!".format(no)
								result += "\n╚══[ 一共 {} 個人 ]".format(str(len(target)))
								client.sendMention(to, result, target)
						elif cmd.startswith("模仿添加 "):
							if 'MENTION' in msg.contentMetadata.keys()!= None:
								names = re.findall(r'@(\w+)', text)
								mention = ast.literal_eval(msg.contentMetadata['MENTION'])
								mentionees = mention['MENTIONEES']
								lists = []
								for mention in mentionees:
									if mention["M"] not in lists:
										lists.append(mention["M"])
								for ls in lists:
									try:
										if ls in settings["mimic"]["target"]:
											client.sendMessage(to, "目標已在列表中")
										else:
											settings["mimic"]["target"][ls] = True
											client.sendMessage(to, "成功添加目標")
									except:
										client.sendMessage(to, "無法添加目標")
						elif cmd.startswith("模仿刪除 "):
							if 'MENTION' in msg.contentMetadata.keys()!= None:
								names = re.findall(r'@(\w+)', text)
								mention = ast.literal_eval(msg.contentMetadata['MENTION'])
								mentionees = mention['MENTIONEES']
								lists = []
								for mention in mentionees:
									if mention["M"] not in lists:
										lists.append(mention["M"])
								for ls in lists:
									try:
										if ls not in settings["mimic"]["target"]:
											client.sendMessage(to, "目標不在列表中")
										else:
											del settings["mimic"]["target"][ls]
											client.sendMessage(to, "成功刪除目標")
									except:
										client.sendMessage(to, "無法刪除目標")


						elif cmd.startswith("IG資訊"):
							sep = text.split(" ")
							txt = text.replace(sep[0] + " ","")
							url = requests.get("http://corrykalam.pw/api/instagram.php?username={}".format(search))
							data = url.json()
							icon = "https://upload.wikimedia.org/wikipedia/commons/thumb/a/a5/Instagram_icon.png/599px-Instagram_icon.png"
							name = "Instagram"
							link = "https://www.instagram.com/{}".format(data["result"]["username"])
							result = "╔══[ Instagram 訊息 ]"
							result += "\n╠ 名稱 : {}".format(data["result"]["name"])
							result += "\n╠ 使用者名稱: {}".format(data["result"]["username"])
							result += "\n╠ 個簽 : {}".format(data["result"]["bio"])
							result += "\n╠ 追蹤者 : {}".format(data["result"]["follower"])
							result += "\n╠ 追蹤中 : {}".format(data["result"]["following"])
							result += "\n╠ 私人 : {}".format(data["result"]["private"])
							result += "\n╠ 貼文 : {}".format(data["result"]["mediacount"])
							result += "\n╚══[ 結束 ]"
							client.sendImageWithURL(to, data["result"]["url"])
							client.sendFooter(to, result, icon, name, link)
						elif cmd.startswith("instastory "):
							sep = text.split(" ")
							query = text.replace(sep[0] + " ","")
							cond = query.split("|")
							search = str(cond[0])
							if len(cond) == 2:
								url = requests.get("http://rahandiapi.herokuapp.com/instastory/{}?key=betakey".format(search))
								data = url.json()
								num = int(cond[1])
								if num <= len(data["url"]):
									search = data["url"][num - 1]
									if search["tipe"] == 1:
										client.sendImageWithURL(to, str(search["link"]))
									elif search["tipe"] == 2:
										client.sendVideoWithURL(to, str(search["link"]))
						elif cmd == "quotes":
							url = requests.get("https://botfamily.faith/api/quotes/?apikey=beta")
							data = url.json()
							result = "╔══[ Quotes ]"
							result += "\n╠ 作者 : {}".format(data["result"]["author"])
							result += "\n╠ 類別 : {}".format(data["result"]["category"])
							result += "\n╠ 引用 : {}".format(data["result"]["quote"])
							result += "\n╚══[ 結束 ]"
							client.sendMessage(to, result)
						elif cmd.startswith("say-"):
							sep = text.split("-")
							sep = sep[1].split(" ")
							lang = sep[0]
							if settings["setKey"] == False:
								txt = text.lower().replace("say-" + lang + " ","")
							else:
								txt = text.lower().replace(settings["keyCommand"] + "say-" + lang + " ","")
							if lang not in language["gtts"]:
								return client.sendMessage(to, "語言 {} 沒找到".format(lang))
							tts = gTTS(text=txt, lang=lang)
							tts.save("line/tmp/tts-{}.mp3".format(lang))
							client.sendAudio(to, "line/tmp/tts-{}.mp3".format(lang))
							client.deleteFile("line/tmp/tts-{}.mp3".format(lang))
						elif cmd.startswith("從YouTube搜尋 "):
							sep = text.split(" ")
							txt = msg.text.replace(sep[0] + " ","")
							cond = txt.split("|")
							search = cond[0]
							url = requests.get("http://api.w3hills.com/youtube/search?keyword={}&api_key=86A7FCF3-6CAF-DEB9-E214-B74BDB835B5B".format(search))
							data = url.json()
							if len(cond) == 1:
								no = 0
								result = "╔══[ Youtube ]"
								for anu in data["videos"]:
									no += 1
									result += "\n╠ {}. {}".format(str(no),str(anu["title"]))
								result += "\n╚══[ 一共 {} 個結果 ]".format(str(len(data["videos"])))
								client.sendMessage(to, result)
							elif len(cond) == 2:
								num = int(str(cond[1]))
								if num <= len(data):
									search = data["videos"][num - 1]
									ret_ = "╔══[ Youtube 資訊 ]"
									ret_ += "\n╠ 頻道 : {}".format(str(search["publish"]["owner"]))
									ret_ += "\n╠ 標題 : {}".format(str(search["title"]))
									ret_ += "\n╠ 發布 : {}".format(str(search["publish"]["date"]))
									ret_ += "\n╠ 觀眾 : {}".format(str(search["stats"]["views"]))
									ret_ += "\n╠ 喜歡 : {}".format(str(search["stats"]["likes"]))
									ret_ += "\n╠ 不喜歡 : {}".format(str(search["stats"]["dislikes"]))
									ret_ += "\n╠ 等級 : {}".format(str(search["stats"]["rating"]))
									ret_ += "\n╠ 描述 : {}".format(str(search["description"]))
									ret_ += "\n╚══[ {} ]".format(str(search["webpage"]))
									client.sendImageWithURL(to, str(search["thumbnail"]))
									client.sendMessage(to, str(ret_))
						elif cmd.startswith("searchimage "):
							sep = text.split(" ")
							txt = text.replace(sep[0] + " ","")
							url = requests.get("http://rahandiapi.herokuapp.com/imageapi?key=betakey&q={}".format(txt))
							data = url.json()
							client.sendImageWithURL(to, random.choice(data["result"]))
						elif cmd.startswith("搜尋音樂 "):
							sep = text.split(" ")
							query = text.replace(sep[0] + " ","")
							cond = query.split("|")
							search = str(cond[0])
							url = requests.get("http://api.ntcorp.us/joox/search?q={}".format(str(search)))
							data = url.json()
							if len(cond) == 1:
								num = 0
								ret_ = "╔══[ 音樂結果 ]"
								for music in data["result"]:
									num += 1
									ret_ += "\n╠ {}. {}".format(str(num), str(music["single"]))
								ret_ += "\n╚══[ 一共 {} 個音樂 ]".format(str(len(data["result"])))
								ret_ += "\n\nUntuk mengirim music, silahkan gunakan command {}SearchMusic {}|「number」".format(str(setKey), str(search))
								client.sendMessage(to, str(ret_))
							elif len(cond) == 2:
								num = int(cond[1])
								if num <= len(data["result"]):
									music = data["result"][num - 1]
									url = requests.get("http://api.ntcorp.us/joox/song_info?sid={}".format(str(music["sid"])))
									data = url.json()
									ret_ = "╔══[ 音樂 ]"
									ret_ += "\n╠ 標題 : {}".format(str(data["result"]["song"]))
									ret_ += "\n╠ 專輯 : {}".format(str(data["result"]["album"]))
									ret_ += "\n╠ Size : {}".format(str(data["result"]["size"]))
									ret_ += "\n╠ 鏈接 : {}".format(str(data["result"]["mp3"][0]))
									ret_ += "\n╚══[ 結束 ]"
									client.sendImageWithURL(to, str(data["result"]["img"]))
									client.sendMessage(to, str(ret_))
									client.sendAudioWithURL(to, str(data["result"]["mp3"][0]))
						elif cmd.startswith("searchlyric "):
							sep = text.split(" ")
							txt = text.replace(sep[0] + " ","")
							cond = txt.split("|")
							query = cond[0]
							with requests.session() as web:
								web.headers["user-agent"] = "Mozilla/5.0"
								url = web.get("https://www.musixmatch.com/search/{}".format(urllib.parse.quote(query)))
								data = BeautifulSoup(url.content, "html.parser")
								result = []
								for trackList in data.findAll("ul", {"class":"tracks list"}):
									for urlList in trackList.findAll("a"):
										title = urlList.text
										url = urlList["href"]
										result.append({"title": title, "url": url})
								if len(cond) == 1:
									ret_ = "╔══[ Musixmatch 結果 ]"
									num = 0
									for title in result:
										num += 1
										ret_ += "\n╠ {}. {}".format(str(num), str(title["title"]))
									ret_ += "\n╚══[ 一共 {} 個結果 ]".format(str(len(result)))
									ret_ += "\n\nUntuk melihat lyric, silahkan gunakan command {}SearchLyric {}|「number」".format(str(setKey), str(query))
									client.sendMessage(to, ret_)
								elif len(cond) == 2:
									num = int(cond[1])
									if num <= len(result):
										data = result[num - 1]
										with requests.session() as web:
											web.headers["user-agent"] = "Mozilla/5.0"
											url = web.get("https://www.musixmatch.com{}".format(urllib.parse.quote(data["url"])))
											data = BeautifulSoup(url.content, "html5lib")
											for lyricContent in data.findAll("p", {"class":"mxm-lyrics__content "}):
												lyric = lyricContent.text
												client.sendMessage(to, lyric)
						elif cmd.startswith("tr-"):
							sep = text.split("-")
							sep = sep[1].split(" ")
							lang = sep[0]
							if settings["setKey"] == False:
								txt = text.lower().replace("tr-" + lang + " ","")
							else:
								txt = text.lower().replace(settings["keyCommand"] + "tr-" + lang + " ","")
							if lang not in language["googletrans"]:
								return client.sendMessage(to, "Bahasa {} tidak ditemukan".format(lang))
							translator = Translator()
							result = translator.translate(txt, dest=lang)
							client.sendMessage(to, result.text)
						if text.lower() == "mykey":
							client.sendMessage(to, "Keycommand已設置 : 「{}」".format(str(settings["keyCommand"])))
						elif text.lower() == "setkey on":
							if settings["setKey"] == True:
								client.sendMessage(to, "Setkey已設置")
							else:
								settings["setKey"] = True
								client.sendMessage(to, "成功設置Setkey")
						elif text.lower() == "setkey off":
							if settings["setKey"] == False:
								client.sendMessage(to, "Setkey已被關閉")
							else:
								settings["setKey"] = False
								client.sendMessage(to, "成功關閉setkey")
						if text is None: return
						if "/ti/g/" in msg.text.lower():
							if settings["autoJoinTicket"] == True:
								link_re = re.compile('(?:line\:\/|line\.me\/R)\/ti\/g\/([a-zA-Z0-9_-]+)?')
								links = link_re.findall(text)
								n_links = []
								for l in links:
									if l not in n_links:
										n_links.append(l)
								for ticket_id in n_links:
									group = client.findGroupByTicket(ticket_id)
									client.acceptGroupInvitationByTicket(group.id,ticket_id)
									client.sendMessage(to, "成功進入群組 %s" % str(group.name))
					elif msg.contentType == 1:
						if settings["changePictureProfile"] == True:
							path = client.downloadObjectMsg(msg_id, saveAs="LineAPI/tmp/{}-cpp.bin".format(time.time()))
							settings["changePictureProfile"] = False
							client.updateProfilePicture(path)
							client.sendMessage(to, "成功更改個人資料照片")
							client.deleteFile(path)
						if msg.toType == 2:
							if to in settings["changeGroupPicture"]:
								path = client.downloadObjectMsg(msg_id, saveAs="LineAPI/tmp/{}-cgp.bin".format(time.time()))
								settings["changeGroupPicture"].remove(to)
								client.updateGroupPicture(to, path)
								client.sendMessage(to, "成功更改群組照片")
								client.deleteFile(path)
					elif msg.contentType == 7:
						if settings["checkSticker"] == True:
							stk_id = msg.contentMetadata['STKID']
							stk_ver = msg.contentMetadata['STKVER']
							pkg_id = msg.contentMetadata['STKPKGID']
							ret_ = "╔══[ 貼圖訊息 ]"
							ret_ += "\n╠ 貼圖ID : {}".format(stk_id)
							ret_ += "\n╠ 包裝貼圖ID : {}".format(pkg_id)
							ret_ += "\n╠ 貼圖版本 : {}".format(stk_ver)
							ret_ += "\n╠ 貼圖URL : line://shop/detail/{}".format(pkg_id)
							ret_ += "\n╚══[ 結束 ]"
							client.sendMessage(to, str(ret_))
					elif msg.contentType == 13:
						if settings["checkContact"] == True:
							try:
								contact = client.getContact(msg.contentMetadata["mid"])
								cover = client.getProfileCoverURL(msg.contentMetadata["mid"])
								ret_ = "╔══[ 友資 ]"
								ret_ += "\n╠ 名稱 : {}".format(str(contact.displayName))
								ret_ += "\n╠ MID : {}".format(str(msg.contentMetadata["mid"]))
								ret_ += "\n╠ 個簽 : {}".format(str(contact.statusMessage))
								ret_ += "\n╠ 頭貼 : http://dl.profile.line-cdn.net/{}".format(str(contact.pictureStatus))
								ret_ += "\n╠ 封面 : {}".format(str(cover))
								ret_ += "\n╚══[ 結束 ]"
								client.sendImageWithURL(to, "http://dl.profile.line-cdn.net/{}".format(str(contact.pictureStatus)))
								client.sendMessage(to, str(ret_))
							except:
								client.sendMessage(to, "友資無效")
					elif msg.contentType == 16:
						if settings["checkPost"] == True:
							try:
								ret_ = "╔══[ 貼文資訊 ]"
								if msg.contentMetadata["serviceType"] == "GB":
									contact = client.getContact(sender)
									auth = "\n╠ 作者 : {}".format(str(contact.displayName))
								else:
									auth = "\n╠ 作者 : {}".format(str(msg.contentMetadata["serviceName"]))
								purl = "\n╠ URL : {}".format(str(msg.contentMetadata["postEndUrl"]).replace("line://","https://line.me/R/"))
								ret_ += auth
								ret_ += purl
								if "mediaOid" in msg.contentMetadata:
									object_ = msg.contentMetadata["mediaOid"].replace("svc=myhome|sid=h|","")
									if msg.contentMetadata["mediaType"] == "V":
										if msg.contentMetadata["serviceType"] == "GB":
											ourl = "\n╠ 對象 URL : https://obs-us.line-apps.com/myhome/h/download.nhn?tid=612w&{}".format(str(msg.contentMetadata["mediaOid"]))
											murl = "\n╠ 媒體 URL : https://obs-us.line-apps.com/myhome/h/download.nhn?{}".format(str(msg.contentMetadata["mediaOid"]))
										else:
											ourl = "\n╠ 對象 URL : https://obs-us.line-apps.com/myhome/h/download.nhn?tid=612w&{}".format(str(object_))
											murl = "\n╠ 媒體 URL : https://obs-us.line-apps.com/myhome/h/download.nhn?{}".format(str(object_))
										ret_ += murl
									else:
										if msg.contentMetadata["serviceType"] == "GB":
											ourl = "\n╠ 對象 URL : https://obs-us.line-apps.com/myhome/h/download.nhn?tid=612w&{}".format(str(msg.contentMetadata["mediaOid"]))
										else:
											ourl = "\n╠ 對象 URL : https://obs-us.line-apps.com/myhome/h/download.nhn?tid=612w&{}".format(str(object_))
									ret_ += ourl
								if "stickerId" in msg.contentMetadata:
									stck = "\n╠ Stiker : https://line.me/R/shop/detail/{}".format(str(msg.contentMetadata["packageId"]))
									ret_ += stck
								if "text" in msg.contentMetadata:
									text = "\n╠ Tulisan : {}".format(str(msg.contentMetadata["text"]))
									ret_ += text
								ret_ += "\n╚══[ Finish ]"
								client.sendMessage(to, str(ret_))
							except:
								client.sendMessage(to, "貼文無效")
			except Exception as error:
				logError(error)


		if op.type == 26:
			try:
				print("[ 26 ] 收到消息")
				msg = op.message
				text = str(msg.text)
				msg_id = msg.id
				receiver = msg.to
				sender = msg._from
				if msg.toType == 0 or msg.toType == 1 or msg.toType == 2:
					if msg.toType == 0:
						if sender != client.profile.mid:
							to = sender
						else:
							to = receiver
					elif msg.toType == 1:
						to = receiver
					elif msg.toType == 2:
						to = receiver
					if sender in settings["mimic"]["target"] and settings["mimic"]["status"] == True and settings["mimic"]["target"][sender] == True:
						if msg.contentType == 0:
							client.sendMessage(to, text)
						elif msg.contentType == 1:
							path = client.downloadObjectMsg(msg_id, saveAs="LineAPI/tmp/{}-mimic.bin".format(time.time()))
							client.sendImage(to, path)
							client.deleteFile(path)
					if msg.contentType == 0:
						if settings["autoRead"] == True:
							client.sendChatChecked(to, msg_id)
						if sender not in clientMid:
							if msg.toType != 0 and msg.toType == 2:
								if 'MENTION' in msg.contentMetadata.keys()!= None:
									names = re.findall(r'@(\w+)', text)
									mention = ast.literal_eval(msg.contentMetadata['MENTION'])
									mentionees = mention['MENTIONEES']
									for mention in mentionees:
										if clientMid in mention["M"]:
											if settings["autoRespon"] == True:
												client.sendMention(sender, settings["autoResponMessage"], [sender])
											break
						if text is None: return
						if "/ti/g/" in msg.text.lower():
							if settings["autoJoinTicket"] == True:
								link_re = re.compile('(?:line\:\/|line\.me\/R)\/ti\/g\/([a-zA-Z0-9_-]+)?')
								links = link_re.findall(text)
								n_links = []
								for l in links:
									if l not in n_links:
										n_links.append(l)
								for ticket_id in n_links:
									group = client.findGroupByTicket(ticket_id)
									client.acceptGroupInvitationByTicket(group.id,ticket_id)
									client.sendMessage(to, "成功進入該組 %s" % str(group.name))
						if settings["detectUnsend"] == True:
							try:
								unsendTime = time.time()
								unsend[msg_id] = {"text": text, "from": sender, "time": unsendTime}
							except Exception as error:
								logError(error)
					if msg.contentType == 1:
						if settings["detectUnsend"] == True:
							try:
								unsendTime = time.time()
								image = client.downloadObjectMsg(msg_id, saveAs="LineAPI/tmp/{}-image.bin".format(time.time()))
								unsend[msg_id] = {"from": sender, "image": image, "time": unsendTime}
							except Exception as error:
								logError(error)
			except Exception as error:
				logError(error)


		if op.type == 55:
			print ("[ 55 ] 通知已讀消息")
			if op.param1 in read["readPoint"]:
				if op.param2 not in read["readMember"][op.param1]:
					read["readMember"][op.param1].append(op.param2)


		if op.type == 65:
			try:
				if settings["detectUnsend"] == True:
					to = op.param1
					sender = op.param2
					if sender in unsend:
						unsendTime = time.time()
						contact = client.getContact(unsend[sender]["from"])
						if "text" in unsend[sender]:
							try:
								sendTime = unsendTime - unsend[sender]["time"]
								sendTime = timeChange(sendTime)
								ret_ = "╔══[ 收回訊息 ]"
								ret_ += "\n╠ 收回者 : @!"
								ret_ += "\n╠ 時間 : {} 前".format(sendTime)
								ret_ += "\n╠ 類型 : 文本"
								ret_ += "\n╠ 內容 : {}".format(unsend[sender]["text"])
								ret_ += "\n╚══[ 結束 ]"
								client.sendMention(to, ret_, [contact.mid])
								del unsend[sender]
							except:
								del unsend[sender]
						elif "image" in unsend[sender]:
							try:
								sendTime = unsendTime - unsend[sender]["time"]
								sendTime = timeChange(sendTime)
								ret_ = "╔══[ 收回訊息 ]"
								ret_ += "\n╠ 收回者 : @!"
								ret_ += "\n╠ 時間 : {} 前".format(sendTime)
								ret_ += "\n╠ 類型 : 圖片"
								ret_ += "\n╠ 文本 : 無"
								ret_ += "\n╚══[ 結束 ]"
								client.sendMention(to, ret_, [contact.mid])
								client.sendImage(to, unsend[sender]["image"])
								client.deleteFile(unsend[sender]["image"])
								del unsend[sender]
							except:
								client.deleteFile(unsend[sender]["image"])
								del unsend[sender]
					else:
						client.sendMessage(to, "未找到未發現的數據")
			except Exception as error:
				logError(error)
		backupData()
	except Exception as error:
		logError(error)

def run():
	while True:
		ops = clientPoll.singleTrace(count=50)
		if ops != None:
			for op in ops:
				try:
					clientBot(op)
				except Exception as error:
					logError(error)
				clientPoll.setRevision(op.revision)

if __name__ == "__main__":
	run()
