from rest_framework.response import Response
from rest_framework.decorators import api_view
from scrape import scrape

@api_view(['GET'])
def sample_api(request, crd_number):
    firm_info = scrape(crd_number)
    return Response(firm_info)