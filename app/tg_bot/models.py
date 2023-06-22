from django.db import models

role_choices = [
    (1, 'admin'),
    (2, 'speaker'),
    (3, 'user')
]


class ParticiantQuerySet(models.QuerySet):
    def get_ids(self):
        ids = [p.telegram_id for p in self.all()]
        return ids


class Particiant(models.Model):
    telegram_id = models.IntegerField(unique=True, verbose_name='Telegram id')
    name = models.CharField(max_length=100, verbose_name='Имя')
    email = models.CharField(max_length=100, verbose_name='email')
    phone = models.CharField(max_length=20, verbose_name='Телефон', blank=True, default='')
    role = models.IntegerField(verbose_name='Роль', choices=role_choices, default=3)

    objects = ParticiantQuerySet.as_manager()
    class Meta:
        verbose_name = 'Участник'
        verbose_name_plural = 'Участники'

    def __str__(self):
        return f'{self.name} - {self.email}'


class Event(models.Model):
    date = models.DateField(verbose_name='Дата проведения митапа')
    start = models.TimeField(verbose_name='Начало митапа')
    end = models.TimeField(verbose_name='Окончание митапа')
    active_or_next_lecture = models.ForeignKey('Lecture', on_delete=models.DO_NOTHING, verbose_name='Лекция сейчас',
                                       related_name='events', blank=True, null=True, default=None)

    class Meta:
        verbose_name = 'Митап'
        verbose_name_plural = 'Митапы'

    def __str__(self):
        return f'Митап {self.date}'


class Lecture(models.Model):
    event = models.ForeignKey(Event, on_delete=models.DO_NOTHING, verbose_name='Митап')
    speaker = models.ForeignKey(Particiant, on_delete=models.DO_NOTHING, verbose_name='Докладчик')
    title = models.CharField(max_length=300, verbose_name='Тема доклада')
    start = models.TimeField(verbose_name='Время начала доклада')
    end = models.TimeField(verbose_name='Время окончания доклада')

    class Meta:
        verbose_name = 'Доклад'
        verbose_name_plural = 'Доклады'

    def __str__(self):
        return f'{self.title} - {self.speaker.name}'
