# thư viện
import pygame
from os import listdir
import cv2
import numpy as np
import pickle
from sklearn.preprocessing import OneHotEncoder
from sklearn.model_selection import train_test_split
from keras.applications.vgg16 import VGG16
from keras.layers import Input, Flatten, Dense, Dropout
from keras.models import Model
from keras.callbacks import ModelCheckpoint
import matplotlib.pyplot as plt
import random
from keras.models import  load_model
import sys
pygame.init()
clock=pygame.time.Clock()

#tiêu đề và icon
pygame.display.set_caption('Dino Game')
icon = pygame.image.load(r'assets\dinosaur.png')

#cửa sổ game
screen = pygame.display.set_mode((600,300))

#tải hình
bg=pygame.image.load(r'assets\background.jpg')
tree=pygame.image.load(r'assets\tree.png')
dino = pygame.image.load(r'assets\dinosaur.png')

#load âm thanh
sound1=pygame.mixer.Sound(r'sound\tick.wav')
sound2=pygame.mixer.Sound(r'sound\te.wav')

#các biến khởi tạo
score=0 #khởi tạo điểm
hscore=0
bg_x = 0 
bg_y = 0
tree_x=550
tree_y = 230
dino_x=0
dino_y = 230
x_def=6 #tốc độ chạy
y_def=7 #tốc độ rơi
jump=False
gameplay=True
stop=False

cap = cv2.VideoCapture(0)

# Dinh nghia class
class_name = ['continue','go','nhay','pause']

my_model=load_model(r'cu_chi.h5')

#hàm kiểm tra va chạm
def checkvc():
    if dino_hcn.colliderect(tree_hcn):
        pygame.mixer.Sound.play(sound2)
        return False
    else:
        return True
    
#đưa score vào game:
game_font=pygame.font.Font('04B_19.TTF',20)

def score_view():
    if gameplay:
        score_txt=game_font.render(f'score: {int(score)}',True,(255,0,0))
        screen.blit(score_txt,(250,50))
        hscore_txt=game_font.render(f'High score: {int(hscore)}',True,(255,0,0))
        screen.blit(hscore_txt,(350,50))

    else:
        hscore_txt=game_font.render(f'High score: {int(hscore)}',True,(255,0,0))
        screen.blit(hscore_txt,(250,50))
        over_txt=game_font.render(f'Game Over',True,(255,0,0))
        screen.blit(over_txt,(250,200))
        


#vòng lặp xử lý game
running=True
while running:
    #chỉnh FPS
    clock.tick(60)
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            running=False
        if event.type==pygame.KEYDOWN:
            if event.key ==pygame.K_SPACE and gameplay:
                print('nhảy')
                if dino_y==230:
                    pygame.mixer.Sound.play(sound1)
                    jump=True
            if event.key ==pygame.K_e and gameplay:
                stop=True
                stop_txt=game_font.render(f'PAUSE',True,(255,0,0))
                screen.blit(stop_txt,(250,200))
            if event.key ==pygame.K_q and gameplay:
                stop=False
            if event.key ==pygame.K_SPACE and gameplay==False:
                gameplay=True



    if gameplay and stop==False:
        #hình nền
        bg_hcn=screen.blit(bg,(bg_x,bg_y)) 
        bg2_hcn=screen.blit(bg,(bg_x+600,bg_y))  
        bg_x-=x_def
        if bg_x<=-600: bg_x=0
        #cây
        tree_hcn=screen.blit(tree,(tree_x,tree_y)) 
        tree_x-=x_def
        if tree_x<=-20: tree_x=600
        #khủng long
        dino_hcn=screen.blit(dino,(dino_x,dino_y))  
        if dino_y>80 and jump:
            dino_y-=y_def
        else:
            jump=False
        if dino_y<230 and jump==False:
            dino_y+=y_def
        score+=0.01
        if hscore<score: hscore=score
        gameplay=checkvc()
        score_view()


    elif gameplay==False:
        #reset game
        score=0
        bg_x = 0 
        bg_y = 0
        tree_x=550
        tree_y = 230
        dino_x=0
        dino_y = 230
        bg_hcn=screen.blit(bg,(bg_x,bg_y)) 
        tree_hcn=screen.blit(tree,(tree_x,tree_y))
        dino_hcn=screen.blit(dino,(dino_x,dino_y)) 
        score_view()

    pygame.display.update()




