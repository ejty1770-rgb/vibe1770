import pygame
import random
from enum import Enum

# 게임 상수
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
GRID_SIZE = 20
GRID_WIDTH = WINDOW_WIDTH // GRID_SIZE
GRID_HEIGHT = WINDOW_HEIGHT // GRID_SIZE

# 색상
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)

class Direction(Enum):
    UP = (0, -1)
    DOWN = (0, 1)
    LEFT = (-1, 0)
    RIGHT = (1, 0)

class SnakeGame:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("Snake Game")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 36)
        
        self.reset_game()
    
    def reset_game(self):
        # 뱀 초기 위치 (머리)
        self.snake = [(GRID_WIDTH // 2, GRID_HEIGHT // 2)]
        self.direction = Direction.RIGHT
        self.next_direction = Direction.RIGHT
        self.food = self.spawn_food()
        self.score = 0
        self.game_over = False
    
    def spawn_food(self):
        """음식을 랜덤하게 배치"""
        while True:
            food = (random.randint(0, GRID_WIDTH - 1), random.randint(0, GRID_HEIGHT - 1))
            if food not in self.snake:
                return food
    
    def handle_input(self):
        """입력 처리"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP and self.direction != Direction.DOWN:
                    self.next_direction = Direction.UP
                elif event.key == pygame.K_DOWN and self.direction != Direction.UP:
                    self.next_direction = Direction.DOWN
                elif event.key == pygame.K_LEFT and self.direction != Direction.RIGHT:
                    self.next_direction = Direction.LEFT
                elif event.key == pygame.K_RIGHT and self.direction != Direction.LEFT:
                    self.next_direction = Direction.RIGHT
                elif event.key == pygame.K_SPACE and self.game_over:
                    self.reset_game()
        
        return True
    
    def update(self):
        """게임 상태 업데이트"""
        if self.game_over:
            return
        
        self.direction = self.next_direction
        
        # 새로운 머리 위치 계산
        head_x, head_y = self.snake[0]
        dx, dy = self.direction.value
        new_head = (head_x + dx, head_y + dy)
        
        # 벽 충돌 체크
        if (new_head[0] < 0 or new_head[0] >= GRID_WIDTH or
            new_head[1] < 0 or new_head[1] >= GRID_HEIGHT):
            self.game_over = True
            return
        
        # 자기 몸 충돌 체크
        if new_head in self.snake:
            self.game_over = True
            return
        
        # 뱀 이동
        self.snake.insert(0, new_head)
        
        # 음식 먹었는지 체크
        if new_head == self.food:
            self.score += 10
            self.food = self.spawn_food()
        else:
            # 음식을 못 먹었으면 꼬리 제거
            self.snake.pop()
    
    def draw(self):
        """화면 그리기"""
        self.screen.fill(BLACK)
        
        # 뱀 그리기
        for i, (x, y) in enumerate(self.snake):
            rect = pygame.Rect(x * GRID_SIZE, y * GRID_SIZE, GRID_SIZE - 2, GRID_SIZE - 2)
            if i == 0:
                # 머리는 밝은 초록색
                pygame.draw.rect(self.screen, GREEN, rect)
            else:
                # 몸은 어두운 초록색
                pygame.draw.rect(self.screen, (0, 180, 0), rect)
        
        # 음식 그리기
        food_rect = pygame.Rect(self.food[0] * GRID_SIZE, self.food[1] * GRID_SIZE, GRID_SIZE - 2, GRID_SIZE - 2)
        pygame.draw.rect(self.screen, RED, food_rect)
        
        # 점수 표시
        score_text = self.font.render(f"Score: {self.score}", True, WHITE)
        self.screen.blit(score_text, (10, 10))
        
        # 게임 오버 메시지
        if self.game_over:
            game_over_text = self.font.render("GAME OVER!", True, RED)
            restart_text = self.font.render("Press SPACE to restart", True, YELLOW)
            
            text_rect1 = game_over_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 - 40))
            text_rect2 = restart_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 + 20))
            
            self.screen.blit(game_over_text, text_rect1)
            self.screen.blit(restart_text, text_rect2)
        
        pygame.display.flip()
    
    def run(self):
        """게임 메인 루프"""
        running = True
        
        while running:
            running = self.handle_input()
            self.update()
            self.draw()
            self.clock.tick(10)  # FPS 설정
        
        pygame.quit()

if __name__ == "__main__":
    game = SnakeGame()
    game.run()
