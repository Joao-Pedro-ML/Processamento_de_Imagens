# Nexte trabalho utilize as teclas:
# 'q' para sair
# 'z' para aumentar a matiz
# 'x' para diminuir a matiz 
# 'b' para mudar a imagem de fundo
# 's' para salvar a imagem
# 't' para mudar o filtro para azul


import cv2
import numpy as np
#import matplotlib.pyplot as plt

# abre a camera
#vid = cv2.VideoCapture(0)

# variável que representa modificação da cor
delta = 60

matiz=95

background1 = cv2.imread('fundo1.jpg')
background2 = cv2.imread('fundo2.jpg')
background3 = cv2.imread('fundo3.jpg')

im0 = cv2.imread('figura.png')
#print(im0.shape)

i = 1

background = cv2.imread("fundo"+"%d"%i+".jpg")

#back2 = cv2.resize(background2, (w, h))
#back3 = cv2.resize(background3, (w, h))

#print(back1.shape)
#print(back2.shape)
#print(back3.shape)

tipo = 0;

while(True):
    #lê uma nova imagem da câmera
    #ret, im0 = vid.read()

    background = cv2.imread("fundo"+"%d"%i+".jpg")
    h, w = im0.shape[0:2]
    back = cv2.resize(background, (w, h))
    
    # transforma a imagem em HSV    
    hsv_img = cv2.cvtColor(im0, cv2.COLOR_BGR2HSV)
    hsv_orig = hsv_img.copy()
    #converte a imagem background em hsv
    hsv_back = cv2.cvtColor(back, cv2.COLOR_BGR2HSV)


    # separa os canais hsv
    h, s, v = cv2.split(hsv_img)
    
    # filtra os pixels dentro do limite
    low = (matiz-2, 20, 20)
    high = (matiz+2, 255, 250)
    mask = cv2.inRange(hsv_img, low, high)

    # máscara com 3 canais
    mask_3 = cv2.cvtColor(mask, cv2.COLOR_GRAY2BGR)
    not_mask_3 = cv2.bitwise_not(mask_3)

    # cria uma imagem com cores alteradas
    hsv_img2 = hsv_back.copy()
    #hsv_img2[:, :,0] = (hsv_img2[:, :,0].astype(int) + delta)%180
    
    # filtra os pixels    
    fg = cv2.bitwise_and(hsv_orig, not_mask_3)
    bg = cv2.bitwise_and(hsv_img2, mask_3)
    fg = cv2.cvtColor(fg, cv2.COLOR_HSV2BGR)
    bg = cv2.cvtColor(bg, cv2.COLOR_HSV2BGR)



    # mostra imagem 
    cv2.imshow('frame', fg+bg)
    
    # lê tecla pressionada
    k = cv2.waitKey(10) & 0xFF
    if k == ord('q'):
        break
    if k == ord('z'):
        matiz += 5
        print(matiz)
    if k == ord('x'):
        matiz -= 5
        print (matiz)
    if k == ord('b'):
        i = i + 1
        if i == 4:
            i = 1
    if k == ord('s'):
        cv2.imwrite("figura.png", im0)
    if k == ord('t'):
        tipo = tipo + 1
        matiz = 105
        if tipo == 2 :
            tipo = 0
            matiz = 95
            

#vid.release()
#cv2.destroyAllWindows()




