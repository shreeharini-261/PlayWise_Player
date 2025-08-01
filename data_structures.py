"""
Custom Data Structures Implementation for PlayWise Music Player
All implementations are from scratch to demonstrate DSA concepts
"""

class HashSet:
    """
    Custom HashSet implementation for artist blocklist
    Time Complexity: O(1) average for add, remove, contains
    Space Complexity: O(n) where n is number of elements
    """
    def __init__(self, initial_capacity=16):
        self.capacity = initial_capacity
        self.size = 0
        self.buckets = [[] for _ in range(self.capacity)]
        self.load_factor_threshold = 0.75
    
    def _hash(self, key):
        """Simple hash function using built-in hash"""
        return hash(key) % self.capacity
    
    def _resize(self):
        """Resize hash table when load factor exceeds threshold"""
        old_buckets = self.buckets
        self.capacity *= 2
        self.size = 0
        self.buckets = [[] for _ in range(self.capacity)]
        
        for bucket in old_buckets:
            for item in bucket:
                self.add(item)
    
    def add(self, item):
        """Add item to set - O(1) average"""
        if self.size >= self.capacity * self.load_factor_threshold:
            self._resize()
        
        index = self._hash(item)
        bucket = self.buckets[index]
        
        if item not in bucket:
            bucket.append(item)
            self.size += 1
    
    def remove(self, item):
        """Remove item from set - O(1) average"""
        index = self._hash(item)
        bucket = self.buckets[index]
        
        if item in bucket:
            bucket.remove(item)
            self.size -= 1
            return True
        return False
    
    def contains(self, item):
        """Check if item exists in set - O(1) average"""
        index = self._hash(item)
        return item in self.buckets[index]
    
    def to_list(self):
        """Return all items as a list"""
        items = []
        for bucket in self.buckets:
            items.extend(bucket)
        return items


class MinHeap:
    """
    Min Heap implementation for finding shortest songs
    Time Complexity: O(log n) for insert/extract, O(1) for peek
    Space Complexity: O(n)
    """
    def __init__(self):
        self.heap = []
    
    def parent(self, i):
        return (i - 1) // 2
    
    def left_child(self, i):
        return 2 * i + 1
    
    def right_child(self, i):
        return 2 * i + 2
    
    def insert(self, item):
        """Insert item maintaining min heap property - O(log n)"""
        self.heap.append(item)
        self._heapify_up(len(self.heap) - 1)
    
    def extract_min(self):
        """Extract minimum element - O(log n)"""
        if not self.heap:
            return None
        
        if len(self.heap) == 1:
            return self.heap.pop()
        
        min_val = self.heap[0]
        self.heap[0] = self.heap.pop()
        self._heapify_down(0)
        return min_val
    
    def peek(self):
        """Get minimum without removing - O(1)"""
        return self.heap[0] if self.heap else None
    
    def _heapify_up(self, i):
        """Maintain heap property upward"""
        while i > 0:
            parent_idx = self.parent(i)
            if self.heap[i] >= self.heap[parent_idx]:
                break
            self.heap[i], self.heap[parent_idx] = self.heap[parent_idx], self.heap[i]
            i = parent_idx
    
    def _heapify_down(self, i):
        """Maintain heap property downward"""
        while True:
            min_idx = i
            left = self.left_child(i)
            right = self.right_child(i)
            
            if left < len(self.heap) and self.heap[left] < self.heap[min_idx]:
                min_idx = left
            
            if right < len(self.heap) and self.heap[right] < self.heap[min_idx]:
                min_idx = right
            
            if min_idx == i:
                break
                
            self.heap[i], self.heap[min_idx] = self.heap[min_idx], self.heap[i]
            i = min_idx


class MaxHeap:
    """
    Max Heap implementation for finding longest songs
    Time Complexity: O(log n) for insert/extract, O(1) for peek
    Space Complexity: O(n)
    """
    def __init__(self):
        self.heap = []
    
    def parent(self, i):
        return (i - 1) // 2
    
    def left_child(self, i):
        return 2 * i + 1
    
    def right_child(self, i):
        return 2 * i + 2
    
    def insert(self, item):
        """Insert item maintaining max heap property - O(log n)"""
        self.heap.append(item)
        self._heapify_up(len(self.heap) - 1)
    
    def extract_max(self):
        """Extract maximum element - O(log n)"""
        if not self.heap:
            return None
        
        if len(self.heap) == 1:
            return self.heap.pop()
        
        max_val = self.heap[0]
        self.heap[0] = self.heap.pop()
        self._heapify_down(0)
        return max_val
    
    def peek(self):
        """Get maximum without removing - O(1)"""
        return self.heap[0] if self.heap else None
    
    def _heapify_up(self, i):
        """Maintain heap property upward"""
        while i > 0:
            parent_idx = self.parent(i)
            if self.heap[i] <= self.heap[parent_idx]:
                break
            self.heap[i], self.heap[parent_idx] = self.heap[parent_idx], self.heap[i]
            i = parent_idx
    
    def _heapify_down(self, i):
        """Maintain heap property downward"""
        while True:
            max_idx = i
            left = self.left_child(i)
            right = self.right_child(i)
            
            if left < len(self.heap) and self.heap[left] > self.heap[max_idx]:
                max_idx = left
            
            if right < len(self.heap) and self.heap[right] > self.heap[max_idx]:
                max_idx = right
            
            if max_idx == i:
                break
                
            self.heap[i], self.heap[max_idx] = self.heap[max_idx], self.heap[i]
            i = max_idx


class DoublyLinkedListNode:
    """Node for doubly linked list"""
    def __init__(self, data):
        self.data = data
        self.next = None
        self.prev = None


class DoublyLinkedList:
    """
    Doubly Linked List for playlist management
    Time Complexity: O(1) for add/remove at ends, O(n) for arbitrary position
    Space Complexity: O(n)
    """
    def __init__(self):
        self.head = None
        self.tail = None
        self.size = 0
    
    def add_song(self, song):
        """Add song to end of playlist - O(1)"""
        new_node = DoublyLinkedListNode(song)
        
        if not self.head:
            self.head = self.tail = new_node
        else:
            new_node.prev = self.tail
            self.tail.next = new_node
            self.tail = new_node
        
        self.size += 1
        return True
    
    def delete_song(self, index):
        """Delete song at given index - O(n)"""
        if index < 0 or index >= self.size:
            return False
        
        current = self._get_node_at_index(index)
        if not current:
            return False
        
        if current.prev:
            current.prev.next = current.next
        else:
            self.head = current.next
        
        if current.next:
            current.next.prev = current.prev
        else:
            self.tail = current.prev
        
        self.size -= 1
        return True
    
    def move_song(self, from_index, to_index):
        """Move song from one position to another - O(n)"""
        if (from_index < 0 or from_index >= self.size or 
            to_index < 0 or to_index >= self.size or 
            from_index == to_index):
            return False
        
        # Get the song to move
        song_node = self._get_node_at_index(from_index)
        if not song_node:
            return False
        
        song_data = song_node.data
        
        # Remove from current position
        self.delete_song(from_index)
        
        # Insert at new position
        self._insert_at_index(to_index if to_index < from_index else to_index - 1, song_data)
        return True
    
    def reverse_playlist(self):
        """Reverse the entire playlist - O(n)"""
        if self.size <= 1:
            return
        
        current = self.head
        while current:
            current.next, current.prev = current.prev, current.next
            current = current.prev
        
        self.head, self.tail = self.tail, self.head
    
    def _get_node_at_index(self, index):
        """Get node at specific index - O(n)"""
        if index < 0 or index >= self.size:
            return None
        
        # Optimize by starting from head or tail
        if index < self.size // 2:
            current = self.head
            for _ in range(index):
                current = current.next
        else:
            current = self.tail
            for _ in range(self.size - 1 - index):
                current = current.prev
        
        return current
    
    def _insert_at_index(self, index, song):
        """Insert song at specific index - O(n)"""
        if index == self.size:
            self.add_song(song)
            return
        
        new_node = DoublyLinkedListNode(song)
        
        if index == 0:
            new_node.next = self.head
            if self.head:
                self.head.prev = new_node
            self.head = new_node
            if not self.tail:
                self.tail = new_node
        else:
            target = self._get_node_at_index(index)
            new_node.next = target
            new_node.prev = target.prev
            target.prev.next = new_node
            target.prev = new_node
        
        self.size += 1
    
    def to_list(self):
        """Convert to Python list for easy iteration"""
        result = []
        current = self.head
        while current:
            result.append(current.data)
            current = current.next
        return result


class Stack:
    """
    Stack implementation for playback history
    Time Complexity: O(1) for all operations
    Space Complexity: O(n)
    """
    def __init__(self):
        self.items = []
    
    def push(self, item):
        """Add item to top of stack - O(1)"""
        self.items.append(item)
    
    def pop(self):
        """Remove and return top item - O(1)"""
        if not self.is_empty():
            return self.items.pop()
        return None
    
    def peek(self):
        """Return top item without removing - O(1)"""
        if not self.is_empty():
            return self.items[-1]
        return None
    
    def is_empty(self):
        """Check if stack is empty - O(1)"""
        return len(self.items) == 0
    
    def size(self):
        """Get stack size - O(1)"""
        return len(self.items)


class BSTNode:
    """Node for Binary Search Tree"""
    def __init__(self, rating):
        self.rating = rating
        self.songs = []  # List of songs with this rating
        self.left = None
        self.right = None


class BinarySearchTree:
    """
    Binary Search Tree for song ratings (1-5 stars)
    Time Complexity: O(log n) average for search/insert/delete
    Space Complexity: O(n)
    """
    def __init__(self):
        self.root = None
    
    def insert_song(self, song, rating):
        """Insert song with given rating - O(log n) average"""
        if rating < 1 or rating > 5:
            return False
        
        song.rating = rating
        self.root = self._insert_node(self.root, rating, song)
        return True
    
    def _insert_node(self, node, rating, song):
        """Recursive helper for insertion"""
        if not node:
            new_node = BSTNode(rating)
            new_node.songs.append(song)
            return new_node
        
        if rating == node.rating:
            node.songs.append(song)
        elif rating < node.rating:
            node.left = self._insert_node(node.left, rating, song)
        else:
            node.right = self._insert_node(node.right, rating, song)
        
        return node
    
    def search_by_rating(self, rating):
        """Search songs by rating - O(log n) average"""
        node = self._search_node(self.root, rating)
        return node.songs if node else []
    
    def _search_node(self, node, rating):
        """Recursive helper for search"""
        if not node or node.rating == rating:
            return node
        
        if rating < node.rating:
            return self._search_node(node.left, rating)
        else:
            return self._search_node(node.right, rating)
    
    def delete_song(self, song_id):
        """Delete song by ID from tree - O(log n) average"""
        self.root = self._delete_song_recursive(self.root, song_id)
    
    def _delete_song_recursive(self, node, song_id):
        """Recursive helper for song deletion"""
        if not node:
            return node
        
        # Remove song from current node if found
        node.songs = [s for s in node.songs if s.id != song_id]
        
        # If no songs left at this rating, remove the node
        if not node.songs:
            # Node with only right child or no child
            if not node.left:
                return node.right
            # Node with only left child
            elif not node.right:
                return node.left
            
            # Node with two children
            min_node = self._find_min(node.right)
            node.rating = min_node.rating
            node.songs = min_node.songs
            node.right = self._delete_node(node.right, min_node.rating)
        
        # Continue search in subtrees
        node.left = self._delete_song_recursive(node.left, song_id)
        node.right = self._delete_song_recursive(node.right, song_id)
        
        return node
    
    def _find_min(self, node):
        """Find minimum value node"""
        while node.left:
            node = node.left
        return node
    
    def _delete_node(self, node, rating):
        """Delete node with specific rating"""
        if not node:
            return node
        
        if rating < node.rating:
            node.left = self._delete_node(node.left, rating)
        elif rating > node.rating:
            node.right = self._delete_node(node.right, rating)
        else:
            if not node.left:
                return node.right
            elif not node.right:
                return node.left
            
            min_node = self._find_min(node.right)
            node.rating = min_node.rating
            node.songs = min_node.songs
            node.right = self._delete_node(node.right, min_node.rating)
        
        return node
    
    def get_all_ratings_count(self):
        """Get count of songs for each rating"""
        counts = {}
        self._count_ratings(self.root, counts)
        return counts
    
    def _count_ratings(self, node, counts):
        """Recursive helper for counting ratings"""
        if node:
            counts[node.rating] = len(node.songs)
            self._count_ratings(node.left, counts)
            self._count_ratings(node.right, counts)


class HashMap:
    """
    Custom HashMap implementation for instant song lookup
    Time Complexity: O(1) average for get/put/delete
    Space Complexity: O(n)
    """
    def __init__(self, initial_capacity=32):
        self.capacity = initial_capacity
        self.size = 0
        self.buckets = [[] for _ in range(self.capacity)]
        self.load_factor_threshold = 0.75
    
    def _hash(self, key):
        """Hash function for string keys"""
        return hash(key) % self.capacity
    
    def _resize(self):
        """Resize hash table when load factor exceeds threshold"""
        old_buckets = self.buckets
        self.capacity *= 2
        self.size = 0
        self.buckets = [[] for _ in range(self.capacity)]
        
        for bucket in old_buckets:
            for key, value in bucket:
                self.put(key, value)
    
    def put(self, key, value):
        """Insert key-value pair - O(1) average"""
        if self.size >= self.capacity * self.load_factor_threshold:
            self._resize()
        
        index = self._hash(key)
        bucket = self.buckets[index]
        
        # Update existing key
        for i, (k, v) in enumerate(bucket):
            if k == key:
                bucket[i] = (key, value)
                return
        
        # Add new key-value pair
        bucket.append((key, value))
        self.size += 1
    
    def get(self, key):
        """Get value by key - O(1) average"""
        index = self._hash(key)
        bucket = self.buckets[index]
        
        for k, v in bucket:
            if k == key:
                return v
        return None
    
    def delete(self, key):
        """Delete key-value pair - O(1) average"""
        index = self._hash(key)
        bucket = self.buckets[index]
        
        for i, (k, v) in enumerate(bucket):
            if k == key:
                del bucket[i]
                self.size -= 1
                return True
        return False
    
    def keys(self):
        """Get all keys"""
        result = []
        for bucket in self.buckets:
            for key, _ in bucket:
                result.append(key)
        return result
    
    def values(self):
        """Get all values"""
        result = []
        for bucket in self.buckets:
            for _, value in bucket:
                result.append(value)
        return result
