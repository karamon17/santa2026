from typing import Dict

from .models import UserState

user_states: Dict[int, UserState] = {}


def get_state(user_id: int) -> UserState:
    if user_id not in user_states:
        user_states[user_id] = UserState()
    return user_states[user_id]
