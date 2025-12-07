from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


def build_answer_keyboard(q_index: int) -> InlineKeyboardMarkup:
    buttons = [
        [InlineKeyboardButton(text=f"{letter}", callback_data=f"answer:{q_index}:{letter}")]
        for letter in ["A", "B", "C", "D"]
    ]
    return InlineKeyboardMarkup(inline_keyboard=buttons)


def build_start_keyboard(callback: str) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[[InlineKeyboardButton(text="🚀 Поехали", callback_data=callback)]]
    )


def build_finish_keyboard(remaining: int) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text=f"Ты можешь ответить на оставшиеся {remaining} вопросов",
                    callback_data="continue_remaining",
                )
            ],
            [InlineKeyboardButton(text="Начать сначала", callback_data="start_quiz")],
        ]
    )
