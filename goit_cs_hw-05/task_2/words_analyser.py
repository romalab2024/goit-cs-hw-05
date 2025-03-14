import asyncio
import aiohttp
import re
import collections
import concurrent.futures
import matplotlib.pyplot as plt
async def fetch_text(url: str) -> str:
    """Завантажує текст із заданої URL-адреси."""
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            return await response.text()
def clean_text(text: str) -> list:
    """Очищує текст від пунктуації та розбиває його на слова."""
    text = re.sub(r'[^a-zA-Z\s]', '', text)  # Видаляємо все, крім літер та пробілів
    words = text.lower().split()  # Приводимо до нижнього регістру
    return words
def map_reduce(words: list) -> collections.Counter:
    """Рахує частоту слів (реалізація парадигми MapReduce)."""
    return collections.Counter(words)
async def process_text(words: list) -> collections.Counter:
    """Запускає MapReduce у багатопотоковому режимі."""
    loop = asyncio.get_running_loop()
    with concurrent.futures.ThreadPoolExecutor() as pool:
        result = await loop.run_in_executor(pool, map_reduce, words)
    return result
def visualize_top_words(counter: collections.Counter, top_n: int = 10):
    """Будує графік для топ N найбільш вживаних слів."""
    top_words = counter.most_common(top_n)
    words, counts = zip(*top_words)  # Розпаковуємо список у два окремі списки

    plt.figure(figsize=(10, 5))
    plt.barh(words[::-1], counts[::-1], color="skyblue")  # Перевертаємо список для гарного вигляду
    plt.xlabel("Частота")
    plt.ylabel("Слова")
    plt.title(f"Топ {top_n} найбільш вживаних слів")
    plt.show()
async def main():
    url = "https://www.gutenberg.org/files/1342/1342-0.txt"  # "Гордість і упередження" Джейн Остін
    
    print("📥 Завантаження тексту...")
    text = await fetch_text(url)

    print("📝 Очищення тексту...")
    words = clean_text(text)

    print("🧠 Обробка слів за допомогою MapReduce...")
    word_counts = await process_text(words)

    print("📊 Візуалізація...")
    visualize_top_words(word_counts)

if __name__ == "__main__":
    asyncio.run(main())
