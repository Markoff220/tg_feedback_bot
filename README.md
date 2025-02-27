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
   cd tg_feedback_bot```

Запуск на linux:
   ```bash
   python -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   cp env_example .env
   nano .env
   *Вписываем свои ADMIN_CHAT_ID и BOT_TOKEN*
   python -m bot```
   
   
