from django.shortcuts import render,redirect
import random
from customer.models import *
from account.models import User

def RandomCreate(request):
    a = random.randint(1,10)
    b = random.randint(1,10)
    c = random.randint(1,10)
    r = RandomModel.objects.all().last()
    ran = RandomModel.objects.create(
        a = a,
        b = b,
        c = c,
        room = 1,
        status = "free",
        roundno = int(str(r.roundno)) + 1,
        total = a + b + c
        )
    ran.save()

    UserResult()
    ran2 = RandomModel.objects.get(status="now",room=1)
    ran2.status = "used"
    ran2.save()
    
    ran = RandomModel.objects.filter(status="free",room=1).first()
    ran.status = "now"
    ran.save()

    return redirect('/app/new_member/')    

def UserChoice(request,uc,am):
    current_user = User.objects.get(email = request.user.email)
    ran = RandomModel.objects.get(status="now")
    uc = UserChoiceModel.objects.create(
            choice = uc,
            amount = am,
            room = 1,
            roundno = ran.roundno,
            user = current_user
        )
    uc.save()
    coin = CoinModel.objects.get(customer=uc.user.id)
    coin.quantity =  coin.quantity - int(uc.amount)
    coin.save()
    return redirect('/customer/new_member/')

def UserChoiceHistroy(request):
    current_user = User.objects.get(email = request.user.email)
    uc = UserChoiceModel.objects.filter(user=current_user)
    return render(request,'userhistroy.html',{"uc":uc})

def UserResult():
    ran = RandomModel.objects.get(status="now",room=1)
    if ran.total <= 13:
        bb = "bear"
    else:
        bb = "bull"

    if ran.total % 2 ==0:
        ts = "twin"
    else:
        ts = "single"

    ucs = UserChoiceModel.objects.filter(roundno=ran.roundno,result="pending")
    for uc in ucs:
        if uc.choice == bb or uc.choice == ts:
            win = uc.amount * 0.9
            coin = CoinModel.objects.get(customer=uc.user.id)
            coin.quantity =  coin.quantity + win
            coin.save()
            uc.result = "success"
            uc.save()
        else:
            uc.result = "failed"
            uc.save()
