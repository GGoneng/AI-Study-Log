import pygame
import os
import sys
import math

class Unit:
    def __init__(self, x, y):
        self.x = x
        self.y = y

        self.des_x = self.x
        self.des_y = self.y
        self.is_stopped = True

        self.speed = 1

    def set_img(self, file_name):
        if file_name[-3:] == "png":
            self.img = pygame.image.load(file_name).convert_alpha()
        else:
            self.img = pygame.image.load(file_name)
        self.size_x, self.size_y = self.img.get_size()
    
    def set_size(self, sx, sy):
        self.img = pygame.transform.scale(self.img, (sx, sy))
        self.size_x, self.size_y = self.img.get_size()
    
    def show(self):
        game_pad.blit(self.img, (self.x, self.y))


    def set_position(self):
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 2:
                self.des_x, self.des_y =  pygame.mouse.get_pos()

    def move(self):
        dx = self.des_x - self.x
        dy = self.des_y - self.y
        length = math.sqrt(dx ** 2, dy ** 2)
        theta = math.atan2(dy, dx)
        
        amount = min(length, self.speed)
        
        # amount는 단위 시간당 이동할 수 있는 빗변의 거리
        # amount와 역탄젠트 각도를 사용한 cos을 곱하면 단위 시간당 이동하는 x좌표, sin을 곱하면 단위 시간당 이동하는 y좌표
        self.x += amount * math.cos(theta)
        self.y += amount * math.sin(theta)

        

def init_game():
    while True:
        pygame.init()
        pygame.mixer.init()
        img_dir = "C:\\Users\\KDP-2\\OneDrive\\바탕 화면\\EX_PY06\\Project"

        win_size = [1280, 960]
        game_pad = pygame.display.set_mode(win_size)
        game_title = "Starcraft"
        pygame.display.set_caption(game_title)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

def run_game():
    ss = Unit()
    ss.set_img(os.path.join(img_dir, "abc.png"))
    ss.set_size(80, 80)
    ss.pos_x = round(win_size[0]/2 - ss.size_x/2) 
    ss.pos_y = win_size[1] - ss.size_y - 15
    ss.move = 5
    
if __name__ == "__main__":
    init_game()
    run_game()
