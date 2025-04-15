# Laser Dodger Game using PyQt6
# Player controls a green circle to avoid falling red lasers
# Difficulty increases over time with faster and more frequent lasers

import sys
import random
from PyQt6.QtCore import Qt, QTimer, QRect
from PyQt6.QtGui import QPainter, QColor, QFont
from PyQt6.QtWidgets import QApplication, QMainWindow, QMessageBox


class LaserDodger(QMainWindow):
    def __init__(self):
        super().__init__()
        # Initialize UI and game state
        self.initUI()
        self.initGame()

    def initUI(self):
        # Set up window properties
        self.setWindowTitle('Laser Dodger')
        self.setFixedSize(400, 700)
        self.setStyleSheet("background-color: #111;")

        # Configure font for score display
        self.font = QFont()
        self.font.setPointSize(12)
        self.font.setBold(True)

    def initGame(self):
        # Player settings
        self.player_size = 30
        self.resetPlayerPosition()
        self.player_speed = 8

        # Laser settings
        self.lasers = []
        self.laser_speed = 5
        self.laser_width = 10
        self.laser_height = 60

        # Game state
        self.score = 0
        self.high_score = 0
        self.game_active = False

        # Initialize game timers
        self.initTimers()

    def initTimers(self):
        # Main game loop timer (30ms)
        self.game_timer = QTimer(self)
        self.game_timer.timeout.connect(self.updateGame)

        # Timer for spawning new lasers
        self.spawn_timer = QTimer(self)
        self.spawn_timer.timeout.connect(self.spawnLaser)

        # Timer for increasing difficulty
        self.difficulty_timer = QTimer(self)
        self.difficulty_timer.timeout.connect(self.increaseDifficulty)

    def resetPlayerPosition(self):
        # Center player at bottom of screen
        self.player_x = (self.width() - self.player_size) // 2
        self.player_y = self.height() - self.player_size - 20

    def startGame(self):
        # Reset game state
        self.lasers.clear()
        self.score = 0
        self.laser_speed = 5

        # Start all timers
        self.spawn_timer.start(800)
        self.difficulty_timer.start(1000)
        self.game_timer.start(30)

        self.game_active = True

    def spawnLaser(self):
        # Create new laser at random x position
        x_position = random.randint(0, self.width() - self.laser_width)
        self.lasers.append(QRect(x_position, 0, self.laser_width, self.laser_height))

    def updateGame(self):
        # Move all lasers down
        for laser in self.lasers[:]:
            new_top = int(laser.top() + self.laser_speed)
            laser.moveTop(new_top)

            # Remove lasers that go off screen
            if laser.top() > self.height():
                self.lasers.remove(laser)

        # Check collisions and update score
        self.checkCollision()
        self.score += 1
        self.update()

    def checkCollision(self):
        # Create player rectangle
        player_rect = QRect(self.player_x, self.player_y,
                            self.player_size, self.player_size)

        # Check collision with each laser
        for laser in self.lasers:
            if player_rect.intersects(laser):
                self.gameOver()
                break

    def gameOver(self):
        # Stop game and update high score
        self.game_active = False
        self.game_timer.stop()
        self.spawn_timer.stop()
        self.difficulty_timer.stop()

        if self.score > self.high_score:
            self.high_score = self.score

        # Show game over message
        msg = QMessageBox()
        msg.setWindowTitle("Game Over")
        msg.setText(f"Score: {self.score}\nHigh Score: {self.high_score}")
        msg.setInformativeText("Press R to restart or ESC to quit")
        msg.setStandardButtons(QMessageBox.StandardButton.Close)
        msg.exec()

    def increaseDifficulty(self):
        # Gradually increase difficulty
        self.laser_speed += 0.5
        if self.spawn_timer.interval() > 200:
            self.spawn_timer.setInterval(int(self.spawn_timer.interval() * 0.95))

    def keyPressEvent(self, event):
        # Handle keyboard input
        if not self.game_active:
            if event.key() == Qt.Key.Key_R:
                self.startGame()
            elif event.key() == Qt.Key.Key_Escape:
                self.close()
            return

        # Player movement controls
        if event.key() == Qt.Key.Key_Left and self.player_x > 0:
            self.player_x -= self.player_speed
        elif event.key() == Qt.Key.Key_Right and self.player_x < self.width() - self.player_size:
            self.player_x += self.player_speed

    def paintEvent(self, event):
        # Draw game elements
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        # Draw player (green circle)
        painter.setBrush(QColor(0, 255, 0))
        painter.drawEllipse(self.player_x, self.player_y,
                            self.player_size, self.player_size)

        # Draw all lasers (red rectangles)
        painter.setBrush(QColor(255, 50, 50))
        for laser in self.lasers:
            painter.drawRect(laser)

        # Draw score text
        painter.setPen(QColor(255, 255, 255))
        painter.setFont(self.font)
        painter.drawText(10, 30, f"Score: {self.score}")
        painter.drawText(10, 60, f"High: {self.high_score}")

        # Show start message if game not active
        if not self.game_active and not self.lasers:
            painter.drawText(self.rect(), Qt.AlignmentFlag.AlignCenter,
                             "Press R to Start")


if __name__ == '__main__':
    app = QApplication(sys.argv)
    game = LaserDodger()
    game.show()
    sys.exit(app.exec())