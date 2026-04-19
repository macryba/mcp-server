# Quiz Tools Documentation

**⚠️ IMPORTANT NOTICE:**

The quiz tools described in this documentation are **NOT currently implemented** on this MCP server. They were removed from the active codebase but this documentation is preserved for future reference and implementation.

This document serves as a comprehensive reference for how quiz tools **were** implemented and can be used as a guide if you wish to recreate or reintegrate quiz functionality into the MCP server in the future.

---

## Overview

The quiz tools provide automated quiz generation capabilities for Polish historical content. These tools extract information from historical sources and transform it into various types of quiz questions, making it easy to build educational applications and history trivia games.

**Key Features:**
- Multiple question types (multiple choice, date-based, figure identification, event identification)
- Difficulty levels (easy, medium, hard, expert)
- Answer validation with feedback
- Fact extraction for custom quiz generation
- Full Polish language support

## Architecture

```
Quiz Tools (tools/quiz.py)
    ↓
Search & Extract Tools
    ↓
Domain Services (Wikipedia + future sources)
    ↓
Historical Content
```

The quiz tools operate as a layer on top of the search and extract infrastructure:
1. **Search** for relevant historical content using search tools
2. **Extract** full article content using extract tools
3. **Generate** quiz questions based on the extracted content
4. **Validate** user answers against source material

## Available Tools

### 1. generate_quiz_question

Generate a single quiz question on a historical topic.

**Parameters:**
- `topic` (str): Historical topic (e.g., "Bolesław III Krzywousty", "Bitwa pod Grunwaldem")
- `difficulty` (str): Difficulty level - "easy", "medium", "hard", or "expert" (default: "medium")
- `question_type` (str): Type of question - "multiple_choice", "date", "figure_identification", or "event_identification" (default: "multiple_choice")

**Returns:**
JSON object with the quiz question structure.

**Example:**
```python
# Generate a medium difficulty multiple choice question about Grunwald
result = await generate_quiz_question(
    topic="Bitwa pod Grunwaldem",
    difficulty="medium",
    question_type="multiple_choice"
)
```

**Response Structure:**
```json
{
  "question": "Czym jest 'Bitwa pod Grunwaldem' w historii Polski?",
  "options": ["Postać historyczna", "Wydarzenie historyczne", "Miejsce historyczne", "Okres historyczny"],
  "correct_answer": "Wydarzenie historyczne",
  "correct_index": 1,
  "difficulty": "medium",
  "topic": "Bitwa pod Grunwaldem",
  "source_url": "https://pl.wikipedia.org/wiki/Bitwa_pod_Grunwaldem",
  "question_type": "multiple_choice"
}
```

### 2. generate_quiz_questions

Generate multiple quiz questions on a historical topic, automatically cycling through different question types.

**Parameters:**
- `topic` (str): Historical topic
- `count` (int): Number of questions to generate (default: 5)
- `difficulty` (str): Difficulty level (default: "medium")

**Returns:**
JSON object containing a list of quiz questions.

**Example:**
```python
# Generate 10 questions about Piast dynasty
result = await generate_quiz_questions(
    topic="Dynastia Piastów",
    count=10,
    difficulty="hard"
)
```

**Response Structure:**
```json
{
  "topic": "Dynastia Piastów",
  "difficulty": "hard",
  "count": 10,
  "questions": [
    {
      "question": "...",
      "options": [...],
      "correct_answer": "...",
      ...
    },
    ...
  ]
}
```

**Question Type Distribution:**
The tool automatically cycles through 4 question types in order:
1. Multiple choice
2. Date question
3. Figure identification
4. Event identification

For `count=5`, you would get: multiple_choice, date, figure_identification, event_identification, multiple_choice

### 3. validate_quiz_answer

Validate a user's quiz answer against the source material.

**Parameters:**
- `question_url` (str): URL of the source article used to generate the question
- `user_answer` (str): User's answer to validate

**Returns:**
JSON object with validation result and feedback.

**Example:**
```python
# Validate an answer about Grunwald
result = await validate_quiz_answer(
    question_url="https://pl.wikipedia.org/wiki/Bitwa_pod_Grunwaldem",
    user_answer="1410"
)
```

**Response Structure:**
```json
{
  "question_url": "https://pl.wikipedia.org/wiki/Bitwa_pod_Grunwaldem",
  "user_answer": "1410",
  "is_correct": true,
  "feedback": "Correct!"
}
```

**Note:** The current implementation uses simple text matching. A production system should use semantic similarity or more sophisticated NLP techniques.

### 4. extract_quiz_facts

Extract facts suitable for quiz generation from historical content.

**Parameters:**
- `topic` (str): Historical topic
- `count` (int): Number of facts to extract (default: 10)

**Returns:**
JSON object with quiz-relevant content.

**Example:**
```python
# Extract facts about Copernicus
result = await extract_quiz_facts(
    topic="Mikołaj Kopernik",
    count=15
)
```

**Response Structure:**
```json
{
  "topic": "Mikołaj Kopernik",
  "title": "Mikołaj Kopernik",
  "content": "Full article content here...",
  "url": "https://pl.wikipedia.org/wiki/Miko%C5%82aj_Kopernik",
  "note": "Structured fact extraction has been removed due to reliability concerns. Please implement custom fact extraction using the article content provided."
}
```

**Important Note:** Due to reliability concerns with regex-based extraction, structured fact extraction has been removed. The tool now returns raw article content for custom processing.

### 5. generate_multiple_choice

Convenience wrapper for generating multiple choice questions.

**Parameters:**
- `topic` (str): Historical topic
- `difficulty` (str): Difficulty level (default: "medium")

**Example:**
```python
result = await generate_multiple_choice(
    topic="Powstanie styczniowe",
    difficulty="easy"
)
```

### 6. generate_date_question

Convenience wrapper for generating date-based questions.

**Parameters:**
- `event` (str): Historical event

**Example:**
```python
result = await generate_date_question(
    event="Unia polsko-litewska"
)
```

**Current Status:** Returns an error message indicating that date question generation is disabled due to reliability concerns with structured fact extraction.

### 7. generate_figure_question

Convenience wrapper for generating figure identification questions.

**Parameters:**
- `person` (str): Historical figure name

**Example:**
```python
result = await generate_figure_question(
    person="Maria Skłodowska-Curie"
)
```

**Current Status:** Returns an error message indicating that figure question generation is disabled due to reliability concerns with structured fact extraction.

### 8. generate_event_question

Convenience wrapper for generating event identification questions.

**Parameters:**
- `description` (str): Event description

**Example:**
```python
result = await generate_event_question(
    description="Bitwa z zakonem krzyżackim"
)
```

**Current Status:** Returns an error message indicating that event question generation is disabled due to reliability concerns with structured fact extraction.

## Data Models

### QuizQuestion

Represents a single quiz question.

**Fields:**
- `question` (str): The question text
- `correct_answer` (str): The correct answer
- `difficulty` (DifficultyLevel): easy, medium, hard, or expert
- `topic` (str): Question topic/category
- `source_url` (str): URL of source material
- `question_type` (QuestionType): Type of question
- `options` (List[str], optional): List of possible answers for multiple choice
- `explanation` (str, optional): Explanation of the answer
- `metadata` (Dict): Additional metadata

### QuizAnswer

Represents a user's answer to a quiz question.

**Fields:**
- `question_url` (str): URL of the question source
- `user_answer` (str): User's answer
- `is_correct` (bool): Whether the answer is correct
- `feedback` (str, optional): Feedback on the answer
- `timestamp` (str, optional): When the answer was submitted

### QuizSet

Represents a collection of quiz questions.

**Fields:**
- `questions` (List[QuizQuestion]): List of quiz questions
- `topic` (str): Overall topic
- `difficulty` (DifficultyLevel): Difficulty level
- `total_questions` (int, read-only): Number of questions
- `metadata` (Dict): Additional metadata

### QuestionType Enum

Available question types:
- `MULTIPLE_CHOICE`: Standard multiple choice format
- `DATE`: Date-based questions
- `FIGURE_IDENTIFICATION`: Identify historical figures
- `EVENT_IDENTIFICATION`: Identify historical events
- `TRUE_FALSE`: True/false questions (planned)
- `SHORT_ANSWER`: Short answer questions (planned)

### DifficultyLevel Enum

Available difficulty levels:
- `EASY`: Basic historical knowledge
- `MEDIUM`: Standard difficulty
- `HARD`: Advanced historical knowledge
- `EXPERT`: Specialized or obscure historical knowledge

## Implementation Reference

### File Structure
```
tools/quiz.py           # Main quiz tool implementations
models/quiz.py          # Data models for quiz functionality
models/facts.py         # Historical fact and timeline models
```

### Core Functions

**Public API (MCP Tools):**
```python
async def generate_quiz_question(topic: str, difficulty: str = 'medium', question_type: str = 'multiple_choice') -> str
async def generate_quiz_questions(topic: str, count: int = 5, difficulty: str = 'medium') -> str
async def validate_quiz_answer(question_url: str, user_answer: str) -> str
async def extract_quiz_facts(topic: str, count: int = 10) -> str
async def generate_multiple_choice(topic: str, difficulty: str = 'medium') -> str
async def generate_date_question(event: str) -> str
async def generate_figure_question(person: str) -> str
async def generate_event_question(description: str) -> str
```

**Internal Helper Functions:**
```python
async def _generate_multiple_choice(article: Dict, topic: str, difficulty: str) -> Dict
async def _generate_date_question(article: Dict, topic: str, difficulty: str) -> Dict
async def _generate_figure_question(article: Dict, topic: str, difficulty: str) -> Dict
async def _generate_event_question(article: Dict, topic: str, difficulty: str) -> Dict
def _generate_wrong_dates(correct_date: str) -> List[str]
```

### Dependencies
```python
from tools.search import search_wikipedia
from tools.extract import extract_article
from models.quiz import QuizQuestion, QuestionType, DifficultyLevel
```

### Complete Implementation: models/quiz.py

```python
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
```

### Complete Implementation: tools/quiz.py

```python
#!/usr/bin/env python3
"""
Quiz generation tools for Polish history
Provides tools to generate quiz questions, validate answers, and extract quiz facts
"""

from tools.search import search_wikipedia
from tools.extract import extract_article
from models.quiz import QuizQuestion, QuestionType, DifficultyLevel
from typing import List, Dict, Any
import logging
import random

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


async def generate_quiz_question(topic: str, difficulty: str = 'medium', question_type: str = 'multiple_choice') -> str:
    """
    Generate a single quiz question on a historical topic

    Args:
        topic: Historical topic (e.g., "Bolesław III Krzywousty", "Bitwa pod Grunwaldem")
        difficulty: Difficulty level (easy, medium, hard, expert)
        question_type: Type of question (multiple_choice, date, figure_identification, event_identification)

    Returns:
        JSON string with quiz question
    """
    try:
        # Search for relevant content
        search_results = await search_wikipedia(topic, max_results=3)
        results = eval(search_results)

        if not results or 'error' in results[0]:
            return str({'error': f'Could not find information about {topic}'})

        # Get the first result
        first_result = results[0]
        url = first_result.get('url')

        # Extract article content
        article_data = await extract_article(url)
        article = eval(article_data)

        if 'error' in article:
            return str({'error': 'Could not extract article for quiz generation'})

        # Generate question based on type
        if question_type == 'multiple_choice':
            question = await _generate_multiple_choice(article, topic, difficulty)
        elif question_type == 'date':
            question = await _generate_date_question(article, topic, difficulty)
        elif question_type == 'figure_identification':
            question = await _generate_figure_question(article, topic, difficulty)
        elif question_type == 'event_identification':
            question = await _generate_event_question(article, topic, difficulty)
        else:
            question = await _generate_multiple_choice(article, topic, difficulty)

        return str(question)
    except Exception as e:
        logger.error(f"Error in generate_quiz_question: {e}")
        return str({'error': str(e)})


async def generate_quiz_questions(topic: str, count: int = 5, difficulty: str = 'medium') -> str:
    """
    Generate multiple quiz questions on a historical topic

    Args:
        topic: Historical topic
        count: Number of questions to generate
        difficulty: Difficulty level

    Returns:
        JSON string with list of quiz questions
    """
    try:
        questions = []

        # Generate different types of questions
        question_types = ['multiple_choice', 'date', 'figure_identification', 'event_identification']

        for i in range(count):
            qtype = question_types[i % len(question_types)]
            question_data = await generate_quiz_question(topic, difficulty, qtype)
            question = eval(question_data)

            if 'error' not in question:
                questions.append(question)

        result = {
            'topic': topic,
            'difficulty': difficulty,
            'count': len(questions),
            'questions': questions
        }

        return str(result)
    except Exception as e:
        logger.error(f"Error in generate_quiz_questions: {e}")
        return str({'error': str(e)})


async def validate_quiz_answer(question_url: str, user_answer: str) -> str:
    """
    Validate a quiz answer against the source material

    Args:
        question_url: URL of the source article
        user_answer: User's answer

    Returns:
        JSON string with validation result and feedback
    """
    try:
        # Get the article content
        article_data = await extract_article(question_url)
        article = eval(article_data)

        if 'error' in article:
            return str({'error': 'Could not fetch article for validation'})

        content = article.get('content', '').lower()
        user_answer_clean = user_answer.strip().lower()

        # Simple validation: check if answer appears in content
        # In a full implementation, this would use more sophisticated semantic matching
        is_correct = user_answer_clean in content

        result = {
            'question_url': question_url,
            'user_answer': user_answer,
            'is_correct': is_correct,
            'feedback': 'Correct!' if is_correct else 'Incorrect. Please review the source material.'
        }

        return str(result)
    except Exception as e:
        logger.error(f"Error in validate_quiz_answer: {e}")
        return str({'error': str(e)})


async def extract_quiz_facts(topic: str, count: int = 10) -> str:
    """
    Extract facts suitable for quiz generation

    Args:
        topic: Historical topic
        count: Number of facts to extract

    Returns:
        JSON string with quiz-relevant facts
    """
    try:
        # Search for relevant content
        search_results = await search_wikipedia(topic, max_results=1)
        results = eval(search_results)

        if not results or 'error' in results[0]:
            return str({'error': f'Could not find information about {topic}'})

        url = results[0].get('url')

        # Extract article content
        article_data = await extract_article(url)
        article = eval(article_data)

        if 'error' in article:
            return str({'error': 'Could not extract article'})

        # Since we no longer use regex-based fact extraction, return article content
        # Users can now implement their own fact extraction using reliable methods
        result = {
            'topic': topic,
            'title': article.get('title', ''),
            'content': article.get('content', ''),
            'url': url,
            'note': 'Structured fact extraction has been removed due to reliability concerns. Please implement custom fact extraction using the article content provided.'
        }

        return str(result)
    except Exception as e:
        logger.error(f"Error in extract_quiz_facts: {e}")
        return str({'error': str(e)})


async def generate_multiple_choice(topic: str, difficulty: str = 'medium') -> str:
    """
    Generate a multiple choice question

    Args:
        topic: Historical topic
        difficulty: Difficulty level

    Returns:
        JSON string with multiple choice question
    """
    return await generate_quiz_question(topic, difficulty, 'multiple_choice')


async def generate_date_question(event: str) -> str:
    """
    Generate a date-based question

    Args:
        event: Historical event

    Returns:
        JSON string with date question
    """
    return await generate_quiz_question(event, 'medium', 'date')


async def generate_figure_question(person: str) -> str:
    """
    Generate a figure identification question

    Args:
        person: Historical figure name

    Returns:
        JSON string with figure question
    """
    return await generate_quiz_question(person, 'medium', 'figure_identification')


async def generate_event_question(description: str) -> str:
    """
    Generate an event identification question

    Args:
        description: Event description

    Returns:
        JSON string with event question
    """
    return await generate_quiz_question(description, 'medium', 'event_identification')


# Helper functions

async def _generate_multiple_choice(article: Dict, topic: str, difficulty: str) -> Dict:
    """Generate a multiple choice question"""
    # Get the title from article
    title = article.get('title', topic)
    url = article.get('url', '')
    content = article.get('content', '')

    # Generate general knowledge question about the topic
    question = f"Czym jest '{title}' w historii Polski?"
    options = [
        "Postać historyczna",
        "Wydarzenie historyczne",
        "Miejsce historyczne",
        "Okres historyczny"
    ]
    random.shuffle(options)
    correct_index = 0  # Default to first option as correct

    return {
        'question': question,
        'options': options,
        'correct_answer': options[correct_index],
        'correct_index': correct_index,
        'difficulty': difficulty,
        'topic': topic,
        'source_url': url,
        'note': 'Quiz generation simplified - structured fact extraction removed due to reliability concerns',
        'question_type': 'multiple_choice'
    }


async def _generate_date_question(article: Dict, topic: str, difficulty: str) -> Dict:
    """Generate a date question"""
    title = article.get('title', topic)
    url = article.get('url', '')

    # Return error since we no longer extract dates
    return {
        'error': 'Date question generation disabled - structured fact extraction removed due to reliability concerns',
        'topic': topic,
        'source_url': url,
        'suggestion': 'Please use article content to manually extract dates or implement a reliable date extraction method'
    }


async def _generate_figure_question(article: Dict, topic: str, difficulty: str) -> Dict:
    """Generate a figure identification question"""
    title = article.get('title', topic)
    url = article.get('url', '')

    # Return error since we no longer extract figures
    return {
        'error': 'Figure question generation disabled - structured fact extraction removed due to reliability concerns',
        'topic': topic,
        'source_url': url,
        'suggestion': 'Please use article content to manually identify figures or implement a reliable figure extraction method'
    }


async def _generate_event_question(article: Dict, topic: str, difficulty: str) -> Dict:
    """Generate an event identification question"""
    title = article.get('title', topic)
    url = article.get('url', '')

    # Return error since we no longer extract events
    return {
        'error': 'Event question generation disabled - structured fact extraction removed due to reliability concerns',
        'topic': topic,
        'source_url': url,
        'suggestion': 'Please use article content to manually identify events or implement a reliable event extraction method'
    }


def _generate_wrong_dates(correct_date: str) -> List[str]:
    """Generate plausible wrong dates"""
    # Simple implementation - shift by a few years
    try:
        year = int(correct_date.split('-')[0])
        wrong_years = [year + 10, year - 10, year + 50]
        return [f"{y}-01-01" for y in wrong_years]
    except:
        return ['1900-01-01', '1800-01-01', '2000-01-01']
```

### MCP Tool Registration Pattern (server.py)

```python
# In server.py imports
from tools import search, extract, quiz

# Add these MCP tool decorators after extract tools

@mcp.tool()
async def generate_quiz_question(topic: str, difficulty: str = 'medium', question_type: str = 'multiple_choice') -> str:
    """Generate a single quiz question on a historical topic"""
    try:
        results = await quiz.generate_quiz_question(topic, difficulty, question_type)
        return results
    except Exception as e:
        logger.error(f"Error in generate_quiz_question: {e}")
        return str({'error': str(e)})

@mcp.tool()
async def generate_quiz_questions(topic: str, count: int = 5, difficulty: str = 'medium') -> str:
    """Generate multiple quiz questions on a historical topic"""
    try:
        results = await quiz.generate_quiz_questions(topic, count, difficulty)
        return results
    except Exception as e:
        logger.error(f"Error in generate_quiz_questions: {e}")
        return str({'error': str(e)})

@mcp.tool()
async def validate_quiz_answer(question_url: str, user_answer: str) -> str:
    """Validate a quiz answer against the source material"""
    try:
        results = await quiz.validate_quiz_answer(question_url, user_answer)
        return results
    except Exception as e:
        logger.error(f"Error in validate_quiz_answer: {e}")
        return str({'error': str(e)})

@mcp.tool()
async def extract_quiz_facts(topic: str, count: int = 10) -> str:
    """Extract facts suitable for quiz generation"""
    try:
        results = await quiz.extract_quiz_facts(topic, count)
        return results
    except Exception as e:
        logger.error(f"Error in extract_quiz_facts: {e}")
        return str({'error': str(e)})

@mcp.tool()
async def generate_multiple_choice(topic: str, difficulty: str = 'medium') -> str:
    """Generate a multiple choice question"""
    try:
        results = await quiz.generate_multiple_choice(topic, difficulty)
        return results
    except Exception as e:
        logger.error(f"Error in generate_multiple_choice: {e}")
        return str({'error': str(e)})
```

## Usage Examples

### Example 1: Generate a Complete Quiz

```python
import json
from tools.quiz import generate_quiz_questions, validate_quiz_answer

# Generate a 10-question quiz about the Polish-Lithuanian Commonwealth
quiz_data = await generate_quiz_questions(
    topic="Rzeczpospolita Obojga Narodów",
    count=10,
    difficulty="medium"
)

quiz = json.loads(quiz_data)

# Display questions
for i, question in enumerate(quiz['questions'], 1):
    print(f"Pytanie {i}: {question['question']}")
    if question.get('options'):
        for j, option in enumerate(question['options'], 0):
            print(f"  {j}. {option}")
    print()

# Validate an answer
answer = "1569"
validation = await validate_quiz_answer(
    question_url=quiz['questions'][0]['source_url'],
    user_answer=answer
)

result = json.loads(validation)
print(f"Answer: {answer}")
print(f"Correct: {result['is_correct']}")
print(f"Feedback: {result['feedback']}")
```

### Example 2: Build a Quiz Application

```python
class PolishHistoryQuiz:
    def __init__(self, topic: str, question_count: int = 5):
        self.topic = topic
        self.question_count = question_count
        self.questions = []
        self.current_question = 0
        self.score = 0

    async def initialize(self):
        """Generate quiz questions"""
        quiz_data = await generate_quiz_questions(
            topic=self.topic,
            count=self.question_count,
            difficulty="medium"
        )
        quiz = json.loads(quiz_data)
        self.questions = quiz['questions']

    async def answer_question(self, answer: str) -> dict:
        """Submit answer and validate"""
        if self.current_question >= len(self.questions):
            return {"error": "Quiz completed"}

        question = self.questions[self.current_question]
        validation = await validate_quiz_answer(
            question_url=question['source_url'],
            user_answer=answer
        )

        result = json.loads(validation)
        if result['is_correct']:
            self.score += 1

        self.current_question += 1
        return result

    def get_current_question(self) -> dict:
        """Get current question"""
        if self.current_question < len(self.questions):
            return self.questions[self.current_question]
        return None

    def is_complete(self) -> bool:
        """Check if quiz is complete"""
        return self.current_question >= len(self.questions)

    def get_score(self) -> dict:
        """Get final score"""
        return {
            "score": self.score,
            "total": len(self.questions),
            "percentage": (self.score / len(self.questions)) * 100
        }

# Usage
quiz = PolishHistoryQuiz("Powstanie listopadowe", question_count=5)
await quiz.initialize()

while not quiz.is_complete():
    question = quiz.get_current_question()
    print(f"Question: {question['question']}")

    user_answer = input("Your answer: ")
    result = await quiz.answer_question(user_answer)

    print(f"Result: {result['feedback']}")
    print()

final_score = quiz.get_score()
print(f"Final score: {final_score['score']}/{final_score['total']} ({final_score['percentage']:.1f}%)")
```

### Example 3: Custom Question Generation

```python
import json
from tools.quiz import extract_quiz_facts

# Extract content for custom processing
content = await extract_quiz_facts(
    topic="Bitwa pod Wiedniem 1683",
    count=20
)

data = json.loads(content)

# Now implement your own fact extraction and question generation
article_text = data['content']

# Custom logic to extract specific information
# For example, using NLP libraries, regex patterns, etc.
# Then generate questions based on extracted facts
```

## Current Limitations

### Structured Fact Extraction
Due to reliability concerns with regex-based extraction, the following features were disabled:
- **Date question generation** (`generate_date_question`, `_generate_date_question`)
- **Figure identification** (`generate_figure_question`, `_generate_figure_question`)
- **Event identification** (`generate_event_question`, `_generate_event_question`)

These tools returned error messages with suggestions for implementing custom extraction methods.

### Answer Validation
The `validate_quiz_answer` implementation used simple text matching:
```python
is_correct = user_answer_clean in content
```

This is a basic implementation that may produce false positives/negatives. A production system should use:
- Semantic similarity (embedding-based matching)
- Fuzzy matching for typos
- Context-aware validation
- NLP-based answer extraction

### Multiple Choice Generation
The `_generate_multiple_choice` function generated generic questions:
```python
question = f"Czym jest '{title}' w historii Polski?"
options = [
    "Postać historyczna",
    "Wydarzenie historyczne",
    "Miejsce historyczne",
    "Okres historyczny"
]
```

This is a simplified implementation. Advanced quiz generation would require:
- Content analysis to extract key facts
- Question generation based on extracted facts
- Distractor generation for plausible wrong answers

## Implementation Checklist

If you want to recreate the quiz tools, here's what you need to implement:

### 1. Core Files to Create
- [ ] `tools/quiz.py` - Main quiz tool implementations
- [ ] `models/quiz.py` - Data models (QuizQuestion, QuizAnswer, QuizSet, enums)

### 2. MCP Tools to Add to server.py
- [ ] `generate_quiz_question` - Generate single question
- [ ] `generate_quiz_questions` - Generate multiple questions
- [ ] `validate_quiz_answer` - Validate answers
- [ ] `extract_quiz_facts` - Extract facts for quizzes
- [ ] `generate_multiple_choice` - Multiple choice wrapper
- [ ] `generate_date_question` - Date question wrapper
- [ ] `generate_figure_question` - Figure question wrapper
- [ ] `generate_event_question` - Event question wrapper

### 3. Dependencies to Add
```python
# In server.py
from tools import quiz

# In tools/quiz.py
from models.quiz import QuizQuestion, QuestionType, DifficultyLevel
```

### 4. Configuration Settings (config.py)
```python
# Quiz settings
QUIZ_DEFAULT_DIFFICULTY = 'medium'
QUIZ_DEFAULT_COUNT = 5
```

### 5. Enhanced Features to Consider
- [ ] NLP-based fact extraction (spaCy, transformers)
- [ ] Semantic similarity for answer validation
- [ ] Template-based question generation
- [ ] Difficulty assessment algorithms
- [ ] Distractor generation for multiple choice
- [ ] Multi-language support beyond Polish

### 6. Testing
```python
# Test quiz generation
pytest tests/test_quiz.py -v

# Test specific quiz type
pytest tests/test_quiz.py::test_generate_multiple_choice -v

# Test with coverage
pytest --cov=tools.quiz tests/
```

## Best Practices

### 1. Topic Selection
- Use Polish historical terms with diacritics
- Include years for disambiguation (e.g., "Powstanie styczniowe 1863")
- Be specific: "Bitwa pod Grunwaldem" is better than "Wojny"
- Use full names: "Bolesław III Krzywousty" not "Bolesław Krzywousty"

### 2. Difficulty Levels
- **Easy**: Basic facts (Who, What, When)
- **Medium**: Connections and context (Why, How)
- **Hard**: Specific details and lesser-known events
- **Expert**: Obscure facts, dates, and nuanced interpretations

### 3. Error Handling
Always check for error responses:
```python
result = json.loads(await generate_quiz_question(topic="..."))
if 'error' in result:
    # Handle error
    print(f"Error: {result['error']}")
else:
    # Process question
    question = result
```

### 4. Answer Validation
Implement robust validation for production use:
```python
async def validate_answer_advanced(question_url: str, user_answer: str, article: dict) -> dict:
    """Advanced answer validation with semantic matching"""
    from sklearn.feature_extraction.text import TfidfVectorizer
    from sklearn.metrics.pairwise import cosine_similarity

    content = article.get('content', '')

    # Extract correct answer from article based on question context
    # This is where you'd implement NLP-based extraction

    # Use semantic similarity
    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform([content, user_answer])
    similarity = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])[0][0]

    is_correct = similarity > 0.7  # Threshold for similarity

    return {
        'is_correct': is_correct,
        'similarity_score': similarity,
        'feedback': 'Correct!' if is_correct else 'Incorrect. Please try again.'
    }
```

## Future Enhancements

### Planned Features
1. **Enhanced Fact Extraction**
   - Integration with NLP libraries (spaCy, transformers)
   - Named entity recognition for dates, figures, locations
   - Relation extraction for event connections

2. **Improved Question Generation**
   - Template-based generation for specific question types
   - Automatic difficulty assessment
   - Context-aware distractor generation

3. **Advanced Validation**
   - Semantic similarity using embeddings
   - Fuzzy matching with edit distance
   - Partial credit for partially correct answers

4. **Multi-Domain Support**
   - Quiz generation from IPN, Dzieje, Polona, PSB, PWN sources
   - Cross-source fact verification
   - Source-specific question types

5. **Performance Optimization**
   - Caching of extracted content
   - Batch question generation
   - Pre-computed fact databases

## Related Documentation

- [MCP Architecture](./mcp-architecture.md) - Overall system architecture
- [Search Tools Documentation](./search_tools.md) - How search tools work
- [Extract Tools Documentation](./extract_tools.md) - How extraction works
- [API Reference](./api-reference.md) - Complete API documentation

---

**Document Status:** Reference Only - Tools Not Currently Implemented
**Last Updated:** 2025-04-19
**Version:** 1.0.0 (Reference)
**Language:** Polish (PL) - All content and interfaces in Polish language

**Note:** This documentation is preserved for historical reference and future implementation guidance. The quiz tools described here are not part of the current MCP server deployment.