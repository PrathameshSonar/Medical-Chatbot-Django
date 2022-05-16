from django.shortcuts import render, redirect, reverse
from . import forms, models
from django.db.models import Sum
from django.contrib.auth.models import Group
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.conf import settings
from customer.chat import get_response, bot_name
from datetime import date, timedelta
import speech_recognition as sr
from django.db.models import Q
from django.core.mail import send_mail
from django.shortcuts import render, HttpResponse, HttpResponseRedirect, redirect
from medical import models as CMODEL
from medical import forms as CFORM
from googletrans import Translator
from translate import Translator as trans
from django.views.generic import TemplateView
from django.contrib.auth.models import User


def customerclick_view(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('afterlogin')
    return render(request, 'customer/customerclick.html')


def customer_signup_view(request):
    userForm = forms.CustomerUserForm()
    customerForm = forms.CustomerForm()
    mydict = {'userForm': userForm, 'customerForm': customerForm}
    if request.method == 'POST':
        userForm = forms.CustomerUserForm(request.POST)
        customerForm = forms.CustomerForm(request.POST, request.FILES)
        if userForm.is_valid() and customerForm.is_valid():
            user = userForm.save()
            user.set_password(user.password)
            user.save()
            customer = customerForm.save(commit=False)
            customer.user = user
            customer.save()
            my_customer_group = Group.objects.get_or_create(name='CUSTOMER')
            my_customer_group[0].user_set.add(user)
        return HttpResponseRedirect('customerlogin')
    return render(request, 'customer/customersignup.html', context=mydict)


def is_customer(user):
    return user.groups.filter(name='CUSTOMER').exists()


class eng(TemplateView):
    Template_view = "customer/eng.html"
    
    def get(self, request):
        return render(request, self.Template_view, {'english' : True})

    def post(self, request):
        if request.method == 'POST':

            user = request.POST.get('input', False)

            if user:
                res = user
            
            else:


                r = sr.Recognizer()
                print("Please talk")
                with sr.Microphone() as source:
                    # read the audio data from the default microphone
                    audio_data = r.record(source, duration=10)
                    print("Recognizing...")
                    # convert speech to text
                    text = r.recognize_google(audio_data)
                    print("Recognised Speech:" + text)
                    res = text
                
            
            result = get_response(res)
            
            context = {"user": res, "bot": result, 'english' : True}
            return render(request, self.Template_view, context)

    # def get(self, request):
    #     return render(request, self.Template_view)

    # def post(self, request):
    #     if request.method == 'POST':
    #         user = request.POST.get('input', False)
    #         context = {"user": user, "bot": get_response(user)}
    #     return render(request, self.Template_view, context)


class engm(TemplateView):
    Template_view = "customer/engm.html"

    def get(self, request):
        return render(request, self.Template_view, {'marathi' : True})

    def post(self, request):
        if request.method == 'POST':
            r = sr.Recognizer()
            print("Please talk")
            with sr.Microphone() as source:
                audio_data = r.record(source, duration=10)
                print("Recognizing...")
                # convert speech to text
                text = r.recognize_google(audio_data)
                print("Recognised Speech:" + text)
                a = text
                translator1 = Translator()
                source_lan1 = "mr"
                translated_to1 = "en"
                translated_text1 = translator1.translate(
                    text, src=source_lan1, dest=translated_to1)
                res = translated_text1.text
                print(translated_text1.text)
                translator5 = trans(from_lang="en", to_lang="mr")
                data3 = translator5.translate(text)
                print(data3)
                print(res)
                result = get_response(res)
                translator2 = Translator()
                source_lan2 = "en"
                translated_to2 = "mr"
                translated_text2 = translator2.translate(
                    result, src=source_lan2, dest=translated_to2)

                print(translated_text2.text)
                final = translated_text2.text

                context = {"user": data3, "bot": final, 'marathi' : True}
            return render(request, self.Template_view, context)


class engh(TemplateView):
    Template_view = "customer/engh.html"

    def get(self, request):
        return render(request, self.Template_view, {'hindi' : True})


    def post(self, request):
        if request.method == 'POST':
            r = sr.Recognizer()
            print("Please talk")
            with sr.Microphone() as source:
                # read the audio data from the default microphone
                audio_data = r.record(source, duration=10)
                print("Recognizing...")
                # convert speech to text
                text = r.recognize_google(audio_data)
                print("Recognised Speech:" + text)
                a = text
                translator1 = Translator()
                source_lan1 = "hi"
                translated_to1 = "en"
                translated_text1 = translator1.translate(
                    text, src=source_lan1, dest=translated_to1)
                res = translated_text1.text
                print(translated_text1.text)
                translator5 = trans(from_lang="en", to_lang="hi")
                data3 = translator5.translate(text)
                print(data3)
                print(res)
                result = get_response(res)
                translator2 = Translator()
                source_lan2 = "en"
                translated_to2 = "hi"
                translated_text2 = translator2.translate(
                    result, src=source_lan2, dest=translated_to2)

                print(translated_text2.text)
                final = translated_text2.text

                context = {"user": data3, "bot": final, 'hindi' : True}
            return render(request, self.Template_view, context)


from .models import *
@login_required(login_url='customerlogin')
def customer_dashboard_view(request):
    data = Customer.objects.get(user = request.user)
    dict = {
        'customer': Customer.objects.get(user_id=request.user.id),
        'dashboard' : True,
        'data' : data,

    }
    

    return render(request, 'customer/customer_dashboard.html', context=dict)


''' 
class home(TemplateView):
	Template_view="index.html"

	def get(self,request):
		return render(request,self.Template_view)

	def post(self,request):
		if request.method == 'POST':
			user = request.POST.get('input',False)
			context={"user":user,"bot":get_response(user)}
			
		return render(request,self.Template_view,context)
      
class hindi(TemplateView):
	Template_view="customer/hindi.html"

	def get(self,request):
		return render(request,self.Template_view)

	def post(self,request):
		if request.method == 'POST':
                        r = sr.Recognizer()
                        print("Please talk")
                        with sr.Microphone() as source:
                        # read the audio data from the default microphone
                                audio_data = r.record(source, duration=10)
                                print("Recognizing...")
                                # convert speech to text
                                text = r.recognize_google(audio_data)
                                print("Recognised Speech:" + text)
                                a=text
                                translator = Translator()
                                source_lan = "hi"
                                translated_to= "en"
                                translated_text = translator.translate(text, src=source_lan, dest = translated_to)
                                res=translated_text.text
                                print(translated_text.text)
                                translator5 = trans(from_lang="en", to_lang="hi")
                                data3 = translator5.translate(text)
                                print(data3)
                                result=get_response(res)
                                translator6 = trans(from_lang="en", to_lang="hi")
                                r = translator5.translate(result)
                                print(r)
                                context={"user":data3,"bot":r}
                        return render(request,self.Template_view,context)
class marathi(TemplateView):
	Template_view="customer/marathi.html"

	def get(self,request):
		return render(request,self.Template_view)

	def post(self,request):
		if request.method == 'POST':
			user = request.POST.get('input',False)
			context={"user":user,"bot":get_response(user)}
			
		return render(request,self.Template_view,context)
        '''


def doctor_signup(request):

    if request.method == 'POST':

        form = forms.doctorFrom(request.POST)

        if form.is_valid():
            form.save()
        else:
            print(form.errors)

        return render(request, "customer/doctorsignup_thankyou.html")

    else:
        return render(request, "customer/doctorsignup.html")
