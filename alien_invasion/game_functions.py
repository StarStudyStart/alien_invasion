import sys
import pygame

from bullet import Bullet

def fire_bullet(ai_settings,screen,ship,bullets):
    """如果还为达到上限就创建一颗子弹"""
    if len(bullets) < 3:
        new_bullet = Bullet(ai_settings,screen,ship)
        bullets.add(new_bullet)
    

def check_keydown_events(event,ai_settings,screen,ship,bullets):
    '''响应按键'''
    if event.key == pygame.K_RIGHT:
        #向右移动飞船
        ship.moving_right = True
    elif event.key == pygame.K_LEFT:
        #向左移动飞船
        ship.moving_left = True
    elif event.key == pygame.K_SPACE:
        #创建一个子弹并且加入bullets中
        fire_bullet(ai_settings,screen,ship,bullets)

        
def check_keyup_events(event,ship):
    '''响应松开'''
    if event.key == pygame.K_RIGHT:
        ship.moving_right = False
    elif event.key == pygame.K_LEFT:
        ship.moving_left = False
    
def check_events(ai_settings,screen,ship,bullets):
    """响应按键和鼠标事件"""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            check_keydown_events(event,ai_settings,screen,ship,bullets)
        elif event.type == pygame.KEYUP:
            check_keyup_events(event,ship)

def update_bullets(bullets):
    """更新子弹的位置，并删除消失的子弹"""
    #更新子弹位置
    bullets.update()
    #删除消失的子弹
    for bullet in bullets.copy():
        if bullet.rect.bottom <= 0:
            bullets.remove(bullet)
    #print(len(bullets))
            
def update_screen(ai_settings,screen,ship,bullets):
    """更新屏幕的图像，并且切换到新屏幕"""
    screen.fill(ai_settings.bg_color)
    ship.blitme()
    #重绘所有子弹
    for bullet in bullets.sprites():
        bullet.draw_bullet()
    
    #重新绘制新屏幕
    pygame.display.flip()
