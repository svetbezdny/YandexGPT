import requests
import json


FOLDER_ID = ""  # идентификатор каталога
API_KEY = ""  # API ключ


def get_answer(query: str, mode: str = "yandexgpt-lite") -> None:
    """
    Функция для взаимодействия с YandexGPT API.

    Параметры:
        - query (str): Запрос к API.
        - mode (str, optional): Режим работы (по умолчанию: yandexgpt-lite).
            Возможные значения:
            - yandexgpt-lite: Промт-режим.
            - summarization: Суммаризация.
    """
    headers = {
        "Authorization": f"Api-Key {API_KEY}",
        "Content-Type": "application/json",
        "x-data-logging-enabled": "false",  # не сохраняем логи на серверах Yandex Cloud
    }
    data = {}
    body = {
        "modelUri": f"gpt://{FOLDER_ID}/{mode}",
        "completionOptions": {
            "stream": False,  # true/false, включает потоковую передачу частично сгенерированного текста
            "temperature": 0.7,  # [0-1], чем выше, тем более креативными и случайными будут ответы
            "maxTokens": "2000",  # устанавливает ограничение на выход модели в токенах
        },
        "messages": [{"role": "system", "text": query}],
    }
    json_data = json.dumps(body, ensure_ascii=False).encode("utf-8")
    web = requests.post(
        url="https://llm.api.cloud.yandex.net/foundationModels/v1/completion",
        headers=headers,
        params=data,
        data=json_data,
    )
    try:
        result = web.json()["result"]["alternatives"][0]["message"]["text"]
    except:
        result = {
            "Code": web.json()["error"]["httpCode"],
            "Text": web.json()["error"]["message"],
        }
    print(result)
