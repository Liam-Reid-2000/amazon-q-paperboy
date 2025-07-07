import pygame

pygame.init()

# Isometric transformation functions
def to_iso(x, y):
    iso_x = (x - y) * 0.866  # cos(30°)
    iso_y = (x + y) * 0.5    # sin(30°)
    return iso_x + WIDTH//2, iso_y + 100

def from_iso(iso_x, iso_y):
    iso_x -= WIDTH//2
    iso_y -= 100
    x = (iso_x / 0.866 + iso_y) / 2
    y = (iso_y - iso_x / 0.866) / 2
    return x, y

WIDTH, HEIGHT = 1000, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Paperboy")
clock = pygame.time.Clock()

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
BROWN = (139, 69, 19)
GRAY = (128, 128, 128)
PINK = (255, 192, 203)

class Player:
    def __init__(self):
        self.x = -150
        self.y = 0
        self.speed = 3
        self.papers = 10
        
    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP]:
            self.y -= self.speed
        if keys[pygame.K_DOWN]:
            self.y += self.speed
        if keys[pygame.K_LEFT]:
            self.x -= self.speed
        if keys[pygame.K_RIGHT]:
            self.x += self.speed    
    def draw(self, screen):
        iso_x, iso_y = to_iso(self.x, self.y)
        pygame.draw.circle(screen, BLUE, (int(iso_x), int(iso_y)), 12)
        pygame.draw.rect(screen, BLACK, (int(iso_x - 8), int(iso_y - 3), 16, 6))

class Newspaper:
    def __init__(self, x, y, dx, dy):
        self.x = x
        self.y = y
        self.vx = dx * 5
        self.vy = dy * 5
        
    def update(self):
        self.x += self.vx
        self.y += self.vy
        
    def draw(self, screen):
        iso_x, iso_y = to_iso(self.x, self.y)
        pygame.draw.rect(screen, BLACK, (int(iso_x - 5), int(iso_y - 5), 10, 10))
        pygame.draw.rect(screen, WHITE, (int(iso_x - 4), int(iso_y - 4), 8, 8))

class House:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.hit = False
        
    def draw(self, screen):
        iso_x, iso_y = to_iso(self.x, self.y)
        # Draw bigger rectangular house
        pygame.draw.rect(screen, BROWN, (int(iso_x - 25), int(iso_y - 15), 50, 30))
        # Draw triangular roof
        roof_points = [
            (iso_x - 30, iso_y - 15),
            (iso_x, iso_y - 35),
            (iso_x + 30, iso_y - 15)
        ]
        pygame.draw.polygon(screen, RED, roof_points)
        if self.hit:
            font = pygame.font.Font(None, 20)
            text = font.render("Delivered!", True, WHITE)
            screen.blit(text, (int(iso_x - 20), int(iso_y - 45)))


def main():
    player = Player()
    newspapers = []
    houses = []
    score = 0
    
    # Generate fewer, more spaced out houses
    for i in range(8):
        # Houses on top side of street
        houses.append(House(-120 + i * 80, -80))
        # Houses on bottom side of street  
        houses.append(House(-220 + i * 80, 200))
    
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_z and player.papers > 0:
                    newspapers.append(Newspaper(player.x, player.y, 0, 1))
                    player.papers -= 1
                elif event.key == pygame.K_x and player.papers > 0:
                    newspapers.append(Newspaper(player.x, player.y, 0, -1))
                    player.papers -= 1
                elif event.key == pygame.K_r:
                    # Restart level
                    player = Player()
                    newspapers = []
                    houses = []
                    score = 0
                    # Generate fewer, more spaced out houses
                    for i in range(8):
                        # Houses on top side of street
                        houses.append(House(-120 + i * 80, -80))
                        # Houses on bottom side of street  
                        houses.append(House(-220 + i * 80, 200))

                elif event.key == pygame.K_ESCAPE:
                    running = False
        
        player.update()
        
        # Update newspapers
        for paper in newspapers[:]:
            paper.update()
            if abs(paper.x) > 300 or abs(paper.y) > 300:
                newspapers.remove(paper)
            else:
                # Check house hits
                for house in houses:
                    if (abs(house.x - paper.x) < 35 and 
                        abs(house.y - paper.y) < 35 and not house.hit):
                        house.hit = True
                        newspapers.remove(paper)
                        score += 10
                        break
        

        
        # Draw everything
        screen.fill(GREEN)
        
        # Draw longer and bigger isometric road
        road_points = [
            to_iso(-400, -50),
            to_iso(800, -50),
            to_iso(800, 200),
            to_iso(-400, 200)
        ]
        pygame.draw.polygon(screen, GRAY, road_points)
        
        player.draw(screen)
        
        for house in houses:
            house.draw(screen)
            

            
        for paper in newspapers:
            paper.draw(screen)
        
        # Draw UI
        font = pygame.font.Font(None, 36)
        score_text = font.render(f"Score: {score}", True, BLACK)
        papers_text = font.render(f"Papers: {player.papers}", True, BLACK)
        screen.blit(score_text, (10, 10))
        screen.blit(papers_text, (10, 50))
        
        if player.papers == 0 and len(newspapers) == 0:
            game_over_text = font.render("Game Over! Press R to restart, ESC to quit", True, RED)
            screen.blit(game_over_text, (WIDTH//2 - 200, HEIGHT//2))
        
        pygame.display.flip()
        clock.tick(60)
    
    pygame.quit()

if __name__ == "__main__":
    main()