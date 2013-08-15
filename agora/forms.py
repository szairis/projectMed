#this is a useless comment to be deleted asap
from django import forms
from agora.models import Posting, Reply, Specialty, MedCenter

class PostingForm(forms.ModelForm):
    class Meta:
        model = Posting
        fields = ('specialty','med_center','needs_irb','needs_basic_sci',\
                'needs_lit_review','needs_patient_inter','needs_chart_mining',\
                'needs_statistics','name','contact_email','title','description','is_active')

class ReplyForm(forms.ModelForm):
    class Meta:
        model = Reply
        fields = ('name','contact_email','med_center','msg_body')

class ViewForm(forms.Form):
    inc_inactive = forms.BooleanField(initial=True,required=False)
    med_center = forms.ModelChoiceField(required=False, \
                                        queryset=MedCenter.objects.all(), \
                                        empty_label=u"")
    specialty = \
             forms.ModelChoiceField(required=False, \
                                    queryset=Specialty.objects.all(), \
                                    empty_label=u"")

class OwnerForm(forms.Form):
    email = forms.EmailField()
    passkey = forms.CharField(widget=forms.PasswordInput())

