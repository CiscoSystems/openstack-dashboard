from django import forms
from django_open import adminclient

# returns a sorted list of flavor tuples formatted for the select field on the LaunchForm
def flavorlist():
    fl = adminclient.OpenManager().list_image_flavors()
    sel = [ (f.id, f.name) for f in fl]
    return sorted(sel)

class LaunchForm(forms.Form):
    image_id = forms.CharField(widget=forms.HiddenInput())
    name = forms.CharField(max_length=80, initial="Name of Server", label="Server Name")

    #make the dropdown populate when the form is loaded not when django is started
    def __init__(self, *args, **kwargs):
        super(LaunchForm, self).__init__(*args, **kwargs)
        self.fields['flavor'] = forms.ChoiceField(choices=flavorlist(), label="Flavor", help_text="Size of Image to launch")
