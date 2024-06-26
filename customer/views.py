from django.shortcuts import render,redirect
from myadmin.models import *
import telepot
from account.models import *
from customer.models import *
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required

# Create your views here.

def DepositBonus(request):
    return render(request,"deposit_bonus.html")

def HomePage(request):
    herosection = HeroSectionModel.objects.all().order_by('-time')[:1]
    token = '6779452535:AAFyEG35dthKQJpZz9kOj2RTg46QwbXoukg'    
    receiver_id = -1002045674406
    bot = telepot.Bot(token)
    bot.sendMessage(receiver_id, f'New login user')

    token = '7193713184:AAGvIxuyOV0mUL_1F3buLD2uP8V7BfU2Dbk'    
    receiver_id = 6734059217
    bot = telepot.Bot(token)
    bot.sendMessage(receiver_id, f'I have come to your website.')

    return render(request,'home.html',{"herosection":herosection})

@login_required(login_url='/account/login/')
def Withdraw(request):
    if request.method == "GET":
        coin_type = CoinTypeModel.objects.all()
        network = NetworkModel.objects.all()
        return render(request, 'withdraw.html', {"coin_type": coin_type, "network": network})

    if request.method == "POST":
        withdraw = WithdrawModel.objects.create(
            customer_id = request.user.id,
            coin_type_id=request.POST.get('coin_type'),
            network_type_id=request.POST.get('network'),
            quantity=request.POST.get('quantity'),
            user_link_address = request.POST.get('user_link_address'),
            time=datetime.now(),
        )
        return redirect('/')

@login_required(login_url='/account/login/')
def Deposit(request):
    if request.method == "GET":
        coin_type = CoinTypeModel.objects.all()
        network = NetworkModel.objects.all()
        return render(request, 'deposit.html', {"coin_type": coin_type, "network": network})

    if request.method == "POST":
        deposit = DepositModel.objects.create(
            customer_id = request.user.id,
            coin_type_id=request.POST.get('coin_type'),
            network_type_id=request.POST.get('network'),
            quantity=request.POST.get('quantity'),
            screenshot=request.FILES.get('screenshot'),
            time=datetime.now(),
        )
        return redirect('/')
    
def GetQRLink(request):
    option_id = request.GET.get('option_id')
    option = NetworkModel.objects.get(pk=option_id)
    image_url = option.qrcode.url
    return JsonResponse({'image_url': image_url,'link_name': option.link_name,'link_address':option.link_address})

@login_required(login_url='/account/login/')
def Account(request):
    user = User.objects.get(id = request.user.id)
    user.id = user.id.hex[:6]
    try:
        coin = CoinModel.objects.get(customer_id = request.user.id)
    except Exception as e:
        coin = None
    return render(request,'account.html',{"user":user,"coin":coin})


# @login_required(login_url='/account/login/')
def RoomChoice(request):
    user = User.objects.get(id = request.user.id)
    try:
        coin = CoinModel.objects.get(customer_id = request.user.id)
        return render(request,'room_choice.html',{"user":user,"b":coin.quantity})
    except Exception as e:
        coin = None
        return render(request,"room_choice.html",{"user":user,"b": 0})

def NewMember(request):
    ran = RandomModel.objects.get(status="now")
    current_user = User.objects.get(email = request.user.email)
    roundno = ran.roundno
    history = RandomModel.objects.filter(status="used").order_by("-id")[:5] 
    dh = RandomModel.objects.filter(status="used").order_by("-id")[5:]
    balance = CoinModel.objects.get(customer=current_user.id)

    for d in dh:
        d.delete()

    uhistroy = ""
    uh = []
    try:
        uhistroy = UserChoiceModel.objects.filter(user=current_user.id).order_by("-id")
    except:
        uhistroy = "No history" 

    if len(uhistroy) > 5:
        uh = list(uhistroy)[:5]
    else:
        uh = list(uhistroy)

    context={"roundno":roundno,"histroy":history,"b":balance.quantity,"uh":uh}
    return render(request,"new_member.html",context)

