import math
import random
import time
import arcade


class SpaceCraft(arcade.Sprite):
    def __init__(self, w , h):
        super().__init__(":resources:images/space_shooter/playerShip1_blue.png")
        self.width = 50
        self.height = 50
        self.center_x = w // 2
        self.center_y = 50
        self.angle = 0
        self.change_angle = 0
        self.bullet_list = []
        self.speed = 5
        self.point = 0
        self.count = 3

    def rotate(self):
        self.angle += self.change_angle * self.speed

    def fire(self):
        self.bullet_list.append(Bullet(self))
        arcade.play_sound(arcade.sound.Sound(":resources:sounds/hurt5.wav"), 1.0, 0.0, False, 1.0)
    
    def score(self):
        self.point += 1
        arcade.play_sound(arcade.sound.Sound(":resources:sounds/explosion1.wav"), 1.0, 0.0, False, 1.0)
        
class Lives(arcade.Sprite):
    def __init__(self , x , y):
        super().__init__("live.png")
        self.width = 20
        self.height = 20
        self.center_x = x
        self.center_y = y
        
class Bullet(arcade.Sprite):
    def __init__(self, host):
        super().__init__("laserBlue01.png")
        self.speed = 5
        self.angle = host.angle
        self.center_x = host.center_x
        self.center_y = host.center_y

    def move(self):
        angle_rad = math.radians(self.angle)
        self.center_x -= self.speed * math.sin(angle_rad)
        self.center_y += self.speed * math.cos(angle_rad)

class Enemy(arcade.Sprite):
    def __init__(self, w, h , s):
        super().__init__(":resources:images/space_shooter/playerShip1_orange.png")
        self.speed = s
        self.center_x = random.randint(0 , w - 5)
        self.center_y = h
        self.angle = 180
        self.width = 48
        self.height = 48


    def move(self):
        self.center_y -= self.speed
    

        


class Game(arcade.Window):
    def __init__(self):
        self.w = 700
        self.h = 550
        super().__init__(width=self.w , height=self.h , title="Space Craft")
        arcade.set_background_color(arcade.color.BLACK)
        self.background_image = arcade.load_texture(":resources:images/backgrounds/stars.png")
        self.sp = SpaceCraft(self.w , self.h)
        self.enemy_list = []
        self.start = time.time()
        self.live_list = []
        self.STS = time.time()
        self.x = 0
    
    



        for i in range(self.sp.count):
            self.live_list.append(Lives(30+self.x ,30))
            self.x += 25

    def on_draw(self):
        arcade.start_render()
        arcade.draw_lrwh_rectangle_textured(0, 0, self.w, self.h , self.background_image)
        self.sp.draw()
        

        for i in range(len(self.sp.bullet_list)):
            self.sp.bullet_list[i].draw()

        for i in range(len(self.enemy_list)):
            self.enemy_list[i].draw()
        
        for i in range(len(self.live_list)):
            self.live_list[i].draw()
        
                   


        arcade.draw_text("Score:", 550 , 30, arcade.color.WHITE)
        arcade.draw_text(str(self.sp.point), 600,30, arcade.color.WHITE)

        if len(self.live_list) == 0:
            arcade.draw_rectangle_filled(0, 0, self.width*4, self.height*4, arcade.color.BLACK)
            arcade.draw_text("Game Over!" , self.width // 2 - 160 ,self.height // 2, arcade.color.RED, bold=True, font_size=40)
            arcade.finish_render()
            time.sleep(0.5)



    def on_update(self, delta_time):
        self.sp.rotate()
        self.end = time.time()
        self.ETS = time.time()
        self.s = 2
       

        for i in range(len(self.sp.bullet_list)):
            self.sp.bullet_list[i].move()
        
        if self.end - self.start > random.randint(2,5):
            self.enemy_list.append(Enemy(self.w , self.h, self.s))
            self.start = time.time()

        for i in range(len(self.enemy_list)):
            if self.ETS - self.STS > 7:
                self.s += random.randint(1,5)
                self.STS = time.time()
            self.enemy_list[i].move()


        for i in self.enemy_list:
            for j in self.sp.bullet_list:
                if arcade.check_for_collision(i,j):
                    self.sp.score()
                    self.enemy_list.remove(i)
                    self.sp.bullet_list.remove(j)

        for e in self.enemy_list:
            if e.center_y < -1:
                self.enemy_list.remove(e)
                self.live_list.pop(-1)

       

                



    def on_key_press(self, symbol, modifiers):
        match symbol:
            case arcade.key.RIGHT:
                self.sp.change_angle = -1
            case arcade.key.LEFT:
                self.sp.change_angle = 1     
            case arcade.key.SPACE:
                self.sp.fire()

    def on_key_release(self, symbol, modifiers):
        self.sp.change_angle = 0 

game = Game()
arcade.run()

