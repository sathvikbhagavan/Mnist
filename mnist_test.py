import pygame
import cv2
import keras
import numpy as np
import itertools

#Button Class for making buttons
class Button:
    #Constructor 
    def __init__(self, color, x, y, width, height, text=''):
        self.color = color
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text

    #Drawing the button on the window
    def draw(self, win):
        
        pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.height), 0)

        if self.text != '':
            font = pygame.font.SysFont('comicsans', 20)
            text = font.render(self.text, 1, (255, 255, 255))
            win.blit(text, (
                self.x + (self.width / 2 - text.get_width() / 2), self.y + (self.height / 2 - text.get_height() / 2)))
    
    #To check if the button is pressed or not 
    def is_over(self, pos):
        if self.x < pos[0] < self.x + self.width:
            if self.y < pos[1] < self.y + self.height:
                return True

        return False

#Predicting from the model trained on standard MNIST dataset
def answer():
    img = cv2.imread('mnist_test.png', cv2.IMREAD_GRAYSCALE)
    img = cv2.subtract(255, img) 
    dim = (28, 28)
    resized_img = cv2.resize(img, dim, interpolation=cv2.INTER_AREA)
    resized_img1 = resized_img[np.newaxis, ..., np.newaxis]
    model = keras.models.load_model('mnist.model')
    prediction = model.predict([resized_img1])
    prediction = np.argmax(prediction)
    return str(prediction)

#Intializing pygame
pygame.init()
pygame.display.list_modes()

#Making the basic setup window of the game
win = pygame.display.set_mode((500, 500))
win.fill((255,255,255))
pygame.display.set_caption("MNIST")
pygame.draw.line(win, (0, 0, 0), (0, 350), (500, 350), 5)
predictButton = Button((0, 0, 0), 75, 400, 100, 40, 'PREDICT')
clearButton = Button((0, 0, 0), 300, 400, 100, 40, 'CLEAR')
predictButton.draw(win)
clearButton.draw(win)
pygame.display.update()

run = True
dots = []
draw = False
while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            (x, y) = event.pos
            
            #if predict button is pressed
            if predictButton.is_over(event.pos):
                rect = pygame.Rect(0, 0, 500, 350)
                sub = win.subsurface(rect)
                pygame.image.save(sub, "mnist_test.png")
                predict = 'You have written ' + answer()
                font = pygame.font.SysFont('comicsans', 25)
                text = font.render(predict, 1, (0, 0, 0))
                win.blit(text, (150 + (100 - text.get_width() / 2), 425 + (50 - text.get_height() / 2)))
                
            #if clear button is pressed
            elif clearButton.is_over(event.pos):
                pygame.draw.rect(win, (255, 255, 255), (0, 0, 500, 350), 0)
                pygame.draw.rect(win, (255, 255, 255), (0, 450, 500, 50), 0)
                pygame.draw.line(win, (0, 0, 0), (0, 350), (500, 350), 5)
                dots = []
                pygame.display.update()
                
            #Not drawing below the line (A horizontal line is displayed below which you cannot draw)
            elif y>350:
                continue
            
            #Coordinates are taken of the points around the mouse click
            else:
                for (i, j) in itertools.product(range(20), range(20)):
                    dots.append((x + i, y + j))
                draw = True
                
        #Drawing is stopped
        elif event.type == pygame.MOUSEBUTTONUP:
            draw = False
            dots = []
        
        #Coordinates are taken of the points around the mouse movement
        elif event.type == pygame.MOUSEMOTION:
            if draw:
                (x, y) = event.pos
                for (i, j) in itertools.product(range(20), range(20)):
                    dots.append((x + i, y + j))
                    
        #Drawing the collected points from mouse click and motion
        if len(dots) > 1:
            pygame.draw.lines(win, (0, 0, 0), False, dots)
        pygame.display.update()

pygame.quit()
