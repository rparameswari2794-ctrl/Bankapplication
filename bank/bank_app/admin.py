# bank_app/admin.py
from django.contrib import admin
from .models import BankApplication

@admin.register(BankApplication)
class BankApplicationAdmin(admin.ModelAdmin):
    list_display = (
        'id', 
        'first_name', 
        'last_name', 
        'email', 
        'mobile_number',
        'alternate_mobile_number',
        'account_type', 
        'submitted_at'
    )
    
    search_fields = (
        'first_name', 
        'last_name', 
        'email', 
        'mobile_number',
        'alternate_mobile_number',
        'pan_number', 
        'aadhaar_number'
    )
    
    list_filter = (
        'account_type', 
        'income_range', 
        'submitted_at'
    )
    
    readonly_fields = ('submitted_at',)
    ordering = ('-submitted_at',)
    
    fieldsets = (
        ('Personal Information', {
            'fields': ('first_name', 'last_name', 'email', 'mobile_number', 'alternate_mobile_number')
        }),
        ('Address Details', {
            'fields': ('address_line', 'city', 'state', 'pincode')
        }),
        ('Account Details', {
            'fields': ('account_type', 'occupation', 'income_range')
        }),
        ('Nominee Details', {
            'fields': ('nominee_name', 'nomination_relation', 'nominee_dob')  # Removed nominee_contact
        }),
        ('Identity Proofs', {
            'fields': ('pan_number', 'aadhaar_number', 'voter_id', 'driving_license')
        }),
        ('Documents', {
            'fields': ('pan_card_image', 'aadhaar_card', 'passport_photo', 'signature')  # Changed to aadhaar_card
        }),
        ('Submission Info', {
            'fields': ('submitted_at', 'agree_terms'),
            'classes': ('collapse',)
        }),
    )