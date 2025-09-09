-- ========================================
-- SUPABASE DATABASE SETUP FOR INDUSTRYROUTER  
-- Copy this entire script and run it in Supabase SQL Editor
-- ========================================

-- Create finance_companies table
CREATE TABLE IF NOT EXISTS finance_companies (
    id SERIAL PRIMARY KEY,
    company_name TEXT NOT NULL,
    industry TEXT NOT NULL DEFAULT 'Finance',
    location TEXT,
    performance_score INTEGER CHECK (performance_score >= 0 AND performance_score <= 100),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Create healthcare_companies table
CREATE TABLE IF NOT EXISTS healthcare_companies (
    id SERIAL PRIMARY KEY,
    company_name TEXT NOT NULL,
    industry TEXT NOT NULL DEFAULT 'Healthcare',
    location TEXT,
    performance_score INTEGER CHECK (performance_score >= 0 AND performance_score <= 100),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Create tech_companies table
CREATE TABLE IF NOT EXISTS tech_companies (
    id SERIAL PRIMARY KEY,
    company_name TEXT NOT NULL,
    industry TEXT NOT NULL DEFAULT 'Technology',
    location TEXT,
    performance_score INTEGER CHECK (performance_score >= 0 AND performance_score <= 100),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Insert sample finance companies
INSERT INTO finance_companies (company_name, industry, location, performance_score) VALUES
('Goldman Sachs', 'Finance', 'New York, NY', 95),
('JPMorgan Chase', 'Finance', 'New York, NY', 92),
('Bank of America', 'Finance', 'Charlotte, NC', 88),
('Wells Fargo', 'Finance', 'San Francisco, CA', 85),
('Morgan Stanley', 'Finance', 'New York, NY', 90),
('Citigroup', 'Finance', 'New York, NY', 87),
('American Express', 'Finance', 'New York, NY', 89),
('Charles Schwab', 'Finance', 'San Francisco, CA', 86),
('Capital One', 'Finance', 'McLean, VA', 84),
('TD Bank', 'Finance', 'Toronto, ON', 83);

-- Insert sample healthcare companies
INSERT INTO healthcare_companies (company_name, industry, location, performance_score) VALUES
('Johnson & Johnson', 'Healthcare', 'New Brunswick, NJ', 94),
('Pfizer', 'Healthcare', 'New York, NY', 91),
('UnitedHealth Group', 'Healthcare', 'Minnetonka, MN', 93),
('Abbott Laboratories', 'Healthcare', 'Abbott Park, IL', 89),
('Merck & Co.', 'Healthcare', 'Kenilworth, NJ', 90),
('Bristol Myers Squibb', 'Healthcare', 'New York, NY', 87),
('AstraZeneca', 'Healthcare', 'Cambridge, UK', 88),
('Novartis', 'Healthcare', 'Basel, Switzerland', 92),
('Roche', 'Healthcare', 'Basel, Switzerland', 91),
('GlaxoSmithKline', 'Healthcare', 'London, UK', 86);

-- Insert sample technology companies
INSERT INTO tech_companies (company_name, industry, location, performance_score) VALUES
('Apple Inc.', 'Technology', 'Cupertino, CA', 98),
('Microsoft Corporation', 'Technology', 'Redmond, WA', 97),
('Alphabet Inc.', 'Technology', 'Mountain View, CA', 96),
('Amazon.com Inc.', 'Technology', 'Seattle, WA', 95),
('Meta Platforms Inc.', 'Technology', 'Menlo Park, CA', 91),
('Tesla Inc.', 'Technology', 'Austin, TX', 92),
('NVIDIA Corporation', 'Technology', 'Santa Clara, CA', 94),
('Intel Corporation', 'Technology', 'Santa Clara, CA', 88),
('IBM', 'Technology', 'Armonk, NY', 87),
('Oracle Corporation', 'Technology', 'Austin, TX', 89);

-- Create indexes for better performance
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

-- ========================================
-- SETUP COMPLETE!
-- Your IndustryRouter database is ready to use.
-- ========================================