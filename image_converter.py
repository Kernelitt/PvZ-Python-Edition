from PIL import Image
from tkinter.filedialog import FileDialog
file = input()
# Загрузка изображений
image = Image.open("images/"+ file +".jpg").convert("RGBA")
alpha = Image.open("images/"+ file +"_.png").convert("L")  # черно-белая карта

# Добавление альфа-канала
image.putalpha(alpha)

# Сохранение результата
image.save(file + ".png")
