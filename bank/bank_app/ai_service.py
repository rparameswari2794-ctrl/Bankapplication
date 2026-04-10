# ai_service.py - Complete Enhanced Version
import re

class AISuggestionService:
    
    # ============ PAN NUMBER VALIDATION ============
    @staticmethod
    def get_pan_suggestion(pan_value):
        """Validate PAN card and provide suggestions"""
        if not pan_value:
            return None
        
        pan_value = pan_value.upper().strip()
        
        if len(pan_value) == 10 and re.match(r'^[A-Z]{5}[0-9]{4}[A-Z]{1}$', pan_value):
            # Enhanced with PAN type detection
            pan_type = {
                'A': 'Association of Persons',
                'B': 'Body of Individuals',
                'C': 'Company',
                'F': 'Firm',
                'G': 'Government',
                'H': 'HUF (Hindu Undivided Family)',
                'L': 'Local Authority',
                'P': 'Person',
                'T': 'Trust'
            }
            entity_type = pan_type.get(pan_value[3], 'Individual')
            
            return {
                'type': 'success',
                'message': f'✅ Valid PAN Card!',
                'icon': 'fa-check-circle',
                'details': f'Type: {entity_type}',
                'pan_format': f'{pan_value[:5]}****{pan_value[9]}'
            }
        elif len(pan_value) == 10:
            return {
                'type': 'warning',
                'message': '⚠️ Invalid PAN format',
                'icon': 'fa-exclamation-triangle',
                'details': 'PAN should have: 5 letters → 4 digits → 1 letter',
                'example': 'Example: ABCDE1234F'
            }
        else:
            return {
                'type': 'error',
                'message': '❌ Invalid PAN number',
                'icon': 'fa-times-circle',
                'details': f'PAN must be exactly 10 characters (current: {len(pan_value)})'
            }
    
    # ============ AADHAAR NUMBER VALIDATION ============
    @staticmethod
    def get_aadhaar_suggestion(aadhaar_value):
        """Validate Aadhaar number and provide suggestions"""
        if not aadhaar_value:
            return None
        
        clean_aadhaar = re.sub(r'\s', '', aadhaar_value)
        
        if re.match(r'^\d{12}$', clean_aadhaar):
            formatted = f"{clean_aadhaar[:4]} {clean_aadhaar[4:8]} {clean_aadhaar[8:12]}"
            
            # Determine region (simplified mapping)
            region_map = {
                '1000': 'Delhi NCR', '2000': 'Mumbai', '3000': 'Chennai',
                '4000': 'Kolkata', '5000': 'Bangalore', '6000': 'Hyderabad',
                '7000': 'Pune', '8000': 'Ahmedabad', '9000': 'Jaipur'
            }
            region = region_map.get(clean_aadhaar[:4], 'India')
            
            return {
                'type': 'success',
                'message': '✅ Valid Aadhaar Number',
                'icon': 'fa-check-circle',
                'details': f'Formatted: {formatted}',
                'region': region
            }
        elif len(clean_aadhaar) == 12 and not clean_aadhaar.isdigit():
            return {
                'type': 'warning',
                'message': '⚠️ Invalid Aadhaar format',
                'icon': 'fa-exclamation-triangle',
                'details': 'Aadhaar should contain only numbers (0-9)'
            }
        else:
            return {
                'type': 'error',
                'message': '❌ Invalid Aadhaar number',
                'icon': 'fa-times-circle',
                'details': f'Aadhaar must be 12 digits (current: {len(clean_aadhaar)})'
            }
    
    # ============ INCOME SUGGESTIONS ============
    @staticmethod
    def get_income_suggestion(occupation, current_income=None):
        """Get income range suggestions based on occupation"""
        suggestions = {
            'salaried': {
                'ranges': ['25001-50000', '50001-100000', '100001-200000'],
                'message': '💼 Based on your employment type, consider:',
                'icon': 'fa-briefcase',
                'average': '₹50,000 - ₹80,000',
                'tip': 'Higher income improves loan eligibility'
            },
            'self_employed': {
                'ranges': ['50001-100000', '100001-200000', '200001-500000'],
                'message': '📈 Self-employed professionals typically report:',
                'icon': 'fa-chart-line',
                'average': '₹60,000 - ₹1,20,000',
                'tip': 'IT returns help verify income'
            },
            'business': {
                'ranges': ['100001-200000', '200001-500000', '500001+'],
                'message': '🏢 Business owners usually declare:',
                'icon': 'fa-building',
                'average': '₹1,00,000 - ₹3,00,000',
                'tip': 'GST registration adds credibility'
            },
            'student': {
                'ranges': ['0-25000'],
                'message': '🎓 Students typically have:',
                'icon': 'fa-graduation-cap',
                'average': '₹0 - ₹15,000',
                'tip': 'Parent/Guardian can be co-applicant'
            },
            'retired': {
                'ranges': ['25001-50000', '50001-100000'],
                'message': '👴 Retired individuals often report:',
                'icon': 'fa-user-graduate',
                'average': '₹30,000 - ₹60,000',
                'tip': 'Pension statement required'
            },
            'homemaker': {
                'ranges': ['0-25000', '25001-50000'],
                'message': '🏠 For homemakers, typical range is:',
                'icon': 'fa-home',
                'average': '₹0 - ₹30,000',
                'tip': 'Spouse income can be considered'
            }
        }
        
        data = suggestions.get(occupation, suggestions['salaried'])
        
        result = {
            'type': 'info',
            'message': data['message'],
            'icon': data['icon'],
            'suggested_ranges': data['ranges'],
            'average': data['average'],
            'tip': data['tip']
        }
        
        if current_income:
            result['current'] = current_income
        
        return result
    
    # ============ OCCUPATION SUGGESTIONS ============
    @staticmethod
    def get_occupation_suggestion(occupation_value):
        """Get occupation-specific document requirements and benefits"""
        suggestions = {
            'salaried': {
                'message': '💼 Salaried Employee - Documents needed:',
                'documents': [
                    'Salary slips (last 3 months)',
                    'Form 16 / Income Tax Returns',
                    'Employment offer letter',
                    'Bank statements (6 months)'
                ],
                'icon': 'fa-briefcase',
                'benefits': [
                    '✓ Easy approval process',
                    '✓ Higher loan eligibility',
                    '✓ Premium credit card offers',
                    '✓ Zero balance account option'
                ]
            },
            'self_employed': {
                'message': '📊 Self Employed - Documents needed:',
                'documents': [
                    'IT returns (last 2 years)',
                    'Business proof / Registration',
                    'Bank statements (12 months)',
                    'GST certificate (if applicable)'
                ],
                'icon': 'fa-chart-pie',
                'benefits': [
                    '✓ Business loan eligibility',
                    '✓ Overdraft facility',
                    '✓ Higher transaction limits',
                    '✓ Merchant services'
                ]
            },
            'business': {
                'message': '🏢 Business Owner - Documents needed:',
                'documents': [
                    'GST registration certificate',
                    'Business license / Shop act',
                    'IT returns (3 years)',
                    'MOA / AOA (for companies)',
                    'Partnership deed (for firms)'
                ],
                'icon': 'fa-building',
                'benefits': [
                    '✓ Business credit card',
                    '✓ Working capital loan',
                    '✓ Trade services',
                    '✓ Higher POS limits'
                ]
            },
            'student': {
                'message': '🎓 Student - Documents needed:',
                'documents': [
                    'College ID card',
                    'Bonafide certificate',
                    'Parent/Guardian KYC',
                    'Fee receipt (current year)'
                ],
                'icon': 'fa-graduation-cap',
                'benefits': [
                    '✓ Zero balance account',
                    '✓ Education loan eligibility',
                    '✓ Student discounts',
                    '✓ No minimum balance'
                ]
            },
            'retired': {
                'message': '👴 Retired - Documents needed:',
                'documents': [
                    'Pension statement',
                    'Retirement letter',
                    'Previous employer proof',
                    'Senior citizen ID (if available)'
                ],
                'icon': 'fa-user-graduate',
                'benefits': [
                    '✓ Senior citizen benefits',
                    '✓ Higher FD interest rates',
                    '✓ Free health checkup',
                    '✓ Priority banking'
                ]
            },
            'homemaker': {
                'message': '🏠 Homemaker - Documents needed:',
                'documents': [
                    'Spouse income proof',
                    'Family ID / Ration card',
                    'Address proof',
                    'Identity proof'
                ],
                'icon': 'fa-home',
                'benefits': [
                    '✓ Joint account option',
                    '✓ Family banking benefits',
                    '✓ Savings incentives',
                    '✓ Free debit card'
                ]
            }
        }
        
        data = suggestions.get(occupation_value, {
            'message': '📋 General Documents needed:',
            'documents': ['Identity proof', 'Address proof', 'Photograph', 'Income proof'],
            'icon': 'fa-folder-open',
            'benefits': ['✓ Standard banking services', '✓ ATM card', '✓ Net banking']
        })
        
        return {
            'type': 'info',
            'message': data['message'],
            'icon': data['icon'],
            'documents': data['documents'],
            'benefits': data.get('benefits', [])
        }
    
    # ============ ADDRESS VALIDATION ============
    @staticmethod
    def get_address_suggestion(address_value):
        """Validate address completeness and suggest improvements"""
        if not address_value:
            return None
        
        suggestions = []
        missing_fields = []
        
        # Check for house/flat number
        if not re.search(r'\d+', address_value):
            missing_fields.append("House/Flat number")
            suggestions.append("🏠 Add house/flat number")
        
        # Check for street/road
        if not re.search(r'(street|road|st|rd|nagar|layout|colony)', address_value.lower()):
            missing_fields.append("Street/Road name")
            suggestions.append("🛣️ Add street/road name")
        
        # Check for city
        cities = ['chennai', 'mumbai', 'delhi', 'bangalore', 'hyderabad', 'kolkata', 'pune', 'ahmedabad', 'jaipur']
        if not any(city in address_value.lower() for city in cities):
            missing_fields.append("City name")
            suggestions.append("🏙️ Add city name")
        
        # Check for pincode
        if not re.search(r'\d{6}', address_value):
            missing_fields.append("6-digit pincode")
            suggestions.append("📮 Add 6-digit pincode")
        
        # Check for state
        states = ['tamil nadu', 'maharashtra', 'karnataka', 'delhi', 'gujarat', 'west bengal', 
                  'rajasthan', 'uttar pradesh', 'telangana', 'kerala']
        if not any(state in address_value.lower() for state in states):
            missing_fields.append("State name")
            suggestions.append("🗺️ Add state name")
        
        # Calculate completeness score
        total_fields = 5
        filled_fields = total_fields - len(missing_fields)
        completeness = int((filled_fields / total_fields) * 100)
        
        if suggestions:
            return {
                'type': 'warning' if completeness < 60 else 'info',
                'message': f'📍 Address Completeness: {completeness}%',
                'icon': 'fa-map-marker-alt',
                'missing_fields': missing_fields,
                'suggestions': suggestions,
                'completeness': completeness
            }
        
        return {
            'type': 'success',
            'message': '✅ Complete address! Ready for verification.',
            'icon': 'fa-check-circle',
            'completeness': 100
        }
    
    # ============ ELIGIBILITY SCORE CALCULATION ============
    @staticmethod
    def get_eligibility_score(application_data):
        """Calculate eligibility score based on application data"""
        score = 0
        max_score = 100
        
        # Name validation (10 points)
        full_name = application_data.get('full_name', '')
        if len(full_name.split()) >= 2:
            score += 10
        elif full_name:
            score += 5
        
        # PAN validation (20 points)
        pan = application_data.get('pan_number', '')
        if re.match(r'^[A-Z]{5}[0-9]{4}[A-Z]{1}$', pan):
            score += 20
        elif pan:
            score += 5
        
        # Aadhaar validation (15 points)
        aadhaar = re.sub(r'\s', '', application_data.get('aadhaar_number', ''))
        if re.match(r'^\d{12}$', aadhaar):
            score += 15
        elif aadhaar:
            score += 5
        
        # Occupation (10 points)
        occupation = application_data.get('occupation', '')
        occupation_scores = {
            'salaried': 10, 'business': 10, 'self_employed': 10,
            'retired': 8, 'homemaker': 6, 'student': 5, 'other': 5
        }
        score += occupation_scores.get(occupation, 5)
        
        # Income (25 points)
        income = application_data.get('income_range', '')
        income_scores = {
            '0-25000': 10, '25001-50000': 15,
            '50001-100000': 20, '100001-200000': 23,
            '200001-500000': 25, '500001+': 25
        }
        score += income_scores.get(income, 0)
        
        # Address completeness (20 points)
        address = application_data.get('address', '')
        address_score = 0
        if re.search(r'\d+', address): address_score += 5
        if re.search(r'(street|road|nagar|layout)', address.lower()): address_score += 5
        if re.search(r'\d{6}', address): address_score += 5
        if any(city in address.lower() for city in ['chennai', 'mumbai', 'delhi', 'bangalore']):
            address_score += 5
        score += address_score
        
        # Determine eligibility tier
        if score >= 80:
            tier = "Premium"
            color = "success"
            message = "🏆 Excellent! You qualify for Premium Banking benefits."
            recommendations = ["Apply for Premium Credit Card", "Get higher loan limits", "Priority customer support"]
        elif score >= 60:
            tier = "Standard"
            color = "primary"
            message = "👍 Good! You qualify for Standard Banking account."
            recommendations = ["Eligible for credit card", "Standard loan limits", "Regular customer support"]
        elif score >= 40:
            tier = "Basic"
            color = "warning"
            message = "📋 Basic eligibility. Complete missing details for better benefits."
            recommendations = ["Submit complete documents", "Add income proof", "Verify address details"]
        else:
            tier = "Pending"
            color = "danger"
            message = "⚠️ Please provide all required documents for eligibility."
            recommendations = ["Fill all mandatory fields", "Upload valid ID proof", "Submit income documents"]
        
        return {
            'score': score,
            'max_score': max_score,
            'percentage': (score / max_score) * 100,
            'tier': tier,
            'color': color,
            'message': message,
            'recommendations': recommendations
        }
    
    # ============ NAME VALIDATION ============
    @staticmethod
    def get_name_suggestion(name_value):
        """Validate name format"""
        if not name_value:
            return None
        
        name_parts = name_value.strip().split()
        
        if len(name_parts) >= 2:
            formatted_name = ' '.join([part.capitalize() for part in name_parts])
            return {
                'type': 'success',
                'message': '✅ Valid name format',
                'icon': 'fa-check-circle',
                'details': f'Formatted: {formatted_name}',
                'tip': 'Ensure name matches PAN card exactly'
            }
        elif len(name_parts) == 1:
            return {
                'type': 'warning',
                'message': '⚠️ Please enter full name',
                'icon': 'fa-exclamation-triangle',
                'details': 'Add both first name and last name',
                'tip': 'Name should match your official ID'
            }
        else:
            return {
                'type': 'error',
                'message': '❌ Name is required',
                'icon': 'fa-times-circle',
                'details': 'Please enter your full name as per PAN card'
            }