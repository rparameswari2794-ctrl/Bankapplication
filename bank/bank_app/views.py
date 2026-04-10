# bank_app/views.py
from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponse
from django.conf import settings
from .forms import BankApplicationForm
from .models import BankApplication
import re
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet

def home(request):
    """Home page with form"""
    if request.method == "POST":
        form = BankApplicationForm(request.POST, request.FILES)
        if form.is_valid():
            app = form.save()
            # Redirect to success page
            return redirect('success')
        else:
            return render(request, 'bank_app/application_form.html', {'form': form})
    else:
        form = BankApplicationForm()
    return render(request, 'bank_app/application_form.html', {'form': form})

def success_page(request):
    """Success page - shows after form submission"""
    try:
        # Get the latest application
        app = BankApplication.objects.latest('id')
        return render(request, 'bank_app/success.html', {'app': app})
    except BankApplication.DoesNotExist:
        return redirect('/')

def ai_suggestion_api(request):
    """AI API for real-time form suggestions"""
    if request.method != "POST":
        return JsonResponse({"error": "Invalid request"}, status=400)
    
    field = request.POST.get("field")
    value = request.POST.get("value", "").strip()
    suggestion = ""
    details = ""
    
    # AI-Powered suggestions for each field
    if field in ["first_name", "last_name", "nominee_name"]:
        if value and value.isalpha():
            suggestion = "✅ Looks good! Use capital letters as per ID proof."
            details = f"Formatted: {value.capitalize()}"
        elif value:
            suggestion = "⚠️ Only letters allowed. Remove numbers or special characters."
            details = "Example: John"
        else:
            suggestion = "❌ This field is required"
            details = "Please enter your full name as per PAN card"
    
    elif field == "email":
        if re.match(r'^[\w\.-]+@[\w\.-]+\.\w+$', value):
            suggestion = "✅ Valid email format!"
            details = "Email will be used for account notifications"
        elif value:
            suggestion = "⚠️ Invalid email format"
            details = "Example: yourname@example.com"
        else:
            suggestion = "❌ Email is required"
            details = "We'll send account updates to this email"
    
    elif field == "mobile_number":
        if re.match(r'^[6-9]\d{9}$', value):
            suggestion = "✅ Valid mobile number!"
            details = "OTP will be sent to this number for verification"
        elif value:
            suggestion = "⚠️ Invalid mobile number"
            details = "Must be 10 digits starting with 6,7,8, or 9"
        else:
            suggestion = "❌ Mobile number is required"
            details = "Required for account verification"
    
    elif field == "pincode":
        if re.match(r'^\d{6}$', value):
            suggestion = "✅ Valid pincode!"
            details = "Location verified"
        elif value:
            suggestion = "⚠️ Invalid pincode"
            details = "Pincode must be exactly 6 digits"
        else:
            suggestion = "❌ Pincode is required"
            details = "Enter your area's 6-digit postal code"
    
    elif field == "pan_number":
        if re.match(r'^[A-Z]{5}[0-9]{4}[A-Z]$', value.upper()):
            suggestion = "✅ Valid PAN Card!"
            details = f"Format: {value[:5]}****{value[9]}"
        elif value:
            suggestion = "⚠️ Invalid PAN format"
            details = "Format: ABCDE1234F (5 letters, 4 digits, 1 letter)"
        else:
            suggestion = "❌ PAN Card number is required"
            details = "Mandatory for KYC compliance"
    
    elif field == "aadhaar_number":
        clean = re.sub(r'\s', '', value)
        if re.match(r'^\d{12}$', clean):
            formatted = f"{clean[:4]} {clean[4:8]} {clean[8:12]}"
            suggestion = "✅ Valid Aadhaar Number!"
            details = f"Formatted: {formatted}"
        elif clean:
            suggestion = "⚠️ Invalid Aadhaar number"
            details = "Must be 12 digits (no spaces or letters)"
        else:
            suggestion = "❌ Aadhaar number is required"
            details = "Required for identity verification"
    
    elif field == "voter_id":
        if not value:
            suggestion = "ℹ️ Optional field"
            details = "Can be provided for additional verification"
        elif re.match(r'^[A-Z]{3}[0-9]{7}$', value.upper()):
            suggestion = "✅ Valid Voter ID format!"
            details = "Optional but helpful for verification"
        else:
            suggestion = "⚠️ Invalid Voter ID format"
            details = "Format: ABC1234567 (3 letters, 7 digits)"
    
    elif field == "driving_license":
        if not value:
            suggestion = "ℹ️ Optional field"
            details = "Can be used as additional ID proof"
        elif re.match(r'^[A-Z]{2}[0-9]{13}$', value.upper()):
            suggestion = "✅ Valid Driving License format!"
            details = "Valid for address proof"
        else:
            suggestion = "⚠️ Invalid format"
            details = "Format: TN1234567890123 (2 letters, 13 digits)"
    
    else:
        suggestion = "✅ Looks good!" if value else "⚠️ This field is recommended"
        details = "Fill this field to complete your application"
    
    return JsonResponse({
        "suggestion": suggestion,
        "details": details,
        "field": field
    })

def download_pdf(request, app_id):
    """Generate and download PDF summary"""
    try:
        app = BankApplication.objects.get(id=app_id)
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="bank_application_{app.id}.pdf"'
        
        doc = SimpleDocTemplate(response)
        styles = getSampleStyleSheet()
        content = []
        
        # Title
        content.append(Paragraph("Bank Account Application Summary", styles['Title']))
        content.append(Spacer(1, 12))
        
        # Personal Details
        content.append(Paragraph("<b>Personal Information</b>", styles['Heading2']))
        content.append(Paragraph(f"Name: {app.first_name} {app.last_name}", styles['Normal']))
        content.append(Paragraph(f"Email: {app.email}", styles['Normal']))
        content.append(Paragraph(f"Mobile: {app.mobile_number}", styles['Normal']))
        if app.alternate_mobile_number:
            content.append(Paragraph(f"Alternate Mobile: {app.alternate_mobile_number}", styles['Normal']))
        content.append(Paragraph(f"Address: {app.address_line}, {app.city}, {app.state} - {app.pincode}", styles['Normal']))
        content.append(Spacer(1, 10))
        
        # Account Details
        content.append(Paragraph("<b>Account Details</b>", styles['Heading2']))
        content.append(Paragraph(f"Account Type: {app.account_type}", styles['Normal']))
        content.append(Paragraph(f"Occupation: {app.occupation}", styles['Normal']))
        content.append(Paragraph(f"Income Range: {app.income_range}", styles['Normal']))
        content.append(Spacer(1, 10))
        
        # Nominee Details
        content.append(Paragraph("<b>Nominee Information</b>", styles['Heading2']))
        content.append(Paragraph(f"Nominee: {app.nominee_name}", styles['Normal']))
        content.append(Paragraph(f"Relationship: {app.nomination_relation}", styles['Normal']))
        content.append(Paragraph(f"DOB: {app.nominee_dob}", styles['Normal']))
        content.append(Spacer(1, 10))
        
        # ID Proofs
        content.append(Paragraph("<b>Identity Proofs</b>", styles['Heading2']))
        content.append(Paragraph(f"PAN: {app.pan_number}", styles['Normal']))
        content.append(Paragraph(f"Aadhaar: {app.aadhaar_number}", styles['Normal']))
        if app.voter_id:
            content.append(Paragraph(f"Voter ID: {app.voter_id}", styles['Normal']))
        if app.driving_license:
            content.append(Paragraph(f"Driving License: {app.driving_license}", styles['Normal']))
        
        doc.build(content)
        return response
    except Exception as e:
        return HttpResponse(f"Error generating PDF: {str(e)}")