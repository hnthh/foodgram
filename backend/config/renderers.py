from rest_framework.renderers import JSONRenderer


class AppJSONRenderer(JSONRenderer):
    charset = 'utf-8'
