"""
Song model representing a music track with all necessary metadata
"""
import uuid
from datetime import datetime

class Song:
    """
    Song model with metadata for playlist management
    Time Complexity: O(1) for initialization
    Space Complexity: O(1)
    """
    def __init__(self, title, artist, duration, rating=0):
        self.id = str(uuid.uuid4())
        self.title = title
        self.artist = artist
        self.duration = duration  # in seconds
        self.rating = rating  # 1-5 stars, 0 for unrated
        self.added_at = datetime.now()
        self.play_count = 0
        
    def __str__(self):
        return f"{self.title} by {self.artist} ({self.duration}s)"
    
    def __repr__(self):
        return f"Song('{self.title}', '{self.artist}', {self.duration}, {self.rating})"
    
    def to_dict(self):
        """Convert song to dictionary for JSON serialization"""
        return {
            'id': self.id,
            'title': self.title,
            'artist': self.artist,
            'duration': self.duration,
            'rating': self.rating,
            'added_at': self.added_at.isoformat(),
            'play_count': self.play_count
        }
    
    def get_duration_formatted(self):
        """Return duration in MM:SS format"""
        minutes = self.duration // 60
        seconds = self.duration % 60
        return f"{minutes:02d}:{seconds:02d}"
