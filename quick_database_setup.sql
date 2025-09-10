-- Quick Database Setup for Supabase
-- Copy this entire content and paste into Supabase SQL Editor

-- Create finance_companies table
CREATE TABLE IF NOT EXISTS finance_companies (
    id SERIAL PRIMARY KEY,
    company_name TEXT NOT NULL,
    industry TEXT NOT NULL DEFAULT 'Finance',
    location TEXT,
    company_size TEXT,
    employee_count INTEGER,
    revenue BIGINT DEFAULT 0,
    founding_year INTEGER,
    description TEXT,
    business_model TEXT,
    target_market TEXT,
    key_services TEXT,
    technology_stack TEXT,
    market_position TEXT,
    recent_news TEXT,
    website_url TEXT,
    contact_email TEXT,
    phone_number TEXT,
    ceo_name TEXT,
    headquarters TEXT,
    subsidiaries TEXT,
    partnerships TEXT,
    awards TEXT,
    financial_status TEXT,
    stock_symbol TEXT,
    last_funding_round TEXT,
    investors TEXT,
    competitive_advantages TEXT,
    challenges TEXT,
    growth_stage TEXT,
    sustainability_initiatives TEXT,
    digital_transformation_level TEXT,
    innovation_focus TEXT,
    customer_base_size TEXT,
    geographic_presence TEXT,
    regulatory_compliance TEXT,
    risk_factors TEXT,
    performance_score INTEGER DEFAULT NULL,
    evaluation_notes TEXT,
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
    company_size TEXT,
    employee_count INTEGER,
    revenue BIGINT DEFAULT 0,
    founding_year INTEGER,
    description TEXT,
    business_model TEXT,
    target_market TEXT,
    key_services TEXT,
    technology_stack TEXT,
    market_position TEXT,
    recent_news TEXT,
    website_url TEXT,
    contact_email TEXT,
    phone_number TEXT,
    ceo_name TEXT,
    headquarters TEXT,
    subsidiaries TEXT,
    partnerships TEXT,
    awards TEXT,
    financial_status TEXT,
    stock_symbol TEXT,
    last_funding_round TEXT,
    investors TEXT,
    competitive_advantages TEXT,
    challenges TEXT,
    growth_stage TEXT,
    sustainability_initiatives TEXT,
    digital_transformation_level TEXT,
    innovation_focus TEXT,
    customer_base_size TEXT,
    geographic_presence TEXT,
    regulatory_compliance TEXT,
    risk_factors TEXT,
    performance_score INTEGER DEFAULT NULL,
    evaluation_notes TEXT,
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
    company_size TEXT,
    employee_count INTEGER,
    revenue BIGINT DEFAULT 0,
    founding_year INTEGER,
    description TEXT,
    business_model TEXT,
    target_market TEXT,
    key_services TEXT,
    technology_stack TEXT,
    market_position TEXT,
    recent_news TEXT,
    website_url TEXT,
    contact_email TEXT,
    phone_number TEXT,
    ceo_name TEXT,
    headquarters TEXT,
    subsidiaries TEXT,
    partnerships TEXT,
    awards TEXT,
    financial_status TEXT,
    stock_symbol TEXT,
    last_funding_round TEXT,
    investors TEXT,
    competitive_advantages TEXT,
    challenges TEXT,
    growth_stage TEXT,
    sustainability_initiatives TEXT,
    digital_transformation_level TEXT,
    innovation_focus TEXT,
    customer_base_size TEXT,
    geographic_presence TEXT,
    regulatory_compliance TEXT,
    risk_factors TEXT,
    performance_score INTEGER DEFAULT NULL,
    evaluation_notes TEXT,
    last_evaluated_at TIMESTAMP WITH TIME ZONE DEFAULT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Insert sample data (just a few key companies for immediate testing)
-- Finance Companies
INSERT INTO finance_companies (company_name, industry, location, company_size, employee_count, revenue, founding_year, description, business_model, target_market, key_services, technology_stack, market_position, recent_news, website_url, contact_email, ceo_name, headquarters, financial_status, stock_symbol, competitive_advantages, challenges, growth_stage, digital_transformation_level, customer_base_size, geographic_presence) VALUES
('Goldman Sachs', 'Finance', 'New York, NY', 'Large', 49100, 59336000000, 1869, 'Leading global investment bank', 'Investment Banking', 'Corporations, Governments, Institutions', 'Investment Banking, Trading, Asset Management', 'Cloud Computing, AI/ML, Python, Java, React', 'Leader', 'Leading digital transformation in investment banking', 'https://www.goldmansachs.com', 'info@goldmansachs.com', 'David Solomon', 'New York, NY', 'Public', 'GS', 'Global reach, technology innovation, diverse revenue streams', 'Regulatory pressure, market volatility, competition from fintech', 'Mature', 'Advanced', 'Global Enterprise', 'Global'),

('BlackRock', 'Finance', 'New York, NY', 'Large', 19800, 19374000000, 1988, 'World''s largest asset manager', 'Asset Management', 'Institutional Investors, Retail Investors, Governments', 'Investment Management, Risk Management, Advisory Services', 'Cloud Computing, AI/ML, Aladdin Platform, Python, Java', 'Leader', 'Leading ESG investing and AI-driven portfolio management', 'https://www.blackrock.com', 'info@blackrock.com', 'Larry Fink', 'New York, NY', 'Public', 'BLK', 'Largest AUM globally, Aladdin technology platform, ESG leadership', 'Fee compression, regulatory changes, market volatility', 'Mature', 'Advanced', 'Institutional', 'Global');

-- Healthcare Companies  
INSERT INTO healthcare_companies (company_name, industry, location, company_size, employee_count, revenue, founding_year, description, business_model, target_market, key_services, technology_stack, market_position, recent_news, website_url, contact_email, ceo_name, headquarters, financial_status, stock_symbol, competitive_advantages, challenges, growth_stage, digital_transformation_level, customer_base_size, geographic_presence) VALUES
('Johnson & Johnson', 'Healthcare', 'New Brunswick, NJ', 'Large', 152700, 94943000000, 1886, 'Multinational healthcare conglomerate', 'Diversified Healthcare', 'Consumers, Healthcare Providers, Patients', 'Pharmaceuticals, Medical Devices, Consumer Products', 'Cloud Computing, AI/ML, IoT, Data Analytics, Java, Python', 'Leader', 'Leading innovation in pharmaceuticals and medical devices', 'https://www.jnj.com', 'info@jnj.com', 'Joaquin Duato', 'New Brunswick, NJ', 'Public', 'JNJ', 'Diversified portfolio, global reach, strong R&D pipeline', 'Regulatory challenges, patent cliffs, healthcare cost pressures', 'Mature', 'Advanced', 'Global Consumer', 'Global'),

('Pfizer', 'Healthcare', 'New York, NY', 'Large', 83000, 100330000000, 1849, 'Global pharmaceutical giant', 'Pharmaceutical R&D', 'Healthcare Providers, Patients, Governments', 'Vaccines, Oncology, Primary Care, Specialty Care', 'Cloud Computing, AI/ML, Bioinformatics, Python, R', 'Leader', 'Leading COVID-19 vaccine development and distribution', 'https://www.pfizer.com', 'info@pfizer.com', 'Albert Bourla', 'New York, NY', 'Public', 'PFE', 'Strong vaccine portfolio, robust R&D, global distribution', 'Patent expirations, regulatory scrutiny, pricing pressure', 'Mature', 'Advanced', 'Global Healthcare', 'Global');

-- Technology Companies
INSERT INTO tech_companies (company_name, industry, location, company_size, employee_count, revenue, founding_year, description, business_model, target_market, key_services, technology_stack, market_position, recent_news, website_url, contact_email, ceo_name, headquarters, financial_status, stock_symbol, competitive_advantages, challenges, growth_stage, digital_transformation_level, customer_base_size, geographic_presence) VALUES
('Apple Inc.', 'Technology', 'Cupertino, CA', 'Large', 164000, 394328000000, 1976, 'Multinational technology company', 'Consumer Electronics & Services', 'Consumers, Businesses, Developers', 'iPhone, Mac, iPad, Apple Watch, Services, App Store', 'iOS, macOS, Swift, Objective-C, Cloud Services, AI/ML', 'Leader', 'Leading smartphone innovation and expanding services revenue', 'https://www.apple.com', 'info@apple.com', 'Tim Cook', 'Cupertino, CA', 'Public', 'AAPL', 'Brand loyalty, ecosystem integration, premium pricing power', 'Supply chain dependency, regulatory scrutiny, market saturation', 'Mature', 'Advanced', 'Global Consumer', 'Global'),

('Microsoft Corporation', 'Technology', 'Redmond, WA', 'Large', 238000, 198270000000, 1975, 'Multinational technology corporation', 'Software & Cloud Services', 'Businesses, Consumers, Developers', 'Azure, Office 365, Windows, LinkedIn, Gaming', 'Cloud Computing, AI/ML, .NET, TypeScript, Python, Azure', 'Leader', 'Leading cloud transformation and AI integration', 'https://www.microsoft.com', 'info@microsoft.com', 'Satya Nadella', 'Redmond, WA', 'Public', 'MSFT', 'Dominant productivity suite, strong cloud growth, AI leadership', 'Intense cloud competition, regulatory scrutiny, legacy system transitions', 'Mature', 'Advanced', 'Global Enterprise', 'Global');

-- Success message
SELECT 'Database setup complete! Tables created and sample data inserted.' AS status;