-- PostgreSQL Database Schema for MyISP Tools - Test Execution Reports
-- Database: myisp_tools

-- Create test_executions table
CREATE TABLE IF NOT EXISTS test_executions (
    id SERIAL PRIMARY KEY,
    test_case_id INTEGER,
    test_case_title TEXT,
    priority VARCHAR(10),
    test_type VARCHAR(20),
    outcome VARCHAR(20),
    assigned_to VARCHAR(200),
    lead VARCHAR(200),
    module VARCHAR(200),
    requirement_id VARCHAR(50),
    requirement_title TEXT,
    bug_count INTEGER DEFAULT 0,
    bug_details TEXT,
    suite_name VARCHAR(200),
    report_type VARCHAR(50),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create index for faster queries
CREATE INDEX IF NOT EXISTS idx_test_case_id ON test_executions(test_case_id);
CREATE INDEX IF NOT EXISTS idx_outcome ON test_executions(outcome);
CREATE INDEX IF NOT EXISTS idx_test_type ON test_executions(test_type);
CREATE INDEX IF NOT EXISTS idx_lead ON test_executions(lead);
CREATE INDEX IF NOT EXISTS idx_created_at ON test_executions(created_at);
CREATE INDEX IF NOT EXISTS idx_report_type ON test_executions(report_type);

-- Create report_metadata table
CREATE TABLE IF NOT EXISTS report_metadata (
    id SERIAL PRIMARY KEY,
    report_name VARCHAR(200),
    report_type VARCHAR(50),
    total_tests INTEGER,
    passed INTEGER,
    failed INTEGER,
    blocked INTEGER,
    not_run INTEGER,
    automation_count INTEGER,
    manual_count INTEGER,
    total_bugs INTEGER,
    generated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

COMMENT ON TABLE test_executions IS 'Stores individual test execution records from Azure DevOps';
COMMENT ON TABLE report_metadata IS 'Stores summary metadata for each generated report';
