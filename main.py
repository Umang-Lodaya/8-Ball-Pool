import pygame
import sys
import math
import pymunk
import pymunk.pygame_util

from constants import *
from cue import Cue


class Game:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("8 Ball Pool")
        self.SCREEN = pygame.display.set_mode((WIDTH, HEIGHT + BOTTOM_PANEL))
        self.CLOCK = pygame.time.Clock()
        self.SPACE = pymunk.Space()
        self.STATIC_BODY = self.SPACE.static_body
        self.DRAW_OPTIONS = pymunk.pygame_util.DrawOptions(self.SCREEN)

        self.TAKING_SHOT = True
        self.POWERING_UP = False
        self.FORCE = 2000
        self.FORCE_DIRECTION = 1
        self.POTTED_BALLS = []
        self.CUE_BALL_POTTED = False

    def createBall(self, radius, position) -> pymunk.Shape:
        body = pymunk.Body()
        body.position = position
        shape = pymunk.Circle(body, radius)
        shape.mass = BALL_MASS
        shape.elasticity = ELASTICITY

        pivot = pymunk.PivotJoint(self.STATIC_BODY, body, (0, 0), (0, 0))
        pivot.max_bias = MAX_BIAS
        pivot.max_force = MAX_FORCE

        self.SPACE.add(body, shape, pivot)
        return shape

    def createCushion(self, poly_dims):
        body = pymunk.Body(body_type=pymunk.Body.STATIC)
        body.position = (0, 0)
        shape = pymunk.Poly(body, poly_dims)
        shape.elasticity = ELASTICITY

        self.SPACE.add(body, shape)

    def run(self):
        TABLE_IMAGE = pygame.image.load("assets/images/table.png").convert_alpha()
        CUE_IMAGE = pygame.image.load("assets/images/cue.png").convert_alpha()

        BALL_IMAGES = []
        for i in range(1, 17):
            image = pygame.image.load(f"assets/images/ball_{i}.png").convert_alpha()
            BALL_IMAGES.append(image)

        BALLS = []
        for col in range(5):
            for row in range(5 - col):
                pos = (
                    250 + (col * (BALL_RADIUS * 2 + 1)),
                    267 + (row * (BALL_RADIUS * 2 + 1)) + (col * BALL_RADIUS),
                )
                newBall = self.createBall(BALL_RADIUS, pos)
                BALLS.append(newBall)

        cueBall = self.createBall(BALL_RADIUS, (888, HEIGHT // 2))
        BALLS.append(cueBall)

        for cushion in CUSHIONS:
            self.createCushion(cushion)

        cue = Cue(CUE_IMAGE, BALLS[-1].body.position)

        POWER_BAR = pygame.Surface((10, 20))
        POWER_BAR.fill("red")

        while True:
            self.SPACE.step(1 / FPS)
            self.CLOCK.tick(FPS)
            self.SCREEN.fill("black")
            self.SCREEN.blit(TABLE_IMAGE, (0, 0))

            for i, ball in enumerate(BALLS):
                for pocket in POCKETS:
                    BALL_DISTS = [abs(ball.body.position[0] - pocket[0]), abs(ball.body.position[1] - pocket[1])]
                    BALL_DIST = math.sqrt(BALL_DISTS[0]**2 + BALL_DISTS[1]**2)
                    if BALL_DIST <= POCKET_RADIUS:
                        if i == len(BALLS) - 1:
                            self.CUE_BALL_POTTED = True
                            ball.body.position = (-100, -100)
                            ball.body.velocity = (0, 0)
                        else:
                            self.SPACE.remove(ball.body)
                            BALLS.remove(ball)
                            self.POTTED_BALLS.append(BALL_IMAGES[i])
                            BALL_IMAGES.pop(i)
            
            # print(self.POTTED_BALLS)

            for i, ball in enumerate(BALLS):
                x, y = ball.body.position
                self.SCREEN.blit(BALL_IMAGES[i], (x - ball.radius, y - ball.radius))

            self.TAKING_SHOT = True
            for ball in BALLS:
                if ball.body.velocity[0] or ball.body.velocity[1]:
                    self.TAKING_SHOT = False
                    break

            if self.TAKING_SHOT:
                if self.CUE_BALL_POTTED:
                    BALLS[-1].body.position = (888, HEIGHT // 2)
                    self.CUE_BALL_POTTED = False

                MOUSE_POS = pygame.mouse.get_pos()
                cue.rect.center = BALLS[-1].body.position
                DIST = [
                    BALLS[-1].body.position[0] - MOUSE_POS[0],
                    -1 * (BALLS[-1].body.position[1] - MOUSE_POS[1]),
                ]

                cue_angle = math.degrees(math.atan2(*DIST[::-1]))
                cue.update(cue_angle)
                cue.draw(self.SCREEN)
                pygame.draw.line(
                    self.SCREEN,
                    "white",
                    BALLS[-1].body.position,
                    MOUSE_POS,
                    CUE_LINE_WIDTH,
                )

            if self.POWERING_UP:
                self.FORCE += 100 * self.FORCE_DIRECTION
                if self.FORCE >= MAX_FORCE or self.FORCE <= 0:
                    self.FORCE_DIRECTION *= -1
                for b in range(math.ceil(self.FORCE / 2000)):
                    self.SCREEN.blit(
                        POWER_BAR,
                        (
                            BALLS[-1].body.position[0] + b * 15 - 30,
                            BALLS[-1].body.position[1] + 30,
                        ),
                    )

            elif not self.POWERING_UP and self.TAKING_SHOT:
                IMPULSE_DIRECTION = [
                    -math.cos(math.radians(cue_angle)),
                    math.sin(math.radians(cue_angle)),
                ]
                IMPULSE_DIRECTION = list(
                    map(lambda x: x * self.FORCE, IMPULSE_DIRECTION)
                )
                BALLS[-1].body.apply_impulse_at_local_point(IMPULSE_DIRECTION, (0, 0))
                self.FORCE = 0
                self.FORCE_DIRECTION = 1

            pygame.draw.rect(self.SCREEN, "black", (0, HEIGHT, WIDTH, BOTTOM_PANEL))

            for i, ball in enumerate(self.POTTED_BALLS):
                self.SCREEN.blit(ball, (10 + (i*50), HEIGHT + 10))

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    print("QUITED!")
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.MOUSEBUTTONDOWN and self.TAKING_SHOT:
                    self.POWERING_UP = True
                elif event.type == pygame.MOUSEBUTTONUP and self.TAKING_SHOT:
                    self.POWERING_UP = False

            pygame.display.update()


if __name__ == "__main__":
    game = Game()
    game.run()
