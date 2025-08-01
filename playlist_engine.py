"""
Main Playlist Engine combining all DSA implementations
Demonstrates real-world application of data structures
"""

from data_structures import (
    HashSet, MinHeap, MaxHeap, DoublyLinkedList, 
    Stack, BinarySearchTree, HashMap
)
from models import Song
import time

class PlaylistEngine:
    """
    Complete playlist management system using custom DSA implementations
    Time and space complexity annotations provided for all methods
    """
    
    def __init__(self):
        # Core data structures
        self.playlist = DoublyLinkedList()  # Main playlist
        self.playback_history = Stack()  # Track played songs for undo
        self.artist_blocklist = HashSet()  # Blocked artists
        self.song_lookup = HashMap()  # title -> song mapping
        self.id_lookup = HashMap()  # id -> song mapping
        self.rating_tree = BinarySearchTree()  # Songs by rating
        
        # Duration tracking heaps
        self.min_duration_heap = MinHeap()  # For shortest songs
        self.max_duration_heap = MaxHeap()  # For longest songs
        
        # Statistics
        self.total_duration = 0
        self.song_count = 0
        
        # Performance tracking
        self.operation_times = {}
    
    def _time_operation(self, operation_name, func, *args, **kwargs):
        """Helper to time operations for performance analysis"""
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        
        if operation_name not in self.operation_times:
            self.operation_times[operation_name] = []
        self.operation_times[operation_name].append(end_time - start_time)
        
        return result
    
    def add_song(self, title, artist, duration, rating=0):
        """
        Add song to playlist with comprehensive data structure updates
        Time Complexity: O(log n) due to heap operations and BST insertion
        Space Complexity: O(1) additional space
        """
        # Check artist blocklist first
        if self.artist_blocklist.contains(artist.lower()):
            return False, f"Artist '{artist}' is blocked"
        
        # Create new song
        song = Song(title, artist, duration, rating)
        
        # Add to main playlist (doubly linked list)
        self.playlist.add_song(song)
        
        # Update lookup structures
        self.song_lookup.put(title.lower(), song)
        self.id_lookup.put(song.id, song)
        
        # Add to rating tree if rated
        if rating > 0:
            self.rating_tree.insert_song(song, rating)
        
        # Update duration heaps
        self.min_duration_heap.insert(duration)
        self.max_duration_heap.insert(duration)
        
        # Update statistics
        self.total_duration += duration
        self.song_count += 1
        
        return True, f"Added '{title}' by {artist}"
    
    def delete_song(self, index):
        """
        Delete song by playlist index
        Time Complexity: O(n) due to linked list traversal
        Space Complexity: O(1)
        """
        if index < 0 or index >= self.playlist.size:
            return False, "Invalid index"
        
        # Get song before deletion
        songs = self.playlist.to_list()
        if index >= len(songs):
            return False, "Index out of range"
        
        song = songs[index]
        
        # Remove from all data structures
        self.playlist.delete_song(index)
        self.song_lookup.delete(song.title.lower())
        self.id_lookup.delete(song.id)
        self.rating_tree.delete_song(song.id)
        
        # Update statistics
        self.total_duration -= song.duration
        self.song_count -= 1
        
        # Note: Heap removal is complex, we rebuild for simplicity
        self._rebuild_heaps()
        
        return True, f"Deleted '{song.title}'"
    
    def move_song(self, from_index, to_index):
        """
        Move song within playlist
        Time Complexity: O(n) due to linked list operations
        Space Complexity: O(1)
        """
        success = self.playlist.move_song(from_index, to_index)
        if success:
            return True, f"Moved song from position {from_index} to {to_index}"
        else:
            return False, "Invalid move operation"
    
    def reverse_playlist(self):
        """
        Reverse entire playlist order
        Time Complexity: O(n) - single pass through linked list
        Space Complexity: O(1) - in-place reversal
        """
        self.playlist.reverse_playlist()
        return True, "Playlist reversed"
    
    def play_song(self, index):
        """
        Simulate playing a song and add to history
        Time Complexity: O(n) for index lookup, O(1) for stack push
        Space Complexity: O(1)
        """
        songs = self.playlist.to_list()
        if index < 0 or index >= len(songs):
            return False, "Invalid song index"
        
        song = songs[index]
        
        # Add to playback history
        self.playback_history.push(song)
        song.play_count += 1
        
        return True, f"Now playing: {song.title} by {song.artist}"
    
    def undo_last_play(self):
        """
        Undo last played song - re-add to playlist if not already there
        Time Complexity: O(1) for stack pop, O(log n) for potential re-add
        Space Complexity: O(1)
        """
        if self.playback_history.is_empty():
            return False, "No songs in playback history"
        
        last_song = self.playback_history.pop()
        
        # Check if song still exists in playlist
        if not self.id_lookup.get(last_song.id):
            # Re-add to playlist
            self.add_song(last_song.title, last_song.artist, 
                         last_song.duration, last_song.rating)
            return True, f"Re-added '{last_song.title}' to playlist"
        else:
            return True, f"Undid play of '{last_song.title}'"
    
    def block_artist(self, artist):
        """
        Add artist to blocklist
        Time Complexity: O(1) average for HashSet add
        Space Complexity: O(1)
        """
        self.artist_blocklist.add(artist.lower())
        
        # Remove any existing songs by this artist
        songs_to_remove = []
        current_songs = self.playlist.to_list()
        
        for i, song in enumerate(current_songs):
            if song.artist.lower() == artist.lower():
                songs_to_remove.append(i)
        
        # Remove in reverse order to maintain indices
        for i in reversed(songs_to_remove):
            self.delete_song(i)
        
        return True, f"Blocked artist '{artist}' and removed {len(songs_to_remove)} songs"
    
    def unblock_artist(self, artist):
        """
        Remove artist from blocklist
        Time Complexity: O(1) average for HashSet remove
        Space Complexity: O(1)
        """
        success = self.artist_blocklist.remove(artist.lower())
        if success:
            return True, f"Unblocked artist '{artist}'"
        else:
            return False, f"Artist '{artist}' was not blocked"
    
    def search_by_title(self, title):
        """
        Instant song lookup by title
        Time Complexity: O(1) average for HashMap lookup
        Space Complexity: O(1)
        """
        song = self.song_lookup.get(title.lower())
        if song:
            return True, song
        else:
            return False, None
    
    def search_by_rating(self, rating):
        """
        Find songs by rating using BST
        Time Complexity: O(log n) for BST search
        Space Complexity: O(k) where k is number of songs with rating
        """
        songs = self.rating_tree.search_by_rating(rating)
        return songs
    
    def rate_song(self, song_id, rating):
        """
        Rate a song (1-5 stars)
        Time Complexity: O(log n) for BST operations
        Space Complexity: O(1)
        """
        if rating < 1 or rating > 5:
            return False, "Rating must be between 1 and 5"
        
        song = self.id_lookup.get(song_id)
        if not song:
            return False, "Song not found"
        
        # Remove from old rating if exists
        if song.rating > 0:
            self.rating_tree.delete_song(song_id)
        
        # Add to new rating
        self.rating_tree.insert_song(song, rating)
        
        return True, f"Rated '{song.title}' {rating} stars"
    
    def get_duration_stats(self):
        """
        Get playlist duration statistics using heaps
        Time Complexity: O(1) for heap peek operations
        Space Complexity: O(1)
        """
        if self.song_count == 0:
            return {
                'total_duration': 0,
                'shortest_song': None,
                'longest_song': None,
                'average_duration': 0
            }
        
        shortest = self.min_duration_heap.peek()
        longest = self.max_duration_heap.peek()
        average = self.total_duration / self.song_count
        
        return {
            'total_duration': self.total_duration,
            'shortest_song': shortest,
            'longest_song': longest,
            'average_duration': round(average, 2)
        }
    
    def sort_playlist(self, criteria='title', algorithm='merge'):
        """
        Sort playlist by various criteria using different algorithms
        Time Complexity: O(n log n) for merge/quick sort
        Space Complexity: O(n) for merge sort, O(log n) for quick sort
        """
        songs = self.playlist.to_list()
        
        if not songs:
            return False, "Playlist is empty"
        
        # Define sort key functions
        sort_keys = {
            'title': lambda s: s.title.lower(),
            'artist': lambda s: s.artist.lower(),
            'duration': lambda s: s.duration,
            'rating': lambda s: s.rating,
            'added_at': lambda s: s.added_at
        }
        
        if criteria not in sort_keys:
            return False, "Invalid sort criteria"
        
        start_time = time.time()
        
        if algorithm == 'merge':
            sorted_songs = self._merge_sort(songs, sort_keys[criteria])
        elif algorithm == 'quick':
            sorted_songs = songs.copy()
            self._quick_sort(sorted_songs, 0, len(sorted_songs) - 1, sort_keys[criteria])
        else:
            return False, "Invalid sort algorithm"
        
        sort_time = time.time() - start_time
        
        # Rebuild playlist with sorted songs
        self.playlist = DoublyLinkedList()
        for song in sorted_songs:
            self.playlist.add_song(song)
        
        return True, f"Sorted by {criteria} using {algorithm} sort in {sort_time:.4f}s"
    
    def _merge_sort(self, arr, key_func):
        """
        Merge sort implementation
        Time Complexity: O(n log n)
        Space Complexity: O(n)
        """
        if len(arr) <= 1:
            return arr
        
        mid = len(arr) // 2
        left = self._merge_sort(arr[:mid], key_func)
        right = self._merge_sort(arr[mid:], key_func)
        
        return self._merge(left, right, key_func)
    
    def _merge(self, left, right, key_func):
        """Helper function for merge sort"""
        result = []
        i, j = 0, 0
        
        while i < len(left) and j < len(right):
            if key_func(left[i]) <= key_func(right[j]):
                result.append(left[i])
                i += 1
            else:
                result.append(right[j])
                j += 1
        
        result.extend(left[i:])
        result.extend(right[j:])
        return result
    
    def _quick_sort(self, arr, low, high, key_func):
        """
        Quick sort implementation
        Time Complexity: O(n log n) average, O(n²) worst case
        Space Complexity: O(log n)
        """
        if low < high:
            pivot_index = self._partition(arr, low, high, key_func)
            self._quick_sort(arr, low, pivot_index - 1, key_func)
            self._quick_sort(arr, pivot_index + 1, high, key_func)
    
    def _partition(self, arr, low, high, key_func):
        """Helper function for quick sort partitioning"""
        pivot = key_func(arr[high])
        i = low - 1
        
        for j in range(low, high):
            if key_func(arr[j]) <= pivot:
                i += 1
                arr[i], arr[j] = arr[j], arr[i]
        
        arr[i + 1], arr[high] = arr[high], arr[i + 1]
        return i + 1
    
    def _rebuild_heaps(self):
        """Rebuild duration heaps after song deletion"""
        self.min_duration_heap = MinHeap()
        self.max_duration_heap = MaxHeap()
        
        for song in self.playlist.to_list():
            self.min_duration_heap.insert(song.duration)
            self.max_duration_heap.insert(song.duration)
    
    def export_snapshot(self):
        """
        Generate live dashboard data integrating all DSA components
        Time Complexity: O(n) for tree traversal and list operations
        Space Complexity: O(n) for data aggregation
        """
        songs = self.playlist.to_list()
        duration_stats = self.get_duration_stats()
        rating_counts = self.rating_tree.get_all_ratings_count()
        
        # Top 5 longest songs
        longest_songs = sorted(songs, key=lambda s: s.duration, reverse=True)[:5]
        
        # Most recently played (from history)
        recent_history = []
        temp_stack = Stack()
        
        # Get recent history without destroying original stack
        while not self.playback_history.is_empty():
            song = self.playback_history.pop()
            recent_history.append(song)
            temp_stack.push(song)
        
        # Restore original stack
        while not temp_stack.is_empty():
            self.playback_history.push(temp_stack.pop())
        
        return {
            'total_songs': self.song_count,
            'total_duration': self.total_duration,
            'duration_stats': duration_stats,
            'longest_songs': [song.to_dict() for song in longest_songs],
            'recent_history': [song.to_dict() for song in recent_history[:5]],
            'rating_distribution': rating_counts,
            'blocked_artists': self.artist_blocklist.to_list(),
            'performance_metrics': {
                name: {
                    'average_time': sum(times) / len(times) if times else 0,
                    'total_calls': len(times)
                } for name, times in self.operation_times.items()
            }
        }
    
    def get_complexity_info(self):
        """
        Educational method to display time/space complexity of operations
        For learning and debugging purposes
        """
        return {
            'data_structures': {
                'DoublyLinkedList': {
                    'add_song': 'O(1) time, O(1) space',
                    'delete_song': 'O(n) time, O(1) space',
                    'move_song': 'O(n) time, O(1) space',
                    'reverse_playlist': 'O(n) time, O(1) space'
                },
                'HashSet (blocklist)': {
                    'add': 'O(1) average time, O(1) space',
                    'contains': 'O(1) average time, O(1) space',
                    'remove': 'O(1) average time, O(1) space'
                },
                'HashMap (lookup)': {
                    'put': 'O(1) average time, O(1) space',
                    'get': 'O(1) average time, O(1) space',
                    'delete': 'O(1) average time, O(1) space'
                },
                'BinarySearchTree (ratings)': {
                    'insert': 'O(log n) average time, O(1) space',
                    'search': 'O(log n) average time, O(k) space for k results',
                    'delete': 'O(log n) average time, O(1) space'
                },
                'MinHeap/MaxHeap (duration)': {
                    'insert': 'O(log n) time, O(1) space',
                    'extract': 'O(log n) time, O(1) space',
                    'peek': 'O(1) time, O(1) space'
                },
                'Stack (history)': {
                    'push': 'O(1) time, O(1) space',
                    'pop': 'O(1) time, O(1) space',
                    'peek': 'O(1) time, O(1) space'
                }
            },
            'sorting_algorithms': {
                'merge_sort': 'O(n log n) time, O(n) space',
                'quick_sort': 'O(n log n) average, O(n²) worst time, O(log n) space'
            }
        }
