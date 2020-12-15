from django.db import models

# Create your models here.
class Search(models.Model):
    """[summary]
        Search model
        [attributes]:
            main_search: String
            attributes: Dictionary
    """
    main_search = ""
    attributes ={}
    def __str__(self):
        return self.main_search
