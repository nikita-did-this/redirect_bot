# redirect_bot
Бот пересылает спам мемов на канал, убирая всё, кроме самого изображения/видео

## Самостоятельный запуск бота:  
1. Создать в корне виртуальное окружение и установить все необходимые зависимости командой **"pip install -r requirements.txt"**
2. В корне создать файл **.env**
3. Создать бота, используя **BotFather**
4. В файле .env инициализировать две переменные: *BOT_API* и *CHAT_ID*
5. Присвоить переменной *BOT_API* значение токена, который предоставил **BotFather** при создании бота, а переменной *CHAT_ID* - идентификатора чата в формате "@your_chat_id"
6. Запуск бота производить через терминал командой **"python main.py"**