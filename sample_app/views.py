import os
from datetime import datetime,timedelta

from django.contrib.auth import authenticate
from django.core.mail import send_mail
from django.shortcuts import render,redirect
from django.http import  HttpResponse
from .models import *
from .forms import *
from django.contrib.auth.models import User
from django.contrib import messages
import uuid
from sample_project.settings import EMAIL_HOST_USER

# Create your views here.


def first(request):
    return HttpResponse("Hello World")

def index(request):
    return render(request,'index.html')

def home(request):
    name = request.session['nameid']
    a = productmodels.objects.all()
    product = []
    price = []
    discription = []
    image = []
    id = []
    for i in a:
        id1 = i.id
        id.append(id1)

        pn = i.productname
        product.append(pn)

        pr = i.price
        price.append(pr)

        dis = i.discription
        discription.append(dis)

        im = i.image
        image.append(str(im).split('/')[-1])

    mylist = zip(product, price, discription, image, id)

    return render(request,'display.html',{'mylist': mylist,'b':name})


def shopregister(request):
    if request.method=='POST':
        a=shopregforms(request.POST)
        if a.is_valid():
            sp=a.cleaned_data['shopname']
            ad=a.cleaned_data['address']
            sid=a.cleaned_data['shopid']
            em=a.cleaned_data['email']
            nm=a.cleaned_data['phone']
            ps=a.cleaned_data['pass1']
            ps2=a.cleaned_data['pass2']
            if ps==ps2:
                b=shopregmodels(shopname=sp,address=ad,shopid=sid,email=em,phone=nm,pass1=ps)
                b.save()
                return redirect(shoplogin)
            else:
                return HttpResponse("not success")
        else:
            return HttpResponse("failed")
    return render(request,'shopregister.html')

def shoplogin(request):
    if request.method=='POST':
        a=shoplogforms(request.POST)
        if a.is_valid():
            sn=a.cleaned_data['shopname']
            ps=a.cleaned_data['pass1']
            #to make a variable global
            request.session['shopname']=sn
            b=shopregmodels.objects.all()
            for i in b:

                if sn==i.shopname and ps==i.pass1:
                    request.session['id']=i.id
                    return redirect(profilee)
            else:
                messages.success(request, 'Wrong password or username')
                return redirect(shoplogin)

    return render(request,"shoplogin.html")







def productupload(request):
    if request.method=='POST':
        a=productForms(request.POST,request.FILES)
        id = request.session['id']
        if a.is_valid():
            pn=a.cleaned_data['productname']
            p=a.cleaned_data['price']
            d=a.cleaned_data['discription']
            im=a.cleaned_data['image']
            b=productmodels(shopid=id,productname=pn,price=p,discription=d,image=im)
            b.save()
            return redirect(profilee)
        else:
            return HttpResponse("upload failed")
    return render(request,'fileupload.html')

def productdisplay(request):
    b=request.session['id']
    a=productmodels.objects.all()

    product=[]
    price=[]
    discription=[]
    image=[]
    id=[]
    shopidL=[]
    for i in a:
        sid=i.shopid
        shopidL.append(sid)
        id1=i.id
        id.append(id1)

        pn=i.productname
        product.append(pn)

        pr=i.price
        price.append(pr)

        dis=i.discription
        discription.append(dis)

        im=i.image
        image.append(str(im).split('/')[-1])

    mylist=zip(product,price,discription,image,id,shopidL)
    return render(request,'productdisplay.html',{'mylist':mylist,'sid':b,'shopid':shopidL})

#models.object.all()//fetch all

#models.objects.get(id=)
def productdelete(request,id):
    a=productmodels.objects.get(id=id)
    a.delete()
    return redirect(productdisplay)

def productedit(request,id):
    a=productmodels.objects.get(id=id)
    im=str(a.image).split('/')[-1]
    if request.method=='POST':
        if len(request.FILES):   #to check the new file
            if len(a.image)>0:   #to check old files
                os.remove(a.image.path)
            a.image=request.FILES['img']
        a.productname=request.POST.get('pname')
        a.price=request.POST.get('price')
        a.discription=request.POST.get('disc')
        a.save()
        return redirect(productdisplay)


    return render(request,'editproduct.html',{'a':a,'im':im})




def regis(request):
    if request.method=='POST':
        username=request.POST.get('username')
        email=request.POST.get('email')
        firstname=request.POST.get('first_name')
        lastname=request.POST.get('last_name')
        password=request.POST.get('password')

        #checking wether the username exists
        if User.objects.filter(username=username).first():
            #filter is used to search filter the msg and allow you to return only the row the matches the search
            #it will get the first object from the filter query
            messages.success(request,'username already taken')
            #message that is the framework that allows you to store messages in one request and retrive them in request page
            return redirect(regis)
        if User.objects.filter(email=email).first():
            messages.success(request,'email already exist')
            return redirect(regis)
        # if User.objects.filter(email=None):
        #     messages.success(request,'email already exist11111')
        #     return redirect(regis)

        user_obj=User(username=username,email=email,first_name=firstname,last_name=lastname)
        user_obj.set_password(password)
        user_obj.save()

        #uuid module:uuid that's stands for universally unique identifiers
        #uuid4() create a random uuid
        auth_token=str(uuid.uuid4())
        #new models created
        profile_obj=profile.objects.create(user=user_obj,auth_token=auth_token)
        profile_obj.save()
        #user defined function
        send_email_register(email,auth_token) #email sending function
        return render(request,'success.html')
    return render(request,'userregister.html')




def send_email_register(email,auth_token):
    subject="your account has been verified"
    message=f'click the link to verify your account http://127.0.0.1:8000/verify/{auth_token} '
    #f is a string literal which contains expressions inside curley brakets the expression are replaced by values
    email_from=EMAIL_HOST_USER
    recipient=[email]
    #inbuild function
    send_mail(subject,message,email_from,recipient)







def uprofile(request):
    return render(request,'userprofile.html')



def profilee(request):
    shopname=request.session['shopname']
    return render(request,'profile.html',{'shopname':shopname})

def success(request):
    return render(request,'success.html')

def verify(request,auth_token):
    profile_obj=profile.objects.filter(auth_token=auth_token).first()
    if profile_obj:
        if profile_obj.is_verified:
            messages.success(request,'your account is already verified')
            return redirect(login)
        profile_obj.is_verified=True
        profile_obj.save()
        messages.success(request,'your account has been verified')
        return redirect(login)
    else:
        messages.success(request,'user not found')
        return redirect(login)

def login(request):
    if request.method=='POST':
        username=request.POST.get('username')
        password=request.POST.get('password')
        request.session['nameid']=username
        user_obj=User.objects.filter(username=username).first()
        if user_obj is None:
            messages.success(request,'user not registered yet')
            return redirect(login)
        request.session['userid'] = user_obj.id
        profile_obj=profile.objects.filter(user=user_obj).first()
        if not profile_obj.is_verified:
            messages.success(request,'profile not verified check your mail')
            return redirect(login)
        user=authenticate(username=username,password=password)
        if user is None:
            messages.success(request,'wrong password or username')
            return redirect(login)
        return redirect(home)
    return render(request,'userlogin.html')


def addtocart(request,id):
    c=request.session['userid']
    a=productmodels.objects.get(id=id)
    # if cart.objects.filter(productname=a.productname):
    #     return HttpResponse("already in cart")
    # else:
    b=cart(productname=a.productname,price=a.price,discription=a.discription,image=a.image,userid=c)
    b.save()
    return redirect(home)
    # return render(request,'cart.html')

def Waddtocart(request,id):
    c=request.session['userid']
    a=wishlist.objects.get(id=id)
    # if cart.objects.filter(productname=a.productname):
    #     return HttpResponse("already in wishlist")
    # else:

    b=cart(productname=a.productname,price=a.price,discription=a.discription,image=a.image,userid=c)
    b.save()
    return redirect(cartdisplay)

def cartdisplay(request):
    b=request.session['userid']
    a=cart.objects.all()
    product = []
    price = []
    discription = []
    image = []
    id = []
    useridL=[]
    for i in a:
        a=i.userid
        useridL.append(a)

        id1 = i.id
        id.append(id1)

        pn = i.productname
        product.append(pn)

        pr = i.price
        price.append(pr)

        dis = i.discription
        discription.append(dis)

        im = i.image
        image.append(str(im).split('/')[-1])

    mylist = zip(product, price, discription, image, id,useridL)
    return render(request, 'cart.html', {'mylist': mylist,'sid':b,'userid':useridL})

def viewfull(request):
    a=productmodels.objects.all()

    product=[]
    price=[]
    discription=[]
    image=[]
    id=[]
    shopidL=[]
    for i in a:
        sid=i.shopid
        shopidL.append(sid)
        id1=i.id
        id.append(id1)

        pn=i.productname
        product.append(pn)

        pr=i.price
        price.append(pr)

        dis=i.discription
        discription.append(dis)

        im=i.image
        image.append(str(im).split('/')[-1])

    mylist=zip(product,price,discription,image,id)
    return render(request,'alldisplay.html',{'mylist':mylist})



def addwish(request,id):
    c=request.session['userid']
    a=productmodels.objects.get(id=id)
    # if wishlist.objects.filter(productname=a.productname):
    #     return HttpResponse("already in wishlist")
    b=wishlist(productname=a.productname,price=a.price,discription=a.discription,image=a.image,userid=c)
    b.save()
    return redirect(home)


def wishlistdisplay(request):
    b=request.session['userid']
    a=wishlist.objects.all()
    product = []
    price = []
    discription = []
    image = []
    id = []
    userid=[]
    for i in a:
        nga=i.userid
        userid.append(nga)

        id1 = i.id
        id.append(id1)

        pn = i.productname
        product.append(pn)

        pr = i.price
        price.append(pr)

        dis = i.discription
        discription.append(dis)

        im = i.image
        image.append(str(im).split('/')[-1])

    mylist = zip(product, price, discription, image, id,userid)
    print(product,price,discription,image,id,userid)
    return render(request, 'wishlist.html', {'mylist': mylist,'sh':b,'use':userid})


def cdelete(request,id):
    a=cart.objects.get(id=id)
    a.delete()
    return redirect(cartdisplay)

def wdelete(request,id):
    a=wishlist.objects.get(id=id)
    a.delete()
    return redirect(wishlistdisplay)

def cartbuy(request,id):
    a=cart.objects.get(id=id)
    im = str(a.image).split('/')[-1]
    if request.method=='POST':
        productname=request.POST.get('productname')
        quantity=request.POST.get('quantity')
        price=request.POST.get('price')
        b=buy(productname=productname,price=price,quantity=quantity)
        b.save()
        total=int(price)*int(quantity)
        return render(request,'finalbuy1.html',{'total':total,'name':productname,'quantity':quantity,'price':price})
    return render(request,'buyed.html',{'a':a,'im':im})

def C_card(request):
    if request.method=='POST':
        ids=request.session['userid']
        cardname = request.POST.get('cardname')
        cardnumber = request.POST.get('cardnumber')
        carddate = request.POST.get('carddate')
        scode = request.POST.get('scode')
        # checking wether the username exists
        b=customercardM(cardname=cardname,cardnumber=cardnumber,carddate=carddate,scode=scode)
        b.save()
        date=datetime.today().date()+timedelta(days=10)
        a=User.objects.get(id=ids)
        mail=a.email
        send_email_reg(mail,date)
        return render(request,'order.html',{'date':date})
    return render(request,'Ecard.html')


def send_email_reg(email,date):
        subject = "order summary"
        message = f'Order has been placed {date} '
        # f is a string literal which contains expressions inside curley brakets the expression are replaced by values
        email_from = EMAIL_HOST_USER
        recipient = [email]
        # inbuild function
        send_mail(subject, message, email_from, recipient)



def fictiondisplay(request):
    return render(request,'fiction.html')

def dummyindex(request):
    a = productmodels.objects.all()
    product = []
    price = []
    discription = []
    image = []
    id = []
    for i in a:
        id1 = i.id
        id.append(id1)

        pn = i.productname
        product.append(pn)

        pr = i.price
        price.append(pr)

        dis = i.discription
        discription.append(dis)

        im = i.image
        image.append(str(im).split('/')[-1])

    mylist = zip(product, price, discription, image, id)

    return render(request, 'index2.html', {'mylist': mylist,})



def carthorror(request,id):
    c = request.session['userid']
    a = productmodels.objects.get(id=id)
    # if cart.objects.filter(productname=a.productname):
    #     return HttpResponse("already in cart")
    # else:

    b = cart(productname=a.productname, price=a.price, discription=a.discription, image=a.image, userid=c)
    b.save()
    return redirect(horror)



def horror(request):
    b=request.session['userid']
    a=productmodels.objects.all()

    product=[]
    price=[]
    discription=[]
    image=[]
    id=[]
    shopidL=[]
    for i in a:
        if i.discription=='Horror':
            sid=i.shopid
            shopidL.append(sid)
            id1=i.id
            id.append(id1)

            pn=i.productname
            product.append(pn)

            pr=i.price
            price.append(pr)

            dis=i.discription
            discription.append(dis)

            im=i.image
            image.append(str(im).split('/')[-1])

    mylist=zip(product,price,discription,image,id,shopidL)
    return render(request,'horror.html',{'mylist':mylist,'sid':b,'shopid':shopidL})



def addto2(request,id):
    c = request.session['userid']
    a = productmodels.objects.get(id=id)
    # if cart.objects.filter(productname=a.productname):
    #     return HttpResponse("already in cart")
    # else:
    b = cart(productname=a.productname, price=a.price, discription=a.discription, image=a.image, userid=c)
    b.save()
    return redirect(fiction)


def wishfiction(request,id):
    c = request.session['userid']
    a = productmodels.objects.get(id=id)
    # if cart.objects.filter(productname=a.productname):
    #     return HttpResponse("already in cart")
    # else:

    b = wishlist(productname=a.productname, price=a.price, discription=a.discription, image=a.image, userid=c)
    b.save()
    return redirect(fiction)



def fiction(request):
    b = request.session['userid']
    a = productmodels.objects.all()

    product = []
    price = []
    discription = []
    image = []
    id = []
    shopidL = []
    for i in a:
        if i.discription == 'fiction':
            sid = i.shopid
            shopidL.append(sid)
            id1 = i.id
            id.append(id1)

            pn = i.productname
            product.append(pn)

            pr = i.price
            price.append(pr)

            dis = i.discription
            discription.append(dis)

            im = i.image
            image.append(str(im).split('/')[-1])

    mylist = zip(product, price, discription, image, id, shopidL)
    return render(request, 'fiction.html', {'mylist': mylist, 'sid': b, 'shopid': shopidL})

def shopNoti(request):
    a=shopNotification.objects.all()
    shoptime=[]
    note=[]
    for i in a:
        no=i.content
        note.append(no)
        t=i.date
        shoptime.append(t)
    mylist=zip(note,shoptime)
    return render(request,'shopnoti.html',{'n':mylist})




def userNoti(request):
    a=userNotification.objects.all()
    note=[]
    shoptime=[]
    for i in a:
        no=i.content
        note.append(no)
        t=i.date
        shoptime.append(t)
    mylist=zip(note,shoptime)

    return render(request,'usernoti.html',{'n':mylist})







