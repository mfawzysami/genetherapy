"""
This python package contains some basic functions that will be used across the screening web applications

"""
from django.utils.translation import get_language
from django.http.response import HttpResponse, Http404
from json import dumps
from django.conf import settings
import os

ARABIC_LANG = "ar"
ENGLISH_LANG = "en"
PAGINATION_PER_PAGE = 20

OSSEC_CONTENT_TYPE = "application/json"
OSSEC_SUCCESS_STATUS_CODE = 200
OSSEC_MAX_LIMIT_SIZE = 100


def get_base_context():
    context = {}
    try:
        language = get_language()
        direction = "ltr"
        if language == ARABIC_LANG:
            direction = "rtl"
        context['direction'] = direction
        context['language'] = language
        context['base_url'] = settings.BASE_COMMON_URL
        return context

    except Exception as e:
        return context


def make_json_response_for_js(status=False, data=None):
    if not status:
        return HttpResponse(200, content_type="application/json", content=dumps({
            'status': False,
            'data': data
        }))
    return HttpResponse(status=200, content_type="application/json", content=dumps({
        'status': status,
        'data': data
    }))


def make_raw_json_response(status=False, data={}):
    payload = {
        'status': status
    }
    payload.update(data)
    return HttpResponse(status=200, content_type="application/json", content=dumps(payload))



def make_raw_response(status=200,data=""):
    return HttpResponse(status=status,content=data)



def make_file_manager_response(status=False, data={}):

    if status:
        payload = {
            "data": data
        }
        return HttpResponse(status=200, content_type="application/json", content=dumps(payload))
    else:
        return HttpResponse(status=500, content_type="application/json", content=dumps(data))


def make_json_response(status=False, message=None):
    if not status:
        return HttpResponse(status=200, content_type="application/json", content=dumps({
            'status': False,
            'message': message
        }))
    return HttpResponse(status=200, content_type="application/json", content=dumps({
        'status': status,
        'message': message
    }))


def download_file(request, path,content_type="text/plain"):
    if os.path.exists(path):
        with open(path, 'r') as fh:
            response = HttpResponse(fh.read(), content_type=content_type)
            response['Content-Disposition'] = 'inline; filename=' + os.path.basename(path)
            response['Content-Transfer-Encoding'] = 'binary'

            return response
    raise Http404


def get_hash(data):
    import hashlib
    md5 = hashlib.md5()
    md5.update(data)
    return md5.hexdigest()