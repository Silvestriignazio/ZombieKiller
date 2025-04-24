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
    fulmine = pygame.transform.scale(pygame.image.load("immagini/fulmine.png"), (70, 70))
    return schermataTitolo, sfondoMappe, personaggio, proiettile, zombie, sangue, cuore, fulmine


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

def InfoProiettili(schermo, proiettiliRimanenti, ricarica, ultimaRicarica):
    font = pygame.font.Font("font/ZOMBIE.TTF", 36)
    testoColpi = font.render(F"Colpi {proiettiliRimanenti}", True, (255,255,255))
    schermo.blit(testoColpi, (10,10))
    if proiettiliRimanenti == 0:
        testoColpi = font.render(F"Colpi {proiettiliRimanenti}", True, (255,0,0))
        schermo.blit(testoColpi, (10,10))
    if ricarica:
        tempo = max(0, 2 - int(time.time() - ultimaRicarica))
        testoRicarica = font.render(F"Ricarica {tempo}s", True, (255,0,0))
        schermo.blit(testoRicarica, (10,50))

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

        # Forza repulsiva dagli altri zombie
        for j, altro in enumerate(ListaZombie):
            if i != j:
                dx = z[0] - altro[0]
                dy = z[1] - altro[1]
                dist_sq = dx**2 + dy**2
                if 0 < dist_sq < distanzaMinima_sq:
                    inv_dist = 1 / (dist_sq**0.5)
                    forza_repulsiva = (distanzaMinima_sq - dist_sq) / distanzaMinima_sq
                    movimentoX += dx * inv_dist * forza_repulsiva * velocitaZombie
                    movimentoY += dy * inv_dist * forza_repulsiva * velocitaZombie

        z[0] += movimentoX
        z[1] += movimentoY

        zImg, zRect = RotazioneZombie(zombie, z[0], z[1], giocatoreX, giocatoreY)
        schermo.blit(zImg, zRect.topleft)


def CollisioniZombie(ListaZombie, listaProiettili ):
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

    for z in daRimuovereZ:
        if z in ListaZombie:
            ListaZombie.remove(z)

    for p in daRimuovereP:
        if p in listaProiettili:
            listaProiettili.remove(p)


def GestisciSangue(ListaSangue):
    tempoAttuale = pygame.time.get_ticks()
    for sanguePos in ListaSangue: 
        if tempoAttuale - sanguePos[2] <= 3000:
            schermo.blit(sangue, (sanguePos[0] - 40, sanguePos[1] - 43))
        else:
            ListaSangue.remove(sanguePos)


def AumentoSpawnZombie(tempoUltimoSpawn, ListaZombie, tempoUltimaOndata, durataOndata, partenzaSu, fineSu, partenzaGiu, fineGiu, partenzaSx, fineSx, partenzaDx, fineDX ):

    if pygame.time.get_ticks() - tempoUltimaOndata >= 15000: # Controlla se sono passati 15 secondi dall'ultima ondata
    
        for _ in range(10):  # Aggiunge una l'ondata di zombie
            ListaZombie.append(SpawnZombie(partenzaSu, fineSu, partenzaGiu, fineGiu, partenzaSx, fineSx, partenzaDx, fineDX))
        
        # Imposta il tempo dell'ultima ondata
        tempoUltimaOndata = pygame.time.get_ticks()
    
    # Gestione  dello spawn 
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
            if contatoreDanno >= 2:  # Ogni 2 danni, riduci un cuore
                cuori -= 1
                contatoreDanno = 0
        tempoUltimoDanno = tempoAttuale

   
    for i in range(3):
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
    # Spawn del cuore se non visibile e trascorso abbastanza tempo
    if not CuoreVisibile and pygame.time.get_ticks() - tempoUltimoCuore >= 5000:
        CuorePos = (random.randint(0, LARGHEZZASCHERMO - 70), random.randint(0, ALTEZZASCHERMO - 70))
        CuoreVisibile = True
        tempoUltimoCuore = pygame.time.get_ticks()

    # Controlla se il giocatore raccoglie il cuore
    if CuoreVisibile:
        rectGiocatore = pygame.Rect(giocatoreX, giocatoreY, 64, 64)
        rectCuore = pygame.Rect(CuorePos[0], CuorePos[1], 70, 70)
        if rectGiocatore.colliderect(rectCuore):
            if cuori < maxCuori:  # Aggiunge un cuore solo se non si supera il massimo
                cuori += 1
            CuoreVisibile = False  # Rimuove il cuore dalla mappa

    # Disegna il cuore sullo schermo se visibile
    if CuoreVisibile:
        schermo.blit(cuore, CuorePos)

    return tempoUltimoCuore, CuorePos, CuoreVisibile, cuori

def FulminiCasuali():
    pass
    

def ColpiCausali():
    pass


schermataTitolo, SfondoMappe, personaggioBase, proiettile, zombie, sangue, cuore, fulmine = CaricaImmagini()

mappaCorrente = None
spazioPremuto = False

giocatoreX = 300
giocatoreY = 300
velocita = 5
velocitaZombie = 2

tempoUltimoCuore = pygame.time.get_ticks()
CuorePos = (0, 0)  # Posizione iniziale
CuoreVisibile = False
tempoApparizioneCuore = 0  # Tempo di quando è apparso l'ultimo fulmine
tempoFulmine = 8000
maxCuori = 3

listaProiettili = []
maxProiettili = 20
proiettili_rimanenti = maxProiettili
velocitaProiettile = 10
ultimoColpo = time.time()
ultimaRicarica = 0
ricarica = False


velocitaZombie = 2
frequenzaSpawn = 2000
tempoUltimoSpawn = pygame.time.get_ticks()
frequenzaSpawn = 2000 
tempoUltimaOndata = 0
durataOndata = 5000
ListaZombie = [] 


sangueMostrato = False
tempoSangue = 0
ListaSangue = []

cuori = 3
contatoreDanno = 0
tempoUltimoDanno = pygame.time.get_ticks()


clock = pygame.time.Clock()
gameOver = False


while not gameOver:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            gameOver = True
        spazioPremuto = GestisciSpazio(event, spazioPremuto)
        if spazioPremuto and mappaCorrente is None:
            scelta = ScegliMappa(event)
            if scelta:
                mappaCorrente = scelta
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and mappaCorrente:
            mouseX, mouseY = pygame.mouse.get_pos()
            if proiettili_rimanenti > 0 and not ricarica and time.time() - ultimoColpo >= 0.5:
                SparaProiettile(giocatoreX, giocatoreY, mouseX, mouseY, listaProiettili)
                proiettili_rimanenti -= 1
                ultimoColpo = time.time()
        if event.type == pygame.KEYDOWN and event.key == pygame.K_r:
            if not ricarica and proiettili_rimanenti < maxProiettili:
                ricarica = True
                ultimaRicarica = time.time()

    if ricarica and time.time() - ultimaRicarica >= 2:
        proiettili_rimanenti = maxProiettili
        ricarica = False

    if not spazioPremuto:
        schermo.blit(schermataTitolo, (0, 0))
    elif mappaCorrente is None:
        schermo.blit(SfondoMappe, (0, 0))
        schermo.blit(MiniMappe[1], (100, 400))
        schermo.blit(MiniMappe[2], (580, 400))
        schermo.blit(MiniMappe[3], (1100, 400))
    else:
        schermo.blit(mappaCorrente, (0, 0))
        if mappaCorrente == DizionarioMappe[1]:
            tasti = pygame.key.get_pressed()
            giocatoreX, giocatoreY = GestisciMovimento(tasti, giocatoreX, giocatoreY, velocita)
            giocatoreRuotato, giocatoreRett = RuotaVersoMouse(personaggioBase, giocatoreX, giocatoreY, *pygame.mouse.get_pos())
            GestisciProiettili(listaProiettili, velocitaProiettile)
            for p in listaProiettili:
                img = pygame.transform.rotate(proiettile, p[4])
                rect = img.get_rect(center=(p[0], p[1]))
                schermo.blit(img, rect.topleft)
            CollisioniZombie(ListaZombie, listaProiettili)
            InfoProiettili(schermo, proiettili_rimanenti, ricarica, ultimaRicarica)
            tempoUltimoSpawn, ListaZombie, tempoUltimaOndata = AumentoSpawnZombie(
                tempoUltimoSpawn, ListaZombie, tempoUltimaOndata, durataOndata,0, LARGHEZZASCHERMO, 0, LARGHEZZASCHERMO, 0, ALTEZZASCHERMO, 0, ALTEZZASCHERMO)
            GestisciSangue(ListaSangue)
            cuori, tempoUltimoDanno, contatoreDanno = GestisciVita(ListaZombie, giocatoreX, giocatoreY, cuori, tempoUltimoDanno, contatoreDanno)
            GestisciZombie(ListaZombie, giocatoreX, giocatoreY, velocitaZombie, zombie)
            schermo.blit(giocatoreRuotato, giocatoreRett.topleft)
            tempoUltimoCuore, CuorePos, CuoreVisibile, cuori = CuoriCasuali(tempoUltimoCuore, CuorePos, CuoreVisibile, giocatoreX, giocatoreY, cuori, maxCuori)
            




        
    pygame.display.update()
    clock.tick(120)

pygame.quit()