
import os
import requests
from dotenv import load_dotenv

load_dotenv()

def test_hunter_api():
    """Test Hunter.io API connection and search functionality."""
    
    print("\n" + "="*70)
    print("🧪 TESTING HUNTER.IO API")
    print("="*70 + "\n")
    
    # Check for API key
    api_key = os.getenv("HUNTER_API_KEY")
    
    if not api_key:
        print("❌ ERROR: HUNTER_API_KEY not found in .env file")
        print("\n💡 To fix this:")
        print("   1. Sign up at https://hunter.io")
        print("   2. Get your API key from https://hunter.io/api_keys")
        print("   3. Add it to your .env file:")
        print("      HUNTER_API_KEY=your_api_key_here\n")
        return False
    
    print(f"✅ API Key found: {api_key[:10]}...{api_key[-4:]}")
    print()
    
    # Test 1: Account Information
    print("📊 Test 1: Checking account information...")
    try:
        response = requests.get(
            "https://api.hunter.io/v2/account",
            params={"api_key": api_key},
            timeout=10
        )
        response.raise_for_status()
        data = response.json()
        
        if data.get('data'):
            account = data['data']
            print(f"✅ Account active!")
            print(f"   Email: {account.get('email', 'N/A')}")
            print(f"   Plan: {account.get('plan_name', 'N/A')}")
            print(f"   Requests used: {account.get('requests', {}).get('used', 0)}/{account.get('requests', {}).get('available', 0)}")
            print()
        else:
            print("⚠️  Could not retrieve account info")
            print()
            
    except Exception as e:
        print(f"❌ Error checking account: {e}\n")
        return False
    
    # Test 2: Domain Search for a well-known company
    print("📊 Test 2: Testing domain search with 'Google'...")
    try:
        response = requests.get(
            "https://api.hunter.io/v2/domain-search",
            params={
                "company": "Google",
                "api_key": api_key,
                "limit": 3
            },
            timeout=10
        )
        response.raise_for_status()
        data = response.json()
        
        if data.get('data') and data['data'].get('domain'):
            print(f"✅ Found domain: {data['data']['domain']}")
            print(f"   Organization: {data['data'].get('organization', 'N/A')}")
            
            emails = data['data'].get('emails', [])
            print(f"   Sample contacts found: {len(emails)}")
            
            if emails:
                print("\n   Sample contact:")
                sample = emails[0]
                print(f"   - Name: {sample.get('first_name', '')} {sample.get('last_name', '')}")
                print(f"   - Email: {sample.get('value', 'N/A')}")
                print(f"   - Position: {sample.get('position', 'N/A')}")
                print(f"   - Confidence: {sample.get('confidence', 0)}%")
            print()
        else:
            print("⚠️  No results found for Google")
            print()
            
    except Exception as e:
        print(f"❌ Error in domain search: {e}\n")
        return False
    
    # Test 3: Try user's target company
    print("📊 Test 3: Enter a company name to search:")
    company = input("   Company name (or press Enter to skip): ").strip()
    
    if company:
        print(f"\n🔍 Searching for '{company}'...")
        try:
            response = requests.get(
                "https://api.hunter.io/v2/domain-search",
                params={
                    "company": company,
                    "api_key": api_key,
                    "limit": 5
                },
                timeout=10
            )
            response.raise_for_status()
            data = response.json()
            
            if data.get('data') and data['data'].get('domain'):
                domain = data['data']['domain']
                print(f"✅ Found domain: {domain}")
                
                emails = data['data'].get('emails', [])
                print(f"✅ Found {len(emails)} contacts")
                
                if emails:
                    print("\n📧 Contacts:")
                    for idx, email in enumerate(emails[:5], 1):
                        print(f"\n   [{idx}] {email.get('first_name', '')} {email.get('last_name', '')}")
                        print(f"       Email: {email.get('value', 'N/A')}")
                        print(f"       Position: {email.get('position', 'N/A')}")
                        print(f"       Confidence: {email.get('confidence', 0)}%")
                else:
                    print(f"⚠️  No contacts found at {domain}")
                    print("   This company might have email privacy settings enabled")
                print()
            else:
                print(f"❌ Could not find domain for '{company}'")
                print("💡 Try using the exact company name as shown on their website\n")
                
        except Exception as e:
            print(f"❌ Error searching for company: {e}\n")
    
    print("="*70)
    print("✅ Hunter.io API test completed!")
    print("="*70 + "\n")
    
    return True


if __name__ == "__main__":
    success = test_hunter_api()
    
    if success:
        print("🎉 Your Hunter.io API is configured correctly!")
        print("You can now use the main application.\n")
    else:
        print("⚠️  Please fix the issues above before using the main application.\n")