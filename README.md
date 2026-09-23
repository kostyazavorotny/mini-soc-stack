Полноценный микро-стенд мониторинга событий ИБ, построенный на базе микросервисной архитектуры в Docker. Проект симулирует работу SIEM/SOC-системы: пайплайн сбора логов, индексация в OpenSearch и автоматическое выявление сетевых атак.

## Архитектура
`Nginx Target` ──>(Access Logs)──> `Vector Shipper` ──>(Parsed JSON)──> `OpenSearch` ◄──(SIEM API Queries)── `Python SOC Detector`

* **Nginx (Target):** Веб-сервис, генерирующий события доступа.
* **Vector:** Сборщик логов , преобразующий сырые логи в структурированный JSON.
* **OpenSearch:** Хранилище и поисковый движок событий безопасности.
* **Python SOC Detector:** Сервис детекта, проверяющий входящие логи на наличие сигнатур атак (SQLi, LFI, Сканеры ИБ) в реальном времени.

## Стек технологий
* **Infrastructure:** Docker, Docker Compose, Linux
* **SIEM & Log Management:** OpenSearch, Vector Shipper, JSON Parsing
* **Security & Automation:** Python 3 (Requests, Regex), SIEM API Integration, Threat Detection Rules

## запуск

1. Клонировать репозиторий:
   ```bash
   git clone [https://github.com/ВАШ_USERNAME/mini-soc-stack.git](https://github.com/kostyazavorotny/mini-soc-stack.git)
   cd mini-soc-stack
