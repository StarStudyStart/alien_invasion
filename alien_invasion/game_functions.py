import sys
import pygame

from bullet import Bullet
from alien import Alien

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
    elif event.key == pygame.K_q:
        sys.exit()

        
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

def update_bullets(bullets,aliens):
    """更新子弹的位置，并删除消失的子弹"""
    #更新子弹位置
    bullets.update()
    
    #检查是否有子弹击中了外星人，如果集中则删除相应的子弹和外星人
    collisions = pygame.sprite.groupcollide(bullets,aliens,True,True)
    
    #删除消失的子弹
    for bullet in bullets.copy():
        if bullet.rect.bottom <= 0:
            bullets.remove(bullet)
    #print(len(bullets))
    
def get_number_aliens_x(ai_settings,alien_width):
    '''计算每行可容纳的外星人容量'''
    available_space_x = ai_settings.screen_width - (2 * alien_width)
    number_aliens_x = int(available_space_x / (2 * alien_width))
    return number_aliens_x

def get_number_y(ai_settings,alien_height,ship_height):
    '''计算可容纳多少行外星人'''
    available_space_y = ai_settings.screen_height - (3 * alien_height) - ship_height
    number_rows = int(available_space_y / (2 * alien_height))
    return number_rows
    

def create_alien(ai_settings,screen,alien_width,aliens,alien_number,row_number):
    '''创建一行外星人'''
    alien = Alien(ai_settings,screen)
    alien.x = alien_width + 2 * alien_width * alien_number
    alien.rect.x = alien.x
    alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number
    aliens.add(alien)
    
def create_fleet(ai_settings,aliens,screen,ship):
    """创建外星人群"""
    #创建外星人。并计算所需宽度
    #外星人间距为外星人宽度
    alien = Alien(ai_settings,screen)
    alien_width = alien.rect.width
    alien_height = alien.rect.height
    ship_height = ship.rect.height
    
    number_aliens_x = get_number_aliens_x(ai_settings,alien_width)
    number_rows = get_number_y(ai_settings,alien_height,ship_height)
    
    #创建第一行外星人
    for row_number in range(number_rows):
        for alien_number in range(number_aliens_x):
            create_alien(ai_settings,screen,alien_width,aliens,alien_number,row_number)
            
def update_screen(ai_settings,screen,ship,aliens,bullets):
    """更新屏幕的图像，并且切换到新屏幕"""
    screen.fill(ai_settings.bg_color)
    ship.blitme()
    #重绘所有飞船
    aliens.draw(screen)
    #重绘所有子弹
    for bullet in bullets.sprites():
        bullet.draw_bullet()
    
    #重新绘制新屏幕
    pygame.display.flip()
    
def check_fleet_edges(ai_settings,aliens):
    """有外星人到达边缘时采取相应措施"""
    for alien in aliens.sprites():
        if alien.check_edge():
            change_fleet_direction(ai_settings,aliens)
            break
    
def change_fleet_direction(ai_settings,aliens):
    """改变外星人移动方向并下移"""
    for alien in aliens.sprites():
        alien.rect.y += ai_settings.fleet_drop_speed
    ai_settings.fleet_direction *= -1
    
def update_aliens(aliens,ai_settings):
    """检查是否有外星人位于屏幕边缘，并更新外星群中所有外星人的位置"""
    check_fleet_edges(ai_settings,aliens)
    aliens.update()
