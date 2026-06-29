"""
Recommendations Module

Generates actionable retention strategies based on customer profile and churn risk.
"""

def get_interventions(customer_data, churn_probability):
    """
    Generate actionable recommendations based on customer profile and churn risk.
    
    Args:
        customer_data (dict): Customer feature dictionary.
        churn_probability (float): Predicted churn probability (0-1).
    
    Returns:
        list of dict: Each dict contains 'issue', 'action', and 'impact'.
    """
    interventions = []
    
    # Contract type
    contract = customer_data.get('Contract', '')
    if contract == 'Month-to-month':
        interventions.append({
            'issue': 'Month-to-month contract (high churn risk)',
            'action': 'Offer 10% discount to switch to 1-year contract.',
            'impact': 'Reduces churn by ~20%'
        })
    
    # Tenure
    tenure = customer_data.get('tenure', 0)
    if tenure < 12:
        interventions.append({
            'issue': 'New customer (tenure < 12 months)',
            'action': 'Send welcome rewards or loyalty bonus.',
            'impact': 'Improves retention by ~15%'
        })
    
    # Monthly charges
    monthly_charges = customer_data.get('MonthlyCharges', 0)
    if monthly_charges > 80:
        interventions.append({
            'issue': 'High monthly charges',
            'action': 'Offer ₹830/month discount for 6 months.',
            'impact': 'Reduces churn by ~12%'
        })
    
    # Online security
    online_security = customer_data.get('OnlineSecurity', '')
    if online_security == 'No':
        interventions.append({
            'issue': 'No Online Security add-on',
            'action': 'Offer free Online Security for 3 months.',
            'impact': 'Increases satisfaction, reduces churn by ~8%'
        })
    
    # Payment method
    payment_method = customer_data.get('PaymentMethod', '')
    if payment_method == 'Electronic check':
        interventions.append({
            'issue': 'Electronic check payment (high churn risk)',
            'action': 'Offer ₹415 credit to switch to auto-pay.',
            'impact': 'Reduces churn by ~10%'
        })
    
    # Internet service with no security
    internet_service = customer_data.get('InternetService', '')
    if internet_service == 'Fiber optic' and online_security == 'No':
        interventions.append({
            'issue': 'Fiber optic without security',
            'action': 'Free fiber internet upgrade for 1 month.',
            'impact': 'Builds loyalty, reduces churn by ~5%'
        })
    
    # High risk overall
    if churn_probability > 0.7:
        interventions.append({
            'issue': 'High churn risk overall',
            'action': 'Priority support call within 24 hours.',
            'impact': 'Personalized outreach can reduce churn by ~25%'
        })
    
    # Partner/Dependents
    partner = customer_data.get('Partner', '')
    dependents = customer_data.get('Dependents', '')
    if partner == 'No' and dependents == 'No':
        interventions.append({
            'issue': 'Single customer (no family ties)',
            'action': 'Offer family plan or referral bonus.',
            'impact': 'Increases engagement, reduces churn by ~7%'
        })
    
    # If no interventions, return a default positive message
    if not interventions:
        interventions.append({
            'issue': 'Low risk customer',
            'action': 'Maintain current service quality.',
            'impact': 'Customer is likely to stay.'
        })
    
    return interventions