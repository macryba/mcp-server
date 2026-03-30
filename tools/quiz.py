#!/usr/bin/env python3
"""
Quiz generation tools for Polish history
Provides tools to generate quiz questions, validate answers, and extract quiz facts
"""

from tools.search import search_wikipedia_polish, search_historical_figures, search_historical_events
from tools.extract import extract_facts, extract_article
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
        search_results = await search_wikipedia_polish(topic, max_results=3)
        results = eval(search_results)

        if not results or 'error' in results[0]:
            return str({'error': f'Could not find information about {topic}'})

        # Get the first result
        first_result = results[0]
        url = first_result.get('url')

        # Extract facts from the article
        facts_data = await extract_facts(url)
        facts = eval(facts_data)

        if 'error' in facts:
            return str({'error': 'Could not extract facts for quiz generation'})

        # Generate question based on type
        if question_type == 'multiple_choice':
            question = await _generate_multiple_choice(facts, topic, difficulty)
        elif question_type == 'date':
            question = await _generate_date_question(facts, topic, difficulty)
        elif question_type == 'figure_identification':
            question = await _generate_figure_question(facts, topic, difficulty)
        elif question_type == 'event_identification':
            question = await _generate_event_question(facts, topic, difficulty)
        else:
            question = await _generate_multiple_choice(facts, topic, difficulty)

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
        search_results = await search_wikipedia_polish(topic, max_results=1)
        results = eval(search_results)

        if not results or 'error' in results[0]:
            return str({'error': f'Could not find information about {topic}'})

        url = results[0].get('url')

        # Extract facts
        facts_data = await extract_facts(url)
        facts = eval(facts_data)

        if 'error' in facts:
            return str({'error': 'Could not extract facts'})

        # Filter and format facts for quiz generation
        quiz_facts = []

        # Add dates
        if facts.get('dates'):
            for date in facts['dates'][:3]:
                quiz_facts.append({
                    'type': 'date',
                    'fact': f'Ważna data: {date}',
                    'data': date
                })

        # Add figures
        if facts.get('figures'):
            for figure in facts['figures'][:3]:
                quiz_facts.append({
                    'type': 'figure',
                    'fact': f'Postać historyczna: {figure}',
                    'data': figure
                })

        # Add events
        if facts.get('events'):
            for event in facts['events'][:3]:
                quiz_facts.append({
                    'type': 'event',
                    'fact': f'Wydarzenie: {event}',
                    'data': event
                })

        result = {
            'topic': topic,
            'facts': quiz_facts[:count],
            'source_url': url
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

async def _generate_multiple_choice(facts: Dict, topic: str, difficulty: str) -> Dict:
    """Generate a multiple choice question"""
    # Get the title from facts
    title = facts.get('title', topic)
    url = facts.get('url', '')

    # Generate question based on available facts
    if facts.get('dates'):
        # Date-based question
        correct_date = facts['dates'][0]
        question = f"Kiedy wydarzyło się {title}?"

        # Generate wrong answers
        wrong_answers = _generate_wrong_dates(correct_date)
        options = [correct_date] + wrong_answers
        random.shuffle(options)

        correct_index = options.index(correct_date)

    else:
        # General knowledge question
        question = f"Co jest znane jako '{title}'?"
        options = [
            "Postać historyczna",
            "Wydarzenie historyczne",
            "Miejsce historyczne",
            "Okres historyczny"
        ]
        correct_index = 0

    return {
        'question': question,
        'options': options,
        'correct_answer': options[correct_index],
        'correct_index': correct_index,
        'difficulty': difficulty,
        'topic': topic,
        'source_url': url,
        'question_type': 'multiple_choice'
    }


async def _generate_date_question(facts: Dict, topic: str, difficulty: str) -> Dict:
    """Generate a date question"""
    title = facts.get('title', topic)
    url = facts.get('url', '')

    if not facts.get('dates'):
        return {
            'error': 'No dates found for this topic'
        }

    correct_date = facts['dates'][0]
    question = f"Podaj datę wydarzenia: {title}"

    wrong_answers = _generate_wrong_dates(correct_date)
    options = [correct_date] + wrong_answers
    random.shuffle(options)
    correct_index = options.index(correct_date)

    return {
        'question': question,
        'options': options,
        'correct_answer': options[correct_index],
        'correct_index': correct_index,
        'difficulty': difficulty,
        'topic': topic,
        'source_url': url,
        'question_type': 'date'
    }


async def _generate_figure_question(facts: Dict, topic: str, difficulty: str) -> Dict:
    """Generate a figure identification question"""
    title = facts.get('title', topic)
    url = facts.get('url', '')

    if not facts.get('figures'):
        return {
            'error': 'No historical figures found for this topic'
        }

    figure = facts['figures'][0]
    question = f"Kto to jest: {figure}?"

    # Generate options
    options = [figure]
    # Would need to generate similar-sounding wrong answers
    for i in range(3):
        options.append(f"Inna postać {i+1}")

    random.shuffle(options)
    correct_index = options.index(figure)

    return {
        'question': question,
        'options': options,
        'correct_answer': options[correct_index],
        'correct_index': correct_index,
        'difficulty': difficulty,
        'topic': topic,
        'source_url': url,
        'question_type': 'figure_identification'
    }


async def _generate_event_question(facts: Dict, topic: str, difficulty: str) -> Dict:
    """Generate an event identification question"""
    title = facts.get('title', topic)
    url = facts.get('url', '')

    if not facts.get('events'):
        return {
            'error': 'No events found for this topic'
        }

    event = facts['events'][0]
    question = f"Jakie wydarzenie opisano: {event[:100]}...?"

    options = [
        event[:50] + "...",
        "Bitwa",
        "Powstanie",
        "Traktat"
    ]

    random.shuffle(options)
    correct_index = 0

    return {
        'question': question,
        'options': options,
        'correct_answer': options[correct_index],
        'correct_index': correct_index,
        'difficulty': difficulty,
        'topic': topic,
        'source_url': url,
        'question_type': 'event_identification'
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
