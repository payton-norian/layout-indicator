#!/usr/bin/env python3
import sys
import subprocess
from PyQt5 import QtWidgets, QtGui, QtCore

class LayoutIndicator(QtWidgets.QLabel):
    def __init__(self):
        super().__init__()
        # Настройка внешнего вида квадрата
        self.setFixedSize(40, 40)
        self.setAlignment(QtCore.Qt.AlignCenter)
        self.setFont(QtGui.QFont("Arial", 14, QtGui.QFont.Bold))
        self.setStyleSheet("background-color: black; color: white; border-radius: 4px;")

        # Переменная для хранения стартовой позиции при перетаскивании
        self._drag_position = None

        # Первичное обновление текста
        self.update_layout()

        # Безопасный таймер Qt для опроса состояния клавиатуры
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.update_layout)
        self.timer.start(1000)  # Проверка каждые 1000 мс

    def get_current_layout(self):
        try:
            out = subprocess.check_output(["xset", "q"], text=True)
            for line in out.splitlines():
                if "LED mask" in line:
                    mask_val = line.split()[-1]
                    if mask_val != "00000000" and int(mask_val, 16) & 0x1000:
                        return "RU"
                    else:
                        return "EN"
        except Exception:
            pass
        return "EN"

    def update_layout(self):
        new_text = self.get_current_layout()
        if self.text() != new_text:
            self.setText(new_text)

    # --- Логика закрытия двойным тапом ---
    def mouseDoubleClickEvent(self, event):
        if event.button() == QtCore.Qt.LeftButton:
            QtWidgets.QApplication.quit()  # Корректно завершаем приложение Qt

    # --- Логика перетаскивания окна ---
    def mousePressEvent(self, event):
        if event.button() == QtCore.Qt.LeftButton:
            self._drag_position = event.globalPos() - self.frameGeometry().topLeft()
            event.accept()

    def mouseMoveEvent(self, event):
        if event.buttons() == QtCore.Qt.LeftButton and self._drag_position is not None:
            self.move(event.globalPos() - self._drag_position)
            event.accept()

    def mouseReleaseEvent(self, event):
        if event.button() == QtCore.Qt.LeftButton:
            self._drag_position = None
            event.accept()

def main():
    app = QtWidgets.QApplication(sys.argv)
    indicator = LayoutIndicator()
    
    indicator.setWindowFlags(
        QtCore.Qt.WindowStaysOnTopHint |
        QtCore.Qt.FramelessWindowHint |
        QtCore.Qt.Tool
    )
    
    indicator.move(20, 20)
    indicator.setWindowOpacity(0.5)  # Ваша полупрозрачность 50%
    
    indicator.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()

