import requests
import time
import smtplib
import ssl
import traceback
import random
from ast import literal_eval
from PIL import Image,ImageFilter
import umb_es as lang
import sys
#hashlib.md5("".join([bd[elotro][i] for i in bd[elotro]]).encode()).hexdigest()

def vign(txt,key,typ):
	universe=[c for c in (chr(i) for i in range(32,255))]
	if not txt:
		print("needs txt")
		return
	if not key:
		print("needs key")
		return
	if typ not in ("d","e"):
		print("typ must be \"e\" or \"d\"")
		return
	if any(t not in universe for t in key):
		print("invalid characters in the key\nmust only use ASCII symbols")
		return
	ret_txt=""
	k_len=len(key)
	for i, l in enumerate(txt):
		if l not in universe:
			ret_txt+=l
		else:
			txt_idx=universe.index(l)
			k=key[i%k_len]
			key_idx=universe.index(k)
			if typ=="d":
				key_idx*=-1
			code=universe[(txt_idx+key_idx)%len(universe)]
			ret_txt+=code
	return ret_txt

def fancysquared(pil_img):
	width,height=pil_img.size
	if width==height:
		return pil_img
	elif width>height:
		result=pil_img.resize((width,width)).filter(ImageFilter.GaussianBlur(100))
		result.paste(pil_img,(0,(width-height)//2))
		return result
	else:
		result=pil_img.resize((height,height)).filter(ImageFilter.GaussianBlur(100))
		result.paste(pil_img,((height-width)//2,0))
		return result

def coder():
	x="".join([random.choice("qwertyuiopasdfghjklzxcvbnmQWERTYUIOPASDFGHJKLZXCVBNM1234567890") for i in range(8)])
	print(x)
	return x

def email(correo,message,sender,password):
	port=465
	receiver=correo
	context=ssl.create_default_context()
	try:
		with smtplib.SMTP_SSL("smtp.gmail.com",port,context=context) as server:
			server.login(sender,password)
			server.sendmail(sender,receiver,message)
	except Exception:
		print("EMAIL ERROR")
		traceback.print_exc()

def deletemsg(chat_id,msg_id):
	try:
		x=requests.get(r'https://api.telegram.org/bot%s/deleteMessage?chat_id=%s&message_id=%s'%(token,chat_id,msg_id))
		return x.json()
	except Exception:
		print("DELETEMSG ERROR")
		traceback.print_exc()

def sendmsg(token,text,chat_id,mas=""):
	try:
		x=requests.get(r'https://api.telegram.org/bot%s/sendMessage?chat_id=%s&text=%s%s'%(token,chat_id,text,mas))
		return str(x.json()["result"]["message_id"])
	except Exception:
		print("BOTTEXT ERROR")
		traceback.print_exc()

def sendphoto(file_id,caption,chat_id,mas=""):
	try:
		x=requests.get(r'https://api.telegram.org/bot%s/sendPhoto?chat_id=%s&photo=%s&caption=%s%s'%(token,chat_id,file_id,caption,mas))
		return str(x.json()["result"]["message_id"])
	except Exception:
		print("SENDPHOTO ERROR")
		traceback.print_exc()

def editphoto(chat_id,msg_id,fileid,mas=""):
	try:
		x=requests.get(r'https://api.telegram.org/bot%s/editMessageMedia?chat_id=%s&message_id=%s&media={"type":"photo","media":"%s"}%s'%(token,chat_id,msg_id,fileid,mas))
		return x.json()
	except Exception:
		print("EDITPHOTO ERROR")
		traceback.print_exc()

def editmsgtxt(chat_id,msg_id,txt):
	try:
		x=requests.get(r'https://api.telegram.org/bot%s/editMessageText?chat_id=%s&message_id=%s&text=%s'%(token,chat_id,msg_id,txt))
		return x.json()
	except Exception:
		print("EDITMSGTXT ERROR")
		traceback.print_exc()

def editmsgcap(chat_id,msg_id,caption,mas=""):
	try:
		x=requests.get(r'https://api.telegram.org/bot%s/editMessageCaption?chat_id=%s&message_id=%s&caption=%s%s'%(token,chat_id,msg_id,caption,mas))
		return x.json()
	except Exception:
		print("EDITMSGCAP ERROR")
		traceback.print_exc()

def vaciar(chat_id,msg_id):
	editphoto(chat_id,msg_id,"AgACAgQAAxkBAAKgdF6PPdTMhxKllkw_coGIUCbfjB3GAAKWsTEbalgYULk0S5odYdGVo2jXIl0AAwEAAwIAA20AA-I7AAIYBA")
	editmsgcap(chat_id,msg_id,"***")

def usercap(bd,user_id):
	return "%s - %s\n%s: %s\n\n%s\n\n%s: %s\n%s: %s"%(bd[user_id]["alias"],bd[user_id]["edad"],lang.situ,bd[user_id]["situ"],bd[user_id]["bio"],lang.prefe,bd[user_id]["prefe"],lang.inte,bd[user_id]["inte"])

def rpmkup(user_id):
	return r'&reply_markup={"inline_keyboard":[[{"text":"👍","callback_data":"like_%s"},{"text":"❔","callback_data":"duda_%s"},{"text":"👎","callback_data":"dislike_%s"},{"text":"❌","callback_data":"denun_%s"}]]}'%(user_id,user_id,user_id,user_id)

def menurpmkup(activ,polimatch):	#menurpmkup(bd[user_id]["activ"],bd[user_id]["polimatch"])
	if activ=="no" or activ=="casi":
		return r'&reply_markup={"inline_keyboard":[[{"text":"%s","callback_data":"editperfil"}],[{"text":"%s (%s)","callback_data":"polimatch"}],[{"text":"%s","callback_data":"salirmenu"}]]}'%(lang.editperf,lang.polimenu,polimatch.upper(),lang.fin)
	elif activ=="si":
		return r'&reply_markup={"inline_keyboard":[[{"text":"%s","callback_data":"editperfil"}],[{"text":"%s","callback_data":"desactivar"}],[{"text":"%s (%s)","callback_data":"polimatch"}],[{"text":"%s","callback_data":"salirmenu"}]]}'%(lang.editperf,lang.desactivar,lang.polimenu,polimatch.upper(),lang.fin)
	elif activ=="confirmarrr":
		return r'&reply_markup={"inline_keyboard":[[{"text":"%s","callback_data":"editperfil"}],[{"text":"%s","callback_data":"sidesactivar"}],[{"text":"%s (%s)","callback_data":"polimatch"}],[{"text":"%s","callback_data":"salirmenu"}]]}'%(lang.editperf,lang.dudas,lang.polimenu,polimatch.upper(),lang.fin)
	else:
		return None
	
def perfilshow(bd,user_id,chat_id):
	return sendphoto(bd[user_id]["foto"],usercap(bd,user_id),chat_id,rpmkup(user_id))

def perfilupdt(bd,chat_id,msg_id,user_id):
	editphoto(chat_id,msg_id,bd[user_id]["foto"])
	editmsgcap(chat_id,msg_id,usercap(bd,user_id),rpmkup(user_id))

def sendmercredi(bd,user_id):
	xfoto="AgACAgQAAxkBAAKgdF6PPdTMhxKllkw_coGIUCbfjB3GAAKWsTEbalgYULk0S5odYdGVo2jXIl0AAwEAAwIAA20AA-I7AAIYBA"
	if bd[user_id]["activ"]=="si":
		return sendphoto(xfoto,lang.mercredi,user_id,r'&reply_markup={"inline_keyboard":[[{"text":"Seguir jugando","callback_data":"seguir"}],[{"text":"Reset total","callback_data":"resetear"}]]}')
	elif bd[user_id]["activ"]=="no":
		return sendphoto(xfoto,lang.mercredi,user_id,r'&reply_markup={"inline_keyboard":[[{"text":"%s","callback_data":"resetear"}]]}'%lang.activar)
	elif bd[user_id]["activ"]=="cad":
		return	sendmsg(token,lang.pcad,user_id,r'&reply_markup={"inline_keyboard":[[{"text":"ACTIVAR perfil","callback_data":"resetear"}]]}')

def mercrediupdt(bd,user_id,msg_id):
	xfoto="AgACAgQAAxkBAAKgdF6PPdTMhxKllkw_coGIUCbfjB3GAAKWsTEbalgYULk0S5odYdGVo2jXIl0AAwEAAwIAA20AA-I7AAIYBA"
	if bd[user_id]["activ"]=="si":
		editphoto(user_id,msg_id,xfoto)
		editmsgcap(user_id,msg_id,lang.mercredi,r'&reply_markup={"inline_keyboard":[[{"text":"Seguir jugando","callback_data":"seguir"}],[{"text":"Reset total","callback_data":"resetear"}]]}')
	elif bd[user_id]["activ"]=="no":
		editphoto(user_id,msg_id,xfoto)
		editmsgcap(user_id,msg_id,lang.mercredi,r'&reply_markup={"inline_keyboard":[[{"text":"ACTIVAR perfil","callback_data":"resetear"}]]}')
	elif bd[user_id]["activ"]=="casi":
		editphoto(user_id,msg_id,bd[user_id]["foto"])
		editmsgcap(user_id,msg_id,usercap(bd,user_id),r'&reply_markup={"inline_keyboard":[[{"text":"👍","callback_data":"resetear"},{"text":"👍","callback_data":"resetear"},{"text":"👍","callback_data":"resetear"},{"text":"👍","callback_data":"resetear"}]]}')
	elif bd[user_id]["activ"]=="cad":
		editphoto(user_id,msg_id,xfoto)
		editmsgcap(user_id,msg_id,lang.pcad,r'&reply_markup={"inline_keyboard":[[{"text":"%s","callback_data":"resetear"}]]}'%lang.activar)

def nextvictim(bd,bdm,user_id,msg_id):
	lll=[i for i in bd if i!=user_id and bd[i]['activ']=='si' and not (i in bdm[user_id] and bdm[user_id][i][1]=="".join([bd[i][j] for j in bd[i]][2:-1]))]
	if len(lll)>0:
		perfilupdt(bd,user_id,msg_id,random.choice(lll))
	else:
		endphoto="AgACAgQAAxkBAAKcLF5c-LPQbYdCueaJ6lRyIpJ7yxTnAAI5szEbgE7pUudDEPvctjK1FR6qGwAEAQADAgADeAADw0sIAAEYBA"
		editphoto(user_id,msg_id,endphoto)
		editmsgcap(user_id,msg_id,lang.jolin)
		editmsgcap(user_id,msg_id,"\n".join([lang.jolin,lang.nohay]),r'&reply_markup={"inline_keyboard":[[{"text":"%s","callback_data":"continuar"}]]}'%lang.continuar)

def pillar(bd,user_id,adminchat_id):
	fpath=requests.get(r'https://api.telegram.org/bot%s/getFile?file_id=%s'%(token,bd[user_id]["foto"])).json()["result"]["file_path"]
	RRR=requests.get(r'https://api.telegram.org/file/bot%s/%s'%(token,fpath))
	fname="photou.%s"%fpath.split(".")[-1]
	open(fname,'wb').write(RRR.content)
	enlace=r'https://api.telegram.org/bot%s/sendPhoto?chat_id=%s&caption=%s'%(admintoken,adminchat_id,usercap(bd,user_id))
	subir={"photo":open(fname,"rb")}
	requests.post(enlace,files=subir)

def fotoguay(foto_id,chat_id):
	try:
		fpath=requests.get(r'https://api.telegram.org/bot%s/getFile?file_id=%s'%(token,foto_id)).json()["result"]["file_path"]
		RRR=requests.get(r'https://api.telegram.org/file/bot%s/%s'%(token,fpath))
		fname="photou.%s"%fpath.split(".")[-1]
		open(fname,'wb').write(RRR.content)
		img_perf=fancysquared(Image.open(fname))
		nfname="perfil_%s"%fname
		img_perf.save(nfname,quality=95)
		enlace=r'https://api.telegram.org/bot%s/sendPhoto?chat_id=%s'%(token,chat_id)
		subir={"photo":open(nfname,"rb")}
		x=requests.post(enlace,files=subir)
		return x.json()["result"]
	except Exception:
		print("FOTOGUAY ERROR")
		traceback.print_exc()

###################################################################################################
def updatebd(bdfn,bd,head):
	f=open(bdfn,"w")
	for i in head:
		f.write(i+"\t")
	f.write("\n")
	for i in bd:
		f.write(str(i)+"\t")
		for j in bd[i]:
			f.write(str(bd[i][j])+"\t")
		f.write("\n")
	f.close()

#user_id	num	correo	nick	foto	alias	situ	edad	bio	prefe	inte	activ	polimatch	
bdfn="bd.tsv"
bd={}
try:	#importar base de datos tsv
	f=open(bdfn,"r")
	bdhead=f.readline().split("\t")[:-1]	#el final de linea es "\t\n"
	lines=[i.split("\t")[:-1] for i in f.readlines()]
	f.close()
	for i in lines:
		if len(i)==len(bdhead):
			bd[i[0]]={}
			for n,j in enumerate(i[1:]):
				bd[i[0]][bdhead[n+1]]=j
except:
	print("ALGO PASA CON LA BD")
#print(bd)

#user_id	estado	correo	codigo	cad	mercredi	lastmsgid	lasttime	
bdsfn="bds.tsv"
bds={}
try:	#importar base de datos tsv
	f=open(bdsfn,"r")
	bdshead=f.readline().split("\t")[:-1]	#el final de línea es "\t\n"
	liness=[i.split("\t")[:-1] for i in f.readlines()]
	f.close()
	for i in liness:
		if len(i)==len(bdshead):
			bds[i[0]]={}
			for n,j in enumerate(i[1:]):
				bds[i[0]][bdshead[n+1]]=j
except:
	print("ALGO PASA CON LA BDS")
#print(bds)

try:
	f=open("bdm.dict","r")
	bdm=literal_eval(f.readline())
	f.close()
except:
	print("ALGO PASA CON LA BDM")
#print(bdm)
###################################################################################################

offsetfn="eloffset.dat"

try:
	f=open(offsetfn,"r")
	offset=int(f.readline())
	f.close()
except:
	offset=1
offset_old=offset-1
###################################################################################################
while True:
	llave=sys.argv[1]#str(input("Contraseña: "))
	try:	#importar datos sensibles
		f=open("bla.enc","r")
		lenc=[i[:-1] for i in f.readlines()]
		f.close()
		token=vign(txt=lenc[0],key=llave,typ="d")
		admintoken=vign(txt=lenc[1],key=llave,typ="d")
		adminchat_id=vign(txt=lenc[2],key=llave,typ="d")
		sender=vign(txt=lenc[3],key=llave,typ="d")
		password=vign(txt=lenc[4],key=llave,typ="d")
		print(vign(txt=lenc[5],key=llave,typ="d"))
		break
	except Exception:
		print("ERROR EN bla.enc\nVuelva a generar el fichero con vigenere.py\n")
		traceback.print_exc()
		exit()
###################################################################################################
dominio="xxxyyy.zzz"
minscad=5	#mins caducidad código verificación
#estds={"alias":"Alias","foto":"Foto","situ":"Situación universitaria","edad":"Edad","bio":"Sobre ti","prefe":"Preferencias","inte":"Intenciones"}
estds=lang.estados
rrr=""
for ii in estds:
	rrr+='[{"text":"%s","callback_data":"edit_%s"}],'%(estds[ii],ii)
qqq=r'&reply_markup={"inline_keyboard":[%s,[{"text":"%s","callback_data":"finmenu"}]]}'%(rrr[:-1],lang.fin)
###################################################################################################
while True:
	user_id=""
	try:
		#ABOUT TIME
		for i in bd:
			if bds[i]["lasttime"]!="" and int(time.time())-int(bds[i]["lasttime"])>3600*24*28:	#perfil caduca tras 28 días de inactividad
				bds[i]["estado"]="fin"
				bd[i]["activ"]="cad"
				bds[i]["mercredi"]="X"	#es miércoles
				vaciar(i,bds[i]["lastmsgid"])
				bds[i]["lastmsgid"]=sendmercredi(bd,i)
			#if time.localtime()[6]==2:	#los miércoles
			if (int(time.time())-int(time.time())%60)%180==0:	#cada 3 mins con precisión de un minuto
				if bds[i]["mercredi"]=="W":
					bds[i]["mercredi"]="X"	#es miércoles
					if bds[i]["estado"]=="fin":
						vaciar(i,bds[i]["lastmsgid"])
						bds[i]["lastmsgid"]=sendmercredi(bd,i)
			else:
				if bds[i]["mercredi"]!="X":
					bds[i]["mercredi"]="W"	#esperar al miércoles
		updatebd(bdsfn,bds,bdshead)
		#GET DATA
		url=r'https://api.telegram.org/bot%s/getUpdates?offset=%s&timeout=10'%(token,offset)
		res=requests.get(url).json()
		#PROCESS DATA
		if "result" in res:
			for item in res["result"]:
				#print(item)
				for jj in bd:
					if not jj in bdm:
						bdm[jj]={}
				offset=item["update_id"]+1
				#GET USER ID
				if "message" in item:
					user_id=str(item["message"]["from"]["id"])
					if user_id in bds:
						bds[user_id]["lasttime"]=int(time.time())
					if user_id in bd and bd[user_id]["activ"]!="":
						if "username" in item["message"]["from"]:
							if bds[user_id]["estado"][:4]=="nick":
								bds[user_id]["estado"]=estado[4:]
							bd[user_id]["nick"]=item["message"]["from"]["username"]
						else:
							if bds[user_id]["estado"][:4]!="nick":
								antestd=bds[user_id]["estado"]
								bds[user_id]["estado"]="nick"+antestd
							sendmsg(token,lang.noname,user_id,r'&reply_markup={"inline_keyboard":[[{"text":"%s","callback_data":"nickready"}]]}'%lang.ready)
				elif "callback_query" in item:
					user_id=str(item["callback_query"]["from"]["id"])
					if user_id in bds:
						bds[user_id]["lasttime"]=int(time.time())
					if user_id in bd and bd[user_id]["activ"]!="":
						if "username" in item["callback_query"]["from"]:
							if bds[user_id]["estado"][:4]=="nick":
								bds[user_id]["estado"]=estado[4:]
							bd[user_id]["nick"]=item["callback_query"]["from"]["username"]
						else:
							if bds[user_id]["estado"][:4]!="nick":
								antestd=bds[user_id]["estado"]
								bds[user_id]["estado"]="nick"+antestd
							sendmsg(token,lang.noname,user_id,r'&reply_markup={"inline_keyboard":[[{"text":"%s","callback_data":"nickready"}]]}'%lang.ready)
				else:
					user_id=""
				#USER IN BDS
				if user_id in bds:
					estado=bds[user_id]["estado"]
				else:
					estado=""
					#WELCOME
					sendmsg(token,lang.bienvenida,user_id)
					sendmsg(token,lang.pidemail,user_id)
					bds[user_id]={}
					for ii in bdshead[1:]:
						bds[user_id][ii]=""
					bds[user_id]["estado"]="correo"
				#USER IN BD SENDS MESSAGE
				if user_id in bd and "message" in item:
					#PROFILE EDITTING STATES (MENU)
					if estado=="alias" and "text" in item["message"]:
						if len(item["message"]["text"])<16 and len(item["message"]["text"])>=3:
							bd[user_id]["alias"]=item["message"]["text"].replace("\n"," ")
							if bd[user_id]["activ"]!="":
								bds[user_id]["estado"]="menu"
								editmsgcap(user_id,bds[user_id]["lastmsgid"],usercap(bd,user_id),qqq)
							else:
								bds[user_id]["estado"]="foto"
								sendmsg(token,lang.pidefoto,user_id)
						else:
							if bd[user_id]["activ"]!="":
								editmsgcap(user_id,bds[user_id]["lastmsgid"],lang.editalias)
							else:
								sendmsg(token,lang.piiidealias,user_id)
					elif estado=="foto":
						if "photo" in item["message"]:
							zzz=sendmsg(token,lang.caca,user_id)
							xxx=fotoguay(item["message"]["photo"][-1]["file_id"],user_id)
							bd[user_id]["foto"]=xxx["photo"][-1]["file_id"]
							if bd[user_id]["activ"]!="":
								bds[user_id]["estado"]="menu"
								editphoto(user_id,bds[user_id]["lastmsgid"],bd[user_id]["foto"],qqq)
								editmsgcap(user_id,bds[user_id]["lastmsgid"],usercap(bd,user_id),qqq)
								deletemsg(user_id,str(xxx["message_id"]))
								deletemsg(user_id,zzz)
							else:
								bds[user_id]["estado"]="situ"
								sendmsg(token,lang.pidesitu,user_id)
						else:
							if bd[user_id]["activ"]!="":
								editmsgcap(user_id,bds[user_id]["lastmsgid"],"Envía una foto")
							else:
								sendmsg(token,lang.pidefoto,user_id)
					elif estado=="situ" and "text" in item["message"]:
						if len(item["message"]["text"])<=64 and len(item["message"]["text"])>=3:
							bd[user_id]["situ"]=item["message"]["text"].replace("\n"," ")
							if bd[user_id]["activ"]!="":
								bds[user_id]["estado"]="menu"
								editmsgcap(user_id,bds[user_id]["lastmsgid"],usercap(bd,user_id),qqq)
							else:
								bds[user_id]["estado"]="edad"
								sendmsg(token,lang.pideedad,user_id)
						else:
							if bd[user_id]["activ"]!="":
								editmsgcap(user_id,bds[user_id]["lastmsgid"],lang.editsitu)
							else:
								sendmsg(token,lang.piiidesitu,user_id)
					elif estado=="edad" and "text" in item["message"]:
						if item["message"]["text"] in [str(i) for i in range(18,201)]:
							bd[user_id]["edad"]=item["message"]["text"]
							if bd[user_id]["activ"]!="":
								bds[user_id]["estado"]="menu"
								editmsgcap(user_id,bds[user_id]["lastmsgid"],usercap(bd,user_id),qqq)
							else:
								bds[user_id]["estado"]="bio"
								sendmsg(token,lang.pidebio,user_id)
								
						else:
							if bd[user_id]["activ"]!="":
								editmsgcap(user_id,bds[user_id]["lastmsgid"],lang.editedad)
							else:
								sendmsg(token,lang.piiideedad,user_id)
					elif estado=="bio" and "text" in item["message"]:
						if len(item["message"]["text"])<=320 and len(item["message"]["text"])>=16:
							bd[user_id]["bio"]=item["message"]["text"].replace("\n"," ")
							if bd[user_id]["activ"]!="":
								bds[user_id]["estado"]="menu"
								editmsgcap(user_id,bds[user_id]["lastmsgid"],usercap(bd,user_id),qqq)
							else:
								bds[user_id]["estado"]="prefe"
								sendmsg(token,lang.pideprefe,user_id)
						else:
							if bd[user_id]["activ"]!="":
								editmsgcap(user_id,bds[user_id]["lastmsgid"],lang.editbio)
							else:
								sendmsg(token,"(%s caracteres)"%str(len(item["message"]["text"])),user_id)
								sendmsg(token,lang.piiidebio,user_id)
					elif estado=="prefe" and "text" in item["message"]:
						if len(item["message"]["text"])<=32 and len(item["message"]["text"])>=2:
							bd[user_id]["prefe"]=item["message"]["text"].replace("\n"," ")
							if bd[user_id]["activ"]!="":
								bds[user_id]["estado"]="menu"
								editmsgcap(user_id,bds[user_id]["lastmsgid"],usercap(bd,user_id),qqq)
							else:
								bds[user_id]["estado"]="inte"
								sendmsg(token,lang.pideinte,user_id)
						else:
							if bd[user_id]["activ"]!="":
								editmsgcap(user_id,bds[user_id]["lastmsgid"],lang.editprefe)
							else:
								sendmsg(token,lang.piiideprefe,user_id)
					elif estado=="inte" and "text" in item["message"]:
						if len(item["message"]["text"])<=64 and len(item["message"]["text"])>=0:
							bd[user_id]["inte"]=item["message"]["text"].replace("\n"," ")
							if bd[user_id]["activ"]!="":
								bds[user_id]["estado"]="menu"
								editmsgcap(user_id,bds[user_id]["lastmsgid"],usercap(bd,user_id),qqq)
							else:
								bds[user_id]["estado"]="fin"
								bd[user_id]["activ"]="casi"
								bds[user_id]["polimatch"]="off"
								bds[user_id]["mercredi"]="X"
								sendmsg(token,lang.empezar,user_id)
								sendmsg(token,lang.editarperfil,user_id)
								bds[user_id]["lastmsgid"]=sendphoto(bd[user_id]["foto"],usercap(bd,user_id),user_id,r'&reply_markup={"inline_keyboard":[[{"text":"👍","callback_data":"resetear"},{"text":"👍","callback_data":"resetear"},{"text":"👍","callback_data":"resetear"},{"text":"👍","callback_data":"resetear"}]]}')
						else:
							if bd[user_id]["activ"]!="":
								editmsgcap(user_id,bds[user_id]["lastmsgid"],lang.editinte)
							else:
								sendmsg(token,lang.piiideinte,user_id)
					#COMPLETE PROFILE
					elif bd[user_id]["activ"]!="" and "text" in item["message"]:
						if item["message"]["text"]=="/perfil":
							bds[user_id]["estado"]="menu"
							vaciar(user_id,bds[user_id]["lastmsgid"])
							bds[user_id]["lastmsgid"]=sendphoto(bd[user_id]["foto"],usercap(bd,user_id),user_id,menurpmkup(bd[user_id]["activ"],bd[user_id]["polimatch"]))
						elif item["message"]["text"]=="/help":
							bds[user_id]["estado"]="menu"
							vaciar(user_id,bds[user_id]["lastmsgid"])
							bds[user_id]["lastmsgid"]=sendmsg(token,lang.help,user_id,r'&reply_markup={"inline_keyboard":[[{"text":"%s","callback_data":"salirmenu"}]]}'%lang.fin)
					#CLEAN WHEN PLAYING
					if bd[user_id]["activ"]!="" and bd[user_id]["activ"]!="casi":
						deletemsg(user_id,str(item["message"]["message_id"]))
				#USER IN BD SENDS CALLBACK QUERY
				elif user_id in bd and "callback_query" in item:
					#AVOID OLD BUTTONS
					if str(item["callback_query"]["message"]["message_id"])!=bds[user_id]["lastmsgid"]:
						vaciar(user_id,str(item["callback_query"]["message"]["message_id"]))
					elif estado=="fin":
						if item["callback_query"]["data"]=="seguir" and bds[user_id]["mercredi"]=="X":
							todel=[]
							for ii in bdm[user_id]:
								if bdm[user_id][ii][0]=="duda":
									todel.append(ii)
							if len(todel)>0:
								for ii in todel:
									del bdm[user_id][ii]
							bds[user_id]["mercredi"]="D"	#durante el miércoles
							nextvictim(bd,bdm,user_id,str(item["callback_query"]["message"]["message_id"]))
						elif item["callback_query"]["data"]=="resetear" and bds[user_id]["mercredi"]=="X":
							bdm[user_id]={}
							bd[user_id]["activ"]="si"	#también activa el perfil
							bds[user_id]["mercredi"]="D"	#durante el miércoles
							nextvictim(bd,bdm,user_id,str(item["callback_query"]["message"]["message_id"]))
						#HASTA AQUÍ LO QUE SE PUEDE HACER CON PERFIL TANTO ACTIVO COMO INACTIVO
						elif bd[user_id]["activ"]=="si":
							if item["callback_query"]["data"].split("_")[0] in ["like","duda","dislike","denun"]:
								elotro=item["callback_query"]["data"].split("_")[1]
								bdm[user_id][elotro]=[item["callback_query"]["data"].split("_")[0],"".join([bd[elotro][j] for j in bd[elotro]][2:-1])]
								nextvictim(bd,bdm,user_id,str(item["callback_query"]["message"]["message_id"]))
								#MATCH
								if bdm[user_id][elotro][0]=="like" and user_id in bdm[elotro] and bdm[elotro][user_id][0]=="like":
									sendmsg(token,"%s\n@%s"%(lang.match,bd[elotro]["nick"]),user_id)
									sendmsg(token,"%s\n@%s"%(lang.match,bd[user_id]["nick"]),elotro)
								#DENUNCIA
								if item["callback_query"]["data"].split("_")[0]=="denun":
									uuu=item["callback_query"]["data"].split("_")[1]
									sendmsg(admintoken,"PERFIL DENUNCIADO:\n%s"%uuu,adminchat_id)
									pillar(bd,uuu,adminchat_id)
							elif item["callback_query"]["data"]=="continuar":
								nextvictim(bd,bdm,user_id,str(item["callback_query"]["message"]["message_id"]))
						else:
							vaciar(user_id,str(item["callback_query"]["message"]["message_id"]))
					elif estado=="menu":
						if item["callback_query"]["data"]=="editperfil":
							editmsgcap(user_id,str(item["callback_query"]["message"]["message_id"]),usercap(bd,user_id),qqq)
						elif item["callback_query"]["data"][:4]=="edit":
							if item["callback_query"]["data"][5:] in estds:
								bds[user_id]["estado"]=item["callback_query"]["data"][5:]	#str del tipo "editxxxxx"
								editmsgcap(user_id,str(item["callback_query"]["message"]["message_id"]),"%s %s:"%(lang.edit,estds[item["callback_query"]["data"][5:]]))
						elif item["callback_query"]["data"]=="finmenu":
							editmsgcap(user_id,str(item["callback_query"]["message"]["message_id"]),usercap(bd,user_id),menurpmkup(bd[user_id]["activ"],bd[user_id]["polimatch"]))
						elif item["callback_query"]["data"]=="salirmenu":
							bds[user_id]["estado"]="fin"
							if bds[user_id]["mercredi"]=="X":
								mercrediupdt(bd,user_id,str(item["callback_query"]["message"]["message_id"]))
							elif bd[user_id]["activ"]=="si":
								nextvictim(bd,bdm,user_id,str(item["callback_query"]["message"]["message_id"]))
						elif item["callback_query"]["data"]=="desactivar":
							editmsgcap(user_id,str(item["callback_query"]["message"]["message_id"]),lang.advertencia,menurpmkup("confirmarrr",bd[user_id]["polimatch"]))
						elif item["callback_query"]["data"]=="sidesactivar":
							bd[user_id]["activ"]="no"
							editmsgcap(user_id,str(item["callback_query"]["message"]["message_id"]),usercap(bd,user_id),menurpmkup(bd[user_id]["activ"],bd[user_id]["polimatch"]))
						elif item["callback_query"]["data"]=="polimatch":
							if bd[user_id]["polimatch"]=="on":
								bd[user_id]["polimatch"]="off"
							elif bd[user_id]["polimatch"]=="off":
								bd[user_id]["polimatch"]="on"
							else:
								bd[user_id]["polimatch"]="off"
							editmsgcap(user_id,str(item["callback_query"]["message"]["message_id"]),usercap(bd,user_id),menurpmkup(bd[user_id]["activ"],bd[user_id]["polimatch"]))
					else:
						vaciar(user_id,str(item["callback_query"]["message"]["message_id"]))
				#VERIFICAR PERFIL PARA METER EN BD###################################################################################################
				else:
					if estado=="correo" and "message" in item and "text" in item["message"]:	#no da error porque comprueba en orden, mola
						if item["message"]["text"].split("@")[-1]==dominio:
							if item["message"]["text"] in [bds[i]["correo"] for i in bd]:
								sendmsg(token,"La dirección de correo %s ya está en uso...\n¿Ahora qué?"%item["message"]["text"])
							else:
								bds[user_id]["correo"]=item["message"]["text"]
								bds[user_id]["codigo"]=coder()
								bds[user_id]["cad"]=str(time.time()+(60*minscad))
								email(bds[user_id]["correo"],bds[user_id]["codigo"],sender,password)
								sendmsg(token," ".join([lang.enviado,bds[user_id]["correo"]]),user_id,r'&reply_markup={"inline_keyboard":[[{"text":"%s","callback_data":"cambiamail"}]]}'%lang.editmail_button)
								sendmsg(token," ".join([lang.todobien,str(minscad),lang.minutos]),user_id)
								sendmsg(token,"Código recibido:",user_id)
								bds[user_id]["estado"]="codigo"
						else:
							sendmsg(token,"".join([lang.piiidemail," \"xxxxxxx@%s\""%dominio,user_id]))
					elif estado=="codigo" and "message" in item and "text" in item["message"]:
						if time.time()>float(bds[user_id]["cad"]):
							sendmsg(token,lang.caducado,user_id,r'&reply_markup={"inline_keyboard":[[{"text":"%s","callback_data":"reenv"}],[{"text":"%s","callback_data":"cambiamail"}]]}'%(lang.reenv,lang.editmail_button))
							bds[user_id]["estado"]="cad"
						else:
							if item["message"]["text"]==bds[user_id]["codigo"]:
								bds[user_id]["codigo"]=""
								bds[user_id]["cad"]=""
								bd[user_id]={}
								for ii in bdhead[1:]:
									bd[user_id][ii]=""
								if len(bd)>0:
									bd[user_id]["num"]=str(int(max([bd[ii]["num"] for ii in bd]))+1)
								else:
									bd[user_id]["num"]="1"
								bd[user_id]["correo"]=bds[user_id]["correo"]
								bds[user_id]["correo"]=""
								sendmsg(token,lang.dentro,user_id)
								bds[user_id]["estado"]="alias"
								sendmsg(token,lang.pidealias,user_id)
							else:
								sendmsg(token,lang.mal,user_id)
					elif estado=="cad" and "callback_query" in item:
						if item["callback_query"]["data"]=="reenv":
							bds[user_id]["codigo"]=coder()
							bds[user_id]["cad"]=str(time.time()+(60*minscad))
							email(bds[user_id]["correo"],bds[user_id]["codigo"],sender,password)
							vaciar(user_id,str(item["callback_query"]["message"]["message_id"]))
							sendmsg(token," ".join([lang.todobien,str(minscad),lang.minutos]),user_id)
							sendmsg(token,lang.pidecodigo,user_id)
							bds[user_id]["estado"]="codigo"
					elif (estado=="codigo" or estado=="cad") and "callback_query" in item and item["callback_query"]["data"]=="cambiamail":
						vaciar(user_id,str(item["callback_query"]["message"]["message_id"]))
						sendmsg(token,lang.editmail,user_id)
						bds[user_id]["estado"]="correo"
				###################################################################################################
				offset_old=offset
				ff=open(offsetfn,"w")
				ff.write(str(offset))
				ff.close()
				updatebd(bdsfn,bds,bdshead)
				updatebd(bdfn,bd,bdhead)
				f=open("bdm.dict","w")
				f.write(str(bdm))
				f.close()
	except Exception:
		print("MAIN LOOP ERROR")
		traceback.print_exc()

