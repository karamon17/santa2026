import os
from dataclasses import dataclass, field
from typing import Dict, List, Optional

from aiogram import Bot, Dispatcher, F
from aiogram.filters import CommandStart
from aiogram.types import CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup, Message, Update
from fastapi import FastAPI, Request

TOKEN = os.getenv("TELEGRAM_TOKEN")
WEBHOOK_URL = os.getenv("WEBHOOK_URL")
TARGET_SCORE = 15

if not TOKEN:
    raise RuntimeError("TELEGRAM_TOKEN environment variable is not set")

app = FastAPI(title="Secret Santa Volvo Quiz")
bot = Bot(TOKEN)
dp = Dispatcher()


@dataclass
class QuizQuestion:
    prompt: str
    options: Dict[str, str]
    correct: str


QUESTIONS: List[QuizQuestion] = [
    QuizQuestion(
        prompt="Какой объём двигателя у твоего Volvo XC40?",
        options={"A": "1 л", "B": "2 л", "C": "3 л", "D": "4 л"},
        correct="B",
    ),
    QuizQuestion(
        prompt="Сколько лошадиных сил у двигателя в твоем XC40?",
        options={"A": "90", "B": "190", "C": "290", "D": "390"},
        correct="B",
    ),
    QuizQuestion(
        prompt="Какой тип привода у твоего автомобиля?",
        options={"A": "Передний", "B": "Задний", "C": "Полный", "D": "Не знаю"},
        correct="C",
    ),
    QuizQuestion(
        prompt="Разгон 0–100 км/ч у твоей машинки составляет:",
        options={"A": "4,0 с", "B": "8,5 с", "C": "14 с", "D": "20.5 с"},
        correct="B",
    ),
    QuizQuestion(
        prompt="Какой средний расход топлива?",
        options={"A": "4,2 л/100 км", "B": "6,9 л/100 км", "C": "14,8 л/100 км", "D": "24,8 л/100 км"},
        correct="B",
    ),
    QuizQuestion(
        prompt="Какой тип двигателя?",
        options={"A": "Дизель", "B": "Гибрид", "C": "Бензиновый", "D": "Электрический"},
        correct="C",
    ),
    QuizQuestion(
        prompt="Какой тип коробки передач используется?",
        options={"A": "Робот", "B": "Механика", "C": "Вариатор", "D": "Автомат"},
        correct="D",
    ),
    QuizQuestion(
        prompt="Какой клиренс (дорожный просвет) у XC40?",
        options={"A": "140 мм", "B": "201 мм", "C": "240 мм", "D": "320 мм"},
        correct="B",
    ),
    QuizQuestion(
        prompt="Какой минимальный бензин надо заливать:",
        options={"A": "86", "B": "92", "C": "95", "D": "Дизель"},
        correct="C",
    ),
    QuizQuestion(
        prompt="Какая страна является «родиной» бренда Volvo?",
        options={"A": "Швеция", "B": "Дания", "C": "Норвегия", "D": "Швейцария"},
        correct="A",
    ),
    QuizQuestion(
        prompt="Кузов?",
        options={"A": "Седан", "B": "Купе", "C": "Внедорожник", "D": "Пикап"},
        correct="C",
    ),
    QuizQuestion(
        prompt="Вольво считается каким классом?",
        options={"A": "Эконом", "B": "Комфорт", "C": "Комфорт+", "D": "Премиум"},
        correct="D",
    ),
    QuizQuestion(
        prompt="Какое важнейшее изобретение было создано инженером Volvo в 1959 году?",
        options={"A": "ABS", "B": "Трёхточечный ремень безопасности", "C": "Подушка безопасности", "D": "Зона программируемой деформации"},
        correct="B",
    ),
    QuizQuestion(
        prompt="Автомобиль какого бренда первым в мире получил максимальный рейтинг безопасности по EuroNCAP?",
        options={"A": "Mercedes-Benz", "B": "Volvo", "C": "Toyota", "D": "BMW"},
        correct="B",
    ),
    QuizQuestion(
        prompt="Что означает, когда водитель моргает дальним на перекрёстке?",
        options={"A": "Хочет проехать первым", "B": "Даёт вам дорогу", "C": "Предупреждает о пробке", "D": "Показывает, что он зол"},
        correct="B",
    ),
    QuizQuestion(
        prompt="Если сзади едет машина и несколько раз моргает дальним светом — это чаще всего:",
        options={"A": "Водитель скучает", "B": "Просьба уступить полосу", "C": "Просьба о помощи", "D": "Обратный отсчёт"},
        correct="B",
    ),
    QuizQuestion(
        prompt="Как Volvo относится к максимальной скорости автомобилей?",
        options={"A": "Ограничивает её на уровне 180 км/ч для безопасности", "B": "Никак не ограничивает", "C": "Даёт регулировку в настройках", "D": "Ограничивает её на уровне 250 км/ч"},
        correct="A",
    ),
    QuizQuestion(
        prompt="Что делает система Pilot Assist?",
        options={"A": "Полностью автономно ведёт машину", "B": "Удерживает скорость и дистанцию + помогает удерживать полосу", "C": "Управляет движением по пересечённой местности", "D": "Помогает парковаться"},
        correct="B",
    ),
    QuizQuestion(
        prompt="Что делает система Auto Hold?",
        options={"A": "Удерживает машину на месте при остановке", "B": "Повышает мощность двигателя", "C": "Включает автодоводчики дверей", "D": "Удерживает скорость на трассе"},
        correct="A",
    ),
    QuizQuestion(
        prompt="Какой факт о Volvo НЕ является правдой?",
        options={"A": "Компания делает собственные манекены для краш-тестов детей", "B": "Volvo первой сделала встроенные детские сиденья", "C": "Volvo изобрела подогрев сидений", "D": "Volvo первой в мире поставила кондиционер"},
        correct="D",
    ),
    QuizQuestion(
        prompt="Что считается самым частым отвлекающим фактором для водителей?",
        options={"A": "Радио", "B": "Телефон", "C": "Открытое окно", "D": "Солнцезащитные очки"},
        correct="B",
    ),
    QuizQuestion(
        prompt="Какой тип усилителя руля установлен?",
        options={"A": "Гидравлический", "B": "Никакой", "C": "Электрический", "D": "Вакуумный"},
        correct="C",
    ),
    QuizQuestion(
        prompt="Где находится рычаг открывания капота?",
        options={"A": "Под рулевой колонкой", "B": "Под передним пассажиром", "C": "Там где ручник", "D": "На мультимедия экране"},
        correct="A",
    ),
    QuizQuestion(
        prompt="Какова длина XC40?",
        options={"A": "4 м", "B": "4.4 м", "C": "5 м", "D": "6 м"},
        correct="B",
    ),
    QuizQuestion(
        prompt="Что означает, когда водитель после обгона кратко мигает аварийкой?",
        options={"A": "Просит проехать первым", "B": "Благодарит за то, что его пропустили", "C": "Просит уступить дорогу", "D": "Сообщает об аварии"},
        correct="B",
    ),
    QuizQuestion(
        prompt="Что обычно означает короткое мигание дальним светом встречной машины?",
        options={"A": "Ты ему понравилась - хочет номерок", "B": "Сообщает о том, что у тебя с машиной что-то не так", "C": "Впереди стоит ДПС/камера", "D": "Он хочет тебя ослепить"},
        correct="C",
    ),
]

SAFETY_TIPS = "\n".join(
    [
        "Советы по безопасности",
        "«Всегда держи дистанцию — она спасает больше, чем тормоза.»",
        "",
        "«Не спеши — безопасность всегда важнее скорости.»",
        "",
        "«Чистые зеркала = залог безопасных маневров»",
        "",
        "«Если сомневаешься — не делай манёвр.»",
        "",
        "«Смотри на три шага вперёд, а не только перед капотом.»",
        "",
        "«Помни от дедовском важном правиле трех Д - дай дорогу дураку.»",
        "",
        "«Плавный разгон, плавный тормоз — и машина, и дети скажут спасибо.»",
        "",
        "«Уставший водитель — как телефон на 5%: вроде работает, но риски большие.»",
        "",
        "«Всегда думай за двоих — за себя и за того, кто рядом.»",
        "",
        "«Не забывай: лучший водитель — спокойный водитель.»",
    ]
)

PARKING_TIPS = "\n".join(
    [
        "🅿️ Лайфхаки по парковке",
        "«Паркуйся так, чтобы выезжать было проще, чем заезжать.»",
        "",
        "«Если сомневаешься — используй камеры и зеркала одновременно.»",
        "",
        "«Медленно — значит правильно. Быстро — значит дорого.»",
        "",
        "«Не бойся перепарковаться — это сила, а не слабость.»",
        "",
        "«Чем ближе к бордюру — тем меньше шанс, что кто-то обдерёт.»",
        "",
        "«Всегда сначала смотри заднюю камеру, потом в зеркала.»",
        "",
        "«Парковка задом почти всегда проще, чем носом.»",
        "",
        "«Ставь машину чуть правее — дверям будет легче открываться.»",
        "",
        "«Если рядом дорогая машина — оставь себе больше пространства.»",
        "",
        "«Главное правило парковки: не спешить. Вообще.»",
    ]
)

INSPIRATION = "\n".join(
    [
        "🌟 Вдохновляющие фразы для уверенности на дороге",
        "«Ты управляешь машиной уверенно — и с каждым километром всё лучше.»",
        "",
        "«Никто не рождается водителем. Все становятся. И ты — уже стала.»",
        "",
        "«Спокойствие — твоя суперспособность за рулём.»",
        "",
        "«Твоя машина доверяет тебе. Доверяй и ты себе.»",
        "",
        "«Ты управляешь XC40, а не страх управляет тобой.»",
        "",
        "«Главная сила — в плавности и уверенности. У тебя это есть.»",
        "",
        "«Каждая поездка делает тебя ещё более опытной.»",
        "",
        "«Ты — отличный водитель. Машина это чувствует.»",
        "",
        "«Дорога любит тех, кто не спешит и не нервничает.»",
        "",
        "«Ты — за рулём. А значит, всё под контролем.»",
    ]
)


@dataclass
class UserState:
    score: int = 0
    current_index: int = 0
    incorrect_queue: List[int] = field(default_factory=list)
    active_question: Optional[int] = None
    sent_safety: bool = False
    sent_parking: bool = False
    sent_inspiration: bool = False
    finished: bool = False


user_states: Dict[int, UserState] = {}


@app.on_event("startup")
async def on_startup() -> None:
    if WEBHOOK_URL:
        await bot.set_webhook(WEBHOOK_URL)


@app.post("/webhook")
async def telegram_webhook(request: Request) -> dict:
    if not TOKEN:
        return {"status": "missing token"}
    data = await request.json()
    update = Update.model_validate(data)
    await dp.feed_update(bot, update)
    return {"status": "ok"}


@app.get("/")
async def root() -> dict:
    return {"status": "running"}


def get_state(user_id: int) -> UserState:
    if user_id not in user_states:
        user_states[user_id] = UserState()
    return user_states[user_id]


def format_question(question: QuizQuestion) -> str:
    options = "\n".join([f"{key}) {value}" for key, value in question.options.items()])
    return f"{question.prompt}\n\n{options}"


def build_answer_keyboard(q_index: int) -> InlineKeyboardMarkup:
    buttons = [
        [InlineKeyboardButton(text=f"{letter}", callback_data=f"answer:{q_index}:{letter}")]
        for letter in ["A", "B", "C", "D"]
    ]
    return InlineKeyboardMarkup(inline_keyboard=buttons)


def build_start_keyboard(callback: str) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[[InlineKeyboardButton(text="Поехали", callback_data=callback)]]
    )


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


def next_question_index(state: UserState) -> Optional[int]:
    if state.score >= TARGET_SCORE:
        return None
    if state.current_index < len(QUESTIONS):
        idx = state.current_index
        state.current_index += 1
        return idx
    if state.incorrect_queue:
        return state.incorrect_queue.pop(0)
    return None


async def send_question(chat_id: int, state: UserState) -> None:
    q_index = next_question_index(state)
    if q_index is None:
        return
    state.active_question = q_index
    question = QUESTIONS[q_index]
    await bot.send_message(
        chat_id=chat_id,
        text=format_question(question),
        reply_markup=build_answer_keyboard(q_index),
    )


@dp.message(CommandStart())
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

    intro = (
        "Привет! Я твой тайный санта и я знаю, что у тебя недавно появилась машинка. "
        "Я подготовил для тебя интересные вопросы. 1 правильный ответ дает тебе 1 балл. "
        "После 5 набранных баллов ты получишь топ советов по безопасности для водителя. "
        "После 10 набранных баллов ты получишь топ лайфхаков по парковке. "
        "После 15 набранных баллов ты получишь топ вдохновляющих фраз для уверенности на дороге и главный приз."
    )

    await message.answer(intro, reply_markup=build_start_keyboard("quiz_rules"))


@dp.callback_query(F.data == "quiz_rules")
async def handle_rules(callback: CallbackQuery) -> None:
    await callback.message.answer(
        "Автомобильный квест: “Мой новый друг”.\n"
        "Внимание! Не бойся ошибиться, при ошибке бот покажет верный ответ, "
        "а ты постарайся его запомнить, ведь возможно получишь этот вопрос повторно, "
        "чтобы добрать необходимые 15 баллов.",
        reply_markup=build_start_keyboard("start_quiz"),
    )
    await callback.answer()


@dp.callback_query(F.data == "start_quiz")
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

    await callback.message.answer("Поехали! Первый вопрос: ")
    await send_question(callback.message.chat.id, state)
    await callback.answer()


@dp.callback_query(F.data.startswith("answer:"))
async def handle_answer(callback: CallbackQuery) -> None:
    user_id = callback.from_user.id
    state = get_state(user_id)

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
        await callback.answer("Подождите следующий вопрос", show_alert=True)
        return

    question = QUESTIONS[q_index]
    if chosen == question.correct:
        state.score += 1
        await callback.message.answer(
            f"Верно! Твой счёт: {state.score}"
        )
    else:
        state.incorrect_queue.append(q_index)
        correct_text = question.options[question.correct]
        await callback.message.answer(
            f"Неверно. Верный ответ: {question.correct}) {correct_text}. "
            f"Твой счёт: {state.score}"
        )

    milestone_text = milestone_message(state.score, state)
    if milestone_text:
        await callback.message.answer(milestone_text)

    if state.score >= TARGET_SCORE:
        state.finished = True
        await callback.message.answer(
            "Ты набрала 15 баллов! Вот главный приз — вдохновляющие фразы, "
            "которые помогут тебе чувствовать себя уверенно за рулём."
        )
        await callback.answer()
        return

    await send_question(callback.message.chat.id, state)
    await callback.answer()


# Run polling when launched directly for local development
if __name__ == "__main__":
    import asyncio

    async def main() -> None:
        if not TOKEN:
            raise RuntimeError("TELEGRAM_TOKEN is not set")
        await dp.start_polling(bot)

    asyncio.run(main())
