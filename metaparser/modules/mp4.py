from typing import Any, Dict, List

import mutagen
import mutagen.easymp4

from .base import BaseParser

FIELD_TITLE = "title"
FIELD_ALBUM = "album"
FIELD_ARTIST = "artist"
FIELD_ALBUMARTIST = "albumartist"
FIELD_DATE = "date"
FIELD_COMMENT = "comment"
FIELD_DESCRIPTION = "description"
FIELD_GROUPING = "grouping"
FIELD_GENRE = "genre"
FIELD_COPYRIGHT = "copyright"
FIELD_ALBUMSORT = "albumsort"
FIELD_ALBUMARTISTSORT = "albumartistsort"
FIELD_ARTISTSORT = "artistsort"
FIELD_TITLESORT = "titlesort"
FIELD_COMPOSERSORT = "composersort"
FIELD_MUSICBRAINZ_ARTISTID = "musicbrainz_artistid"
FIELD_MUSICBRAINZ_TRACKID = "musicbrainz_trackid"
FIELD_MUSICBRAINZ_ALBUMID = "musicbrainz_albumid"
FIELD_MUSICBRAINZ_ALBUMARTISTID = "musicbrainz_albumartistid"
FIELD_MUSICIP_PUID = "musicip_puid"
FIELD_MUSICBRAINZ_ALBUMSTATUS = "musicbrainz_albumstatus"
FIELD_MUSICBRAINZ_ALBUMTYPE = "musicbrainz_albumtype"
FIELD_RELEASECOUNTRY = "releasecountry"
FIELD_BPM = "bpm"
FIELD_TRACKNUMBER = "tracknumber"
FIELD_DISCNUMBER = "discnumber"

class Mp4Parser(BaseParser):
    @staticmethod
    def supported_mimes() -> List[str]:
        return ["video/mp4"]

    def __init__(self) -> None:
        super().__init__()
        self.__tag = None

    def parse(self, filename: str) -> None:
        file = mutagen.File(filename, easy=True)
        self.__tag = file.tags.items()

    def get_fields(self) -> List[str]:
        return [
            FIELD_TITLE,
            FIELD_ALBUM,
            FIELD_ARTIST,
            FIELD_ALBUMARTIST,
            FIELD_DATE,
            FIELD_COMMENT,
            FIELD_DESCRIPTION,
            FIELD_GROUPING,
            FIELD_GENRE,
            FIELD_COPYRIGHT,
            FIELD_ALBUMSORT,
            FIELD_ALBUMARTISTSORT,
            FIELD_ARTISTSORT,
            FIELD_TITLESORT,
            FIELD_COMPOSERSORT,
            FIELD_MUSICBRAINZ_ARTISTID,
            FIELD_MUSICBRAINZ_TRACKID,
            FIELD_MUSICBRAINZ_ALBUMID,
            FIELD_MUSICBRAINZ_ALBUMARTISTID,
            FIELD_MUSICIP_PUID,
            FIELD_MUSICBRAINZ_ALBUMSTATUS,
            FIELD_MUSICBRAINZ_ALBUMTYPE,
            FIELD_RELEASECOUNTRY,
            FIELD_BPM,
            FIELD_TRACKNUMBER,
            FIELD_DISCNUMBER,
        ]

    def set_field(self, field: str, value: Any) -> None:
        if self.__tag is None:
            raise TypeError("Tag is null, parse the file first")
        if field not in self.get_fields():
            raise KeyError("Field not present in parser")
        setattr(self.__tag, field, value)
        # other way of saving

    def clear(self):
        self.__tag.clear()

    def delete_field(self, field: str) -> None:
        self.set_field(field, None)

    def get_all_values(self) -> Dict[str, str]:
        if self.__tag is None:
            raise TypeError("Tag is null, parse the file first")
        values = {}
        for field in self.get_fields():
            if field in self.__tag:
                attr = getattr(self.__tag, field, None)
                if attr is not None and (isinstance(attr, tuple) and any(attr)):
                    values[field] = attr
        return values

    def write(self) -> None:
        self.__tag.save()  # type: ignore
