"""Support for the demo for speech to text service."""
from typing import List

from aiohttp import StreamReader

from homeassistant.components.stt import Provider, SpeechMetadata, SpeechResult
from homeassistant.components.stt.const import (
    AudioBitRates,
    AudioChannels,
    AudioCodecs,
    AudioFormats,
    AudioSampleRates,
    SpeechResultState,
)

SUPPORTED_LANGUAGES = [
    "af-ZA",
    "sq-AL",
    "am-ET",
    "ar-DZ",
    "ar-BH",
    "ar-EG",
    "ar-IQ",
    "ar-IL",
    "ar-JO",
    "ar-KW",
    "ar-LB",
    "ar-MA",
    "ar-OM",
    "ar-QA",
    "ar-SA",
    "ar-PS",
    "ar-TN",
    "ar-AE",
    "ar-YE",
    "hy-AM",
    "az-AZ",
    "eu-ES",
    "bn-BD",
    "bn-IN",
    "bs-BA",
    "bg-BG",
    "my-MM",
    "ca-ES",
    "zh-CN",
    "zh-TW",
    "hr-HR",
    "cs-CZ",
    "da-DK",
    "nl-BE",
    "nl-NL",
    "en-AU",
    "en-CA",
    "en-GH",
    "en-HK",
    "en-IN",
    "en-IE",
    "en-KE",
    "en-NZ",
    "en-NG",
    "en-PK",
    "en-PH",
    "en-SG",
    "en-ZA",
    "en-TZ",
    "en-GB",
    "en-US",
    "et-EE",
    "fil-PH",
    "fi-FI",
    "fr-BE",
    "fr-CA",
    "fr-FR",
    "fr-CH",
    "gl-ES",
    "ka-GE",
    "de-AT",
    "de-DE",
    "de-CH",
    "el-GR",
    "gu-IN",
    "iw-IL",
    "hi-IN",
    "hu-HU",
    "is-IS",
    "id-ID",
    "it-IT",
    "it-CH",
    "ja-JP",
    "jv-ID",
    "kn-IN",
    "kk-KZ",
    "km-KH",
    "ko-KR",
    "lo-LA",
    "lv-LV",
    "lt-LT",
    "mk-MK",
    "ms-MY",
    "ml-IN",
    "mr-IN",
    "mn-MN",
    "ne-NP",
    "no-NO",
    "fa-IR",
    "pl-PL",
    "pt-BR",
    "pt-PT",
    "ro-RO",
    "ru-RU",
    "sr-RS",
    "si-LK",
    "sk-SK",
    "sl-SI",
    "es-AR",
    "es-BO",
    "es-CL",
    "es-CO",
    "es-CR",
    "es-DO",
    "es-EC",
    "es-SV",
    "es-GT",
    "es-HN",
    "es-MX",
    "es-NI",
    "es-PA",
    "es-PY",
    "es-PE",
    "es-PR",
    "es-ES",
    "es-US",
    "es-UY",
    "es-VE",
    "su-ID",
    "sw-KE",
    "sw-TZ",
    "sv-SE",
    "ta-IN",
    "ta-MY",
    "ta-SG",
    "ta-LK",
    "te-IN",
    "th-TH",
    "tr-TR",
    "uk-UA",
    "ur-IN",
    "ur-PK",
    "uz-UZ",
    "vi-VN",
    "zu-ZA",
]


async def async_get_engine(hass, config, discovery_info=None):
    """Set up Demo speech component."""
    return DemoProvider()


class DemoProvider(Provider):
    """Demo speech API provider."""

    @property
    def supported_languages(self) -> List[str]:
        """Return a list of supported languages."""
        return SUPPORTED_LANGUAGES

    @property
    def supported_formats(self) -> List[AudioFormats]:
        """Return a list of supported formats."""
        return [AudioFormats.WAV, AudioFormats.OGG]

    @property
    def supported_codecs(self) -> List[AudioCodecs]:
        """Return a list of supported codecs."""
        return [AudioCodecs.PCM, AudioCodecs.OPUS]

    @property
    def supported_bit_rates(self) -> List[AudioBitRates]:
        """Return a list of supported bit rates."""
        return [AudioBitRates.BITRATE_8, AudioBitRates.BITRATE_16, AudioBitRates.BITRATE_24, AudioBitRates.BITRATE_32]

    @property
    def supported_sample_rates(self) -> List[AudioSampleRates]:
        """Return a list of supported sample rates."""
        return [
            AudioSampleRates.SAMPLERATE_8000,
            AudioSampleRates.SAMPLERATE_11000,
            AudioSampleRates.SAMPLERATE_16000,
            AudioSampleRates.SAMPLERATE_18900,
            AudioSampleRates.SAMPLERATE_22000,
            AudioSampleRates.SAMPLERATE_32000,
            AudioSampleRates.SAMPLERATE_37800,
            AudioSampleRates.SAMPLERATE_44100,
            AudioSampleRates.SAMPLERATE_48000
            ]

    @property
    def supported_channels(self) -> List[AudioChannels]:
        """Return a list of supported channels."""
        return [AudioChannels.CHANNEL_MONO, AudioChannels.CHANNEL_STEREO]

    async def async_process_audio_stream(
        self, metadata: SpeechMetadata, stream: StreamReader
    ) -> SpeechResult:
        """Process an audio stream to STT service."""

        # Read available data
        async for _ in stream.iter_chunked(4096):
            pass

        return SpeechResult("Turn the Kitchen Lights on", SpeechResultState.SUCCESS)