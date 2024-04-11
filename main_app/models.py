from django.db import models
from django.urls import reverse
from datetime import date

# Create your models here.

MEALS = (
    ('B', 'Breakfast'),
    ('L', 'Lunch'),
    ('D', 'Dinner')
)

class Seed(models.Model):
  name = models.CharField(max_length=50)
  color = models.CharField('image url')

  def __str__(self):
    return self.name

  def get_absolute_url(self):
    return reverse('seeds_detail', kwargs={'pk': self.id})


class Finch(models.Model):
    name = models.CharField(max_length = 50)
    size = models.TextField(max_length = 50)
    description = models.TextField(max_length = 200)
    image_url = models.URLField(blank=True)
    seeds = models.ManyToManyField(Seed)

    
    def __str__(self):
        return f'{self.name} ({self.id})'

    def get_absolute_url(self):
        return reverse('detail', kwargs={'finch_id': self.id})
    
    def fed_for_today(self):
       return self.feeding_set.filter(date=date.today()).count() >= len(MEALS) 
    

    
class Feeding(models.Model):
  date = models.DateField('feeding date')
  meal = models.CharField(
    max_length=1,
    choices=MEALS,
    default=MEALS[0][0]
  )
  # Create a cat_id FK
  finch = models.ForeignKey(Finch, on_delete=models.CASCADE)

  def __str__(self):
    return f"{self.get_meal_display()} on {self.date}"
  class Meta:
     ordering = ['-date']