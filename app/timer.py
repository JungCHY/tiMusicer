from PyQt6.QtCore import QTimer, pyqtSignal, QObject

class TimerHandler(QObject):
    tick = pyqtSignal(str) # Emits the formatted time
    
    def __init__(self):
        super().__init__()
        self.timer = QTimer(self)
        self.timer.timeout.connect(self._on_tick)
        self.timer.setInterval(100) # 100ms updates
        self.elapsed_ms = 0
        self.is_running = False

    def start(self):
        self.is_running = True
        self.timer.start()

    def pause(self):
        self.is_running = False
        self.timer.stop()

    def reset(self):
        self.pause()
        self.elapsed_ms = 0
        self._emit_time()

    def _on_tick(self):
        self.elapsed_ms += 100
        self._emit_time()

    def _emit_time(self):
        total_seconds = self.elapsed_ms // 1000
        minutes = total_seconds // 60
        seconds = total_seconds % 60
        ms = (self.elapsed_ms % 1000) // 10
        self.tick.emit(f"{minutes:02d}:{seconds:02d}.{ms:02d}")
