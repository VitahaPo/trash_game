__author__ = 'Vitaha'
from livewires import games, color
import random

#init screen
games.init(screen_width = 640, screen_height = 480, fps = 50)

class Man(games.Sprite):
    """man - trash catcher """
    image = games.load_image('man.bmp')
    cycle = 20
    score = 0

    def __init__(self):
        """init man and score text"""
        super(Man, self).__init__(image = Man.image,
                                  x = games.mouse.x,
                                  bottom = games.screen.height)
        self.score = games.Text(value = Man.score,
                                size = 25,
                                color = color.purple,
                                top = 5,
                                right = games.screen.width - 10)
        games.screen.add(self.score)
        self.time_til_drop = 0

    def update(self):
        #game status
        if 0 <= Man.score < 400:
            self.check_drop()
        elif Man.score >= 400:
            self.end_game('You WIN')
        else:
           self.end_game('GAME OVER')

        #gorizontal moving of man
        self.x = games.mouse.x
        if self.left < 0:
            self.left = 0
        if self.right > games.screen.width:
            self.right = games.screen.width
        self.check_catch()
        self.difficulty()


    def check_catch(self):
        """checking for catch"""
        for trash in self.overlapping_sprites:
            if trash.image in Trash.TRASH_IMAGE[:3]:
                Man.score -= 10
                self.score.value = Man.score
                self.score.right = games.screen.width - 10
            else:
                Man.score += 10
                self.score.value = Man.score
                self.score.right = games.screen.width - 10
            trash.handle_catch()

    def difficulty(self):
        """difficulty change"""
        if Man.score/Man.cycle == 1:
            Trash.speed += 0.3
            Man.cycle += 20

    def check_drop(self):
        """drop trash"""
        if self.time_til_drop > 0:
            self.time_til_drop -= 1
        else:
            new_trash = Trash(x = random.randint(40, 600))
            games.screen.add(new_trash)
            self.time_til_drop = int(new_trash.height * 3 / Trash.speed) + 1

    def end_game(self, text):
        """start ending game"""
        end_message = games.Message(value = text,
                                    size = 90,
                                    color = color.purple,
                                    x = games.screen.width/2,
                                    y = games.screen.height/2,
                                    lifetime = 5 * games.screen.fps,
                                    after_death = games.screen.quit)
        games.screen.add(end_message)

class Trash(games.Sprite):
    """trash class"""
    TRASH_IMAGE = []
    TRASH_IMAGE.append(games.load_image('drug.bmp'))
    TRASH_IMAGE.append(games.load_image('drunk.bmp'))
    TRASH_IMAGE.append(games.load_image('smoke.bmp'))
    TRASH_IMAGE.append(games.load_image('apple.bmp'))
    speed = 1

    def __init__(self, x, y = 20):
        """init trash"""
        super(Trash, self).__init__(image = Trash.TRASH_IMAGE[random.randrange(4)],
                                    x = x, y = y,
                                    dy = Trash.speed)

    def update(self):
        """check for Trash position"""
        if self.bottom > games.screen.height:
            self.destroy()

    def handle_catch(self):
        """destroy handeled trash"""
        self.destroy()



def main():
    """main prog"""
    #background
    wall_image = games.load_image('background.jpg', transparent = False)
    games.screen.background = wall_image

    the_man = Man()
    games.screen.add(the_man)

    games.mouse.is_visible = False
    games.screen.event_grab = True
    games.screen.mainloop()

main()