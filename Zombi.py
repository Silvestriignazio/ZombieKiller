import pygame
import os
import math
import time
import random

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
    3: pygame.image.load("mappe/mappa3.png")
}
MiniMappe = {
    1: pygame.transform.scale(DizionarioMappe[1], (MINIMAPPA_LARGHEZZA, MINIMAPPA_ALTEZZA)),
    2: pygame.transform.scale(DizionarioMappe[2], (MINIMAPPA_LARGHEZZA, MINIMAPPA_ALTEZZA)),
    3: pygame.transform.scale(DizionarioMappe[3], (MINIMAPPA_LARGHEZZA, MINIMAPPA_ALTEZZA))
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

    return schermataTitolo, sfondoMappe, personaggio, proiettile, zombie, sangue, cuore, fulmine, cuoreBonus, rifornimenti, GameOver

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


def ScegliMappa(event):
    if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_1:
            return DizionarioMappe[1]
        elif event.key == pygame.K_2:
            return DizionarioMappe[2]
        elif event.key == pygame.K_3:
            return DizionarioMappe[3]
    return None

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

def GestisciScritte(schermo, caricatore, ricarica, ultimaRicarica, scorte, ZombieUccisi):
    font = pygame.font.Font("font/ZOMBIE.TTF", 36)
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
    TestoKill = font.render(F"Zombie eliminati {ZombieUccisi}", True, (255,255,255))
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
        rectZ = pygame.Rect(z[0], z[1], 40, 43)
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



def GestisciVita(ListaZombie, giocatoreX, giocatoreY, cuori, tempoUltimoDanno, contatoreDanno):
    rectGiocatore = pygame.Rect(giocatoreX, giocatoreY, 32, 32)
    tempoAttuale = pygame.time.get_ticks()
    dannoSubito = False

    for z in ListaZombie:
        rectZombie = pygame.Rect(z[0], z[1], 40, 43)
        if rectGiocatore.colliderect(rectZombie):
            dannoSubito = True

    if dannoSubito and tempoAttuale - tempoUltimoDanno >= 2000:
        if cuori > 0:
            contatoreDanno += 1 
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
        rectGiocatore = pygame.Rect(giocatoreX, giocatoreY, 64, 64)
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
        rectGiocatore = pygame.Rect(giocatoreX, giocatoreY, 64, 64)
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
        rectGiocatore = pygame.Rect(giocatoreX, giocatoreY, 64, 64)
        rectRifornimento = pygame.Rect(RifPos[0], RifPos[1], 70, 70)

        if rectGiocatore.colliderect(rectRifornimento):
            ColpiVisibili = False
            Presi = True
            tempoColpiRaccolti = tempoAttuale
            scorte += random.randint(5, 10)

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
            gioco)

def InserisciNome():
    pass


def CreaMappa():
    pass



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
 gioco) = StatoIniziale()

clock = pygame.time.Clock()
gameOver = False

# Carica tutte le immagini
schermataTitolo, SfondoMappe, personaggioBase, proiettile, zombie, sangue, cuore, fulmine, cuoreBonus, rifornimenti, GameOver = CaricaImmagini()

while not gameOver:
    for event in pygame.event.get():
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
                gioco) = StatoIniziale()

                
                spazioPremuto = False
                mappaCorrente = None
                gioco = False

            
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
            if spazioPremuto and mappaCorrente is None:
                scelta = ScegliMappa(event)
                if scelta:
                    mappaCorrente = scelta
                    gioco = True
    
    
    if not gioco:
        if not spazioPremuto:
            schermo.blit(schermataTitolo, (0, 0))
        elif mappaCorrente is None:
            schermo.blit(SfondoMappe, (0, 0))
            schermo.blit(MiniMappe[1], (100, 400))
            schermo.blit(MiniMappe[2], (580, 400))
            schermo.blit(MiniMappe[3], (1100, 400))
    else:
        if cuori <= 0:
            schermo.blit(GameOver, (400, 10))
        else:
            schermo.blit(mappaCorrente, (0, 0))
            
            
            tasti = pygame.key.get_pressed()
            giocatoreX, giocatoreY = GestisciMovimento(tasti, giocatoreX, giocatoreY, velocita)
            
            
            giocatoreRuotato, giocatoreRett = RuotaVersoMouse(personaggioBase, giocatoreX, giocatoreY, *pygame.mouse.get_pos())
            
            
            GestisciProiettili(listaProiettili, velocitaProiettile)
            for p in listaProiettili:
                img = pygame.transform.rotate(proiettile, p[4])
                rect = img.get_rect(center=(p[0], p[1]))
                schermo.blit(img, rect.topleft)
            
           
            GestisciSangue(ListaSangue)

            
            schermo.blit(giocatoreRuotato, giocatoreRett.topleft)

            
            ZombieUccisi = CollisioniZombie(ListaZombie, listaProiettili, ZombieUccisi)
            tempoUltimoSpawn, ListaZombie, tempoUltimaOndata = AumentoSpawnZombie(
                tempoUltimoSpawn, ListaZombie, tempoUltimaOndata, durataOndata, 
                0, LARGHEZZASCHERMO, 0, LARGHEZZASCHERMO, 0, ALTEZZASCHERMO, 0, ALTEZZASCHERMO)
            GestisciZombie(ListaZombie, giocatoreX, giocatoreY, velocitaZombie, zombie)
            
            
            
        
            cuori, tempoUltimoDanno, contatoreDanno = GestisciVita(ListaZombie, giocatoreX, giocatoreY, cuori, tempoUltimoDanno, contatoreDanno)
            
            
            
            
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
            
            
            GestisciScritte(schermo, caricatore, ricarica, ultimaRicarica, scorte, ZombieUccisi)

    pygame.display.update()
    clock.tick(120)

pygame.quit()