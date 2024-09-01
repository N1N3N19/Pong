import pygame, sys, random

from constant import *
from Ball import Ball
from Paddle import Paddle


class GameMain:
    def __init__(self):
        pygame.init()

        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))

        self.music_channel = pygame.mixer.Channel(0)
        self.music_channel.set_volume(0.2)
        
        self.sounds_list = {
            'paddle_hit': pygame.mixer.Sound('sounds/paddle_hit.wav'),
            'score': pygame.mixer.Sound('sounds/score.wav'),
            'wall_hit': pygame.mixer.Sound('sounds/wall_hit.wav'),
            'upgrade': pygame.mixer.Sound('sounds/upgrade.mp3')
        }

        self.select_state = 'start'
        self.game_mode = PLAYER_VS_BOT

        self.small_font = pygame.font.Font('font.ttf', 24)
        self.large_font = pygame.font.Font('font.ttf', 48)
        self.score_font = pygame.font.Font('font.ttf', 96)

        self.player1_score = 0
        self.player2_score = 0

        self.serving_player = 1
        self.winning_player = 0
        self.player1 = Paddle(self.screen, 30, 90, 15, PADDLE_SIZE)
        self.player2 = Paddle(self.screen, WIDTH - 30, HEIGHT - 90, 15, 60)
        
        self.ball = Ball(self.screen, WIDTH/2 - 6, HEIGHT/2 - 6, 12, 12)

        self.game_state = 'menu'

    def update(self, dt, events):
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            match self.game_state:
                case 'menu':
                    match self.select_state:
                        case 'start':
                            if event.type == pygame.KEYDOWN:
                                if event.key == KEYDOWN or event.key == S:
                                    self.select_state = UPGRADE
                                elif event.key == ENTER:
                                    self.game_state = PREPARE 
                                    self.select_state = PLAYER_VS_BOT
                        case 'upgrade':
                            if event.type == pygame.KEYDOWN:
                                if event.key == KEYUP or event.key == W:
                                    self.select_state = START
                                elif event.key == KEYDOWN or event.key == S:
                                    self.select_state = EXIT
                                elif event.key == ENTER:
                                    self.game_state = UPGRADE
                                    self.select_state = SPEED 
                        case 'exit':
                            if event.type == pygame.KEYDOWN:
                                if event.key == KEYUP or event.key == W:
                                    self.select_state = UPGRADE
                                elif event.key == ENTER:
                                    pygame.quit()
                                    sys.exit()
                case 'prepare':
                    match self.select_state:
                        case 'bot':
                            if event.type == pygame.KEYDOWN:
                                if event.key == KEYDOWN or event.key == S:
                                    self.select_state = PLAYER_VS_PLAYER
                                elif event.key == ENTER:
                                    self.game_state = START
                                    self.game_mode = PLAYER_VS_BOT
                        case 'player':
                            if event.type == pygame.KEYDOWN:
                                if event.key == KEYUP or event.key == W:
                                    self.select_state = PLAYER_VS_BOT
                                elif event.key == KEYDOWN or event.key == S:
                                    self.select_state = BACK
                                elif event.key == ENTER:
                                    self.player1 = Paddle(self.screen, 30, 90, 15, PADDLE_SIZE)
                                    self.game_state = START
                                    self.game_mode = PLAYER_VS_PLAYER
                        case 'back':
                            if event.type == pygame.KEYDOWN:
                                if event.key == KEYUP or event.key == W:
                                    self.select_state = PLAYER_VS_PLAYER
                                elif event.key == ENTER:
                                    self.game_state = MENU
                                    self.select_state = START
                case 'upgrade':
                    match self.select_state:
                        case 'speed':
                            if event.type == pygame.KEYDOWN:
                                if event.key == KEYDOWN or event.key == S:
                                    self.select_state = SIZE
                                elif event.key == pygame.K_RETURN:
                                    if (self.player1.extra_speed < 100 and self.player1.point >= 50):
                                        self.player1.point -= 50
                                        self.player1.extra_speed += 20
                                        self.music_channel.play(self.sounds_list['upgrade'])
                        case 'size':
                            if event.type == pygame.KEYDOWN:
                                if event.key == KEYDOWN or event.key == S:
                                    self.select_state = RESET
                                elif event.key == KEYUP or event.key == W:
                                    self.select_state = SPEED
                                elif event.key == ENTER:
                                    if (self.player1.added_size < 5 and self.player1.point >= 200):
                                        self.player1.change_size(20)
                                        self.player1.point -= 200
                                        self.player1.added_size += 1
                                        self.music_channel.play(self.sounds_list['upgrade'])

                        case 'reset':
                            if event.type == pygame.KEYDOWN:
                                if event.key == KEYDOWN or event.key == S:
                                    self.select_state = BACK
                                elif event.key == KEYUP or event.key == W:
                                    self.select_state = SIZE
                                elif event.key == ENTER:
                                    self.player1 = Paddle(self.screen, 30, 90, 15, PADDLE_SIZE)
                        case 'back':
                            if event.type == pygame.KEYDOWN:
                                if event.key == KEYUP or event.key == W:
                                    self.select_state = RESET
                                elif event.key == ENTER:
                                    self.game_state = MENU
                                    self.select_state = START

                case 'start':
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_RETURN:
                            self.game_state = SERVE

                case 'serve':
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_RETURN:
                            self.game_state = 'play'
                        if event.key == pygame.K_ESCAPE:
                            self.game_state = MENU
                            self.select_state = START
        match self.game_state:
            case 'serve':
                self.ball.dy = random.uniform(-150, 150)
                if self.serving_player == 1:
                    self.ball.dx = random.uniform(420, 600)
                else:
                    self.ball.dx = -random.uniform(420, 600)
                
            case 'play':
                if self.ball.Collides(self.player1):
                    self.ball.dx = -self.ball.dx * 1.03  # reflect speed multiplier
                    self.ball.rect.x = self.player1.rect.x + 15

                    #ball goes down
                    if self.ball.dy < 0:
                        self.ball.dy = -random.uniform(30, 450)
                    else:
                        self.ball.dy = random.uniform(30, 450)
                    self.music_channel.play(self.sounds_list['paddle_hit'])

                if self.ball.Collides(self.player2):
                    self.ball.dx = -self.ball.dx * 1.03
                    self.ball.rect.x = self.player2.rect.x - 12
                    if self.ball.dy < 0:
                        self.ball.dy = -random.uniform(30, 450)
                    else:
                        self.ball.dy = random.uniform(30, 450)

                    self.music_channel.play(self.sounds_list['paddle_hit'])

                # ball hit top wall
                if self.ball.rect.y <= 0:
                    self.ball.rect.y = 0
                    self.ball.dy = -self.ball.dy
                    self.music_channel.play(self.sounds_list['wall_hit'])

                # ball hit bottom wall, 12 represents ball size
                if self.ball.rect.y >= HEIGHT - 12:
                    self.ball.rect.y = HEIGHT - 12
                    self.ball.dy = -self.ball.dy
                    self.music_channel.play(self.sounds_list['wall_hit'])

                if self.ball.rect.x < 0:
                    self.serving_player = 1
                    self.player2_score += 1
                    self.music_channel.play(self.sounds_list['score'])
                    if self.player2_score == WINNING_SCORE:
                        self.winning_player = 2
                        self.game_state = 'done'
                    else:
                        self.game_state = 'serve'
                        self.ball.Reset()

                if self.ball.rect.x > WIDTH:
                    self.serving_player = 2
                    self.player1_score += 1
                    self.music_channel.play(self.sounds_list['score'])
                    if self.player1_score == WINNING_SCORE:
                        self.winning_player = 1
                        self.game_state = 'done'
                    else:
                        self.game_state = 'serve'
                        self.ball.Reset()
                #Counting point
                
            case 'done':
                self.game_state = SERVE
                self.ball.Reset()
                self.player1_score = 0
                self.player2_score = 0

                if self.winning_player == 1:
                    self.serving_player = 2
                else:
                    self.serving_player = 1
        match self.game_mode:
            case 'bot':
                key = pygame.key.get_pressed()            
                if key[W]:
                    self.player1.dy = -(PADDLE_SPEED + self.player1.extra_speed)
                elif key[S]:
                    self.player1.dy = PADDLE_SPEED + self.player1.extra_speed
                else:
                    self.player1.dy = 0
                match self.game_state:
                    case 'play':
                        if self.player1_score >= 1:
                            if self.ball.rect.y > self.player2.rect.y+30:
                                self.player2.dy = PADDLE_SPEED
                            elif self.ball.rect.y < self.player2.rect.y+30:
                                self.player2.dy = -PADDLE_SPEED
                            else:
                                self.player2.dy = 0
                        else:
                            if self.ball.rect.y > self.player2.rect.y + 30:
                                self.player2.dy = EASY_AI_SPEED
                            elif self.ball.rect.y < self.player2.rect.y + 30:
                                self.player2.dy = -EASY_AI_SPEED
                            else:
                                self.player2.dy = 0
                            if random.random() < 0.2:
                                self.player2.dy = 200 if random.choice([True, False]) else -EASY_AI_SPEED
                        self.player1.point += 0.01
                        
            case 'player':
                
                key = pygame.key.get_pressed()            
                if key[W]:
                    self.player1.dy = -PADDLE_SPEED
                elif key[S]:
                    self.player1.dy = PADDLE_SPEED
                else:
                    self.player1.dy = 0

                if key[KEYUP]:
                    self.player2.dy = -PADDLE_SPEED
                elif key[KEYDOWN]:
                    self.player2.dy = PADDLE_SPEED
                else:
                    self.player2.dy = 0    
            
        if self.game_state == 'play':
            self.ball.update(dt)

        self.player1.update(dt)
        self.player2.update(dt)

    def render(self):
        self.screen.fill((40, 45, 52))
        texts = {}
        index = 1
        match self.game_state:
            case 'menu':
                t_welcome = self.small_font.render("Welcome to Pong!", False, (255, 255, 255))
                text_rect = t_welcome.get_rect(center=(WIDTH / 2, 30))
                for label, color in MENU_PAGE[self.select_state].items():
                    text = self.large_font.render(label, False, color)
                    rect = text.get_rect(center=POSITIONS_3[index])
                    index += 1
                    texts[label] = (text, rect)
                for text, rect in texts.values():
                    self.screen.blit(text, rect)
                self.screen.blit(t_welcome, text_rect)
            case 'upgrade':
                t_point = self.small_font.render("You have " + str(int(self.player1.point)) + " points", False, WHITE)
                point_rect = t_point.get_rect(center=(WIDTH / 2, 30))
                t_speed_qouta = self.small_font.render("Speed: 50 points each  " + str(int(5 - self.player1.extra_speed/20)) + "/5", False, WHITE)
                speed_quota_rect = t_speed_qouta.get_rect(center=(WIDTH / 2, 60))
                t_size_qouta = self.small_font.render("Size: 200 points each  " + str(int(5 - self.player1.added_size)) + "/5", False, WHITE)
                size_quota_rect = t_speed_qouta.get_rect(center=(WIDTH / 2, 85))
                for label, color in UPGRADE_PAGE[self.select_state].items():
                    text = self.large_font.render(label, False, color)
                    rect = text.get_rect(center=POSITIONS_4[index])
                    index += 1
                    texts[label] = (text, rect)
                for text, rect in texts.values():
                    self.screen.blit(text, rect)
                self.screen.blit(t_point, point_rect)
                self.screen.blit(t_speed_qouta, speed_quota_rect)
                self.screen.blit(t_size_qouta, size_quota_rect)
            case 'prepare':
                t_game_mode = self.small_font.render("Select game mode!", False, (255, 255, 255))
                game_mode_rect = t_game_mode.get_rect(center=(WIDTH / 2, 30))
                for label, color in PREPARE_PAGE[self.select_state].items():
                    text = self.large_font.render(label, False, color)
                    rect = text.get_rect(center=POSITIONS_3[index])
                    index += 1
                    texts[label] = (text, rect)
                for text, rect in texts.values():
                    self.screen.blit(text, rect)
                self.screen.blit(t_game_mode, game_mode_rect)
            case 'start':
                t_press_enter_begin = self.small_font.render('Press Enter to begin!', False, WHITE)
                text_rect = t_press_enter_begin.get_rect(center=(WIDTH / 2, 60))
                self.screen.blit(t_press_enter_begin, text_rect)
            case 'serve':
                t_serve = self.small_font.render("player" + str(self.serving_player) + "'s serve!", False, WHITE)
                text_rect = t_serve.get_rect(center=(WIDTH/2, 30))
                t_esc = self.small_font.render("Press ESC back to Menu", False, WHITE)
                esc_rect = t_esc.get_rect(center=(170, 15))
                self.screen.blit(t_serve, text_rect)
                self.screen.blit(t_esc, esc_rect)
                t_enter_serve = self.small_font.render("Press Enter to serve!", False, WHITE)
                text_rect = t_enter_serve.get_rect(center=(WIDTH / 2, 60))
                self.screen.blit(t_enter_serve, text_rect)               
            case 'play':
                t_point = self.small_font.render("Point: " + str(int(self.player1.point)), False, YELLOW)
                point_rect = t_point.get_rect(center=(WIDTH/2, HEIGHT - 30))
                self.screen.blit(t_point, point_rect)
                pass
                
            case 'done':
                t_win = self.large_font.render("player" + str(self.serving_player) + "'s wins!", False, WHITE)
                text_rect = t_win.get_rect(center=(WIDTH / 2, 30))
                self.screen.blit(t_win, text_rect)

                t_restart = self.small_font.render("Press Enter to restart", False, WHITE)
                text_rect = t_restart.get_rect(center=(WIDTH / 2, 70))
                self.screen.blit(t_restart, text_rect)
        if self.game_state != PREPARE and self.game_state != UPGRADE and self.game_state != MENU: 
            self.DisplayScore()
            #right paddle
            self.player2.render()

            #left paddle
            self.player1.render()

            #ball
            self.ball.render()
            

        



    def DisplayScore(self):
        self.t_p1_score = self.score_font.render(str(self.player1_score), False, (255, 255, 255))
        self.t_p2_score = self.score_font.render(str(self.player2_score), False, (255, 255, 255))
        self.screen.blit(self.t_p1_score, (WIDTH/2 - 150, HEIGHT/3))
        self.screen.blit(self.t_p2_score, (WIDTH / 2 + 90, HEIGHT / 3))

if __name__ == '__main__':
    main = GameMain()

    clock = pygame.time.Clock()

    while True:
        pygame.display.set_caption("Pong game running with {:d} FPS".format(int(clock.get_fps())))

        # elapsed time from the last call
        dt = clock.tick(MAX_FRAME_RATE)/1000.0

        events = pygame.event.get()
        main.update(dt, events)
        main.render()

        pygame.display.update()
