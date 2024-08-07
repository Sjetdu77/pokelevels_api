from django.db import models

# Create your models here.
class Game(models.Model):
    name = models.CharField(max_length=200)
    generation = models.IntegerField()
    color = models.CharField(max_length=7)

    def __str__(self) -> str:
        if (self.name.startswith("Légendes")):
            return f"Légendes Pokémon : {self.name[11:]}"
        else:
            return f"Pokémon {self.name}"

class Specie(models.Model):
    id = models.CharField(primary_key=True, max_length=7)
    name = models.CharField(max_length=200)
    generation = models.IntegerField()
    sprite = models.CharField(max_length=200)
    xp = models.IntegerField(null=True)
    xp1_4 = models.IntegerField(null=True)

    def __str__(self) -> str:
        return self.name

class Region(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self) -> str:
        return self.name

class GameRegion(models.Model):
    game = models.ForeignKey(Game, on_delete=models.CASCADE, related_name='associated_regions')
    region = models.ForeignKey(Region, on_delete=models.CASCADE, related_name='associated_games')

    def __str__(self) -> str:
        return f"{ self.region } ({ self.game })"

class Route(models.Model):
    name = models.CharField(max_length=200)
    access = models.IntegerField(default=0)
    game_region = models.ForeignKey(GameRegion, on_delete=models.CASCADE, related_name='routes')

    def __str__(self) -> str:
        return f"{self.name} -> {self.game_region.game}"

class Wild(models.Model):
    route = models.ForeignKey(Route, on_delete=models.CASCADE, related_name='wilds')
    specie = models.ForeignKey(Specie, on_delete=models.CASCADE, related_name='wilds')
    probability = models.IntegerField()
    lvl = models.IntegerField()
    mode = models.CharField(max_length=3, default='gs',
                            choices=[
                                ('gs', 'Grass'),
                                ('sf', 'Surf'),
                                ('or', 'Old Rod'),
                                ('gr', 'Good Rod'),
                                ('sr', 'Super Rod')
                            ]
    )

    time = models.CharField(max_length=1, default='a',
                            choices=[
                                ('a', 'All'),
                                ('m', 'Morning'),
                                ('d', 'Day'),
                                ('n', 'Night')
                            ]
    )

    def __str__(self) -> str:
        return f"{self.id} -> {self.specie} lvl {self.lvl} on {self.mode} : {self.route} ({self.probability} %)"

class Access(models.Model):
    game = models.ForeignKey(Game, on_delete=models.CASCADE, related_name='accesses')
    number = models.IntegerField()
    name = models.CharField(max_length=200)

    def __str__(self):
        return f'{self.number} : {self.name} ({self.game})'
    