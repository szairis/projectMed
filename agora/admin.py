from agora.models import Posting, Reply
from django.contrib import admin

class PostingAdmin(admin.ModelAdmin):
    fieldsets = [
        ('Associations', {'fields':['specialty','med_center']}),
        ('Stages', {'fields':['needs_irb','needs_basic_sci','needs_lit_review','needs_patient_inter','needs_chart_mining','needs_statistics']}),
        ('Listing',{'fields':['name','contact_email','title','description']}),
        (None, {'fields':['is_active','is_alive']}),
        ]
    list_display = ('title','is_active','date_created','number_replies','contact_email','passkey')
    list_filter = ['date_created','is_active']
    
admin.site.register(Posting, PostingAdmin)
admin.site.register(Reply)
