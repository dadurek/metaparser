from typing import Any, Dict, List

import mutagen  # type: ignore
import mutagen.easymp4  # type: ignore

from .base import BaseParser

FIELD_TITLE = "title"
FIELD_ALBUM = "album"
FIELD_ARTIST = "artist"
FIELD_ALBUM_ARTIST = "albumartist"
FIELD_DATE = "date"
FIELD_COMMENT = "comment"
FIELD_DESCRIPTION = "description"
FIELD_GROUPING = "grouping"
FIELD_GENRE = "genre"
FIELD_COPYRIGHT = "copyright"
FIELD_ALBUM_SORT = "albumsort"
FIELD_ALBUM_ARTIST_SORT = "albumartistsort"
FIELD_ARTIST_SORT = "artistsort"
FIELD_TITLE_SORT = "titlesort"
FIELD_COMPOSER_SORT = "composersort"
FIELD_MUSICBRAINZ_ARTIST_ID = "musicbrainz_artistid"
FIELD_MUSICBRAINZ_TRACK_ID = "musicbrainz_trackid"
FIELD_MUSICBRAINZ_ALBUM_ID = "musicbrainz_albumid"
FIELD_MUSICBRAINZ_ALBUM_ARTIST_ID = "musicbrainz_albumartistid"
FIELD_MUSICIP_PUID = "musicip_puid"
FIELD_MUSICBRAINZ_ALBUM_STATUS = "musicbrainz_albumstatus"
FIELD_MUSICBRAINZ_ALBUM_TYPE = "musicbrainz_albumtype"
FIELD_RELEASE_COUNTRY = "releasecountry"
FIELD_BPM = "bpm"
FIELD_TRACK_NUMBER = "tracknumber"
FIELD_DISC_NUMBER = "discnumber"


class Mp4Parser(BaseParser):
    @staticmethod
    def supported_mimes() -> List[str]:
        return ["video/mp4"]

    def __init__(self) -> None:
        super().__init__()
        self.__file: mutagen.easymp4.EasyMP4

    def parse(self, filename: str) -> None:
        self.__file = mutagen.easymp4.EasyMP4(filename)

    def get_fields(self) -> List[str]:
        return [
            FIELD_TITLE,
            FIELD_ALBUM,
            FIELD_ARTIST,
            FIELD_ALBUM_ARTIST,
            FIELD_DATE,
            FIELD_COMMENT,
            FIELD_DESCRIPTION,
            FIELD_GROUPING,
            FIELD_GENRE,
            FIELD_COPYRIGHT,
            FIELD_ALBUM_SORT,
            FIELD_ALBUM_ARTIST_SORT,
            FIELD_ARTIST_SORT,
            FIELD_TITLE_SORT,
            FIELD_COMPOSER_SORT,
            FIELD_MUSICBRAINZ_ARTIST_ID,
            FIELD_MUSICBRAINZ_TRACK_ID,
            FIELD_MUSICBRAINZ_ALBUM_ID,
            FIELD_MUSICBRAINZ_ALBUM_ARTIST_ID,
            FIELD_MUSICIP_PUID,
            FIELD_MUSICBRAINZ_ALBUM_STATUS,
            FIELD_MUSICBRAINZ_ALBUM_TYPE,
            FIELD_RELEASE_COUNTRY,
            FIELD_BPM,
            FIELD_TRACK_NUMBER,
            FIELD_DISC_NUMBER,
        ]

    def set_field(self, field: str, value: Any) -> None:
        super().set_field(field, value)
        self.__file.tags[field] = value

    def clear(self):
        self.__file.tags.clear()

    def delete_field(self, field: str) -> None:
        super().delete_field(field)
        if field not in dict(self.__file.tags).keys():
            raise KeyError("Field not present in file")
        self.__file.tags.pop(field)

    def get_all_values(self) -> Dict[str, str]:
        values = {}
        for k, v in dict(self.__file.tags).items():
            if k in self.get_fields():
                values[k] = v
        return values

    def write(self) -> None:
        self.__file.save()
