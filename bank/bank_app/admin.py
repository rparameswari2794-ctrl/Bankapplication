# bank_app/admin.py
from django.contrib import admin
from .models import BankApplication

@admin.register(BankApplication)
class BankApplicationAdmin(admin.ModelAdmin):
    # Display these fields in the list view
    list_display = (
        'id', 
        'first_name', 
        'last_name', 
        'email', 
        'mobile_number',
        'account_type', 
        'submitted_at'
    )
    
    # Add search functionality
    search_fields = (
        'first_name', 
        'last_name', 
        'email', 
        'mobile_number',
        'pan_number', 
        'aadhaar_number'
    )
    
    # Add filters
    list_filter = (
        'account_type', 
        'income_range', 
        'submitted_at'
    )
    
    # Make fields read-only
    readonly_fields = ('submitted_at',)  # Removed 'id' as it's auto-managed
    
    # Set default ordering
    ordering = ('-submitted_at',)
    
    # Fields to display in detail view - REMOVED non-existent fields
    fieldsets = (
        ('Personal Information', {
            'fields': ('first_name', 'last_name', 'email', 'mobile_number')  # Removed 'alternate_mobile_number'
        }),
        ('Address Details', {
            'fields': ('address_line1', 'city', 'state', 'pincode')
        }),
        ('Account Details', {
            'fields': ('account_type', 'occupation', 'income_range')
        }),
        ('Nominee Details', {
            'fields': ('nominee_name', 'nomination_relation', 'nominee_dob')  # Removed 'nominee_contact'
        }),
        ('Identity Proofs', {
            'fields': ('pan_number', 'aadhaar_number', 'voter_id', 'driving_license')
        }),
        ('Documents', {
            'fields': ('pan_card_image', 'aadhaar_front_image', 'passport_photo')  # Removed 'signature'
        }),
        ('Submission Info', {
            'fields': ('submitted_at', 'agree_terms'),  # Removed 'id'
            'classes': ('collapse',)
        }),
    )