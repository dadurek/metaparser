from typing import Dict, List, Optional

import eyed3  # type: ignore
import eyed3.mp3  # type: ignore

from .base import BaseParser

FIELD_COMPOSER = "composer"
FIELD_ARTIST = "artist"
FIELD_ALBUM = "album"
FIELD_ALBUM_ARTIST = "album_artist"
FIELD_TITLE = "title"
FIELD_TRACK_NUM = "track_num"
FIELD_PUBLISHER = "publisher"
FIELD_GENRE = "genre"
FIELD_ALBUM_TYPE = "album_type"
FIELD_ARTIST_ORIGIN = "artist_origin"
FIELD_ARTIST_URL = "artist_url"
FIELD_AUDIO_FILE_URL = "audio_file_url"
FIELD_AUDIO_SOURCE_URL = "audio_source_url"
FIELD_BEST_RELEASE_DATE = "best_release_date"
FIELD_BPM = "bmp"
FIELD_CD_ID = "cd_id"
FIELD_COMMERCIAL_URL = "commercial_url"
FIELD_COPYRIGHT = "copyright"
FIELD_COPYRIGHT_URL = "copyright_url"
FIELD_ENCODED_BY = "encoded_by"
FIELD_ENCODING_DATE = "encoding_date"
FIELD_INTERNET_RADIO_URL = "internet_radio_url"
FIELD_ORIGINAL_ARTIST = "original_artist"
FIELD_ORIGINAL_RELEASE_DATE = "original_release_date"
FIELD_PAYMENT_URL = "payment_url"
FIELD_PLAY_COUNT = "play_count"
FIELD_PUBLISHER_URL = "publisher_url"
FIELD_READ_ONLY = "read_only"
FIELD_RECORDING_DATE = "recording_date"
FIELD_RELEASE_DATE = "release_date"
FIELD_TAGGING_DATE = "tagging_date"
FIELD_TERMS_OF_USE = "terms_of_use"


class Mp3Parser(BaseParser):
    @staticmethod
    def supported_mimes() -> List[str]:
        return ["audio/mpeg"]

    def __init__(self) -> None:
        super().__init__()
        self.__tag = None

    def parse(self, filename: str) -> None:
        file = eyed3.load(filename)
        self.__tag = file.tag

    def get_fields(self) -> List[str]:
        return [
            FIELD_PUBLISHER,
            FIELD_ARTIST,
            FIELD_ALBUM,
            FIELD_ALBUM_ARTIST,
            FIELD_TITLE,
            FIELD_TRACK_NUM,
            FIELD_GENRE,
            FIELD_COMPOSER,
            FIELD_ALBUM_TYPE,
            FIELD_ARTIST_ORIGIN,
            FIELD_ARTIST_URL,
            FIELD_AUDIO_FILE_URL,
            FIELD_AUDIO_SOURCE_URL,
            FIELD_BEST_RELEASE_DATE,
            FIELD_BPM,
            FIELD_CD_ID,
            FIELD_COMMERCIAL_URL,
            FIELD_COPYRIGHT,
            FIELD_COPYRIGHT_URL,
            FIELD_ENCODED_BY,
            FIELD_ENCODING_DATE,
            FIELD_INTERNET_RADIO_URL,
            FIELD_ORIGINAL_ARTIST,
            FIELD_ORIGINAL_RELEASE_DATE,
            FIELD_PAYMENT_URL,
            FIELD_PLAY_COUNT,
            FIELD_PUBLISHER_URL,
            FIELD_READ_ONLY,
            FIELD_RECORDING_DATE,
            FIELD_RELEASE_DATE,
            FIELD_TAGGING_DATE,
            FIELD_TERMS_OF_USE,
        ]

    def set_field(self, field: str, value: Optional[str]) -> None:
        if self.__tag is None:
            raise TypeError("Tag is null, parse the file first")
        if field not in self.get_fields():
            raise KeyError("Field not present in parser")
        setattr(self.__tag, field, value)

    def clear(self):
        self.__tag.clear()

    def delete_field(self, field: str) -> None:
        self.set_field(field, None)

    def get_all_values(self) -> Dict[str, str]:
        if self.__tag is None:
            raise TypeError("Tag is null, parse the file first")
        values = {}
        for field in self.get_fields():
            if hasattr(self.__tag, field):
                attr = getattr(self.__tag, field, None)
                if attr is not None and (isinstance(attr, tuple) and any(attr)):
                    values[field] = attr
        return values

    def write(self) -> None:
        self.__tag.save()  # type: ignore
