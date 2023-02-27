from tkinter import messagebox, Tk
import pygame
import sys
from random import random
from pynput import keyboard
from pynput.keyboard import Listener


window_width = 400
window_height = 400

window = pygame.display.set_mode((window_width, window_height))

grid = [] #Inicializamos el arreglo que almacenará arreglos, para así formar una matríz que almacenará el estado de todas nuestras celdas.
cellsToCheck = []
shortestPath = []

#Celdas y columnas usadas para dibujar la cuadrícula que representará el mapa
columns = 20
rows = 20
startSearching = False
cell_width = int(window_width / columns)
cell_height = int(window_height / rows)

#Las celdas son unidades de espacio o distancia,
class Cell:
    def __init__(self, i, j):
        self.x = i
        self.y = j
        self.start = False
        self.end = False
        self.wall = False
        self.pendingCheck = False #Variable para definir si una celda esta en la cola para ser procesada
        self.checked = False #Variable para definir si una celda ya fue procesada
        self.adyacentCells = []
        self.previousCell = None
        self.fromShortestPath = False

    def setCloseCells(self):
        if self.x > 0:
            self.adyacentCells.append(grid[self.x - 1][self.y])
        if self.x < columns - 1:
            self.adyacentCells.append(grid[self.x + 1][self.y])
        if self.y > 0:
            self.adyacentCells.append(grid[self.x][self.y - 1])
        if self.y < rows - 1:
            self.adyacentCells.append(grid[self.x][self.y + 1])
    
    def paint(self, window, color):
        pygame.draw.circle(window, color, (int(self.x*cell_width+cell_width/2), int(self.y*cell_height+cell_height/2)), int((cell_height if cell_height<cell_width else cell_width)/2)-1)

    def paintWall(self, window, color):
        pygame.draw.rect(window, color, (self.x*cell_width+1, self.y*cell_height+1, cell_width-1, cell_height-1))



#Función con la que pintamos los límites entre las celdas.
def drawCellLimits(xSteps, ySteps, xMax, yMax):
    for i in range(0, xMax, xSteps):
        pygame.draw.line(window, '#3C3C3C', (i, 0), (i, yMax))
    for i in range(0, yMax, ySteps):
        pygame.draw.line(window, '#3C3C3C', (0, i), (xMax, i))



#Por medio de este método creamos un nuevo mapa
def generateWalls():
    #Reseteamos los valores de las paredes
    for i in range(columns):
        for j in range (rows):
            grid[i][j].wall = False
            grid[i][j].checked = False
            grid[i][j].pendingCheck = False
            grid[i][j].fromShortestPath = False

    isWall = True
    wallLengthVariator = 0 #Esta variable nos sirve para variar la longitud del muro un poco
    for j in range(1, rows, 2):
        for i in range (columns):
            if isWall:
                grid[i][j].wall = True
            wallLengthVariator += int(random()*200)
            if wallLengthVariator >= 100:
                isWall = not isWall
                wallLengthVariator = 0
    
    isWall = False
    for i in range(1, rows, 4):
        for j in range (columns):
            if isWall:
                grid[i][j].wall = True
            wallLengthVariator += int(random()*200)
            if wallLengthVariator >= 100:
                isWall = not isWall
                wallLengthVariator = 0
    
    #Inicialización o Reiniicialización de variables
    startingCell.wall = False
    endCell.wall = False

def regenerateWalls():
    generateWalls()     

#Creamos un eventListener y lo agregamos al hilo de ejecución principal.


#Creamos la matriz de celdas
for i in range(columns):
    arr = []
    for j in range (rows):
        arr.append(Cell(i, j))
    grid.append(arr)


#Definimos la primera y útlima celda
startingCell = grid[0][0]
endCell = grid[columns-8][rows-8]

#Enlazamos las celdas aledañas para cada celda:
for i in range (columns):
    for j in range(rows):
        grid[i][j].setCloseCells()

#Inicializamos la primer celda:
startingCell.start = True
startingCell.checked = True
cellsToCheck.append(startingCell)

endCell.end = True  


    
def main():
    generateWalls()
    pygame.init()
    searching = True
    startSearching = True
    foudit = True
    font = pygame.font.Font('JetBrainsMono-ExtraBold.ttf  ', 16)
    img = font.render('No se puede encontrar el final!', True, 'yellow')

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                foudit = True
                startingCell.start = True
                startingCell.checked = True
                cellsToCheck.clear()
                cellsToCheck.append(startingCell)
                startSearching = True
                searching = True
                regenerateWalls()
        
        
        #Dibujamos el fondo y las celdas
        window.fill('#2C2C2C')
        drawCellLimits(cell_width, cell_height, window_width, window_height)
        #Dibujamos los cuadros
        for i in range(columns):
            for j in range(rows):
                if grid[i][j].wall == True:
                    grid[i][j].paintWall(window, 'black')
                if grid[i][j].pendingCheck:
                    grid[i][j].paintWall(window, '#365c5d')
                if grid[i][j].checked:
                    grid[i][j].paintWall(window, '#558f90')
                if grid[i][j].fromShortestPath:
                    grid[i][j].paintWall(window, '#f6d010')
                if grid[i][j].start:
                    grid[i][j].paintWall(window, '#eedc98')
                if grid[i][j].end:
                    grid[i][j].paintWall(window, '#d38b9a')


        
        if startSearching:
            if len(cellsToCheck) > 0 and searching: #Mientras no encontremos el destino y tengamos más celdas por checar:
                currentCell = cellsToCheck.pop(0)
                currentCell.checked = True #Al sacar una celda de la cola la marcamos como visitada
                if currentCell == endCell: 
                    searching = False #Una vez encontrada la celda final regresamos a través de los antecesores uno a la vez para marcar el camino más corto:
                    while currentCell != startingCell:
                        currentCell.fromShortestPath = True
                        currentCell = currentCell.previousCell
                else:
                    for adyacentCell in currentCell.adyacentCells:
                        if not adyacentCell.pendingCheck and not adyacentCell.wall:
                            adyacentCell.pendingCheck = True
                            adyacentCell.previousCell = currentCell
                            cellsToCheck.append(adyacentCell)
            else:
                if searching: #Si buscabamos pero nos quedamos sin celdas por checar significa que no existe una solución:
                    foudit = False
                    searching = False
        
        
        if not foudit:
            window.blit(img, (50, 180))
        pygame.time.delay(10)
        pygame.display.flip()           

        
    

main()