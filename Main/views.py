from django.shortcuts import render,redirect
from django.contrib.auth import authenticate, login
from .forms import *
from django.contrib.auth.decorators import login_required
from .models import * 
from django.contrib import messages
from decimal import Decimal , InvalidOperation
from plotly.offline import plot
import plotly.graph_objs as go
from django.db.models import Sum
from django.shortcuts import get_object_or_404
from django.db.models.functions import Coalesce
from django.db.models import F, ExpressionWrapper, fields
from django.db.models.functions import TruncDate

def coslogin(request):
    # Check if the user is already authenticated
    if request.user.is_authenticated:
        return redirect('mainpage')  # Redirect to main page if already authenticated

    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('mainpage')
    else:
        form = LoginForm()
    return render(request, 'coslogin.html', {'form': form})


@login_required
def mainpage(request):
    # Retrieve user-specific data for display on the main page
    user = request.user
    user = User.objects.get(username=user)  # Replace 'username' with the actual username

# Retrieve the associated user profile
    user_profile = Userprofile.objects.get(user=user)

    
    balance = user_profile.balance
    
    # Retrieve user-specific content based on the user, e.g., user.posts.all()

    # Pass the user and user-specific content to the template
    return render(request, 'mainpage.html', {'user': user,'balance':balance })

@login_required
def set_balance(request):
    try:
        # Try to retrieve the user's Userprofile
        user_profile = Userprofile.objects.get(user=request.user)
        created = False
    except Userprofile.DoesNotExist:
        # If Userprofile doesn't exist, create a new one with a default balance
        user_profile = Userprofile.objects.create(user=request.user, balance=0.0)
        created = True

    if request.method == 'POST':
        form = BalanceForm(request.POST, instance=user_profile)
        if form.is_valid():
            # Delete existing transactions for the user
            BalanceTransaction.objects.filter(user=request.user).delete()
            HisTransction.objects.filter(user=request.user).delete()
            Masrif.objects.filter(user=request.user).delete()
            # Save the form to update the balance
            form.save()
            messages.success(request, 'Balance updated successfully.')
            return redirect('mainpage')
    else:
        form = BalanceForm(instance=user_profile)

    return render(request, 'set_balance.html', {'form': form ,})


@login_required
def add_transaction(request):
    if request.method == 'POST':
        form = TransactionForm(request.POST)
        if form.is_valid():
            transaction = form.save(commit=False)
            transaction.user = request.user
            transaction.save()
            update_balance(request)  # Pass the request object
            messages.success(request, 'Transaction recorded successfully.')
            return redirect('mainpage')
    else:
        form = TransactionForm()
    return render(request, 'add_transaction.html', {'form': form})







@login_required
def update_balance(request):
    transactions = BalanceTransaction.objects.filter(user=request.user)
    balance = Decimal('0.0')  # Use Decimal for consistency
    for transaction in transactions:
        balance += transaction.amount

    # Assuming Userprofile is your custom user model
    user_profile, _ = Userprofile.objects.get_or_create(user=request.user)
    user_profile.balance = balance
    user_profile.save() 
    
    
    
@login_required
def increase_balance(request):
    if request.method == 'POST':
        amount = request.POST.get('amount')
        unit = request.POST.get('unit')
        souscategorie = request.POST.get('souscat')
        try:
            amount_decimal = Decimal(amount)
            if amount_decimal > 0:
                user_profile = Userprofile.objects.get(user=request.user)
                user_profile.balance += amount_decimal
                user_profile.save()
                transaction = HisTransction.objects.create(
                    amount=amount_decimal,
                    categorie=unit,  # Adjust this based on your application logic
                    souscategorie=souscategorie,  # Adjust this based on your application logic
                    descrption=f"Increase balance by {amount_decimal}",
                    date=timezone.now(),
                    user=request.user
                )
                transaction.save()
                

                return redirect('increase_balance')
            else:
                messages.error(request, 'Invalid amount. Please enter a positive number.')
        except InvalidOperation:
            messages.error(request, 'Invalid amount. Please enter a valid number.')
        
        
    units = Categorie.objects.filter(user=request.user)
    souscat = SousCategorie.objects.filter(user=request.user)
    historique = HisTransction.objects.filter(user=request.user) 
    walita = Userprofile.objects.filter(user=request.user) 
    return render(request, 'increase_balance.html' , {'units': units , 'souscat':souscat , 'historique':historique , 'walita':walita})


@login_required
def decrease_balance(request):
    if request.method == 'POST':
        amount = request.POST.get('amount')
        unit = request.POST.get('unit') 
        souscategorie = request.POST.get('souscat')
        try:
            amount_decimal = Decimal(amount)
            if amount_decimal > 0:
                user_profile = Userprofile.objects.get(user=request.user)
                user_profile.balance -= amount_decimal
                user_profile.save()
                transaction = HisTransction.objects.create(
                    amount=amount_decimal*-1,
                    categorie=unit,  # Adjust this based on your application logic
                    souscategorie=souscategorie,  # Adjust this based on your application logic
                    descrption=f"Increase balance by {amount_decimal}",
                    date=timezone.now(),
                    user=request.user
                )
                transaction.save()
  
                messages.success(request, f'Balance decreased by {amount_decimal}.')
                return redirect('decrease_balance')
            else:
                messages.error(request, 'Invalid amount. Please enter a positive number.')
        except InvalidOperation:
            messages.error(request, 'Invalid amount. Please enter a valid number.')
    units = Categorie.objects.filter(user=request.user)
    souscat = SousCategorie.objects.filter(user=request.user)
    historique = HisTransction.objects.filter(user=request.user) 
    walita = Userprofile.objects.filter(user=request.user) 

    return render(request, 'decrease_balance.html' , {'units': units , 'souscat':souscat ,'historique':historique , 'walita':walita}) 


@login_required
def add_unit(request):
    if request.method == 'POST':
        form = UnitForm(request.POST)
        if form.is_valid():
            unit = form.save(commit=False)  # Create a unit object without saving to the database
            unit.user = request.user  # Set the user to the currently logged-in user
            unit.save()  # Save the unit with the user
            # Optionally, you can add a success message here
            return redirect('add_unit')  # Replace 'mainpage' with the appropriate URL
    else:
        form = UnitForm()
    categories = Categorie.objects.filter(user=request.user)


    return render(request, 'add_unit.html', {'form': form , 'categories':categories}) 


@login_required
def add_scategorie(request):
    if request.method == 'POST':
        form = SouscategorieForm(request.POST)
        if form.is_valid():
            unit = form.save(commit=False)  # Create a unit object without saving to the database
            unit.user = request.user  # Set the user to the currently logged-in user
            unit.save()  # Save the unit with the user
            # Optionally, you can add a success message here
            return redirect('add_scategorie')  # Replace 'mainpage' with the appropriate URL
    else:
        form = SouscategorieForm()
    
    souscategories = SousCategorie.objects.filter(user=request.user)

    return render(request, 'add_souscat.html', {'form': form , 'souscategories':souscategories}) 

def dashboard(request):
    # Retrieve data for negative amounts, grouped by category
    user_transactions = Masrif.objects.filter(user=request.user)
    category_sums = user_transactions.values('categorie').annotate(category_sum=Sum('amount'))
    category_sums = [{'categorie': entry['categorie'], 'category_sum': round(entry['category_sum'], 3) if entry['category_sum'] is not None else 0} for entry in category_sums]

    daily_amount_sums = user_transactions.annotate(transaction_date=TruncDate('date')).values('transaction_date').annotate(daily_amount_sum=Sum('amount'))
    daily_amount_sums = [{'date': entry['transaction_date'], 'daily_amount_sum': round(entry['daily_amount_sum'], 3) if entry['daily_amount_sum'] is not None else 0} for entry in daily_amount_sums]

    return render(request, 'dashboard.html', {'category_sums':category_sums , 'daily_amount_sums':daily_amount_sums})

def delete_categorie(request, categorie_id):
    categorie = get_object_or_404(Categorie, id=categorie_id)
    categorie.delete()
    return redirect('add_unit')

def delete_souscategorie(request, souscategorie_id):
    categorie = get_object_or_404(SousCategorie, id=souscategorie_id)
    categorie.delete()
    return redirect('add_scategorie')


def delete_his_i(request, his_id):
    his = get_object_or_404(HisTransction, id=his_id)
    if his.amount > 0 :
        user_profile = Userprofile.objects.get(user=request.user)
        user_profile.balance -= his.amount
    elif his.amount < 0 : 
        user_profile = Userprofile.objects.get(user=request.user)
        user_profile.balance += his.amount
        user_profile.save()
        
    his.delete()
    return redirect('increase_balance') 

def delete_his_d(request, his_id):
    his = get_object_or_404(HisTransction, id=his_id)
    print(his)
    if his.amount > 0 :
        user_profile = Userprofile.objects.get(user=request.user)
        user_profile.balance -= his.amount
    elif his.amount < 0 : 
        user_profile = Userprofile.objects.get(user=request.user)
        user_profile.balance += his.amount
        user_profile.save()
        print('ok')
        
    his.delete()
    return redirect('decrease_balance')