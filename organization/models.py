from django.db import models

# Create your models here.

class org(models.Model):
	org_name = models.CharField(max_length=64, unique=True)
	org_bio = models.CharField(max_length=512, blank=True)

class review(models.Model):

	defineRating = (
	    ('1', '1 star'),
	    ('2', '2 star'),
	    ('3', '3 star'),
	    ('4', '4 star'),
	    ('5', '5 star'),

	)
	organization = models.ForeignKey(org, unique=False)
	rating = models.CharField(max_length=2,
                                      choices=defineRating,
                                      default='3')
	review = models.CharField(max_length=512, blank=True)
##Have it store an average somewhere as well, for easier figuring out of the total.

class cluster(models.Model):
	defineMaterial = (
            ('abs', 'abs'),
            ('pla', 'pla'),

        )

	organization = models.ForeignKey(org, unique=False)
	material = models.CharField(max_length=32,
                                      choices=defineMaterial,
                                      default='abs')
	colour = models.CharField(max_length=32)
	location = models.CharField(max_length=256, blank=False)


