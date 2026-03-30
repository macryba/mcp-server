#!/usr/bin/env python3
"""
Data models for quiz functionality
"""

from dataclasses import dataclass, field
from typing import List, Optional, Dict, Any
from enum import Enum


class QuestionType(Enum):
    """Types of quiz questions"""
    MULTIPLE_CHOICE = "multiple_choice"
    DATE = "date"
    FIGURE_IDENTIFICATION = "figure_identification"
    EVENT_IDENTIFICATION = "event_identification"
    TRUE_FALSE = "true_false"
    SHORT_ANSWER = "short_answer"


class DifficultyLevel(Enum):
    """Difficulty levels for quiz questions"""
    EASY = "easy"
    MEDIUM = "medium"
    HARD = "hard"
    EXPERT = "expert"


@dataclass
class QuizQuestion:
    """
    Represents a single quiz question

    Attributes:
        question: The question text
        options: List of possible answers (for multiple choice)
        correct_answer: The correct answer
        difficulty: Difficulty level
        topic: Question topic/category
        source_url: URL of source material
        question_type: Type of question
        explanation: Explanation of the answer
        metadata: Additional metadata
    """
    question: str
    correct_answer: str
    difficulty: DifficultyLevel
    topic: str
    source_url: str
    question_type: QuestionType
    options: Optional[List[str]] = None
    explanation: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        return {
            'question': self.question,
            'options': self.options,
            'correct_answer': self.correct_answer,
            'difficulty': self.difficulty.value if isinstance(self.difficulty, DifficultyLevel) else self.difficulty,
            'topic': self.topic,
            'source_url': self.source_url,
            'question_type': self.question_type.value if isinstance(self.question_type, QuestionType) else self.question_type,
            'explanation': self.explanation,
            'metadata': self.metadata
        }


@dataclass
class QuizAnswer:
    """
    Represents an answer to a quiz question

    Attributes:
        question_url: URL of the question source
        user_answer: User's answer
        is_correct: Whether the answer is correct
        feedback: Feedback on the answer
        timestamp: When the answer was submitted
    """
    question_url: str
    user_answer: str
    is_correct: bool
    feedback: Optional[str] = None
    timestamp: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        return {
            'question_url': self.question_url,
            'user_answer': self.user_answer,
            'is_correct': self.is_correct,
            'feedback': self.feedback,
            'timestamp': self.timestamp
        }


@dataclass
class QuizSet:
    """
    Represents a set of quiz questions

    Attributes:
        questions: List of quiz questions
        topic: Overall topic
        difficulty: Difficulty level
        total_questions: Total number of questions
        metadata: Additional metadata
    """
    questions: List[QuizQuestion]
    topic: str
    difficulty: DifficultyLevel
    metadata: Dict[str, Any] = field(default_factory=dict)

    @property
    def total_questions(self) -> int:
        """Get total number of questions"""
        return len(self.questions)

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        return {
            'questions': [q.to_dict() for q in self.questions],
            'topic': self.topic,
            'difficulty': self.difficulty.value if isinstance(self.difficulty, DifficultyLevel) else self.difficulty,
            'total_questions': self.total_questions,
            'metadata': self.metadata
        }
