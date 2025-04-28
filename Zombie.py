import pygame
import os
import math
import time
import random
import datetime

os.system("cls")
pygame.init()

MINIMAPPA_LARGHEZZA = 300
MINIMAPPA_ALTEZZA = 250
LARGHEZZASCHERMO = 1440
ALTEZZASCHERMO = 796
pygame.display.set_caption('ZOMBI KILLER')
schermo = pygame.display.set_mode((LARGHEZZASCHERMO, ALTEZZASCHERMO))


DizionarioMappe = {
    1: pygame.image.load("mappe/mappa1.png"),
    2: pygame.image.load("mappe/mappa2.png"),
    3: pygame.image.load("mappe/mappa3.png"),
    "m": pygame.image.load("mappe/aggiuntaMappa.png")
}
MiniMappe = {
    1: pygame.transform.scale(DizionarioMappe[1], (MINIMAPPA_LARGHEZZA, MINIMAPPA_ALTEZZA)),
    2: pygame.transform.scale(DizionarioMappe[2], (MINIMAPPA_LARGHEZZA, MINIMAPPA_ALTEZZA)),
    3: pygame.transform.scale(DizionarioMappe[3], (MINIMAPPA_LARGHEZZA, MINIMAPPA_ALTEZZA)),
    "m": pygame.transform.scale(DizionarioMappe["m"], (MINIMAPPA_LARGHEZZA, MINIMAPPA_ALTEZZA))
}
def CaricaImmagini():
    schermataTitolo = pygame.image.load("immagini/titolo.png")
    sfondoMappe = pygame.image.load("immagini/sfondoMappe.png")
    personaggio = pygame.image.load("immagini/personaggio.png")
    proiettile = pygame.transform.scale(pygame.image.load("immagini/weapon_gun.png"), (10, 10))
    zombie = pygame.image.load("immagini/zombie.png")
    sangue = pygame.image.load("immagini/sangue.png")
    sangue = pygame.transform.scale(sangue, (100, 100))
    cuore = pygame.transform.scale(pygame.image.load("immagini/cuore.png"), (70, 70))
    cuoreBonus = pygame.transform.scale(pygame.image.load("immagini/cuore.png"), (50, 50))
    fulmine = pygame.transform.scale(pygame.image.load("immagini/fulmine.png"), (50, 50))
    rifornimenti = pygame.transform.scale(pygame.image.load("immagini/risorse.png"), (40, 40))
    GameOver = pygame.transform.scale(pygame.image.load("immagini/GAMEOVER.png"), (700, 700))
    uno = pygame.transform.scale(pygame.image.load("immagini/uno.png"), (50, 50))
    due = pygame.transform.scale(pygame.image.load("immagini/due.png"), (50, 50))
    tre = pygame.transform.scale(pygame.image.load("immagini/tre.png"), (50, 50))
    quattro = pygame.transform.scale(pygame.image.load("immagini/quattro.png"), (50, 50))
    nuovaMappa = pygame.transform.scale(pygame.image.load("mappe/aggiuntaMappa.png"), (300, 250))
    boss = pygame.transform.scale(pygame.image.load("immagini/boss.png"), (100, 100))
    mirino = pygame.transform.scale(pygame.image.load("immagini\mirino.png"), (50, 50))
    SfondoMieMappe = pygame.image.load("immagini/sfondoMieMappe.png")
    bomba = pygame.transform.scale(pygame.image.load("immagini/bomba.png"), (50, 50))

    return schermataTitolo, sfondoMappe, personaggio, proiettile, zombie, sangue, cuore, fulmine, cuoreBonus, rifornimenti, GameOver, uno,due,tre,quattro, nuovaMappa, boss, mirino,SfondoMieMappe,bomba

def RuotaVersoMouse(immagine, x, y, mouseX, mouseY):
    dx = mouseX - x
    dy = mouseY - y
    angolo = -math.degrees(math.atan2(dy, dx))
    immagineRuotata = pygame.transform.rotate(immagine, angolo)
    rett = immagineRuotata.get_rect(center=(x + immagine.get_width()//2, y + immagine.get_height()//2))
    return immagineRuotata, rett

def RotazioneZombie(immagine, zx, zy, giocatoreX, giocatoreY):
    dx = giocatoreX - zx
    dy = giocatoreY - zy
    angolo = -math.degrees(math.atan2(dy, dx))
    immagineRuotata = pygame.transform.rotate(immagine, angolo)
    rett = immagineRuotata.get_rect(center=(zx, zy))
    return immagineRuotata, rett


def ScegliMappa(event,nuovoPercorso):
    if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_1:
            return DizionarioMappe[1],1
        elif event.key == pygame.K_2:
            return DizionarioMappe[2],2
        elif event.key == pygame.K_3:
            return DizionarioMappe[3],3
        elif event.key == pygame.K_4:
            return nuovoPercorso ,4, 
    return None, None

def GestisciSpazio(event, SpazioPremuto):
    if not SpazioPremuto and event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
        return True
    return SpazioPremuto

def GestisciMovimento(tasti, x, y, velocita):
    if tasti[pygame.K_a] and x > 0:
        x -= velocita
    if tasti[pygame.K_d] and x < LARGHEZZASCHERMO - 64:
        x += velocita
    if tasti[pygame.K_w] and y > 0:
        y -= velocita
    if tasti[pygame.K_s] and y < ALTEZZASCHERMO - 64:
        y += velocita
    return x, y

def SparaProiettile(x, y, mouseX, mouseY, listaProiettili):
    angoloRad = math.atan2(mouseY - (y+32), mouseX - (x+32))
    dx = math.cos(angoloRad)
    dy = math.sin(angoloRad)
    distanza = 32
    startX = x + 32 + dx * distanza
    startY = y + 32 + dy * distanza
    listaProiettili.append([startX, startY, dx, dy, -math.degrees(angoloRad)])

def GestisciProiettili(listaProiettili, velocitaProiettile):
    restanti = []
    for p in listaProiettili:
        p[0] += p[2] * velocitaProiettile
        p[1] += p[3] * velocitaProiettile
        if 0 <= p[0] <= LARGHEZZASCHERMO and 0 <= p[1] <= ALTEZZASCHERMO:
            restanti.append(p)
    listaProiettili[:] = restanti

def GestisciScritte(schermo, caricatore, ricarica, ultimaRicarica, scorte, ZombieUccisi, font):
    testoColpi = font.render(F"Colpi {caricatore}", True, (255,255,255))
    schermo.blit(testoColpi, (10,10))
    if caricatore == 0:
        testoColpi = font.render(F"Colpi {caricatore}", True, (255,0,0))
        schermo.blit(testoColpi, (10,10))
    if ricarica:
        tempo = max(0, 2 - int(time.time() - ultimaRicarica))
        testoRicarica = font.render(F"Ricarica {tempo}s", True, (255,0,0))
        schermo.blit(testoRicarica, (130,10))
        schermo.blit(testoRicarica, (130,10))
    TestoScorte = font.render(F"Scorte {scorte}", True, (255,255,255))
    TestoKill = font.render(F"Punteggio {ZombieUccisi}", True, (255,255,255))
    schermo.blit(TestoKill, (600, 10))
    schermo.blit(TestoScorte, (10, 50))

def SpawnZombie(partenzaSu, fineSu, partenzaGiu, fineGiu, partenzaSx, fineSx, partenzaDx, fineDX):
    lato = random.choice(["su","giu","sinistra","destra"])
    if lato == "su":
        return [random.randint(partenzaSu, fineSu), -50]
    if lato == "giu":
        return [random.randint(partenzaGiu, fineGiu), ALTEZZASCHERMO + 50]
    if lato == "sinistra":
        return [-50, random.randint(partenzaSx, fineSx)]
    if lato == "destra":
        return [LARGHEZZASCHERMO + 50, random.randint(partenzaDx, fineDX)]

def GestisciZombie(ListaZombie, giocatoreX, giocatoreY, velocitaZombie, zombie):
    centroX = giocatoreX + 32
    centroY = giocatoreY + 32
    distanzaMinima = 40
    distanzaMinima_sq = distanzaMinima * distanzaMinima

    for i, z in enumerate(ListaZombie):
        dxGiocatore = centroX - z[0]
        dyGiocatore = centroY - z[1]
        distanza_giocatore_quadrato = dxGiocatore**2 + dyGiocatore**2

        if distanza_giocatore_quadrato != 0:
            inv_distanza = 1 / (distanza_giocatore_quadrato**0.5)
            movimentoX = dxGiocatore * inv_distanza * velocitaZombie
            movimentoY = dyGiocatore * inv_distanza * velocitaZombie
        else:
            movimentoX, movimentoY = 0, 0

        for j, altro in enumerate(ListaZombie):
            if i != j:
                dx = z[0] - altro[0]
                dy = z[1] - altro[1]
                dist_sq = dx**2 + dy**2
                if 0 < dist_sq and dist_sq < distanzaMinima_sq:
                    inv_dist = 1 / (dist_sq**0.5)
                    forza_repulsiva = (distanzaMinima_sq - dist_sq) / distanzaMinima_sq
                    movimentoX += dx * inv_dist * forza_repulsiva * velocitaZombie
                    movimentoY += dy * inv_dist * forza_repulsiva * velocitaZombie

        z[0] += movimentoX
        z[1] += movimentoY

        zImg, zRect = RotazioneZombie(zombie, z[0], z[1], giocatoreX, giocatoreY)
        schermo.blit(zImg, zRect.topleft)


def CollisioniZombie(ListaZombie, listaProiettili, ZombieUccisi):
    daRimuovereZ = []
    daRimuovereP = []

    for z in ListaZombie:
        rectZ = pygame.Rect(z[0], z[1], 35, 43)
        for p in listaProiettili:
            rectP = pygame.Rect(p[0], p[1], 10, 10)
            if rectZ.colliderect(rectP):
                daRimuovereZ.append(z)
                daRimuovereP.append(p)
                ListaSangue.append([z[0], z[1], pygame.time.get_ticks()])
                ZombieUccisi +=1

    for z in daRimuovereZ:
        if z in ListaZombie:
            ListaZombie.remove(z)
            
            

    for p in daRimuovereP:
        if p in listaProiettili:
            listaProiettili.remove(p)

    return ZombieUccisi


def GestisciSangue(ListaSangue):
    tempoAttuale = pygame.time.get_ticks()
    for sanguePos in ListaSangue: 
        if tempoAttuale - sanguePos[2] <= 3000:
            schermo.blit(sangue, (sanguePos[0] - 40, sanguePos[1] - 43))
        else:
            ListaSangue.remove(sanguePos)


def AumentoSpawnZombie(tempoUltimoSpawn, ListaZombie, tempoUltimaOndata, durataOndata, partenzaSu, fineSu, partenzaGiu, fineGiu, partenzaSx, fineSx, partenzaDx, fineDX ):
    incremento = random.randint(3,10)
    incremento = random.randint(3,10)
    if pygame.time.get_ticks() - tempoUltimaOndata >= 15000:
        for _ in range(10+incremento):
            ListaZombie.append(SpawnZombie(partenzaSu, fineSu, partenzaGiu, fineGiu, partenzaSx, fineSx, partenzaDx, fineDX))
        
        tempoUltimaOndata = pygame.time.get_ticks()
    
    if pygame.time.get_ticks() - tempoUltimoSpawn >= durataOndata:
        ListaZombie.append(SpawnZombie(partenzaSu, fineSu, partenzaGiu, fineGiu, partenzaSx, fineSx, partenzaDx, fineDX))
        tempoUltimoSpawn = pygame.time.get_ticks()

    return tempoUltimoSpawn, ListaZombie, tempoUltimaOndata



def GestisciVita(ListaZombie, giocatoreX, giocatoreY, cuori, tempoUltimoDanno, contatoreDanno, n):
    rectGiocatore = pygame.Rect(giocatoreX, giocatoreY, 49, 43)
    tempoAttuale = pygame.time.get_ticks()
    dannoSubito = False

    for z in ListaZombie:
        rectZombie = pygame.Rect(z[0], z[1], 35, 43)
        if rectGiocatore.colliderect(rectZombie):
            dannoSubito = True

    if dannoSubito and tempoAttuale - tempoUltimoDanno >= 2000:
        if cuori > 0:
            contatoreDanno += n 
            if contatoreDanno >= 2:
                cuori -= 1
                contatoreDanno = 0
        tempoUltimoDanno = tempoAttuale

   
    for _ in range(3):
        if cuori>0:
            schermo.blit(cuore, (1250, 10))
        if cuori>1:
            schermo.blit(cuore, (1250, 10))
            schermo.blit(cuore, (1310, 10))
        if cuori>2:
            schermo.blit(cuore, (1250, 10))
            schermo.blit(cuore, (1310, 10))
            schermo.blit(cuore, (1370, 10))


    return cuori, tempoUltimoDanno, contatoreDanno


def CuoriCasuali(tempoUltimoCuore, CuorePos, CuoreVisibile, giocatoreX, giocatoreY, cuori, maxCuori):
    if not CuoreVisibile and pygame.time.get_ticks() - tempoUltimoCuore >= 20000 and cuori<=2:
        if random.random() < 0.05:
            CuorePos = (random.randint(0, LARGHEZZASCHERMO - 50), random.randint(0, ALTEZZASCHERMO - 50))
            CuoreVisibile = True
            tempoUltimoCuore = pygame.time.get_ticks()

    if CuoreVisibile:
        rectGiocatore = pygame.Rect(giocatoreX, giocatoreY, 49, 43)
        rectCuore = pygame.Rect(CuorePos[0], CuorePos[1], 50, 50)
        if rectGiocatore.colliderect(rectCuore):
            if cuori < maxCuori:
                cuori += 1
            CuoreVisibile = False

    if CuoreVisibile:
        schermo.blit(cuoreBonus, CuorePos)

    return tempoUltimoCuore, CuorePos, CuoreVisibile, cuori


def FulminiCasuali(tempoUltimoFulmine, FulminePos, FulmineVisibile, giocatoreX, giocatoreY, velocita, velocitaProiettile, tempoProiettili, Fulmineattivo, raccolto):
    
    tempoAttuale = pygame.time.get_ticks()

    
    if not FulmineVisibile and tempoAttuale - tempoUltimoFulmine >= 20000:
        if random.random() < 0.02:
            FulminePos = (random.randint(0, LARGHEZZASCHERMO - 70), random.randint(0, ALTEZZASCHERMO - 70))
            FulmineVisibile = True
            tempoUltimoFulmine = tempoAttuale

    
    if FulmineVisibile:
        rectGiocatore = pygame.Rect(giocatoreX, giocatoreY, 49, 43)
        rectFulmine = pygame.Rect(FulminePos[0], FulminePos[1], 70, 70)

        if rectGiocatore.colliderect(rectFulmine):
            FulmineVisibile = False
            Fulmineattivo = tempoAttuale
            raccolto = True

    
    if raccolto:
        if tempoAttuale - Fulmineattivo <= 5000:
            velocita = 10
            velocitaProiettile = 15
            tempoProiettili = 0.2
        else:
            raccolto = False
            velocita = 5
            velocitaProiettile = 10
            tempoProiettili = 0.5
            Fulmineattivo = 0

    
    if FulmineVisibile:
        schermo.blit(fulmine, FulminePos)

    return tempoUltimoFulmine, FulminePos, FulmineVisibile, velocita, velocitaProiettile, tempoProiettili, Fulmineattivo, raccolto



def ColpiCasuali(ColpiVisibili, tempoUltimoRifornimento, RifPos, giocatoreX, giocatoreY, scorte, Presi, tempoColpiRaccolti):
    tempoAttuale = pygame.time.get_ticks()

    if not ColpiVisibili and tempoAttuale - tempoUltimoRifornimento >= 25000:
        if random.random() < 0.04:
            RifPos = (random.randint(0, LARGHEZZASCHERMO - 70), random.randint(0, ALTEZZASCHERMO - 70))
            ColpiVisibili = True
            tempoUltimoRifornimento = tempoAttuale

    if ColpiVisibili:
        rectGiocatore = pygame.Rect(giocatoreX, giocatoreY, 49, 43)
        rectRifornimento = pygame.Rect(RifPos[0], RifPos[1], 70, 70)

        if rectGiocatore.colliderect(rectRifornimento):
            ColpiVisibili = False
            Presi = True
            tempoColpiRaccolti = tempoAttuale
            scorte += random.randint(10, 20)

    if ColpiVisibili:
        schermo.blit(rifornimenti, (RifPos))

    return tempoUltimoRifornimento, scorte, ColpiVisibili, RifPos, Presi, tempoColpiRaccolti


def StatoIniziale():
    mappaCorrente = None
    spazioPremuto = False

    giocatoreX = 300
    giocatoreY = 300
    velocita = 5

    tempoUltimoCuore = pygame.time.get_ticks()
    CuorePos = (0, 0)
    CuoreVisibile = False
    maxCuori = 3

    tempoUltimoFulmine = pygame.time.get_ticks()
    FulminePos = (0, 0)
    FulmineVisibile = False
    Fulmineattivo = 0
    raccolto = False

    tempoUltimoRifornimento = 0
    ColpiVisibili = False
    RifPos = (0, 0)
    Presi = False
    tempoColpiRaccolti = 0

    listaProiettili = []
    velocitaProiettile = 10
    scorte = 100
    caricatore = 20
    maxCaricatore = 20
    ultimoColpo = time.time()
    ultimaRicarica = 0
    ricarica = False
    IntervalloSparo = 0.5

    MieMappe = False

    ZombieUccisi = 0
    velocitaZombie = 2
    frequenzaSpawn = 2000
    tempoUltimoSpawn = pygame.time.get_ticks()
    tempoUltimaOndata = 0
    durataOndata = 5000
    ListaZombie = []

    sangueMostrato = False
    tempoSangue = 0
    ListaSangue = []

    cuori = 3
    contatoreDanno = 0
    tempoUltimoDanno = pygame.time.get_ticks()

    gioco = False

    font = pygame.font.Font("font/ZOMBIE.TTF", 36)

    nomeGiocatore = ""
    inserendoNome = True
    nomeInserito = False

    Salvato = False

    MioFile = False

    tempoUltimoBoss = 0
    ListaBoss = []
    vitaBoss = 10
    velocitaBoss = 3

    nuovoPercorso = ""
    messaggioMappaNonCorretta = False
    tempoMessaggioErrore = 0

    tempoUltimaBomba = 0
    BombaVisibile = False
    BombaPos = (0, 0)
    BombaPresa = False
    tempoBombaRaccolta = 0

    return (mappaCorrente, spazioPremuto, giocatoreX, giocatoreY, velocita,
            tempoUltimoCuore, CuorePos, CuoreVisibile, maxCuori,
            tempoUltimoFulmine, FulminePos, FulmineVisibile, Fulmineattivo, raccolto,
            tempoUltimoRifornimento, ColpiVisibili, RifPos, Presi, tempoColpiRaccolti,
            listaProiettili, velocitaProiettile, scorte, caricatore, maxCaricatore,
            ultimoColpo, ultimaRicarica, ricarica, IntervalloSparo,
            ZombieUccisi, velocitaZombie, frequenzaSpawn, tempoUltimoSpawn,
            tempoUltimaOndata, durataOndata, ListaZombie,
            sangueMostrato, tempoSangue, ListaSangue,
            cuori, contatoreDanno, tempoUltimoDanno,
            gioco, font, nomeGiocatore, inserendoNome, nomeInserito, Salvato, MieMappe, MioFile, tempoUltimoBoss,ListaBoss,vitaBoss,velocitaBoss, 
            nuovoPercorso, messaggioMappaNonCorretta, tempoMessaggioErrore, tempoUltimaBomba,BombaVisibile,BombaPos,BombaPresa,tempoBombaRaccolta )


def InserisciNome(eventi, schermo, font, nomeGiocatore, nomeInserito, Salvato):
    
    RectCasella = pygame.Rect(500, 90, 400, 60)
    for evento in eventi:
        if evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_RETURN and nomeGiocatore.strip() != "":
                nomeInserito = True
                Salvato = True
            elif evento.key == pygame.K_BACKSPACE:
                nomeGiocatore = nomeGiocatore[:-1]
            else:
                if len(nomeGiocatore) < 15 and evento.unicode.isprintable(): #questa funzione serve in modo tale che vengano scritti solo caratteri visibili
                    nomeGiocatore += evento.unicode


    Nome = font.render("COME TI CHIAMI?:", True, (255,255,255,255))
    schermo.blit(Nome, (560, 40))

    # va a disegnare a schermo il rettangolo
    pygame.draw.rect(schermo, (184, 20, 20), RectCasella, 3, 5)

    # va a scrivere il testo dentro la casella
    Testo = font.render(nomeGiocatore, True, (255,255,255,255))
    schermo.blit(Testo, (505, 100))

    return nomeGiocatore.strip(), nomeInserito, Salvato


def CreaMappa(path):
    mappa = []
    try:
        f = open(path, "r", encoding="utf-8")
        for riga in f:
            riga = riga.strip().upper()
            mappa.append(riga)
        f.close()

        # Controllo che ci siano 25 righe
        if len(mappa) != 25:
            print(f"Errore: la mappa '{path}' ha {len(mappa)} righe, ma ne servono 25.")
            return None

        # Controllo che ogni riga abbia 45 caratteri
        for i, riga in enumerate(mappa):
            if len(riga) != 45:
                print(f"Errore: nella mappa '{path}' la riga {i+1} ha {len(riga)} colonne, ma ne servono 45.")
                return None
            

        return mappa

    except Exception:
        print(F"Errore caricando la mappa {path}")
        return None


mappaTile = {
    "A" : pygame.image.load("tile/prato.png"),
    "B" : pygame.image.load("tile/fiume.png"),
    "C" : pygame.image.load("tile/sentiero.png"),
    "D" : pygame.image.load("tile/strada.png"),
    "E" : pygame.image.load("tile/muro.png")
    }


def DisegnaMappa(mappa, mappaTile, messaggioMappaNonCorretta):
    for y, riga in enumerate(mappa):
        for x, tile in enumerate(riga):
            if tile in mappaTile:
                # Disegna il tile corrispondente alla lettera
                schermo.blit(mappaTile[tile], (x * 32, y * 32))
            else:  
                messaggioMappaNonCorretta = True
                return messaggioMappaNonCorretta

def DataEOraPartita():
    data = datetime.datetime.now()
    data1 = datetime.date.strftime(data, "%d/%m/%y")
    ora = datetime.date.strftime(data, "%H:%M:%S")
    return data1, ora

def AggiungiGiocatoreAFile(nomeGiocatore, ZombieUccisi):
    data1, ora = DataEOraPartita()

    file = open("File/Classifica.txt", "r", encoding="utf-8")
    contenuto = file.read()
    file.close()

    riga = f"Nome: {nomeGiocatore} - Punteggio: {ZombieUccisi} - Data: {data1} - Ora: {ora}\n"

    if nomeGiocatore not in contenuto:
        file = open("File/Classifica.txt", "a", encoding="utf-8")
        file.write(riga)
        file.close()
    else:
        file = open("File/Classifica.txt", "w", encoding="utf-8")
        for linea in contenuto.splitlines():
            if nomeGiocatore in linea:
                # Estrae le uccisioni della partita
                parti = linea.split(" - ")
                uccisioniAttuali = 0
                for parte in parti:
                    if "Punteggio:" in parte:
                        uccisioniAttuali = int(parte.replace("Punteggio:", "").strip()) # si estrae il valore solo per la riga che si sta controllando

                if ZombieUccisi > uccisioniAttuali:
                    file.write(riga)
                else:
                    file.write(linea + "\n")  # Se non ci sono cambiamenti viene mantenuta la riga attuale
            
            else:
                file.write(linea + "\n")
        
        file.close()

    
    OrdinaClassifica()

# estrae le uccisioni da qualsiasi riga
def estraiUccisioni(riga):
    parti = riga.split(" - ")
    for parte in parti:
        if "Punteggio:" in parte:
            return int(parte.replace("Punteggio:", "").strip())
    return 0


def OrdinaClassifica(crescente=False):
    file = open("File/Classifica.txt", "r", encoding="utf-8")
    righe = file.read().splitlines()
    file.close()


    for k in range(len(righe), 0, -1):
        for i in range(0, k-1):
            if crescente:
                if estraiUccisioni(righe[i]) > estraiUccisioni(righe[i+1]):
                    righe[i], righe[i+1] = righe[i+1], righe[i]
            else:
                if estraiUccisioni(righe[i]) < estraiUccisioni(righe[i+1]):
                    righe[i], righe[i+1] = righe[i+1], righe[i]

    # vado a sovrascrivere il tutto 
    file = open("File/Classifica.txt", "w", encoding="utf-8")
    for riga in righe:
        file.write(riga + "\n")
    file.close()


def SpawnBoss(partenzaSu, fineSu, partenzaGiu, fineGiu, partenzaSx, fineSx, partenzaDx, fineDX, VitaBoss):
    lato = random.choice(["su", "giu", "sinistra", "destra"])
    if lato == "su":
        return [random.randint(partenzaSu, fineSu), -50, VitaBoss]
    if lato == "giu":
        return [random.randint(partenzaGiu, fineGiu), ALTEZZASCHERMO + 50, VitaBoss]
    if lato == "sinistra":
        return [-50, random.randint(partenzaSx, fineSx), VitaBoss]
    if lato == "destra":
        return [LARGHEZZASCHERMO + 50, random.randint(partenzaDx, fineDX), VitaBoss]


def GestisciBoss(ListaBoss, giocatoreX, giocatoreY, velocitaBoss, boss):
    centroX = giocatoreX + 32
    centroY = giocatoreY + 32
    distanzaMinima = 40
    distanzaMinima_sq = distanzaMinima * distanzaMinima

    for i, z in enumerate(ListaBoss):
        dxGiocatore = centroX - z[0]
        dyGiocatore = centroY - z[1]
        distanza_giocatore_quadrato = dxGiocatore**2 + dyGiocatore**2

        if distanza_giocatore_quadrato != 0:
            inv_distanza = 1 / (distanza_giocatore_quadrato**0.5)
            movimentoX = dxGiocatore * inv_distanza * velocitaBoss
            movimentoY = dyGiocatore * inv_distanza * velocitaBoss
        else:
            movimentoX, movimentoY = 0, 0

        
        for j, altro in enumerate(ListaBoss):
            if i != j:
                dx = z[0] - altro[0]
                dy = z[1] - altro[1]
                dist_sq = dx**2 + dy**2
                if 0 < dist_sq < distanzaMinima_sq:
                    inv_dist = 1 / (dist_sq**0.5)
                    forza_repulsiva = (distanzaMinima_sq - dist_sq) / distanzaMinima_sq
                    movimentoX += dx * inv_dist * forza_repulsiva * velocitaBoss
                    movimentoY += dy * inv_dist * forza_repulsiva * velocitaBoss

        z[0] += movimentoX
        z[1] += movimentoY

        BImg, BRect = RotazioneZombie(boss, z[0], z[1], giocatoreX, giocatoreY)
        schermo.blit(BImg, BRect.topleft)

def CollisioneBoss(ListaBoss, listaProiettili, ListaSangue,ZombieUccisi):
    daRimuovereB = []
    daRimuovereP = []

    for b in ListaBoss:
        rectB = pygame.Rect(b[0], b[1], 50, 50)
        for p in listaProiettili:
            rectP = pygame.Rect(p[0], p[1], 10, 10)
            if rectB.colliderect(rectP):
                b[2] -= 1
                daRimuovereP.append(p)

        
        if b[2] <= 0:
            ListaSangue.append([b[0], b[1], pygame.time.get_ticks()])
            daRimuovereB.append(b)
            ZombieUccisi +=10
    
    
    for p in daRimuovereP:
        if p in listaProiettili:
            listaProiettili.remove(p)

    for b in daRimuovereB:
        if b in ListaBoss:
            ListaBoss.remove(b)

    return ZombieUccisi

def DisegnaMirino(mirino, mouseX, mouseY):
    rett = mirino.get_rect(center=(mouseX, mouseY))
    schermo.blit(mirino, rett)

clock = pygame.time.Clock()
gameOver = False


(mappaCorrente, spazioPremuto, giocatoreX, giocatoreY, velocita,
            tempoUltimoCuore, CuorePos, CuoreVisibile, maxCuori,
            tempoUltimoFulmine, FulminePos, FulmineVisibile, Fulmineattivo, raccolto,
            tempoUltimoRifornimento, ColpiVisibili, RifPos, Presi, tempoColpiRaccolti,
            listaProiettili, velocitaProiettile, scorte, caricatore, maxCaricatore,
            ultimoColpo, ultimaRicarica, ricarica, IntervalloSparo,
            ZombieUccisi, velocitaZombie, frequenzaSpawn, tempoUltimoSpawn,
            tempoUltimaOndata, durataOndata, ListaZombie,
            sangueMostrato, tempoSangue, ListaSangue,
            cuori, contatoreDanno, tempoUltimoDanno,
            gioco, font, nomeGiocatore, inserendoNome, nomeInserito, Salvato, MieMappe, MioFile, tempoUltimoBoss,ListaBoss,vitaBoss,velocitaBoss,nuovoPercorso, messaggioMappaNonCorretta, tempoMessaggioErrore,tempoUltimaBomba,BombaVisibile,BombaPos,BombaPresa,tempoBombaRaccolta) = StatoIniziale()

def MostraSceltaMappaPersonale(schermo, font):
    cartella = "MieMappe"
    file = []
    listaFile = os.listdir(cartella)

    for i in listaFile:
        if ".txt" in i:
            file.append(i)

    scegliendo = True

    while scegliendo:
        schermo.blit(SfondoMieMappe, (0, 0))

        for indice, nomefile in enumerate(file):
            testo = font.render(F"{indice+1} - {nomefile}", True, (255, 255, 255))
            schermo.blit(testo, (800, 100 + indice * 80))

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "chiudi"  
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    if len(file) >= 1:
                        return cartella + "/" + file[0]
                if event.key == pygame.K_2:
                    if len(file) >= 2:
                        return cartella + "/" + file[1]
                if event.key == pygame.K_3:
                    if len(file) >= 3:
                        return cartella + "/" + file[2]
                if event.key == pygame.K_4:
                    if len(file) >= 4:
                        return cartella + "/" + file[3]
                if event.key == pygame.K_5:
                    if len(file) >= 5:
                        return cartella + "/" + file[4]
                if event.key == pygame.K_6:
                    if len(file) >= 6:
                        return cartella + "/" + file[5]
                if event.key == pygame.K_7:
                    if len(file) >= 7:
                        return cartella + "/" + file[6]
                if event.key == pygame.K_8:
                    if len(file) >= 8:
                        return cartella + "/" + file[7]
                if event.key == pygame.K_9:
                    if len(file) >= 9:
                        return cartella + "/" + file[8]
                if event.key == pygame.K_ESCAPE:
                    return None

def GeneraBomba(BombaVisibile, tempoUltimaBomba, BombaPos, giocatoreX, giocatoreY, BombaPresa, tempoBombaRaccolta, ListaZombie, ZombieUccisi):
    n = len(ListaZombie)
    tempoAttuale = pygame.time.get_ticks()

    if not BombaVisibile and tempoAttuale - tempoUltimaBomba >= 25000:
        if random.random() < 0.004:
            BombaPos = (random.randint(0, LARGHEZZASCHERMO - 70), random.randint(0, ALTEZZASCHERMO - 70))
            BombaVisibile = True
            tempoUltimaBomba = tempoAttuale

    if BombaVisibile == True:
        rectGiocatore = pygame.Rect(giocatoreX, giocatoreY, 49, 43)
        rectBomba = pygame.Rect(BombaPos[0], BombaPos[1], 50, 50)

        if rectGiocatore.colliderect(rectBomba):
            BombaVisibile = False
            BombaPresa = True
            tempoBombaRaccolta = tempoAttuale
            for z in ListaZombie.copy():
                ListaZombie.remove(z)
                ListaSangue.append([z[0], z[1], pygame.time.get_ticks()])
            ZombieUccisi +=n 

    if BombaVisibile:
        schermo.blit(bomba, (BombaPos))

    GestisciSangue(ListaSangue)

    return tempoUltimaBomba, BombaVisibile, BombaPos,BombaPresa, tempoBombaRaccolta, ZombieUccisi




clock = pygame.time.Clock()
gameOver = False


(mappaCorrente, spazioPremuto, giocatoreX, giocatoreY, velocita,
            tempoUltimoCuore, CuorePos, CuoreVisibile, maxCuori,
            tempoUltimoFulmine, FulminePos, FulmineVisibile, Fulmineattivo, raccolto,
            tempoUltimoRifornimento, ColpiVisibili, RifPos, Presi, tempoColpiRaccolti,
            listaProiettili, velocitaProiettile, scorte, caricatore, maxCaricatore,
            ultimoColpo, ultimaRicarica, ricarica, IntervalloSparo,
            ZombieUccisi, velocitaZombie, frequenzaSpawn, tempoUltimoSpawn,
            tempoUltimaOndata, durataOndata, ListaZombie,
            sangueMostrato, tempoSangue, ListaSangue,
            cuori, contatoreDanno, tempoUltimoDanno,
            gioco, font, nomeGiocatore, inserendoNome, nomeInserito, Salvato, MieMappe, MioFile, tempoUltimoBoss,ListaBoss,vitaBoss,velocitaBoss,nuovoPercorso, messaggioMappaNonCorretta, tempoMessaggioErrore,tempoUltimaBomba,BombaVisibile,BombaPos,BombaPresa,tempoBombaRaccolta) = StatoIniziale()


schermataTitolo, SfondoMappe, personaggioBase, proiettile, zombie, sangue, cuore, fulmine, cuoreBonus, rifornimenti, GameOver, uno,due,tre,quattro, nuovaMappa, boss,mirino, SfondoMieMappe, bomba = CaricaImmagini()


while not gameOver:
    eventi = pygame.event.get()

    for event in eventi:
        if event.type == pygame.QUIT:
            gameOver = True
        
        if gioco:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE and cuori == 0:
            
                (mappaCorrente, spazioPremuto, giocatoreX, giocatoreY, velocita,
                tempoUltimoCuore, CuorePos, CuoreVisibile, maxCuori,
                tempoUltimoFulmine, FulminePos, FulmineVisibile, Fulmineattivo, raccolto,
                tempoUltimoRifornimento, ColpiVisibili, RifPos, Presi, tempoColpiRaccolti,
                listaProiettili, velocitaProiettile, scorte, caricatore, maxCaricatore,
                ultimoColpo, ultimaRicarica, ricarica, IntervalloSparo,
                ZombieUccisi, velocitaZombie, frequenzaSpawn, tempoUltimoSpawn,
                tempoUltimaOndata, durataOndata, ListaZombie,
                sangueMostrato, tempoSangue, ListaSangue,
                cuori, contatoreDanno, tempoUltimoDanno,
                gioco, font, nomeGiocatore, inserendoNome, nomeInserito, Salvato, MieMappe, MioFile, tempoUltimoBoss,ListaBoss,vitaBoss,
                velocitaBoss,nuovoPercorso, messaggioMappaNonCorretta, tempoMessaggioErrore,tempoUltimaBomba,BombaVisibile,BombaPos,BombaPresa,tempoBombaRaccolta) = StatoIniziale()

            
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mouseX, mouseY = pygame.mouse.get_pos()
                if caricatore > 0 and not ricarica and time.time() - ultimoColpo >= IntervalloSparo:
                    SparaProiettile(giocatoreX, giocatoreY, mouseX, mouseY, listaProiettili)
                    caricatore -= 1
                    ultimoColpo = time.time()
            
            if event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                if not ricarica and caricatore < maxCaricatore and scorte > 0:
                    ricarica = True
                    ultimaRicarica = time.time()
        
        else:
            spazioPremuto = GestisciSpazio(event, spazioPremuto)

    if not gioco:
        if not spazioPremuto:
            schermo.blit(schermataTitolo, (0, 0))
        elif mappaCorrente is None and not MieMappe:

            schermo.blit(SfondoMappe, (0, 0))
            schermo.blit(MiniMappe[1], (30, 400))
            schermo.blit(MiniMappe[2], (400, 400))
            schermo.blit(MiniMappe[3], (760, 400))
            schermo.blit(MiniMappe["m"], (1120, 400))
            schermo.blit(uno, (140, 650))
            schermo.blit(due, (525, 650))
            schermo.blit(tre, (890, 650))
            schermo.blit(quattro, (1255, 650))
            
            if messaggioMappaNonCorretta:
                tempoAdesso = pygame.time.get_ticks()
                if tempoAdesso - tempoMessaggioErrore <= 3000:  
                    testoErrore = font.render("LA MAPPA NON È CORRETTA", True, (255, 0, 0))
                    schermo.blit(testoErrore, (400, 100))
                else:
                    messaggioMappaNonCorretta = False

            if not nomeInserito:
                nomeGiocatore, nomeInserito, Salvato = InserisciNome(eventi, schermo, font, nomeGiocatore, nomeInserito, Salvato)
                    
            else:
                for event in eventi:
                    scelta, n = ScegliMappa(event,nuovoPercorso)
                    if n == 1 or n == 2 or n == 3:
                        mappaCorrente = scelta
                        gioco = True
                    elif n == 4:
                        nuovoPercorso = MostraSceltaMappaPersonale(schermo, font)
                        if nuovoPercorso == "chiudi":
                            gameOver = True 
                        elif nuovoPercorso:
                            mappa = CreaMappa(nuovoPercorso)
                            if mappa is not None:
                                mappaCorrente = nuovoPercorso
                                gioco = True
                                MioFile = True
                            else:
                                MieMappe = False
                                mappaCorrente = None
                                messaggioMappaNonCorretta = True
                                tempoMessaggioErrore = pygame.time.get_ticks()
                         
    else:
        if cuori <= 0:
            schermo.blit(GameOver, (400, 10))
            AggiungiGiocatoreAFile(nomeGiocatore, ZombieUccisi)

        else:
            if MioFile == False:
                schermo.blit(mappaCorrente, (0, 0))
                tempoDiGioco = pygame.time.get_ticks()
            else:
                mappa = CreaMappa(mappaCorrente)
                if mappa:  # CONTROLLA che la mappa esista
                    messaggioMappaNonCorretta = DisegnaMappa(mappa, mappaTile, messaggioMappaNonCorretta)
                    if messaggioMappaNonCorretta == True:
                        tempoAdesso = pygame.time.get_ticks()
                        if tempoAdesso - tempoMessaggioErrore <= 3000:  
                            testoErrore = font.render("LA MAPPA NON È CORRETTA", True, (255, 0, 0))
                            schermo.blit(testoErrore, (400, 100))

                    
            
            tasti = pygame.key.get_pressed()
            giocatoreX, giocatoreY = GestisciMovimento(tasti, giocatoreX, giocatoreY, velocita)
            
            giocatoreRuotato, giocatoreRett = RuotaVersoMouse(personaggioBase, giocatoreX, giocatoreY, *pygame.mouse.get_pos())
            
            GestisciProiettili(listaProiettili, velocitaProiettile)
            for p in listaProiettili:
                img = pygame.transform.rotate(proiettile, p[4])
                rect = img.get_rect(center=(p[0], p[1]))
                schermo.blit(img, rect.topleft)
            
            tempoUltimaBomba, BombaVisibile, BombaPos,BombaPresa, tempoBombaRaccolta,ZombieUccisi = GeneraBomba(BombaVisibile, tempoUltimaBomba, BombaPos, giocatoreX, giocatoreY, BombaPresa, tempoBombaRaccolta, ListaZombie, ZombieUccisi)
            GestisciSangue(ListaSangue)

            schermo.blit(giocatoreRuotato, giocatoreRett.topleft)

            ZombieUccisi = CollisioniZombie(ListaZombie, listaProiettili, ZombieUccisi)
            tempoUltimoSpawn, ListaZombie, tempoUltimaOndata = AumentoSpawnZombie(
                tempoUltimoSpawn, ListaZombie, tempoUltimaOndata, durataOndata, 
                0, LARGHEZZASCHERMO, 0, LARGHEZZASCHERMO, 0, ALTEZZASCHERMO, 0, ALTEZZASCHERMO)
            GestisciZombie(ListaZombie, giocatoreX, giocatoreY, velocitaZombie, zombie)

    
            tempoDiGioco = pygame.time.get_ticks()

            
            if len(ListaBoss) == 0 and tempoDiGioco - tempoUltimoBoss > random.randint(55000, 60000):
                bossSpawnato = SpawnBoss(100, LARGHEZZASCHERMO-100, 100, LARGHEZZASCHERMO-100, 100, ALTEZZASCHERMO-100, 100, ALTEZZASCHERMO-100, vitaBoss)
                ListaBoss.append(bossSpawnato)
                tempoUltimoBoss = tempoDiGioco

            if len(ListaBoss) > 0:
                GestisciBoss(ListaBoss, giocatoreX, giocatoreY, velocitaBoss, boss)
                ZombieUccisi = CollisioneBoss(ListaBoss, listaProiettili, ListaSangue, ZombieUccisi)
                cuori, tempoUltimoDanno, contatoreDanno = GestisciVita(ListaBoss, giocatoreX, giocatoreY, cuori, tempoUltimoDanno, contatoreDanno, n = 2)

            
            cuori, tempoUltimoDanno, contatoreDanno = GestisciVita(ListaZombie, giocatoreX, giocatoreY, cuori, tempoUltimoDanno, contatoreDanno, n = 1)
            
            tempoUltimoCuore, CuorePos, CuoreVisibile, cuori = CuoriCasuali(tempoUltimoCuore, CuorePos, CuoreVisibile, giocatoreX, giocatoreY, cuori, maxCuori)
            tempoUltimoFulmine, FulminePos, FulmineVisibile, velocita, velocitaProiettile, IntervalloSparo, Fulmineattivo, raccolto = FulminiCasuali(
                tempoUltimoFulmine, FulminePos, FulmineVisibile, giocatoreX, giocatoreY, 
                velocita, velocitaProiettile, IntervalloSparo, Fulmineattivo, raccolto)
            tempoUltimoRifornimento, scorte, ColpiVisibili, RifPos, Presi, tempoColpiRaccolti = ColpiCasuali(
                ColpiVisibili, tempoUltimoRifornimento, RifPos, giocatoreX, giocatoreY, 
                scorte, Presi, tempoColpiRaccolti)

            

           
            
            if ricarica and time.time() - ultimaRicarica >= 2:
                diff = min(maxCaricatore - caricatore, scorte)
                scorte -= diff
                caricatore += diff
                ricarica = False
            

            mouseX, mouseY = pygame.mouse.get_pos()
            DisegnaMirino(mirino, mouseX, mouseY)
            GestisciScritte(schermo, caricatore, ricarica, ultimaRicarica, scorte, ZombieUccisi, font)
            


    pygame.display.update()
    clock.tick(30)


AggiungiGiocatoreAFile(nomeGiocatore, ZombieUccisi)



pygame.quit()