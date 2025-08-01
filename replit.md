# PlayWise - DSA Music Player

## Overview

PlayWise is an educational music playlist management system built as a demonstration of data structures and algorithms (DSA) concepts. The application implements a complete music player backend using custom-built data structures including doubly linked lists, hash sets, stacks, binary search trees, and heaps. It features a Flask web interface that allows users to manage playlists, track playback history, filter content, and analyze performance metrics in real-time.

## User Preferences

Preferred communication style: Simple, everyday language.

## System Architecture

### Backend Architecture
- **Framework**: Flask web application with a single-threaded, development-focused architecture
- **Core Engine**: Custom `PlaylistEngine` class that orchestrates all DSA implementations
- **Data Structures**: All data structures implemented from scratch without external libraries:
  - Doubly Linked List for main playlist management
  - Stack for playback history and undo functionality
  - HashSet for artist blocklist management
  - HashMap for song lookup operations
  - Binary Search Tree for rating-based song organization
  - Min/Max Heaps for duration-based song retrieval

### Frontend Architecture
- **Template Engine**: Jinja2 templates with Bootstrap for responsive UI
- **Styling**: Bootstrap 5 with dark theme and custom CSS
- **JavaScript**: Vanilla JavaScript for client-side interactions, form validation, and dashboard auto-refresh
- **Icons**: Feather icons for consistent visual elements

### Data Model
- **Song Model**: Custom Song class with metadata including ID, title, artist, duration, rating, timestamps, and play count
- **No Database**: All data stored in memory using custom data structures for educational purposes

### Performance Monitoring
- **Operation Timing**: Built-in performance tracking for all major operations
- **Complexity Analysis**: Time and space complexity annotations throughout the codebase
- **Live Dashboard**: Real-time visualization of system performance and statistics

### Session Management
- **Flask Sessions**: Basic session handling with configurable secret key
- **Development Mode**: Debug mode enabled for development with detailed error reporting

## External Dependencies

### Python Packages
- **Flask**: Web framework for HTTP handling and template rendering
- **Werkzeug**: WSGI utilities including ProxyFix middleware for deployment compatibility

### Frontend Assets
- **Bootstrap 5**: CSS framework loaded via CDN with dark theme variant
- **Feather Icons**: Icon library loaded via CDN for consistent UI elements

### Development Tools
- **Python Logging**: Built-in logging module configured for debug-level output
- **UUID**: Standard library for unique song ID generation
- **Datetime**: Standard library for timestamp management

Note: The application intentionally avoids external database dependencies to focus on demonstrating custom data structure implementations. All persistence is handled in-memory, making it suitable for educational and demonstration purposes.