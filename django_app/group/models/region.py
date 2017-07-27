from django.db import models


# Region
# 	pk
# 	si			CharField					max_length=20
# 	gu			CharField					max_length=20
# 	dong		CharField					max_length=20
# 	lat			FloatField
# 	lng			FloatField

class Region(models.Model):
    si = models.CharField(max_length=24)
    gu = models.CharField(max_length=24)
    dong = models.CharField(max_length=24)
    lat = models.FloatField()
    lng = models.FloatField()

    def __str__(self):
        return '{} {} {}'.format(self.si, self.gu, self.dong)