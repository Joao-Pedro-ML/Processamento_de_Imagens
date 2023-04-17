import cv2
import numpy as np
import matplotlib.pyplot as plt

WSHED = 0



imgc = cv2.imread("./Imagens/blood.png")
img = cv2.imread("./Imagens/blood.png", 0)

plt.close('all')
#Leitura da imagem
plt.figure(1)
plt.subplot(1, 2, 1, title="original")
plt.imshow(imgc)
plt.subplot(1, 2, 2, title="grayscale")
plt.imshow(img, cmap='gray')


#binarização (thresholding)
ret, th0 = cv2.threshold(img,0,255,cv2.THRESH_BINARY_INV+cv2.THRESH_OTSU)
plt.figure(2)
plt.title("2 - Binarização")
plt.imshow(th0, cmap='gray')

#realiza a erosão para remover imperfeições
kernel = np.ones((3,3),np.uint8)
ero = cv2.erode(th0, kernel, iterations=2)
#opening = cv2.morphologyEx(ero, cv2.MORPH_OPEN, kernel)
plt.figure(3.1)
plt.title("3.1 - Erosão")
plt.imshow(ero, cmap='gray')
# plt.figure(3.2)
# plt.title("3.2 - Opening")
# plt.imshow(opening, cmap='gray')

if WSHED:

    
    
    #Componentes conectados
    ret, markers = cv2.connectedComponents(ero)
    print(markers.shape, markers.max(), markers.min())
    #markers[markers%2==0] = 0
    plt.figure(4)
    plt.title("4 - Componentes Conectados")
    plt.imshow(markers, cmap='gray')
    
    #Aplicando o watershed
    roi = cv2.watershed(imgc,markers)
    imgc[markers==-1] = [0, 0, 255]
    plt.figure(5)
    plt.title("5 - Watershed")
    plt.imshow(imgc)
    
    #comparando o Canny com um filtro de detecção de bordas com kernel
    k2 = np.ones((3,3)) *-1
    k2[1,1] = 8
    im = cv2.imread("./Imagens/coins.jpg")
    f1 = cv2.filter2D(im, -1, k2)
    plt.figure(6)
    plt.imshow(f1, cmap='gray')
    can = cv2.Canny(im, 100, 200)
    plt.figure(7)
    plt.imshow(can, cmap='gray')


#contornos 
contours, hierarchy = cv2.findContours(ero, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
print(len(contours))
cnt_img = imgc.copy()
cv2.drawContours(cnt_img, contours, -1, (0,255,0), 3)
plt.figure(7)
plt.title("7 - Draw Contours")
plt.imshow(cnt_img)

#contornos externos
cnt_img2 = imgc.copy()
contours, hierarchy = cv2.findContours(ero, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
cv2.drawContours(cnt_img2, contours, -1, (0,255,0), 3)
plt.figure(8)
plt.title("8 - Draw Contours pegando somente bordas externas")
plt.imshow(cnt_img2)


# filtro por área
areas = [cv2.contourArea(c) for c in contours]
mx = np.max(areas)
print(mx)
contours_f = [contours[i] for i in range(len(contours)) if areas[i] > mx/3]
contours_f2 = [c for c in contours if cv2.contourArea(c) > mx/3] #faz a mesma coisa que contours
cv2.drawContours(cnt_img, contours_f, -1, (0,0,255), 3)
plt.figure(9)
plt.title("Filtro por area")
plt.imshow(cnt_img)


# convex hull
cnt_img = imgc.copy()
c_hull = [cv2.convexHull(c) for c in contours]
cv2.drawContours(cnt_img, contours, -1, (255,0,0), 2)
cv2.drawContours(cnt_img, c_hull, -1, (0,0,255), 1)
plt.figure(11); plt.imshow(cnt_img)

# filtro por diferença de área
areas_ch = [cv2.contourArea(c) for c in c_hull]
cont_filt2 = [contours[i] for i in range(len(contours)) if areas_ch[i] > areas[i]*1.1]
cnt_img = imgc.copy()
cv2.drawContours(cnt_img, cont_filt2, -1, (0,0,255), 1)
plt.figure(12); plt.imshow(cnt_img)
