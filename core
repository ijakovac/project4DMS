from random import *
from pygame import *
from sys import exit,executable,argv
from os import execl
from time import sleep
polje = []
otvor = []

# 4D MS
# i,q1  4.dimenzija / broj kocki
# j,q2  visina - z os
# k,q3 + l,q4	x,y osi

def arraySusjed(q1,q2,q3,q4): #  vraca array stringova 'q1q2q3q4' susjednih polja
	susjedi = []
	for i in range(q1-1,q1+2):
		for j in range(q2-1,q2+2):
			if abs(i+j-q1-q2)==1 or (i==q1 and j==q2):   #pobrisati za hard verziju s 8 susjeda
				for k in range(q3-1,q3+2):
					for l in range(q4-1,q4+2):
						if i==q1 and j==q2 and k==q3 and l==q4:
							continue
						else:
							susjedi.append(str(i)+str(j)+str(k)+str(l))
	return susjedi

def autogrid(v,m,n,bd,l,p,x,y): #  automatski crta gridove v i m (dim: n*n, border: bd) sa elementima l[x][y] (l = polje)
	grid(v,n,bd)
	gridfill(v,n,bd,l[x][y],p[x][y])
	for i in range(-1,2):
		for j in range(-1,2):
			grid(m[i+1][j+1],n,bd)
			gridfill(m[i+1][j+1],n,bd,l[x+i][y+j],p[x+i][y+j])
			m[i+1][j+1].set_alpha(150)

def autonums(x,y):		#  brojevi uz grid
	fnt = font.Font(None,36)
	for j in range(-1,2):
		if y+j == dim+1 or y+j == 0:
			v = ''
		else:
			v = str(y+j)
		hoff = fnt.size(v)[1]//2
		text = fnt.render(v,1,color[3])
		scrn.blit(text, (20, (j+2)*scrn.get_height()//4-hoff))
	for i in range(-1,2):
		if x+i == dim+1 or x+i == 0:
			v = ''
		else:
			v = str(x+i)
		woff = fnt.size(v)[0]//2
		text = fnt.render(v,1,color[3])
		scrn.blit(text, ((i+2)*scrn.get_width()//4-woff,20))

def boolGranica(q1,q2,q3,q4,n):  # odreduje granice
	if (q1*q2*q3*q4==0)or(q1==n+1)or(q2==n+1)or(q3==n+1)or(q4==n+1):
		return True
	else:
		return False

def chain(mine,p,q1,q2,q3,q4):
	n = str(q1)+str(q2)+str(q3)+str(q4)
	globals()['chainf'].append(n)
	lsusj = arraySusjed(q1,q2,q3,q4)
	for s in lsusj:
		p[int(s[0])][int(s[1])][int(s[2])][int(s[3])]=1
		if mine[int(s[0])][int(s[1])][int(s[2])][int(s[3])] == 0 and (s not in globals()['chainf']):
			chain(polje,otvor,int(s[0]),int(s[1]),int(s[2]),int(s[3]))
		
def click(n,bd,p,mine,loc,but):	#  popunjava polje otvor [0]/[1]/[-3]flag
	x0 = (scrn.get_width()-bigK.get_width())//2+bd
	y0 = (scrn.get_height()-bigK.get_height())//2+bd
	xcord,ycord = 0,0
	s = (bigK.get_width()-2*bd)//n
	for i in range(n):
		if loc[0]>x0+i*s and loc[0]<x0+(i+1)*s:
			for j in range(n):
				if loc[1]>y0+j*s and loc[1]<y0+(j+1)*s:
					xcord = i+1
					ycord = j+1
					break
			break
	if but[0]:
		if not p[xcord][ycord] == 2:
			p[xcord][ycord]=1
			if mine[xcord][ycord] == 0:
				globals()['chainf']=[]
				chain(polje,otvor,x,y,xcord,ycord)
			elif mine[xcord][ycord] == -2:
				gameover()
	elif but[2]:
		if p[xcord][ycord]==2:
			p[xcord][ycord]=0
		else:
			p[xcord][ycord]=2
	
def gameover():  # otvara sva polja, prekida igru play=False
	for i in range(1,dim+1):
		for j in range(1,dim+1):
			for k in range(1,dim+1):
				for l in range(1,dim+1):
					otvor[i][j][k][l] = 1
	refresh()
	gameovertext()
	globals()['play'] = False	

def gameovertext(): # ispisuje transparentni text GAMEOVER
	fnt = font.Font(None,100)
	v = 'GAMEOVER'
	woff = fnt.size(v)[0]//2
	hoff = fnt.size(v)[1]//2
	surf = Surface(fnt.size(v))
	surf.blit(fnt.render(v,1,color[4]),(0,0))
	surf.set_alpha(100)
	scrn.blit(surf,(scrn.get_width()//2-woff,scrn.get_height()//2-hoff))
	display.update()
		
def gen(n,p,value): # generira 4-dimenzionalno polje s n-koordinata + granice (0,n+1)
	for i in range(n+2):
		p.append(list())
		for j in range(n+2):
			p[i].append(list())
			for k in range(n+2):
				p[i][j].append(list())
				for l in range(n+2):
					if boolGranica(i,j,k,l,n):
						p[i][j][k].append(-1)
					else:
						p[i][j][k].append(value)

def grid(g,n,bd):  #crta n*n mrezu na surface-u k sa borderom bd
	d = g.get_width()
	s = (d-2*bd)//n # stranica kvadrata
	for i in range(n):
		for j in range(n):
			draw.rect(g,color[3],(bd+i*s,bd+j*s,s,s),2)

def gridfill(g,n,bd,l,p):  #popunjava grid g (dim: n*n, border: bd) sa elementima l (l = polje[x][y])
	d = g.get_width()
	s = (d-2*bd)//n
	fnt = font.Font(None,s-2)
	for y in range(1,n+1):
		for x in range(1,n+1):
			v = str(l[x][y])
			if v == '-2':
				v = 'M'
			if v == '-1':
				v = 'KRAJ!'
				fnt = font.Font(None,10)
			text = fnt.render(v,1,color[l[x][y]%4+1])
			woff = (s-fnt.size(v)[0])//2
			hoff = (s-fnt.size(v)[1])//2
			if p[x][y] == 1 or p[x][y] == -1:
				g.blit(text,(bd+(x-1)*s+woff,bd+(y-1)*s+hoff))
			elif p[x][y] == 2:
				text = fnt.render('F',1,color[4])
				g.blit(text,(bd+(x-1)*s+woff,bd+(y-1)*s+hoff))

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
			for k in range(1,n+1):
				for l in range(1,n+1):
					if polje[i][j][k][l] == -2:
						continue
					else:
						cnt=0
						for s in arraySusjed(i,j,k,l):
							if polje[int(s[0])][int(s[1])][int(s[2])][int(s[3])] == -2:
								cnt+=1
						polje[i][j][k][l] = cnt
			
def refresh(): # prilikom svake akcije ponovo poziva autogrid(grid+gridfill),autonums
	scrn.fill(color[0])
	bigK = Surface((200,200))
	smlK = list(list(Surface((150,150)) for i in range(3)) for j in range(3))
	autogrid(bigK,smlK,dim,5,polje,otvor,x,y)
	autonums(x,y)
	scrn.blit(bigK,((scrn.get_width()-bigK.get_width())//2,(scrn.get_height()-bigK.get_height())//2))
	for i in range(3):
		for j in range(3):
			if not (i==j==1):
				scrn.blit(smlK[i][j],((i+1)*scrn.get_width()//4-smlK[i][j].get_width()//2,(j+1)*scrn.get_height()//4-smlK[i][j].get_height()//2))
	display.update()


		
def restart(): # restarta igru
	py = executable
	execl(py, py, * argv)
			
def seed(p,n): # generira mine gustoce p u n-koordinatnom 4D polju
	m = round(n*n*n*n*p)
	cnt = 0
	while cnt<m:
		i,j,k,l=randint(1,n),randint(1,n),randint(1,n),randint(1,n)
		if polje[i][j][k][l] == -2:
			continue
		else:
			polje[i][j][k][l] = -2
			cnt+=1
	print 'seedane mine:',cnt

dim = 5
gen(dim,polje,0)
gen(dim,otvor,0)
seed(0.1,dim)
tragac(dim)
chainf = []
play = True

init()                        # ***pocetak inicijalizacije***
display.set_caption('4DMS by Ivan')
scrn = display.set_mode((800,800))
color = [(0,0,0),(255,255,255),(0,0,255),(0,255,0),(255,0,0)] # 0:crna 1:bijela 2:plava 3:zelena 4:crvena
scrn.fill(color[0])
bigK = Surface((200,200))
smlK = list(list(Surface((150,150)) for i in range(3)) for j in range(3))
x = dim//2+1
y = dim//2+1			
refresh()		# ***kraj inicijalizacije***



while True:
	for evt in event.get():
		if evt.type == QUIT:
			quit(); exit();
		if evt.type == KEYUP:
			if evt.key == K_UP and y>1:
				y-=1
			elif evt.key == K_DOWN and y<dim:
				y+=1
			elif evt.key == K_LEFT and x>1:
				x-=1
			elif evt.key == K_RIGHT and x<dim:
				x+=1
			refresh()
			if not play:
				gameovertext()
		if evt.type == MOUSEBUTTONDOWN:
			if not play:
				restart()
			click(dim,5,otvor[x][y],polje[x][y],mouse.get_pos(),mouse.get_pressed())
			print mouse.get_pressed()
			if play:
				refresh()








						
