import pygame
import random
import os
from pygame import mixer
from spritesheet import SpriteSheet
from dusman import Dusman

mixer.init()
pygame.init()

ekran_genislik=400
ekran_yukseklik=600

ekran=pygame.display.set_mode((ekran_genislik,ekran_yukseklik))
pygame.display.set_caption('jumpjump')

sure=pygame.time.Clock()
kare_hizi=60

pygame.mixer.music.load("gamesong.mp3")
pygame.mixer.music.set_volume(0.6)
pygame.mixer.music.play(-1,7.0)
jump_fx=pygame.mixer.Sound("jump.mp3")
jump_fx.set_volume(0.5)
öldün_fx=pygame.mixer.Sound("öldün.mp3")
öldün_fx.set_volume(0.5)

yercekimi=1
max_basamak=10
kaydirmak=200
kaydir=0
arkaplan_kaydir=0
oyun_bitis=False
puan=0
sayaç=0

if os.path.exists('score.txt'):

    with open('score.txt','r') as file:
        yuksek_score=int(file.read()) 
else:

    yuksek_score=0


WHITE=(255,255,255)
BLACK=(0,0,0)
PANEL=(130,90,180)

font_küçük=pygame.font.SysFont('Lucida Sans',20)
font_büyük=pygame.font.SysFont('Lucida Sans',24)

karakter_resmi=pygame.image.load("spiderman.png").convert_alpha()
arkaplan_resmi=pygame.image.load("arkaplan.png").convert_alpha()
basamak_resmi=pygame.image.load("basamak.png").convert_alpha()
dusman_resmi=pygame.image.load("bird.png").convert_alpha()
helikopter=SpriteSheet(dusman_resmi)


def çiz_yazı(text,font,text_col,x,y):
    resim=font.render(text,True,text_col)
    ekran.blit(resim,(x,y))


def çiz_panel():
    pygame.draw.rect(ekran,PANEL,(0,0,ekran_genislik,30))
    pygame.draw.line(ekran,WHITE,(0,30),(ekran_genislik,30),2)
    çiz_yazı('PUAN: ' + str(puan),font_küçük,WHITE,10,10)



def arkaplan_çizimi(arkaplan_kaydir):
    ekran.blit(arkaplan_resmi,(0,0+arkaplan_kaydir))
    ekran.blit(arkaplan_resmi,(0,-600 +arkaplan_kaydir))


class Oyuncu():
    def __init__(self,x,y):

        self.image=pygame.transform.scale(karakter_resmi,(50,50))
        self.genislik=40
        self.yukseklik=25
        self.rect=pygame.Rect(0,0,self.genislik,self.yukseklik)
        self.rect.center=(x,y)
        self.hiz_y=0
        self.çevir=False
    

    def hareket(self):

        delta_x=0
        delta_y=0
        kaydir=0

        anahtar=pygame.key.get_pressed()
        if anahtar[pygame.K_a]:
            delta_x  = -10
            self.çevir=True

        if anahtar[pygame.K_d]:
            delta_x = 10
            self.çevir=False

        self.hiz_y += yercekimi
        delta_y += self.hiz_y

        if self.rect.left + delta_x <0:
            delta_x = 0-self.rect.left

        if self.rect.right +delta_x > ekran_genislik:
            delta_x = ekran_genislik-self.rect.right


        for basamak in basamak_grubu:
            if basamak.rect.colliderect(self.rect.x,self.rect.y + delta_y, self.genislik,self.yukseklik):
                if self.rect.bottom < basamak.rect.centery:
                    if self.hiz_y > 0:
                        self.rect.bottom = basamak.rect.top
                        delta_y=0
                        self.hiz_y=-20
                        jump_fx.play()





        if self.rect.top<=kaydirmak:
           #eğer karakter zıplıyorsa
            if self.hiz_y<0:
                kaydir=-delta_y



        self.rect.x +=delta_x
        self.rect.y +=delta_y + kaydir 

        self.mask = pygame.mask.from_surface(self.image)

        return kaydir



    def çiz(self):
        ekran.blit(pygame.transform.flip(self.image,self.çevir,False),(self.rect.x-12,self.rect.y-5))
        

class Basamak(pygame.sprite.Sprite):
    def __init__(self,x,y,genislik,hareket) :
        pygame.sprite.Sprite.__init__(self)
        self.image=pygame.transform.scale(basamak_resmi,(genislik+7,50))
        self.moving=hareket
        self.hareket_merkezi=random.randint(0,50)
        self.yon=random.choice([-1,1])
        self.hiz=random.randint(1,2)
        self.rect=self.image.get_rect()
        self.rect.x = x
        self.rect.y = y


    def update(self,kaydir):

        if self.moving==True:
            self.hareket_merkezi+=1
            self.rect.x+=self.yon * self.hiz

        if self.hareket_merkezi >= 100 or self.rect.left < 0 or self.rect.right > ekran_genislik:
            self.yon *= -1
            self.hareket_merkezi = 0

        self.rect.y+=kaydir

        if self.rect.top > ekran_yukseklik:
            self.kill()


    
zıpla=Oyuncu(ekran_genislik//2,ekran_yukseklik-150)

basamak_grubu=pygame.sprite.Group()
dusman_grubu=pygame.sprite.Group()

basamakk=Basamak(ekran_genislik//2-50,ekran_yukseklik-50,100,False)
basamak_grubu.add(basamakk)



run=True
while run:

    sure.tick(kare_hizi)


    if oyun_bitis==False:
        
        kaydir=zıpla.hareket()

        arkaplan_kaydir+=kaydir

        if arkaplan_kaydir>=600:
            arkaplan_kaydir=600
        arkaplan_çizimi(arkaplan_kaydir)
        

        if len(basamak_grubu)<max_basamak:
            basamak_genislik=random.randint(40,60)
            basamak_x=random.randint(0,ekran_genislik-basamak_genislik)
            basamak_y=basamakk.rect.y - random.randint(80,120)
            basamak_tip=random.randint(1,2)
            if basamak_tip==1 and puan > 600:
                basamak_hareket=True
            else:
                basamak_hareket=False

            basamakk=Basamak(basamak_x,basamak_y,basamak_genislik,basamak_hareket)
            basamak_grubu.add(basamakk)

        
        
        basamak_grubu.update(kaydir)
        
        if len(dusman_grubu) == 0 and puan > 1500:
            dusman=Dusman(ekran_genislik,100,helikopter,1.5)
            dusman_grubu.add(dusman)

        dusman_grubu.update(kaydir,ekran_genislik)

        if kaydir>0:
            puan+=kaydir

        pygame.draw.line(ekran,WHITE,(0,puan - yuksek_score +kaydirmak),(ekran_genislik,puan - yuksek_score + kaydirmak),3)
        çiz_yazı('YÜKSEK SKOR',font_küçük,WHITE,ekran_genislik-130, puan - yuksek_score+kaydirmak)

        basamak_grubu.draw(ekran)
        dusman_grubu.draw(ekran)
        zıpla.çiz()


        çiz_panel()


        if zıpla.rect.top> ekran_yukseklik:
            oyun_bitis=True
            öldün_fx.play()

        if pygame.sprite.spritecollide(zıpla,dusman_grubu,False):
            if pygame.sprite.spritecollide(zıpla,dusman_grubu,False,pygame.sprite.collide_mask):
                oyun_bitis=True
                öldün_fx.play()

    else:
        if sayaç<ekran_genislik:
            sayaç+=5
            for y in range(0,6,2):
               pygame.draw.rect(ekran,BLACK,(0,y*100,sayaç,100))
               pygame.draw.rect(ekran,BLACK,(ekran_genislik-sayaç,(y+1)*100,ekran_genislik,100))

        else:

            çiz_yazı('OYUN BİTTİ',font_büyük,WHITE,130,200)
            çiz_yazı('PUAN: '+ str(puan),font_büyük,WHITE,130,250)
            çiz_yazı('TEKRAR OYNAMAK İÇİN SPACE',font_büyük,WHITE,40,300)
            çiz_yazı('EN YUKSEK SKOR: ' + str(yuksek_score),font_büyük,WHITE,10,10)

            if puan > yuksek_score:
                yuksek_score=puan
                with open('score.txt','w') as file:
                    file.write(str(yuksek_score))
                    
            key=pygame.key.get_pressed()
            if key[pygame.K_SPACE]:
                oyun_bitis=False
                puan=0
                kaydir=0
                sayaç=0
                zıpla.rect.center=(ekran_genislik//2,ekran_yukseklik-150)
                dusman_grubu.empty()
                basamak_grubu.empty()
                basamakk=Basamak(ekran_genislik//2-50,ekran_yukseklik-50,100,False)
                basamak_grubu.add(basamakk)


    

    


    for olay in pygame.event.get():
        if olay.type==pygame.QUIT:
            if puan > yuksek_score:
                yuksek_score=puan
                with open('score.txt','w') as file:
                    file.write(str(yuksek_score))
            run=False

    pygame.display.update()

pygame.quit()