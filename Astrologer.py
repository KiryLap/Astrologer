import random
import io
from tkinter import END
import customtkinter
import sqlite3
from PIL import Image, ImageTk

# Открытие базы данных
db = sqlite3.connect('constellations.db')
c = db.cursor()

# Генерируем список длиной 33 элемента с хаотичным расположением элементов
lst_indx = random.sample(range(1, 34), 33)
k = 0
wrong_ans = 0

# Выберите случайное изображение из базы данных
c.execute("SELECT image FROM constellations WHERE id=?", (lst_indx[k],))
image_data = c.fetchone()[0]

#Создание окна приложения
app = customtkinter.CTk()
app.title("Созвездия")
app.geometry("900x650")
app.resizable(False, False)

#Получения списка названий созвездий с базы данных
c.execute("SELECT name FROM constellations")
constellation_names = c.fetchall()

# Создание списка названий созвездий
background_label = customtkinter.CTkLabel(app, text="", width=300, height=630, bg_color="gray18", corner_radius=100)
background_label.place(x=550, y=10)
background_label_img = customtkinter.CTkLabel(app, text="", width=445, height=630, bg_color="gray18", corner_radius=100)
background_label_img.place(x=77, y=10)
label_constellation_names = customtkinter.CTkLabel(app, text='Название оставшихся созвездий:\n' + '\n'.join(
    [name[0] for name in constellation_names]), font=("Arial", 15, "bold"), bg_color='grey18')
label_constellation_names.place(x=580, y=20)

# Создание надписи-оповещения над картинкой
label = customtkinter.CTkLabel(app, text='Как называется это созвездие?', font=("Arial", 20, "bold"), bg_color="gray18")
label.place(x=150, y=20)

# Создание кнопки и поля ввода
entry = customtkinter.CTkEntry(app, placeholder_text="Введите ответ", bg_color='gray18')
entry.place(x=230, y=510)

# Преобразуйте данные изображения в объект PIL.Image
image = Image.open(io.BytesIO(image_data))
# Создание объекта CTkImage из объекта PIL.Image
image_tk = customtkinter.CTkImage(light_image=image, size=(400, 400))

# Создание счётчиков ответов
label_correct_answers = customtkinter.CTkLabel(app, text=f"Правильных ответов: {k}/{len(lst_indx)}",
                                               font=("Arial", 16, "bold"), bg_color="gray18")
label_correct_answers.place(x=200, y=450)
label_not_correct_answers = customtkinter.CTkLabel(app, text=f"Неверных ответов: {wrong_ans}/5",
                                                   font=("Arial", 16, "bold"), bg_color="gray18")
label_not_correct_answers.place(x=210, y=470)

# Создание метки и вывод изображения на окно
label_img = customtkinter.CTkLabel(app, image=image_tk, text='')
label_img.place(x=100, y=50)


def restart():
    # Объявляем глобальные переменные, которые будут использоваться внутри функции
    global wrong_ans
    global k
    global constellation_names

    # Выполняем SQL-запрос для получения названий созвездий из базы данных
    c.execute("SELECT name FROM constellations")
    # Получаем все результаты запроса и сохраняем их в переменную
    constellation_names = c.fetchall()

    # Обновляем текст на экране с названиями оставшихся созвездий
    label_constellation_names.configure(app, text='Название оставшихся созвездий:\n' + '\n'.join(
        [name[0] for name in constellation_names]), font=("Arial", 15, "bold"))

    # Сбрасываем счетчики правильных и неправильных ответов
    k = 0
    wrong_ans = 0

    # Обновляем текст на экране с вопросом о созвездии
    label.configure(text='Как называется это созвездие?', font=("Arial", 20, "bold"))
    label.place(x=150, y=20)

    # Перемешиваем индексы созвездий для вывода в случайном порядке
    random.shuffle(lst_indx)

    # Выбираем случайное созвездие из базы данных и получаем его изображение
    c.execute("SELECT image FROM constellations WHERE id=?", (lst_indx[k],))
    new_image_data = c.fetchone()[0]
    new_image = Image.open(io.BytesIO(new_image_data))

    # Отображаем изображение на экране
    image_tk = customtkinter.CTkImage(light_image=new_image, size=(400, 400))
    label_img = customtkinter.CTkLabel(app, image=image_tk, text='')
    label_img.place(x=100, y=50)

    # Обновляем счетчик правильных ответов
    label_correct_answers.configure(app, text=f"Правильных ответов: {k}/{len(lst_indx)}")

    # Обновляем счетчик неправильных ответов
    label_not_correct_answers.configure(text=f"Неверных ответов: {wrong_ans}/5")


def button_callback():
    global k
    global wrong_ans
    global constellation_names

    # Получаем текст из поля ввода
    user_input = entry.get()

    # Выбираем название созвездия из базы данных по его индексу
    c.execute("SELECT name FROM constellations WHERE id=?", (lst_indx[k],))
    correct_name = c.fetchone()[0]

    # Проверяем, совпадает ли введенное название созвездия с правильным или равно "r"
    if user_input.lower() == correct_name.lower() or user_input.lower() == "r":
        # Обновляем текст на экране
        label.configure(text="Правильно! Продолжай в том же духе.", font=("Arial", 20, "bold"))
        label.place(x=110, y=20)

        # Удаляем использованное созвездие из списка оставшихся
        constellation_names = [name for name in constellation_names if name[0].lower() != correct_name.lower()]
        label_constellation_names.configure(
            text='Название оставшихся созвездий:\n' + '\n'.join([name[0] for name in constellation_names]))

        # Увеличиваем счетчик правильных ответов
        k += 1

        # Если еще есть созвездия для проверки, то выбираем следующее
        if k < len(lst_indx):
            c.execute("SELECT image FROM constellations WHERE id=?", (lst_indx[k],))
            new_image_data = c.fetchone()[0]
            new_image = Image.open(io.BytesIO(new_image_data))
            image_tk = customtkinter.CTkImage(light_image=new_image, size=(400, 400))
            label_img = customtkinter.CTkLabel(app, image=image_tk, text='')
            label_img.place(x=100, y=50)
            entry.delete(0, END)
            label_correct_answers.configure(text=f"Правильных ответов: {k}/{len(lst_indx)}")
        else:
            # Если все созвездия проверены, то запускаем новую вкладку с сообщением об успехе
            restart()
            new_app = customtkinter.CTk()
            new_app.title("Успешно!")
            new_app.geometry("420x100")
            new_label = customtkinter.CTkLabel(new_app, text="Поздравляем! \n Вы успешно прошли обучение!",
                                               font=("Arial", 20, "bold"))
            new_label.pack(pady=20)
            new_app.mainloop()
    else:
        # Обновляем текст на экране с сообщением о неправильном ответе
        if correct_name.lower() == 'большая медведица' or correct_name.lower() == "большой пёс":
            label.configure(text=f"Неверно. Правильный ответ: {correct_name.lower()}", font=("Arial", 16, "bold"))
            label.place(x=97, y=20)
        else:
            label.configure(text=f"Неверно. Правильный ответ: {correct_name.lower()}", font=("Arial", 20, "bold"))
            label.place(x=130, y=20)

        # Увеличиваем счетчик неправильных ответов
        wrong_ans += 1
        entry.delete(0, END)
        label_not_correct_answers.configure(text=f"Неверных ответов: {wrong_ans}/5")

        # Если количество неправильных ответов достигло 5, то запускаем новую вкладку с сообщением о провале
        if wrong_ans >= 5:
            restart()
            new_app = customtkinter.CTk()
            new_app.title("Провал :(")
            new_app.geometry("420x100")
            new_label = customtkinter.CTkLabel(new_app,
                                               text="Вы допустили слишком много ошибок! \n Пройдите тест заново.",
                                               font=("Arial", 20, "bold"))
            new_label.pack(pady=20)
            new_app.mainloop()
        else:
            pass


# Создание кнопок
button = customtkinter.CTkButton(app, text="Проверить", command=button_callback, bg_color='gray18')
button.place(x=230, y=550)
button_restart = customtkinter.CTkButton(app, text="Заново", command=restart, bg_color='gray18', fg_color='#D63B2F',
                                         hover_color='#992A22')
button_restart.place(x=230, y=590)
# Запуск приложения
app.mainloop()
