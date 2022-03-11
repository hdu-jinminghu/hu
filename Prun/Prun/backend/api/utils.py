
import re
import time
from pathlib import Path
from django.http import HttpResponseNotAllowed, HttpResponseBadRequest, \
    JsonResponse, HttpResponse
import json



def validate_get_request(request, func, accept_params=None, args=None):
    """Check if method of request is GET and request params is legal

    Args:
         request: request data given by django
         func: function type, get request and return HTTP response
         accept_params: list type, acceptable parameter list
         args: value of parameters
    Returns:
         HTTP response
    """
    if accept_params is None:
        accept_params = []
    if args is None:
        args = []
    if request.method != 'GET':
        return HttpResponseNotAllowed(['GET'])
    elif set(accept_params).issubset(set(request.GET)):
        return func(request, *args)
    else:
        return HttpResponseBadRequest('parameter lost!')


def validate_post_request(request, func, accept_params=None, args=None):
    """Check if method of request is POST and request params is legal

    Args:
         request: request data given by django
         func: function type, get request and return HTTP response
         accept_params: list type, acceptable parameter list
         args: value of parameters
    Returns:
         HTTP response
    """
    if accept_params is None:
        accept_params = []
    if args is None:
        args = []
    if request.method != 'POST':
        return HttpResponseNotAllowed(['POST'])
    elif set(accept_params).issubset(set(request.POST)):
        return func(request, *args)
    else:
        return HttpResponseBadRequest('parameter lost!')
    
# response数据结构
def response_wrapper(fn):
    def inner(*args, **kwargs):
        # try:
        res = fn(*args, **kwargs)
        if not isinstance(res, HttpResponse):
            return JsonResponse({
                'code': 200,
                'msg': 'ok',
                'data': res
            })
        return res
        # except Exception as e:
            # return JsonResponse({
            #     'code': 500,
            #     'msg': str(e),
            #     'data': ""
            # })
            

    return inner