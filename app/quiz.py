from typing import Optional

from aiogram import Bot

from .config import get_settings
from .content import INSPIRATION, PARKING_TIPS, QUESTIONS, SAFETY_TIPS
from .keyboards import build_answer_keyboard, build_restart_keyboard
from .models import QuizQuestion, UserState


def format_question(question: QuizQuestion) -> str:
    options = "\n".join([f"{key}) {value}" for key, value in question.options.items()])
    return f"{question.prompt}\n\n{options}"


def milestone_message(score: int, state: UserState) -> Optional[str]:
    if score >= 15 and not state.sent_inspiration:
        state.sent_inspiration = True
        return INSPIRATION
    if score >= 10 and not state.sent_parking:
        state.sent_parking = True
        return PARKING_TIPS
    if score >= 5 and not state.sent_safety:
        state.sent_safety = True
        return SAFETY_TIPS
    return None


def remaining_questions_count(state: UserState) -> int:
    remaining_indices = set(range(state.current_index, len(QUESTIONS)))
    remaining_indices.update(state.incorrect_queue)
    return len(remaining_indices)


def next_question_index(state: UserState) -> Optional[int]:
    target_score = get_settings().target_score
    if state.score >= target_score and not state.postgame:
        return None
    if state.current_index < len(QUESTIONS):
        idx = state.current_index
        state.current_index += 1
        return idx
    if state.incorrect_queue:
        return state.incorrect_queue.pop(0)
    return None


def progress_bar(score: int, target_score: int) -> str:
    steps = min(score, target_score)
    filled = "█" * steps
    empty = "░" * max(target_score - steps, 0)
    return f"{filled}{empty} ({score}/{target_score})"


async def send_question(bot: Bot, chat_id: int, state: UserState) -> None:
    q_index = next_question_index(state)
    if q_index is None:
        state.active_question = None
        if state.postgame:
            await bot.send_message(
                chat_id=chat_id,
                text="Все вопросы кончились. Спасибо за игру!",
                reply_markup=build_restart_keyboard(),
            )
        return
    state.active_question = q_index
    question = QUESTIONS[q_index]
    await bot.send_message(
        chat_id=chat_id,
        text=format_question(question),
        reply_markup=build_answer_keyboard(q_index),
    )
