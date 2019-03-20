import pygame
# change the name of this module
import players as p
import diff
import thorpy
import pong


def buttons(screen):
    again = thorpy.make_button("Play Again", func=more)
    leave = thorpy.make_button("Exit", func=thorpy.functions.quit_func)
    again.surface = screen
    leave.surface = screen
    box = thorpy.Box.make([again, leave])
    box.fit_children((30, 30))
    box.center()
    box.set_main_color((0, 0, 0, 0))
    menu = thorpy.Menu(box)
    menu.play()


def more():
    p.menu.play()


def main(lvl):
    pygame.init()
    screen = pygame.display.set_mode((900, 600))
    pygame.display.set_caption("Pong")
    background = pygame.Surface(screen.get_size())
    background = background.convert()
    background.fill((0, 0, 0))
    font = pygame.font.Font(None, 36)

    global player1
    global computer
    player1 = pong.Pad("left")
    computer = pong.AI(lvl)
    ball = pong.Ball()
    players = pygame.sprite.RenderPlain((player1, computer))
    balls = pygame.sprite.RenderPlain(ball)
    screen.blit(background, (0, 0))
    pygame.display.flip()
    clock = pygame.time.Clock()
    game_over = False

    while 1:
        # fix intialized angle of the ball
        # add function to change the angle of the ball on reflection
        # this was probably the diff function
        clock.tick(60)
        screen.fill((0, 0, 0))
        #  fix ball movement when the button is held for a long time
        pygame.key.set_repeat(100, 100)
        for event in pygame.event.get():
            action = computer.predict()
            if action == -1:
                computer.movedown()
            elif action == 1:
                computer.moveup()
            elif action == 0:
                computer.movepos = [0, 0]
                computer.state = "still"

            if event.type == pygame.QUIT:
                return
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_w:
                    player1.moveup()
                if event.key == pygame.K_s:
                    player1.movedown()
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_w or event.key == pygame.K_s:
                    player1.movepos = [0, 0]
                    player1.state = "still"
        if abs(player1.score-computer.score) > 3:
            game_over = True

        if game_over:
            text = font.render("Game Over", 1, (200, 200, 200))
            textpos = text.get_rect(centerx=background.get_width()/2)
            textpos.top = 50
            screen.blit(text, textpos)
            win_mess = "You win!" if (
                player1.score > computer.score) else "You lose!"
            win_text = font.render(win_mess, 1, (200, 200, 200))
            winpos = win_text.get_rect(centerx=background.get_width()/2)
            winpos.top = 150
            screen.blit(win_text, winpos)
            buttons(screen)

        scoreprint = "You: " + str(player1.score)
        text = font.render(scoreprint, 1, (255, 255, 255))
        textpos = (200, 0)
        screen.blit(text, textpos)

        scoreprint = "Computer: " + str(computer.score)
        text = font.render(scoreprint, 1, (255, 255, 255))
        textpos = (600, 0)
        screen.blit(text, textpos)

        screen.blit(background, ball.rect, ball.rect)
        screen.blit(background, player1.rect, player1.rect)
        screen.blit(background, computer.rect, computer.rect)
        ball.update(player1, computer)
        players.update()
        balls.draw(screen)
        players.draw(screen)
        pygame.display.flip()


if __name__ == "__main__":
    import sys
    main(lvl=diff.sel_diff)