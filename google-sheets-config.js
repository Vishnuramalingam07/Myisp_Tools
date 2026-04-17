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
    API_KEY: 'AIzaSyCqVIcsGui9z0X2BUa3UJmRSnfpHII3YfA',
    
    // STEP 2: Replace with your Spreadsheet ID
    // (from URL: https://docs.google.com/spreadsheets/d/SPREADSHEET_ID/edit)
    SPREADSHEET_ID: '1hKJxhyYu7XiA0rG21zW_DTv_7IX9Cot3GXLnEHVrNTs',
    
    // Sheet names for different tabs
    SHEET_NAMES: {
        prodSanityTab: 'Prod Sanity Scenarios',
        prodUSSanityTab: 'Prod US Sanity',
        insprintStatusTab: 'Insprint US Prod Status',
        readyForProdBugTab: 'Ready for Prod Bug',
        prodSanityDefectsTab: 'Leadwise Prod Sanity Status'
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
        // Simple approach: store entire data as JSON with timestamp
        return [
            ['Tab ID', 'Data JSON', 'Last Updated'],
            [tabId, JSON.stringify(data), timestamp]
        ];
    }

    /**
     * Convert 2D array from Sheets back to object
     */
    sheetDataToObject(tabId, values) {
        if (!values || values.length < 2) return {};
        try {
            // Extract JSON from second row
            const dataJson = values[1][1];
            return JSON.parse(dataJson || '{}');
        } catch (error) {
            console.error('Error parsing sheet data:', error);
            return {};
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
