from django.shortcuts import render_to_response
from django.contrib.auth.decorators import login_required
from django.template import RequestContext
from starbowmodweb.streams.models import StreamInfo
from starbowmodweb.streams.getstreamstatus import update_stream_cache
from starbowmodweb.streams.forms import AddStreamForm

@login_required
def edit_stream(request):
    messages = []

    # previous stream_info data or None, if not available
    stream_info = StreamInfo.objects.filter(user=request.user).first()
    if request.method == 'POST':            # If the form has been submitted...
        form = AddStreamForm(request.POST, instance=stream_info)  # A form bound to the POST data
        if form.is_valid():
            if 'edit' in request.POST:
                # add/edit stream
                stream_info = form.save(commit=False)
                stream_info.user = request.user
                stream_info.save()
                messages.append('Your stream was added/edited succesfully.')
            elif 'delete' in request.POST:
                # delete stream
                stream_info.delete()
                stream_info = None
                messages.append('Your stream link was deleted.')
                form = AddStreamForm()
    else:
        form = AddStreamForm(instance=stream_info)   # An unbound form

    ctx = RequestContext(request, {'form': form,
                                   'messages': messages,
                                   'edit': stream_info is not None})
    return render_to_response('streams/register_stream.html', ctx)


def list_streams(request):
    update_stream_cache()
    online_streams = StreamInfo.objects.filter(online=True).order_by('-viewers')
    offline_streams = StreamInfo.objects.filter(online=False)
    return render_to_response('streams/list_streams.html', {'online_streams': online_streams,
                                                            'offline_streams': offline_streams})