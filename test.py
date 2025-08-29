"""
COMPREHENSIVE AI FOUNDER DETECTION PIPELINE - FULLY SELF-CONTAINED VERSION
This script contains all configurations and can run independently
"""

import os
import sys
import json
import time
from datetime import datetime, timedelta
from typing import List, Dict, Any, Optional
from dotenv import load_dotenv

# Add project root to path
current_file = os.path.abspath(__file__)
project_root = os.path.dirname(current_file)
sys.path.insert(0, project_root)

# ============================================================================
# EMBEDDED CONFIGURATIONS - No external config files needed
# ============================================================================

# All US States (you can enable/disable any)
ALL_US_STATES = [
    # Major Tech Hubs (RECOMMENDED - High startup density)
    'california',      # Silicon Valley, SF, LA
    'new york',        # NYC tech scene
    'texas',           # Austin, Dallas, Houston
    'washington',      # Seattle (Amazon, Microsoft)
    'massachusetts',   # Boston/Cambridge (MIT, Harvard)
    
    # Secondary Tech Hubs (GOOD OPTIONS)
    'colorado',        # Denver/Boulder
    'illinois',        # Chicago
    'georgia',         # Atlanta
    'florida',         # Miami, Orlando
    'virginia',        # Northern VA (DC area)
    'north carolina',  # Raleigh-Durham
    'pennsylvania',    # Philadelphia, Pittsburgh
    
    # Business-Friendly States (INCORPORATION HUBS)
    'delaware',        # Most companies incorporate here
    'nevada',          # Tax benefits
    'wyoming',         # Privacy benefits
    
    # Emerging Tech Markets
    'utah',            # Salt Lake City
    'arizona',         # Phoenix
    'oregon',          # Portland
    'michigan',        # Detroit (auto tech)
    'minnesota',       # Minneapolis
    'tennessee',       # Nashville
    'maryland',        # Baltimore (cybersecurity)
    'new jersey',      # Close to NYC
    'connecticut',     # Finance tech
    'ohio',            # Columbus, Cincinnati
    
    # Other States (OPTIONAL - Lower startup density)
    'alabama', 'alaska', 'arkansas', 'hawaii', 'idaho', 
    'indiana', 'iowa', 'kansas', 'kentucky', 'louisiana',
    'maine', 'mississippi', 'missouri', 'montana', 'nebraska',
    'new hampshire', 'new mexico', 'north dakota', 'oklahoma',
    'rhode island', 'south carolina', 'south dakota', 'vermont',
    'west virginia', 'wisconsin'
]

# AI/ML Focused Companies (High Priority)
AI_FOCUSED_BIG_TECH = [
    # Pure AI Companies
    "openai",           # GPT, DALL-E
    "anthropic",        # Claude
    "deepmind",         # AlphaGo, AlphaFold
    "huggingface",      # ML models platform
    "cohere",           # LLMs
    "stability ai",     # Stable Diffusion
    "inflection ai",    # Personal AI
    "adept",            # AI agents
    "character ai",     # Conversational AI
    
    # Big Tech with Strong AI
    "google",           # Google AI, Bard
    "alphabet",         # Parent of Google
    "meta",             # Facebook AI Research
    "facebook",         # Legacy name
    "microsoft",        # OpenAI partner, Copilot
    "amazon",           # AWS AI, Alexa
    "apple",            # Siri, Core ML
    "nvidia",           # AI chips, CUDA
    "tesla",            # Autonomous driving
    "netflix",          # Recommendation systems
    "uber",             # ML for routing
    "linkedin",         # Owned by Microsoft
    "twitter",          # X.com
    "x",                # Twitter rebrand
    
    # AI Infrastructure
    "databricks",       # ML platform
    "scale ai",         # Data labeling
    "weights & biases", # ML tools
    "snorkel",          # Data programming
]

# Traditional Tech Companies
TRADITIONAL_BIG_TECH = [
    "oracle",           # Database, cloud
    "ibm",              # Watson AI
    "adobe",            # Creative AI
    "salesforce",       # CRM, Einstein AI
    "intel",            # AI chips
    "amd",              # GPUs
    "qualcomm",         # Mobile AI
    "cisco",            # Network AI
    "vmware",           # Virtualization
    "dell",             # Hardware
    "hp",               # Hardware
    "sap",              # Enterprise software
    "palantir",         # Data analytics
    "snowflake",        # Data warehouse
    "stripe",           # Payments
    "square",           # Block
    "block",            # Square rebrand
    "coinbase",         # Crypto
    "airbnb",           # Travel tech
    "doordash",         # Delivery
    "instacart",        # Grocery delivery
    "lyft",             # Rideshare
    "spotify",          # Music streaming
    "snap",             # Snapchat
    "pinterest",        # Visual discovery
    "reddit",           # Social platform
    "discord",          # Communication
    "slack",            # Work communication
    "zoom",             # Video conferencing
    "docusign",         # E-signatures
    "okta",             # Identity management
    "twilio",           # Communications API
    "shopify",          # E-commerce
    "roblox",           # Gaming platform
    "unity",            # Game engine
    "epic games",       # Unreal Engine
]

# AI/ML Job Roles to Track
AI_ML_ROLES = {
    'primary': [
        'research', 'engineering', 'product', 'data_science'
    ],
    'titles': [
        'research scientist', 'machine learning engineer', 'ml engineer',
        'ai researcher', 'deep learning engineer', 'data scientist',
        'computer vision engineer', 'nlp engineer', 'robotics engineer',
        'ai product manager', 'ml ops engineer', 'ai architect',
        'principal engineer', 'staff engineer', 'distinguished engineer',
        'technical lead', 'engineering manager', 'director of engineering',
        'vp engineering', 'cto', 'chief scientist', 'head of ai'
    ],
    'keywords': [
        'artificial intelligence', 'machine learning', 'deep learning',
        'neural network', 'computer vision', 'natural language processing',
        'reinforcement learning', 'generative ai', 'large language model',
        'transformer', 'pytorch', 'tensorflow', 'cuda', 'gpu'
    ]
}

# Stealth Mode Indicators
STEALTH_INDICATORS = {
    'company_names': [
        'stealth', 'stealth startup', 'stealth mode',
        'new venture', 'self-employed', 'self employed',
        'independent', 'consulting', 'advisor', 'personal project',
        'freelance', 'contractor', 'entrepreneur', 'founder',
        'building something', 'working on something'
    ],
    'job_titles': [
        'founder', 'co-founder', 'cofounder', 'building',
        'working on', 'creating', 'developing', 'entrepreneur',
        'chief executive', 'chief technology', 'chief product',
        'stealth', 'advisor', 'consultant', 'independent'
    ],
    'vague_phrases': [
        'building something cool', 'building something new',
        'working on something exciting', 'can\'t share yet',
        'more to come', 'stay tuned', 'stealth mode',
        'confidential', 'under wraps', 'coming soon',
        'exciting project', 'new adventure', 'next chapter',
        'something big', 'watch this space', 'to be announced'
    ]
}

# ============================================================================
# MAIN PIPELINE CLASS
# ============================================================================

class ComprehensiveFounderPipeline:
    """
    Complete self-contained pipeline for AI founder detection
    """
    
    def __init__(self, custom_config=None):
        """Initialize with comprehensive configuration"""
        load_dotenv()
        
        # Check API key
        if not os.getenv('API_KEY'):
            print("\n" + "="*70)
            print("⚠️  NO API KEY FOUND!")
            print("="*70)
            print("\nPlease create a .env file with:")
            print("API_KEY=your_pdl_api_key_here")
            print("\nGet your API key from: https://www.peopledatalabs.com/")
            print("="*70)
            raise ValueError("No API_KEY found in .env file!")
        
        # Import after API key check
        try:
            from src.data_collection.pdl_client import get_pdl_client
            self.client = get_pdl_client()
        except ImportError as e:
            print(f"Error importing PDL client: {e}")
            print("Make sure peopledatalabs is installed: pip install peopledatalabs")
            raise
        
        # Default comprehensive configuration
        self.config = custom_config or {
            # Geographic Coverage - Choose your target states
            'states': [
                # RECOMMENDED: Top tech hubs only (5 states)
                'california', 'new york', 'texas', 'washington', 'massachusetts'
                
                # OPTIONAL: Add more states as needed
                # Uncomment lines below to expand coverage:
                # 'colorado', 'illinois', 'georgia', 'florida', 'virginia',
                # 'delaware',  # Many startups incorporate here
                # 'nevada',    # Tax benefits
            ],
            
            # Company Coverage - Which companies to search
            'companies': {
                'ai_focused': AI_FOCUSED_BIG_TECH,      # Highly recommended
                'traditional': [],  # Add TRADITIONAL_BIG_TECH if needed
                'custom': []        # Add any specific companies
            },
            
            # API Limits (adjust based on budget)
            'limits': {
                'max_companies_per_state': 500,      # Startups to find per state
                'max_employees_per_company': 500,    # Employees per company
                'api_batch_size': 100,                # Results per API call
                'rate_limit_delay': 0.5               # Seconds between API calls
            },
            
            # Scoring Thresholds
            'thresholds': {
                'min_startup_score': 3.0,      # 0-10 scale for startups
                'min_founder_score': 4.0,      # 0-10 scale for founders  
                'min_match_confidence': 50.0,  # 0-100 for matches
                'high_confidence': 70.0,       # High confidence threshold
                'vip_monitoring_score': 70.0   # Score for daily monitoring
            },
            
            # Feature Flags
            'features': {
                'collect_companies': True,      # Search for startups
                'collect_employees': True,      # Search for employees
                'process_data': True,          # Process collected data
                'run_matching': True,          # Match founders to startups
                'setup_monitoring': True,      # Setup ongoing monitoring
                'generate_reports': True       # Create detailed reports
            },
            
            # Output Settings
            'output': {
                'save_raw_data': True,         # Keep raw API responses
                'save_processed': True,        # Keep processed data
                'save_matches': True,          # Keep match results
                'verbose': True,               # Detailed output
                'create_summary': True         # Create summary report
            }
        }
        
        # Initialize statistics
        self.stats = {
            'timestamp': datetime.now().isoformat(),
            'companies_collected': 0,
            'employees_collected': 0,
            'qualified_startups': 0,
            'potential_founders': 0,
            'matches_found': 0,
            'high_confidence_matches': 0,
            'api_calls_made': 0,
            'estimated_cost': 0.0,
            'states_processed': [],
            'companies_searched': []
        }
        
        # Ensure output directories exist
        self.setup_directories()
    
    def setup_directories(self):
        """Create all necessary directories"""
        directories = [
            'data/raw/pdl_companies',
            'data/raw/pdl_employees',
            'data/processed/pdl_employees',
            'data/processed',
            'data/results',
            'data/monitoring',
            'data/monitoring/reports',
            'logs'
        ]
        
        for directory in directories:
            os.makedirs(directory, exist_ok=True)
    
    def run_complete_pipeline(self, mode='interactive'):
        """
        Run the complete pipeline
        
        Modes:
        - 'interactive': Ask for confirmation at each step
        - 'auto': Run everything automatically
        - 'test': Limited test run
        - 'process_only': Skip API calls, process existing data
        """
        
        print("\n" + "="*70)
        print("🚀 COMPREHENSIVE AI FOUNDER DETECTION PIPELINE")
        print("="*70)
        print(f"Mode: {mode.upper()}")
        print(f"Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("="*70)
        
        # Adjust configuration based on mode
        if mode == 'test':
            self.config['states'] = ['california']  # Just California
            self.config['limits']['max_companies_per_state'] = 10
            self.config['limits']['max_employees_per_company'] = 10
            self.config['companies']['ai_focused'] = ['openai', 'google', 'meta']
            print("\n📋 TEST MODE: Limited to California, 3 companies, 10 results each")
        
        elif mode == 'process_only':
            self.config['features']['collect_companies'] = False
            self.config['features']['collect_employees'] = False
            print("\n📋 PROCESS ONLY MODE: Skipping data collection")
        
        # Show configuration
        self.show_configuration()
        
        if mode == 'interactive':
            if input("\nProceed with this configuration? (y/n): ").lower() != 'y':
                print("Pipeline cancelled.")
                return
        
        # Execute pipeline phases
        try:
            # Phase 1: Data Collection
            if self.config['features']['collect_companies'] or self.config['features']['collect_employees']:
                self.phase1_data_collection(mode)
            
            # Phase 2: Data Processing
            if self.config['features']['process_data']:
                self.phase2_data_processing()
            
            # Phase 3: Matching
            if self.config['features']['run_matching']:
                self.phase3_matching()
            
            # Phase 4: Monitoring Setup
            if self.config['features']['setup_monitoring']:
                self.phase4_monitoring()
            
            # Phase 5: Generate Reports
            if self.config['features']['generate_reports']:
                self.phase5_reports()
            
            # Final Summary
            self.print_final_summary()
            
        except KeyboardInterrupt:
            print("\n\n⚠️ Pipeline interrupted by user")
            self.save_progress()
        except Exception as e:
            print(f"\n❌ Pipeline error: {e}")
            import traceback
            traceback.print_exc()
            self.save_progress()
    
    def show_configuration(self):
        """Display current configuration"""
        print("\n📋 CURRENT CONFIGURATION:")
        print("-"*50)
        
        # States
        print(f"States to search ({len(self.config['states'])}):")
        for i in range(0, len(self.config['states']), 5):
            batch = self.config['states'][i:i+5]
            print(f"  {', '.join(batch)}")
        
        # Companies
        all_companies = self.get_all_target_companies()
        print(f"\nCompanies to search ({len(all_companies)}):")
        sample = all_companies[:10]
        print(f"  {', '.join(sample)}{'...' if len(all_companies) > 10 else ''}")
        
        # Limits
        print(f"\nAPI Limits:")
        print(f"  Max startups per state: {self.config['limits']['max_companies_per_state']}")
        print(f"  Max employees per company: {self.config['limits']['max_employees_per_company']}")
        
        # Estimated cost
        estimated_calls = (
            len(self.config['states']) * (self.config['limits']['max_companies_per_state'] // 100) +
            len(all_companies) * (self.config['limits']['max_employees_per_company'] // 100)
        )
        estimated_cost = estimated_calls * 0.01  # Assuming $0.01 per API call
        print(f"\nEstimated API calls: ~{estimated_calls}")
        print(f"Estimated cost: ~${estimated_cost:.2f}")
        print("-"*50)
    
    def phase1_data_collection(self, mode):
        """Phase 1: Collect data from APIs"""
        print("\n" + "="*70)
        print("📥 PHASE 1: DATA COLLECTION")
        print("="*70)
        
        # Step 1: Collect Companies
        if self.config['features']['collect_companies']:
            self.collect_companies_by_state(mode)
        
        # Step 2: Collect Employees  
        if self.config['features']['collect_employees']:
            self.collect_employees_by_company(mode)
    
    def collect_companies_by_state(self, mode):
        """Collect startups from each state"""
        print(f"\n🏢 COLLECTING STARTUPS FROM {len(self.config['states'])} STATES")
        print("-"*50)
        
        if mode == 'interactive':
            if input("Proceed with company collection? (y/n): ").lower() != 'y':
                print("Skipping company collection.")
                return
        
        # Import necessary functions
        try:
            from src.data_collection.pdl_client import get_pdl_client
            client = get_pdl_client()
        except ImportError:
            print("❌ Could not import PDL client. Using direct implementation...")
            client = self.client
        
        for state_num, state in enumerate(self.config['states'], 1):
            print(f"\n[{state_num}/{len(self.config['states'])}] Processing {state.upper()}...")
            
            # Build query for this state
            query = f"""
                SELECT * FROM company 
                WHERE location.region = '{state}'
                AND founded >= 2022
                AND employee_count <= 50 
                AND size IN ('1-10', '11-50')
            """
            
            output_file = f"data/raw/pdl_companies/{state.replace(' ', '_')}.jsonl"
            companies_collected = 0
            offset = 0
            
            while companies_collected < self.config['limits']['max_companies_per_state']:
                try:
                    # Make API call
                    params = {
                        'sql': query,
                        'size': min(
                            self.config['limits']['api_batch_size'],
                            self.config['limits']['max_companies_per_state'] - companies_collected
                        ),
                        'from': offset
                    }
                    
                    response = client.company.search(**params).json()
                    self.stats['api_calls_made'] += 1
                    
                    if response.get('status') != 200:
                        print(f"  ❌ API error for {state}: {response.get('error')}")
                        break
                    
                    data = response.get('data', [])
                    if not data:
                        print(f"  ✓ No more results for {state}")
                        break
                    
                    # Save to file
                    with open(output_file, 'a', encoding='utf-8') as f:
                        for company in data:
                            f.write(json.dumps(company) + '\n')
                    
                    companies_collected += len(data)
                    offset += len(data)
                    
                    print(f"  Collected {companies_collected} companies from {state}...")
                    
                    # Rate limiting
                    time.sleep(self.config['limits']['rate_limit_delay'])
                    
                except Exception as e:
                    print(f"  ❌ Error collecting from {state}: {e}")
                    break
            
            self.stats['companies_collected'] += companies_collected
            self.stats['states_processed'].append(state)
            print(f"  ✅ Total collected from {state}: {companies_collected}")
        
        print(f"\n✅ Total startups collected: {self.stats['companies_collected']}")
    
    def collect_employees_by_company(self, mode):
        """Collect employees from target companies"""
        companies = self.get_all_target_companies()
        
        print(f"\n👥 COLLECTING EMPLOYEES FROM {len(companies)} COMPANIES")
        print("-"*50)
        
        if mode == 'interactive':
            print(f"Target companies: {', '.join(companies[:5])}{'...' if len(companies) > 5 else ''}")
            if input("Proceed with employee collection? (y/n): ").lower() != 'y':
                print("Skipping employee collection.")
                return
        
        try:
            from src.data_collection.pdl_client import get_pdl_client
            client = get_pdl_client()
        except:
            client = self.client
        
        for comp_num, company in enumerate(companies, 1):
            print(f"\n[{comp_num}/{len(companies)}] Processing {company.upper()}...")
            
            # Build query for AI/ML employees from this company
            query = {
                'bool': {
                    'must': [
                        {'term': {'experience.company.name': company}},
                        {
                            'bool': {
                                'should': [
                                    {'match': {'job_title': 'machine learning'}},
                                    {'match': {'job_title': 'data scientist'}},
                                    {'match': {'job_title': 'ai'}},
                                    {'match': {'job_title': 'research'}},
                                    {'term': {'job_title_role': 'engineering'}},
                                    {'term': {'job_title_role': 'research'}}
                                ]
                            }
                        }
                    ]
                }
            }
            
            output_file = f"data/raw/pdl_employees/{company.replace(' ', '_')}_employees.jsonl"
            employees_collected = 0
            offset = 0
            
            while employees_collected < self.config['limits']['max_employees_per_company']:
                try:
                    params = {
                        'query': query,
                        'size': min(
                            self.config['limits']['api_batch_size'],
                            self.config['limits']['max_employees_per_company'] - employees_collected
                        ),
                        'from': offset
                    }
                    
                    response = client.person.search(**params).json()
                    self.stats['api_calls_made'] += 1
                    
                    if response.get('status') != 200:
                        print(f"  ❌ API error for {company}: {response.get('error')}")
                        break
                    
                    data = response.get('data', [])
                    if not data:
                        print(f"  ✓ No more results for {company}")
                        break
                    
                    # Save to file
                    with open(output_file, 'a', encoding='utf-8') as f:
                        for employee in data:
                            f.write(json.dumps(employee) + '\n')
                    
                    employees_collected += len(data)
                    offset += len(data)
                    
                    print(f"  Collected {employees_collected} employees from {company}...")
                    
                    # Rate limiting
                    time.sleep(self.config['limits']['rate_limit_delay'])
                    
                except Exception as e:
                    print(f"  ❌ Error collecting from {company}: {e}")
                    break
            
            self.stats['employees_collected'] += employees_collected
            self.stats['companies_searched'].append(company)
            print(f"  ✅ Total collected from {company}: {employees_collected}")
        
        print(f"\n✅ Total employees collected: {self.stats['employees_collected']}")
        self.stats['estimated_cost'] = self.stats['api_calls_made'] * 0.01
        print(f"💰 Estimated API cost: ${self.stats['estimated_cost']:.2f}")
    
    def phase2_data_processing(self):
        """Phase 2: Process collected data"""
        print("\n" + "="*70)
        print("📊 PHASE 2: DATA PROCESSING")
        print("="*70)
        
        # Process companies
        print("\n🏢 Processing companies to identify tech startups...")
        try:
            from src.data_processing.company_qualifier import process_potential_tech_startups
            qualified_startups = process_potential_tech_startups()
            self.stats['qualified_startups'] = len(qualified_startups)
        except Exception as e:
            print(f"❌ Error processing companies: {e}")
            self.stats['qualified_startups'] = 0
        
        # Process employees
        print("\n👥 Processing employees to identify founders...")
        try:
            # First process employment histories
            from src.data_processing.employee_processor import process_all_employees
            process_all_employees()
            
            # Then qualify founders
            from src.data_processing.founder_qualifier import process_potential_founders
            potential_founders = process_potential_founders()
            self.stats['potential_founders'] = len(potential_founders)
        except Exception as e:
            print(f"❌ Error processing employees: {e}")
            self.stats['potential_founders'] = 0
        
        print(f"\n✅ Qualified startups: {self.stats['qualified_startups']}")
        print(f"✅ Potential founders: {self.stats['potential_founders']}")
    
    def phase3_matching(self):
        """Phase 3: Match founders with startups"""
        print("\n" + "="*70)
        print("🔗 PHASE 3: FOUNDER-STARTUP MATCHING")
        print("="*70)
        
        try:
            from src.matching.employment_matcher import EmploymentMatcher, save_matches_to_jsonl
            
            # Load processed data
            with open('data/processed/potential_founders.json', 'r') as f:
                founders = json.load(f)
            with open('data/processed/qualified_startups.json', 'r') as f:
                startups = json.load(f)
            
            if not founders or not startups:
                print("⚠️ No data to match")
                return
            
            print(f"Matching {len(founders)} founders with {len(startups)} startups...")
            
            # Run matching
            matcher = EmploymentMatcher()
            matches = matcher.find_employment_matches(founders, startups)
            
            self.stats['matches_found'] = len(matches)
            self.stats['high_confidence_matches'] = len([m for m in matches if m.confidence_score >= 70])
            
            # Save results
            if matches:
                save_matches_to_jsonl(matches, 'data/results/employment_matches.jsonl')
                
                # High confidence
                high = [m for m in matches if m.confidence_score >= 70]
                if high:
                    save_matches_to_jsonl(high, 'data/results/high_confidence_employment_matches.jsonl')
                
                # Manual review
                manual = [m for m in matches if 50 <= m.confidence_score < 70]
                if manual:
                    save_matches_to_jsonl(manual, 'data/results/manual_review_employment_matches.jsonl')
            
            print(f"\n✅ Total matches: {self.stats['matches_found']}")
            print(f"🌟 High confidence: {self.stats['high_confidence_matches']}")
            
        except Exception as e:
            print(f"❌ Error during matching: {e}")
    
    def phase4_monitoring(self):
        """Phase 4: Setup monitoring"""
        print("\n" + "="*70)
        print("📡 PHASE 4: MONITORING SETUP")
        print("="*70)
        
        try:
            from src.monitoring.employment_monitor import EmploymentMonitor
            monitor = EmploymentMonitor()
            
            # Load founders for monitoring
            with open('data/processed/potential_founders.json', 'r') as f:
                founders = json.load(f)
            
            # Setup monitoring for top founders
            top_founders = sorted(founders, key=lambda x: x.get('founder_score', 0), reverse=True)[:100]
            
            for founder in top_founders:
                monitor.save_snapshot(founder)
                
                # Determine tier
                score = founder.get('founder_score', 0)
                if score >= 7:
                    tier = 'vip'
                elif score >= 5:
                    tier = 'watch'
                else:
                    tier = 'general'
                
                monitor.update_monitoring_schedule(
                    founder, tier, score, 
                    founder.get('qualification_reasons', [])
                )
            
            stats = monitor.get_monitoring_stats()
            print(f"\n✅ Monitoring setup complete")
            print(f"  VIP: {stats['tier_distribution'].get('vip', 0)} people")
            print(f"  Watch: {stats['tier_distribution'].get('watch', 0)} people")
            print(f"  General: {stats['tier_distribution'].get('general', 0)} people")
            
        except Exception as e:
            print(f"❌ Error setting up monitoring: {e}")
    
    def phase5_reports(self):
        """Phase 5: Generate comprehensive reports"""
        print("\n" + "="*70)
        print("📈 PHASE 5: REPORT GENERATION")
        print("="*70)
        
        # Create comprehensive report
        report = {
            'metadata': {
                'timestamp': datetime.now().isoformat(),
                'pipeline_version': '2.0',
                'mode': 'comprehensive'
            },
            'configuration': {
                'states_searched': self.config['states'],
                'companies_searched': self.get_all_target_companies(),
                'thresholds': self.config['thresholds']
            },
            'statistics': self.stats,
            'files_created': {
                'raw_companies': [f"{state}.jsonl" for state in self.stats['states_processed']],
                'raw_employees': [f"{company}_employees.jsonl" for company in self.stats['companies_searched']],
                'processed': [
                    'potential_founders.json',
                    'qualified_startups.json'
                ],
                'results': [
                    'employment_matches.jsonl',
                    'high_confidence_employment_matches.jsonl',
                    'manual_review_employment_matches.jsonl'
                ]
            }
        }
        
        # Save main report
        report_file = f"pipeline_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(report_file, 'w') as f:
            json.dump(report, f, indent=2)
        
        print(f"✅ Report saved to: {report_file}")
        
        # Create summary CSV for quick viewing
        self.create_summary_csv()
    
    def create_summary_csv(self):
        """Create CSV summary of matches"""
        try:
            import csv
            
            # Load matches
            matches = []
            match_file = 'data/results/employment_matches.jsonl'
            if os.path.exists(match_file):
                with open(match_file, 'r') as f:
                    for line in f:
                        matches.append(json.loads(line))
            
            if not matches:
                return
            
            # Create CSV
            csv_file = f"matches_summary_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
            with open(csv_file, 'w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                
                # Header
                writer.writerow([
                    'Founder Name', 'Previous Company', 'Current Company',
                    'Startup Name', 'Startup Industry', 'Confidence Score',
                    'Match Reasons'
                ])
                
                # Data rows
                for match in matches:
                    writer.writerow([
                        match['founder'].get('full_name', 'Unknown'),
                        match['founder'].get('last_big_tech_departure_date', 'N/A'),
                        match['founder'].get('current_company', {}).get('name', 'N/A'),
                        match['startup'].get('name', 'Unknown'),
                        match['startup'].get('industry', 'N/A'),
                        match['confidence_score'],
                        '; '.join(match.get('match_reasons', []))
                    ])
            
            print(f"✅ CSV summary saved to: {csv_file}")
            
        except Exception as e:
            print(f"Warning: Could not create CSV summary: {e}")
    
    def get_all_target_companies(self):
        """Get complete list of target companies"""
        companies = []
        companies.extend(self.config['companies'].get('ai_focused', []))
        companies.extend(self.config['companies'].get('traditional', []))
        companies.extend(self.config['companies'].get('custom', []))
        return list(set(companies))  # Remove duplicates
    
    def save_progress(self):
        """Save current progress in case of interruption"""
        progress_file = f"pipeline_progress_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(progress_file, 'w') as f:
            json.dump({
                'stats': self.stats,
                'config': self.config,
                'timestamp': datetime.now().isoformat()
            }, f, indent=2)
        print(f"\n💾 Progress saved to: {progress_file}")
    
    def print_final_summary(self):
        """Print final summary of the pipeline run"""
        print("\n" + "="*70)
        print("🎯 PIPELINE COMPLETE - FINAL SUMMARY")
        print("="*70)
        
        print(f"\n📊 Data Collection:")
        print(f"  States processed: {len(self.stats['states_processed'])}")
        print(f"  Companies searched: {len(self.stats['companies_searched'])}")
        print(f"  Total startups found: {self.stats['companies_collected']}")
        print(f"  Total employees found: {self.stats['employees_collected']}")
        
        print(f"\n✅ Processing Results:")
        print(f"  Qualified tech startups: {self.stats['qualified_startups']}")
        print(f"  Potential founders identified: {self.stats['potential_founders']}")
        
        print(f"\n🔗 Matching Results:")
        print(f"  Total matches: {self.stats['matches_found']}")
        print(f"  High confidence matches: {self.stats['high_confidence_matches']}")
        
        print(f"\n💰 API Usage:")
        print(f"  Total API calls: {self.stats['api_calls_made']}")
        print(f"  Estimated cost: ${self.stats['estimated_cost']:.2f}")
        
        print(f"\n📁 Output Files:")
        print(f"  Check data/raw/ for raw data")
        print(f"  Check data/processed/ for processed data")
        print(f"  Check data/results/ for matches")
        
        print("\n" + "="*70)
        print("✅ SUCCESS! AI Founder Detection Pipeline Complete")
        print("="*70)

# ============================================================================
# MAIN EXECUTION
# ============================================================================

def main():
    """Main entry point with interactive menu"""
    
    print("\n" + "="*70)
    print("🚀 COMPREHENSIVE AI FOUNDER DETECTION SYSTEM")
    print("="*70)
    print("\nThis system will:")
    print("• Search for tech startups across multiple states")
    print("• Find AI/ML employees from major tech companies")
    print("• Identify potential founders who left to start companies")
    print("• Match founders with their likely startups")
    print("• Setup ongoing monitoring")
    print("="*70)
    
    print("\n📋 QUICK START OPTIONS:")
    print("-"*50)
    print("1. TEST RUN - California only, 3 companies (~$0.30)")
    print("2. SMALL RUN - 5 states, 10 companies (~$5)")
    print("3. MEDIUM RUN - 10 states, 20 companies (~$20)")
    print("4. LARGE RUN - 20 states, all AI companies (~$100)")
    print("5. CUSTOM - Configure everything yourself")
    print("6. PROCESS EXISTING DATA - No API calls (FREE)")
    print("7. EXIT")
    print("-"*50)
    
    choice = input("\nSelect option (1-7): ").strip()
    
    # Create pipeline with appropriate configuration
    if choice == '1':
        # Test configuration
        config = {
            'states': ['california'],
            'companies': {
                'ai_focused': ['openai', 'google', 'meta'],
                'traditional': [],
                'custom': []
            },
            'limits': {
                'max_companies_per_state': 10,
                'max_employees_per_company': 10,
                'api_batch_size': 10,
                'rate_limit_delay': 0.5
            },
            'thresholds': {
                'min_startup_score': 3.0,
                'min_founder_score': 4.0,
                'min_match_confidence': 50.0,
                'high_confidence': 70.0,
                'vip_monitoring_score': 70.0
            },
            'features': {
                'collect_companies': True,
                'collect_employees': True,
                'process_data': True,
                'run_matching': True,
                'setup_monitoring': True,
                'generate_reports': True
            },
            'output': {
                'save_raw_data': True,
                'save_processed': True,
                'save_matches': True,
                'verbose': True,
                'create_summary': True
            }
        }
        pipeline = ComprehensiveFounderPipeline(config)
        pipeline.run_complete_pipeline(mode='auto')
        
    elif choice == '2':
        # Small run
        config = {
            'states': ['california', 'new york', 'texas', 'washington', 'massachusetts'],
            'companies': {
                'ai_focused': AI_FOCUSED_BIG_TECH[:10],  # First 10 companies
                'traditional': [],
                'custom': []
            },
            'limits': {
                'max_companies_per_state': 50,
                'max_employees_per_company': 50,
                'api_batch_size': 50,
                'rate_limit_delay': 0.5
            },
            'thresholds': {
                'min_startup_score': 3.0,
                'min_founder_score': 4.0,
                'min_match_confidence': 50.0,
                'high_confidence': 70.0,
                'vip_monitoring_score': 70.0
            },
            'features': {
                'collect_companies': True,
                'collect_employees': True,
                'process_data': True,
                'run_matching': True,
                'setup_monitoring': True,
                'generate_reports': True
            },
            'output': {
                'save_raw_data': True,
                'save_processed': True,
                'save_matches': True,
                'verbose': True,
                'create_summary': True
            }
        }
        pipeline = ComprehensiveFounderPipeline(config)
        pipeline.run_complete_pipeline(mode='interactive')
        
    elif choice == '3':
        # Medium run
        config = {
            'states': ALL_US_STATES[:10],  # First 10 states
            'companies': {
                'ai_focused': AI_FOCUSED_BIG_TECH[:20],  # First 20 companies
                'traditional': [],
                'custom': []
            },
            'limits': {
                'max_companies_per_state': 100,
                'max_employees_per_company': 100,
                'api_batch_size': 100,
                'rate_limit_delay': 0.5
            },
            'thresholds': {
                'min_startup_score': 3.0,
                'min_founder_score': 4.0,
                'min_match_confidence': 50.0,
                'high_confidence': 70.0,
                'vip_monitoring_score': 70.0
            },
            'features': {
                'collect_companies': True,
                'collect_employees': True,
                'process_data': True,
                'run_matching': True,
                'setup_monitoring': True,
                'generate_reports': True
            },
            'output': {
                'save_raw_data': True,
                'save_processed': True,
                'save_matches': True,
                'verbose': True,
                'create_summary': True
            }
        }
        print("\n⚠️ This will cost approximately $20 in API credits.")
        if input("Continue? (y/n): ").lower() == 'y':
            pipeline = ComprehensiveFounderPipeline(config)
            pipeline.run_complete_pipeline(mode='interactive')
        else:
            print("Cancelled.")
            
    elif choice == '4':
        # Large run
        config = {
            'states': ALL_US_STATES[:20],  # First 20 states
            'companies': {
                'ai_focused': AI_FOCUSED_BIG_TECH,  # All AI companies
                'traditional': [],
                'custom': []
            },
            'limits': {
                'max_companies_per_state': 200,
                'max_employees_per_company': 200,
                'api_batch_size': 100,
                'rate_limit_delay': 0.5
            },
            'thresholds': {
                'min_startup_score': 3.0,
                'min_founder_score': 4.0,
                'min_match_confidence': 50.0,
                'high_confidence': 70.0,
                'vip_monitoring_score': 70.0
            },
            'features': {
                'collect_companies': True,
                'collect_employees': True,
                'process_data': True,
                'run_matching': True,
                'setup_monitoring': True,
                'generate_reports': True
            },
            'output': {
                'save_raw_data': True,
                'save_processed': True,
                'save_matches': True,
                'verbose': True,
                'create_summary': True
            }
        }
        print("\n⚠️ WARNING: This will cost approximately $100 in API credits!")
        print("This is a LARGE production run.")
        if input("Are you absolutely sure? (type 'yes' to confirm): ").lower() == 'yes':
            pipeline = ComprehensiveFounderPipeline(config)
            pipeline.run_complete_pipeline(mode='interactive')
        else:
            print("Cancelled.")
            
    elif choice == '5':
        # Custom configuration
        print("\n📋 CUSTOM CONFIGURATION")
        print("-"*50)
        
        # Select states
        print("\nAvailable states:")
        for i, state in enumerate(ALL_US_STATES, 1):
            print(f"{i:2}. {state}")
        
        state_input = input("\nEnter state numbers (comma-separated, e.g., 1,2,3): ")
        selected_states = []
        for num in state_input.split(','):
            try:
                idx = int(num.strip()) - 1
                if 0 <= idx < len(ALL_US_STATES):
                    selected_states.append(ALL_US_STATES[idx])
            except:
                pass
        
        if not selected_states:
            selected_states = ['california']  # Default
        
        # Select companies
        print("\nSelect company groups:")
        print("1. AI-focused companies only")
        print("2. AI + Traditional tech")
        print("3. Custom list")
        
        comp_choice = input("Choice (1-3): ").strip()
        
        if comp_choice == '1':
            companies = {'ai_focused': AI_FOCUSED_BIG_TECH, 'traditional': [], 'custom': []}
        elif comp_choice == '2':
            companies = {'ai_focused': AI_FOCUSED_BIG_TECH, 'traditional': TRADITIONAL_BIG_TECH, 'custom': []}
        else:
            custom = input("Enter company names (comma-separated): ").split(',')
            companies = {'ai_focused': [], 'traditional': [], 'custom': [c.strip() for c in custom]}
        
        # Get limits
        max_companies = int(input("\nMax companies per state (default 100): ") or "100")
        max_employees = int(input("Max employees per company (default 100): ") or "100")
        
        config = {
            'states': selected_states,
            'companies': companies,
            'limits': {
                'max_companies_per_state': max_companies,
                'max_employees_per_company': max_employees,
                'api_batch_size': 100,
                'rate_limit_delay': 0.5
            },
            'thresholds': {
                'min_startup_score': 3.0,
                'min_founder_score': 4.0,
                'min_match_confidence': 50.0,
                'high_confidence': 70.0,
                'vip_monitoring_score': 70.0
            },
            'features': {
                'collect_companies': True,
                'collect_employees': True,
                'process_data': True,
                'run_matching': True,
                'setup_monitoring': True,
                'generate_reports': True
            },
            'output': {
                'save_raw_data': True,
                'save_processed': True,
                'save_matches': True,
                'verbose': True,
                'create_summary': True
            }
        }
        
        pipeline = ComprehensiveFounderPipeline(config)
        pipeline.run_complete_pipeline(mode='interactive')
        
    elif choice == '6':
        # Process existing data only
        pipeline = ComprehensiveFounderPipeline()
        pipeline.run_complete_pipeline(mode='process_only')
        
    else:
        print("Exiting...")
        return

if __name__ == "__main__":
    main()