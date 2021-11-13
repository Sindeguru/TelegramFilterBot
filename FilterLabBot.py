import telebot
from telebot import types
import cv2

bot = telebot.TeleBot('2120584682:AAHMhg6Lvy3iNQoTIh6hqymT2l5Or6OsZfE')

@bot.message_handler(content_types=['text', 'photo'])
def get_text_messages(message):
    if message.text.lower() == "привет":
        bot.send_message(message.from_user.id, "Привет, чем я могу тебе помочь?")
    elif message.text == "/help":
        bot.send_message(message.from_user.id,
                        "Я бот Семен. Накладываю фильтры на твое изображение. Попробуй - /filter")
    elif message.text == "/filter":
        rmk = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
        rmk.add(types.KeyboardButton('1'), types.KeyboardButton('2'), types.KeyboardButton('3'))
        msg = bot.send_message(message.from_user.id, "Выбери фильтр.\n1) Bilateral\n2) Median Blur\n3) Threshold", reply_markup=rmk)
        bot.register_next_step_handler(msg, filter)

    else:
        bot.send_message(message.from_user.id, "Я тебя не понимаю. Напиши /help.")


def filter(message):
    msg = bot.send_message(message.from_user.id, "Отправь мне изображение")
    if message.text.lower() == "1":
        bot.register_next_step_handler(msg, bilateralFilter)
    if message.text.lower() == "2":
        bot.register_next_step_handler(msg, medianBlurFilter)
    if message.text.lower() == "3":
        bot.register_next_step_handler(msg, thresholdFilter)

def bilateralFilter(message):
    fileID = message.photo[-1].file_id
    file_info = bot.get_file(fileID)
    img = bot.download_file(file_info.file_path)
    with open("image.jpg", 'wb') as new_file:
        new_file.write(img)
    img = cv2.imread("image.jpg")
    bilateral = cv2.bilateralFilter(img, 3, 75, 75)
    cv2.imwrite("image.jpg", bilateral)
    img = open("image.jpg", 'rb')
    bot.send_photo(message.from_user.id, img)

def medianBlurFilter(message):
    fileID = message.photo[-1].file_id
    file_info = bot.get_file(fileID)
    img = bot.download_file(file_info.file_path)
    with open("image.jpg", 'wb') as new_file:
        new_file.write(img)
    img = cv2.imread("image.jpg")
    medBl = cv2.medianBlur(img, 3)
    cv2.imwrite("image.jpg", medBl)
    img = open("image.jpg", 'rb')
    bot.send_photo(message.from_user.id, img)

def thresholdFilter(message):
    fileID = message.photo[-1].file_id
    file_info = bot.get_file(fileID)
    img = bot.download_file(file_info.file_path)
    with open("image.jpg", 'wb') as new_file:
        new_file.write(img)
    img = cv2.imread("image.jpg")
    _, threshold_image = cv2.threshold(img, 127, 255, 0)
    cv2.imwrite("image.jpg", threshold_image)
    img = open("image.jpg", 'rb')
    bot.send_photo(message.from_user.id, img)


bot.polling(none_stop=True, interval=0)