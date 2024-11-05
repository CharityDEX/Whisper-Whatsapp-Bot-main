"""Константы текстов. Поддерживается Markdown."""

# Текст для приветственного сообщения
START_MESSAGE = """*✨Welcome to Whisper AI bot!*

Transcribe audio and video seamlessly with this bot.

1️⃣ *Click “New audio”*

2️⃣ *Upload ANY audio or video to the bot*

🤖 “In process. Your file is being processed. Please wait a moment.”

3️⃣ *Whisper will make a perfect transcription and the bullet point summary.*

4️⃣ *After you receive a transcription, you can ask any questions regarding uploaded file in the chat.*

⚠️ Note, that the bot does not accept audio/video file over 1 hour.

⁉️ If you have any questions, contact support by clicking “Support”

*Click “New audio”*👇"""

# Текст для сообщения с контактами поддержки
SUPPORT_MESSAGE = """💥If you are facing difficulties or you have a question, contact support here: +1 (669) 210-4822 💥"""


# Текст для сообщения с статистикой
STATS_MESSAGE = """📈 *Statistics:*

👥 *New users (today):* {new_users}
👥 *Registered users:* {registered_users}
📄 *Uploaded audios:* {uploaded_audios}
💬 *GPT requests:* {gpt_requests}"""

# Текст для сообщения с просьбой загрузить файл для получения транскрипции
WITHOUT_TRANSCRIPTION_MESSAGE = """ℹ️ Before asking questions, please transcribe the audio."""

# Текст для сообщения с ошибкой, если пользователь не найден
USER_NOT_FOUND_MESSAGE = """User {number} not found"""

# Текст для сообщения что пользователь установлен в качестве администратора
SET_ADMIN_MESSAGE = """User {number} set as admin"""

# Текст для сообщения что пользователь удален из списка администраторов
UNSET_ADMIN_MESSAGE = """User {number} removed as admin"""

# Текст для сообщения что пользователь не может быть изменен
NOT_CHANGE_ADMIN_MESSAGE = """That {number} can't be changed"""

# Текст для сообщения о том, как установить пользователя в качестве администратора
ADMIN_COMMAND_HELP_MESSAGE = """*Admin command help:*

admin set <number> - *set user as admin*
admin unset <number> - *unset user as admin*

*number format:* 1234567890"""

# Текст для сообщения с информацией о том, что файл обрабатывается
IN_PROCESS_MESSAGE = """*In process...*

Your file is being processed. Please wait a moment. 🕒"""

# Текст для сообщения с информацией о том, что пользователь уже обрабатывает аудио
ALREADY_IN_PROCESS_MESSAGE = """⚠️ You are already processing audio. Please wait until the previous audio is processed."""

# Текст для сообщения с информацией о том, что произошла ошибка при обработке аудио
ERROR_IN_PROCESS_MESSAGE = """⚠️ An error occurred while processing your audio. Please try again later."""

# Текст для сообщения с транскрипцией
TRANSCRIPTION_MESSAGE = """*Transcription:*"""

# Текст для сообщения с суммаризацией
SUMMARY_MESSAGE = """*Summary:*
{summary}

*Now you can ask questions about transcribing.*
"""

# Текст для сообщения с информацией о том, что вопрос обрабатывается
RESPONSE_GENERATION_MESSAGE = """*Response generation...*

Your question is being processed. Please wait a moment. 🕒"""

# Текст для сообщения с информацией о том, что произошла ошибка при генерации ответа
ERROR_RESPONSE_GENERATION_MESSAGE = """⚠️ An error occurred while generating a response. Please try again later."""

# Текст для сообщения с информацией о том, что действие отменено
CANCEL_MESSAGE = """*Action canceled*"""

# Текст для сообщения с просьбой отправить файл
NEW_AUDIO_MESSAGE = """⚡️Please send a file (audio, video, or voice message)⚡️"""
