from django.shortcuts import render,HttpResponse,HttpResponseRedirect,redirect
from mainpage.models import Product,Category,ExtendedUser,order
from django.contrib.auth.models import User,auth
from django.core.mail import send_mail,EmailMultiAlternatives
from django.contrib import messages
from django.contrib.auth import authenticate
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm,AuthenticationForm,SetPasswordForm
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from gopalji import settings
import razorpay
# Create your views here.
def indexpage(request):
    allcategories=Category.objects.all()
    myproducts=Product.objects.all()
    prod1=Product.objects.filter(prod_deal="New Arraivels")
    
    
    # TrendingProducts=Product.objects.filter(Prod_type=1)
    # newproducts=Product.objects.filter(Prod_type=2)
    cart=request.session.get('cart')
    if not cart:
        request.session.cart={}
    if request.user.is_authenticated:
         profile = ExtendedUser.objects.get(user=request.user)
         return render(request,'index.html',{'allcategories':allcategories,'myproducts':myproducts,'profile':profile,'prod1':prod1})
    return render(request,'index.html',{'allcategories':allcategories,'myproducts':myproducts,'prod1':prod1})

def productsearch(request):
    allcategories=Category.objects.all()
    if "qry" in request.GET:
        q=request.GET["qry"]
        print(q)
        if Product.objects.filter(category=q):
            myproducts=Product.objects.filter(category=q)
            return render(request,'customerview.html',{'myproducts':myproducts,'allcategories':allcategories})
    return HttpResponse("not fond")
    
def productview(request,myid):
    allcategories=Category.objects.all()
    myproducts=Product.objects.filter(id=myid)
    return render(request,'productview.html',{'myproducts':myproducts[0],'allcategories':allcategories})

def myaddtocart(request):
    if request.method=='POST':
        productt=request.POST['sendid']
        print(productt)
        cart=request.session.get('cart')
        print("empty card = ",cart)
        if cart:
           quantity = cart.get(productt)
           print(cart.get(productt))
           if quantity:
                cart[productt] = quantity+1  
                print("+1 kita")
           else:
               cart[productt] = 1
        else:
            cart={}
            cart[productt] = 1
        request.session['cart'] = cart
        print( request.session['cart'])
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

def mycart(request):
    allcategories=Category.objects.all()
    cart=request.session.get('cart')
    if not cart:
        request.session.cart={}
        return render(request,'showcart.html',{"allcategories":allcategories})
    print(request.session.get('cart'))
    print(request.session.get('cart').keys())
    print("list of keys = ",list(request.session.get('cart').keys()))
    ids=list(request.session.get('cart').keys())
    print(ids)
    myproducts=Product.objects.filter(id__in=ids)
    print(myproducts)
    return render(request,'showcart.html',{'myproducts':myproducts,"allcategories":allcategories})

def clearcart(request):
    # request.session.get('cart').clear()
    request.session['cart'] = {}
    print("cart clear")
    return HttpResponseRedirect('/')

def myorders(request):
    if request.user.is_authenticated:
        mcart=order.objects.filter(cust_ki_id=request.user.id)
        return render(request,'myorders.html',{'mcart':mcart})
    return redirect('login')

def myaddtocarttcart(request):
    if request.method=='POST':
        productt=request.POST['sendid']
        remove=request.POST['remove']
        print(productt,remove)
        cart=request.session.get('cart')
        # print(cart)
        if cart:
           quantity = cart.get(productt)
           if quantity:
               if remove:
                   if quantity<=1:
                       cart.pop(productt)
                       print("pop kiya")
                   else:    
                      cart[productt] = quantity-1
                      print("-1 kiya")
               else:
                 cart[productt] = quantity+1  
                 print("+1 kita")
           else:
               cart[productt] = 1
        else:
            cart={}
            cart[productt] = 1
        request.session['cart'] = cart
        print( request.session['cart'])
        return HttpResponseRedirect('mycart')  

def myaddtocartcart(request):
    if request.method=='POST':
        productt=request.POST['sendid']
        cart=request.session.get('cart')
        # print(cart)
        if cart:
           quantity = cart.get(productt)
           if quantity:
                cart[productt] = quantity+1  
                print("+1 kita")
           else:
               cart[productt] = 1
        else:
            cart={}
            cart[productt] = 1
        request.session['cart'] = cart
        print( request.session['cart'])
        return HttpResponseRedirect('mycart') 

def removecatitem(request):
    if request.method=='POST':
        productt=request.POST['sendid']
        remove=request.POST['remove']
        print(productt,remove)
        cart=request.session.get('cart')
        # print(cart)
        if cart:
           quantity = cart.get(productt)
           if quantity:
               if remove:
                   if quantity:
                       cart.pop(productt)
                       print("pop kiya")
                   else:    
                       cart.pop(productt)
                       print("pop kiya")
               else:
                 cart[productt] = quantity+1  
                 print("+1 kita")
           else:
               cart[productt] = 1
        else:
            cart={}
            cart[productt] = 1
        request.session['cart'] = cart
        print( request.session['cart'])
        return HttpResponseRedirect('mycart')  

def login(request):
    if request.method=='POST':
            uname=request.POST['username']
            ppass=request.POST['Password']
            #  print(uname,ppass)
            user=auth.authenticate(username=uname,password=ppass)
            if user is not None:
                auth.login(request,user)
                myproducts=Product.objects.all()
                if request.user.is_authenticated:
                   return HttpResponseRedirect('/')
                return render(request,'index.html',{'myproducts':myproducts})
               
            else:
                print("record not found") 
                messages.info(request,'Password or username is incorrect Or Create your new Account')  
                return redirect('login')
                # this elif is for get request
    elif request.user.is_authenticated:
        myproducts=Product.objects.all()
        profile = ExtendedUser.objects.get(user=request.user)
        return render(request,'index.html',{'profile':profile,'myproducts':myproducts})
    return render(request,'login.html')

def signup(request):
    if request.method=='POST':
        f_name=request.POST['firstname']
        l_name=request.POST['lastname']
        u_name=request.POST['username']
        passw1=request.POST['password']
        passw2=request.POST['repassword']
        email=request.POST['email']
        phone1=request.POST['phone']
        phone2=request.POST['altnum']
        addre=request.POST['address']
        print(f_name)
        if User.objects.filter(username=u_name).exists():
            messages.info(request,'User Name already exists...')
            # print("user pale se available hai")
            return redirect('signup')
        else:
            user=ExtendedUser.objects.create_user(first_name=f_name,last_name=l_name,username=u_name,password=passw2,email=email,phone_no=phone1, alt_no=phone2,address=addre)
            user.save()
            user=auth.authenticate(username=u_name,password=passw2)
            if user is not None:
                auth.login(request,user)
                return HttpResponseRedirect('/')
            return redirect('signin')     
                # messages.add_message(request,messages.SUCCESS,' Account Created Successfully..!!!')
            # print("user created") 
              
            
    return render(request,'createaccount.html')
def logout(request):
    auth.logout(request)
    return redirect('/')

def profile(request):
    if request.user.is_authenticated:
        profile = ExtendedUser.objects.get(user=request.user)
        return render(request,'profile.html',{'profile':profile})
    return render(request,'login.html')

def edit_profile(request):
    if request.user.is_authenticated:
        profile = ExtendedUser.objects.get(user=request.user)
        if request.method=='POST':
            print(request.POST)
            f_name=request.POST['firstname']
            l_name=request.POST['lastname']
            u_name=request.POST['username']
            email=request.POST['email']
            phone1=request.POST['phone']
            phone2=request.POST['altnum']
            addre=request.POST['address']
            print(f_name)
            usra=ExtendedUser.objects.get(user=request.user)
            usra.first_name=f_name
            usra.last_name=l_name
            usra.phone_no=phone1
            usra.alt_no=phone2
            usra.email=email
            usra.address=addre
            usra.username=u_name
            usra.save()
        return render(request,'editprofile.html',{'profile':profile})
    return render(request,'login.html')    

def changepassword(request):
    if request.user.is_authenticated: 
        if request.method == "POST":
            fm = PasswordChangeForm(user=request.user,data=request.POST)
            if fm.is_valid():
                # print(fm)
                fm.save()
                update_session_auth_hash(request,fm.user)
                messages.success(request,'password change Successfully')
                return HttpResponseRedirect('profile')
        else:    
            fm=PasswordChangeForm(user=request.user)
        return render (request,'changepassword.html',{'form':fm})
    else:
        return HttpResponseRedirect('login')     

# another method to change password is old password nai hoga
def changepassword2(request):
    if request.user.is_authenticated: 
        if request.method == "POST":
            fm = SetPasswordForm(user=request.user,data=request.POST)
            if fm.is_valid():
                fm.save()
                update_session_auth_hash(request,fm.user)
                messages.success(request,'password change Successfully')
                return HttpResponseRedirect('profile')
        else:    
            fm=SetPasswordForm(user=request.user)
        return render (request,'changepassword.html',{'form':fm})
    else:
        return HttpResponseRedirect('login')    

def search(request):
    allcategories=Category.objects.all()
    myproducts=Product.objects.all()
    cart=request.session.get('cart')
    if not cart:
        request.session.cart={}
    if "qry" in request.GET:
        q=request.GET["qry"]
        if Product.objects.filter(prod_name__icontains=q):
            myproducts=Product.objects.filter(prod_name__icontains=q)
            return render(request,'search.html',{'myproducts':myproducts,'allcategories':allcategories})
     
        elif Product.objects.filter(Prod_descriptiontwo__icontains=q):  
            myproducts=Product.objects.filter(Prod_descriptiontwo__icontains=q)
            return render(request,'search.html',{'myproducts':myproducts,'allcategories':allcategories}) 
        elif Product.objects.filter(Prod_descriptionthree__icontains=q):  
            myproducts=Product.objects.filter(Prod_descriptionthree__icontains=q)
            return render(request,'search.html',{'myproducts':myproducts}) 
        elif Product.objects.filter(Prod_descriptionfour__icontains=q):  
            myproducts=Product.objects.filter(Prod_descriptionfour__icontains=q)
            return render(request,'search.html',{'myproducts':myproducts,'allcategories':allcategories}) 
        elif Product.objects.filter(Prod_descriptionfive__icontains=q):  
            myproducts=Product.objects.filter(Prod_descriptionfive__icontains=q)
            return render(request,'search.html',{'myproducts':myproducts,'allcategories':allcategories}) 
        elif Product.objects.filter(Prod_descriptionsix__icontains=q):  
            myproducts=Product.objects.filter(Prod_descriptionsix__icontains=q)
            return render(request,'search.html',{'myproducts':myproducts,'allcategories':allcategories})      
        elif Product.objects.filter(prod_price__icontains=q):  
            myproducts=Product.objects.filter( prod_price__icontains=q)
            return render(request,'search.html',{'myproducts':myproducts,'allcategories':allcategories}) 
      
    return HttpResponse("<h1>No result found</h1>") 

def orderdone(request):
     if request.user.is_authenticated:
        profile = ExtendedUser.objects.get(user=request.user)
        currentcustomer=profile.user_id
        cart=request.session.get('cart')
        print("my cart = ",cart)
        mproducts=Product.objects.filter(id__in=list(cart.keys()))
        print(mproducts)
        for i in mproducts:
            print("quant",cart.get(str(i.id)))
            Product_ki_quantity=cart.get(str(i.id))
            html_content=render_to_string("email_template.html",{'content':i,'profile':profile,'Product_ki_quantity':Product_ki_quantity})
            text_content=strip_tags(html_content)
            email=EmailMultiAlternatives(
               "Your GOPALI Order confirmation",
                text_content,
                settings.EMAIL_HOST_USER,
                [ profile.email],
                )
            email.attach_alternative(html_content,"text/html")
           
            email.send(fail_silently=True)
            ordernow=order(customer_id=currentcustomer,product_order_id=i.id,cust_ki_id=currentcustomer,cust_ka_name=profile.first_name,cust_ka_username=profile.username,cust_ka_phone=profile.phone_no, cust_ka_alt_no=profile.phone_no,cust_ki_email=profile.email, cust_ka_address=profile.address,Product_ki_quantity=cart.get(str(i.id)),Product_ki_id=i.id,product_ki_price=i.prod_price,product_ka_name=i.prod_name, product_ki_img=i.prod_img)
            ordernow.save()
        request.session['cart'] = {}    
        return render(request,'orderdone.html')
     return render(request,'login.html') 

def gopaljigift(request):
    myproducts=Product.objects.filter(id=2)
    print(myproducts)
    return render(request,'gopaljigiftcard.html',{'myproducts':myproducts[0]})

def success(request):
    if request.method=="POST":
        a=request.post_save
        print(a)
        request.session['cart'] = {}
    return render(request,"orderdone.html")