from django import forms
from starbowmodweb.streams.models import StreamInfo, StreamingPlatform
from starbowmodweb.streams.getstreamstatus import twitch_channel_exists


class AddStreamForm(forms.ModelForm):
    channel_name = forms.RegexField(regex=r'^[a-zA-Z0-9]+[a-zA-Z0-9_]*$',
                                    min_length=4, max_length=25,
                                    required=True,
                                    label='Channel')
    streaming_platform = forms.ModelChoiceField(queryset=StreamingPlatform.objects.all(),
                                                required=True,
                                                empty_label=None,
                                                label='Platform')

    class Meta:
        model = StreamInfo
        fields = ['channel_name', 'streaming_platform', 'description']

    def clean(self):
        cleaned_data = super(AddStreamForm, self).clean()

        # For Twitch streams, check if channel name exists
        platform = cleaned_data.get('streaming_platform')
        channel_name = cleaned_data.get('channel_name')
        twitch = StreamingPlatform.objects.filter(name='Twitch').first()
        if twitch and platform and channel_name:
            if twitch == platform and not twitch_channel_exists(channel_name):
                err_msg = 'The channel name does not exist on Twitch!'
                self._errors['channel_name'] = self.error_class([err_msg])
                del cleaned_data['channel_name']

        return cleaned_data