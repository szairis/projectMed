from django.db import models

class Specialty(models.Model):
    name = models.CharField(primary_key=True,max_length=100)
    training_length = models.IntegerField()
    salary = models.IntegerField()
    step1_score = models.IntegerField(null=True)
    number_publications = models.DecimalField(max_digits=3,decimal_places=1,null=True)
    aoa_percentage = models.DecimalField(max_digits=3,decimal_places=1,null=True)
    academic_percentage = models.DecimalField(max_digits=3,decimal_places=1,null=True)
    def __unicode__(self):
        return self.name
    
class MedCenter(models.Model):
    name = models.CharField(primary_key=True,max_length=100)
    state = models.CharField(max_length=2)
    rank_medschool = models.IntegerField(null=True)
    nih_funding = models.IntegerField()
    def __unicode__(self):
        return self.name

class Posting(models.Model):
    id = models.AutoField(primary_key=True)
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=False,blank=True,null=True)
    name = models.CharField(max_length=50)
    contact_email = models.EmailField()
    passkey = models.CharField(max_length=5)
    specialty = models.ForeignKey(Specialty)
    med_center = models.ForeignKey(MedCenter)
    needs_irb = models.BooleanField()
    needs_basic_sci = models.BooleanField()
    needs_lit_review = models.BooleanField()
    needs_patient_inter = models.BooleanField()
    needs_chart_mining = models.BooleanField()
    needs_statistics = models.BooleanField()
    title = models.CharField(max_length=200)
    description = models.TextField()
    is_active = models.BooleanField(default=True)
    is_alive = models.BooleanField(default=True)
    number_replies = models.IntegerField(default=0)
    
    def gen_url(self):
        cipher = 0xabcdef
        encrypted = str(hex(self.id ^ cipher))
        return encrypted[2:]

    def gen_passkey(self):
        import hashlib
        m = hashlib.md5()
        m.update(str(self.date_created))
        return m.hexdigest()[:5]

    def __unicode__(self):
        return self.title
        
class Reply(models.Model):
    id = models.AutoField(primary_key=True)
    posting = models.ForeignKey(Posting)
    med_center = models.ForeignKey(MedCenter)
    name = models.CharField(max_length=50)
    contact_email = models.EmailField()
    msg_body = models.TextField()

    def __unicode__(self):
        return "Student: %s" %(self.name)
