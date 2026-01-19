"""
Database management for Roastify Premium v15.0
"""

import json
import sqlite3
import pickle
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional, Any, Union
import logging

logger = logging.getLogger(__name__)

class DatabaseManager:
    """Manage all database operations"""
    
    def __init__(self, db_path: str = "database/roastify.db"):
        self.db_path = Path(db_path)
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self._init_database()
        logger.info("DatabaseManager initialized")
    
    def _init_database(self):
        """Initialize database tables"""
        conn = self._get_connection()
        cursor = conn.cursor()
        
        # Users table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY,
                username TEXT,
                first_name TEXT NOT NULL,
                last_name TEXT,
                join_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                is_premium BOOLEAN DEFAULT 0,
                theme TEXT DEFAULT 'diamond',
                total_roasts INTEGER DEFAULT 0,
                upvotes INTEGER DEFAULT 0,
                downvotes INTEGER DEFAULT 0,
                level INTEGER DEFAULT 1,
                xp INTEGER DEFAULT 0,
                last_active TIMESTAMP,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Roasts table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS roasts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                roast_text TEXT,
                roast_type TEXT,
                upvotes INTEGER DEFAULT 0,
                downvotes INTEGER DEFAULT 0,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users (id)
            )
        ''')
        
        # Analytics table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS analytics (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                metric_name TEXT,
                metric_value TEXT,
                recorded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users (id)
            )
        ''')
        
        # Badges table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS badges (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                badge_name TEXT,
                badge_data TEXT,
                earned_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users (id)
            )
        ''')
        
        # Cache table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS cache (
                cache_key TEXT PRIMARY KEY,
                cache_value BLOB,
                expires_at TIMESTAMP,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def _get_connection(self):
        """Get database connection"""
        return sqlite3.connect(self.db_path)
    
    def add_or_update_user(self, user_id: int, username: str = None, 
                          first_name: str = "", last_name: str = None,
                          is_premium: bool = False):
        """Add or update user in database"""
        conn = self._get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT OR REPLACE INTO users 
            (id, username, first_name, last_name, is_premium, last_active)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (user_id, username, first_name, last_name, is_premium, datetime.now()))
        
        conn.commit()
        conn.close()
    
    def get_user_stats(self, user_id: int) -> Dict:
        """Get user statistics"""
        conn = self._get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT 
                total_roasts, upvotes, downvotes, level, xp, 
                is_premium, theme, join_date
            FROM users 
            WHERE id = ?
        ''', (user_id,))
        
        row = cursor.fetchone()
        conn.close()
        
        if row:
            return {
                'total_roasts': row[0] or 0,
                'upvotes': row[1] or 0,
                'downvotes': row[2] or 0,
                'level': row[3] or 1,
                'xp': row[4] or 0,
                'is_premium': bool(row[5]),
                'theme': row[6] or 'diamond',
                'join_date': row[7] or datetime.now()
            }
        return {}
    
    def increment_user_stat(self, user_id: int, stat_name: str, amount: int = 1):
        """Increment user statistic"""
        conn = self._get_connection()
        cursor = conn.cursor()
        
        if stat_name in ['total_roasts', 'upvotes', 'downvotes']:
            cursor.execute(f'''
                UPDATE users 
                SET {stat_name} = {stat_name} + ? 
                WHERE id = ?
            ''', (amount, user_id))
        
        conn.commit()
        conn.close()
    
    def add_roast(self, user_id: int, roast_text: str, roast_type: str = "funny"):
        """Add roast to database"""
        conn = self._get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO roasts (user_id, roast_text, roast_type)
            VALUES (?, ?, ?)
        ''', (user_id, roast_text, roast_type))
        
        # Increment user's roast count
        self.increment_user_stat(user_id, 'total_roasts')
        
        conn.commit()
        conn.close()
        return cursor.lastrowid
    
    def get_user_rank(self, user_id: int) -> int:
        """Get user's rank based on upvotes"""
        conn = self._get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT id, upvotes FROM users 
            ORDER BY upvotes DESC
        ''')
        
        rows = cursor.fetchall()
        conn.close()
        
        for rank, (uid, _) in enumerate(rows, 1):
            if uid == user_id:
                return rank
        
        return 999
    
    def get_leaderboard(self, limit: int = 10) -> List[Dict]:
        """Get leaderboard"""
        conn = self._get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT id, username, first_name, total_roasts, upvotes, level
            FROM users 
            ORDER BY upvotes DESC 
            LIMIT ?
        ''', (limit,))
        
        leaderboard = []
        for row in cursor.fetchall():
            leaderboard.append({
                'id': row[0],
                'username': row[1],
                'first_name': row[2],
                'total_roasts': row[3],
                'upvotes': row[4],
                'level': row[5]
            })
        
        conn.close()
        return leaderboard
    
    def set_cache(self, key: str, value: Any, ttl_hours: int = 24):
        """Set cache value"""
        conn = self._get_connection()
        cursor = conn.cursor()
        
        expires_at = datetime.now() + timedelta(hours=ttl_hours)
        serialized = pickle.dumps(value)
        
        cursor.execute('''
            INSERT OR REPLACE INTO cache (cache_key, cache_value, expires_at)
            VALUES (?, ?, ?)
        ''', (key, serialized, expires_at))
        
        conn.commit()
        conn.close()
    
    def get_cache(self, key: str) -> Optional[Any]:
        """Get cache value"""
        conn = self._get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT cache_value, expires_at FROM cache 
            WHERE cache_key = ? AND (expires_at IS NULL OR expires_at > ?)
        ''', (key, datetime.now()))
        
        row = cursor.fetchone()
        conn.close()
        
        if row:
            return pickle.loads(row[0])
        return None
    
    def cleanup_old_data(self, days: int = 30):
        """Cleanup old data"""
        conn = self._get_connection()
        cursor = conn.cursor()
        
        cutoff_date = datetime.now() - timedelta(days=days)
        
        # Clean old cache
        cursor.execute('DELETE FROM cache WHERE expires_at < ?', (cutoff_date,))
        
        # Clean old analytics
        cursor.execute('DELETE FROM analytics WHERE recorded_at < ?', (cutoff_date,))
        
        conn.commit()
        conn.close()
        logger.info(f"Cleaned up data older than {days} days")


def get_database():
    """Get database instance"""
    return DatabaseManager()
