import pygame
import random

# Константы
GRID_SIZE = 20
GRID_WIDTH = 32
GRID_HEIGHT = 24
SCREEN_WIDTH = GRID_SIZE * GRID_WIDTH
SCREEN_HEIGHT = GRID_SIZE * GRID_HEIGHT

COLORS = {
    'background': (0, 0, 0),
    'snake': (0, 255, 0),
    'apple': (255, 0, 0)
}

BOARD_BACKGROUND_COLOR = COLORS['background']

UP = (0, -GRID_SIZE)
DOWN = (0, GRID_SIZE)
LEFT = (-GRID_SIZE, 0)
RIGHT = (GRID_SIZE, 0)

# Глобальные переменные для тестов
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pygame.time.Clock()


class GameObject:
    """Базовый класс для объектов игры."""

    def __init__(self, position=(0, 0), body_color=COLORS['background']):
        self.position = position
        self.body_color = body_color

    def draw(self, surface):
        """Отрисовка объекта."""
        rect = pygame.Rect(
            self.position[0],
            self.position[1],
            GRID_SIZE,
            GRID_SIZE
        )
        pygame.draw.rect(surface, self.body_color, rect)


class Apple(GameObject):
    """Класс для яблока."""

    def __init__(self, body_color=COLORS['apple']):
        super().__init__((0, 0), body_color)
        self.randomize_position()

    def randomize_position(self):
        """Генерация случайной позиции."""
        self.position = (
            random.randint(0, GRID_WIDTH - 1) * GRID_SIZE,
            random.randint(0, GRID_HEIGHT - 1) * GRID_SIZE
        )

    def draw(self, surface):
        """Отрисовка яблока."""
        rect = pygame.Rect(
            self.position[0],
            self.position[1],
            GRID_SIZE,
            GRID_SIZE
        )
        pygame.draw.rect(surface, self.body_color, rect)


class Snake(GameObject):
    """Класс для змейки."""

    def __init__(self, body_color=COLORS['snake']):
        start_position = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        super().__init__(start_position, body_color)
        self.positions = [start_position]
        self.direction = RIGHT
        self.next_direction = None
        self.last = None

    def get_head_position(self):
        """Возвращает позицию головы змейки."""
        return self.positions[0]

    def update_direction(self, direction):
        """Обновляет направление движения."""
        if self.next_direction is None:
            if (direction[0] * -1, direction[1] * -1) != self.direction:
                self.next_direction = direction

    def move(self):
        """Движение змейки."""
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None

        head_x, head_y = self.get_head_position()
        new_x = (head_x + self.direction[0]) % SCREEN_WIDTH
        new_y = (head_y + self.direction[1]) % SCREEN_HEIGHT
        new_head = (new_x, new_y)

        self.last = self.positions[-1]
        self.positions.insert(0, new_head)

        if len(self.positions) > 1:
            self.positions.pop()

    def grow(self):
        """Рост змейки."""
        self.positions.append(self.last)

    def check_collision(self):
        """Проверяет столкновение с собой."""
        return self.get_head_position() in self.positions[1:]

    def reset(self):
        """Сброс змейки после столкновения."""
        start = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        self.positions = [start]
        self.direction = RIGHT
        self.next_direction = None
        self.last = None

    def eats_apple(self, apple):
        """Проверяет, съела ли змейка яблоко."""
        head_rect = pygame.Rect(
            self.get_head_position()[0],
            self.get_head_position()[1],
            GRID_SIZE,
            GRID_SIZE
        )
        apple_rect = pygame.Rect(
            apple.position[0],
            apple.position[1],
            GRID_SIZE,
            GRID_SIZE
        )
        return head_rect.colliderect(apple_rect)

    def draw(self, surface):
        """Отрисовка змейки."""
        for position in self.positions:
            rect = pygame.Rect(
                position[0],
                position[1],
                GRID_SIZE,
                GRID_SIZE
            )
            pygame.draw.rect(surface, self.body_color, rect)


def handle_keys(snake):
    """Обрабатывает нажатия клавиш."""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                snake.update_direction(UP)
            elif event.key == pygame.K_DOWN:
                snake.update_direction(DOWN)
            elif event.key == pygame.K_LEFT:
                snake.update_direction(LEFT)
            elif event.key == pygame.K_RIGHT:
                snake.update_direction(RIGHT)
    return True


def update_game_state(snake, apple):
    """Обновляет состояние игры."""
    snake.move()

    if snake.check_collision():
        snake.reset()
        apple.randomize_position()
        while apple.position in snake.positions:
            apple.randomize_position()

    if snake.eats_apple(apple):
        snake.grow()
        apple.randomize_position()
        while apple.position in snake.positions:
            apple.randomize_position()


def main():
    """Основная функция игры."""
    pygame.init()
    pygame.display.set_caption('Изгиб Питона')

    snake = Snake()
    apple = Apple()

    running = True
    while running:
        running = handle_keys(snake)
        if not running:
            break

        update_game_state(snake, apple)

        screen.fill(BOARD_BACKGROUND_COLOR)
        snake.draw(screen)
        apple.draw(screen)
        pygame.display.flip()
        clock.tick(8)

    pygame.quit()


if __name__ == '__main__':
    main()
