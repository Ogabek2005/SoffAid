from django.db import models
from django.core.validators import RegexValidator , MaxValueValidator




phone_validator = RegexValidator(regex=r"^\+998\d{9}$", message='phone number is wrong',
                                 code="invalid_phone")


class BaseModel(models.Model):
    created_ad = models.DateTimeField(auto_now_add=True)
    updated_ad = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

class Banner(BaseModel):
    image = models.ImageField(upload_to='banner_image/')
    title = models.CharField(max_length=255)
    description = models.TextField()

    def __str__(self):
        return f"{self.title}-{self.description}"
    
class Expert(BaseModel):
        image = models.ImageField(upload_to='expert_image/')
        first_name = models.CharField(max_length=255)
        last_name = models.CharField(max_length=255)
        telephone_number = models.CharField(max_length=255,
                                            validators=[phone_validator],
                                            unique=True,
                                            verbose_name='Phone number',
                                            )
        degree = models.FileField(upload_to='expert_deegre/')
        description = models.TextField()
        free_time = models.CharField(max_length=255)
        cost = models.DecimalField(max_digits=20,
                                   decimal_places=2,
                                   verbose_name="Cost",
                                   )
        category = models.ForeignKey('Category',
                                     on_delete=models.CASCADE,
                                     related_name='expert_category',
                                     verbose_name='Category')
        def __str__(self):
            return f"{self.id}-{self.first_name}-{self.last_name}"
        
class Category(BaseModel):
     image = models.ImageField(upload_to='category_image/')
     name = models.CharField(max_length=255,
                             verbose_name='Name')
     
     def __str__(self):
         return f"{self.id}-{self.name}"
     
class Appeal(BaseModel):
    expert = models.ForeignKey(Expert,
                                related_name='expert_appeal',
                                on_delete=models.CASCADE,
                                verbose_name='Appeal',
                                )
    full_name = models.CharField(max_length=255,
                                  verbose_name="Full name",
                                  )
    telephone_number = models.CharField(max_length=255,
                                         validators=[phone_validator],
                                         verbose_name='Phone number',
                                         )
    description = models.TextField()


    def __str__(self):
        return f"{self.id}-{self.full_name}-{self.telephone_number}"
    
class Comment(BaseModel):
    expert = models.ForeignKey(Expert,
                                on_delete=models.CASCADE,
                                related_name='expert_comment',
                                verbose_name='Comment',
                                )
    degree = models.PositiveIntegerField(validators=[MaxValueValidator(5)])
    description = models.TextField()

    def __str__(self) -> str:
        return f"{self.id}-{self.degree}-{self.description}"
    
class Meeting(BaseModel):
    title = models.CharField(max_length=255)
    zoom_meeting_id = models.CharField(max_length=255)
    start_time = models.DateTimeField()
    duration = models.IntegerField()
    organizer = models.ForeignKey('User', on_delete=models.CASCADE)

    def __str__(self) -> str:
        return f"{self.id}-{self.title}"
        