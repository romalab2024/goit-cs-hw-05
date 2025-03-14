import asyncio
import aiofiles
import aiopath
import argparse
import os
import logging
import random
import string

# Налаштування логування
logging.basicConfig(
    filename="file_sorter.log",
    level=logging.ERROR,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

# Функція для створення випадкових файлів
async def generate_random_files(folder: aiopath.AsyncPath, num_files: int = 30):
    extensions = [".txt", ".pdf", ".png", ".docx", ".csv", ".log", ".json", ".xml"]
    
    await folder.mkdir(parents=True, exist_ok=True)  # Створюємо папку, якщо її немає
    
    for _ in range(num_files):
        ext = random.choice(extensions)
        file_name = ''.join(random.choices(string.ascii_letters + string.digits, k=8)) + ext
        file_path = folder / file_name

        content = ''.join(random.choices(string.ascii_letters + string.digits, k=100))  # Випадковий вміст
        
        try:
            async with aiofiles.open(file_path, 'w') as file:
                await file.write(content)
            print(f"Файл {file_name} створено у {folder}")
        except Exception as e:
            logging.error(f"Помилка створення файлу {file_name}: {e}")

# Функція для рекурсивного читання та сортування файлів
async def read_folder(source: aiopath.AsyncPath, output: aiopath.AsyncPath):
    try:
        async for item in source.iterdir():
            if await item.is_file():
                await copy_file(item, output)
            elif await item.is_dir():
                await read_folder(item, output)
    except Exception as e:
        logging.error(f"Помилка читання папки {source}: {e}")

# Функція копіювання файлу в нову папку
async def copy_file(file_path: aiopath.AsyncPath, output: aiopath.AsyncPath):
    try:
        ext = file_path.suffix[1:] or "unknown"  # Отримуємо розширення
        dest_folder = output / ext
        await dest_folder.mkdir(parents=True, exist_ok=True)

        dest_file = dest_folder / file_path.name

        async with aiofiles.open(file_path, 'rb') as src, aiofiles.open(dest_file, 'wb') as dst:
            await dst.write(await src.read())  # Читаємо та записуємо файл асинхронно

        print(f"Файл {file_path.name} скопійовано до {dest_folder}")
    except Exception as e:
        logging.error(f"Помилка копіювання файлу {file_path}: {e}")

# Головна функція
async def main():
    source = aiopath.AsyncPath("D:/GoIT/PROJECTS Python/Comp_Systems/goit_cs_hw-05/random files")
    output = aiopath.AsyncPath("D:/GoIT/PROJECTS Python/Comp_Systems/goit_cs_hw-05/sorted files")

    # Генеруємо файли
    await generate_random_files(source, 30)

    # Сортуємо файли
    if not await source.exists():
        print(f"Помилка: вихідна папка {source} не існує!")
        return

    await read_folder(source, output)

if __name__ == "__main__":
    asyncio.run(main())
