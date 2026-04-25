import time

import pygame

WIDTH = 800
HEIGHT = 600

def narysuj_piksel(x,y):
    screen.set_at((x, y), (255, 255, 255))

def narysuj_kwadrat(x,y):
    pygame.draw.rect(screen, (255, 255, 255), (x, y - 10, 20, 20))

def wyswietl():
    pygame.display.flip()

def wymarz():
    screen.fill((0, 0, 0))
    pygame.display.flip()

# pygame.init() uruchamia wszystkie moduły pygame (dźwięk, ekran, czcionki itd.)
# Trzeba to wywołać przed użyciem czegokolwiek z pygame
pygame.init()

# set_mode() tworzy okno o podanym rozmiarze (szerokość, wysokość) w pikselach
# Zwraca "surface" — to jest nasz ekran, na którym rysujemy
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pixel")

# fill() wypełnia cały ekran jednym kolorem (R, G, B) — tutaj czarnym
screen.fill((0, 0, 0))

# set_at() ustawia kolor JEDNEGO piksela na pozycji (x, y)
# To jest najniższy poziom rysowania — dosłownie jeden punkt na ekranie
cx = WIDTH // 2
cy = HEIGHT // 2
# screen.set_at((cx, cy), (255, 255, 255))

# flip() "przerzuca" to co narysowaliśmy na ekran
# Pygame rysuje najpierw w pamięci (buforze), a flip() pokazuje wynik
# Bez flip() nic nie zobaczymy — ekran pozostanie pusty
pygame.display.flip()

# Pętla gry — program działa dopóki nie zamkniemy okna
# pygame.event.get() sprawdza co się dzieje (kliknięcia, klawisze, zamknięcie)
# Bez tej pętli okno by się otworzyło i natychmiast zamknęło
running = True
x = cx
y = cy

# -----------------------------------------------------------------------

idziemy_w_prawo = True

while running:
    
    narysuj_kwadrat(x, y)
    wyswietl()
    
    if idziemy_w_prawo:
        x = x + 1
    else:
        x = x - 1
    
    if x == 800-10:
        idziemy_w_prawo = False
    elif x == 0:
        idziemy_w_prawo = True
        
    time.sleep(0.003)
    wymarz()
        
    print(x+1)
    

# ----------------------------------------------------------------------

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

# quit() zamyka pygame i zwalnia zasoby (pamięć, okno)
pygame.quit()
