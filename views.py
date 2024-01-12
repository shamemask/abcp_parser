from django.utils.decorators import method_decorator
from drf_yasg.utils import swagger_auto_schema
from rest_framework.views import APIView

from abcp_parser.abcp_parser import abcp_parser, url_to_parse


def abcp(request):
        # Cинхронная функция для парсинга abcp
        abcp_parser(url_to_parse)
        return 'Done'


