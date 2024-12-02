from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from .models import Property, UserPreference
from .forms import PropertyForm, UserPreferenceForm
from django.core.mail import send_mail
from django.conf import settings
from django.contrib import messages
from .library import HomeLoan

def property_list(request):
    properties = Property.objects.all()

    # Filters
    location = request.GET.get('location')
    property_type = request.GET.get('property_type')
    price_min = request.GET.get('price_min')
    price_max = request.GET.get('price_max')

    filters = {}
    if location:
        filters['location__icontains'] = location
    if property_type:
        filters['property_type'] = property_type
    if price_min:
        filters['price__gte'] = price_min
    if price_max:
        filters['price__lte'] = price_max

    properties = properties.filter(**filters)

    # Sorting
    sort_by = request.GET.get('sort_by')
    if sort_by == 'price_asc':
        properties = properties.order_by('price')
    elif sort_by == 'price_desc':
        properties = properties.order_by('-price')
    elif sort_by == 'area_asc':
        properties = properties.order_by('area')
    elif sort_by == 'area_desc':
        properties = properties.order_by('-area')
    elif sort_by == 'newest':
        properties = properties.order_by('-created_at')

    return render(request, 'properties/property_list.html', {'properties': properties})

def property_detail(request, pk):
    property_instance = get_object_or_404(Property, pk=pk)
    
    # WhatsApp URL with a pre-filled message
    whatsapp_url = f"https://wa.me/{property_instance.owner.phone_number}?text=Hi, I am interested in your property titled '{property_instance.title}'. Can we discuss further?"

    return render(request, 'properties/property_detail.html', {
        'property': property_instance,
        'whatsapp_url': whatsapp_url
    })

@login_required
def add_property(request):
    if request.method == 'POST':
        form = PropertyForm(request.POST, request.FILES)
        if form.is_valid():
            property_instance = form.save(commit=False)
            property_instance.owner = request.user
            property_instance.save()

            # Notify users based on their preferences
            preferences = UserPreference.objects.filter(
                location__icontains=property_instance.location,
                property_type=property_instance.property_type,
                min_price__lte=property_instance.price,
                max_price__gte=property_instance.price
            )

            for preference in preferences:
                user = preference.user
                send_mail(
                    subject="New Property Matching Your Preferences",
                    message=f"Hi {user.username},\n\nA new property titled '{property_instance.title}' in {property_instance.location} matches your preferences. Check it out!",
                    from_email=settings.EMAIL_HOST_USER,
                    recipient_list=[user.email],
                    fail_silently=False,
                )

            messages.success(request, "Property added successfully, and notifications were sent.")
            return redirect('property_list')
    else:
        form = PropertyForm()
    return render(request, 'properties/add_property.html', {'form': form})

@login_required
def edit_property(request, pk):
    property_instance = get_object_or_404(Property, pk=pk, owner=request.user)
    if request.method == 'POST':
        form = PropertyForm(request.POST, request.FILES, instance=property_instance)
        if form.is_valid():
            form.save()
            messages.success(request, "Property updated successfully.")
            return redirect('property_list')
    else:
        form = PropertyForm(instance=property_instance)
    return render(request, 'properties/edit_property.html', {'form': form, 'property': property_instance})

@login_required
def delete_property(request, pk):
    property_instance = get_object_or_404(Property, pk=pk, owner=request.user)
    if request.method == 'POST':
        property_instance.delete()
        messages.success(request, "Property deleted successfully.")
        return redirect('property_list')
    return render(request, 'properties/delete_property.html', {'property': property_instance})

@login_required
def set_preferences(request):
    try:
        preference = request.user.preference
    except UserPreference.DoesNotExist:
        preference = None

    if request.method == 'POST':
        form = UserPreferenceForm(request.POST, instance=preference)
        if form.is_valid():
            user_preference = form.save(commit=False)
            user_preference.user = request.user
            user_preference.save()
            messages.success(request, "Preferences updated successfully.")
            return redirect('property_list')
    else:
        form = UserPreferenceForm(instance=preference)

    return render(request, 'properties/set_preferences.html', {'form': form})

@login_required
def notify_users(request):
    preferences = UserPreference.objects.all()
    for preference in preferences:
        user = preference.user
        send_mail(
            subject="New Properties Matching Your Preferences",
            message=f"Hi {user.username},\n\nNew properties have been added that match your preferences. Check them out!",
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[user.email],
            fail_silently=False,
        )
    messages.success(request, "Notifications sent successfully.")
    return redirect('property_list')

@login_required
def calculator(request):
    loan_obj = HomeLoan()
    emi = None
    max_loan_amount = None
    max_property_price = None
    total_payable = None
    total_interest = None
    if request.method == 'POST':
        if 'emi_calculate' in request.POST:
            loan_amount = float(request.POST.get('loan_amount', 0))
            annual_rate = float(request.POST.get('annual_rate', 0))
            tenure_years = int(request.POST.get('tenure_years', 0))
            emi = loan_obj.calculate_emi(loan_amount, annual_rate, tenure_years)
        elif 'eligibility_calculate' in request.POST:
            monthly_income = float(request.POST.get('monthly_income', 0))
            monthly_expenses = float(request.POST.get('monthly_expenses', 0))
            interest_rate = float(request.POST.get('interest_rate', 0))
            tenure_years = int(request.POST.get('tenure_years', 0))
            max_loan_amount, _, _, _, _ = loan_obj.calculate_eligibility(monthly_income, monthly_expenses, interest_rate, tenure_years)
        elif 'affordability_calculate' in request.POST:
            monthly_income = float(request.POST.get('monthly_income', 0))
            monthly_expenses = float(request.POST.get('monthly_expenses', 0))
            interest_rate = float(request.POST.get('interest_rate', 0))
            tenure_years = int(request.POST.get('tenure_years', 0))
            max_property_price, _, _, _, _ = loan_obj.calculate_affordability(monthly_income, monthly_expenses, interest_rate, tenure_years)
        elif 'total_payable_calculate' in request.POST:
            loan_amount = float(request.POST.get('loan_amount', 0))
            annual_rate = float(request.POST.get('annual_rate', 0))
            tenure_years = int(request.POST.get('tenure_years', 0))
            total_payable, total_interest, emi, _, _, _ = loan_obj.calculate_total_payable(tenure_years, annual_rate, loan_amount)

    return render(request, 'properties/calculator.html', {
        'emi': round(emi, 2) if emi else None,
        'max_loan_amount': round(max_loan_amount, 2) if max_loan_amount else None,
        'max_property_price': round(max_property_price, 2) if max_property_price else None,
        'total_payable': round(total_payable, 2) if total_payable else None,
        'total_interest': round(total_interest, 2) if total_interest else None,
    })

@login_required
def owner_dashboard(request):
    properties = Property.objects.filter(owner=request.user)
    return render(request, 'properties/owner_dashboard.html', {'properties': properties})
