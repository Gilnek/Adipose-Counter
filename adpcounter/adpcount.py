#!/usr/bin env python3

import cv2 as cv
from cv2 import imwrite
import numpy as np
import math
from typing import Any, Tuple
from pathlib import Path

def adp_count(image_path: Path | str, return_image = True) -> Tuple[int,Any|None]:
    original = cv.imread(image_path)
    image = original.copy()

    #transformação da imagem para escala de cinza
    gray = cv.cvtColor(image, cv.COLOR_BGR2GRAY)
    cv.imwrite("gray.png", gray)

    

    #binarização da imagem
    thresh =  cv.threshold(gray, 125, 125,  #FIXME PFVZIN
        cv.THRESH_BINARY | cv.THRESH_OTSU
    )[1]
    imwrite("threshold.png", thresh)


    #engrossa a imagem
    kernel = np.ones((2,2),np.uint8)
    dilation = cv.dilate(thresh,kernel,iterations = 1)

    #afina a imagem
    erosion = cv.erode(dilation,kernel,iterations = 2)

    mask = erosion
    cv.imwrite("mask.png", mask)

    kernel = cv.getStructuringElement(cv.MORPH_ELLIPSE, (3,3))
    opening = cv.morphologyEx(mask, cv.MORPH_OPEN, kernel, iterations=1)
    close = cv.morphologyEx(opening, cv.MORPH_CLOSE, kernel, iterations=2)

    cnts = cv.findContours(close, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
    cnts = cnts[0] if len(cnts) == 2 else cnts[1]

    area_min = 50  #60
    area_med = 75 #550
    area_conexao = 500 #500
    adipocitos = 0

    #faz os contornos
    for c in cnts:
        area = cv.contourArea(c)
        if area > area_min:
            cv.drawContours(image, [c], -1, (36,255,12), 2)
            if area > area_conexao:
                adipocitos += math.ceil(area / area_med)
            else:
                adipocitos += 1

    return adipocitos, image if return_image else None