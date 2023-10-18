from django.db import models
from django.contrib.auth import get_user_model
from django.utils.text import slugify

User = get_user_model()


class Business(models.Model):
    id = models.AutoField(primary_key=True, unique=True, editable=False)
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, unique=True,
                            editable=False, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    location = models.CharField(max_length=150)
    founded_year = models.PositiveIntegerField(null=True, blank=True)
    industry = models.CharField(max_length=50, null=True, blank=True)
    website = models.URLField()
    email = models.EmailField()
    logo = models.ImageField(upload_to='logos/', blank=True, null=True)
    social_media_facebook = models.URLField(blank=True, null=True)
    social_media_twitter = models.URLField(blank=True, null=True)
    social_media_linkedin = models.URLField(blank=True, null=True)
    revenue = models.DecimalField(
        max_digits=10, decimal_places=2, blank=True, null=True)
    employee_count = models.PositiveIntegerField(blank=True, null=True)
    address = models.CharField(max_length=200, blank=True, null=True)

    # branch

    parent_business = models.ForeignKey(
        'self', on_delete=models.CASCADE, null=True, blank=True, related_name='branches')
    has_branch = models.BooleanField(default=False)
    branch_num = models.PositiveIntegerField(default=0)

    ceo_name = models.CharField(max_length=100, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.id:
            last_business = Business.objects.last()
            if last_business:
                self.id = last_business.id + 1
            else:
                self.id = 1000

        # If it's a branch, include branch name in the slug
        if self.parent_business:
            self.slug = slugify(f"{self.parent_business.name}-{self.name}")
        else:
            self.slug = slugify(self.name)

        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


# class Type(models.Model):
#     business = models.ForeignKey(Business, on_delete=models.CASCADE, null=True, blank=True)
#     name = models.CharField(max_length=50)

#     def __str__(self):
#         return self.name


# class UniversalEntities(models.Model):
#     xbusiness = models.ForeignKey(Business, on_delete=models.CASCADE)
#     xtype = models.ForeignKey(Type, on_delete=models.CASCADE)
#     xname = models.CharField(max_length=100)
#     xdescription = models.TextField(blank=True)
#     xcode = models.CharField(max_length=20, blank=True)
#     xlatitude = models.DecimalField(max_digits=10, decimal_places=6, null=True, blank=True)
#     xlongitude = models.DecimalField(max_digits=10, decimal_places=6, null=True, blank=True)
#     created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
#     status = models.BooleanField(default=True)
#     xcreated_at = models.DateTimeField(auto_now_add=True)
#     xupdated_at = models.DateTimeField(auto_now=True)                                      

#     def __str__(self):
#         return self.xname
    
#     class Meta:
#         unique_together = ('xtype', 'xname')
        
        
        