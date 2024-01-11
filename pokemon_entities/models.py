from django.db import models  # noqa F401


class Pokemon(models.Model):
    """Make Pokemon ID card"""
    title = models.CharField(max_length=200)
    title_en = models.CharField(max_length=200, verbose_name="Имя покемона на аглийском", blank=True)
    title_jp = models.CharField(max_length=200, verbose_name="Имя покемона на японском", blank=True)
    description = models.TextField("Описание покемона", blank=True)
    image = models.ImageField(upload_to='media', null=True, blank=True)
    previous_evolution = models.ForeignKey("self", verbose_name="Из кого эволюционировал", on_delete=models.SET_NULL,
                                           null=True, blank=True,
                                           related_name="next_evolutions")

    class Meta:
        verbose_name = 'Покемон'
        verbose_name_plural = 'Покемоны'

    def __str__(self):
        return self.title


class PokemonEntity(models.Model):
    """Make Pokemon Entity"""
    pokemon = models.ForeignKey(Pokemon, on_delete=models.CASCADE, verbose_name="Покемон", related_name='entities')
    lat = models.FloatField(verbose_name="Широта")
    lon = models.FloatField(verbose_name="Долгота")
    appeared_at = models.DateTimeField(verbose_name="Время появления", null=True, blank=True)
    disappeared_at = models.DateTimeField(verbose_name="Время исчезновения", null=True, blank=True)
    level = models.IntegerField(verbose_name="Уровень покемона", null=True, blank=True)
    health = models.IntegerField(verbose_name="Количество Здоровья", null=True, blank=True)
    strength = models.IntegerField(verbose_name="Сила покемона", null=True, blank=True)
    defence = models.IntegerField(verbose_name="Уровень защиты", null=True, blank=True)
    stamina = models.IntegerField(verbose_name="Очки выносливости покемона", null=True, blank=True)

    class Meta:
        verbose_name = 'Сущность покемона'
        verbose_name_plural = 'Сущности покемонов'

    def __str__(self):
        return self.pokemon.title