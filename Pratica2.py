# -*- coding: utf-8 -*-
"""
Created on Wed Apr 19 08:25:08 2023

@author: Joao Pedro
"""

import cv2
import numpy as np
import matplotlib.pyplot as plt

plt.close('all')

arv = cv2.imread("./Imagens/arvores.jpg")
arv = cv2.resize(arv, (600,300)) #redimensionamento da imagem
print(arv.shape)
# plt.figure(1)
# plt.imshow(arv, cmap='gray')


b, g, r = cv2.split(arv)

plt.figure(1); plt.imshow(b, cmap='gray') #canal azul
cv2.imwrite("./Imagens/b.png", b)

plt.figure(2); plt.imshow(g, cmap='gray') #canal verde
cv2.imwrite("./Imagens/g.png",g)

plt.figure(3); plt.imshow(r, cmap='gray') #canal vermelho
cv2.imwrite("./Imagens/r.png",r)

blur = cv2.blur(b, (4,4)) #blur para poder detectar melhor a área das árvores

#Binarização
ret, th0 = cv2.threshold(blur, 0, 155, cv2.THRESH_BINARY_INV+cv2.THRESH_OTSU)
plt.figure(4)
plt.title("4 - Binarização")
plt.imshow(th0, cmap='gray')
cv2.imwrite("./Imagens/threshold.png",th0)
#Para saber a área das árvores, somei todas as posições da imagem binarizada que tinham valor 0
print("Área total ocupada pelas árvores em pixels:", np.sum(th0 == 0))

#erosão, que mostra os píxels de cada árvore
kernel1 = np.ones((2,2), np.uint8)
ero = cv2.erode(th0, kernel1, iterations=2)
opening = cv2.morphologyEx(ero, cv2.MORPH_OPEN, kernel1) #opening para obter um resultado melhor da binarização
plt.figure(5)
plt.title("5 - Erosão")
plt.imshow(opening, cmap='gray')
cv2.imwrite("./Imagens/opening.png",opening)


#contornos 
contours, hierarchy = cv2.findContours(opening, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
cnt = blur.copy()
cv2.drawContours(cnt, contours, -2, (0,255,0), 2)
plt.figure(6)
plt.title("6 - Contornos")
plt.imshow(cnt)
cv2.imwrite("./Imagens/contorno.png",cnt)
# utiliza a função findCountours para contar os contornos da imagem, que foram obtidos acima
(number, hierarchy2) = cv2.findContours(cnt.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
print("Número de árvores: ", len(number))







