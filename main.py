import Tkinter as tk
import subprocess
import pygame
import ttk
import time

from Tkinter import *
from threading import Thread
from recognizer import q, get_note
from functools import partial  

root = Tk()

root.title('Scale trainer')
root.geometry('{}x{}'.format(500,700))

left = Frame(root, width=100, height=700)
left.grid(row=0, column=0, sticky="ns")

right = Frame(root, width=400, height=700)
right.grid(row=0, column=1, sticky="ns")

#watek zeby rozpoznawiaine dzialalo w tle
t = Thread(target=get_note)
t.daemon = True
t.start()

clr=0
running= True
active=""
sound = None

def playScale(a):
    global right, clr, active, sound
    data=""
    sound=""	
    file1=open(a+'.txt', 'r')
    nazwa = file1.readline()
    dzwieki = file1.readline()
    print("W pliku txt o nazwie:"+a+", jest: ")
    
    right.destroy()
    right = Frame(root, width=500, height=700)
    right.grid(row=0, column=1, sticky="ns")
    b=Button(right, text="cls", command=clear)
    b.pack()
    w = tk.Label(right, text=nazwa)
    w.config(height=3, width=50)

    w.pack()

       

    target=[]
    
    num_sound=0    

    for l in dzwieki:
	num_sound= num_sound + 1
	target.extend(l)
	w = tk.Label(right, text=l)
	w.config(font=("Courier", 20))
	w.pack(fill=tk.X)

    target.pop()	

    xd=False
    
    print(target)
    print(num_sound)
    i=0
    time.sleep(1)
    while True:
           
	    if clr==1:
		break

	    
		
	    #print("---"+str(i))
	    #i=i+1
	   
	   
	   
	    #print("i={}".format(i))
	    #print("num={}".format(num_sound-1))

	    if i >= (num_sound-1):
                num_sound=0    
	        sound=""
	        clear()
                return None	
	    else: 
		sound=get_sound()

	    if sound['Note'][0] == target[i]:
	    	print("OK: "+ str(i))
		i=i+1
		right.destroy()
	        right = Frame(root, width=500, height=700)
	        right.grid(row=0, column=1, sticky="ns")
	        b=Button(right, text="cls", command=clear)
	        b.pack()
	        w = tk.Label(right, text=nazwa)
	        w.config(height=3, width=50)
    
	        w.pack()
		j=0
		for l in dzwieki:
			
			w = tk.Label(right, text=l)
			if i > j:			
				w.config(font=("Courier", 20), fg="green")
			else:
				w.config(font=("Courier", 20))
			w.pack(fill=tk.X)
			j=j+1
	    sound=""
	   	
	 
	    right.update()

	    #time.sleep(.25)	
    return None	

def get_sound():
	if not q.empty():
	    sound = q.get()
	   # print(":) : "+ sound['Note'])
	    return sound
	else:
	    q.put({'Note': 'xx'})
	    sound = q.get()
	   # print(":( : "+ sound['Note'])
	    return sound
	
	
def clear():
    global right, clr, active
    q.queue.clear()
    right.destroy()
    right = Frame(root, width=500, height=700)
    right.grid(row=0, column=1, sticky="ns")
    clr=1
    active=""
    print("Niszcze: " +clr)

def openlink(i):
    global clr
    print("I w funkcji openlink: "+i)
    if i == 'tuner':
        tuner_main()
    elif i == 'DODAJ':
	subprocess.call("python bb.py",shell=True)
	load_scales()
    else:
	clr=0
        eval(i)


def tuner_main():
	pygame.init()
	pygame.display.set_caption('Guitar Tuner')
	screenWidth, screenHeight = 300, 500
	screen = pygame.display.set_mode((screenWidth, screenHeight))
	clock = pygame.time.Clock()

	running = True

	titleFont = pygame.font.SysFont("comicsansms", 34)
	titleText = titleFont.render("Note name:", True, (0, 128, 0))
	noteFont = pygame.font.SysFont("comicsansms", 55)

	#watek zeby rozpoznawiaine dzialalo w tle
	t = Thread(target=get_note)
	t.daemon = True
	t.start()

	

	while running:
	    for event in pygame.event.get():
		if event.type == pygame.QUIT:
		    running = False
		if event.type == pygame.KEYDOWN and event.key == pygame.K_q:
		    running = False

	    tuner(screen)
	    
	    pygame.display.flip()
	    clock.tick(30)

def tuner(screen):
	    screen.fill((0, 0, 0))
	    screenWidth, screenHeight = 300, 500
            titleFont = pygame.font.SysFont("comicsansms", 34)
	    titleText = titleFont.render("Note name:", True, (0, 128, 0))
	    noteFont = pygame.font.SysFont("comicsansms", 55)
	    pygame.draw.line(screen, (255, 255, 255), (10, 290), (10, 310))
	    pygame.draw.line(screen, (255, 255, 255), (screenWidth - 10, 290),(screenWidth - 10, 310))
	    pygame.draw.line(screen, (255, 255, 255), (screenWidth/2 - 10, 290),(screenWidth/2 - 10, 310))
	    pygame.draw.line(screen, (255, 255, 255), (10, 300),(screenWidth - 10, 300))

	    if not q.empty():
		b = q.get()
		if b['Cents'] < 15:
		    pygame.draw.circle(screen, (0, 128, 0), 
		                       (screenWidth // 2 + (int(b['Cents']) * 2),300),
		                       10)
		else:
		    pygame.draw.circle(screen, (128, 0, 0),
		                       (screenWidth // 2 + (int(b['Cents']) * 2), 300),
		                       10)

		noteText = noteFont.render(b['Note'], True, (0, 128, 0))
	    else:
		noteText = noteFont.render('---', True, (0, 128, 0))
		
	    screen.blit(noteText, (160, 80))
	    screen.blit(titleText, (10,  80))

def load_scales():
	global left
    
    	left.destroy()
	left = Frame(root, width=100, height=700)
	left.grid(row=0, column=0, sticky="ns")
	
	names=[]
	sounds=[]
	
	fp = open("LISTA.txt", "r") 
	for contents in fp: 
		names=names+[contents]
		sounds=sounds+['playScale("'+str(contents[:-1])+'")']

	names=['DODAJ']+['Tuner']+names
	sounds=['DODAJ']+['tuner']+sounds

	res=[names,sounds]
	
	for i, x in enumerate(res[0]):
	   b=Button(left, text= res[0][i], height=1, width=10,command=lambda i=i,x=x: openlink(res[1][i])).pack()
	
	return [names,sounds]
		
	
if __name__ == "__main__":

#	lis = ['DODAJ','Tuner','Skala C-dur','Skala Dorycka','Pent. a-mol','Pent. a-dur']
#	com = ['DODAJ','tuner', 'playScale("Skala C-dur")','playScale("Skala Dorycka")', 'playScale("Pent. a-mol")', 'playScale("Pent. a-dur")']
	xxx=load_scales()
	print("***main***")	
	print(xxx[0])
	print(xxx[1])
	print("***end***")
	while True:
		

		
		
		
	

		root.mainloop()
