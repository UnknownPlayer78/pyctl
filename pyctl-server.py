import _thread as thread
import socket
import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import pygame
from time import sleep

width = 300
height = 300
running = True

pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("pyctl")

HOST = '0.0.0.0'
PORT = 8193


def connection_handler(c,addr):
    global running
    while running:
        pressed = pygame.key.get_pressed()
        data = ":" + "".join([str(s) for s in pressed]) + ";"
        c.send(bytearray(data.encode()))
        sleep(0.01)

def event_handler():
    global running
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                os._exit(0)

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((HOST, PORT))
s.listen()

while running:
    thread.start_new_thread(event_handler,tuple())
    c, addr = s.accept()
    print(addr, "connected.")
    thread.start_new_thread(connection_handler,(c,addr))


s.close()
pygame.quit()