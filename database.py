#!/usr/bin/env python3
"""
Database models and operations for Roastify Bot
UPDATED VERSION with all required tables
"""

import sqlite3
import json
import os
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional, Tuple
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class Database:
    """Database handler for Roastify Bot - COMPLETE VERSION"""
    
    def __init__(self, db_path: str = "data/database.db"):
        """Initialize database connection"""
        os.makedirs(os.path.dirname(db_path), exist_ok=True)
        self.db_path = db_path
        self.conn = None
        self.cursor = None
        self._initialize_database()
    
    def _initialize_database(self):
        """Create ALL tables if they don't exist"""
        try:
            self.conn = sqlite3.connect(self.db_path, check_same_thread=False)
            self.cursor = self.conn.cursor()
            
            # ========== USERS TABLE ==========
            self.cursor.execute('''
                CREATE TABLE IF NOT EXISTS users (
                    user_id INTEGER PRIMARY KEY,
                    username TEXT,
                    first_name TEXT,
                    last_name TEXT,
                    roast_count INTEGER DEFAULT 0,
                    vote_count INTEGER DEFAULT 0,
                    reaction_count INTEGER DEFAULT 0,
                    last_active TIMESTAMP,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            # ========== CHATS TABLE ==========
            self.cursor.execute('''
                CREATE TABLE IF NOT EXISTS chats (
                    chat_id INTEGER PRIMARY KEY,
                    chat_type TEXT,
                    title TEXT,
                    roast_count INTEGER DEFAULT 0,
                    last_activity TIMESTAMP,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            # ========== VOTES TABLE ==========
            self.cursor.execute('''
                CREATE TABLE IF NOT EXISTS votes (
                    vote_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER,
                    chat_id INTEGER,
                    message_id INTEGER,
                    vote_type TEXT,
                    voted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (user_id) REFERENCES users (user_id)
                )
            ''')
            
            # ========== TEMPLATE USAGE TABLE ==========
            self.cursor.execute('''
                CREATE TABLE IF NOT EXISTS template_usage (
                    usage_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    template_name TEXT,
                    user_id INTEGER,
                    chat_id INTEGER,
                    used_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    votes_received INTEGER DEFAULT 0,
                    FOREIGN KEY (user_id) REFERENCES users (user_id)
                )
            ''')
            
            # ========== USER STATS TABLE ==========
            self.cursor.execute('''
                CREATE TABLE IF NOT EXISTS user_stats (
                    stat_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER,
                    stat_date DATE,
                    roasts_sent INTEGER DEFAULT 0,
                    roasts_received INTEGER DEFAULT 0,
                    votes_given INTEGER DEFAULT 0,
                    votes_received INTEGER DEFAULT 0,
                    reactions_sent INTEGER DEFAULT 0,
                    FOREIGN KEY (user_id) REFERENCES users (user_id),
                    UNIQUE(user_id, stat_date)
                )
            ''')
            
            # ========== COOLDOWNS TABLE ==========
            self.cursor.execute('''
                CREATE TABLE IF NOT EXISTS cooldowns (
                    cooldown_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER,
                    cooldown_type TEXT,
                    expires_at TIMESTAMP,
                    FOREIGN KEY (user_id) REFERENCES users (user_id)
                )
            ''')
            
            # ========== LEADERBOARD CACHE ==========
            self.cursor.execute('''
                CREATE TABLE IF NOT EXISTS leaderboard_cache (
                    cache_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    leaderboard_type TEXT,
                    data_json TEXT,
                    cached_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            # ========== TEMPLATE UNLOCKS TABLE ==========
            self.cursor.execute('''
                CREATE TABLE IF NOT EXISTS template_unlocks (
                    unlock_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER,
                    template_id TEXT,
                    unlocked_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (user_id) REFERENCES users (user_id),
                    UNIQUE(user_id, template_id)
                )
            ''')
            
            # ========== USER MOOD HISTORY TABLE ==========
            self.cursor.execute('''
                CREATE TABLE IF NOT EXISTS user_mood_history (
                    mood_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER,
                    mood_type TEXT,
                    confidence REAL,
                    analyzed_text TEXT,
                    analyzed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (user_id) REFERENCES users (user_id)
                )
            ''')
            
            # ========== DAILY QUOTE LOGS ==========
            self.cursor.execute('''
                CREATE TABLE IF NOT EXISTS daily_quote_logs (
                    log_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    quote_id TEXT,
                    posted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    posted_to_chat_id INTEGER,
                    reactions_received INTEGER DEFAULT 0
                )
            ''')
            
            # ========== FESTIVAL ACTIVITY LOGS ==========
            self.cursor.execute('''
                CREATE TABLE IF NOT EXISTS festival_activity (
                    activity_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    festival_id TEXT,
                    user_id INTEGER,
                    activity_type TEXT,
                    activity_data TEXT,
                    performed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (user_id) REFERENCES users (user_id)
                )
            ''')
            
            # ========== FORWARD SHARE LOGS ==========
            self.cursor.execute('''
                CREATE TABLE IF NOT EXISTS forward_share_logs (
                    share_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER,
                    original_message_id INTEGER,
                    target_chat_id INTEGER,
                    shared_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    privacy_filter_applied BOOLEAN DEFAULT 1,
                    FOREIGN KEY (user_id) REFERENCES users (user_id)
                )
            ''')
            
            # ========== REACTION HISTORY ==========
            self.cursor.execute('''
                CREATE TABLE IF NOT EXISTS reaction_history (
                    reaction_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER,
                    chat_id INTEGER,
                    message_id INTEGER,
                    reaction_type TEXT,
                    reacted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (user_id) REFERENCES users (user_id)
                )
            ''')
            
            # ========== MENTION HISTORY ==========
            self.cursor.execute('''
                CREATE TABLE IF NOT EXISTS mention_history (
                    mention_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    sender_id INTEGER,
                    target_id INTEGER,
                    chat_id INTEGER,
                    message_id INTEGER,
                    mentioned_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (sender_id) REFERENCES users (user_id),
                    FOREIGN KEY (target_id) REFERENCES users (user_id)
                )
            ''')
            
            # ========== WELCOME MESSAGE LOGS ==========
            self.cursor.execute('''
                CREATE TABLE IF NOT EXISTS welcome_logs (
                    welcome_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    chat_id INTEGER,
                    user_id INTEGER,
                    welcome_type TEXT,
                    sent_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (user_id) REFERENCES users (user_id)
                )
            ''')
            
            # ========== ADMIN ACTION LOGS ==========
            self.cursor.execute('''
                CREATE TABLE IF NOT EXISTS admin_action_logs (
                    action_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    admin_id INTEGER,
                    action_type TEXT,
                    target_id INTEGER,
                    action_details TEXT,
                    performed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (admin_id) REFERENCES users (user_id)
                )
            ''')
            
            # ========== SYSTEM STATS ==========
            self.cursor.execute('''
                CREATE TABLE IF NOT EXISTS system_stats (
                    stat_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    stat_date DATE,
                    total_users INTEGER DEFAULT 0,
                    total_messages INTEGER DEFAULT 0,
                    total_roasts INTEGER DEFAULT 0,
                    total_votes INTEGER DEFAULT 0,
                    total_reactions INTEGER DEFAULT 0,
                    uptime_seconds INTEGER DEFAULT 0,
                    recorded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    UNIQUE(stat_date)
                )
            ''')
            
            # Create indexes for performance
            self._create_indexes()
            
            self.conn.commit()
            logger.info("Database initialized successfully with ALL tables")
            
        except Exception as e:
            logger.error(f"Error initializing database: {e}")
            raise
    
    def _create_indexes(self):
        """Create indexes for better performance"""
        indexes = [
            # Users table indexes
            "CREATE INDEX IF NOT EXISTS idx_users_username ON users(username)",
            "CREATE INDEX IF NOT EXISTS idx_users_roast_count ON users(roast_count)",
            "CREATE INDEX IF NOT EXISTS idx_users_last_active ON users(last_active)",
            
            # Votes table indexes
            "CREATE INDEX IF NOT EXISTS idx_votes_user_message ON votes(user_id, message_id)",
            "CREATE INDEX IF NOT EXISTS idx_votes_chat ON votes(chat_id)",
            "CREATE INDEX IF NOT EXISTS idx_votes_type ON votes(vote_type)",
            
            # Template usage indexes
            "CREATE INDEX IF NOT EXISTS idx_template_usage_name ON template_usage(template_name)",
            "CREATE INDEX IF NOT EXISTS idx_template_usage_user ON template_usage(user_id)",
            
            # User stats indexes
            "CREATE INDEX IF NOT EXISTS idx_user_stats_date ON user_stats(stat_date)",
            "CREATE INDEX IF NOT EXISTS idx_user_stats_user_date ON user_stats(user_id, stat_date)",
            
            # Cooldowns indexes
            "CREATE INDEX IF NOT EXISTS idx_cooldowns_user_type ON cooldowns(user_id, cooldown_type)",
            "CREATE INDEX IF NOT EXISTS idx_cooldowns_expires ON cooldowns(expires_at)",
            
            # Template unlocks indexes
            "CREATE INDEX IF NOT EXISTS idx_template_unlocks_user ON template_unlocks(user_id)",
            "CREATE INDEX IF NOT EXISTS idx_template_unlocks_template ON template_unlocks(template_id)",
            
            # Mood history indexes
            "CREATE INDEX IF NOT EXISTS idx_mood_history_user ON user_mood_history(user_id)",
            "CREATE INDEX IF NOT EXISTS idx_mood_history_date ON user_mood_history(analyzed_at)",
            
            # Reaction history indexes
            "CREATE INDEX IF NOT EXISTS idx_reaction_history_user ON reaction_history(user_id)",
            "CREATE INDEX IF NOT EXISTS idx_reaction_history_chat ON reaction_history(chat_id)",
            
            # Mention history indexes
            "CREATE INDEX IF NOT EXISTS idx_mention_history_sender ON mention_history(sender_id)",
            "CREATE INDEX IF NOT EXISTS idx_mention_history_target ON mention_history(target_id)",
            
            # System stats indexes
            "CREATE INDEX IF NOT EXISTS idx_system_stats_date ON system_stats(stat_date)",
        ]
        
        for index_sql in indexes:
            try:
                self.cursor.execute(index_sql)
            except Exception as e:
                logger.error(f"Error creating index: {e}")
    
    # ========== USER METHODS ==========
    
    def add_or_update_user(self, user_id: int, username: str = None, 
                          first_name: str = None, last_name: str = None):
        """Add or update user information"""
        try:
            self.cursor.execute('''
                INSERT OR REPLACE INTO users 
                (user_id, username, first_name, last_name, last_active)
                VALUES (?, ?, ?, ?, ?)
            ''', (user_id, username, first_name, last_name, datetime.now()))
            self.conn.commit()
        except Exception as e:
            logger.error(f"Error adding/updating user: {e}")
    
    def increment_roast_count(self, user_id: int):
        """Increment roast count for user"""
        try:
            self.cursor.execute('''
                UPDATE users 
                SET roast_count = roast_count + 1,
                    last_active = ?
                WHERE user_id = ?
            ''', (datetime.now(), user_id))
            self.conn.commit()
        except Exception as e:
            logger.error(f"Error incrementing roast count: {e}")
    
    def get_user(self, user_id: int) -> Optional[Tuple]:
        """Get user information"""
        try:
            self.cursor.execute('''
                SELECT * FROM users WHERE user_id = ?
            ''', (user_id,))
            return self.cursor.fetchone()
        except Exception as e:
            logger.error(f"Error getting user: {e}")
            return None
    
    def get_total_users(self) -> int:
        """Get total number of users"""
        try:
            self.cursor.execute('SELECT COUNT(*) FROM users')
            return self.cursor.fetchone()[0]
        except Exception as e:
            logger.error(f"Error getting total users: {e}")
            return 0
    
    # ========== VOTE METHODS ==========
    
    def add_vote(self, user_id: int, chat_id: int, message_id: int, vote_type: str):
        """Record a vote"""
        try:
            self.cursor.execute('''
                INSERT INTO votes (user_id, chat_id, message_id, vote_type)
                VALUES (?, ?, ?, ?)
            ''', (user_id, chat_id, message_id, vote_type))
            
            # Update user vote count
            self.cursor.execute('''
                UPDATE users 
                SET vote_count = vote_count + 1
                WHERE user_id = ?
            ''', (user_id,))
            
            self.conn.commit()
            return True
        except Exception as e:
            logger.error(f"Error adding vote: {e}")
            return False
    
    def check_vote_exists(self, user_id: int, message_id: int) -> bool:
        """Check if user already voted on a message"""
        try:
            self.cursor.execute('''
                SELECT COUNT(*) FROM votes 
                WHERE user_id = ? AND message_id = ?
            ''', (user_id, message_id))
            return self.cursor.fetchone()[0] > 0
        except Exception as e:
            logger.error(f"Error checking vote: {e}")
            return False
    
    def get_total_votes(self) -> int:
        """Get total number of votes"""
        try:
            self.cursor.execute('SELECT COUNT(*) FROM votes')
            return self.cursor.fetchone()[0]
        except Exception as e:
            logger.error(f"Error getting total votes: {e}")
            return 0
    
    # ========== TEMPLATE METHODS ==========
    
    def record_template_usage(self, template_name: str, user_id: int, chat_id: int):
        """Record template usage"""
        try:
            self.cursor.execute('''
                INSERT INTO template_usage (template_name, user_id, chat_id)
                VALUES (?, ?, ?)
            ''', (template_name, user_id, chat_id))
            self.conn.commit()
        except Exception as e:
            logger.error(f"Error recording template usage: {e}")
    
    def get_template_stats(self, template_name: str = None) -> List:
        """Get template usage statistics"""
        try:
            if template_name:
                self.cursor.execute('''
                    SELECT COUNT(*) as usage_count,
                           AVG(votes_received) as avg_votes
                    FROM template_usage
                    WHERE template_name = ?
                ''', (template_name,))
            else:
                self.cursor.execute('''
                    SELECT template_name,
                           COUNT(*) as usage_count,
                           AVG(votes_received) as avg_votes
                    FROM template_usage
                    GROUP BY template_name
                    ORDER BY usage_count DESC
                ''')
            
            return self.cursor.fetchall()
        except Exception as e:
            logger.error(f"Error getting template stats: {e}")
            return []
    
    def get_total_template_usage(self) -> int:
        """Get total template usage count"""
        try:
            self.cursor.execute('SELECT COUNT(*) FROM template_usage')
            return self.cursor.fetchone()[0]
        except Exception as e:
            logger.error(f"Error getting total template usage: {e}")
            return 0
    
    # ========== TEMPLATE UNLOCK METHODS ==========
    
    def unlock_template_for_user(self, user_id: int, template_id: str) -> bool:
        """Unlock template for user"""
        try:
            self.cursor.execute('''
                INSERT OR IGNORE INTO template_unlocks (user_id, template_id)
                VALUES (?, ?)
            ''', (user_id, template_id))
            self.conn.commit()
            return self.cursor.rowcount > 0
        except Exception as e:
            logger.error(f"Error unlocking template: {e}")
            return False
    
    def is_template_unlocked(self, user_id: int, template_id: str) -> bool:
        """Check if template is unlocked for user"""
        try:
            self.cursor.execute('''
                SELECT COUNT(*) FROM template_unlocks
                WHERE user_id = ? AND template_id = ?
            ''', (user_id, template_id))
            return self.cursor.fetchone()[0] > 0
        except Exception as e:
            logger.error(f"Error checking template unlock: {e}")
            return False
    
    def get_unlocked_templates(self, user_id: int) -> List[str]:
        """Get list of unlocked templates for user"""
        try:
            self.cursor.execute('''
                SELECT template_id FROM template_unlocks
                WHERE user_id = ?
            ''', (user_id,))
            return [row[0] for row in self.cursor.fetchall()]
        except Exception as e:
            logger.error(f"Error getting unlocked templates: {e}")
            return []
    
    # ========== MOOD HISTORY METHODS ==========
    
    def record_mood_analysis(self, user_id: int, mood_type: str, 
                            confidence: float, analyzed_text: str = None):
        """Record mood analysis result"""
        try:
            self.cursor.execute('''
                INSERT INTO user_mood_history 
                (user_id, mood_type, confidence, analyzed_text)
                VALUES (?, ?, ?, ?)
            ''', (user_id, mood_type, confidence, analyzed_text))
            self.conn.commit()
            return True
        except Exception as e:
            logger.error(f"Error recording mood analysis: {e}")
            return False
    
    def get_user_mood_history(self, user_id: int, limit: int = 50) -> List[Tuple]:
        """Get mood history for user"""
        try:
            self.cursor.execute('''
                SELECT mood_type, confidence, analyzed_at
                FROM user_mood_history
                WHERE user_id = ?
                ORDER BY analyzed_at DESC
                LIMIT ?
            ''', (user_id, limit))
            return self.cursor.fetchall()
        except Exception as e:
            logger.error(f"Error getting mood history: {e}")
            return []
    
    # ========== COOLDOWN METHODS ==========
    
    def set_cooldown(self, user_id: int, cooldown_type: str, seconds: int):
        """Set cooldown for user"""
        try:
            expires_at = datetime.now() + timedelta(seconds=seconds)
            self.cursor.execute('''
                INSERT OR REPLACE INTO cooldowns (user_id, cooldown_type, expires_at)
                VALUES (?, ?, ?)
            ''', (user_id, cooldown_type, expires_at))
            self.conn.commit()
        except Exception as e:
            logger.error(f"Error setting cooldown: {e}")
    
    def check_cooldown(self, user_id: int, cooldown_type: str) -> bool:
        """Check if user is in cooldown"""
        try:
            self.cursor.execute('''
                SELECT expires_at FROM cooldowns
                WHERE user_id = ? AND cooldown_type = ?
            ''', (user_id, cooldown_type))
            
            result = self.cursor.fetchone()
            if result:
                expires_at = datetime.fromisoformat(result[0])
                return datetime.now() < expires_at
            return False
        except Exception as e:
            logger.error(f"Error checking cooldown: {e}")
            return False
    
    # ========== LEADERBOARD METHODS ==========
    
    def get_leaderboard(self, leaderboard_type: str = "most_roasted", 
                       limit: int = 10) -> List[Tuple]:
        """Get leaderboard data"""
        try:
            if leaderboard_type == "most_roasted":
                self.cursor.execute('''
                    SELECT user_id, username, first_name, roast_count
                    FROM users
                    ORDER BY roast_count DESC
                    LIMIT ?
                ''', (limit,))
            elif leaderboard_type == "most_reacted":
                self.cursor.execute('''
                    SELECT user_id, username, first_name, reaction_count
                    FROM users
                    ORDER BY reaction_count DESC
                    LIMIT ?
                ''', (limit,))
            elif leaderboard_type == "most_votes":
                self.cursor.execute('''
                    SELECT user_id, username, first_name, vote_count
                    FROM users
                    ORDER BY vote_count DESC
                    LIMIT ?
                ''', (limit,))
            
            return self.cursor.fetchall()
        except Exception as e:
            logger.error(f"Error getting leaderboard: {e}")
            return []
    
    def cache_leaderboard(self, leaderboard_type: str, data: List):
        """Cache leaderboard data"""
        try:
            data_json = json.dumps(data)
            self.cursor.execute('''
                INSERT OR REPLACE INTO leaderboard_cache (leaderboard_type, data_json)
                VALUES (?, ?)
            ''', (leaderboard_type, data_json))
            self.conn.commit()
        except Exception as e:
            logger.error(f"Error caching leaderboard: {e}")
    
    def get_cached_leaderboard(self, leaderboard_type: str) -> Optional[List]:
        """Get cached leaderboard data"""
        try:
            self.cursor.execute('''
                SELECT data_json FROM leaderboard_cache
                WHERE leaderboard_type = ?
                ORDER BY cached_at DESC
                LIMIT 1
            ''', (leaderboard_type,))
            
            result = self.cursor.fetchone()
            if result:
                return json.loads(result[0])
            return None
        except Exception as e:
            logger.error(f"Error getting cached leaderboard: {e}")
            return None
    
    # ========== SYSTEM STATS METHODS ==========
    
    def record_system_stats(self, stats: Dict[str, Any]):
        """Record system statistics"""
        try:
            today = datetime.now().date().isoformat()
            
            self.cursor.execute('''
                INSERT OR REPLACE INTO system_stats 
                (stat_date, total_users, total_messages, total_roasts, 
                 total_votes, total_reactions, uptime_seconds)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (
                today,
                stats.get('total_users', 0),
                stats.get('total_messages', 0),
                stats.get('total_roasts', 0),
                stats.get('total_votes', 0),
                stats.get('total_reactions', 0),
                stats.get('uptime_seconds', 0)
            ))
            
            self.conn.commit()
            return True
            
        except Exception as e:
            logger.error(f"Error recording system stats: {e}")
            return False
    
    def get_system_stats_history(self, days: int = 30) -> List[Tuple]:
        """Get system stats history"""
        try:
            cutoff_date = (datetime.now() - timedelta(days=days)).date().isoformat()
            
            self.cursor.execute('''
                SELECT stat_date, total_users, total_messages, total_roasts,
                       total_votes, total_reactions, uptime_seconds
                FROM system_stats
                WHERE stat_date >= ?
                ORDER BY stat_date ASC
            ''', (cutoff_date,))
            
            return self.cursor.fetchall()
        except Exception as e:
            logger.error(f"Error getting system stats history: {e}")
            return []
    
    # ========== CLEANUP METHODS ==========
    
    def cleanup_old_data(self, days: int = 30):
        """Cleanup old data from database"""
        try:
            cutoff_date = datetime.now() - timedelta(days=days)
            
            # Clean old cooldowns
            self.cursor.execute('''
                DELETE FROM cooldowns
                WHERE expires_at < ?
            ''', (cutoff_date,))
            
            # Clean old cache
            self.cursor.execute('''
                DELETE FROM leaderboard_cache
                WHERE cached_at < ?
            ''', (cutoff_date,))
            
            # Clean old mood history
            self.cursor.execute('''
                DELETE FROM user_mood_history
                WHERE analyzed_at < ?
            ''', (cutoff_date,))
            
            # Clean old reaction history
            self.cursor.execute('''
                DELETE FROM reaction_history
                WHERE reacted_at < ?
            ''', (cutoff_date,))
            
            self.conn.commit()
            logger.info(f"Cleaned up data older than {days} days")
            
        except Exception as e:
            logger.error(f"Error cleaning up old data: {e}")
    
    def backup_database(self, backup_path: str):
        """Create a backup of the database"""
        try:
            import shutil
            shutil.copy2(self.db_path, backup_path)
            logger.info(f"Database backed up to {backup_path}")
            return True
        except Exception as e:
            logger.error(f"Error backing up database: {e}")
            return False
    
    def close(self):
        """Close database connection"""
        if self.conn:
            self.conn.close()
            logger.info("Database connection closed")


# Global database instance
db_instance = None

def get_database() -> Database:
    """Get or create database instance"""
    global db_instance
    if db_instance is None:
        db_instance = Database()
    return db_instance