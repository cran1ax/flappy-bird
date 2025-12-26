import pygame
import random
import sys

# Initialize Pygame
pygame.init()

# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
SKY_BLUE = (135, 206, 235)
GREEN = (34, 139, 34)
DARK_GREEN = (0, 100, 0)
YELLOW = (255, 215, 0)
RED = (220, 20, 60)

# Game variables
GRAVITY = 0.5
FLAP_STRENGTH = -10
PIPE_SPEED = 3
PIPE_GAP = 200
PIPE_FREQUENCY = 1500  # milliseconds

class Bird:
    def __init__(self):
        self.x = 100
        self.y = SCREEN_HEIGHT // 2
        self.velocity = 0
        self.radius = 20
        self.color = YELLOW
        self.rotation = 0
        
    def flap(self):
        self.velocity = FLAP_STRENGTH
        
    def update(self):
        # Apply gravity
        self.velocity += GRAVITY
        self.y += self.velocity
        
        # Update rotation based on velocity
        self.rotation = max(-30, min(30, -self.velocity * 3))
        
    def draw(self, screen):
        # Draw bird body
        pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), self.radius)
        # Draw bird eye
        eye_x = int(self.x + 8)
        eye_y = int(self.y - 5)
        pygame.draw.circle(screen, WHITE, (eye_x, eye_y), 6)
        pygame.draw.circle(screen, BLACK, (eye_x + 2, eye_y), 3)
        # Draw beak
        beak_points = [
            (int(self.x + self.radius), int(self.y)),
            (int(self.x + self.radius + 10), int(self.y - 3)),
            (int(self.x + self.radius + 10), int(self.y + 3))
        ]
        pygame.draw.polygon(screen, RED, beak_points)
        
    def get_rect(self):
        return pygame.Rect(self.x - self.radius, self.y - self.radius, 
                          self.radius * 2, self.radius * 2)
    
    def check_boundaries(self):
        # Check if bird hit top or bottom
        if self.y - self.radius <= 0 or self.y + self.radius >= SCREEN_HEIGHT:
            return True
        return False

class Pipe:
    def __init__(self, x):
        self.x = x
        self.width = 70
        self.gap = PIPE_GAP
        self.top_height = random.randint(100, SCREEN_HEIGHT - self.gap - 100)
        self.bottom_y = self.top_height + self.gap
        self.passed = False
        
    def update(self):
        self.x -= PIPE_SPEED
        
    def draw(self, screen):
        # Draw top pipe
        pygame.draw.rect(screen, GREEN, (self.x, 0, self.width, self.top_height))
        pygame.draw.rect(screen, DARK_GREEN, (self.x, 0, self.width, self.top_height), 3)
        # Draw top pipe cap
        pygame.draw.rect(screen, GREEN, (self.x - 5, self.top_height - 20, self.width + 10, 20))
        pygame.draw.rect(screen, DARK_GREEN, (self.x - 5, self.top_height - 20, self.width + 10, 20), 3)
        
        # Draw bottom pipe
        pygame.draw.rect(screen, GREEN, (self.x, self.bottom_y, self.width, SCREEN_HEIGHT - self.bottom_y))
        pygame.draw.rect(screen, DARK_GREEN, (self.x, self.bottom_y, self.width, SCREEN_HEIGHT - self.bottom_y), 3)
        # Draw bottom pipe cap
        pygame.draw.rect(screen, GREEN, (self.x - 5, self.bottom_y, self.width + 10, 20))
        pygame.draw.rect(screen, DARK_GREEN, (self.x - 5, self.bottom_y, self.width + 10, 20), 3)
        
    def collide(self, bird):
        bird_rect = bird.get_rect()
        
        # Top pipe collision
        top_pipe_rect = pygame.Rect(self.x, 0, self.width, self.top_height)
        # Bottom pipe collision
        bottom_pipe_rect = pygame.Rect(self.x, self.bottom_y, self.width, SCREEN_HEIGHT - self.bottom_y)
        
        if bird_rect.colliderect(top_pipe_rect) or bird_rect.colliderect(bottom_pipe_rect):
            return True
        return False
    
    def is_off_screen(self):
        return self.x + self.width < 0

class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Flappy Bird")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 48)
        self.small_font = pygame.font.Font(None, 32)
        self.reset_game()
        
    def reset_game(self):
        self.bird = Bird()
        self.pipes = []
        self.score = 0
        self.game_state = "start"  # start, playing, game_over
        self.last_pipe_time = pygame.time.get_ticks()
        
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    if self.game_state == "start":
                        self.game_state = "playing"
                        self.bird.flap()
                    elif self.game_state == "playing":
                        self.bird.flap()
                    elif self.game_state == "game_over":
                        self.reset_game()
                        
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.game_state == "start":
                    self.game_state = "playing"
                    self.bird.flap()
                elif self.game_state == "playing":
                    self.bird.flap()
                elif self.game_state == "game_over":
                    self.reset_game()
                    
        return True
    
    def update(self):
        if self.game_state == "playing":
            # Update bird
            self.bird.update()
            
            # Check boundary collision
            if self.bird.check_boundaries():
                self.game_state = "game_over"
                
            # Generate pipes
            current_time = pygame.time.get_ticks()
            if current_time - self.last_pipe_time > PIPE_FREQUENCY:
                self.pipes.append(Pipe(SCREEN_WIDTH))
                self.last_pipe_time = current_time
                
            # Update pipes
            for pipe in self.pipes[:]:
                pipe.update()
                
                # Check collision
                if pipe.collide(self.bird):
                    self.game_state = "game_over"
                    
                # Check if bird passed pipe
                if not pipe.passed and pipe.x + pipe.width < self.bird.x:
                    pipe.passed = True
                    self.score += 1
                    
                # Remove off-screen pipes
                if pipe.is_off_screen():
                    self.pipes.remove(pipe)
                    
    def draw(self):
        # Draw background
        self.screen.fill(SKY_BLUE)
        
        # Draw ground line
        pygame.draw.rect(self.screen, GREEN, (0, SCREEN_HEIGHT - 50, SCREEN_WIDTH, 50))
        pygame.draw.rect(self.screen, DARK_GREEN, (0, SCREEN_HEIGHT - 50, SCREEN_WIDTH, 5))
        
        # Draw pipes
        for pipe in self.pipes:
            pipe.draw(self.screen)
            
        # Draw bird
        self.bird.draw(self.screen)
        
        # Draw score
        score_text = self.font.render(str(self.score), True, WHITE)
        score_outline = self.font.render(str(self.score), True, BLACK)
        self.screen.blit(score_outline, (SCREEN_WIDTH // 2 - score_text.get_width() // 2 + 2, 52))
        self.screen.blit(score_text, (SCREEN_WIDTH // 2 - score_text.get_width() // 2, 50))
        
        # Draw start screen
        if self.game_state == "start":
            title_text = self.font.render("Flappy Bird", True, WHITE)
            title_outline = self.font.render("Flappy Bird", True, BLACK)
            self.screen.blit(title_outline, (SCREEN_WIDTH // 2 - title_text.get_width() // 2 + 2, SCREEN_HEIGHT // 2 - 52))
            self.screen.blit(title_text, (SCREEN_WIDTH // 2 - title_text.get_width() // 2, SCREEN_HEIGHT // 2 - 50))
            
            instruction_text = self.small_font.render("Press SPACE or Click to Start", True, WHITE)
            instruction_outline = self.small_font.render("Press SPACE or Click to Start", True, BLACK)
            self.screen.blit(instruction_outline, (SCREEN_WIDTH // 2 - instruction_text.get_width() // 2 + 1, SCREEN_HEIGHT // 2 + 21))
            self.screen.blit(instruction_text, (SCREEN_WIDTH // 2 - instruction_text.get_width() // 2, SCREEN_HEIGHT // 2 + 20))
            
        # Draw game over screen
        if self.game_state == "game_over":
            game_over_text = self.font.render("Game Over!", True, WHITE)
            game_over_outline = self.font.render("Game Over!", True, BLACK)
            self.screen.blit(game_over_outline, (SCREEN_WIDTH // 2 - game_over_text.get_width() // 2 + 2, SCREEN_HEIGHT // 2 - 52))
            self.screen.blit(game_over_text, (SCREEN_WIDTH // 2 - game_over_text.get_width() // 2, SCREEN_HEIGHT // 2 - 50))
            
            final_score_text = self.small_font.render(f"Final Score: {self.score}", True, WHITE)
            final_score_outline = self.small_font.render(f"Final Score: {self.score}", True, BLACK)
            self.screen.blit(final_score_outline, (SCREEN_WIDTH // 2 - final_score_text.get_width() // 2 + 1, SCREEN_HEIGHT // 2 + 1))
            self.screen.blit(final_score_text, (SCREEN_WIDTH // 2 - final_score_text.get_width() // 2, SCREEN_HEIGHT // 2))
            
            restart_text = self.small_font.render("Press SPACE or Click to Restart", True, WHITE)
            restart_outline = self.small_font.render("Press SPACE or Click to Restart", True, BLACK)
            self.screen.blit(restart_outline, (SCREEN_WIDTH // 2 - restart_text.get_width() // 2 + 1, SCREEN_HEIGHT // 2 + 51))
            self.screen.blit(restart_text, (SCREEN_WIDTH // 2 - restart_text.get_width() // 2, SCREEN_HEIGHT // 2 + 50))
            
        pygame.display.flip()
        
    def run(self):
        running = True
        while running:
            running = self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(FPS)
            
        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    game = Game()
    game.run()
