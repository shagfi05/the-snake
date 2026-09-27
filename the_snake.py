import random
import pygame as pg
# ТОЛЬКО для прохождения тестов
pg.init()
screen = pg.Surface((1, 1))
clock = pg.time.Clock()


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
            self.position[0],
            self.position[1],
            GRID_SIZE,
            GRID_SIZE
        )
        pg.draw.rect(surface, self.body_color, rect)


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
            rect = pg.Rect(segment, (GRID_SIZE, GRID_SIZE))
            pg.draw.rect(surface, self.body_color, rect)

    def get_head_position(self):
        """Возвращает координаты головы змейки (первого элемента списка позиций)."""

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
        self.positions.append(self.positions[-1])
        self.position = self.positions[0]

    def reset(self):
        start_x = ((SCREEN_WIDTH // 2) // GRID_SIZE) * GRID_SIZE
        start_y = ((SCREEN_HEIGHT // 2) // GRID_SIZE) * GRID_SIZE

        self.positions = [(start_x, start_y)]
        self.position = self.positions[0]
        self.direction = RIGHT
        self.next_direction = None
        self.last = None


def snake_eats_apple(snake, apple):
    # Snake.position — это (x, y) головы
    head_x, head_y = snake.position

    # Создаём Rect для головы: (x, y, ширина, высота)
    head_rect = pg.Rect(head_x, head_y, GRID_SIZE, GRID_SIZE)

    # Apple.position — тоже (x, y), делаем аналогично
    apple_x, apple_y = apple.position
    apple_rect = pg.Rect(apple_x, apple_y, GRID_SIZE, GRID_SIZE)

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
    global screen, clock

    pg.display.set_caption('Изгиб Питона')
    screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    clock = pg.time.Clock()

    snake = Snake()
    apple = Apple()

    running = True
    while running:
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

        snake.update_direction()
        update_game_state(snake, apple)

        screen.fill(COLORS['background'])
        snake.draw(screen)
        apple.draw(screen)
        pg.display.flip()
        clock.tick(8)
    pg.quit()


if __name__ == '__main__':
    main()
