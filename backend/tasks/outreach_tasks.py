from crewai import Task
import requests
import os
import json
import re

def get_company_domain(company_name, api_key):
    """
    Uses Hunter.io to find the actual domain for a company name.
    This is a free API call that doesn't consume credits.
    """
    url = "https://api.hunter.io/v2/domain-search"
    
    # Try the company parameter - Hunter will attempt to find the domain
    params = {
        "company": company_name,
        "api_key": api_key,
        "limit": 1
    }
    
    try:
        response = requests.get(url, params=params, timeout=15)
        
        if response.status_code == 200:
            data = response.json()
            if data.get('data') and data['data'].get('domain'):
                return data['data']['domain']
        
        # If that didn't work, try removing spaces and adding .com
        clean_name = company_name.lower().strip().replace(" ", "").replace("'", "").replace(",", "")
        return f"{clean_name}.com"
        
    except:
        # Fallback
        clean_name = company_name.lower().strip().replace(" ", "").replace("'", "").replace(",", "")
        return f"{clean_name}.com"


def find_contacts_hunter(company_name, role, limit=10):
    """
    Finds contacts using Hunter.io Domain Search API.
    Free tier: 50 searches/month (1 credit per 10 emails found)
    """
    print(f"\n{'='*70}")
    print(f"🔍 SEARCHING FOR CONTACTS VIA HUNTER.IO")
    print(f"{'='*70}")
    print(f"Company: {company_name}")
    print(f"Role: {role}")
    print(f"{'='*70}\n")
    
    hunter_api_key = os.getenv("HUNTER_API_KEY")

    if not hunter_api_key:
        print("❌ ERROR: HUNTER_API_KEY not found in .env file.")
        print("Sign up at https://hunter.io to get a free API key")
        print("Free tier: 50 searches/month\n")
        return []

    # If user already provided a domain (contains .), use it directly
    if "." in company_name and len(company_name.split(".")) > 1:
        company_domain = company_name.lower().strip()
        print(f"🔗 Using provided domain: {company_domain}")
    else:
        # Try to find the domain dynamically
        print(f"🔍 Looking up domain for: {company_name}")
        company_domain = get_company_domain(company_name, hunter_api_key)
        print(f"🔗 Resolved to domain: {company_domain}")
    
    # Hunter.io Domain Search endpoint
    url = "https://api.hunter.io/v2/domain-search"
    
    params = {
        "domain": company_domain,
        "api_key": hunter_api_key,
        "limit": min(limit, 10),
        "type": "personal"
    }
    
    # Add department filter if we can map the role
    if role:
        role_lower = role.lower()
        department = None
        
        if any(word in role_lower for word in ['data', 'analyst', 'analytics', 'engineer', 'developer', 'scientist']):
            department = 'it'
        elif any(word in role_lower for word in ['hr', 'people', 'talent', 'recruiter']):
            department = 'hr'
        elif any(word in role_lower for word in ['sales', 'account', 'business development']):
            department = 'sales'
        elif any(word in role_lower for word in ['marketing', 'brand', 'content']):
            department = 'marketing'
        elif any(word in role_lower for word in ['finance', 'accounting', 'controller']):
            department = 'finance'
        elif any(word in role_lower for word in ['support', 'customer success', 'service']):
            department = 'support'
        elif any(word in role_lower for word in ['ceo', 'cto', 'cfo', 'chief', 'executive', 'president', 'vp']):
            department = 'executive'
        
        if department:
            params['department'] = department
            print(f"🎯 Filtering by department: {department}")
    
    try:
        print(f"🌐 Making API request to Hunter.io...")
        
        response = requests.get(url, params=params, timeout=20)
        
        print(f"📡 Response Status Code: {response.status_code}")
        
        # Check for errors
        if response.status_code == 400:
            print(f"❌ Bad Request (400)")
            error_data = response.json()
            print(f"   Error: {error_data.get('errors', [{}])[0].get('details', 'Invalid request')}")
            return []
        elif response.status_code == 401:
            print(f"❌ Unauthorized (401) - Invalid API key")
            return []
        elif response.status_code == 429:
            print(f"❌ Rate limit exceeded (429)")
            print(f"   Free plan: 50 searches/month")
            return []
        elif response.status_code != 200:
            print(f"❌ HTTP Error: {response.status_code}")
            return []
        
        data = response.json()
        contacts = []
        
        if data.get('data') and data['data'].get('emails'):
            emails_data = data['data']['emails']
            domain = data['data'].get('domain', company_domain)
            organization = data['data'].get('organization', company_name)
            
            print(f"\n✅ Found {len(emails_data)} contacts from Hunter.io")
            print(f"   Domain: {domain}")
            print(f"   Organization: {organization}")
            print(f"{'='*70}\n")
            
            for idx, person in enumerate(emails_data, 1):
                if len(contacts) >= limit:
                    break
                
                first_name = person.get('first_name', '')
                last_name = person.get('last_name', '')
                name = f"{first_name} {last_name}".strip()
                
                if not name:
                    name = person.get('value', '').split('@')[0].replace('.', ' ').title()
                
                title = person.get('position', role or 'Not specified')
                email = person.get('value', '')
                confidence = person.get('confidence', 0)
                
                # Construct LinkedIn URL
                linkedin_url = person.get('linkedin', '')
                if not linkedin_url and first_name and last_name:
                    linkedin_url = construct_linkedin_url(name)
                
                if email:
                    contacts.append({
                        "name": name,
                        "title": title,
                        "email": email,
                        "linkedin": linkedin_url,
                        "confidence": confidence
                    })
                    
                    print(f"[{len(contacts)}] {name}")
                    print(f"     Title: {title}")
                    print(f"     Email: {email}")
                    print(f"     LinkedIn: {linkedin_url}")
                    print(f"     Confidence: {confidence}%")
                    print()
            
        else:
            print(f"\n❌ No contacts found for domain: {company_domain}")
            print(f"   Hunter.io may not have data for this company")
            print(f"   Try entering the exact domain (e.g., 'hpe.com')\n")
            
        print(f"{'='*70}")
        print(f"✅ Retrieved {len(contacts)} contacts from Hunter.io")
        print(f"{'='*70}\n")
        
        return contacts
        
    except Exception as e:
        print(f"❌ Error: {type(e).__name__}: {str(e)}\n")
        return []


def construct_linkedin_url(name):
    """Construct a LinkedIn profile URL from a name."""
    if not name:
        return ""
    
    name_clean = name.lower().strip()
    name_clean = re.sub(r'[^a-z\s-]', '', name_clean)
    parts = name_clean.split()
    
    if len(parts) >= 2:
        return f"https://linkedin.com/in/{parts[0]}-{parts[-1]}"
    elif len(parts) == 1:
        return f"https://linkedin.com/in/{parts[0]}"
    return ""


def create_outreach_task(agent, company_name, role, user_resume):
    """
    Creates an outreach task with REAL contacts from Hunter.io
    Agent will scrape LinkedIn profiles for personalization
    """
    print("\n" + "="*70)
    print("🚀 CREATING OUTREACH TASK WITH LINKEDIN SCRAPING")
    print("="*70)
    
    # Get real contacts using Hunter.io
    contacts = find_contacts_hunter(company_name, role, limit=5)
    
    if not contacts or len(contacts) == 0:
        print("❌ ERROR: No real contacts found from Hunter.io")
        print("Returning error task.\n")
        
        return Task(
            description=(
                f"No contacts were found for {company_name} via Hunter.io API.\n\n"
                "This usually means Hunter.io doesn't have email data for this company.\n"
                "Try entering the company's domain directly (e.g., 'hpe.com' instead of 'Hewlett Packard Enterprise')."
            ),
            expected_output='{"error": "No contacts found via Hunter.io"}',
            agent=agent
        )
    
    print(f"\n✅ USING {len(contacts)} REAL CONTACTS FROM HUNTER.IO:")
    print("="*70)
    for i, c in enumerate(contacts, 1):
        print(f"{i}. {c['name']:25} | {c['email']:30} | {c['title'][:40]}")
        print(f"   LinkedIn: {c['linkedin']}")
    print("="*70 + "\n")
    
    contacts_json_str = json.dumps(contacts, indent=2)
    
    return Task(
        description=(
            f"="*70 + "\n"
            f"STEP 1: SCRAPE LINKEDIN PROFILES\n"
            f"="*70 + "\n"
            f"You have {len(contacts)} REAL contacts (from Hunter.io).\n"
            f"For EACH contact with a LinkedIn URL, use the ScrapeWebsiteTool to scrape their profile.\n"
            f"Extract key information:\n"
            f"- Current role and responsibilities\n"
            f"- Previous experience and career path\n"
            f"- Skills and expertise areas\n"
            f"- Education background\n"
            f"- Recent posts or activities (if available)\n"
            f"- Any shared interests or connections\n\n"
            f"CONTACTS TO RESEARCH:\n"
            f"{contacts_json_str}\n\n"
            f"="*70 + "\n"
            f"STEP 2: ANALYZE CANDIDATE'S RESUME\n"
            f"="*70 + "\n"
            f"{user_resume}\n\n"
            f"="*70 + "\n"
            f"STEP 3: FIND CONNECTION POINTS\n"
            f"="*70 + "\n"
            f"For each contact, identify:\n"
            f"- Shared skills or technologies\n"
            f"- Similar career paths or interests\n"
            f"- Relevant projects from candidate's resume that match contact's work\n"
            f"- Common educational background or certifications\n"
            f"- Industry trends or challenges they both care about\n\n"
            f"="*70 + "\n"
            f"STEP 4: WRITE PERSONALIZED MESSAGES\n"
            f"="*70 + "\n"
            f"For EACH contact, write:\n\n"
            f"1. LinkedIn connection note (under 300 characters):\n"
            f"   - Reference something SPECIFIC from their LinkedIn profile\n"
            f"   - Mention a genuine connection point with candidate's background\n"
            f"   - Keep it warm, professional, and authentic\n"
            f"   - Example: 'Hi [Name], saw your work on [specific project/skill]. I've been "
            f"working on similar challenges with [relevant candidate experience]. Would love to connect!'\n\n"
            f"2. Cold email:\n"
            f"   - Compelling subject line that references their work\n"
            f"   - Personalized greeting using their name\n"
            f"   - First paragraph: Reference specific detail from their LinkedIn (project, post, skill)\n"
            f"   - Second paragraph: Connect it to candidate's relevant experience (2-3 specific skills/projects)\n"
            f"   - Third paragraph: Clear ask for 15-20 min informational chat\n"
            f"   - Professional signature with candidate's name from resume\n\n"
            f"CRITICAL RULES:\n"
            f"- Output exactly {len(contacts)} contacts\n"
            f"- Use EXACT names, emails, titles, and LinkedIn URLs from input\n"
            f"- Do NOT modify any contact information\n"
            f"- Base personalization on ACTUAL scraped LinkedIn data\n"
            f"- If scraping fails for a profile, use their title and company for personalization\n"
            f"- Make each message unique based on their specific background\n"
            f"- Extract candidate's name from resume for email signatures\n"
        ),
        expected_output=(
            f"A JSON array with EXACTLY {len(contacts)} objects.\n\n"
            "Format (raw JSON, no markdown code blocks):\n"
            "[\n"
            "  {\n"
            '    "name": "exact name from input",\n'
            '    "title": "exact title from input",\n'
            '    "linkedin": "exact LinkedIn URL from input",\n'
            '    "email": "exact email from input",\n'
            '    "linkedin_profile_summary": "brief summary of key findings from their profile (2-3 sentences)",\n'
            '    "connection_points": "specific connections between their profile and candidate background",\n'
            '    "linkedin_note": "personalized note under 300 chars referencing their profile",\n'
            '    "cold_email": "Subject: [compelling subject]\\n\\nDear [Name],\\n\\n[Paragraph 1: Reference their work]\\n\\n[Paragraph 2: Candidate relevant experience]\\n\\n[Paragraph 3: Request chat]\\n\\nBest regards,\\n[Candidate Name]"\n'
            "  }\n"
            "]\n\n"
            "IMPORTANT:\n"
            "- Copy name, title, linkedin, email EXACTLY as provided\n"
            "- Add linkedin_profile_summary and connection_points based on scraped data\n"
            "- Create personalized linkedin_note and cold_email using the research\n"
            "- Return ONLY the JSON array, no markdown formatting\n"
        ),
        agent=agent
    )
