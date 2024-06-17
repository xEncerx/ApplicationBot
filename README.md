[![Python](https://img.shields.io/badge/python-3.11-blue.svg)](https://www.python.org/downloads/)
[![aiogram](https://img.shields.io/badge/aiogram-3.x-blue.svg)](https://github.com/aiogram/aiogram)

# Бот для приема заявок
### 📃 | О боте
- **Этот бот поможет вам отбирать кандидатов в вашу команду. Вы создаете вопросы, которые хотите задать, а бот собирает ответы. Администратор получает ответы в отдельный канал, где может одобрить или отклонить заявку.**
### 🛠 | Для запуска бота
- Установите python 3.x (Протестировано на 3.11)
- Далее, установите все библиотеки из файла requirements.txt
  ```
  pip install -r requirements.txt
  ```
- Заполняем файл **config.ini** Инструкция: https://telegra.ph/Zapolnenie-nastroek-bota-06-11
- Заполняем модель вопросов **bot/data/application_model.py** Инструкция: https://telegra.ph/Redaktirovanie-modeli-zayavok-06-11
- Не устраивает сдандартный текст? Измените его в файле **bot/data/bot_text.py**
- Запустите файл main.py / run.bat и наслаждайтесь!

## ❤️ Вклад и поддержка

Если у вас есть предложения по улучшению этого проекта или вы столкнулись с проблемами, пожалуйста, создайте новый issue или отправьте pull request.
