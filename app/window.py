from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QPushButton, 
                             QLabel, QFileDialog, QSizePolicy)
from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QPixmap, QIcon
from PyQt6.QtMultimedia import QMediaPlayer

from app.timer import TimerHandler
from app.audio_player import AudioPlayer

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Timusic")
        self.setMinimumSize(150, 150)
        self.setMaximumSize(200, 300)
        self.setStyleSheet("background-color: white; color: #333333; font-family: 'Segoe UI', sans-serif;")
        
        # condition variable 
        self.play_img_path = None
        self.stop_img_path = None
        
        # functional variable
        self.timer = TimerHandler()
        self.audio = AudioPlayer()
        
        # initialization
        self.init_ui() 
        self.setup_connections() 
        
    def init_ui(self):
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(10, 10, 10, 10)
        main_layout.setSpacing(5)
        
        # --- TOP NAV ---
        top_nav = QHBoxLayout()
        self.btn_folder = QPushButton("Music")
        self.btn_play_img = QPushButton("I-Play")
        self.btn_stop_img = QPushButton("I-Stop")
        
        for btn in (self.btn_folder, self.btn_play_img, self.btn_stop_img):
            btn.setStyleSheet("background-color: #f0f0f0; border: 1px solid #ccc; border-radius: 4px; padding: 4px; font-size: 11px;")
            btn.setCursor(Qt.CursorShape.PointingHandCursor)
        
        top_nav.addWidget(self.btn_folder)
        top_nav.addWidget(self.btn_play_img)
        top_nav.addWidget(self.btn_stop_img)
        main_layout.addLayout(top_nav)

        # --- CENTER ---
        self.center_label = QLabel("Click to Play/Pause")
        self.center_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.center_label.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.center_label.setStyleSheet("border: 1px dashed #ccc; border-radius: 8px; font-weight: bold; color: #888; font-size: 12px;")
        self.center_label.setCursor(Qt.CursorShape.PointingHandCursor)
        self.center_label.mousePressEvent = self.on_center_click
        main_layout.addWidget(self.center_label)
        
        # Timer Display
        self.timer_label = QLabel("00:00.00")
        self.timer_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.timer_label.setStyleSheet("font-size: 24px; font-weight: bold; color: #222; margin: 2px 0px;")
        main_layout.addWidget(self.timer_label)
        

        # --- BOTTOM CONTROLS ---
        bottom_layout = QHBoxLayout()
        
        # Audio controls
        self.btn_prev = QPushButton("<<") #⏮
        self.btn_next = QPushButton(">>") #⏭   
        
        # Timer controls
        self.btn_t_start = QPushButton("▶")
        self.btn_t_pause = QPushButton("P") #⏸
        self.btn_t_reset = QPushButton("■")
        
        for btn in (self.btn_prev, self.btn_t_start, self.btn_t_pause, self.btn_t_reset, self.btn_next):
            btn.setStyleSheet("background-color: #f0f0f0; border: none; font-size: 14px; padding: 5px; border-radius: 4px;")
            btn.setCursor(Qt.CursorShape.PointingHandCursor)
            
        bottom_layout.addWidget(self.btn_prev)
        bottom_layout.addStretch()
        bottom_layout.addWidget(self.btn_t_start)
        bottom_layout.addWidget(self.btn_t_pause)
        bottom_layout.addWidget(self.btn_t_reset)
        bottom_layout.addStretch()
        bottom_layout.addWidget(self.btn_next)
        
        main_layout.addLayout(bottom_layout)
        
    def setup_connections(self):
        # Top Nav
        self.btn_folder.clicked.connect(self.select_folder)
        self.btn_play_img.clicked.connect(lambda: self.select_image('play'))
        self.btn_stop_img.clicked.connect(lambda: self.select_image('stop'))
        
        # Audio Player
        self.btn_prev.clicked.connect(self.audio.prev_track)
        self.btn_next.clicked.connect(self.audio.next_track)
        self.audio.playback_state_changed.connect(self.update_image_state)
        
        # Timer
        self.timer.tick.connect(self.timer_label.setText)
        self.btn_t_start.clicked.connect(self.timer.start)
        self.btn_t_pause.clicked.connect(self.timer.pause)
        self.btn_t_reset.clicked.connect(self.timer.reset)
        
    def on_center_click(self, event):
        self.audio.toggle_play_pause()
        
    def select_folder(self):
        folder = QFileDialog.getExistingDirectory(self, "Select Music Folder")
        if folder:
            self.audio.load_folder(folder)
            
    def select_image(self, state):
        file, _ = QFileDialog.getOpenFileName(self, f"Select {state.capitalize()} Image", "", "Images (*.png *.jpg *.jpeg)")
        if file:
            if state == 'play':
                self.play_img_path = file
            else:
                self.stop_img_path = file
            self.update_image_state(self.audio.player.playbackState() == QMediaPlayer.PlaybackState.PlayingState)
                
    def update_image_state(self, is_playing):
        img_path = self.play_img_path if is_playing else self.stop_img_path
        
        if img_path:
            pixmap = QPixmap(img_path)
            # Maximum available space for image is approx 180x150 considering other widgets
            scaled_pixmap = pixmap.scaled(180, 160, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
            self.center_label.setPixmap(scaled_pixmap)
            self.center_label.setStyleSheet("border: none;")
            
            # Adjust window size
            w = max(180, scaled_pixmap.width() + 20)
            h = max(240, scaled_pixmap.height() + 140)
            self.resize(min(w, 200), min(h, 300))
        else:
            self.center_label.clear()
            self.center_label.setText("Playing" if is_playing else "Stopped")
            self.center_label.setStyleSheet("border: 1px dashed #ccc; border-radius: 8px; font-weight: bold; color: #888; font-size: 12px;")
            self.resize(180, 240)
