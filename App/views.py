from django.shortcuts import render

from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import cache_control #Destroy after logout
from . models import Customer #From models.py
from App.forms import Customerform, EmailForm
from django.contrib import messages #return messages
from django.http import HttpResponseRedirect #redirect the pages
from django.core.paginator import Paginator #Pagination
from django.db.models import Q #Global Search
from datetime import datetime #to get Today's message
from django.core.mail import EmailMessage, EmailMultiAlternatives # Send mails
from django.template.loader import render_to_string #
from django.utils.html import strip_tags
from django.contrib.auth import logout #To auto logout

# =========== FRONT END ===================
def home(request):
    return render(request, "home.html")

def sendMessage(request):
    if request.method == "POST":
        form = Customerform(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "Message send successfully! ")
            return HttpResponseRedirect('/')
        else:
            form = Customerform()
        return render(request, 'home.html', {'form': form})

# ============ BACK END =================
@login_required(login_url="login")
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def inbox(request):
    if 'q' in request.GET:
        q = request.GET['q']
        all_customer_list = Customer.objects.filter(
            Q(name__icontains=q) | Q(phone__icontains=q) | Q(email__icontains=q) | Q(subject__icontains=q) | Q(status__icontains=q) | Q(message__icontains=q)
        ).order_by('-created_at')
    else:
        all_customer_list = Customer.objects.all().order_by('-created_at')

    paginator = Paginator(all_customer_list, 10)
    page = request.GET.get('page')
    all_customer = paginator.get_page(page)

    # Messages counter
    # Total
    total = Customer.objects.all().count()
    # Read
    read = Customer.objects.filter(status='Read')
    # Unread
    unread = Customer.objects.filter(status='Pending')
    # Today
    base = datetime.now().date()
    today = Customer.objects.filter(created_at__gt = base)

    context = {'customers':all_customer, 'total':total, 'read':read, 'unread':unread, 'today':today}
    return render(request, "inbox.html", context)

@login_required(login_url="login")
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def deleteMessage(request, customer_id):
    customer = Customer.objects.get(id=customer_id)
    customer.delete()
    messages.success(request, "Message deleted successfully !")
    return HttpResponseRedirect('/inbox')

# View message individually
@login_required(login_url="login")
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def Customers(request, customer_id):
    customer = Customer.objects.get(id=customer_id)
    if customer != None :
        return render(request, "customer.html", {'customer': customer})

@login_required(login_url="login")
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def markAsRead(request):
    if request.method == 'POST':
        customer = Customer.objects.get(id=request.POST.get('id'))
        if customer != None:
            customer.status = request.POST.get('status')
            customer.save()
            messages.success(request, "Message marked as read!")
            return HttpResponseRedirect('/inbox')

def email(request):
    if request.method == 'POST':
        form = EmailForm(request.POST, request.FILES)
        company = "Reply from OurProject"
        if form.is_valid():
            subject = form.cleaned_data["subject"]
            message = form.cleaned_data["message"]
            email = form.cleaned_data["email"]
            cc = form.cleaned_data["cc"]
            files = request.FILES.getlist("attach")
            html_content = render_to_string("email.html", {'subject': subject, 'content': message, 'email': email, 'cc': cc, 'files':files})
            text_content = strip_tags(html_content)

            mails = EmailMultiAlternatives(subject, text_content, company, [email], [cc])

            # mail = EmailMessage(subject, message, company, [email], [cc])
            for f in files:
                mails.attach(f.name, f.read(), f.content_type)
            mails.attach_alternative(html_content, "text/html")
            mails.send()
            messages.success(request, "Reply sent successfully !")
            return HttpResponseRedirect('/inbox')
        else:
            messages.error(request, "Invalid email")
            return HttpResponseRedirect('/inbox')
    else:
        form = EmailForm()
        return render(request, {'form': form})

def AutoLogoutUser(request):
    logout(request)
    request.user = None
    messages.info(request, ".") #The argument can't be empty
    return HttpResponseRedirect('/')

############  ERRORS ###########
def E_500(request):
    return render(request, 'e500.html')

def E_404(request, exception):
    return render(request, 'e404.html')

# About Page
def about(request):
    return render(request, 'about.html')