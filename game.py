import pygame
from network import Network
from random import randint

WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)

class Cube:
    width = height = 20


    def __init__(self, startx, starty):
        self.x = startx
        self.y = starty
        self.color = GREEN
        self.cubeRect = pygame.Rect(self.x, self.y, self.width, self.height)


    def draw(self, g):
        pygame.draw.rect(g, self.color, (self.x, self.y, self.width, self.height), 0)



class Player:
    width = height = 50


    def __init__(self, startx, starty, color=RED):
        self.x = startx
        self.y = starty
        self.velocity = 3
        self.color = color
        self.colected = 0
        self.playerRect = pygame.Rect(self.x, self.y, self.width, self.height)


    def draw(self, g):
        self.updateRect()
        pygame.draw.rect(g, self.color, self.playerRect, 0)


    def move(self, dirn):
        """
        :param dirn: 0 - 3 (right, left, up, down)
        :return: None
        """

        if dirn == 0:
            self.x += self.velocity
        elif dirn == 1:
            self.x -= self.velocity
        elif dirn == 2:
            self.y -= self.velocity
        else:
            self.y += self.velocity


    def updateRect(self):
        self.playerRect = pygame.Rect(self.x, self.y, self.width, self.height)
    

    def touch(self, cube):
        if self.playerRect.colliderect(cube.cubeRect):
            return True
        return False


class Game:


    def __init__(self, w, h):
        self.net = Network()
        self.width = w
        self.height = h
        self.player = Player(50, 50)
        self.player2 = Player(100, 100, BLUE)
        self.canvas = Canvas(self.width, self.height, "Come Come")
        self.cube = Cube(600, 600)


    def run(self):
        clock = pygame.time.Clock()
        run = True
        cubeExist = True
        while run:
            clock.tick(60)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False

                if event.type == pygame.K_ESCAPE:
                    run = False

            keys = pygame.key.get_pressed()

            if keys[pygame.K_RIGHT]:
                if self.player.x <= self.width - self.player.velocity:
                    self.player.move(0)

            if keys[pygame.K_LEFT]:
                if self.player.x >= self.player.velocity:
                    self.player.move(1)

            if keys[pygame.K_UP]:
                if self.player.y >= self.player.velocity:
                    self.player.move(2)

            if keys[pygame.K_DOWN]:
                if self.player.y <= self.height - self.player.velocity:
                    self.player.move(3)

            # Send Network Stuff
            self.player2.x, self.player2.y, newCubeX, newCubeY = self.parse_data(self.send_data(cubeExist, False))
                
            # Update Canvas
            self.canvas.draw_background()
            self.player.draw(self.canvas.get_canvas())
            self.player2.draw(self.canvas.get_canvas())
            if cubeExist:
                self.cube.draw(self.canvas.get_canvas())
            self.canvas.update()

            if not cubeExist:
                cubeExist = True
                self.cube = Cube(newCubeX, newCubeY)
                print(newCubeX, newCubeY)

            if cubeExist:
                if self.player.touch(self.cube):
                    self.player.colected += 1
                    cubeExist = False
                elif self.player2.touch(self.cube):
                    self.player2.colected += 1
                    cubeExist = False
            
            self.check_winner()

        pygame.quit()


    def send_data(self, cubeExist, winner):
        """
        Send position to server
        :return: None
        """
        if winner:
            self.net.send('WINNER')
            return True
        else:
            cubeEaten = '2' if cubeExist else '3'
            data = str(self.net.id) + ":" + str(self.player.x) + "," + str(self.player.y) + '/' + cubeEaten + ':' + str(self.cube.x) + ',' + str(self.cube.y)
            reply = self.net.send(data)
            return reply


    @staticmethod
    def parse_data(data):
        try:
            if data == 'WINNER':
                return True

            playerData = data.split('/')[0]
            playerPos = playerData.split(":")[1].split(",")
            cubeData = data.split('/')[1]
            cubePos = cubeData.split(':')[1].split(',')
            return int(playerPos[0]), int(playerPos[1]), int(cubePos[0]), int(cubePos[1])
        except Exception as err:
            print('Error on client side!', err)
            return 0, 0, 0, 0
    

    def check_winner(self):
        if self.player.colected == 5:
            winner = self.parse_data(self.send_data(False, True))
            if winner:
                print('You win!')
                exit()



class Canvas:


    def __init__(self, w, h, name="None"):
        self.width = w
        self.height = h
        self.screen = pygame.display.set_mode((w,h))
        pygame.display.set_caption(name)


    @staticmethod
    def update():
        pygame.display.update()


    def draw_text(self, text, size, x, y):
        pygame.font.init()
        font = pygame.font.SysFont("comicsans", size)
        render = font.render(text, 1, (0, 0, 0))

        self.screen.draw(render, (x,y))


    def get_canvas(self):
        return self.screen


    def draw_background(self):
        self.screen.fill(WHITE)



if __name__ == "__main__":
    g = Game(800, 800)
    g.run()
