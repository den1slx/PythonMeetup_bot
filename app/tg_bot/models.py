from django.db import models


class Particiant(models.Model):
    telegram_id = models.IntegerField(verbose_name='Telegram id')
    name = models.CharField(max_length=100, verbose_name='Имя')
    email = models.CharField(max_length=100, verbose_name='email')

    class Meta:
        verbose_name = 'Участник'
        verbose_name_plural = 'Участники'

    def __str__(self):
        return f'{self.name} - {self.email}'


class Event(models.Model):
    date = models.DateField(verbose_name='Дата проведения митапа')
    start = models.TimeField(verbose_name='Начало митапа')
    end = models.TimeField(verbose_name='Окончание митапа')

    class Meta:
        verbose_name = 'Митап'
        verbose_name_plural = 'Митапы'

    def __str__(self):
        return f'Митап {self.start} - {self.end}'


class Lecture(models.Model):
    event = models.ForeignKey(Event, on_delete=models.DO_NOTHING, verbose_name='Митап')
    speaker = models.ForeignKey(Particiant, on_delete=models.DO_NOTHING, verbose_name='Доклатчик')
    title = models.CharField(max_length=300, verbose_name='Тема доклада')
    start = models.TimeField(verbose_name='Время начала доклада')
    end = models.TimeField(verbose_name='Время окончания доклада')

    class Meta:
        verbose_name = 'Доклад'
        verbose_name_plural = 'Доклады'

    def __str__(self):
        return f'{self.title} - {self.speaker.name}'
