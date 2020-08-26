from django.http import QueryDict
import json
from rest_framework import parsers
'''
this is from 
https://stackoverflow.com/questions/20473572/django-rest-framework-file-upload/62247880#62247880
'''


class MultipartJsonParser(parsers.MultiPartParser):

    def parse(self, stream, media_type=None, parser_context=None):
        result = super().parse(
            stream,
            media_type=media_type,
            parser_context=parser_context
        )
        data = {}

        # for case 2
        # find the data field and parse it
        data = json.loads(result.data["data"])

        qdict = QueryDict('', mutable=True)
        qdict.update(data)
        return parsers.DataAndFiles(qdict, result.files)


'''
        # for case1 with nested serializers
        # parse each field with json
        for key, value in result.data.items():
            if type(value) != str:
                data[key] = value
                continue
            if '{' in value or "[" in value:
                try:
                    data[key] = json.loads(value)
                except ValueError:
                    data[key] = value
            else:
                data[key] = value
'''
