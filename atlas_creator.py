import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog
from PIL import Image
import os
import re
import shutil  # Для копирования файла иконки

def create_sprite_atlas(input_folder):
    # Получаем список PNG-файлов и сортируем по имени
    png_files = [f for f in os.listdir(input_folder) if f.lower().endswith('.png')]
    png_files.sort()  # Сортировка по имени (предполагаем последовательность)
    
    if not png_files:
        messagebox.showerror("Ошибка", "В выбранной папке нет PNG-файлов.")
        return
    
    # Извлекаем базовое имя из первого файла (без номера)
    first_file_name = os.path.splitext(png_files[0])[0]  # Убираем расширение, e.g., "walk_0001"
    base_name = re.sub(r'_\d+$', '', first_file_name)  # Удаляем "_числа" в конце, e.g., "walk"
    if not base_name:  # Если после удаления ничего не осталось, используем оригинал
        base_name = first_file_name
    
    output_file = os.path.join(input_folder, f"atlas_{base_name}.png")
    
    # Загружаем первое изображение для определения размера
    first_img = Image.open(os.path.join(input_folder, png_files[0]))
    width, height = first_img.size
    
    # Вычисляем размеры атласа: один ряд, все спрайты в ширину
    num_sprites = len(png_files)
    atlas_width = num_sprites * width
    atlas_height = height  # Высота атласа равна высоте одного спрайта
    
    # Создаём новое изображение для атласа
    atlas = Image.new('RGBA', (atlas_width, atlas_height), (0, 0, 0, 0))  # Прозрачный фон
    
    # Размещаем спрайты горизонтально в одном ряду
    for i, png_file in enumerate(png_files):
        img = Image.open(os.path.join(input_folder, png_file))
        x = i * width  # Сдвиг по X
        y = 0  # Все в одном ряду, Y=0
        atlas.paste(img, (x, y))
    
    # Сохраняем атлас
    atlas.save(output_file)
    messagebox.showinfo("Успех", f"Атлас сохранён как {output_file}")
    return png_files, base_name  # Возвращаем список файлов и базовое имя для иконки

def create_sprite_atlas_with_icon(input_folder):
    png_files, base_name = create_sprite_atlas(input_folder)
    if not png_files:
        return
    
    # Спрашиваем номер кадра для иконки (от 1 до количества кадров)
    num_sprites = len(png_files)
    frame_index = simpledialog.askinteger("Выбор иконки", f"Введите номер кадра для иконки (от 1 до {num_sprites}):", minvalue=1, maxvalue=num_sprites)
    if frame_index is None:  # Пользователь отменил
        return
    
    # Копируем выбранный кадр как иконку
    selected_file = png_files[frame_index - 1]  # Индекс от 0
    icon_file = os.path.join(input_folder, f"icon_{base_name}.png")
    shutil.copy(os.path.join(input_folder, selected_file), icon_file)
    messagebox.showinfo("Успех", f"Иконка сохранена как {icon_file}")

def select_folder():
    folder = filedialog.askdirectory(title="Выберите папку с PNG-файлами")
    if folder:
        create_sprite_atlas(folder)

def select_folder_with_icon():
    folder = filedialog.askdirectory(title="Выберите папку с PNG-файлами")
    if folder:
        create_sprite_atlas_with_icon(folder)

# GUI
root = tk.Tk()
root.title("Конвертер анимации в горизонтальный атлас спрайтов (авто-имя)")
root.geometry("450x250")

label = tk.Label(root, text="Выберите папку с последовательностью PNG-файлов.\nАтлас будет создан в одну линию (только в ширину)\nи сохранён автоматически с именем на основе кадра без номера.")
label.pack(pady=20)

button1 = tk.Button(root, text="Выбрать папку и создать атлас", command=select_folder)
button1.pack(pady=5)

button2 = tk.Button(root, text="Выбрать папку, создать атлас и иконку", command=select_folder_with_icon)
button2.pack(pady=5)

root.mainloop()
