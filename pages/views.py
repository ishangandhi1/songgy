# Create your views here.
from django.http import HttpResponseRedirect ,HttpResponse, Http404
from django.template import RequestContext
from django.shortcuts import render_to_response

def index(request):
	context = RequestContext(request)
	return render_to_response('userena/index.html', {}, context)