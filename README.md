# Yandex-stt-speechkit

# Установка через HACS
Вставьте ссылку https://github.com/xpolter/Yandex-sst-speechkit в раздел CUSTOM REPOSITORIES в HACS

# Конфигурация

https://cloud.yandex.ru/docs/speechkit/stt/api/request-api

```
stt:
  platform: yandexstt
  api_key: "AQVNxHgPQDMNmnSVXoWxvUvaGzTH87kEgapMH4rG"
  topic: "general"
  profanity_filter: false
  raw_results: false
```

Ошибка в логах:
```
ERROR (MainThread) [homeassistant.helpers.config_validation] The stt integration does not support any configuration parameters, got
```
Причина: https://github.com/home-assistant/core/issues/97161
