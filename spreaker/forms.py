from django import forms


class AddPodcastForm(forms.Form):
    name = forms.CharField(
        label="Podcast Name",
        required=True,
        widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "Podcast Name"}),
    )
    podcast_url = forms.CharField(
        label="Spreaker URL",
        required=True,
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "Spreaker Url (i.e https://www.spreaker.com/show/la-voce-della-storia)",
            }
        ),
    )
