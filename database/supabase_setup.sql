-- Create finance_companies table
CREATE TABLE IF NOT EXISTS finance_companies (
    id SERIAL PRIMARY KEY,
    company_name TEXT NOT NULL,
    industry TEXT NOT NULL DEFAULT 'Finance',
    location TEXT,
    company_size TEXT, -- Small, Medium, Large, Enterprise
    employee_count INTEGER,
    revenue BIGINT DEFAULT 0,
    founding_year INTEGER,
    description TEXT,
    business_model TEXT,
    target_market TEXT,
    key_services TEXT,
    technology_stack TEXT,
    market_position TEXT, -- Leader, Challenger, Follower, Niche
    recent_news TEXT,
    website_url TEXT,
    contact_email TEXT,
    phone_number TEXT,
    ceo_name TEXT,
    headquarters TEXT,
    subsidiaries TEXT,
    partnerships TEXT,
    awards TEXT,
    financial_status TEXT, -- Public, Private, Subsidiary
    stock_symbol TEXT,
    last_funding_round TEXT,
    investors TEXT,
    competitive_advantages TEXT,
    challenges TEXT,
    growth_stage TEXT, -- Startup, Growth, Mature, Declining
    sustainability_initiatives TEXT,
    digital_transformation_level TEXT, -- Low, Medium, High, Advanced
    innovation_focus TEXT,
    customer_base_size TEXT,
    geographic_presence TEXT, -- Local, Regional, National, Global
    regulatory_compliance TEXT,
    risk_factors TEXT,
    performance_score INTEGER DEFAULT NULL, -- To be evaluated by agents
    evaluation_notes TEXT, -- Agent evaluation details
    last_evaluated_at TIMESTAMP WITH TIME ZONE DEFAULT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Create healthcare_companies table
CREATE TABLE IF NOT EXISTS healthcare_companies (
    id SERIAL PRIMARY KEY,
    company_name TEXT NOT NULL,
    industry TEXT NOT NULL DEFAULT 'Healthcare',
    location TEXT,
    company_size TEXT, -- Small, Medium, Large, Enterprise
    employee_count INTEGER,
    revenue BIGINT DEFAULT 0,
    founding_year INTEGER,
    description TEXT,
    business_model TEXT,
    target_market TEXT,
    key_services TEXT,
    technology_stack TEXT,
    market_position TEXT, -- Leader, Challenger, Follower, Niche
    recent_news TEXT,
    website_url TEXT,
    contact_email TEXT,
    phone_number TEXT,
    ceo_name TEXT,
    headquarters TEXT,
    subsidiaries TEXT,
    partnerships TEXT,
    awards TEXT,
    financial_status TEXT, -- Public, Private, Subsidiary
    stock_symbol TEXT,
    last_funding_round TEXT,
    investors TEXT,
    competitive_advantages TEXT,
    challenges TEXT,
    growth_stage TEXT, -- Startup, Growth, Mature, Declining
    sustainability_initiatives TEXT,
    digital_transformation_level TEXT, -- Low, Medium, High, Advanced
    innovation_focus TEXT,
    customer_base_size TEXT,
    geographic_presence TEXT, -- Local, Regional, National, Global
    regulatory_compliance TEXT,
    risk_factors TEXT,
    performance_score INTEGER DEFAULT NULL, -- To be evaluated by agents
    evaluation_notes TEXT, -- Agent evaluation details
    last_evaluated_at TIMESTAMP WITH TIME ZONE DEFAULT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Create tech_companies table
CREATE TABLE IF NOT EXISTS tech_companies (
    id SERIAL PRIMARY KEY,
    company_name TEXT NOT NULL,
    industry TEXT NOT NULL DEFAULT 'Technology',
    location TEXT,
    company_size TEXT, -- Small, Medium, Large, Enterprise
    employee_count INTEGER,
    revenue BIGINT DEFAULT 0,
    founding_year INTEGER,
    description TEXT,
    business_model TEXT,
    target_market TEXT,
    key_services TEXT,
    technology_stack TEXT,
    market_position TEXT, -- Leader, Challenger, Follower, Niche
    recent_news TEXT,
    website_url TEXT,
    contact_email TEXT,
    phone_number TEXT,
    ceo_name TEXT,
    headquarters TEXT,
    subsidiaries TEXT,
    partnerships TEXT,
    awards TEXT,
    financial_status TEXT, -- Public, Private, Subsidiary
    stock_symbol TEXT,
    last_funding_round TEXT,
    investors TEXT,
    competitive_advantages TEXT,
    challenges TEXT,
    growth_stage TEXT, -- Startup, Growth, Mature, Declining
    sustainability_initiatives TEXT,
    digital_transformation_level TEXT, -- Low, Medium, High, Advanced
    innovation_focus TEXT,
    customer_base_size TEXT,
    geographic_presence TEXT, -- Local, Regional, National, Global
    regulatory_compliance TEXT,
    risk_factors TEXT,
    performance_score INTEGER DEFAULT NULL, -- To be evaluated by agents
    evaluation_notes TEXT, -- Agent evaluation details
    last_evaluated_at TIMESTAMP WITH TIME ZONE DEFAULT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Insert comprehensive finance company data (30 companies)
INSERT INTO finance_companies (company_name, industry, location, company_size, employee_count, revenue, founding_year, description, business_model, target_market, key_services, technology_stack, market_position, recent_news, website_url, contact_email, ceo_name, headquarters, financial_status, stock_symbol, competitive_advantages, challenges, growth_stage, digital_transformation_level, customer_base_size, geographic_presence) VALUES

('Goldman Sachs', 'Finance', 'New York, NY', 'Enterprise', 43000, 59000000000, 1869, 'Leading global investment banking, securities and investment management firm', 'Investment Banking & Asset Management', 'Institutional Investors, Corporations, High Net Worth', 'Investment Banking, Securities Trading, Asset Management, Consumer Banking', 'Cloud Computing, AI/ML, Blockchain, Java, Python', 'Leader', 'Expanding AI-driven trading platforms and sustainable finance initiatives', 'https://www.goldmansachs.com', 'info@gs.com', 'David Solomon', 'New York, NY', 'Public', 'GS', 'Global reach, sophisticated trading technology, strong client relationships', 'Regulatory scrutiny, market volatility, competition from fintech', 'Mature', 'Advanced', 'Large Enterprise', 'Global'),

('JPMorgan Chase', 'Finance', 'New York, NY', 'Enterprise', 271025, 158100000000, 1799, 'Multinational investment bank and financial services company', 'Universal Banking', 'Consumers, Small Business, Corporate, Institutional', 'Consumer Banking, Investment Banking, Commercial Banking, Asset Management', 'Cloud Native, AI/ML, Microservices, React, Java', 'Leader', 'Leading digital banking transformation with $15B annual tech investment', 'https://www.jpmorganchase.com', 'investor.relations@jpmchase.com', 'Jamie Dimon', 'New York, NY', 'Public', 'JPM', 'Largest US bank by assets, strong technology investment, diverse revenue streams', 'Regulatory compliance costs, credit risk, cyber security threats', 'Mature', 'Advanced', 'Mass Market', 'Global'),

('Bank of America', 'Finance', 'Charlotte, NC', 'Enterprise', 208000, 89113000000, 1904, 'Multinational investment bank and financial services company', 'Universal Banking', 'Consumers, Small Business, Corporate, Institutional', 'Consumer Banking, Global Banking, Global Markets, Global Wealth Management', 'Cloud Computing, AI/ML, Mobile-First, Java, Python', 'Leader', 'Committed to net-zero emissions by 2050, expanding digital capabilities', 'https://www.bankofamerica.com', 'investor.relations@bofa.com', 'Brian Moynihan', 'Charlotte, NC', 'Public', 'BAC', 'Extensive branch network, strong digital platform, comprehensive services', 'Interest rate sensitivity, regulatory requirements, competition', 'Mature', 'High', 'Mass Market', 'Global'),

('Wells Fargo', 'Finance', 'San Francisco, CA', 'Enterprise', 238000, 73393000000, 1852, 'Diversified financial services company', 'Universal Banking', 'Consumers, Small Business, Commercial, Corporate', 'Banking, Lending, Investment, Insurance', 'Hybrid Cloud, AI/ML, Mobile Banking, Java, .NET', 'Challenger', 'Rebuilding reputation and focusing on operational excellence', 'https://www.wellsfargo.com', 'investor.relations@wellsfargo.com', 'Charlie Scharf', 'San Francisco, CA', 'Public', 'WFC', 'Strong retail presence, mortgage lending expertise, diversified services', 'Regulatory issues, reputation recovery, operational risk', 'Mature', 'High', 'Mass Market', 'National'),

('Morgan Stanley', 'Finance', 'New York, NY', 'Enterprise', 75000, 61035000000, 1935, 'Global financial services firm', 'Investment Banking & Wealth Management', 'Institutional Investors, High Net Worth, Corporations', 'Investment Banking, Wealth Management, Investment Management', 'Cloud Computing, AI/ML, Blockchain, Python, Java', 'Leader', 'Acquired E*TRADE and Eaton Vance, expanding digital wealth management', 'https://www.morganstanley.com', 'investor.relations@morganstanley.com', 'James Gorman', 'New York, NY', 'Public', 'MS', 'Strong wealth management, global investment banking presence', 'Market volatility, regulatory changes, fee compression', 'Mature', 'Advanced', 'High Net Worth', 'Global'),

('Citigroup', 'Finance', 'New York, NY', 'Enterprise', 223000, 75338000000, 1812, 'Global diversified financial services holding company', 'Universal Banking', 'Consumers, Corporations, Governments, Institutions', 'Consumer Banking, Institutional Clients Group, Corporate Banking', 'Multi-Cloud, AI/ML, APIs, Java, Python', 'Challenger', 'Transforming to focus on wealth management and institutional banking', 'https://www.citigroup.com', 'ir@citi.com', 'Jane Fraser', 'New York, NY', 'Public', 'C', 'Global presence in emerging markets, institutional banking expertise', 'Regulatory capital requirements, geopolitical risks, operational complexity', 'Mature', 'High', 'Global Corporate', 'Global'),

('American Express', 'Finance', 'New York, NY', 'Large', 64000, 50922000000, 1850, 'Multinational financial services corporation', 'Closed-Loop Payment Network', 'Premium Consumers, Small Business, Corporate', 'Credit Cards, Charge Cards, Travel Services, Business Solutions', 'Cloud Native, AI/ML, Real-time Processing, Java, Python', 'Leader', 'Expanding premium card offerings and digital payment solutions', 'https://www.americanexpress.com', 'ir@aexp.com', 'Stephen Squeri', 'New York, NY', 'Public', 'AXP', 'Premium brand, closed-loop network, strong customer loyalty', 'Network acceptance, economic sensitivity, competition from fintech', 'Mature', 'Advanced', 'Premium Segment', 'Global'),

('Charles Schwab', 'Finance', 'Westlake, TX', 'Large', 34500, 20858000000, 1971, 'Financial services company', 'Discount Brokerage & Wealth Management', 'Individual Investors, Financial Advisors, Institutions', 'Brokerage, Banking, Advisory Services, Retirement Plans', 'Cloud Computing, AI/ML, Mobile-First, Java, Python', 'Leader', 'Completed TD Ameritrade acquisition, largest online brokerage', 'https://www.schwab.com', 'investor.relations@schwab.com', 'Walt Bettinger', 'Westlake, TX', 'Public', 'SCHW', 'Low-cost structure, comprehensive platform, strong brand', 'Zero commission pressure, interest rate sensitivity, integration challenges', 'Mature', 'High', 'Mass Affluent', 'National'),

('Capital One', 'Finance', 'McLean, VA', 'Large', 52000, 32472000000, 1994, 'Diversified bank', 'Digital-First Banking', 'Consumers, Small Business, Commercial', 'Credit Cards, Banking, Commercial Lending, Auto Loans', 'Cloud Native, AI/ML, Open Source, Python, Java', 'Challenger', 'Leading digital banking transformation and data-driven decisions', 'https://www.capitalone.com', 'investor.relations@capitalone.com', 'Richard Fairbank', 'McLean, VA', 'Public', 'COF', 'Data analytics expertise, digital-first approach, innovation culture', 'Credit risk, regulatory compliance, cyber security', 'Mature', 'Advanced', 'Mass Market', 'National'),

('TD Bank', 'Finance', 'Toronto, ON', 'Large', 95000, 42900000000, 1855, 'Canadian multinational banking and financial services corporation', 'Universal Banking', 'Consumers, Small Business, Commercial, Institutional', 'Personal Banking, Business Banking, Wealth Management, Investment Banking', 'Hybrid Cloud, AI/ML, Mobile Banking, Java, .NET', 'Leader', 'Expanding digital capabilities and sustainable finance initiatives', 'https://www.td.com', 'investor.relations@td.com', 'Bharat Masrani', 'Toronto, ON', 'Public', 'TD', 'Strong Canadian market position, growing US presence', 'Regulatory requirements, competition, economic sensitivity', 'Mature', 'High', 'Mass Market', 'North America'),

-- Additional 20 finance companies
('BlackRock', 'Finance', 'New York, NY', 'Large', 19800, 19374000000, 1988, 'World\'s largest asset manager', 'Asset Management', 'Institutional Investors, Retail Investors, Governments', 'Investment Management, Risk Management, Advisory Services', 'Cloud Computing, AI/ML, Aladdin Platform, Python, Java', 'Leader', 'Leading ESG investing and AI-driven portfolio management', 'https://www.blackrock.com', 'info@blackrock.com', 'Larry Fink', 'New York, NY', 'Public', 'BLK', 'Largest AUM globally, Aladdin technology platform, ESG leadership', 'Fee compression, regulatory changes, market volatility', 'Mature', 'Advanced', 'Institutional', 'Global'),

('Vanguard', 'Finance', 'Malvern, PA', 'Large', 17600, 31600000000, 1975, 'Investment management company', 'Mutual Fund Company', 'Individual Investors, Institutional Investors', 'Mutual Funds, ETFs, Advisory Services, Retirement Plans', 'Cloud Computing, Data Analytics, Java, Python', 'Leader', 'Leading low-cost index investing and retirement services', 'https://www.vanguard.com', 'info@vanguard.com', 'Tim Buckley', 'Malvern, PA', 'Private', NULL, 'Low-cost structure, index fund expertise, client ownership model', 'Fee competition, scale requirements, regulatory compliance', 'Mature', 'High', 'Mass Affluent', 'Global'),

('Fidelity Investments', 'Finance', 'Boston, MA', 'Large', 50000, 24500000000, 1946, 'Multinational financial services corporation', 'Asset Management & Brokerage', 'Individual Investors, Institutional Investors, Employers', 'Investment Management, Brokerage, Retirement Services, Benefits Administration', 'Cloud Native, AI/ML, Blockchain, Java, Python', 'Leader', 'Pioneering cryptocurrency services and digital retirement planning', 'https://www.fidelity.com', 'info@fidelity.com', 'Abigail Johnson', 'Boston, MA', 'Private', NULL, 'Comprehensive platform, innovation in crypto, strong retirement business', 'Regulatory uncertainty, fee competition, technology investments', 'Mature', 'Advanced', 'Mass Market', 'National'),

('Berkshire Hathaway', 'Finance', 'Omaha, NE', 'Enterprise', 372000, 364482000000, 1839, 'Multinational conglomerate holding company', 'Diversified Holdings', 'Insurance, Energy, Retail, Manufacturing', 'Insurance, Reinsurance, Utilities, Manufacturing, Retail', 'Legacy Systems, Gradual Modernization, Java, .NET', 'Leader', 'Warren Buffett succession planning and continued value investing', 'https://www.berkshirehathaway.com', 'berkshire@berkshirehathaway.com', 'Warren Buffett', 'Omaha, NE', 'Public', 'BRK.A', 'Value investing expertise, diversified holdings, strong balance sheet', 'Succession planning, finding large acquisitions, technology lag', 'Mature', 'Medium', 'Institutional', 'Global'),

('State Street', 'Finance', 'Boston, MA', 'Large', 39000, 12539000000, 1792, 'Financial services and bank holding company', 'Custodial Banking & Asset Management', 'Institutional Investors, Asset Managers, Corporations', 'Custody Services, Investment Management, Investment Research, Trading', 'Cloud Computing, AI/ML, Blockchain, Java, Python', 'Leader', 'Digital transformation and expansion of Alpha platform', 'https://www.statestreet.com', 'investor.relations@statestreet.com', 'Ronald O\'Hanley', 'Boston, MA', 'Public', 'STT', 'Custody services expertise, ETF leadership (SPDR), institutional focus', 'Fee pressure, operational efficiency, technology modernization', 'Mature', 'High', 'Institutional', 'Global'),

('PayPal', 'Finance', 'San Jose, CA', 'Large', 29900, 27518000000, 1998, 'Digital payments platform', 'Digital Payments', 'Consumers, Merchants, Developers', 'Digital Payments, Mobile Payments, Credit Services, Crypto', 'Cloud Native, AI/ML, Real-time Processing, Python, Java', 'Leader', 'Expanding crypto services and buy-now-pay-later offerings', 'https://www.paypal.com', 'investor.relations@paypal.com', 'Dan Schulman', 'San Jose, CA', 'Public', 'PYPL', 'Large user base, two-sided network, digital payments expertise', 'Increased competition, regulatory scrutiny, customer acquisition costs', 'Mature', 'Advanced', 'Mass Market', 'Global'),

('Square (Block)', 'Finance', 'San Francisco, CA', 'Large', 8000, 17661000000, 2009, 'Financial services and digital payments company', 'Digital Payments & Financial Services', 'Small Business, Individual Consumers', 'Payment Processing, Point of Sale, Cash App, Bitcoin Services', 'Cloud Native, AI/ML, Blockchain, Python, Java, Go', 'Challenger', 'Focus on Bitcoin and decentralized financial services', 'https://www.block.xyz', 'ir@block.xyz', 'Jack Dorsey', 'San Francisco, CA', 'Public', 'SQ', 'Small business focus, Cash App growth, Bitcoin integration', 'Competition, regulatory uncertainty, Bitcoin volatility', 'Growth', 'Advanced', 'Small Business', 'National'),

('Stripe', 'Finance', 'San Francisco, CA', 'Large', 4000, 12000000000, 2010, 'Financial services and software company', 'Payment Infrastructure', 'Online Businesses, Platforms, Marketplaces', 'Payment Processing, Financial Infrastructure, Business Tools', 'Cloud Native, AI/ML, APIs, Python, Ruby, Go', 'Leader', 'Expanding global presence and business banking services', 'https://www.stripe.com', 'press@stripe.com', 'Patrick Collison', 'San Francisco, CA', 'Private', NULL, 'Developer-friendly APIs, global reach, comprehensive platform', 'Competition, regulatory complexity, scaling challenges', 'Growth', 'Advanced', 'Online Businesses', 'Global'),

('Robinhood', 'Finance', 'Menlo Park, CA', 'Medium', 3400, 1815000000, 2013, 'Financial services company', 'Commission-Free Trading', 'Individual Retail Investors', 'Stock Trading, Options, Crypto, Cash Management', 'Cloud Native, AI/ML, Real-time Data, Python, Go', 'Challenger', 'Expanding product offerings and improving user experience post-IPO', 'https://www.robinhood.com', 'press@robinhood.com', 'Vlad Tenev', 'Menlo Park, CA', 'Public', 'HOOD', 'Commission-free model, mobile-first design, young user base', 'Regulatory scrutiny, revenue concentration, user acquisition', 'Growth', 'Advanced', 'Retail Investors', 'National'),

('Coinbase', 'Finance', 'San Francisco, CA', 'Medium', 3730, 7840000000, 2012, 'Cryptocurrency exchange platform', 'Crypto Exchange', 'Individual Investors, Institutional Investors', 'Crypto Trading, Custody, NFTs, DeFi Services', 'Cloud Native, Blockchain, AI/ML, Python, Go, Solidity', 'Leader', 'Leading cryptocurrency exchange expanding institutional services', 'https://www.coinbase.com', 'press@coinbase.com', 'Brian Armstrong', 'San Francisco, CA', 'Public', 'COIN', 'Market leader in crypto, regulatory compliance, institutional focus', 'Crypto market volatility, regulatory uncertainty, competition', 'Growth', 'Advanced', 'Crypto Users', 'Global'),

('SoFi', 'Finance', 'San Francisco, CA', 'Medium', 4500, 1277000000, 2011, 'Digital personal finance company', 'Digital Banking & Lending', 'Young Professionals, Students, Mass Affluent', 'Personal Loans, Student Loans, Mortgages, Investment, Banking', 'Cloud Native, AI/ML, Mobile-First, Python, Java', 'Challenger', 'Expanding digital banking services and gaining bank charter benefits', 'https://www.sofi.com', 'press@sofi.com', 'Anthony Noto', 'San Francisco, CA', 'Public', 'SOFI', 'Digital-native approach, comprehensive financial platform, strong brand', 'Credit risk, funding costs, intense competition', 'Growth', 'Advanced', 'Millennials', 'National'),

('Klarna', 'Finance', 'Stockholm, Sweden', 'Large', 5000, 1629000000, 2005, 'Buy now, pay later service provider', 'BNPL & Shopping Platform', 'Consumers, Merchants', 'Buy Now Pay Later, Shopping App, Banking Services', 'Cloud Native, AI/ML, Mobile-First, Python, Java, Scala', 'Leader', 'Expanding globally and diversifying into broader financial services', 'https://www.klarna.com', 'press@klarna.com', 'Sebastian Siemiatkowski', 'Stockholm, Sweden', 'Private', NULL, 'BNPL market leader, shopping platform, global presence', 'Regulatory scrutiny, credit risk, intense competition', 'Growth', 'Advanced', 'Millennials & Gen Z', 'Global'),

('Affirm', 'Finance', 'San Francisco, CA', 'Medium', 2700, 1345000000, 2012, 'Financial technology company', 'BNPL & Consumer Lending', 'Consumers, Merchants', 'Buy Now Pay Later, Personal Loans, Savings', 'Cloud Native, AI/ML, Real-time Decisioning, Python, Go', 'Challenger', 'Expanding merchant partnerships and international presence', 'https://www.affirm.com', 'press@affirm.com', 'Max Levchin', 'San Francisco, CA', 'Public', 'AFRM', 'Transparent lending, strong merchant network, AI-driven underwriting', 'Credit losses, funding costs, competitive pressure', 'Growth', 'Advanced', 'Millennials', 'North America'),

('Plaid', 'Finance', 'San Francisco, CA', 'Medium', 1100, 500000000, 2013, 'Financial technology company', 'Financial Data Connectivity', 'Fintech Companies, Banks, Developers', 'API Platform, Account Connectivity, Identity Verification', 'Cloud Native, APIs, Real-time Data, Python, Go', 'Leader', 'Expanding internationally and launching new data products', 'https://www.plaid.com', 'press@plaid.com', 'Zach Perret', 'San Francisco, CA', 'Private', NULL, 'API platform leader, strong developer ecosystem, data connectivity', 'Privacy regulations, bank relationships, competition', 'Growth', 'Advanced', 'Fintech Developers', 'North America'),

('Chime', 'Finance', 'San Francisco, CA', 'Medium', 1500, 2000000000, 2013, 'Digital banking platform', 'Digital Banking', 'Underbanked Consumers, Millennials', 'Checking Accounts, Savings, Credit Building, Early Pay', 'Cloud Native, AI/ML, Mobile-First, Python, Java', 'Challenger', 'Expanding product suite and improving path to profitability', 'https://www.chime.com', 'press@chime.com', 'Chris Britt', 'San Francisco, CA', 'Private', NULL, 'Fee-free banking, large user base, mobile-first experience', 'Interchange revenue dependence, regulatory scrutiny, profitability', 'Growth', 'Advanced', 'Underbanked', 'National'),

('Credit Karma', 'Finance', 'San Francisco, CA', 'Medium', 1400, 1000000000, 2007, 'Personal finance platform', 'Credit Monitoring & Financial Marketplace', 'Consumers Seeking Credit Information', 'Credit Monitoring, Financial Products, Tax Filing', 'Cloud Computing, AI/ML, Data Analytics, Python, Java', 'Leader', 'Acquired by Intuit, integrating with broader financial ecosystem', 'https://www.creditkarma.com', 'press@creditkarma.com', 'Kenneth Lin', 'San Francisco, CA', 'Subsidiary', NULL, 'Free credit monitoring, large user base, financial marketplace', 'Data privacy concerns, regulatory compliance, user monetization', 'Mature', 'High', 'Credit Conscious', 'National'),

('LendingClub', 'Finance', 'San Francisco, CA', 'Medium', 1200, 711000000, 2007, 'Digital marketplace bank', 'Digital Lending & Banking', 'Consumers, Small Business, Investors', 'Personal Loans, Auto Loans, Business Loans, Savings', 'Cloud Computing, AI/ML, Risk Analytics, Python, Java', 'Challenger', 'Operating as a bank post-acquisition, focusing on digital lending', 'https://www.lendingclub.com', 'IR@lendingclub.com', 'Scott Sanborn', 'San Francisco, CA', 'Public', 'LC', 'Digital lending expertise, bank charter, data-driven underwriting', 'Credit risk, funding costs, regulatory compliance', 'Mature', 'High', 'Prime Borrowers', 'National'),

('Upstart', 'Finance', 'San Mateo, CA', 'Medium', 1000, 849000000, 2012, 'AI lending platform', 'AI-Powered Lending', 'Consumers, Auto Buyers, Bank Partners', 'Personal Loans, Auto Loans, AI Underwriting Platform', 'Cloud Native, AI/ML, Advanced Analytics, Python, TensorFlow', 'Challenger', 'Expanding AI lending platform to more verticals and partners', 'https://www.upstart.com', 'IR@upstart.com', 'Dave Girouard', 'San Mateo, CA', 'Public', 'UPST', 'AI-powered underwriting, strong automation, partner network', 'Credit risk, economic sensitivity, model performance', 'Growth', 'Advanced', 'Prime Borrowers', 'National'),

('Marqeta', 'Finance', 'Oakland, CA', 'Medium', 800, 634000000, 2010, 'Payment card issuing platform', 'Card Issuing Platform', 'Fintech Companies, Banks, Enterprises', 'Card Issuing APIs, Payment Processing, Program Management', 'Cloud Native, APIs, Real-time Processing, Java, Python', 'Challenger', 'Expanding globally and adding new payment capabilities', 'https://www.marqeta.com', 'IR@marqeta.com', 'Simon Khalaf', 'Oakland, CA', 'Public', 'MQ', 'Modern card issuing platform, API-first approach, fast deployment', 'Competition, customer concentration, scaling challenges', 'Growth', 'Advanced', 'Fintech & Enterprise', 'Global'),

('Rocket Companies', 'Finance', 'Detroit, MI', 'Large', 24000, 15730000000, 1985, 'Financial services company', 'Digital Mortgage & Financial Services', 'Home Buyers, Homeowners, Real Estate Professionals', 'Mortgage Lending, Real Estate Services, Personal Loans, Insurance', 'Cloud Computing, AI/ML, Mobile-First, Python, Java', 'Leader', 'Leading digital mortgage platform expanding into broader financial services', 'https://www.rocketcompanies.com', 'IR@rocketcompanies.com', 'Jay Farner', 'Detroit, MI', 'Public', 'RKT', 'Digital mortgage leadership, strong brand, integrated platform', 'Interest rate sensitivity, regulatory compliance, market cyclicality', 'Mature', 'High', 'Homebuyers', 'National');

-- Insert comprehensive healthcare company data (30 companies)
INSERT INTO healthcare_companies (company_name, industry, location, company_size, employee_count, revenue, founding_year, description, business_model, target_market, key_services, technology_stack, market_position, recent_news, website_url, contact_email, ceo_name, headquarters, financial_status, stock_symbol, competitive_advantages, challenges, growth_stage, digital_transformation_level, customer_base_size, geographic_presence) VALUES

('Johnson & Johnson', 'Healthcare', 'New Brunswick, NJ', 'Enterprise', 144500, 94943000000, 1886, 'Multinational pharmaceutical, medical technologies and consumer products corporation', 'Diversified Healthcare', 'Patients, Healthcare Providers, Consumers', 'Pharmaceuticals, Medical Devices, Consumer Products', 'Cloud Computing, AI/ML, IoT, Java, Python, R', 'Leader', 'Leading COVID-19 vaccine development and digital health initiatives', 'https://www.jnj.com', 'investor.relations@jnj.com', 'Joaquin Duato', 'New Brunswick, NJ', 'Public', 'JNJ', 'Diversified portfolio, strong R&D, global reach', 'Patent expirations, regulatory compliance, litigation risks', 'Mature', 'High', 'Global Healthcare', 'Global'),

('Pfizer', 'Healthcare', 'New York, NY', 'Enterprise', 79000, 100330000000, 1849, 'American multinational pharmaceutical and biotechnology corporation', 'Pharmaceutical Development & Manufacturing', 'Patients, Healthcare Providers, Governments', 'Prescription Medicines, Vaccines, Oncology, Rare Diseases', 'Cloud Native, AI/ML, Data Analytics, Python, R, SAS', 'Leader', 'COVID-19 vaccine success and expansion of mRNA platform', 'https://www.pfizer.com', 'investor.relations@pfizer.com', 'Albert Bourla', 'New York, NY', 'Public', 'PFE', 'mRNA expertise, strong vaccine portfolio, global manufacturing', 'Patent cliffs, regulatory risks, R&D productivity', 'Mature', 'Advanced', 'Global Healthcare', 'Global'),

('UnitedHealth Group', 'Healthcare', 'Minnetonka, MN', 'Enterprise', 400000, 324162000000, 1977, 'Diversified health care company', 'Managed Healthcare & Health Services', 'Consumers, Employers, Government Programs', 'Health Insurance, Pharmacy Benefits, Health Services, Technology', 'Cloud Computing, AI/ML, Big Data, Java, Python, .NET', 'Leader', 'Expanding technology-enabled healthcare services and value-based care', 'https://www.unitedhealthgroup.com', 'investor.relations@uhg.com', 'Andrew Witty', 'Minnetonka, MN', 'Public', 'UNH', 'Integrated model, data analytics, scale advantages', 'Healthcare cost inflation, regulatory changes, provider relations', 'Mature', 'Advanced', 'Mass Market', 'National'),

('Abbott Laboratories', 'Healthcare', 'Abbott Park, IL', 'Enterprise', 115000, 43653000000, 1888, 'American multinational medical devices and health care company', 'Medical Devices & Diagnostics', 'Patients, Healthcare Providers, Laboratories', 'Medical Devices, Diagnostics, Nutritionals, Pharmaceuticals', 'Cloud Computing, AI/ML, IoT, Sensors, Java, Python', 'Leader', 'Leading continuous glucose monitoring and point-of-care diagnostics', 'https://www.abbott.com', 'investor.relations@abbott.com', 'Robert Ford', 'Abbott Park, IL', 'Public', 'ABT', 'Innovation in diabetes care, strong diagnostics, global reach', 'Competitive pressure, regulatory approval timelines, supply chain', 'Mature', 'High', 'Global Healthcare', 'Global'),

('Merck & Co.', 'Healthcare', 'Rahway, NJ', 'Enterprise', 68000, 59283000000, 1668, 'American multinational pharmaceutical company', 'Pharmaceutical Research & Development', 'Patients, Healthcare Providers, Governments', 'Prescription Medicines, Vaccines, Animal Health Products', 'Cloud Computing, AI/ML, Bioinformatics, Python, R, Java', 'Leader', 'Leading immunotherapy treatments and expanding vaccine portfolio', 'https://www.merck.com', 'investor_relations@merck.com', 'Robert Davis', 'Rahway, NJ', 'Public', 'MRK', 'Oncology leadership, vaccine expertise, strong pipeline', 'Patent expirations, R&D risks, competitive pressure', 'Mature', 'High', 'Global Healthcare', 'Global'),

('Bristol Myers Squibb', 'Healthcare', 'New York, NY', 'Enterprise', 34300, 46385000000, 1887, 'American multinational pharmaceutical company', 'Biopharmaceutical Research & Development', 'Patients with Serious Diseases', 'Oncology, Immunology, Cardiovascular, Fibrosis Treatments', 'Cloud Computing, AI/ML, Bioinformatics, Python, R, Spotfire', 'Leader', 'Focus on innovative treatments for cancer and immune diseases', 'https://www.bms.com', 'investor.relations@bms.com', 'Giovanni Caforio', 'New York, NY', 'Public', 'BMY', 'Oncology expertise, immunology focus, strong R&D', 'Patent expirations, clinical trial risks, competitive markets', 'Mature', 'High', 'Specialty Healthcare', 'Global'),

('AstraZeneca', 'Healthcare', 'Cambridge, UK', 'Enterprise', 83100, 44354000000, 1999, 'British-Swedish multinational pharmaceutical and biotechnology company', 'Biopharmaceutical Research & Development', 'Patients, Healthcare Systems, Governments', 'Oncology, Cardiovascular, Respiratory, Immunology Medicines', 'Cloud Computing, AI/ML, Genomics, Python, R, AWS', 'Leader', 'Strong oncology pipeline and COVID-19 vaccine development', 'https://www.astrazeneca.com', 'investor.relations@astrazeneca.com', 'Pascal Soriot', 'Cambridge, UK', 'Public', 'AZN', 'Strong oncology pipeline, respiratory franchise, emerging markets', 'R&D execution, regulatory approvals, market access', 'Mature', 'Advanced', 'Global Healthcare', 'Global'),

('Novartis', 'Healthcare', 'Basel, Switzerland', 'Enterprise', 108000, 51626000000, 1996, 'Swiss multinational pharmaceutical corporation', 'Innovative Pharmaceuticals', 'Patients with Serious Medical Conditions', 'Innovative Medicines, Generics, Eye Care, Advanced Therapies', 'Cloud Computing, AI/ML, Digital Health, Python, R, Spotfire', 'Leader', 'Leading gene and cell therapy development and digital health solutions', 'https://www.novartis.com', 'investor.relations@novartis.com', 'Vas Narasimhan', 'Basel, Switzerland', 'Public', 'NVS', 'Innovation leadership, gene therapy, strong pipeline', 'Patent expirations, regulatory challenges, market competition', 'Mature', 'Advanced', 'Global Healthcare', 'Global'),

('Roche', 'Healthcare', 'Basel, Switzerland', 'Enterprise', 101465, 68220000000, 1896, 'Swiss multinational healthcare company', 'Pharmaceuticals & Diagnostics', 'Patients, Healthcare Providers, Laboratories', 'Pharmaceuticals, Diagnostics, Personalized Medicine', 'Cloud Computing, AI/ML, Genomics, Java, Python, R', 'Leader', 'Leading personalized medicine and companion diagnostics', 'https://www.roche.com', 'investor.relations@roche.com', 'Severin Schwan', 'Basel, Switzerland', 'Public', 'ROG.SW', 'Personalized medicine, diagnostics integration, oncology leadership', 'Biosimilar competition, regulatory complexity, R&D costs', 'Mature', 'Advanced', 'Global Healthcare', 'Global'),

('GlaxoSmithKline', 'Healthcare', 'London, UK', 'Enterprise', 95000, 45755000000, 2000, 'British multinational pharmaceutical and biotechnology company', 'Pharmaceutical & Consumer Healthcare', 'Patients, Healthcare Providers, Consumers', 'Prescription Medicines, Vaccines, Consumer Healthcare Products', 'Cloud Computing, AI/ML, Data Science, Python, R, SAS', 'Challenger', 'Spin-off of consumer healthcare business and vaccine focus', 'https://www.gsk.com', 'investor.relations@gsk.com', 'Emma Walmsley', 'London, UK', 'Public', 'GSK', 'Vaccine expertise, respiratory franchise, emerging markets', 'Pipeline execution, competitive pressure, regulatory challenges', 'Mature', 'High', 'Global Healthcare', 'Global'),

-- Additional 20 healthcare companies
('Anthem', 'Healthcare', 'Indianapolis, IN', 'Enterprise', 70000, 138640000000, 1944, 'Health insurance company', 'Managed Healthcare', 'Individuals, Families, Employers, Government Programs', 'Health Insurance, Pharmacy Benefits, Medical Management', 'Cloud Computing, AI/ML, Big Data Analytics, Java, Python', 'Leader', 'Rebranding to Elevance Health and expanding healthcare services', 'https://www.antheminc.com', 'investor.relations@anthem.com', 'Gail Boudreaux', 'Indianapolis, IN', 'Public', 'ANTM', 'Scale advantages, government program expertise, data analytics', 'Healthcare cost inflation, regulatory changes, medical utilization', 'Mature', 'High', 'Mass Market', 'National'),

('CVS Health', 'Healthcare', 'Woonsocket, RI', 'Enterprise', 300000, 292111000000, 1963, 'Integrated healthcare services company', 'Integrated Healthcare Services', 'Consumers, Patients, Healthcare Providers', 'Pharmacy Services, Health Insurance, Retail Healthcare', 'Cloud Computing, AI/ML, IoT, Java, Python, .NET', 'Leader', 'Expanding HealthHub locations and integrated care model', 'https://www.cvshealth.com', 'investor.relations@cvshealth.com', 'Karen Lynch', 'Woonsocket, RI', 'Public', 'CVS', 'Integrated model, retail presence, pharmacy benefits scale', 'Healthcare cost management, competitive pressure, integration complexity', 'Mature', 'High', 'Mass Market', 'National'),

('Humana', 'Healthcare', 'Louisville, KY', 'Large', 65000, 83096000000, 1961, 'Health insurance company', 'Medicare Advantage & Health Services', 'Medicare Beneficiaries, Medicaid Members', 'Medicare Advantage, Medicaid, Pharmacy Benefits, Provider Services', 'Cloud Computing, AI/ML, Predictive Analytics, Java, Python', 'Leader', 'Leading Medicare Advantage provider expanding value-based care', 'https://www.humana.com', 'investor.relations@humana.com', 'Bruce Broussard', 'Louisville, KY', 'Public', 'HUM', 'Medicare Advantage expertise, value-based care, data analytics', 'Regulatory changes, medical cost trends, Star ratings performance', 'Mature', 'High', 'Medicare & Medicaid', 'National'),

('Cigna', 'Healthcare', 'Bloomfield, CT', 'Enterprise', 70000, 174091000000, 1982, 'Health services company', 'Health Services & Insurance', 'Individuals, Families, Employers, Government', 'Health Insurance, Pharmacy Benefits, Medical Services', 'Cloud Computing, AI/ML, Data Analytics, Java, Python', 'Leader', 'Focus on Evernorth health services business growth', 'https://www.cigna.com', 'investor.relations@cigna.com', 'David Cordani', 'Bloomfield, CT', 'Public', 'CI', 'Integrated services, pharmacy benefits scale, global presence', 'Healthcare cost inflation, competitive markets, regulatory compliance', 'Mature', 'High', 'Employer Market', 'Global'),

('Aetna (CVS)', 'Healthcare', 'Hartford, CT', 'Large', 50000, 84156000000, 1853, 'Health insurance company', 'Health Insurance & Benefits', 'Individuals, Employers, Government Programs', 'Health Insurance, Medicare, Medicaid, Dental, Vision', 'Cloud Computing, AI/ML, Member Analytics, Java, .NET', 'Challenger', 'Integration with CVS Health creating integrated care model', 'https://www.aetna.com', 'investor.relations@aetna.com', 'Dan Finke', 'Hartford, CT', 'Subsidiary', NULL, 'CVS integration, provider networks, government programs', 'Integration challenges, competitive pressure, medical costs', 'Mature', 'High', 'Employer & Government', 'National'),

('Eli Lilly', 'Healthcare', 'Indianapolis, IN', 'Large', 35000, 28318000000, 1876, 'Pharmaceutical company', 'Pharmaceutical Research & Manufacturing', 'Patients with Diabetes, Cancer, Neurological Conditions', 'Diabetes Care, Oncology, Immunology, Neuroscience', 'Cloud Computing, AI/ML, Bioinformatics, Python, R', 'Leader', 'Leading Alzheimer\'s treatment development and diabetes innovation', 'https://www.lilly.com', 'investor.relations@lilly.com', 'David Ricks', 'Indianapolis, IN', 'Public', 'LLY', 'Diabetes franchise, Alzheimer\'s research, strong pipeline', 'Clinical trial risks, patent expirations, regulatory approval', 'Mature', 'High', 'Chronic Disease Patients', 'Global'),

('Gilead Sciences', 'Healthcare', 'Foster City, CA', 'Large', 14800, 27300000000, 1987, 'Biopharmaceutical company', 'Antiviral & Oncology Therapeutics', 'Patients with HIV, Hepatitis, Cancer', 'Antiviral Medicines, Oncology Treatments, Inflammatory Diseases', 'Cloud Computing, AI/ML, Bioinformatics, Python, R, Java', 'Leader', 'Expanding oncology portfolio and cell therapy capabilities', 'https://www.gilead.com', 'investor.relations@gilead.com', 'Daniel O\'Day', 'Foster City, CA', 'Public', 'GILD', 'HIV franchise, antiviral expertise, cell therapy platform', 'Patent expirations, competitive pressure, R&D productivity', 'Mature', 'High', 'Specialty Patient Populations', 'Global'),

('Moderna', 'Healthcare', 'Cambridge, MA', 'Medium', 3900, 18471000000, 2010, 'Biotechnology company', 'mRNA Therapeutics & Vaccines', 'Patients, Healthcare Systems, Governments', 'mRNA Vaccines, Therapeutic Development, Platform Technologies', 'Cloud Native, AI/ML, Bioinformatics, Python, R, AWS', 'Challenger', 'Expanding mRNA platform beyond COVID-19 to other diseases', 'https://www.modernatx.com', 'investor.relations@modernatx.com', 'Stéphane Bancel', 'Cambridge, MA', 'Public', 'MRNA', 'mRNA platform technology, rapid development capabilities, strong IP', 'Platform validation, competitive threats, manufacturing scale', 'Growth', 'Advanced', 'Global Healthcare', 'Global'),

('Regeneron', 'Healthcare', 'Tarrytown, NY', 'Large', 11000, 16072000000, 1988, 'Biotechnology company', 'Biotechnology Research & Development', 'Patients with Serious Diseases', 'Monoclonal Antibodies, Gene Therapies, Immuno-oncology', 'Cloud Computing, AI/ML, Genomics, Python, R, Bioinformatics', 'Leader', 'Leading COVID-19 antibody treatment and eye disease therapies', 'https://www.regeneron.com', 'investor.relations@regeneron.com', 'Leonard Schleifer', 'Tarrytown, NY', 'Public', 'REGN', 'Platform technologies, strong R&D, ophthalmology leadership', 'Clinical development risks, competitive pressure, patent protection', 'Mature', 'Advanced', 'Specialty Patient Populations', 'Global'),

('Biogen', 'Healthcare', 'Cambridge, MA', 'Large', 7800, 10982000000, 1978, 'Biotechnology company', 'Neurological & Neurodegenerative Therapeutics', 'Patients with Neurological Conditions', 'Multiple Sclerosis, Alzheimer\'s, Spinal Muscular Atrophy Treatments', 'Cloud Computing, AI/ML, Neuroinformatics, Python, R', 'Challenger', 'Focus on Alzheimer\'s treatment Aduhelm and pipeline development', 'https://www.biogen.com', 'investor.relations@biogen.com', 'Michel Vounatsos', 'Cambridge, MA', 'Public', 'BIIB', 'Neuroscience expertise, Alzheimer\'s focus, strong R&D capabilities', 'Aduhelm controversy, competitive MS market, clinical execution', 'Mature', 'High', 'Neurological Patients', 'Global'),

('Vertex Pharmaceuticals', 'Healthcare', 'Boston, MA', 'Large', 5000, 8930000000, 1989, 'Biotechnology company', 'Rare Disease Therapeutics', 'Patients with Rare Diseases', 'Cystic Fibrosis, Sickle Cell Disease, Beta Thalassemia Treatments', 'Cloud Computing, AI/ML, Computational Biology, Python, R', 'Leader', 'Leading cystic fibrosis treatment and expanding to other rare diseases', 'https://www.vrtx.com', 'investor.relations@vrtx.com', 'Reshma Kewalramani', 'Boston, MA', 'Public', 'VRTX', 'Cystic fibrosis dominance, rare disease expertise, strong pipeline', 'Small patient populations, high development costs, competitive threats', 'Mature', 'High', 'Rare Disease Patients', 'Global'),

('Illumina', 'Healthcare', 'San Diego, CA', 'Large', 8600, 4526000000, 1998, 'Biotechnology company', 'Genomic Sequencing & Array Technologies', 'Research Institutions, Clinical Labs, Pharmaceutical Companies', 'DNA Sequencing, Genomic Analysis, Molecular Diagnostics', 'Cloud Native, AI/ML, Bioinformatics, Python, R, Genomics Platforms', 'Leader', 'Leading genomic sequencing technology and expanding clinical applications', 'https://www.illumina.com', 'investor.relations@illumina.com', 'Francis deSouza', 'San Diego, CA', 'Public', 'ILMN', 'Sequencing technology leadership, comprehensive platform, market dominance', 'Competitive pressure, regulatory scrutiny, technology transitions', 'Mature', 'Advanced', 'Research & Clinical Labs', 'Global'),

('Amgen', 'Healthcare', 'Thousand Oaks, CA', 'Large', 25400, 25979000000, 1980, 'Biotechnology company', 'Biotechnology Therapeutics', 'Patients with Serious Illnesses', 'Oncology, Cardiovascular, Inflammatory, Bone Health Treatments', 'Cloud Computing, AI/ML, Bioinformatics, Python, R, Java', 'Leader', 'Focus on innovative biologics and biosimilar competition management', 'https://www.amgen.com', 'investor.relations@amgen.com', 'Robert Bradway', 'Thousand Oaks, CA', 'Public', 'AMGN', 'Biotechnology expertise, strong franchises, manufacturing capabilities', 'Biosimilar competition, patent expirations, R&D productivity', 'Mature', 'High', 'Specialty Patient Populations', 'Global'),

('Danaher', 'Healthcare', 'Washington, DC', 'Enterprise', 80000, 31917000000, 1984, 'Life sciences and diagnostics company', 'Life Sciences & Diagnostics', 'Research Labs, Clinical Labs, Bioprocessing Companies', 'Life Sciences Tools, Diagnostics, Bioprocessing', 'Cloud Computing, AI/ML, IoT, Laboratory Automation, Java, Python', 'Leader', 'Leading life sciences tools and expanding bioprocessing capabilities', 'https://www.danaher.com', 'investor.relations@danaher.com', 'Rainer Blair', 'Washington, DC', 'Public', 'DHR', 'Diverse portfolio, innovation focus, operational excellence', 'End market cyclicality, competitive pressure, integration execution', 'Mature', 'High', 'Life Sciences Industry', 'Global'),

('Thermo Fisher Scientific', 'Healthcare', 'Waltham, MA', 'Enterprise', 130000, 44915000000, 1956, 'Life sciences company', 'Life Sciences Services & Products', 'Pharmaceutical, Biotech, Academic, Government, Clinical Labs', 'Analytical Instruments, Laboratory Equipment, Reagents, Software', 'Cloud Computing, AI/ML, Laboratory Informatics, Java, Python, .NET', 'Leader', 'Leading COVID-19 testing and expanding precision medicine capabilities', 'https://www.thermofisher.com', 'investor.relations@thermofisher.com', 'Marc Casper', 'Waltham, MA', 'Public', 'TMO', 'Comprehensive portfolio, scale advantages, innovation leadership', 'Economic sensitivity, competitive markets, supply chain complexity', 'Mature', 'High', 'Life Sciences Industry', 'Global'),

('Medtronic', 'Healthcare', 'Minneapolis, MN', 'Enterprise', 95000, 30117000000, 1949, 'Medical technology company', 'Medical Device Manufacturing', 'Patients, Healthcare Providers, Hospitals', 'Cardiac Devices, Surgical Technologies, Diabetes Management, Neurology', 'Cloud Computing, AI/ML, IoT, Medical Devices, Java, Python', 'Leader', 'Expanding minimally invasive therapies and diabetes technology', 'https://www.medtronic.com', 'investor.relations@medtronic.com', 'Geoff Martha', 'Minneapolis, MN', 'Public', 'MDT', 'Broad portfolio, global reach, clinical evidence', 'Device competition, regulatory approval timelines, reimbursement pressure', 'Mature', 'High', 'Global Healthcare', 'Global'),

('Boston Scientific', 'Healthcare', 'Marlborough, MA', 'Large', 46000, 12687000000, 1979, 'Medical device company', 'Medical Device Development', 'Patients, Healthcare Providers, Hospitals', 'Interventional Cardiology, Electrophysiology, Peripheral Interventions, Urology', 'Cloud Computing, AI/ML, Medical Device Software, Java, Python', 'Challenger', 'Expanding interventional oncology and structural heart programs', 'https://www.bostonscientific.com', 'investor_relations@bsci.com', 'Mike Mahoney', 'Marlborough, MA', 'Public', 'BSX', 'Innovation focus, emerging markets presence, broad portfolio', 'Competitive markets, regulatory approval processes, reimbursement challenges', 'Mature', 'High', 'Interventional Medicine', 'Global'),

('Stryker', 'Healthcare', 'Kalamazoo, MI', 'Large', 50000, 18441000000, 1941, 'Medical technology company', 'Medical Equipment & Devices', 'Hospitals, Surgery Centers, Healthcare Providers', 'Orthopedics, Medical Surgical Equipment, Neurotechnology, Spine', 'Cloud Computing, AI/ML, Robotics, Medical Devices, Java, Python', 'Leader', 'Leading surgical robotics and expanding digital surgery capabilities', 'https://www.stryker.com', 'investor.relations@stryker.com', 'Kevin Lobo', 'Kalamazoo, MI', 'Public', 'SYK', 'Innovation leadership, surgical robotics, strong franchises', 'Competitive pressure, regulatory approval timelines, capital equipment cycles', 'Mature', 'High', 'Surgical Procedures', 'Global'),

('Edwards Lifesciences', 'Healthcare', 'Irvine, CA', 'Large', 15000, 5232000000, 1958, 'Medical device company', 'Structural Heart & Critical Care', 'Patients with Cardiovascular Disease', 'Transcatheter Heart Valves, Surgical Heart Valves, Critical Care Monitoring', 'Cloud Computing, AI/ML, Medical Device Innovation, Java, Python', 'Leader', 'Leading transcatheter aortic valve replacement (TAVR) technology', 'https://www.edwards.com', 'investor.relations@edwards.com', 'Michael Mussallem', 'Irvine, CA', 'Public', 'EW', 'TAVR leadership, structural heart expertise, innovation focus', 'Competitive threats, clinical trial execution, reimbursement dynamics', 'Mature', 'High', 'Cardiovascular Patients', 'Global'),

('Intuitive Surgical', 'Healthcare', 'Sunnyvale, CA', 'Large', 8800, 6017000000, 1995, 'Medical device company', 'Robotic Surgery Systems', 'Surgeons, Hospitals, Surgery Centers', 'da Vinci Surgical Systems, Instruments, Accessories, Training', 'Cloud Computing, AI/ML, Robotics, Computer Vision, C++, Python', 'Leader', 'Leading robotic surgery with expanding procedure applications', 'https://www.intuitive.com', 'investor.relations@intuitive.com', 'Gary Guthart', 'Sunnyvale, CA', 'Public', 'ISRG', 'Robotic surgery leadership, installed base, procedure growth', 'Competitive threats, capital equipment replacement cycles, regulatory approval', 'Mature', 'Advanced', 'Surgical Procedures', 'Global');

-- Insert comprehensive technology company data (30 companies)
INSERT INTO tech_companies (company_name, industry, location, company_size, employee_count, revenue, founding_year, description, business_model, target_market, key_services, technology_stack, market_position, recent_news, website_url, contact_email, ceo_name, headquarters, financial_status, stock_symbol, competitive_advantages, challenges, growth_stage, digital_transformation_level, customer_base_size, geographic_presence) VALUES

('Apple Inc.', 'Technology', 'Cupertino, CA', 'Enterprise', 164000, 394328000000, 1976, 'Multinational technology company designing and manufacturing consumer electronics', 'Consumer Electronics & Services', 'Consumers, Businesses, Developers', 'iPhone, Mac, iPad, Apple Watch, Services, App Store', 'iOS, macOS, Swift, Objective-C, Cloud Services, AI/ML', 'Leader', 'Leading smartphone innovation and expanding services revenue', 'https://www.apple.com', 'investor.relations@apple.com', 'Tim Cook', 'Cupertino, CA', 'Public', 'AAPL', 'Brand loyalty, ecosystem integration, premium pricing power', 'Supply chain dependency, regulatory scrutiny, market saturation', 'Mature', 'Advanced', 'Global Consumer', 'Global'),

('Microsoft Corporation', 'Technology', 'Redmond, WA', 'Enterprise', 221000, 198270000000, 1975, 'Multinational technology corporation developing software, services and solutions', 'Software & Cloud Services', 'Consumers, Enterprises, Developers, Governments', 'Windows, Office 365, Azure, Teams, LinkedIn, Xbox', 'Azure Cloud, .NET, C#, TypeScript, AI/ML, Power Platform', 'Leader', 'Leading cloud computing growth and AI integration across products', 'https://www.microsoft.com', 'investor.relations@microsoft.com', 'Satya Nadella', 'Redmond, WA', 'Public', 'MSFT', 'Enterprise relationships, cloud leadership, comprehensive platform', 'Open source competition, cybersecurity threats, regulatory challenges', 'Mature', 'Advanced', 'Global Enterprise', 'Global'),

('Alphabet Inc.', 'Technology', 'Mountain View, CA', 'Enterprise', 174014, 307394000000, 1998, 'Multinational conglomerate specializing in Internet services and products', 'Digital Advertising & Cloud Services', 'Consumers, Advertisers, Enterprises, Developers', 'Search, YouTube, Android, Google Cloud, Google Ads, Maps', 'Google Cloud, TensorFlow, Kubernetes, Go, Python, AI/ML', 'Leader', 'Leading AI development and expanding cloud market share', 'https://www.abc.xyz', 'investor.relations@abc.xyz', 'Sundar Pichai', 'Mountain View, CA', 'Public', 'GOOGL', 'Search dominance, data advantage, AI/ML expertise, innovation culture', 'Regulatory pressure, privacy concerns, competition in cloud', 'Mature', 'Advanced', 'Global Internet Users', 'Global'),

('Amazon.com Inc.', 'Technology', 'Seattle, WA', 'Enterprise', 1541000, 513983000000, 1994, 'Multinational technology and e-commerce company', 'E-commerce & Cloud Computing', 'Consumers, Businesses, Developers, Enterprises', 'E-commerce, AWS, Prime, Alexa, Advertising, Logistics', 'AWS Cloud, Java, Python, React, AI/ML, Microservices', 'Leader', 'Expanding AWS services and international e-commerce growth', 'https://www.amazon.com', 'ir@amazon.com', 'Andy Jassy', 'Seattle, WA', 'Public', 'AMZN', 'Scale advantages, logistics network, cloud leadership, customer obsession', 'Regulatory scrutiny, labor relations, competitive pressure', 'Mature', 'Advanced', 'Global Consumer & Enterprise', 'Global'),

('Meta Platforms Inc.', 'Technology', 'Menlo Park, CA', 'Enterprise', 87314, 134902000000, 2004, 'Social media and metaverse technology company', 'Social Media & Virtual Reality', 'Consumers, Advertisers, Developers', 'Facebook, Instagram, WhatsApp, Messenger, VR/AR, Metaverse', 'React, GraphQL, PyTorch, PHP, Python, VR/AR Technologies', 'Leader', 'Investing heavily in metaverse and VR/AR technologies', 'https://www.meta.com', 'investor@fb.com', 'Mark Zuckerberg', 'Menlo Park, CA', 'Public', 'META', 'Social network effects, advertising platform, VR leadership', 'Privacy regulations, content moderation, metaverse adoption uncertainty', 'Mature', 'Advanced', 'Global Social Media Users', 'Global'),

('Tesla Inc.', 'Technology', 'Austin, TX', 'Large', 140473, 96773000000, 2003, 'Electric vehicle and clean energy company', 'Electric Vehicles & Energy Storage', 'Consumers, Businesses, Utilities', 'Electric Vehicles, Battery Storage, Solar Panels, Supercharger Network', 'Autopilot AI, Battery Technology, Manufacturing Innovation, Python', 'Leader', 'Leading EV market and expanding autonomous driving capabilities', 'https://www.tesla.com', 'ir@tesla.com', 'Elon Musk', 'Austin, TX', 'Public', 'TSLA', 'EV technology leadership, vertical integration, brand strength', 'Production scaling, autonomous driving challenges, competition', 'Growth', 'Advanced', 'Global EV Market', 'Global'),

('NVIDIA Corporation', 'Technology', 'Santa Clara, CA', 'Large', 29600, 126956000000, 1993, 'Multinational technology company specializing in graphics and AI computing', 'Graphics & AI Computing', 'Gamers, Data Centers, Automotive, Professionals', 'Graphics Cards, Data Center GPUs, AI Computing, Omniverse', 'CUDA, Deep Learning, GPU Computing, AI/ML Frameworks', 'Leader', 'Leading AI computing revolution and data center GPU market', 'https://www.nvidia.com', 'investor.relations@nvidia.com', 'Jensen Huang', 'Santa Clara, CA', 'Public', 'NVDA', 'AI computing leadership, CUDA ecosystem, gaming dominance', 'Cyclical demand, geopolitical risks, intense competition', 'Growth', 'Advanced', 'AI & Gaming Markets', 'Global'),

('Intel Corporation', 'Technology', 'Santa Clara, CA', 'Enterprise', 124800, 79024000000, 1968, 'Multinational semiconductor chip manufacturer', 'Semiconductor Manufacturing', 'PC Manufacturers, Data Centers, Automotive, IoT', 'CPUs, Data Center Processors, Memory, Networking, Foundry Services', 'x86 Architecture, Manufacturing Process Technology, AI Acceleration', 'Challenger', 'Investing in advanced manufacturing and competing in AI chips', 'https://www.intel.com', 'investor.relations@intel.com', 'Pat Gelsinger', 'Santa Clara, CA', 'Public', 'INTC', 'x86 ecosystem, manufacturing expertise, broad portfolio', 'Manufacturing delays, competition from AMD/ARM, foundry challenges', 'Mature', 'High', 'Global Computing', 'Global'),

('IBM', 'Technology', 'Armonk, NY', 'Enterprise', 282100, 60530000000, 1911, 'Multinational technology and consulting company', 'Enterprise Technology & Consulting', 'Enterprises, Governments, Institutions', 'Cloud Computing, AI, Consulting, Software, Mainframes', 'Red Hat, Watson AI, Hybrid Cloud, Java, Python, Open Source', 'Challenger', 'Focus on hybrid cloud and AI transformation services', 'https://www.ibm.com', 'investor.relations@ibm.com', 'Arvind Krishna', 'Armonk, NY', 'Public', 'IBM', 'Enterprise relationships, consulting expertise, hybrid cloud', 'Legacy transformation, cloud competition, talent retention', 'Mature', 'High', 'Global Enterprise', 'Global'),

('Oracle Corporation', 'Technology', 'Austin, TX', 'Enterprise', 164000, 49954000000, 1977, 'Multinational computer technology corporation', 'Enterprise Database & Cloud Applications', 'Enterprises, Governments, Developers', 'Database Software, Cloud Applications, Infrastructure, Java', 'Oracle Database, Java, MySQL, Cloud Infrastructure, AI/ML', 'Leader', 'Expanding autonomous database and cloud applications', 'https://www.oracle.com', 'investor_relations@oracle.com', 'Safra Catz', 'Austin, TX', 'Public', 'ORCL', 'Database market leadership, enterprise relationships, Java ecosystem', 'Cloud transition challenges, open source competition, SAP rivalry', 'Mature', 'High', 'Global Enterprise', 'Global'),

-- Additional 20 technology companies
('Salesforce', 'Technology', 'San Francisco, CA', 'Large', 79390, 31352000000, 1999, 'Cloud-based software company', 'SaaS CRM & Platform', 'Businesses, Sales Teams, Marketers, Developers', 'CRM, Sales Cloud, Service Cloud, Marketing Cloud, Platform', 'Salesforce Platform, Apex, Lightning, AI/ML, Multi-tenant SaaS', 'Leader', 'Leading CRM platform expanding with AI and industry-specific solutions', 'https://www.salesforce.com', 'investor.relations@salesforce.com', 'Marc Benioff', 'San Francisco, CA', 'Public', 'CRM', 'CRM market leadership, platform ecosystem, customer success focus', 'Competition from Microsoft, customer acquisition costs, integration complexity', 'Mature', 'Advanced', 'Global Business', 'Global'),

('Adobe Inc.', 'Technology', 'San Jose, CA', 'Large', 28000, 19411000000, 1982, 'Multinational computer software company', 'Creative & Digital Experience Software', 'Creatives, Marketers, Enterprises, Developers', 'Creative Cloud, Document Cloud, Experience Cloud, Digital Marketing', 'Creative Suite, PDF, Web Technologies, AI/ML, Cloud Services', 'Leader', 'Leading digital creativity and customer experience management', 'https://www.adobe.com', 'ir@adobe.com', 'Shantanu Narayen', 'San Jose, CA', 'Public', 'ADBE', 'Creative market dominance, subscription model, innovation leadership', 'Creative software competition, economic sensitivity, customer retention', 'Mature', 'Advanced', 'Creatives & Enterprises', 'Global'),

('ServiceNow', 'Technology', 'Santa Clara, CA', 'Large', 22000, 8097000000, 2003, 'Cloud computing platform company', 'Enterprise Service Management', 'Enterprises, IT Departments, HR, Customer Service', 'IT Service Management, HR Service Delivery, Customer Service Management', 'ServiceNow Platform, JavaScript, REST APIs, AI/ML, Workflow Automation', 'Leader', 'Expanding platform to enterprise-wide digital workflows', 'https://www.servicenow.com', 'investor.relations@servicenow.com', 'Bill McDermott', 'Santa Clara, CA', 'Public', 'NOW', 'Platform approach, workflow automation, strong customer relationships', 'Competition from larger players, market expansion challenges, talent costs', 'Growth', 'Advanced', 'Global Enterprise', 'Global'),

('Workday', 'Technology', 'Pleasanton, CA', 'Large', 18000, 6222000000, 2005, 'Enterprise cloud applications for finance and human resources', 'Enterprise SaaS Applications', 'Enterprises, HR Departments, Finance Teams', 'Human Capital Management, Financial Management, Analytics', 'Workday Platform, Java, Machine Learning, Cloud-native Architecture', 'Leader', 'Leading cloud-based HCM and expanding financial management solutions', 'https://www.workday.com', 'investor.relations@workday.com', 'Aneel Bhusri', 'Pleasanton, CA', 'Public', 'WDAY', 'Cloud-native architecture, user experience, comprehensive HCM', 'ERP competition, international expansion, customer concentration', 'Growth', 'Advanced', 'Mid to Large Enterprise', 'Global'),

('Snowflake', 'Technology', 'Bozeman, MT', 'Medium', 6000, 2817000000, 2012, 'Cloud-based data platform company', 'Cloud Data Platform', 'Enterprises, Data Teams, Analytics Teams', 'Data Warehouse, Data Lake, Data Exchange, Analytics', 'Cloud-native Architecture, SQL, Python, Scala, Multi-cloud', 'Challenger', 'Leading modern data stack with cloud-native data platform', 'https://www.snowflake.com', 'investor.relations@snowflake.com', 'Frank Slootman', 'Bozeman, MT', 'Public', 'SNOW', 'Cloud-native architecture, ease of use, consumption-based model', 'Data warehouse competition, customer acquisition costs, execution risk', 'Growth', 'Advanced', 'Data-driven Enterprises', 'Global'),

('Palantir Technologies', 'Technology', 'Denver, CO', 'Medium', 3500, 2232000000, 2003, 'Big data analytics company', 'Data Analytics & AI Platform', 'Government, Defense, Enterprises', 'Data Integration, Analytics, AI/ML, Decision Support', 'Palantir Gotham, Foundry, Python, Java, Machine Learning', 'Challenger', 'Expanding commercial business and AI-powered analytics', 'https://www.palantir.com', 'investor.relations@palantir.com', 'Alex Karp', 'Denver, CO', 'Public', 'PLTR', 'Government relationships, complex data integration, AI capabilities', 'Commercial market penetration, competition, controversial government work', 'Growth', 'Advanced', 'Government & Enterprise', 'Global'),

('Zoom Video Communications', 'Technology', 'San Jose, CA', 'Medium', 8400, 4393000000, 2011, 'Video communications platform', 'Video Communications & Collaboration', 'Businesses, Educational Institutions, Consumers', 'Video Conferencing, Phone, Webinars, Cloud Contact Center', 'Cloud-based Video, WebRTC, AI/ML, Real-time Communications', 'Leader', 'Expanding platform beyond video with communications hub', 'https://www.zoom.us', 'investor.relations@zoom.us', 'Eric Yuan', 'San Jose, CA', 'Public', 'ZM', 'Video quality, ease of use, platform reliability', 'Post-pandemic normalization, Microsoft competition, security concerns', 'Mature', 'Advanced', 'Global Business', 'Global'),

('Slack Technologies', 'Technology', 'San Francisco, CA', 'Medium', 2500, 1500000000, 2009, 'Business communication platform', 'Team Collaboration Software', 'Businesses, Teams, Developers', 'Team Messaging, File Sharing, App Integration, Workflow Automation', 'Slack Platform, APIs, JavaScript, Python, Real-time Messaging', 'Challenger', 'Acquired by Salesforce, integrating with broader business platform', 'https://www.slack.com', 'ir@salesforce.com', 'Stewart Butterfield', 'San Francisco, CA', 'Subsidiary', NULL, 'Team adoption, developer ecosystem, workflow integration', 'Microsoft Teams competition, enterprise adoption, monetization', 'Growth', 'Advanced', 'Knowledge Workers', 'Global'),

('Atlassian', 'Technology', 'Sydney, Australia', 'Large', 11000, 3066000000, 2002, 'Software development and collaboration tools', 'Developer & Team Collaboration Tools', 'Software Teams, IT Teams, Businesses', 'Jira, Confluence, Bitbucket, Trello, Opsgenie', 'Atlassian Platform, Java, JavaScript, REST APIs, Cloud Services', 'Leader', 'Leading agile development tools and expanding team collaboration', 'https://www.atlassian.com', 'investor.relations@atlassian.com', 'Mike Cannon-Brookes', 'Sydney, Australia', 'Public', 'TEAM', 'Developer tool dominance, strong ecosystem, cloud migration', 'Competition from Microsoft/GitHub, enterprise sales, cloud transition', 'Growth', 'Advanced', 'Software Development Teams', 'Global'),

('Shopify', 'Technology', 'Ottawa, Canada', 'Large', 12000, 5598000000, 2006, 'E-commerce platform company', 'E-commerce Platform & Services', 'Small to Medium Businesses, Entrepreneurs', 'E-commerce Platform, Payments, Shipping, Marketing, Analytics', 'Ruby on Rails, React, GraphQL, Cloud Infrastructure, AI/ML', 'Leader', 'Leading e-commerce platform for SMBs with expanding enterprise focus', 'https://www.shopify.com', 'investor.relations@shopify.com', 'Tobi Lütke', 'Ottawa, Canada', 'Public', 'SHOP', 'SMB e-commerce leadership, comprehensive platform, developer ecosystem', 'Amazon competition, economic sensitivity, international expansion', 'Growth', 'Advanced', 'E-commerce Businesses', 'Global'),

('Square (Block)', 'Technology', 'San Francisco, CA', 'Large', 8000, 17661000000, 2009, 'Financial services and digital payments company', 'Digital Payments & Financial Services', 'Small Business, Individual Consumers', 'Payment Processing, Point of Sale, Cash App, Bitcoin Services', 'Cloud Native, AI/ML, Blockchain, Python, Java, Go', 'Leader', 'Focus on Bitcoin and decentralized financial services', 'https://www.block.xyz', 'ir@block.xyz', 'Jack Dorsey', 'San Francisco, CA', 'Public', 'SQ', 'Small business focus, Cash App growth, Bitcoin integration', 'Competition, regulatory uncertainty, Bitcoin volatility', 'Growth', 'Advanced', 'Small Business', 'National'),

('Twilio', 'Technology', 'San Francisco, CA', 'Medium', 10000, 4140000000, 2008, 'Customer engagement platform', 'Communications Platform as a Service', 'Developers, Businesses, Customer Experience Teams', 'Messaging, Voice, Video, Email, Customer Data Platform', 'REST APIs, JavaScript, Python, Ruby, Real-time Communications', 'Leader', 'Leading CPaaS provider expanding customer data and engagement platform', 'https://www.twilio.com', 'investor.relations@twilio.com', 'Jeff Lawson', 'San Francisco, CA', 'Public', 'TWLO', 'Developer-first approach, comprehensive communications APIs, scale', 'Competition, customer concentration, execution challenges', 'Growth', 'Advanced', 'Developers & Enterprises', 'Global'),

('MongoDB', 'Technology', 'New York, NY', 'Medium', 4500, 1284000000, 2007, 'Database platform company', 'Modern Database Platform', 'Developers, Enterprises, Startups', 'Document Database, Atlas Cloud, Mobile, Analytics', 'MongoDB Database, BSON, JavaScript, Python, Cloud Services', 'Leader', 'Leading modern database for cloud applications and developer productivity', 'https://www.mongodb.com', 'investor.relations@mongodb.com', 'Dev Ittycheria', 'New York, NY', 'Public', 'MDB', 'Developer adoption, cloud-native architecture, document model flexibility', 'Database competition, cloud vendor relationships, enterprise adoption', 'Growth', 'Advanced', 'Developers & Enterprises', 'Global'),

('Datadog', 'Technology', 'New York, NY', 'Medium', 6000, 1675000000, 2010, 'Monitoring and security platform', 'Cloud Monitoring & Observability', 'Developers, DevOps Teams, IT Operations', 'Application Monitoring, Infrastructure Monitoring, Log Management, Security', 'SaaS Platform, Time-series Database, AI/ML, Real-time Analytics', 'Leader', 'Leading application performance monitoring and expanding security', 'https://www.datadoghq.com', 'investor.relations@datadoghq.com', 'Olivier Pomel', 'New York, NY', 'Public', 'DDOG', 'Comprehensive monitoring platform, strong growth, cloud-native focus', 'Competition, customer expansion, product execution', 'Growth', 'Advanced', 'Cloud-native Organizations', 'Global'),

('CrowdStrike', 'Technology', 'Austin, TX', 'Medium', 8000, 2242000000, 2011, 'Cybersecurity technology company', 'Cloud-native Cybersecurity', 'Enterprises, Government, SMBs', 'Endpoint Protection, Threat Intelligence, Identity Protection, Cloud Security', 'Falcon Platform, AI/ML, Cloud-native Architecture, Threat Intelligence', 'Leader', 'Leading next-generation endpoint protection and cloud security', 'https://www.crowdstrike.com', 'investor.relations@crowdstrike.com', 'George Kurtz', 'Austin, TX', 'Public', 'CRWD', 'Cloud-native platform, AI-powered threat detection, rapid deployment', 'Cybersecurity competition, talent costs, execution risk', 'Growth', 'Advanced', 'Security-conscious Organizations', 'Global'),

('Okta', 'Technology', 'San Francisco, CA', 'Medium', 6000, 1840000000, 2009, 'Identity and access management company', 'Identity & Access Management', 'Enterprises, IT Teams, Developers', 'Single Sign-On, Multi-Factor Authentication, Lifecycle Management, API Access', 'Identity Cloud, SAML, OAuth, REST APIs, Cloud Services', 'Leader', 'Leading cloud identity platform expanding zero trust security', 'https://www.okta.com', 'investor.relations@okta.com', 'Todd McKinnon', 'San Francisco, CA', 'Public', 'OKTA', 'Identity platform leadership, integration ecosystem, cloud-first approach', 'Microsoft competition, security breaches impact, customer concentration', 'Growth', 'Advanced', 'Cloud-first Enterprises', 'Global'),

('Splunk', 'Technology', 'San Francisco, CA', 'Medium', 7500, 3014000000, 2003, 'Data platform company', 'Data Analytics & Observability', 'Enterprises, IT Operations, Security Teams', 'Data Analytics, SIEM, IT Operations, Application Monitoring', 'Splunk Platform, SPL, Machine Learning, Cloud Services', 'Leader', 'Transitioning to cloud and expanding observability platform', 'https://www.splunk.com', 'investor.relations@splunk.com', 'Gary Steele', 'San Francisco, CA', 'Public', 'SPLK', 'Data analytics expertise, enterprise relationships, security focus', 'Cloud transition, competition, customer retention during transformation', 'Mature', 'High', 'Enterprise IT & Security', 'Global'),

('DocuSign', 'Technology', 'San Francisco, CA', 'Medium', 7000, 2543000000, 2003, 'Electronic signature and digital transaction management', 'Digital Agreement Cloud', 'Businesses, Legal Teams, Sales Teams', 'Electronic Signature, Contract Lifecycle Management, Document Generation', 'Agreement Cloud, APIs, Mobile Apps, AI/ML, Cloud Services', 'Leader', 'Leading e-signature expanding into contract lifecycle management', 'https://www.docusign.com', 'investor.relations@docusign.com', 'Dan Springer', 'San Francisco, CA', 'Public', 'DOCU', 'E-signature market leadership, network effects, brand recognition', 'Competition, post-pandemic normalization, customer expansion challenges', 'Mature', 'High', 'Knowledge Workers', 'Global'),

('HubSpot', 'Technology', 'Cambridge, MA', 'Medium', 7000, 1731000000, 2006, 'Inbound marketing, sales, and service software', 'Customer Platform', 'Small to Medium Businesses, Marketing Teams', 'Marketing Hub, Sales Hub, Service Hub, CMS Hub, Operations Hub', 'HubSpot Platform, JavaScript, Python, APIs, Inbound Marketing', 'Challenger', 'Leading inbound marketing platform expanding to full customer platform', 'https://www.hubspot.com', 'investor.relations@hubspot.com', 'Yamini Rangan', 'Cambridge, MA', 'Public', 'HUBS', 'Inbound marketing leadership, SMB focus, comprehensive platform', 'Salesforce competition, enterprise market penetration, customer acquisition costs', 'Growth', 'Advanced', 'SMB to Mid-market', 'Global'),

('Zscaler', 'Technology', 'San Jose, CA', 'Medium', 5500, 1091000000, 2007, 'Cloud security company', 'Zero Trust Cloud Security', 'Enterprises, Remote Workers, IT Teams', 'Zero Trust Exchange, Cloud Firewall, Data Protection, Browser Isolation', 'Zero Trust Architecture, Cloud-native Security, AI/ML, Global Cloud', 'Leader', 'Leading zero trust network access and cloud security transformation', 'https://www.zscaler.com', 'investor.relations@zscaler.com', 'Jay Chaudhry', 'San Jose, CA', 'Public', 'ZS', 'Zero trust leadership, cloud-native architecture, global presence', 'Security competition, customer expansion, technology execution', 'Growth', 'Advanced', 'Cloud-first Enterprises', 'Global');

-- Create indexes for better query performance
CREATE INDEX IF NOT EXISTS idx_finance_companies_location ON finance_companies(location);
CREATE INDEX IF NOT EXISTS idx_finance_companies_performance ON finance_companies(performance_score);
CREATE INDEX IF NOT EXISTS idx_finance_companies_name ON finance_companies(company_name);

CREATE INDEX IF NOT EXISTS idx_healthcare_companies_location ON healthcare_companies(location);
CREATE INDEX IF NOT EXISTS idx_healthcare_companies_performance ON healthcare_companies(performance_score);
CREATE INDEX IF NOT EXISTS idx_healthcare_companies_name ON healthcare_companies(company_name);

CREATE INDEX IF NOT EXISTS idx_tech_companies_location ON tech_companies(location);
CREATE INDEX IF NOT EXISTS idx_tech_companies_performance ON tech_companies(performance_score);
CREATE INDEX IF NOT EXISTS idx_tech_companies_name ON tech_companies(company_name);

-- Enable Row Level Security (RLS) for better security
ALTER TABLE finance_companies ENABLE ROW LEVEL SECURITY;
ALTER TABLE healthcare_companies ENABLE ROW LEVEL SECURITY;
ALTER TABLE tech_companies ENABLE ROW LEVEL SECURITY;

-- Create policies to allow read access (adjust based on your needs)
CREATE POLICY "Allow read access for finance_companies" ON finance_companies
    FOR SELECT USING (true);

CREATE POLICY "Allow read access for healthcare_companies" ON healthcare_companies
    FOR SELECT USING (true);

CREATE POLICY "Allow read access for tech_companies" ON tech_companies
    FOR SELECT USING (true);

-- Function to update the updated_at timestamp
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ language 'plpgsql';

-- Create triggers to automatically update updated_at
CREATE TRIGGER update_finance_companies_updated_at BEFORE UPDATE
    ON finance_companies FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_healthcare_companies_updated_at BEFORE UPDATE
    ON healthcare_companies FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_tech_companies_updated_at BEFORE UPDATE
    ON tech_companies FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();