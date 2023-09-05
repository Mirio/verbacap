from django import forms


class AddChannelForm(forms.Form):
    name = forms.CharField(
        label="Channel Name",
        required=True,
        widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "Channel Name (i.e Youtube)"}),
    )
    channel_url = forms.CharField(
        label="Channel URL",
        required=True,
        widget=forms.TextInput(
            attrs={"class": "form-control", "placeholder": "Channel url (i.e https://www.youtube.com/@Youtube)"}
        ),
    )
