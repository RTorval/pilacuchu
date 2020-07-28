import traceback

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

print("INTRODUCCIÓN DE DATOS SENSIBLES\n")
llave=""
llaveee=""
while True:
	llave=str(input("Contraseña: "))
	llaveee=str(input("Confirmar contraseña: "))
	if llave!=llaveee:
		print("No coinciden")
	elif any(k not in [j for j in (chr(i) for i in range(32,127))] for k in llave):
		print("Contiene caracteres \"indeseados\"")
	else:
		break

f=open("bla.enc","w")
for i in ["token","admintoken","adminchat_id","sender","password"]:
	value=vign(txt=str(input("Introducir %s: "%i)),key=llave,typ="e")
	f.write(value+"\n")
f.write(vign(txt="¡Correcto!",key=llave,typ="e")+"\n")
f.close()
