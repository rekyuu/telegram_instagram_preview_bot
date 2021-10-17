import os
import re
import shutil
import subprocess
from telegram import ChatAction, InputMediaPhoto, InputMediaVideo, Update
from telegram.ext import CallbackContext, Filters, MessageHandler, Updater


def process_message(update: Update, context: CallbackContext) -> None:
    if not update.message:
        return
        
    chat_id = update.message.chat_id
    message_id = update.message.message_id
    message = update.message.text
    
    # Image: https://www.instagram.com/p/CVGdB86vdbS/
    # Album: https://www.instagram.com/p/CVIK7loPKgG/
    # Video: https://www.instagram.com/reel/CU1NOltB_eK/

    if _is_instagram_picture_url(message):
        context.bot.send_chat_action(chat_id, ChatAction.UPLOAD_PHOTO, timeout=600)

        subprocess.call(['instalooter', 'post', message, './data/images'])

        files = os.listdir('./data/images')

        if len(files) > 1:
            photos = []
            for file in files:
                with open(f'./data/images/{file}', 'rb') as filebytes:
                    photos.append(InputMediaPhoto(media=filebytes))

            context.bot.send_media_group(
                chat_id=chat_id, 
                reply_to_message_id=message_id,
                disable_notification=True,
                media=photos)
        else:
            with open(f'./data/images/{files[0]}', 'rb') as filebytes:
                context.bot.send_photo(
                    chat_id=chat_id, 
                    reply_to_message_id=message_id,
                    disable_notification=True,
                    photo=filebytes)

        shutil.rmtree('./data/images')

    elif _is_instagram_video_url(message):
        context.bot.send_chat_action(chat_id, ChatAction.UPLOAD_VIDEO, timeout=600)

        subprocess.call(['youtube-dl', message, '--format', 'mp4', '--output', './data/video.mp4'])

        with open('./data/video.mp4', 'rb') as filebytes:
            context.bot.send_video(
                chat_id=chat_id, 
                reply_to_message_id=message_id,
                disable_notification=True,
                video=filebytes)

        os.remove('./data/video.mp4')


def _is_instagram_picture_url(text: str) -> bool:
    regex = re.compile(r'^((http(s)?://)?(www.)?)?instagram.com/p/.+/?$', re.IGNORECASE)
    return re.match(regex, text) is not None


def _is_instagram_video_url(text: str) -> bool:
    regex = re.compile(r'^((http(s)?://)?(www.)?)?instagram.com/reel/.+/?$', re.IGNORECASE)
    return re.match(regex, text) is not None


def _cleanup():
    try:
        shutil.rmtree('./data/images')
        os.remove('./data/video.mp4')
        os.remove('./data/video.mp4.part')
    except:
        pass


_cleanup()

updater = Updater(token=os.environ['TELEGRAM_TOKEN'], use_context=True)
dispatcher = updater.dispatcher

message_handler = MessageHandler(Filters.text & (~Filters.command), process_message)
dispatcher.add_handler(message_handler)

updater.start_polling()
