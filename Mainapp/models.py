from django.db import models

#借りられる部屋の分類分け（例：高校校舎）
class Area(models.Model):
    name = models.CharField(max_length=20)
    IsAvailable = models.BooleanField(default=True,help_text="もしfalseなら選択/表示ができない")
    helptext = models.CharField(max_length=50,blank=True,help_text="補足が必要な場合")
    def __str__(self):
        return self.name

#借りられる部屋の一覧
class Room(models.Model):
    name = models.CharField(max_length=20)
    IsNeedCheck = models.BooleanField(help_text="部屋の管理者の先生に尋ねる必要があるか")
    IsAvailable = models.BooleanField(default=True,help_text="もしfalseなら選択/表示ができない")
    helptext = models.CharField(max_length=50,blank=True,help_text="補足が必要な場合")
    area=models.ForeignKey(Area,limit_choices_to={"IsAvailable":True},on_delete=models.PROTECT)
    def __str__(self):
        return self.name

#その日のイベント
class Event(models.Model):
    date=models.DateField()
    title=models.CharField(max_length=20)
    def __str__(self):
        return self.title

#部屋の予約
class Schedule(models.Model):
    date = models.DateField()
    time = models.CharField(max_length=20,help_text="文字列。'昼休み'や'放課後'等")
    place = models.ForeignKey(Room,limit_choices_to={"IsAvailable":True},on_delete=models.PROTECT)
    organization = models.CharField(max_length=20)
    StudentNum = models.CharField(max_length=4)
    teacherSeal = models.CharField(max_length=20,blank=True,help_text="許可をした先生が名前を入力")
    affairsSeal = models.CharField(max_length=20,blank=True,help_text="許可をした教務の方が名前を入力")
    roomSeal = models.CharField(max_length=20,blank=True,help_text="申請した部屋管理の方が名前を入力")
    states = ((1, '使用前'), (2, '使用中'),(3, '終了後'))
    state = models.IntegerField(default=1,help_text="部屋の使用を使用前/使用中/終了後",choices=states)
    created_datetime = models.DateTimeField(auto_now_add=True)
    updated_datetime = models.DateTimeField(auto_now=True)
