from aiogram import Bot, Dispatcher
from aiogram.filters import Command
from aiogram.types import Message
from aiogram.types import ContentType
from aiogram import F
import requests


# Вместо BOT TOKEN HERE нужно вставить токен вашего бота
BOT_TOKEN = 'BOT TOKEN HERE'
API_URL: str = 'https://api.telegram.org/bot'
API_CATS_URL = 'https://api.thecatapi.com/v1/images/search'
API_DOGS_URL = 'https://random.dog/woof.json'
API_FOXES_URL = 'https://randomfox.ca/floof/'
# Создание объектов бота и диспетчера
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()
api_urls = (API_CATS_URL, API_DOGS_URL, API_FOXES_URL)
offset: int = -2


# Функция для обработки команды /start
async def process_start_command(message: Message):
    await message.answer(
        'Привет!\n'
        'Меня зовут Эхо-бот!\n'
        'Напиши мне что-нибудь или используй команды!'
    )


# Функция для обработки команды /help
async def process_help_command(message: Message):
    await message.answer(
        'Напиши мне что-нибудь и в ответ '
        'я пришлю тебе твое сообщение'
    )


# Функция для обработки команды /cat
async def send_cat(message: Message):
    offset: int = -2
    updates = requests.get(
        f'{API_URL}{BOT_TOKEN}/getUpdates?offset={offset + 1}'
        ).json()
    for result in updates['result']:
        offset = result['update_id']
        chat_id = result['message']['from']['id']
        response = requests.get(API_CATS_URL)
        if response.status_code == 200:
            link = response.json()[0]['url']
            requests.get(
                f'{API_URL}{BOT_TOKEN}/sendPhoto?'
                f'chat_id={chat_id}&photo={link}')


# Функция для обработки команды /dog
async def send_dog(message: Message):
    offset: int = -2
    updates = requests.get(
        f'{API_URL}{BOT_TOKEN}/getUpdates?offset={offset + 1}'
        ).json()
    for result in updates['result']:
        offset = result['update_id']
        chat_id = result['message']['from']['id']
        response = requests.get(API_DOGS_URL)
        if response.status_code == 200:
            link = response.json()['url']
            requests.get(
                f'{API_URL}{BOT_TOKEN}/sendPhoto?'
                f'chat_id={chat_id}&photo={link}')


# Функция для обработки команды /fox
async def send_fox(message: Message):
    offset: int = -2
    updates = requests.get(
        f'{API_URL}{BOT_TOKEN}/getUpdates?offset={offset + 1}'
        ).json()
    for result in updates['result']:
        offset = result['update_id']
        chat_id = result['message']['from']['id']
        response = requests.get(API_FOXES_URL)
        if response.status_code == 200:
            link = response.json()['image']
            requests.get(f'{API_URL}{BOT_TOKEN}/sendPhoto?'
                         f'chat_id={chat_id}&photo={link}')


# Функция для эха фото
async def send_photo_echo(message: Message):
    if message.photo:
        await message.reply_photo(message.photo[0].file_id)
    else:
        await message.reply("Вы не отправили фото")


# Функция для эха видео
async def send_video_echo(message: Message):
    if message.video is not None:
        await message.reply_video(message.video.file_id)
    else:
        await message.reply("Вы не отправили видео")


# Функция для эха кружков
async def send_video_note_echo(message: Message):
    if message.video_note is not None:
        await message.reply_video_note(message.video_note.file_id)
    else:
        await message.reply("Вы не отправили кружок наверное")


# Функция для эха аудио
async def send_audio_echo(message: Message):
    if message.audio is not None:
        await message.reply_audio(message.audio.file_id)
    else:
        await message.reply("Вы не отправили аудио")


# Функция для эха стикеров
async def send_sticker_echo(message: Message):
    if message.sticker is not None:
        await message.reply_sticker(message.sticker.file_id)
    else:
        await message.reply("Вы не отправили стикер")


# Функция для эха голосового сообщения
async def send_voice_echo(message: Message):
    if message.voice is not None:
        await message.reply_voice(message.voice.file_id)
    else:
        await message.reply("Вы не отправили голосовое сообщение")


# Функция для эха файла
async def send_file_echo(message: Message):
    if message.document is not None:
        await message.reply_document(message.document.file_id)
    else:
        await message.reply("Вы не отправили файл")


# Функция для обработки ошибок
async def send_echo(message: Message):
    try:
        await message.send_copy(chat_id=message.chat.id)
    except TypeError:
        await message.reply(
            text='Данный тип апдейтов не поддерживается '
                 'методом send_copy'
        )


# Регистрируем хэндлеры
dp.message.register(process_start_command, Command(commands='start'))
dp.message.register(process_help_command, Command(commands='help'))
dp.message.register(send_cat, Command(commands='cat'))
dp.message.register(send_dog, Command(commands='dog'))
dp.message.register(send_fox, Command(commands='fox'))
dp.message.register(send_photo_echo, F.content_type == ContentType.PHOTO)
dp.message.register(send_video_echo, F.video)
dp.message.register(send_video_note_echo, F.video_note)
dp.message.register(send_sticker_echo, F.sticker)
dp.message.register(send_audio_echo, F.audio)
dp.message.register(send_voice_echo, F.voice)
dp.message.register(send_file_echo, F.document)
dp.message.register(send_echo)

if __name__ == '__main__':
    dp.run_polling(bot)
