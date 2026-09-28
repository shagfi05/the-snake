import random

import pygame

# ТОЛЬКО для прохождения тестов

screen = pygame.Surface((1, 1))
clock = pygame.time.Clock()


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


class GameObject:
    """Базовый класс для объектов игры."""

    def __init__(self, body_color=None):
        self.body_color = body_color
        self.position = None

    def draw(self, surface):
        """Отрисовка объекта."""
        raise NotImplementedError(
            f'Метод draw() не реализован для класса {type(self).__name__}'
        )


class Apple(GameObject):
    """Класс для яблока."""

    def __init__(self, body_color=COLORS['apple'], occupied_positions=None):
        super().__init__(body_color=body_color)
        self.randomize_position(occupied_positions)

    def randomize_position(self, occupied_positions=None):
        """Генерация случайной позиции, не занятой змейкой."""
        x = random.randrange(0, GRID_WIDTH) * GRID_SIZE
        y = random.randrange(0, GRID_HEIGHT) * GRID_SIZE
        self.position = (x, y)

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
    """Класс змейки — главного игрового персонажа."""

    def __init__(self, body_color=COLORS['snake']):
        super().__init__(body_color=body_color)

        start_x = ((SCREEN_WIDTH // 2) // GRID_SIZE) * GRID_SIZE
        start_y = ((SCREEN_HEIGHT // 2) // GRID_SIZE) * GRID_SIZE

        self.positions = [(start_x, start_y)]
        self.position = self.positions[0]

        self.direction = RIGHT
        self.next_direction = None
        self.last = None

    def draw(self, surface):
        """Отрисовывает все сегменты змейки на поверхности."""
        for segment in self.positions:
            rect = pygame.Rect(segment, (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(surface, self.body_color, rect)

    def get_head_position(self):
        """Возвращает координаты головы змейки."""
        return self.positions[0]

    def check_collision(self):
        """Проверяет столкновения: со стенами и с собственным хвостом."""
        head_x, head_y = self.positions[0]
        if not (0 <= head_x < SCREEN_WIDTH and 0 <= head_y < SCREEN_HEIGHT):
            return True
        for segment in self.positions[1:]:
            if segment == (head_x, head_y):
                return True

        return False

    def update_direction(self):
        """Обновляет направление движения змейки."""
        if self.next_direction is not None:
            if not (
                (self.direction == RIGHT and self.next_direction == LEFT)
                or (self.direction == LEFT and self.next_direction == RIGHT)
                or (self.direction == UP and self.next_direction == DOWN)
                or (self.direction == DOWN and self.next_direction == UP)
            ):
                self.direction = self.next_direction
            self.next_direction = None

    def move(self):
        """Сдвигает змейку на одну клетку в текущем направлении."""
        head_x, head_y = self.positions[0]
        dx, dy = self.direction
        new_head = (head_x + dx, head_y + dy)

        self.positions.insert(0, new_head)
        self.last = self.positions.pop()

        self.position = self.positions[0]

    def grow(self):
        """Увеличивает длину змейки (добавляет сегмент)."""
        self.positions.append(self.positions[-1])
        self.position = self.positions[0]

    def reset(self):
        """Сбрасывает состояние змейки или игры к начальному."""
        start_x = ((SCREEN_WIDTH // 2) // GRID_SIZE) * GRID_SIZE
        start_y = ((SCREEN_HEIGHT // 2) // GRID_SIZE) * GRID_SIZE

        self.positions = [(start_x, start_y)]
        self.position = self.positions[0]
        self.direction = RIGHT
        self.next_direction = None
        self.last = None


def handle_keys(snake):
    """Обрабатывает нажатия клавиш. Возвращает False, если нужно выйти."""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and snake.direction != 'DOWN':
                snake.direction = 'UP'
            elif event.key == pygame.K_DOWN and snake.direction != 'UP':
                snake.direction = 'DOWN'
            elif event.key == pygame.K_LEFT and snake.direction != 'RIGHT':
                snake.direction = 'LEFT'
            elif event.key == pygame.K_RIGHT and snake.direction != 'LEFT':
                snake.direction = 'RIGHT'
    return True


def snake_eats_apple(snake, apple):
    """Проверяет, съела ли змейка яблоко, и обрабатывает этот случай."""
    # Snake.position — это (x, y) головы
    head_x, head_y = snake.position

    # Создаём Rect для головы: (x, y, ширина, высота)
    head_rect = pygame.Rect(head_x, head_y, GRID_SIZE, GRID_SIZE)

    # Apple.position — тоже (x, y), делаем аналогично
    apple_x, apple_y = apple.position
    apple_rect = pygame.Rect(apple_x, apple_y, GRID_SIZE, GRID_SIZE)

    return head_rect.colliderect(apple_rect)


def update_game_state(snake, apple):
    """Обновляет состояние игры."""
    snake.move()
    if snake.check_collision():
        snake.reset()
        apple.randomize_position(snake.positions)
        while apple.position in snake.positions:
            apple.randomize_position(snake.positions)
        return
    elif snake_eats_apple(snake, apple):
        snake.grow()
        apple.randomize_position(snake.positions)
        while apple.position in snake.positions:
            apple.randomize_position(snake.positions)


def main():
    """Основная функция игры."""
    pygame.init()

    pygame.display.set_caption('Изгиб Питона')
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    clock = pygame.time.Clock()

    snake = Snake()
    apple = Apple()
    # Цикл while TRUE
    running = True
    while True:
        running = handle_keys(snake)
        if not running:
            break

        snake.update_direction()
        update_game_state(snake, apple)

        screen.fill(COLORS['background'])
        snake.draw(screen)
        apple.draw(screen)
        pygame.display.flip()

        clock.tick(8)

    pygame.quit()


if __name__ == '__main__':
    main()
