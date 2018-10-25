import sys
import pygame
from time import sleep

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

def update_bullets(ai_settings,screen,ship,bullets,aliens):
    """更新子弹的位置，并删除消失的子弹"""
    #更新子弹位置
    bullets.update()

    #删除消失的子弹
    for bullet in bullets.copy():
        if bullet.rect.bottom <= 0:
            bullets.remove(bullet)
    #print(len(bullets))
    check_bullet_alien_collisions(ai_settings,aliens,screen,ship,bullets)
    
        
def check_bullet_alien_collisions(ai_settings,aliens,screen,ship,bullets):
    """响应子弹和外星人碰撞"""
    #检查是否有子弹击中了外星人，如果集中则删除相应的子弹和外星人
    collisions = pygame.sprite.groupcollide(bullets,aliens,True,True)
    if len(aliens) == 0:
        #清空子弹并重建外星人
        bullets.empty()
        create_fleet(ai_settings,aliens,screen,ship)
    
def update_screen(ai_settings,screen,ship,aliens,bullets,stats, play_button):
    """更新屏幕的图像，并且切换到新屏幕"""
    screen.fill(ai_settings.bg_color)
     #重绘所有飞船，外星人
    ship.blitme()
    aliens.draw(screen)
    
    #重绘所有子弹
    for bullet in bullets.sprites():
        bullet.draw_bullet()
        
    #如果游戏处于非活动状态，则绘制play按钮
    if not stats.game_active:
        play_button.draw_button()
        
    #重新绘制新屏幕
    pygame.display.flip()
    
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
    
    #创建多行外星人群
    for row_number in range(number_rows):
        for alien_number in range(number_aliens_x):
            create_alien(ai_settings,screen,alien_width,aliens,alien_number,row_number)
    
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
    
def ship_hit(ai_settings,stats,screen,ship,bullets,aliens):
    """响应被外星人撞到飞船"""
    #ship_left 减1
    if stats.ships_left > 0:
        
        stats.ships_left -= 1
    
        #清空外星人和子弹列表
        aliens.empty()
        bullets.empty()
    
        #重新创建外星人群,并将飞船放置到中间位置
        create_fleet(ai_settings,aliens,screen,ship)
        ship.center_ship()
    
        sleep(0.5)
    else:
        stats.game_active = False

def check_aliens_bottom(ai_settings,screen,stats,ship,aliens,bullets):
    """检查是否有外星人到达了屏幕底端"""
    screen_rect = screen.get_rect()
    for alien in aliens.sprites():
        if alien.rect.bottom >= screen_rect.bottom:
            #像撞击飞船一样处理
            ship_hit(ai_settings,stats,screen,ship,bullets,aliens)
            break

def update_aliens(ai_settings,stats,screen,ship,bullets,aliens):
    """检查是否有外星人位于屏幕边缘，并更新外星群中所有外星人的位置"""
    check_fleet_edges(ai_settings,aliens)
    aliens.update()
    #检查外星人与飞船之间的碰撞
    if pygame.sprite.spritecollideany(ship,aliens):
        #print("Ship hit!!!")
        ship_hit(ai_settings,stats,screen,ship,bullets,aliens)
    #检查是否有外星人到达屏幕底端
    check_aliens_bottom(ai_settings,screen,stats,ship,aliens,bullets)
        
