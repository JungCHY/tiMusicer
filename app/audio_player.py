import os
from PyQt6.QtMultimedia import QMediaPlayer, QAudioOutput
from PyQt6.QtCore import QUrl, pyqtSignal, QObject

class AudioPlayer(QObject):
    playback_state_changed = pyqtSignal(bool) # True if playing
    
    def __init__(self):
        super().__init__()
        self.player = QMediaPlayer()
        self.audio_output = QAudioOutput()
        self.player.setAudioOutput(self.audio_output)
        self.audio_output.setVolume(0.5)
        
        self.playlist = []
        self.current_index = -1
        
        self.player.playbackStateChanged.connect(self._on_state_changed)
        self.player.mediaStatusChanged.connect(self._on_media_status)
        
    def load_folder(self, folder_path):
        self.playlist = []
        for file in os.listdir(folder_path):
            if file.lower().endswith('.mp3'):
                self.playlist.append(os.path.join(folder_path, file))
        
        if self.playlist:
            self.current_index = 0
            self.load_track(self.current_index)
            
    def load_track(self, index):
        if 0 <= index < len(self.playlist):
            self.player.setSource(QUrl.fromLocalFile(self.playlist[index]))
            
    def toggle_play_pause(self):
        if not self.playlist:
            return
            
        if self.player.playbackState() == QMediaPlayer.PlaybackState.PlayingState:
            self.player.pause()
        else:
            self.player.play()
            
    def next_track(self):
        if not self.playlist: return
        self.current_index = (self.current_index + 1) % len(self.playlist)
        self.load_track(self.current_index)
        self.player.play()
        
    def prev_track(self):
        if not self.playlist: return
        self.current_index = (self.current_index - 1) % len(self.playlist)
        self.load_track(self.current_index)
        self.player.play()
        
    def _on_state_changed(self, state):
        is_playing = state == QMediaPlayer.PlaybackState.PlayingState
        self.playback_state_changed.emit(is_playing)
        
    def _on_media_status(self, status):
        if status == QMediaPlayer.MediaStatus.EndOfMedia:
            self.next_track()
