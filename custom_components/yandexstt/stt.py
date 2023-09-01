"""Speech-to-text YandexCloudSTT conversion service."""
from __future__ import annotations

import logging
from collections.abc import AsyncIterable

import async_timeout
import voluptuous as vol

from homeassistant.components.stt import (
    AudioBitRates,
    AudioChannels,
    AudioCodecs,
    AudioFormats,
    AudioSampleRates,
    Provider,
    SpeechMetadata,
    SpeechResult,
    SpeechResultState,
)
import homeassistant.helpers.config_validation as cv
from homeassistant.const import CONF_API_KEY


import asyncio
import aiohttp
from homeassistant.helpers.aiohttp_client import async_get_clientsession

_LOGGER = logging.getLogger(__name__)

YANDEX_API_URL = "https://stt.api.cloud.yandex.net/speech/v1/stt:recognize"
YANDEX_API_KEY = ""  # AQVNxHgPQDMNmnSVXoWxvUvaGzTH87kEgapMH4rG

SUPPORTED_LANGUAGES = [
    "de-DE",
    "en-US",
    "es-ES",
    "fi-FI",
    "fr-FR",
    "he-HE",
    "it-IT",
    "kk-KZ",
    "nl-NL",
    "pl-PL",
    "pt-PT",
    "pt-BR",
    "ru-RU",
    "sv-SE",
    "tr-TR",
    "uz-UZ",
]
"""Язык, для которого будет выполнено распознавание.
Допустимые значения см. в описании модели. Значение по умолчанию — ru-RU  — русский язык.
"""

TOPIC = "general"
"""Языковая модель, которую следует использовать при распознавании.
Чем точнее выбрана модель, тем лучше результат распознавания. В одном запросе можно указать только одну модель.
Допустимые значения зависят от выбранного языка. Значение параметра по умолчанию: general.

https://cloud.yandex.ru/docs/speechkit/stt/models
"""

PROFANITY_FILTER = False
"""Параметр, регулирующий работу фильтра ненормативной лексики в распознанной речи.

Допустимые значения:
False (по умолчанию) — ненормативная лексика не будет исключена из результатов распознавания;
True — ненормативная лексика будет исключена из результатов распознавания."""

RAW_RESULTS = False
"""Флаг, указывающий, как писать числа. True — писать прописью, False (по умолчанию) — писать цифрами."""


PLATFORM_SCHEMA = cv.PLATFORM_SCHEMA.extend(
    {
        vol.Required(CONF_API_KEY): cv.string,
        vol.Optional("topic", default="general"): vol.In(["general", "general:rc", "general:deprecated"]),
        vol.Optional("profanity_filter", default=False): vol.Boolean(),
        vol.Optional("raw_results", default=False): vol.Boolean(),
    }
)


async def async_get_engine(hass, config, discovery_info=None):
    """Set up YandexCloudSTT speech component."""
    return YandexCloudSTTProvider(hass, config)


class YandexCloudSTTProvider(Provider):
    """YandexCloudSTTProvider API provider."""

    def __init__(self, hass, conf):
        """Init STT service."""
        self.hass = hass
        self._key = conf.get(CONF_API_KEY)
        self._topic = conf.get("topic")
        self._profanity_filter = conf.get("profanity_filter")
        self._raw_results = conf.get("raw_results")
        self.name = "YandexSpeechKit STT"

    @property
    def supported_languages(self):
        """Return a list of supported languages."""
        return SUPPORTED_LANGUAGES

    @property
    def supported_formats(self):
        """Return a list of supported formats."""
        return [AudioFormats.WAV, AudioFormats.OGG]

    @property
    def supported_codecs(self):
        """Return a list of supported codecs."""
        return [AudioCodecs.PCM, AudioCodecs.OPUS]

    @property
    def supported_bit_rates(self):
        """Return a list of supported bit rates."""
        return [AudioBitRates.BITRATE_8, AudioBitRates.BITRATE_16]

    @property
    def supported_sample_rates(self):
        """Return a list of supported sample rates."""
        return [
            AudioSampleRates.SAMPLERATE_8000,
            AudioSampleRates.SAMPLERATE_16000,
            AudioSampleRates.SAMPLERATE_48000
        ]

    @property
    def supported_channels(self):
        """Return a list of supported channels."""
        return [AudioChannels.CHANNEL_MONO]

    async def async_process_audio_stream(
        self, metadata: SpeechMetadata, stream: AsyncIterable[bytes]
    ) -> SpeechResult:
        websession = async_get_clientsession(self.hass)
        # Collect data
        audio_data = b""
        async for chunk in stream:
            audio_data += chunk

        params = {
            "lang": metadata.language,
            "topic": self._topic,
            "profanityFilter": 'true' if self._profanity_filter else 'false',
            "rawResults": 'true' if self._raw_results else 'false',
        }

        if metadata.codec.value == "pcm":
            params["format"] = "lpcm"
            params["sampleRateHertz"] = metadata.sample_rate.value
        else:
            params["format"] = "oggopus"

        try:
            with async_timeout.timeout(10):
                request = await websession.post(YANDEX_API_URL, headers={"Authorization": "Api-Key " + self._key}, params=params, data=audio_data)
                if request.status != 200:
                    error = await request.json()
                    _LOGGER.error("Error %d on load URL %s. Response %s",
                                  request.status, request.url, error)
                    return SpeechResult("["+request.status+"] "+error["error_code"]+" "+error["error_message"], SpeechResultState.ERROR)
                data = await request.json()
        except (asyncio.TimeoutError, aiohttp.ClientError):
            _LOGGER.error("Timeout for yandex speech kit API")
            return SpeechResult("Timeout for yandex speech kit API", SpeechResultState.ERROR)
        return SpeechResult(data["result"], SpeechResultState.SUCCESS)
