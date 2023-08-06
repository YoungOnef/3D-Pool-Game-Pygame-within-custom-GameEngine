import math
import pygame
import PyParticles
import time

#  setting up the pygame window / title of the window
pygame.display.set_caption("Pool Game")
screen = pygame.display.set_mode((600, 600))
#  setting up the font for displaying text on the screen
pygame.font.init()

#  setting up the environment for the game using PyParticles
environment = PyParticles.Environment(600, 600)
# add functions to the environment for movement, bouncing, collision detection, and drag
environment.addFunctions(['move','bounceWindowGame','bounceLines','collide','drag'])

# add the table and pockets to the environment
environment.addLine((50, 50), (550, 50))  # top edge
environment.addLine((550, 50), (550, 550))  # right edge
environment.addLine((550, 550), (50, 550))  # bottom edge
environment.addLine((50, 550), (50, 50))  # left edge

environment.addCircle(50, 50, 15)  # top left pocket
environment.addCircle(550, 50, 15)  # top right pocket
environment.addCircle(550, 550, 15)  # bottom right pocket
environment.addCircle(50, 550, 15)  # bottom left pocket

# add a variable to store the total number of balls added to the environment
total_balls = 16
# add the pool balls to the environment
environment.addParticles(total_balls, 50, 50, 550, 550, size=10, colour=(0, 0, 255)) # 16 balls, 10px size, 100g mass, blue colour

#  setting up variables to track the state of the game
player1_score = 0
player2_score = 0
player1_time = 0
player2_time = 0
turn = 1  
# setting up clock (frame per second)
clock = pygame.time.Clock()
#state of the game
running = True
#defining the time when the game starts
start_time = time.time()
while running:
    for event in pygame.event.get():
        # check if the window has been closed
        if event.type == pygame.QUIT:
            running = False
        # check if the mouse button has been pressed down
        elif event.type == pygame.MOUSEBUTTONDOWN:
            # select the ball at the mouse position
            selected_ball = environment.findParticle(event.pos)
            # if a ball was selected store the initial position of the ball
            if selected_ball:
                initial_pos = pygame.mouse.get_pos()
        # check if the mouse button has been released
        elif event.type == pygame.MOUSEBUTTONUP:
            # if a ball was selected aim and shoot the ball based on the initial and final positions
            if selected_ball:
                final_pos = pygame.mouse.get_pos()
                # calculate the distance and angle between the initial and final positions
                distance = math.hypot(final_pos[0] - initial_pos[0], final_pos[1] - initial_pos[1])
                angle = math.atan2(final_pos[1] - initial_pos[1], final_pos[0] - initial_pos[0])
                # set the angle and speed of the selected ball
                selected_ball.angle = angle - math.pi/2 
                selected_ball.speed = distance * 0.1
            # deselect the ball
            selected_ball = None
            
    # update the environment
    environment.update()

    # check for pocketed balls
    pocketed_balls = environment.checkCircleCollision()
    #check who hit the ball to the pocket and adding the score
    for ball in pocketed_balls:
        if turn == 1:
            player1_score += 1
            print("Player 1 scores!", player1_score)
        else:
            player2_score += 1
            print("Player 2 scores!", player2_score)

    # update the elapsed time for each player when a ball is pocketed
    if pocketed_balls:
        # switch turns
        turn = 3 - turn
        # record the elapsed time for the current player
        if turn == 1:
            player1_time += time.time() - start_time
            print("player1_time", player1_time)
        else:
            player2_time += time.time() - start_time
            print("player2_time", player2_time)
        # reset the timer
        start_time = time.time()
    #checking if all balls have been pocketed
    if len(environment.particles) == 0:
        # check if all balls have been pocketed by either player
        if player1_score + player2_score == total_balls:
            # determine the winner based on elapsed time and display the results on the screen
            if player1_time < player2_time:
                winner_text = font.render("Player 1 wins!", True, (0, 0, 0))
                # display the elapsed time for both players on the screen
                time_text = font.render(f"Player 1 elapsed time: {player1_time:.2f}s", True, (0, 0, 0))
                loser_time_text = font.render(f"Player 2 elapsed time: {player2_time:.2f}s", True, (0, 0, 0))
            else:
                winner_text = font.render("Player 2 wins!", True, (0, 0, 0))
                # display the elapsed time for both players on the screen
                time_text = font.render(f"Player 2 elapsed time: {player2_time:.2f}s", True, (0, 0, 0))
                loser_time_text = font.render(f"Player 1 elapsed time: {player1_time:.2f}s", True, (0, 0, 0))
            #refresh the screen
            screen.blit(winner_text, (200, 300))
            screen.blit(time_text, (200, 340))
            screen.blit(loser_time_text, (200, 380))
            pygame.display.flip()
            # wait for 10 seconds before quitting the game
            pygame.time.wait(10000)
            # quit the pygame module to end the game
            pygame.quit()

    # draw the environment
    screen.fill((255, 255, 255))  # white background
    
    # draw lines and circles on screen
    for line in environment.lines:
        pygame.draw.line(screen, (0, 0, 0), line[0], line[1], 2)
    for circle in environment.circles:
        pygame.draw.circle(screen, (0, 0, 0), circle[:2], circle[2], 2)

    # draw balls on screen
    for ball in environment.particles:
        pygame.draw.circle(screen, ball.colour, (int(ball.x), int(ball.y)), ball.size, ball.thickness)

    # draw scores on screen
    font = pygame.font.Font(None, 36)
    player1_text = font.render(f"Player 1: {player1_score}", True, (0, 0, 0))
    player2_text = font.render(f"Player 2: {player2_score}", True, (0, 0, 0))
    player_text = font.render(f"Player {turn} turn", True, (0, 0, 0))
    #refresh the screen
    screen.blit(player_text, (200, 10))
    screen.blit(player1_text, (10, 10))
    screen.blit(player2_text, (450, 10))

    # update screen
    pygame.display.flip()

    # limit frame rate
    clock.tick(60)
