# Server Control Space

## English

### Directory Retention Manager

A Python script that automatically manages and cleans up dated directories based on a configured retention policy. It parses dates from folder names, sorts them chronologically, and removes the oldest folders once a specified limit is reached.

### Features
* **Flexible Date Parsing:** Uses the `dateparser` library to intelligently extract dates from various directory naming formats.
* **Configurable Limits:** Define the maximum number of folders to keep for different target paths using a JSON file.
* **Deletion Logging:** Records all deleted folders with timestamps into `DELETE_LOG.txt` for easy auditing.

### Requirements
* Python 3.6+
* `dateparser` library

Install the required dependency using pip:
```bash
pip install dateparser
```


## Ukrainian

Python-скрипт, який автоматично керує та очищає застарілі директорії на основі налаштованої політики зберігання. Він розпізнає дати з назв папок, сортує їх у хронологічному порядку та видаляє найстаріші папки, коли досягається встановлений ліміт.

### Особливості
* **Гнучке розпізнавання дат:** Використовує бібліотеку `dateparser` для інтелектуального вилучення дат із різноманітних форматів назв директорій.
* **Настроювані ліміти:** Дозволяє задати максимальну кількість папок для зберігання для різних шляхів за допомогою JSON-файлу.
* **Логування видалень:** Записує всі видалені папки з часовими мітками у файл `DELETE_LOG.txt` для зручного аудиту.

### Вимоги
* Python 3.6+
* Бібліотека `dateparser`

Встановіть необхідну залежність за допомогою pip:
```bash
pip install dateparser
```
