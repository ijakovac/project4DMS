from random import *
from pygame import *
from sys import exit,executable,argv
from os import execl
from time import sleep
polje = []
otvor = []

# 4D MS
# i,q4  4.dimenzija / broj kocki
# j,q3  visina - z os
# x,q1 + y,q2	x,y osi
# s - string za upis
# play - bool - je li gameover?

def array_susjedi(q4,q3,q2,q1): #  vraca array stringova 'q4q3q2q1' susjednih polja
	susjedi = []
	for i in range(q4-1,q4+2):
		for j in range(q3-1,q3+2):
			if abs(i+j-q4-q3)==1 or (i==q4 and j==q3):   #pobrisati za hard verziju s 8 susjeda
				for y in range(q2-1,q2+2):
					for x in range(q1-1,q1+2):
						if i==q1 and j==q2 and k==q3 and l==q4:
							continue
						else:
							susjedi.append(str(i)+str(j)+str(y)+str(x))
	return susjedi

def auto_grid(g1,g2, n, bd, p1, p2, q4, q3): #  automatski crta gridove g1 i g2 (dim: n*n, border: bd) sa elementima p1[i][j] (p1 = polje) uz uvijet p2 = 1
	grid_gen(g1, n, bd)
	grid_fill(g1, n, bd, p1[q4][q3], p2[q4][q3])
	for i in range(-1,2):
		for j in range(-1,2):
			grid_gen(g2[i+1][j+1], n, bd)
			grid_fill(g2[i+1][j+1], n, bd, p1[q4+i][q3+j], p2[q4+i][q3+j])
			g2[i+1][j+1].set_alpha(150)

def auto_nums(q4,q3):		#  brojevi uz grid
	fnt = font.Font(None,36)
	for j in range(-1,2):
		if q3+j == dim+1 or q3+j == 0:
			s = ''
		else:
			s = str(q3+j)+'q3'
		hoff = fnt.size(s)[1]//2
		text = fnt.render(s,1,color[3])
		scrn.blit(text, (20, (j+2)*scrn.get_height()//4-hoff))
	for i in range(-1,2):
		if q4+i == dim+1 or q4+i == 0:
			s = ''
		else:
			s = str(q4+i)
		woff = fnt.size(s)[0]//2
		text = fnt.render(s,1,color[3])
		scrn.blit(text, ((i+2)*scrn.get_width()//4-woff, 20))

def bool_granica(q4,q3,q2,q1,n):  # odreduje granice
	if (q1*q2*q3*q4==0)or(q1==n+1)or(q2==n+1)or(q3==n+1)or(q4==n+1):
		return True
	else:
		return False

def chain(p1,p2,q4,q3,q2,q1):
	n = str(q4)+str(q3)+str(q2)+str(q1)
	globals()['chainf'].append(n)
	psus = arraySusjed(q4,q3,q2,q1)
	for s in lsus:
		p2[int(s[0])][int(s[1])][int(s[2])][int(s[3])]=1
		if p1[int(s[0])][int(s[1])][int(s[2])][int(s[3])] == 0 and (s not in globals()['chainf']):
			chain(p1,p2,int(s[0]),int(s[1]),int(s[2]),int(s[3]))
		
def click(p1,p2,n,bd,loc,but):	#  popunjava polje otvor [0]/[1]/[-3]flag
	x0 = (scrn.get_width()-bigK.get_width())//2+bd
	y0 = (scrn.get_height()-bigK.get_height())//2+bd
	xcord,ycord = 0,0
	d = (bigK.get_width()-2*bd)//n
	for x in range(n):
		if loc[0]>x0+x*d and loc[0]<x0+(x+1)*d:
			for y in range(n):
				if loc[1]>y0+y*d and loc[1]<y0+(y+1)*d:
					xcord = x+1
					ycord = y+1
					break
			break
	if but[0]:
		if not p2[ycord][xcord] == 2:
			p2[ycord][xcord]=1
			if p1[ycord][xcord] == 0:
				globals()['chainf']=[]
				chain(polje,otvor,i,j,ycord,xcord)
			elif p1[ycord][xcord] == -2:
				gameover()
	elif but[2]:
		if p[ycord][xcord]==2:
			p[ycord][xcord]=0
		else:
			p[ycord][xcord]=2
	
def gameover():  # otvara sva polja, prekida igru play=False
	for i in range(1,dim+1):
		for j in range(1,dim+1):
			for y in range(1,dim+1):
				for x in range(1,dim+1):
					otvor[i][j][y][x] = 1
	refresh()
	gameover_text()
	globals()['play'] = False	

def gameover_text(): # ispisuje transparentni text GAMEOVER
	fnt = font.Font(None,100)
	s = 'GAMEOVER'
	woff = fnt.size(s)[0]//2
	hoff = fnt.size(s)[1]//2
	surf = Surface(fnt.size(s))
	surf.blit(fnt.render(s,1,color[4]),(0,0))
	surf.set_alpha(100)
	scrn.blit(surf,(scrn.get_width()//2-woff,scrn.get_height()//2-hoff))
	display.update()
		
def array_gen(p, n, value): # generira 4-dimenzionalno polje p s n-koordinata + granice (0,n+1)
	for i in range(n+2):
		p.append(list())
		for j in range(n+2):
			p[i].append(list())
			for y in range(n+2):
				p[i][j].append(list())
				for x in range(n+2):
					if bool_granica(i,j,y,x,n):
						p[i][j][y].append(-1)
					else:
						p[i][j][y].append(value)

def grid_gen(g, n, bd):  #crta n*n mrezu na surface-u g sa borderom bd
	d1 = g.get_width() # stranica polja
	d2 = (d1-2*bd)//n # stranica 1 kvadratica
	for y in range(n):
		for x in range(n):
			draw.rect(g,color[3],(bd+x*d2,bd+y*d2,d2,d2),1)

def grid_fill(g, n, bd, p1, p2):  #popunjava grid g (dim: n*n, border: bd) sa elementima p1 (p1 = polje[q4][q3]) uz uvijet p2 = 1
	d1 = g.get_width()
	d2 = (d1-2*bd)//n
	fnt = font.Font(None,d2-2)
	for y in range(1,n+1):
		for x in range(1,n+1):
			s = str(l[y][x])
			if s == '-2':
				s = 'M'
			if s == '-1':
				s = 'KRAJ!'
				fnt = font.Font(None,10)
			text = fnt.render(s,1,color[l[y][x]%4+1])
			woff = (d2-fnt.size(s)[0])//2
			hoff = (d2-fnt.size(s)[1])//2
			if p[y][x] == 1 or p[y][x] == -1:
				g.blit(text,(bd+(x-1)*d2+woff,bd+(y-1)*d2+hoff))
			elif p[y][x] == 2:
				text = fnt.render('F',1,color[4])
				woff = (d2-fnt.size('F')[0])//2
				hoff = (d2-fnt.size('F')[1])//2
				g.blit(text,(bd+(x-1)*d2+woff,bd+(y-1)*d2+hoff))

def tmpprint(n): # print generiranog polja u terminalu
	for i in range(1,n+1):
		print '4D koord:',i
		for j in range(1,n+1):
			print 'sloj kocke:',j
			for k in range(1,n+1):
				print polje[i][j][k][1],polje[i][j][k][2],polje[i][j][k][3] # za n=3 polje

def tragac(n): # vraca broj mina na susjednim poljima
	for i in range(1,n+1):
		for j in range(1,n+1):
			for y in range(1,n+1):
				for x in range(1,n+1):
					if polje[i][j][y][x] == -2:
						continue
					else:
						cnt=0
						for s in arraySusjed(i,j,y,x):
							if polje[int(s[0])][int(s[1])][int(s[2])][int(s[3])] == -2:
								cnt+=1
						polje[i][j][y][x] = cnt
			
def refresh(): # prilikom svake akcije ponovo poziva autogrid(grid+gridfill),autonums
	scrn.fill(color[0])
	bigK = Surface((200,200))
	smlK = list(list(Surface((150,150)) for q3 in range(3)) for q4 in range(3))
	autogrid(bigK,smlK,dim,5,polje,otvor,i,j)
	autonums(i,j)
	scrn.blit(bigK,((scrn.get_width()-bigK.get_width())//2,(scrn.get_height()-bigK.get_height())//2))
	for i in range(3):
		for j in range(3):
			if not (i==j==1):
				scrn.blit(smlK[i][j],((i+1)*scrn.get_width()//4-smlK[i][j].get_width()//2,(j+1)*scrn.get_height()//4-smlK[i][j].get_height()//2))
	display.update()


		
def restart(): # restarta igru
	py = executable
	execl(py, py, * argv)
			
def mine_gen(p,n): # generira mine gustoce p u n-koordinatnom 4D polju
	m = round(n*n*n*n*p)
	cnt = 0
	while cnt<m:
		i,j,y,x=randint(1,n),randint(1,n),randint(1,n),randint(1,n)
		if polje[i][j][y][x] == -2:
			continue
		else:
			polje[i][j][y][x] = -2
			cnt+=1
	print 'seedane mine:',cnt

dim = 5
array_gen(dim,polje,0)
array_gen(dim,otvor,0)
mine_gen(0.1,dim)
tragac(dim)
chainf = []
play = True

init()                        # ***pocetak inicijalizacije***
display.set_caption('4DMS by Ivan')
scrn = display.set_mode((800,800))
color = [(0,0,0),(255,255,255),(0,0,255),(0,255,0),(255,0,0)] # 0:crna 1:bijela 2:plava 3:zelena 4:crvena
scrn.fill(color[0])
bigK = Surface((200,200))
smlK = list(list(Surface((150,150)) for q3 in range(3)) for q4 in range(3))
i = dim//2+1
j = dim//2+1			
refresh()		# ***kraj inicijalizacije***



while True:
	for evt in event.get():
		if evt.type == QUIT:
			quit(); exit();
		if evt.type == KEYUP:
			if evt.key == K_UP and j>1:
				j-=1
			elif evt.key == K_DOWN and j<dim:
				j+=1
			elif evt.key == K_LEFT and i>1:
				i-=1
			elif evt.key == K_RIGHT and i<dim:
				i+=1
			refresh()
			if not play:
				gameovertext()
		if evt.type == MOUSEBUTTONDOWN:
			if not play:
				restart()
			click(dim,5,otvor[i][j],polje[i][j],mouse.get_pos(),mouse.get_pressed())
			print mouse.get_pressed()
			if play:
				refresh()








						
