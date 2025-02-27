from aiogram import types
from asyncio import create_task, sleep

from aiogram import Router, F, Bot
from aiogram.filters import Command
from aiogram.types import ContentType
from aiogram.types import Message
from aiogram_media_group import media_group_handler, MediaGroupFilter
from fluent.runtime import FluentLocalization

from bot.blocklists import banned, shadowbanned
from bot.config_reader import config
from bot.filters import SupportedMediaFilter

router = Router()


async def _send_expiring_notification(message: Message, l10n: FluentLocalization):
    """
    Отправляет "самоуничтожающееся" через 5 секунд сообщение

    :param message: сообщение, на которое бот отвечает подтверждением отправки
    :param l10n: объект локализации
    """
    msg = await message.reply(l10n.format_value("sent-confirmation"))
    if config.remove_sent_confirmation:
        await sleep(5.0)
        await msg.delete()


@router.message(Command(commands=["start"]))
async def cmd_start(message: Message, l10n: FluentLocalization):
    """
    Приветственное сообщение от бота пользователю

    :param message: сообщение от пользователя с командой /start
    :param l10n: объект локализации
    """
    await message.answer(l10n.format_value("intro"))


@router.message(Command(commands=["help"]))
async def cmd_help(message: Message, l10n: FluentLocalization):
    """
    Справка для пользователя

    :param message: сообщение от пользователя с командой /help
    :param l10n: объект локализации
    """
    await message.answer(l10n.format_value("help"))


@router.message(F.text)
async def text_message(message: Message, bot: Bot, l10n: FluentLocalization):
    """
    Хэндлер на текстовые сообщения от пользователя

    :param message: сообщение от пользователя для админа(-ов)
    :param l10n: объект локализации
    """

    if len(message.text) > 4000:
        return await message.reply(l10n.format_value("too-long-text-error"))

    if message.from_user.id in banned:
        await message.answer(l10n.format_value("you-were-banned-error"))

    elif message.from_user.id in shadowbanned:
        return

    else:
        await bot.send_message(
            config.admin_chat_id,
            message.html_text + f"\n\n#id{message.from_user.id}", parse_mode="HTML"
        )
        create_task(_send_expiring_notification(message, l10n))


@router.message(MediaGroupFilter())
@media_group_handler
async def supported_media(message: list[types.Message], bot: Bot, l10n: FluentLocalization):
    """Обрабатывает группу медиафайлов."""
    first_message = message[0]  # Берем первое сообщение из группы

    if first_message.from_user.id in banned:
        try:
            await first_message.answer(l10n.format_value("you-were-banned-error"))

        except Exception as e:
            print(f"Error sending 'you-were-banned-error': {e}")
        return

    elif first_message.from_user.id in shadowbanned:
        return

    # Собираем подписи и файлы из всех сообщений в группе.  Если сообщение не имеет медиа, пропускаем его
    media = []

    for msg in message:
        if msg.photo:
            file_id = msg.photo[-1].file_id # Берем последнее фото с максимальным разрешением
            file_type = "photo"

        elif msg.video:
            file_id = msg.video.file_id
            file_type = "video"

        elif msg.document:
            file_id = msg.document.file_id
            file_type = "document"

        else:
            continue # Пропускаем сообщения без медиа

        if msg.caption:
            if msg.caption and len(msg.caption) > 1000:
                return await msg.reply(l10n.format_value("too-long-caption-error"))

        if file_type == "photo":
            media.append(types.InputMediaPhoto(media=file_id))

        elif file_type == "video":
            media.append(types.InputMediaVideo(media=file_id))

        elif file_type == "document":
            media.append(types.InputMediaDocument(media=file_id))

    if not media:
        return # Если в группе нет медиа, выходим

    # Добавляем ID пользователя в конец общей подписи
    combined_caption = f"{message[0].html_text}\n\n#id{first_message.from_user.id}"
    media[0].caption = combined_caption
    media[0].parse_mode = 'HTML'

    # Отправляем медиагруппу в целевой чат
    try:
        await bot.send_media_group(
            chat_id=config.admin_chat_id,
            media=media
        )

        # Отправляем подпись отдельным сообщением, если она есть
        # if combined_caption:
        #     await bot.send_message(
        #         chat_id=config.admin_chat_id,
        #         text=combined_caption,
        #         parse_mode="HTML"
        #     )

    except Exception as e:
        print(f"Error sending media group: {e}")
        return

    create_task(_send_expiring_notification(first_message, l10n))

@router.message(SupportedMediaFilter())
async def supported_media(message: Message, l10n: FluentLocalization):
    """
    Хэндлер на медиафайлы от пользователя.
    Поддерживаются только типы, к которым можно добавить подпись (полный список см. в регистраторе внизу)

    :param message: медиафайл от пользователя
    :param l10n: объект локализации
    """

    if message.caption and len(message.caption) > 1000:
        return await message.reply(l10n.format_value("too-long-caption-error"))

    if message.from_user.id in banned:
        await message.answer(l10n.format_value("you-were-banned-error"))

    elif message.from_user.id in shadowbanned:
        return

    else:
        await message.copy_to(
            config.admin_chat_id,
            caption=((message.caption or "") + f"\n\n#id{message.from_user.id}"),
            parse_mode="HTML"
        )
        create_task(_send_expiring_notification(message, l10n))


@router.message()
async def unsupported_types(message: Message, l10n: FluentLocalization):
    """
    Хэндлер на неподдерживаемые типы сообщений, т.е. те, к которым нельзя добавить подпись

    :param message: сообщение от пользователя
    :param l10n: объект локализации
    """
    # Игнорируем служебные сообщения
    if message.content_type not in (
            ContentType.NEW_CHAT_MEMBERS, ContentType.LEFT_CHAT_MEMBER, ContentType.VIDEO_CHAT_STARTED,
            ContentType.VIDEO_CHAT_ENDED, ContentType.VIDEO_CHAT_PARTICIPANTS_INVITED,
            ContentType.MESSAGE_AUTO_DELETE_TIMER_CHANGED, ContentType.NEW_CHAT_PHOTO, ContentType.DELETE_CHAT_PHOTO,
            ContentType.SUCCESSFUL_PAYMENT, "proximity_alert_triggered",  # в 3.0.0b3 нет поддержка этого контент-тайпа
            ContentType.NEW_CHAT_TITLE, ContentType.PINNED_MESSAGE):
        await message.reply(l10n.format_value("unsupported-message-type-error"))
