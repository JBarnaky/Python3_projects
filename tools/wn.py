import time
import numpy as np
import pygame


class WhiteNoiseGenerator:
    """Класс для генерации белого шума в Pygame"""

    def __init__(self, width=1920, height=1080, fps=60):
        """
        Инициализация параметров

        Args:
            width (int): Ширина экрана (по умолчанию 1920)
            height (int): Высота экрана (по умолчанию 1080)
            fps (int): Частота кадров (по умолчанию 60)
        """
        self.width = width
        self.height = height
        self.fps = fps
        self.screen = None
        self.clock = None
        self.running = False

    def _initialize(self):
        """Инициализация Pygame и экрана"""
        pygame.init()
        self.screen = pygame.display.set_mode((self.width, self.height))
        self.clock = pygame.time.Clock()

    def _generate_noise(self):
        """Генерация белого шума"""
        return np.random.randint(
            0, 256, (self.height, self.width, 3), dtype=np.uint8
        )

    def _process_events(self):
        """Обработка событий Pygame"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

    def _render_frame(self, noise_array):
        """Рендеринг кадра"""
        noise_surface = pygame.surfarray.make_surface(noise_array)
        scaled_surface = pygame.transform.scale(
            noise_surface, (self.width, self.height)
        )
        self.screen.blit(scaled_surface, (0, 0))
        pygame.display.flip()

    def run(self):
        """Запуск основного цикла"""
        self._initialize()
        self.running = True

        try:
            while self.running:
                self._process_events()
                noise = self._generate_noise()
                self._render_frame(noise)
                self.clock.tick(self.fps)
        finally:
            self.cleanup()

    def cleanup(self):
        """Очистка ресурсов"""
        if self.screen:
            pygame.display.quit()
        pygame.quit()


def main():
    """Функция для запуска как скрипта"""
    generator = WhiteNoiseGenerator()
    generator.run()


if __name__ == "__main__":
    main()
