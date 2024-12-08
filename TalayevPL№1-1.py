import os
import requests
from tqdm.auto import tqdm
from shutil import copyfileobj

def fetch_resource(resource_url: str, save_to: str = None) -> None:
    try:
        # Выполняем запрос на получение ресурса
        with requests.get(resource_url, stream=True) as response:
            response.raise_for_status()
            
            # Если путь для сохранения не указан, используем имя файла из URL
            file_name = os.path.basename(response.url) if not save_to else os.path.basename(save_to)
            destination = save_to if save_to else file_name

            # Определяем общий размер
            content_size = int(response.headers.get("Content-Length", 0))

            # Настройка прогресс-бара для отображения в одной строке
            with tqdm(
                total=content_size,
                desc=f"Загрузка {file_name}",
                unit="B",
                unit_scale=True,
                dynamic_ncols=True,  
                leave=False          
            ) as progress_bar, open(destination, "wb") as output_file:
                for chunk in response.iter_content(chunk_size=1024):
                    output_file.write(chunk)
                    progress_bar.update(len(chunk))

            print(f"\nЗагрузка завершена: {destination}")

    except requests.exceptions.RequestException as err:
        print(f"Не удалось загрузить ресурс: {err}")
    except Exception as unexpected_error:
        print(f"Произошла ошибка: {unexpected_error}")


if __name__ == "__main__":
    url_input = input("Укажите ссылку на файл: ").strip()
    fetch_resource(url_input)
