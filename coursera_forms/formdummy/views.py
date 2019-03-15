from django.shortcuts import render

from django.views import View
from .forms import DummyForm
from .schemas import REVIEW_SCHEMA, ReviewSchema
from jsonschema import validate
from jsonschema.exceptions import ValidationError
import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from marshmallow import ValidationError as MarshmallowError


class FormDummyView(View):
    def get(self, request):
        form = DummyForm()
        # from pdb import setf_trace; set_trace()
        return render(request, "form.html", {'form': form})

    def post(self, request):
        form = DummyForm(request.POST)
        if form.is_valid():
            context = form.cleaned_data
            return render(request, "form.html", context)
        else:
            return render(request, "error.html", {'error': form.errors})

@method_decorator(csrf_exempt, name='dispatch')
class SchemaView(View):

    def post(self, request):
        try:
            document = json.loads(request.body)
            validate(document, REVIEW_SCHEMA)
            return JsonResponse(document, status=201)
        except json.JSONDecodeError:
            return JsonResponse({'errors': 'Invalid JSON'}, status=400)
        except ValidationError as exc:
            return JsonResponse({'errors': exc.message}, status=400)

@method_decorator(csrf_exempt, name='dispatch')
class MarshView(View):

    def post(self, request):
        try:
            document = json.loads(request.body)
            schema =ReviewSchema(strict=True)
            data = schema.load(document)
            return JsonResponse(data.data, status=201)
        except json.JSONDecodeError:
            return JsonResponse({'errors': 'Invalid JSON'}, status=400)
        except MarshmallowError as exc:
            return JsonResponse({'errors': exc.messages}, status=400)
