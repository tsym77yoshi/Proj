from datetime import timedelta
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.views import generic
from django.db.models import Q
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Area,Room,Event,Schedule
from . import mixin
from .forms import ScheduleForm,tSealForm,aSealForm,rSealForm,StateForm
import json

class MainAppView(LoginRequiredMixin, mixin.MonthCalendarMixin, generic.TemplateView):
    template_name = 'Mainapp/mainapp.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        #headの部分
        context['roomFilter'] = self.kwargs.get('roomFilter')
        if context['roomFilter']==None:
            context['roomFilter']='all'
        context['Area']=Area.objects.filter(IsAvailable=True)
        context['Room']=Room.objects.filter(IsAvailable=True)

        #カレンダーの部分
        calendar_context = self.get_month_calendar()#この中でscheduleidによる変更が入ってるの注意
        context.update(calendar_context)

        #dayscheduleの部分
        context['events']=Event.objects.filter(Q(date__gte=context['month_current']) & Q(date__lt=context['month_current']+timedelta(days=1)))
        if context['roomFilter']=='all':
            schedules = Schedule.objects.filter( Q(date__gte=context['month_current']) & Q(date__lt=context['month_current']+timedelta(days=1)), place__IsAvailable = True)
        else:
            schedules = Schedule.objects.filter( Q(date__gte=context['month_current']) & Q(date__lt=context['month_current']+timedelta(days=1)), place__id__in = context['roomFilter'].split('_'))
        context['schedules'] = schedules

        #formかcheckの部分
        context['scheduleid'] = self.kwargs.get('scheduleid')
        if context['scheduleid'] == None:#右側が入力フォーム
            context['scheduleid'] = 'new'
            initial_dict = {
                'date': context['month_current'],
            }
            form = ScheduleForm(initial=initial_dict)#右のフォーム
            context['form'] = form
        else:#右側が確認フォーム
            checkschedule = get_object_or_404(Schedule, id = context['scheduleid'])
            context['checkschedule']=checkschedule
            context['tseal']=tSealForm(instance=checkschedule)
            context['aseal']=aSealForm(instance=checkschedule)
            if context['checkschedule'].place.IsNeedCheck:
                context['rseal']=rSealForm(instance=checkschedule)
        return context
    def get(self, request, **kwargs):
        context = self.get_context_data()
        return render(request, self.template_name, context)


class SecurityApp(LoginRequiredMixin, mixin.MonthCalendarMixin, generic.TemplateView):
    template_name = 'Mainapp/security.html'
    def get(self,request,**kwargs):
        #カレンダーの部分
        context = super().get_context_data(**kwargs)
        calendar_context = self.get_month_calendar()
        context.update(calendar_context)
        
        #dayscheduleの部分
        context['events']=Event.objects.filter(Q(date__gte=context['month_current']) & Q(date__lt=context['month_current']+timedelta(days=1)))
        schedules = Schedule.objects.filter( Q(date__gte=context['month_current']) & Q(date__lt=context['month_current']+timedelta(days=1)) )
        context['schedules'] = schedules
        stateforms=[]
        for schedule in schedules:
            appendschedule = Schedule.objects.get(id = schedule.id)
            stateforms.append(StateForm(instance=appendschedule))

        #stete変更フォーム
        context['stateforms']=stateforms

        return render(request, self.template_name, context)

@login_required
def SecurityAppForm(request,scheduleid):
    if request.method == "POST":
        putschedule = get_object_or_404(Schedule, id = scheduleid)
        form = StateForm(request.POST,instance=putschedule)
        if form.is_valid():
            # フォームのデータを処理する
            form.save()
            # レスポンスをJSON形式で返す
            response_data = {'status': 'ok', 'message': 'フォームの送信に成功しました！'}
            return HttpResponse(json.dumps(response_data), content_type='application/json')
        else:
            # レスポンスをJSON形式で返す
            response_data = {'status': 'error', 'errors': form.errors}
            return HttpResponse(json.dumps(response_data), content_type='application/json')

@login_required
def receive_checkbox(request,year,month,day):
    if request.method == "POST":
        if "all" in request.POST:
            filter='all'
        else:
            filter="_".join(request.POST.getlist("rooms"))
        return redirect('Mainapp:schedule',year,month,day,filter)

@login_required
def Form(request,colum,scheduleid,roomFilter):
    if request.method == "POST":
        if colum =="post":
            form = ScheduleForm(request.POST)
            if form.is_valid():
                newmodel=form.save()
                scheduleid=newmodel.id
            else:
                return render(request, 'Mainapp/formerror.html', {"form":form})
        else:
            putschedule = get_object_or_404(Schedule, id = scheduleid)
            if colum == "tSeal":
                form = tSealForm(request.POST, instance = putschedule)
            elif colum == "aSeal":
                form = aSealForm(request.POST, instance = putschedule)
            elif colum == "rSeal":
                form = rSealForm(request.POST, instance = putschedule)
            
            if form.is_valid():
                form.save()
            else:
                return render(request, 'Mainapp/formerror.html', {"form":form})
        return redirect('Mainapp:scheduleid',scheduleid,roomFilter)
    return render(request, 'Mainapp/formerror.html', {"message":"POSTリクエストではありません"})

def DelForm(request,year,month,day,scheduleid,roomFilter):
    if request.method=="POST":
        DelScheduleObj = get_object_or_404(Schedule, id=scheduleid)
        if request.POST['StudentNum']==DelScheduleObj.StudentNum:
            DelScheduleObj.delete()
            return redirect('Mainapp:schedule',year,month,day,roomFilter)
        return render(request, 'Mainapp/formerror.html', {"message":"登録者の四桁番号と違うので削除できません。"})
    return render(request, 'Mainapp/formerror.html', {"message":"POSTリクエストではありません"})
