"""Клавиатуры для бота."""
from app.whapi.buttons import Markup, Button

# Идентификаторы кнопок
NEW_AUDIO_ID = 'new_audio'
SUPPORT_ID = 'support'
CANCEL_ID = 'cancel'

# Клавиатура для приветственного сообщения
start_keyboard = Markup(
    buttons=[
        Button(title='🎧 New audio', id=NEW_AUDIO_ID),
        Button(title='📞 Support', id=SUPPORT_ID)
    ]
)

# Клавиатура для нового аудио (только новый аудио)
new_audio_keyboard = Markup(
    buttons=[
        Button(title='🎧 New audio', id=NEW_AUDIO_ID)
    ]
)

# Клавиатура для отмены
cancel_keyboard = Markup(
    buttons=[
        Button(title='❌ Cancel', id=CANCEL_ID)
    ]
)
