"""
Script to create sample real estate documents for testing
"""

import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from app.config import settings


def create_sample_documents():
    """
    Create sample documents in the documents directory
    """
    docs_dir = settings.DOCS_DIR
    docs_dir.mkdir(parents=True, exist_ok=True)

    # Sample FAQ document
    faq_content = """
# Real Estate Buying FAQ

## What documents do I need to buy a property?

To purchase a property, you typically need:
1. Identity proof (Aadhaar, PAN, Passport)
2. Address proof
3. Income proof (salary slips, IT returns)
4. Bank statements for the last 6 months
5. Property documents from the seller

## What is the registration process?

Property registration involves:
1. Drafting the sale agreement
2. Paying stamp duty and registration fees
3. Visiting the sub-registrar office with both parties
4. Signing the documents in front of the registrar
5. Receiving the registered sale deed

## How do I verify property titles?

Title verification steps:
1. Check the title deed for the last 30 years
2. Verify encumbrance certificate from the registrar
3. Check for any pending loans or mortgages
4. Verify property tax receipts
5. Confirm property boundaries with survey records

## What are the common hidden costs?

Hidden costs in property buying:
1. Stamp duty (varies by state, typically 5-7%)
2. Registration fees (1-2%)
3. Legal verification charges
4. Home loan processing fees
5. Property insurance
6. Maintenance deposit

## What should I check before buying land?

Before buying land:
1. Verify land use zoning (residential, commercial, agricultural)
2. Check for clear title and ownership
3. Verify survey number and boundaries
4. Check for any litigation or disputes
5. Confirm water and electricity availability
6. Verify approval from local authorities
7. Check soil quality and topography
"""

    # Sample sale agreement
    sale_agreement_content = """
# Sample Sale Agreement

## PROPERTY DETAILS

Property Type: Residential Apartment
Location: Hyderabad, Telangana
Survey Number: 123/4/A
Total Area: 2400 sqft
Carpet Area: 1850 sqft
Floor: 5th Floor
Total Floors: 12

## AGREEMENT TERMS

1. Sale Price: INR 1,20,00,000 (One Crore Twenty Lakhs)
2. Token Amount: INR 5,00,000
3. Advance Payment: INR 25,00,000
4. Balance Payment: At the time of registration

## PAYMENT SCHEDULE

- Token: On signing this agreement
- 25%: Within 30 days
- 50%: Within 60 days
- Balance: At registration

## SELLER OBLIGATIONS

1. Provide clear title documents
2. Obtain necessary approvals and NOCs
3. Pay all outstanding property taxes
4. Vacate the property by agreed date
5. Transfer all utility connections

## BUYER OBLIGATIONS

1. Make payments as per schedule
2. Complete loan documentation if applicable
3. Pay stamp duty and registration fees
4. Take possession on agreed date

## CONDITIONS

1. This agreement is subject to title verification
2. Property should be free from all encumbrances
3. All approvals must be valid and current
4. Possession to be given within 90 days
"""

    # Sample property listing
    property_listing_content = """
# Property Listing Details

## PROPERTY ID: HYD-APT-2024-001

Location: Gachibowli, Hyderabad
Property Type: 3 BHK Apartment
Built-up Area: 1650 sqft
Floor: 8th of 15 floors
Age: 2 years
Parking: 2 covered slots
Facing: East

## AMENITIES

- 24/7 Security
- Swimming Pool
- Gymnasium
- Clubhouse
- Children's Play Area
- Power Backup
- Elevator
- Rainwater Harvesting

## PRICE DETAILS

Asking Price: INR 1,45,00,000
Price per sqft: INR 8,788
Maintenance: INR 3,500/month
Property Tax: INR 18,000/year

## CONTACT

Owner: Rajesh Kumar
Phone: +91-98765-43210
Email: rajesh@example.com
"""

    # Sample legal guide
    legal_guide_content = """
# Legal Guide for Property Buyers in Telangana

## DUE DILIGENCE CHECKLIST

### 1. Title Verification
- Check mother deed for last 30 years
- Verify chain of ownership
- Look for any gaps in title
- Check for inheritance or gift transfers

### 2. Encumbrance Certificate
- Apply for EC at sub-registrar office
- Check for last 13 years minimum
- Look for any mortgages or loans
- Verify no pending litigation

### 3. Property Documents to Verify
- Sale deed
- Gift deed (if applicable)
- Partition deed (if applicable)
- Release deed (if applicable)
- Power of attorney (if applicable)
- Will and probate (if applicable)

### 4. Land Use and Zoning
- Check master plan for the area
- Verify land use classification
- Confirm building approval
- Check for any acquisition notices

### 5. Tax Verification
- Check property tax receipts
- Verify water tax payments
- Check for any pending dues
- Confirm assessment number

## STAMP DUTY AND REGISTRATION

Current rates in Telangana:
- Stamp Duty: 4% for women, 5% for men
- Registration Fee: 0.5% of property value
- Transfer Fee: 1% of property value

## COMMON FRAUDS TO AVOID

1. Properties with disputed titles
2. Unauthorized constructions
3. Properties under litigation
4. Fake power of attorney
5. Benami transactions
6. Properties in prohibited zones
"""

    # Write sample documents
    samples = [
        ("faq_buying_guide.txt", faq_content),
        ("sale_agreement_sample.txt", sale_agreement_content),
        ("property_listing_sample.txt", property_listing_content),
        ("legal_guide_telangana.txt", legal_guide_content),
    ]

    for filename, content in samples:
        filepath = docs_dir / filename
        filepath.write_text(content.strip(), encoding="utf-8")
        print(f"Created: {filepath}")

    print(f"\nSample documents created in: {docs_dir}")
    print("Run the ingestion script to add these to the vector store.")


if __name__ == "__main__":
    create_sample_documents()