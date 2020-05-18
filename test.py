import pygame
import cv2
import keras
import numpy as np
import itertools


class button():
    def __init__(self, color, x,y,width,height, text=''):
        self.color = color
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text

    def draw(self,win,outline):
        if outline:
            pygame.draw.rect(win, outline, (self.x-2,self.y-2,self.width+4,self.height+4),2)
            
        pygame.draw.rect(win, self.color, (self.x,self.y,self.width,self.height),0)
        
        if self.text != '':
            font = pygame.font.SysFont('comicsans', 20)
            text = font.render(self.text, 1, (255,255,255))
            win.blit(text, (self.x + (self.width/2 - text.get_width()/2), self.y + (self.height/2 - text.get_height()/2)))

    def isOver(self, pos):
        if pos[0] > self.x and pos[0] < self.x + self.width:
            if pos[1] > self.y and pos[1] < self.y + self.height:
                return True
            
        return False

def answer():
	img = cv2.imread('test.png', cv2.IMREAD_GRAYSCALE)
	dim = (28, 28)
	resized_img = cv2.resize(img, dim, interpolation = cv2.INTER_AREA)
	resized_img1 = resized_img[np.newaxis,...,np.newaxis]
	model = keras.models.load_model('mnist.model')
	prediction = model.predict([resized_img1])
	prediction = np.argmax(prediction)
	return str(prediction)
 
pygame.init()
pygame.display.list_modes()
win = pygame.display.set_mode((500,500))
pygame.display.set_caption("MNIST")
pygame.display.update()
pygame.draw.line(win, (255,255,255),(0,350),(500,350))
pygame.display.flip()
predictButton = button((0,0,0), 75,400,100,40,'Predict')
clearButton = button((0,0,0), 300,400,100,40,'Clear')
predictButton.draw(win,(255,255,255))
clearButton.draw(win,(255,255,255))
run = True
dots = []
draw = False
while run:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			run = False
		elif event.type == pygame.MOUSEBUTTONDOWN:
			(x,y) = event.pos
			if predictButton.isOver(event.pos):
				rect = pygame.Rect(0, 0, 500, 350)
				sub = win.subsurface(rect)
				pygame.image.save(sub, "test.png")
				predict = 'You have written '+ answer()
				font = pygame.font.SysFont('comicsans', 25)
				text = font.render(predict, 1, (255,255,255))
				win.blit(text, (150 + (100 - text.get_width()/2), 425 + (50 - text.get_height()/2)))
			elif clearButton.isOver(event.pos):
				pygame.draw.rect(win, (0,0,0), (0, 0, 500, 350), 0)
				pygame.draw.rect(win, (0,0,0), (0, 450, 500, 50), 0)
				dots = []
				pygame.display.update()
			else:
				for (i,j) in itertools.product(range(20),range(20)):
					dots.append((x+i,y+j))
				draw = True
		elif event.type == pygame.MOUSEBUTTONUP:
			draw = False
		elif event.type == pygame.MOUSEMOTION:
			if draw:
				(x,y) = event.pos
				for (i,j) in itertools.product(range(20),range(20)):
					dots.append((x+i,y+j))
		if len(dots)>1:
			pygame.draw.lines(win, (255, 255, 255), False, dots) 
		pygame.display.update()

pygame.quit()
