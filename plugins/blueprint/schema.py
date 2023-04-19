from pyrogram import types

from .struct import content_struct, search_struct


class Schema:
    def __init__(self, Client):
        self.Client = Client

    def search_message(self, response, language):
        message = ''
        for count, item in enumerate(response.get('items', {})):
            if count >= 20:
                break

            message = search_struct.format(
                count=count+1,
                title=item.get('name')[:100],
                size=item.get('size'),
                seeders=item.get('seeders'),
                leechers=item.get('leechers'),
                torrent_id=item.get('torrentId'),
                link_str=self.Client.LG.STR('size', language),
            ) + message

        return message or self.Client.LG.STR('noResults', language)

    def content_message(self, data, language, restricted_mode, bookmarked=False):
        # Check if the data is valid
        if not data.get('name') and not data.get('title'):
            return self.Client.LG.STR('errorFetchingLink', language), None

        # Check if the content is explicit
        elif restricted_mode and self.Client.EXPLICIT.predict(
            data.get('name') or data.get('title'),
        ):
            return self.Client.LG.STR('cantView', language), None

        message = content_struct.format(
            title=data.get('name') or data.get('title'),
            size=data.get('size'),
            seeders=data.get('seeders'),
            leechers=data.get('leechers'),
            uploaded_on=data.get('uploadDate') or data.get('uploaded_on'),
            magnet=data.get('magnetLink') or data.get('magnet'),
            size_str=self.Client.LG.STR('size', language),
            seeders_str=self.Client.LG.STR('seeders', language),
            leechers_str=self.Client.LG.STR('leechers', language),
            uploaded_on_str=self.Client.LG.STR('uploadedOn', language),
            magnet_link_str=self.Client.LG.STR('link', language),
        )

        markup = self.Client.KB.torrent_info(
            language,
            data.get('infoHash'),
            bookmarked=bookmarked,
        )

        return message, markup
