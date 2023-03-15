from django.core.validators import RegexValidator
from django.db import models

from common_utils import path_and_rename
from hashtag.models import Hashtag
from membership.models import User


Energy = (('E', 'Extroverted(E)'), ('I', 'Introverted(I)'), ('x', 'Nothing'))  # 외향, 내향
Information = (('N', 'Intuitive(N)'), ('S', 'Observant(S)'), ('x', 'Nothing'))  # 직관, 감각
Decision = (('T', 'Thinking(T)'), ('F', 'Feeling(F)'), ('x', 'Nothing'))  # 사고, 감정
Lifestyle = (('J', 'Judging(J)'), ('P', 'Prospecting(P)'), ('x', 'Nothing'))  # 판단, 인식


QUESTION_CATEGORY = (
    (0, 'Energy'),  # 외내향
    (1, 'Information'),  # 이상현실
    (2, 'Decision'),  # 관계합리
    (3, 'Lifestyle')  # 계획적응
)

QUESTION_CATEGORY = (
    ('energy', 'Energy'),  # 외내향 IE
    ('information', 'Information'),  # 이상현실 SN
    ('decision', 'Decision'),  # 관계합리 TF
    ('lifestyle', 'Lifestyle')  # 계획적응 PJ
)


class MBTIQuestion(models.Model):
    index = models.PositiveSmallIntegerField(null=False, blank=False)
    # category = models.PositiveSmallIntegerField(choices=QUESTION_CATEGORY, null=False, blank=False)
    category = models.CharField(max_length=20, choices=QUESTION_CATEGORY, null=False, blank=False)
    text = models.TextField()
    select0_score = models.SmallIntegerField(null=False, blank=False, verbose_name='Not at all')
    select1_score = models.SmallIntegerField(null=False, blank=False, verbose_name='No')
    select2_score = models.SmallIntegerField(null=False, blank=False, verbose_name='Yes')
    select3_score = models.SmallIntegerField(null=False, blank=False, verbose_name='Absolutely')

    class Meta:
        db_table = 'mbti_question'
        ordering = ('index', )

    def __str__(self):
        return f"MBTIQuestion({self.index})"


class MBTITestThreshold(models.Model):
    energy = models.PositiveSmallIntegerField(null=False, blank=False)
    information = models.PositiveSmallIntegerField(null=False, blank=False)
    decision = models.PositiveSmallIntegerField(null=False, blank=False)
    lifestyle = models.PositiveSmallIntegerField(null=False, blank=False)

    class Meta:
        db_table = 'mbti_question_threshold'

    def __str__(self):
        return f"MBTI Test score Threshold(include)"


MBTI_CLASS_CHOICES = (
    ('ESFJ', 'ESFJ'),
    ('ESTJ', 'ESTJ'),
    ('ESFP', 'ESFP'),
    ('ESTP', 'ESTP'),

    ('ISFJ', 'ISFJ'),
    ('ISTJ', 'ISTJ'),
    ('ISFP', 'ISFP'),
    ('ISTP', 'ISTP'),

    ('ENFJ', 'ENFJ'),
    ('ENTJ', 'ENTJ'),
    ('ENFP', 'ENFP'),
    ('ENTP', 'ENTP'),

    ('INFJ', 'INFJ'),
    ('INTJ', 'INTJ'),
    ('INFP', 'INFP'),
    ('INTP', 'INTP'),

    ('xxxx', 'xxxx'),
)


class MBTIClass(models.Model):
    mbti = models.CharField(max_length=4, choices=MBTI_CLASS_CHOICES, validators=[RegexValidator(regex=r"[IEx][SNx][TFx][PJx]", message='Not match MBTI Characters')])
    title = models.CharField(max_length=50, null=False, blank=True)
    summary = models.TextField()
    content = models.TextField()

    class Meta:
        db_table = 'mbti_class'

    def __str__(self):
        return f"[{self.mbti}]{self.title}"


class MBTIClassImage(models.Model):
    mbti_class_id = models.ForeignKey(MBTIClass, on_delete=models.SET_NULL, null=True, db_column='mbti_class_id', related_name='mbti_class_image_set')
    image = models.ImageField(upload_to=path_and_rename)
    name = models.CharField(max_length=50, null=False, blank=False)
    alt = models.CharField(max_length=255, null=False, blank=False)

    class Meta:
        db_table = 'mbti_class_image'

    def __str__(self):
        return f"{self.name}"


class MBTIClassHashtagAssoc(models.Model):
    mbti_class_id = models.ForeignKey(MBTIClass, on_delete=models.SET_NULL, null=True, db_column='mbti_class_id', related_name='hashtag_assoc_set')
    hashtag_id = models.ForeignKey(Hashtag, on_delete=models.SET_NULL, null=True, db_column='hashtag_id', related_name='mbti_class_assoc_set')

    class Meta:
        db_table = 'mbti_class_hashtag'
        verbose_name = 'MBTI class hashtag'

    def __str__(self):
        return f"{self.mbti_class_id}-{self.hashtag_id}"
