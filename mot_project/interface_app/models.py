from django.db import models
from django.utils import timezone
import datetime
from django.contrib.auth.models import User
from django.forms import ModelForm


class ParticipantProfile(models.Model):
    # Properties shared in both experimentations:
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    date = models.DateTimeField(default=timezone.now, verbose_name="Inscription Date")
    birth_date = models.DateField(default=datetime.date.today, blank=True, help_text='yyyy-mm-dd')
    study = models.CharField(max_length=10, default='unk')
    nb_sess_started = models.IntegerField(default=0)
    nb_sess_finished = models.IntegerField(default=0)
    nb_followups_finished = models.IntegerField(default=0)
    consent = models.BooleanField(default=False)
    general_profil = models.BooleanField(null=True, default=False)
    attention_profil = models.BooleanField(null=True, default=False)
    condition = models.CharField(max_length=50, null=True, default='None')

    # JOLD properties:
    wind = models.IntegerField(null=True)
    plat = models.IntegerField(null=True)
    dist = models.IntegerField(null=True)

    # ZPDES-exp extra infos:
    screen_params = models.FloatField(null=True)
    sexe = models.CharField(max_length=20, choices=(("Femme", "Femme"), ("Homme", "Homme"), ("Autre", "Autre")),
                            null=True)
    job = models.CharField(max_length=40, null=True)
    # Frequency of video games practice is a Response model
    video_game_start = models.IntegerField(null=True)
    # For vide_game_freq, vid_game_habit and driving_freq, custom widget would be used
    # ( a question object is passed to ModelForm and the widget is set up )
    video_game_freq = models.CharField(max_length=40, null=True) # range : "Never, sometimes, often, daily"
    video_game_habit = models.CharField(max_length=40, null=True) # range : "Action, Sport, FPS, RPG, MMO"
    driver = models.BooleanField(null=False, default=True, choices=((True, "Oui"), (False, "Non")))
    driving_start = models.IntegerField(null=True)
    driving_freq = models.CharField(max_length=40, null=True) # range : "Never, sometimes, once a week, daily"
    attention_training = models.BooleanField(null=True, default=True, choices=((True, "Oui"), (False, "Non")))
    online_training = models.BooleanField(null=True, default=True, choices=((True, "Oui"), (False, "Non")))

    class Meta:
        verbose_name = 'Participant'
        ordering = ['birth_date']


class Episode(models.Model):
    # Foreign key to user :
    participant = models.ForeignKey(User, on_delete=models.CASCADE)

    # Description of the task
    date = models.DateTimeField(default=datetime.date.today)
    secondary_task = models.CharField(max_length=20, default='none')
    episode_number = models.IntegerField(default=0)

    # Task parameters:
    n_distractors = models.IntegerField(default=0)
    n_targets = models.IntegerField(default=0)
    angle_max = models.IntegerField(default=0)
    angle_min = models.IntegerField(default=0)
    radius = models.IntegerField(default=0)
    speed_min = models.FloatField(default=0)
    speed_max = models.FloatField(default=0)
    RSI = models.FloatField(default=0)
    SRI_max = models.FloatField(default=0)
    presentation_time = models.FloatField(default=0)
    fixation_time = models.FloatField(default=0)
    tracking_time = models.FloatField(default=0)

    # User Score:
    nb_target_retrieved = models.IntegerField(default=0)
    nb_distract_retrieved = models.IntegerField(default=0)

    # To avoid creating session model but to be able to make joint queries:
    id_session = models.IntegerField(default=0)
    finished_session = models.BooleanField(default=False)


class SecondaryTask(models.Model):
    episode = models.ForeignKey(Episode, on_delete=models.CASCADE)
    type = models.CharField(max_length=20, default='detection')
    delta_orientation = models.FloatField(default=0)
    success = models.BooleanField(default=False)
    answer_duration = models.FloatField(default=0)


class JOLD_LL_trial(models.Model):
    date = models.DateTimeField(default=timezone.now)
    participant = models.ForeignKey(ParticipantProfile, on_delete=models.CASCADE)
    sess_number = models.IntegerField(default=0)
    trial = models.IntegerField(null=True)
    wind = models.DecimalField(decimal_places=2, max_digits=3)
    init_site = models.IntegerField(null=True)
    plat_site = models.IntegerField(null=True)
    init_dist = models.DecimalField(decimal_places=2, max_digits=5)
    end_dist = models.DecimalField(decimal_places=2, max_digits=5)
    time_trial = models.DecimalField(decimal_places=1, max_digits=8)
    time_sess = models.DecimalField(decimal_places=1, max_digits=8)
    fuel = models.IntegerField(null=True)
    presses = models.IntegerField(null=True)
    outcome = models.CharField(max_length=10)
    interruptions = models.IntegerField(null=True)
    forced = models.BooleanField(default=True)


# A model to store dynamic data to display on Home Page
class DynamicProps(models.Model):
    study = models.CharField(max_length=10, null=True)
    project = models.CharField(max_length=100, null=True)
    base_html = models.CharField(max_length=50, null=True)
    task_url = models.CharField(max_length=50, null=True)
    style = models.CharField(max_length=50, null=True)
    instructions = models.CharField(max_length=50, null=True)
    consent_text = models.CharField(max_length=50, null=True)
    nb_sess = models.IntegerField(default=5)
    tutorial = models.CharField(max_length=50, default='')


class QBank(models.Model):
    instrument = models.CharField(max_length=100, null=True)
    component = models.CharField(max_length=100, null=True)
    group = models.CharField(max_length=100, null=True)
    handle = models.CharField(max_length=10, null=True)
    order = models.IntegerField(null=True)
    prompt = models.CharField(max_length=300, null=True)
    reverse = models.BooleanField(null=True)
    min_val = models.IntegerField(null=1)
    max_val = models.IntegerField(null=1)
    step = models.IntegerField(null=1)
    annotations = models.CharField(max_length=200, null=True)
    widget = models.CharField(max_length=30, null=True)
    sessions = models.CharField(max_length=20, null=True)


class Responses(models.Model):
    participant = models.ForeignKey(ParticipantProfile, on_delete=models.CASCADE)
    question = models.ForeignKey(QBank, on_delete=models.PROTECT)
    answer = models.IntegerField(null=True)
    sess = models.IntegerField(null=True)
