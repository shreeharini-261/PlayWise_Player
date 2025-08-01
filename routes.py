"""
Flask routes for PlayWise Music Player
Handles all web interface interactions with the playlist engine
"""

from flask import render_template, request, redirect, url_for, flash, jsonify
from app import app
from playlist_engine import PlaylistEngine
import json

# Global playlist engine instance
playlist_engine = PlaylistEngine()

@app.route('/')
def index():
    """
    Main playlist view showing current songs and controls
    """
    songs = playlist_engine.playlist.to_list()
    duration_stats = playlist_engine.get_duration_stats()
    blocked_artists = playlist_engine.artist_blocklist.to_list()
    
    return render_template('index.html', 
                         songs=songs,
                         duration_stats=duration_stats,
                         blocked_artists=blocked_artists)

@app.route('/add_song', methods=['POST'])
def add_song():
    """Add new song to playlist"""
    title = request.form.get('title', '').strip()
    artist = request.form.get('artist', '').strip()
    duration = request.form.get('duration', type=int)
    rating = request.form.get('rating', 0, type=int)
    
    if not title or not artist or not duration:
        flash('Please fill in all required fields', 'error')
        return redirect(url_for('index'))
    
    if duration <= 0:
        flash('Duration must be positive', 'error')
        return redirect(url_for('index'))
    
    success, message = playlist_engine.add_song(title, artist, duration, rating)
    
    if success:
        flash(message, 'success')
    else:
        flash(message, 'error')
    
    return redirect(url_for('index'))

@app.route('/delete_song/<int:index>')
def delete_song(index):
    """Delete song by index"""
    success, message = playlist_engine.delete_song(index)
    
    if success:
        flash(message, 'success')
    else:
        flash(message, 'error')
    
    return redirect(url_for('index'))

@app.route('/move_song', methods=['POST'])
def move_song():
    """Move song from one position to another"""
    from_index = request.form.get('from_index', type=int)
    to_index = request.form.get('to_index', type=int)
    
    if from_index is None or to_index is None:
        flash('Invalid move parameters', 'error')
        return redirect(url_for('index'))
    
    success, message = playlist_engine.move_song(from_index, to_index)
    
    if success:
        flash(message, 'success')
    else:
        flash(message, 'error')
    
    return redirect(url_for('index'))

@app.route('/reverse_playlist')
def reverse_playlist():
    """Reverse the entire playlist"""
    success, message = playlist_engine.reverse_playlist()
    flash(message, 'success')
    return redirect(url_for('index'))

@app.route('/play_song/<int:index>')
def play_song(index):
    """Play song and add to history"""
    success, message = playlist_engine.play_song(index)
    
    if success:
        flash(message, 'success')
    else:
        flash(message, 'error')
    
    return redirect(url_for('index'))

@app.route('/undo_play')
def undo_play():
    """Undo last played song"""
    success, message = playlist_engine.undo_last_play()
    
    if success:
        flash(message, 'success')
    else:
        flash(message, 'error')
    
    return redirect(url_for('index'))

@app.route('/block_artist', methods=['POST'])
def block_artist():
    """Add artist to blocklist"""
    artist = request.form.get('artist', '').strip()
    
    if not artist:
        flash('Please enter an artist name', 'error')
        return redirect(url_for('index'))
    
    success, message = playlist_engine.block_artist(artist)
    
    if success:
        flash(message, 'success')
    else:
        flash(message, 'error')
    
    return redirect(url_for('index'))

@app.route('/unblock_artist/<artist>')
def unblock_artist(artist):
    """Remove artist from blocklist"""
    success, message = playlist_engine.unblock_artist(artist)
    
    if success:
        flash(message, 'success')
    else:
        flash(message, 'error')
    
    return redirect(url_for('index'))

@app.route('/search', methods=['GET', 'POST'])
def search():
    """Search songs by title or rating"""
    if request.method == 'POST':
        search_type = request.form.get('search_type')
        query = request.form.get('query', '').strip()
        
        if search_type == 'title':
            success, song = playlist_engine.search_by_title(query)
            if success:
                flash(f"Found: {song.title} by {song.artist}", 'success')
            else:
                flash(f"No song found with title '{query}'", 'error')
        
        elif search_type == 'rating':
            try:
                rating = int(query)
                songs = playlist_engine.search_by_rating(rating)
                if songs:
                    song_names = [f"{s.title} by {s.artist}" for s in songs]
                    flash(f"Found {len(songs)} songs with {rating} stars: {', '.join(song_names)}", 'success')
                else:
                    flash(f"No songs found with {rating} stars", 'error')
            except ValueError:
                flash("Rating must be a number between 1 and 5", 'error')
    
    return redirect(url_for('index'))

@app.route('/rate_song', methods=['POST'])
def rate_song():
    """Rate a song"""
    song_id = request.form.get('song_id')
    rating = request.form.get('rating', type=int)
    
    if not song_id or not rating:
        flash('Invalid rating parameters', 'error')
        return redirect(url_for('index'))
    
    success, message = playlist_engine.rate_song(song_id, rating)
    
    if success:
        flash(message, 'success')
    else:
        flash(message, 'error')
    
    return redirect(url_for('index'))

@app.route('/sort_playlist', methods=['POST'])
def sort_playlist():
    """Sort playlist by specified criteria"""
    criteria = request.form.get('criteria', 'title')
    algorithm = request.form.get('algorithm', 'merge')
    
    success, message = playlist_engine.sort_playlist(criteria, algorithm)
    
    if success:
        flash(message, 'success')
    else:
        flash(message, 'error')
    
    return redirect(url_for('index'))

@app.route('/dashboard')
def dashboard():
    """Live dashboard showing system statistics"""
    snapshot = playlist_engine.export_snapshot()
    complexity_info = playlist_engine.get_complexity_info()
    
    return render_template('dashboard.html', 
                         snapshot=snapshot,
                         complexity_info=complexity_info)

@app.route('/api/duration_stats')
def api_duration_stats():
    """API endpoint for duration statistics (for real-time updates)"""
    stats = playlist_engine.get_duration_stats()
    return jsonify(stats)

@app.route('/api/snapshot')
def api_snapshot():
    """API endpoint for complete system snapshot"""
    snapshot = playlist_engine.export_snapshot()
    return jsonify(snapshot)

# Error handlers
@app.errorhandler(404)
def page_not_found(e):
    """Handle 404 errors"""
    return render_template('base.html', error="Page not found"), 404

@app.errorhandler(500)
def internal_server_error(e):
    """Handle 500 errors"""
    return render_template('base.html', error="Internal server error"), 500
