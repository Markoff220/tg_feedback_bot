# Feedback Bot 🤖  
Этот бот на aiogram собирает обратную связь в Telegram.  

## 📌 Функции  
- Принимает сообщения от пользователей  
- Отправляет их администратору в чат или в лс  
- Поддерживает прием текста, фото, видео, файлов и медиагрупп

## 🚀 Установка и запуск  
Клонируй репозиторий:  
   ```bash
   git clone https://github.com/Markoff220/tg_feedback_bot
   cd tg_feedback_bot
   ```

## Запуск на linux:
   ```bash
   python -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   cp env_example .env
   nano .env
   *Вписываем свои ADMIN_CHAT_ID и BOT_TOKEN*
   python -m bot
   ```

## Запуск на windows:
   ```bash
   python -m venv venv
   ./venv/Scripts/activate
   pip install -r requirements.txt
   copy env_example .env
   .env
   *Вписываем свои ADMIN_CHAT_ID и BOT_TOKEN*
   python -m bot
   ```
   
## Запуск на Docker + Docker Compose (рекомендуется):
   1. Возьмите файл `docker-compose.example.yml` из репозитория и переименуйте как `docker-compose.yml`;
   2. Возьмите файл `env_example` там же, переименуйте как `.env` (с точкой в начале), откройте и заполните переменные;
   3. Запустите бота: `docker compose up -d` (или docker-compose up -d на старых версиях Docker);
   4. Проверьте, что контейнер поднялся: `docker compose ps`


## Принцпи работы:
Сообщения от пользователей копируются методом copyMessage в чат к админу (или админам) с добавлением ID пользователя в виде хэштега, например, #id1234567, к тексту или подписи к медиафайлу. Когда администратор отвечает на сообщение, этот хэштег извлекается, парсится и используется в качестве получателя.

Как переписку видит пользователь:
![image](https://github.com/user-attachments/assets/ef60f027-21ef-49a9-985d-48e0fb1cb290)


В свою очередь, администратор видит так (и может пользоваться расширенным набором команд):
![image](https://github.com/user-attachments/assets/b9057fc7-abaa-4e8e-befd-f2a6e9e54b42)


Ряд команд из админского чата для управления ботом:
![image](https://github.com/user-attachments/assets/8fea2572-5b11-4653-a63c-883869bbee55)


За основу взят telegram-feedback-bot от @MasterGroosha и несколько доработан под свои задачи.


