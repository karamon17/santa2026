from aiogram import F, Router
from aiogram.filters import CommandStart
from aiogram.types import CallbackQuery, Message

from .config import get_settings
from .content import INTRO_MESSAGE, QUESTIONS, RULES_MESSAGE
from .keyboards import build_start_keyboard
from .quiz import milestone_message, progress_bar, send_question
from .state import get_state

router = Router()


@router.message(CommandStart())
async def handle_start(message: Message) -> None:
    state = get_state(message.from_user.id)
    state.score = 0
    state.current_index = 0
    state.incorrect_queue.clear()
    state.active_question = None
    state.sent_safety = False
    state.sent_parking = False
    state.sent_inspiration = False
    state.finished = False

    await message.answer(INTRO_MESSAGE, reply_markup=build_start_keyboard("quiz_rules"))


@router.callback_query(F.data == "quiz_rules")
async def handle_rules(callback: CallbackQuery) -> None:
    await callback.message.answer(RULES_MESSAGE, reply_markup=build_start_keyboard("start_quiz"))
    await callback.answer()


@router.callback_query(F.data == "start_quiz")
async def handle_start_quiz(callback: CallbackQuery) -> None:
    state = get_state(callback.from_user.id)
    state.score = 0
    state.current_index = 0
    state.incorrect_queue.clear()
    state.active_question = None
    state.sent_safety = False
    state.sent_parking = False
    state.sent_inspiration = False
    state.finished = False

    await callback.message.answer("Поехали! Первый вопрос:")
    await send_question(callback.bot, callback.message.chat.id, state)
    await callback.answer()


@router.callback_query(F.data.startswith("answer:"))
async def handle_answer(callback: CallbackQuery) -> None:
    user_id = callback.from_user.id
    state = get_state(user_id)
    settings = get_settings()

    if state.finished:
        await callback.answer("Ты уже набрала 15 баллов!", show_alert=True)
        return

    try:
        _, q_index_str, chosen = callback.data.split(":")
        q_index = int(q_index_str)
    except ValueError:
        await callback.answer()
        return

    if state.active_question != q_index:
        await callback.answer("Подожди следующий вопрос", show_alert=True)
        return

    question = QUESTIONS[q_index]
    if chosen == question.correct:
        state.score += 1
        progress = progress_bar(state.score, settings.target_score)
        await callback.message.answer(
            f"Верно! Твой счёт: {state.score}\nПрогресс: {progress}"
        )
    else:
        state.incorrect_queue.append(q_index)
        correct_text = question.options[question.correct]
        await callback.message.answer(
            f"Неверно. Верный ответ: {question.correct}) {correct_text}. "
            f"Твой счёт: {state.score}\nНе сдавайся, попробуем ещё раз!"
        )

    milestone_text = milestone_message(state.score, state)
    if milestone_text:
        await callback.message.answer(milestone_text)

    if state.score >= settings.target_score:
        state.finished = True
        await callback.message.answer(
            "Поздравляю! Ты набрала 15 баллов! Вот вдохновляющие фразы, "
            "которые помогут тебе чувствовать себя уверенно за рулём. "
            "Теперь можно открывать подарок от тайного Санты!"
        )
        await callback.answer()
        return

    await send_question(callback.bot, callback.message.chat.id, state)
    await callback.answer()
