import random
<<<<<<< HEAD
import pygame as pg
#ТОЛЬКО для прохождения тестов
pg.init()
screen = pg.Surface((1, 1))
clock = pg.time.Clock()
=======
>>>>>>> 5439b67d396319517ef067e0266ea3379f58c307


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
<<<<<<< HEAD
=======

# Глобальные переменные для тестов
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pygame.time.Clock()
>>>>>>> 5439b67d396319517ef067e0266ea3379f58c307


class GameObject:
    """Базовый класс для объектов игры."""

<<<<<<< HEAD
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
        while True:
            self.position = (
                random.randint(0, GRID_WIDTH - 1) * GRID_SIZE,
                random.randint(0, GRID_HEIGHT - 1) * GRID_SIZE
            )
            if occupied_positions is None or self.position not in occupied_positions:
                break

    def draw(self, surface):
        """Отрисовка яблока."""
        rect = pg.Rect(
=======
    def __init__(self, position=(0, 0), body_color=COLORS['background']):
        self.position = position
        self.body_color = body_color

    def draw(self, surface):
        """Отрисовка объекта."""
        rect = pygame.Rect(
>>>>>>> 5439b67d396319517ef067e0266ea3379f58c307
            self.position[0],
            self.position[1],
            GRID_SIZE,
            GRID_SIZE
        )
<<<<<<< HEAD
        pg.draw.rect(surface, self.body_color, rect)

class Snake(GameObject):
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
        for segment in self.positions:
            rect = pg.Rect(segment, (GRID_SIZE, GRID_SIZE))
            pg.draw.rect(surface, self.body_color, rect)
            #pg.draw.rect(surface, COLORS['border'], rect, 1)

    def get_head_position(self):
        return self.positions[0]

    def check_collision(self):
        """Проверяет столкновения: со стенами и с собственным хвостом."""
        head_x, head_y = self.positions[0]

        # Столкновение со стенами
        if not (0 <= head_x < SCREEN_WIDTH and 0 <= head_y < SCREEN_HEIGHT):
            return True

        # Столкновение с собственным хвостом (проверяем все сегменты, кроме головы)
        for segment in self.positions[1:]:
            if segment == (head_x, head_y):
                return True

        return False

    def update_direction(self):
        if self.next_direction is not None:
            if not (
                (self.direction == RIGHT and self.next_direction == LEFT) or
                (self.direction == LEFT and self.next_direction == RIGHT) or
                (self.direction == UP and self.next_direction == DOWN) or
                (self.direction == DOWN and self.next_direction == UP)
            ):
                self.direction = self.next_direction
            self.next_direction = None

    def move(self):
        head_x, head_y = self.positions[0]
        dx, dy = self.direction
        new_head = (head_x + dx, head_y + dy)

        self.positions.insert(0, new_head)
        self.last = self.positions.pop()

        self.position = self.positions[0]

    def grow(self):
        self.positions.append(self.positions[-1])
        self.position = self.positions[0]

    def reset(self):
        start_x = ((SCREEN_WIDTH // 2) // GRID_SIZE) * GRID_SIZE
        start_y = ((SCREEN_HEIGHT // 2) // GRID_SIZE) * GRID_SIZE

        self.positions = [(start_x, start_y)]
        self.position = self.positions[0]
=======
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
>>>>>>> 5439b67d396319517ef067e0266ea3379f58c307
        self.direction = RIGHT
        self.next_direction = None
        self.last = None

<<<<<<< HEAD

def snake_eats_apple(snake, apple):
    # snake.position — это (x, y) головы
    head_x, head_y = snake.position
    
    # Создаём Rect для головы: (x, y, ширина, высота)
    head_rect = pg.Rect(head_x, head_y, GRID_SIZE, GRID_SIZE)
    
    # apple.position — тоже (x, y), делаем аналогично
    apple_x, apple_y = apple.position
    apple_rect = pg.Rect(apple_x, apple_y, GRID_SIZE, GRID_SIZE)
    
    return head_rect.colliderect(apple_rect)
=======
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
>>>>>>> 5439b67d396319517ef067e0266ea3379f58c307


def update_game_state(snake, apple):
    """Обновляет состояние игры."""
    snake.move()
<<<<<<< HEAD
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
=======

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
>>>>>>> 5439b67d396319517ef067e0266ea3379f58c307


def main():
    """Основная функция игры."""
<<<<<<< HEAD
    global screen, clock
    
    pg.display.set_caption('Изгиб Питона')
    screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    clock = pg.time.Clock()
=======
    pygame.init()
    pygame.display.set_caption('Изгиб Питона')
>>>>>>> 5439b67d396319517ef067e0266ea3379f58c307

    snake = Snake()
    apple = Apple()

    running = True
    while running:
<<<<<<< HEAD
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False
            elif event.type == pg.KEYDOWN:
                if event.key == pg.K_UP and snake.direction != DOWN:
                    snake.next_direction = UP
                elif event.key == pg.K_DOWN and snake.direction != UP:
                    snake.next_direction = DOWN
                elif event.key == pg.K_LEFT and snake.direction != RIGHT:
                    snake.next_direction = LEFT
                elif event.key == pg.K_RIGHT and snake.direction != LEFT:
                    snake.next_direction = RIGHT
=======
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
>>>>>>> 5439b67d396319517ef067e0266ea3379f58c307

        snake.update_direction()
        update_game_state(snake, apple)

        screen.fill(COLORS['background'])
        snake.draw(screen)
        apple.draw(screen)
        pg.display.flip()
        clock.tick(8)
    pg.quit()

if __name__ == '__main__':
<<<<<<< HEAD
    main()
=======
    main()
>>>>>>> 5439b67d396319517ef067e0266ea3379f58c307
