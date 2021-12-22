#"O" representa a la IA; "X" al jugador; 0 casilla vacia
#El jugador siempre empieza primero y es representado por -1 con turno
import copy
import pygame, sys
from pygame.locals import *

turno=1
hojas=[]

class button():
    def __init__(self, color, x,y,width,height, text=''):
        self.color = color
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = 0

    def draw(self,win,caracter="X"):
        pygame.draw.rect(win, self.color, (self.x,self.y,self.width,self.height),0)

        if self.text != '':
            font = pygame.font.SysFont('comicsans', 60)
            if caracter=="X":
                text = font.render(self.text, 1, (45,164,215))
            elif caracter =="O":
                text = font.render(self.text, 1, (150,50,50))
            win.blit(text, (self.x + (self.width/2 - text.get_width()/2), self.y + (self.height/2 - text.get_height()/2)))

    def isOver(self, pos):
        #Pos is the mouse position or a tuple of (x,y) coordinates
        if pos[0] > self.x and pos[0] < self.x + self.width:
            if pos[1] > self.y and pos[1] < self.y + self.height:
                return True

        return False

    def cancelar(self,win,caracter):
        self.text=caracter
        self.draw(win,caracter)

class Node:
    def __init__(self, padre, caracter, i, j, estado):
        if padre==None and caracter==None and i==None and j==None:
            self.estado=copy.deepcopy(estado)
        elif padre!=None:
            self.padre=padre
            self.estado=copy.deepcopy(padre.estado)
            self.caracter = caracter
            self.i = i
            self.j = j
            self.estado[i][j] = caracter
        elif estado!=None:
            self.estado=copy.deepcopy(estado)
            self.caracter = caracter
            self.i = i
            self.j = j
            self.estado[i][j] = caracter
        self.hijos=[]
        self.valor=False
def espaciosVacios(estado):
    espacios=[]
    for i in range(3):
        for j in range(3):
            if(estado[i][j]==0):
                espacios.append([i,j])
    return espacios

def verElFuturo(node, turno):
    tuplaEspacios=espaciosVacios(node.estado)
    if turno==1:
        caracter="O"
    else:
        caracter="X"
    turno=-turno
    for i in range(len(tuplaEspacios)):
        hijo=Node(node, caracter, tuplaEspacios[i][0], tuplaEspacios[i][1], None)
        gana=ganador(hijo.estado)
        if gana=="X":
            hijo.valor=-10
            hojas.append(hijo)
            node.hijos.append(hijo)
            return
        elif gana=="O":
            hijo.valor=10
            hojas.append(hijo)
            node.hijos.append(hijo)
            return
        elif len(tuplaEspacios)==0:
            hijo.valor=0
            hojas.append(hijo)
            node.hijos.append(hijo)
            return
        node.hijos.append(hijo)
        verElFuturo(hijo, turno)

def ganador(estado):
    gano=""
    for i in range(3):
        if estado[0][i]=="X" and estado[1][i]=="X" and estado[2][i]=="X":
            gano="X"
        elif estado[i][0]=="X" and estado[i][1]=="X" and estado[i][2]=="X":
            gano="X"
        elif estado[0][i]=="O" and estado[1][i]=="O" and estado[2][i]=="O":
            gano="O"
        elif estado[i][0]=="O" and estado[i][1]=="O" and estado[i][2]=="O":
            gano="O"
    if estado[0][0]=="X" and estado[1][1]=="X" and estado[2][2]=="X":
        gano="X"
    elif estado[0][0]=="O" and estado[1][1]=="O" and estado[2][2]=="O":
        gano="O"
    elif estado[0][2]=="X" and estado[1][1]=="X" and estado[2][0]=="X":
        gano="X"
    elif estado[0][2]=="O" and estado[1][1]=="O" and estado[2][0]=="O":
        gano="O"
    return gano

def evaluarNodos(padre, turno):
    if len(padre.hijos)==0:
        return
    if turno==-1:
        min=15
        for i in range(len(padre.hijos)):
            if padre.hijos[i].valor==False:
                evaluarNodos(padre.hijos[i],-turno)
            if padre.hijos[i].valor==-10:
                min=-10
                nodo_electo=padre.hijos[i]
                break
            if padre.hijos[i].valor<min:
                min=padre.hijos[i].valor
                nodo_electo=padre.hijos[i]
        padre.valor=min
    else:
        max=-15
        for i in range(len(padre.hijos)):
            if padre.hijos[i].valor==False:
                evaluarNodos(padre.hijos[i],-turno)
            if padre.hijos[i].valor==10:
                max=10
                nodo_electo=padre.hijos[i]
                break
            if padre.hijos[i].valor>max:
                max=padre.hijos[i].valor
                nodo_electo=padre.hijos[i]
        padre.valor=max
    return nodo_electo

def cuadrante(i, j):
    fila=int(i/3)
    columna=int(j/3)
    return fila, columna

def colorear(grid_i,grid_j,chara):
    for j in range(3):
        for i in range(3):
            aux=tablero[(grid_i*3)+i][(grid_j*3)+j]
            if chara=="X":
                aux.color=fondoX
            elif chara=="O":
                aux.color=fondoO
            else:
                aux.color=fondoE
            font = pygame.font.SysFont('comicsans', 60)
            text = font.render(aux.text, 1, (45,164,215))
            pygame.draw.rect(screen, aux.color, (aux.x,aux.y,aux.width,aux.height),0)

def verificacion(meow, grid_i, grid_j, meowsote):
    mini_ganador=ganador(meow[grid_i][grid_j])
    verificar=False
    termino=False
    if len(espaciosVacios(meow[grid_i][grid_j]))==0:
        meowsote[grid_i][grid_j]="/"
        colorear(grid_i,grid_j,"/")
        verificar=True
    else:
        if mini_ganador=="X":
            meowsote[grid_i][grid_j]="X"
            colorear(grid_i,grid_j,"X")
            verificar = True
        elif mini_ganador=="O":
            meowsote[grid_i][grid_j]="O"
            colorear(grid_i,grid_j,"O")
            verificar = True
    if verificar==True:
        ganador_total=ganador(meowsote)
        if ganador_total=="X":
            print "Gano el humano"
            termino = True
        elif ganador_total=="O":
            print "Gano IA"
            termino = True
        elif len(espaciosVacios(meowsote))==0:
            print "Empate!"
            termino=True

    return termino

pygame.init()
screen = pygame.display.set_mode((1000, 1000))
colorBG = pygame.Color(35,35,35)
screen.fill(colorBG)
pygame.display.set_caption("Gato de gatos")

colorCeldas = pygame.Color(20,20,20)
fondoX = pygame.Color(50,50,100)
fondoO = pygame.Color(100,50,50)
fondoE = pygame.Color(0,0,0)

auxiliarx=2
auxiliary=2
separacionx=-85
separaciony=-85
tablero=[]
for y in range(9):
    auxiliary+=1
    if auxiliary%3 == 0:
        separaciony+=10
    separaciony+=105
    tablero.append([])
    for x in range(9):
        auxiliarx+=1
        if auxiliarx%3 == 0:
            separacionx+=10
        separacionx+=105
        tablero[y].append(button(colorCeldas,separacionx,separaciony,95,95))
        tablero[y][x].draw(screen)

    separacionx = -85
#separaciones vergas
meow=[[[[0 for i in range(3)] for j in range(3)] for k in range(3)] for m in range(3)]
meowsote=[[0,0,0],[0,0,0],[0,0,0]]

switch=False
while True:
    jugada=[0,0]
    for evento in pygame.event.get():
        if evento.type==MOUSEBUTTONDOWN:
            pos=pygame.mouse.get_pos()
            for j in range(len(tablero)): #j es la fila
                conti=-1
                for i in tablero[j]:
                    conti+=1
                    if i.isOver(pos)==True:
                        i.cancelar(screen,"X")
                        jugada[0]=j
                        jugada[1]=conti
                        switch=True

        if evento.type==QUIT:
            pygame.quit()
            sys.exit()

    #ya le dieron click, ahora va la AI
    if switch==True:
        jugada[0]=int(jugada[0])
        jugada[1]=int(jugada[1])
        grid_i, grid_j = cuadrante(jugada[0], jugada[1])
        meow[grid_i][grid_j][(jugada[0])%3][(jugada[1])%3]='X'
        termino=verificacion(meow, grid_i, grid_j, meowsote)
        if termino==True:
            break
        if meowsote[grid_i][grid_j]=='/':
            for i in range(3):
                for j in range(3):
                    if meowsote[i][j]==0:
                        grid_i=i
                        grid_j=j
                        break
            Padre=Node(None,None,None,None,meow[grid_i][grid_j])
        elif meowsote[grid_i][grid_j]==0:
            Padre=Node(None,'X',(jugada[0])%3, (jugada[1])%3,meow[grid_i][grid_j])
        else:
            print "No puedes introducir una ficha ahi"
        verElFuturo(Padre,1)
        Nodo_electo=evaluarNodos(Padre,1)
        meow[grid_i][grid_j][Nodo_electo.i][Nodo_electo.j]='O' #grid i-col grid j-fila
        tablero[(grid_i*3)+Nodo_electo.i][(grid_j*3)+Nodo_electo.j].cancelar(screen,"O") #AQUIIIIIIII
        termino = verificacion(meow, grid_i, grid_j, meowsote)
        if termino == True:
            break
        switch=False
    pygame.display.update()
