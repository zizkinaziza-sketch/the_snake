"""Игра змейка"""

import random
from random import randint

import pygame

# Константы для размеров поля и сетки:
SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE

# Направления движения:
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

# Цвета:
BOARD_BACKGROUND_COLOR = (0, 0, 0)
BORDER_COLOR = (93, 216, 228)
APPLE_COLOR = (255, 0, 0)
SNAKE_COLOR = (0, 255, 0)

# Скорость:
SPEED = 10

# Инициализация PyGame и экрана:
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)
pygame.display.set_caption("Змейка")
clock = pygame.time.Clock()


# --- Базовый класс ---
class GameObject:
    """Базовый класс объекта, от которого наследуются все остальные объекты"""

    def __init__(self, position=(0, 0), color=(255, 255, 255)):
        """Инициализирует объект"""
        self.position = position
        self.body_color = color

    def draw(self):
        """Отрисовывает объект. Переопределяется в классах наследниках"""
        pass


# --- Класс яблока ---
class Apple(GameObject):
    """Яблоко, которое съедает змейка"""

    def __init__(self):
        """Конструктор клааса"""
        super().__init__(self.randomize_position(), APPLE_COLOR)

    @staticmethod
    def randomize_position():
        """
        Статический метод, который рандомно в пределах экрана

        выбирает новые координаты яблока
        """
        x = randint(0, GRID_WIDTH - 1) * GRID_SIZE
        y = randint(0, GRID_HEIGHT - 1) * GRID_SIZE
        return (x, y)

    def draw(self):
        """Отрисовка яблока"""
        rect = pygame.Rect(self.position, (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, rect)
        pygame.draw.rect(screen, BORDER_COLOR, rect, 1)


# --- Класс змейки ---
class Snake(GameObject):
    """Сама змейка"""

    def __init__(self):
        """Конструктор змейки"""
        center = screen.get_rect().center
        x = center[0] // GRID_SIZE * GRID_SIZE
        y = center[1] // GRID_SIZE * GRID_SIZE
        super().__init__((x, y), SNAKE_COLOR)
        self.positions = [self.position]
        self.length = 1
        self.direction = RIGHT
        self.next_direction = None

    def draw(self):
        """Отрисовка змейки на поле"""
        for position in self.positions:
            rect = pygame.Rect(position, (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(screen, self.body_color, rect)
            pygame.draw.rect(screen, BORDER_COLOR, rect, 1)

    @property
    def get_head_position(self):
        """
        Возвращает позицию

        головы змейки
        """
        return self.positions[0]

    def reset(self):
        """
        При столкновении с самой собой змейка
        сбрасывается в начальное положение
        """
        center = screen.get_rect().center
        x = center[0] // GRID_SIZE * GRID_SIZE
        y = center[1] // GRID_SIZE * GRID_SIZE
        self.length = 1
        self.position = (x, y)
        self.positions = [(x, y)]
        self.direction = random.choice([UP, DOWN, LEFT, RIGHT])

    def move(self, apple):
        """Метод отвечает за движение змейки и обновление координат яблока"""
        x, y = self.get_head_position
        dx, dy = self.direction
        new_pos = (
            (x + dx * GRID_SIZE) % SCREEN_WIDTH,
            (y + dy * GRID_SIZE) % SCREEN_HEIGHT,
        )

        ate_apple = False
        if new_pos == apple.position:
            self.length += 1
            ate_apple = True

        self.positions.insert(0, new_pos)

        if new_pos in self.positions[1:]:
            self.reset()
            return apple

        if len(self.positions) > self.length:
            self.positions.pop(-1)

        if ate_apple:
            return Apple()

        return apple

    def update_direction(self):
        """Метод отвечает за обновление направления движения змейки"""
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None


# --- Обработка клавиш ---
def handle_keys(game_object):
    """Обработка клавиш"""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            raise SystemExit
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and game_object.direction != DOWN:
                game_object.next_direction = UP
            elif event.key == pygame.K_DOWN and game_object.direction != UP:
                game_object.next_direction = DOWN
            elif event.key == pygame.K_LEFT and game_object.direction != RIGHT:
                game_object.next_direction = LEFT
            elif event.key == pygame.K_RIGHT and game_object.direction != LEFT:
                game_object.next_direction = RIGHT


def main():
    """Главный метод"""
    snake = Snake()
    apple = Apple()
    while True:
        clock.tick(SPEED)

        handle_keys(snake)
        snake.update_direction()

        apple = snake.move(apple)
        screen.fill(BOARD_BACKGROUND_COLOR)
        apple.draw()
        snake.draw()

        pygame.display.update()


if __name__ == "__main__":
    main()
