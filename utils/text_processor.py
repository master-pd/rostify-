#!/usr/bin/env python3
"""
Text Processing Utilities for Roastify Bot
Handles text sanitization, analysis, and processing
"""

import re
import logging
from typing import Dict, List, Any, Optional, Tuple
import emoji

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class TextProcessor:
    """Text processing and analysis utilities"""
    
    def __init__(self):
        """Initialize text processor"""
        # Bengali stop words
        self.bengali_stopwords = {
            'আমি', 'তুমি', 'সে', 'আমরা', 'তোমরা', 'তারা',
            'একটি', 'কয়েকটি', 'সব', 'কিছু', 'কোনো',
            'এবং', 'বা', 'কিন্তু', 'যদি', 'তাহলে',
            'হয়', 'হয়েছে', 'হচ্ছে', 'হবে',
            'না', 'নেই', 'কি', 'কেন', 'কখন', 'কোথায়'
        }
        
        # Sensitive words to filter
        self.sensitive_words = {
            # Add sensitive Bengali words that should be filtered
            'গালি', 'অপমান', 'অশ্লীল', 'গঞ্জনা'
        }
        
        logger.info("Text Processor initialized")
    
    def sanitize_text(self, text: str, remove_links: bool = True,
                     remove_sensitive: bool = True,
                     normalize_whitespace: bool = True) -> str:
        """Sanitize input text"""
        if not text:
            return ""
        
        # Remove links if requested
        if remove_links:
            text = self._remove_links(text)
        
        # Remove sensitive words if requested
        if remove_sensitive:
            text = self._remove_sensitive_words(text)
        
        # Normalize whitespace if requested
        if normalize_whitespace:
            text = self._normalize_whitespace(text)
        
        # Remove excessive punctuation
        text = self._normalize_punctuation(text)
        
        # Trim and return
        return text.strip()
    
    def _remove_links(self, text: str) -> str:
        """Remove URLs and links from text"""
        # URL pattern
        url_pattern = r'https?://\S+|www\.\S+'
        text = re.sub(url_pattern, '', text)
        
        # Telegram-specific links
        telegram_pattern = r't\.me/\S+|@\S+bot'
        text = re.sub(telegram_pattern, '', text)
        
        return text
    
    def _remove_sensitive_words(self, text: str) -> str:
        """Remove sensitive words from text"""
        words = text.split()
        filtered_words = [
            word for word in words 
            if word.lower() not in self.sensitive_words
        ]
        
        return ' '.join(filtered_words)
    
    def _normalize_whitespace(self, text: str) -> str:
        """Normalize whitespace in text"""
        # Replace multiple spaces with single space
        text = re.sub(r'\s+', ' ', text)
        
        # Remove leading/trailing whitespace
        text = text.strip()
        
        return text
    
    def _normalize_punctuation(self, text: str) -> str:
        """Normalize punctuation in text"""
        # Replace multiple punctuation with single
        text = re.sub(r'([!?.]){2,}', r'\1', text)
        
        # Add space after punctuation if missing
        text = re.sub(r'([!?.])([^\s])', r'\1 \2', text)
        
        return text
    
    def analyze_text(self, text: str) -> Dict[str, Any]:
        """Analyze text for various characteristics"""
        if not text:
            return {}
        
        analysis = {
            "length": len(text),
            "word_count": len(text.split()),
            "char_count": len(text.replace(" ", "")),
            "has_links": self._has_links(text),
            "has_emojis": self._has_emojis(text),
            "has_mentions": self._has_mentions(text),
            "is_question": self._is_question(text),
            "is_exclamation": self._is_exclamation(text),
            "sentiment_score": self._calculate_sentiment(text),
            "complexity_score": self._calculate_complexity(text)
        }
        
        # Detect language (simple detection for Bengali/English)
        analysis["language"] = self._detect_language(text)
        
        # Extract emojis
        analysis["emojis"] = self._extract_emojis(text)
        
        # Extract keywords
        analysis["keywords"] = self._extract_keywords(text)
        
        return analysis
    
    def _has_links(self, text: str) -> bool:
        """Check if text contains links"""
        url_pattern = r'https?://|www\.'
        return bool(re.search(url_pattern, text))
    
    def _has_emojis(self, text: str) -> bool:
        """Check if text contains emojis"""
        return bool(emoji.emoji_count(text))
    
    def _has_mentions(self, text: str) -> bool:
        """Check if text contains mentions"""
        mention_pattern = r'@\w+'
        return bool(re.search(mention_pattern, text))
    
    def _is_question(self, text: str) -> bool:
        """Check if text is a question"""
        text = text.strip()
        
        # Check for question marks
        if '?' in text:
            return True
        
        # Check for Bengali question words
        question_words = ['কি', 'কেন', 'কখন', 'কোথায়', 'কেমন', 'কত']
        first_word = text.split()[0] if text.split() else ""
        
        return first_word in question_words
    
    def _is_exclamation(self, text: str) -> bool:
        """Check if text is an exclamation"""
        text = text.strip()
        
        # Check for exclamation marks
        if '!' in text:
            return True
        
        # Check for excited words
        excited_words = ['আহা', 'ওহ', 'বাহ', 'অসাধারণ', 'দারুন']
        
        for word in excited_words:
            if word in text.lower():
                return True
        
        return False
    
    def _calculate_sentiment(self, text: str) -> float:
        """Calculate simple sentiment score (-1 to 1)"""
        # Simple keyword-based sentiment analysis
        positive_words = {
            'ভাল', 'সুন্দর', 'দারুন', 'অসাধারণ', 'চমৎকার',
            'খুশি', 'আনন্দ', 'প্রশংসা', 'ধন্যবাদ', 'লাভ'
        }
        
        negative_words = {
            'খারাপ', 'মন্দ', 'দুঃখ', 'কষ্ট', 'বিরক্ত',
            'হতাশ', 'অসন্তুষ্ট', 'সমস্যা', 'ত্রুটি', 'ভুল'
        }
        
        words = text.lower().split()
        
        positive_count = sum(1 for word in words if word in positive_words)
        negative_count = sum(1 for word in words if word in negative_words)
        
        total_words = len(words)
        
        if total_words == 0:
            return 0
        
        sentiment = (positive_count - negative_count) / total_words
        
        # Normalize to -1 to 1 range
        return max(-1, min(1, sentiment))
    
    def _calculate_complexity(self, text: str) -> float:
        """Calculate text complexity score (0 to 1)"""
        words = text.split()
        
        if not words:
            return 0
        
        # Average word length
        avg_word_length = sum(len(word) for word in words) / len(words)
        
        # Sentence count (approximate)
        sentence_count = text.count('.') + text.count('?') + text.count('!')
        if sentence_count == 0:
            sentence_count = 1
        
        avg_sentence_length = len(words) / sentence_count
        
        # Unique word ratio
        unique_words = set(words)
        unique_ratio = len(unique_words) / len(words)
        
        # Complexity formula (simplified)
        complexity = (avg_word_length * 0.3 + 
                     avg_sentence_length * 0.4 + 
                     unique_ratio * 0.3) / 20
        
        return min(1, max(0, complexity))
    
    def _detect_language(self, text: str) -> str:
        """Detect language of text (Bengali/English/Mixed)"""
        # Count Bengali and English characters
        bengali_chars = re.findall(r'[\u0980-\u09FF]', text)
        english_chars = re.findall(r'[a-zA-Z]', text)
        
        bengali_count = len(bengali_chars)
        english_count = len(english_chars)
        
        total_chars = len(text.replace(" ", ""))
        
        if total_chars == 0:
            return "unknown"
        
        bengali_ratio = bengali_count / total_chars
        english_ratio = english_count / total_chars
        
        if bengali_ratio > 0.7:
            return "bengali"
        elif english_ratio > 0.7:
            return "english"
        else:
            return "mixed"
    
    def _extract_emojis(self, text: str) -> List[str]:
        """Extract emojis from text"""
        return [c for c in text if c in emoji.EMOJI_DATA]
    
    def _extract_keywords(self, text: str, max_keywords: int = 5) -> List[str]:
        """Extract important keywords from text"""
        words = text.lower().split()
        
        # Remove stopwords
        filtered_words = [
            word for word in words 
            if word not in self.bengali_stopwords and len(word) > 2
        ]
        
        # Count word frequency
        from collections import Counter
        word_counts = Counter(filtered_words)
        
        # Get most common words
        keywords = [word for word, count in word_counts.most_common(max_keywords)]
        
        return keywords
    
    def wrap_text(self, text: str, max_width: int = 30) -> List[str]:
        """Wrap text into multiple lines"""
        if not text:
            return []
        
        # Split into words
        words = text.split()
        
        lines = []
        current_line = []
        current_length = 0
        
        for word in words:
            word_length = len(word)
            
            # If adding this word would exceed max width, start new line
            if current_length + word_length + len(current_line) > max_width:
                if current_line:
                    lines.append(' '.join(current_line))
                current_line = [word]
                current_length = word_length
            else:
                current_line.append(word)
                current_length += word_length
        
        # Add the last line
        if current_line:
            lines.append(' '.join(current_line))
        
        return lines
    
    def truncate_text(self, text: str, max_length: int, 
                     ellipsis: str = "...") -> str:
        """Truncate text to maximum length"""
        if len(text) <= max_length:
            return text
        
        # Try to break at word boundary
        truncated = text[:max_length]
        last_space = truncated.rfind(' ')
        
        if last_space > max_length * 0.7:  # If space found in reasonable position
            truncated = truncated[:last_space]
        
        return truncated.rstrip() + ellipsis
    
    def clean_for_filename(self, text: str, max_length: int = 50) -> str:
        """Clean text to be used as filename"""
        # Remove invalid filename characters
        cleaned = re.sub(r'[<>:"/\\|?*]', '', text)
        
        # Replace spaces with underscores
        cleaned = cleaned.replace(' ', '_')
        
        # Remove multiple underscores
        cleaned = re.sub(r'_+', '_', cleaned)
        
        # Trim to max length
        if len(cleaned) > max_length:
            cleaned = cleaned[:max_length]
        
        return cleaned.strip('_')
    
    def calculate_readability(self, text: str) -> Dict[str, float]:
        """Calculate readability scores for text"""
        words = text.split()
        sentences = re.split(r'[.!?]+', text)
        
        # Filter out empty sentences
        sentences = [s.strip() for s in sentences if s.strip()]
        
        if not words or not sentences:
            return {
                "flesch_reading_ease": 0,
                "flesch_kincaid_grade": 0,
                "gunning_fog": 0,
                "smog_index": 0
            }
        
        # Count syllables (approximate for English)
        # For Bengali, this would need different logic
        syllable_count = 0
        for word in words:
            # Simple English syllable counting
            word = word.lower()
            if len(word) <= 3:
                syllable_count += 1
            else:
                # Count vowel groups
                vowels = re.findall(r'[aeiouy]+', word)
                syllable_count += len(vowels)
        
        # Calculate metrics
        avg_sentence_length = len(words) / len(sentences)
        avg_syllables_per_word = syllable_count / len(words)
        
        # Flesch Reading Ease
        flesch = 206.835 - (1.015 * avg_sentence_length) - (84.6 * avg_syllables_per_word)
        
        # Flesch-Kincaid Grade Level
        fk_grade = (0.39 * avg_sentence_length) + (11.8 * avg_syllables_per_word) - 15.59
        
        # Gunning Fog Index (simplified)
        fog_index = 0.4 * (avg_sentence_length + (100 * avg_syllables_per_word))
        
        # SMOG Index (simplified)
        smog_index = 1.0430 * (30 * avg_syllables_per_word) ** 0.5 + 3.1291
        
        return {
            "flesch_reading_ease": max(0, min(100, flesch)),
            "flesch_kincaid_grade": max(0, fk_grade),
            "gunning_fog": max(0, fog_index),
            "smog_index": max(0, smog_index)
        }
    
    def generate_summary(self, text: str, max_sentences: int = 3) -> str:
        """Generate a summary of the text"""
        if not text:
            return ""
        
        # Split into sentences
        sentences = re.split(r'[.!?]+', text)
        sentences = [s.strip() for s in sentences if s.strip()]
        
        if len(sentences) <= max_sentences:
            return text
        
        # Simple extraction-based summary (first few sentences)
        summary_sentences = sentences[:max_sentences]
        
        # Join with proper punctuation
        summary = '. '.join(summary_sentences) + '.'
        
        return summary