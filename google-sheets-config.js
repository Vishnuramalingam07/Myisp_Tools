// ============================================
// GOOGLE SHEETS API CONFIGURATION
// ============================================
// Setup Instructions:
// 1. Go to https://console.cloud.google.com/
// 2. Create a new project (or select existing)
// 3. Enable Google Sheets API
// 4. Create credentials (API Key)
// 5. Replace YOUR_API_KEY below
// 6. Create a Google Sheet and make it publicly editable
// 7. Replace YOUR_SPREADSHEET_ID below

const GOOGLE_SHEETS_CONFIG = {
    // STEP 1: Replace with your Google Sheets API Key
    API_KEY: 'YOUR_API_KEY_HERE',
    
    // STEP 2: Replace with your Spreadsheet ID
    // (from URL: https://docs.google.com/spreadsheets/d/SPREADSHEET_ID/edit)
    SPREADSHEET_ID: 'YOUR_SPREADSHEET_ID_HERE',
    
    // Sheet names for different tabs
    SHEET_NAMES: {
        summary: 'Summary',
        execution: 'Execution',
        bugAnalysis: 'BugAnalysis',
        coverage: 'Coverage',
        regressions: 'Regressions',
        testCases: 'TestCases'
    }
};

// ============================================
// GOOGLE SHEETS API HELPER FUNCTIONS
// ============================================

class GoogleSheetsAPI {
    constructor(config) {
        this.apiKey = config.API_KEY;
        this.spreadsheetId = config.SPREADSHEET_ID;
        this.baseUrl = 'https://sheets.googleapis.com/v4/spreadsheets';
    }

    /**
     * Save tab data to Google Sheets
     * @param {string} tabId - Tab identifier
     * @param {Object} data - Data to save
     */
    async saveTabData(tabId, data) {
        try {
            const sheetName = this.getSheetName(tabId);
            const range = `${sheetName}!A1`;
            
            // Convert data object to 2D array for Sheets
            const values = this.objectToSheetData(tabId, data);
            
            const url = `${this.baseUrl}/${this.spreadsheetId}/values/${range}?valueInputOption=RAW&key=${this.apiKey}`;
            
            const response = await fetch(url, {
                method: 'PUT',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    range: range,
                    values: values
                })
            });

            if (!response.ok) {
                const error = await response.json();
                throw new Error(`Sheets API Error: ${error.error.message}`);
            }

            return await response.json();
        } catch (error) {
            console.error('Error saving to Google Sheets:', error);
            throw error;
        }
    }

    /**
     * Load tab data from Google Sheets
     * @param {string} tabId - Tab identifier
     */
    async loadTabData(tabId) {
        try {
            const sheetName = this.getSheetName(tabId);
            const range = `${sheetName}!A1:Z1000`; // Adjust range as needed
            
            const url = `${this.baseUrl}/${this.spreadsheetId}/values/${range}?key=${this.apiKey}`;
            
            const response = await fetch(url);
            
            if (!response.ok) {
                const error = await response.json();
                throw new Error(`Sheets API Error: ${error.error.message}`);
            }

            const result = await response.json();
            
            // Convert 2D array back to object
            return this.sheetDataToObject(tabId, result.values || []);
        } catch (error) {
            console.error('Error loading from Google Sheets:', error);
            return null;
        }
    }

    /**
     * Get all data from all sheets
     */
    async getAllData() {
        const allData = {};
        
        for (const [tabId, sheetName] of Object.entries(GOOGLE_SHEETS_CONFIG.SHEET_NAMES)) {
            try {
                allData[tabId] = await this.loadTabData(tabId);
            } catch (error) {
                console.error(`Error loading ${tabId}:`, error);
                allData[tabId] = null;
            }
        }
        
        return allData;
    }

    /**
     * Convert tab data object to 2D array for Sheets
     */
    objectToSheetData(tabId, data) {
        const timestamp = new Date().toISOString();
        
        switch (tabId) {
            case 'summary':
                return [
                    ['Field', 'Value', 'Last Updated'],
                    ['Total Test Cases', data.totalTestCases || '', timestamp],
                    ['Pass', data.pass || '', timestamp],
                    ['Fail', data.fail || '', timestamp],
                    ['Not Run', data.notRun || '', timestamp],
                    ['Pass Rate', data.passRate || '', timestamp],
                    ['Execution Time', data.executionTime || '', timestamp],
                    ['Environment', data.environment || '', timestamp],
                    ['Build Version', data.buildVersion || '', timestamp],
                    ['Comments', data.comments || '', timestamp]
                ];
            
            case 'execution':
                return [
                    ['Field', 'Value', 'Last Updated'],
                    ['Start Time', data.startTime || '', timestamp],
                    ['End Time', data.endTime || '', timestamp],
                    ['Duration', data.duration || '', timestamp],
                    ['Executed By', data.executedBy || '', timestamp],
                    ['Test Suite', data.testSuite || '', timestamp],
                    ['Platform', data.platform || '', timestamp],
                    ['Browser', data.browser || '', timestamp]
                ];
            
            case 'bugAnalysis':
                return [
                    ['Field', 'Value', 'Last Updated'],
                    ['Total Bugs', data.totalBugs || '', timestamp],
                    ['Critical', data.critical || '', timestamp],
                    ['High', data.high || '', timestamp],
                    ['Medium', data.medium || '', timestamp],
                    ['Low', data.low || '', timestamp],
                    ['Fixed', data.fixed || '', timestamp],
                    ['Open', data.open || '', timestamp]
                ];
            
            case 'coverage':
                return [
                    ['Field', 'Value', 'Last Updated'],
                    ['Code Coverage %', data.codeCoverage || '', timestamp],
                    ['Feature Coverage %', data.featureCoverage || '', timestamp],
                    ['Automation Coverage %', data.automationCoverage || '', timestamp],
                    ['Modules Tested', data.modulesTested || '', timestamp],
                    ['Total Modules', data.totalModules || '', timestamp]
                ];
            
            case 'regressions':
                return [
                    ['Field', 'Value', 'Last Updated'],
                    ['New Regressions', data.newRegressions || '', timestamp],
                    ['Fixed Regressions', data.fixedRegressions || '', timestamp],
                    ['Open Regressions', data.openRegressions || '', timestamp],
                    ['Regression Details', data.regressionDetails || '', timestamp]
                ];
            
            case 'testCases':
                // For test cases, convert array to rows
                const headers = ['Test ID', 'Test Name', 'Status', 'Priority', 'Duration', 'Last Updated'];
                const rows = (data.testCases || []).map(tc => [
                    tc.id || '',
                    tc.name || '',
                    tc.status || '',
                    tc.priority || '',
                    tc.duration || '',
                    timestamp
                ]);
                return [headers, ...rows];
            
            default:
                return [['Data', 'Last Updated'], [JSON.stringify(data), timestamp]];
        }
    }

    /**
     * Convert 2D array from Sheets back to object
     */
    sheetDataToObject(tabId, values) {
        if (!values || values.length === 0) {
            return {};
        }
        
        switch (tabId) {
            case 'summary':
            case 'execution':
            case 'bugAnalysis':
            case 'coverage':
            case 'regressions':
                // Key-value format: [Field, Value, Timestamp]
                const data = {};
                for (let i = 1; i < values.length; i++) {
                    const [field, value] = values[i];
                    // Convert field name to camelCase key
                    const key = field.replace(/\s+/g, '').replace(/^./, str => str.toLowerCase());
                    data[key] = value;
                }
                return data;
            
            case 'testCases':
                // Array format: [Test ID, Test Name, Status, Priority, Duration]
                const testCases = [];
                for (let i = 1; i < values.length; i++) {
                    const [id, name, status, priority, duration] = values[i];
                    testCases.push({ id, name, status, priority, duration });
                }
                return { testCases };
            
            default:
                try {
                    return JSON.parse(values[1][0] || '{}');
                } catch {
                    return {};
                }
        }
    }

    /**
     * Get sheet name for tab ID
     */
    getSheetName(tabId) {
        return GOOGLE_SHEETS_CONFIG.SHEET_NAMES[tabId] || tabId;
    }

    /**
     * Check if API is configured
     */
    isConfigured() {
        return this.apiKey !== 'YOUR_API_KEY_HERE' && 
               this.spreadsheetId !== 'YOUR_SPREADSHEET_ID_HERE';
    }
}

// Create global instance
const sheetsAPI = new GoogleSheetsAPI(GOOGLE_SHEETS_CONFIG);
