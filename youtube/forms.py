from django import forms


class AddChannelForm(forms.Form):
    name = forms.CharField(
        label="Playlist Name",
        required=True,
        widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "Channel Name (i.e Youtube)"}),
    )
    channel_url = forms.CharField(
        label="Playlist URL",
        required=True,
        widget=forms.TextInput(
            attrs={"class": "form-control", "placeholder": "Channel url (i.e https://www.youtube.com/@Youtube)"}
        ),
    )


class AddPlaylistForm(forms.Form):
    name = forms.CharField(
        label="Playlist Name",
        required=True,
        widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "Playlist Name (i.e Youtube - Foo)"}),
    )
    playlist_url = forms.CharField(
        label="Playlist URL",
        required=True,
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": ("Playlist url (i.e https://www.youtube.com/watch?v=...&list=PLbpi6ZahtOH7c...)"),
            }
        ),
    )
