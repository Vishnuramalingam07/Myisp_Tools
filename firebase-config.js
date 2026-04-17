// ============================================
// FIREBASE REALTIME DATABASE CONFIGURATION
// ============================================
// Setup Instructions:
// 1. Go to https://console.firebase.google.com/
// 2. Create a new project (or select existing)
// 3. Click "Realtime Database" in left menu
// 4. Click "Create Database" → Start in TEST MODE (for now)
// 5. Go to Project Settings (gear icon) → General tab
// 6. Scroll to "Your apps" → Click Web icon (</>)
// 7. Copy the firebaseConfig object and paste below

const FIREBASE_CONFIG = {
    apiKey: "AIzaSyB_9XEWyPOsM4p8aCdgHo4zOljH-eGPLdM",
    authDomain: "myisptools.firebaseapp.com",
    databaseURL: "https://myisptools-default-rtdb.firebaseio.com",
    projectId: "myisptools",
    storageBucket: "myisptools.firebasestorage.app",
    messagingSenderId: "231946416648",
    appId: "1:231946416648:web:8123b8e35ab43c0b2997bd",
    measurementId: "G-8166Z09Z8B"
};

// ============================================
// FIREBASE HELPER CLASS
// ============================================

class FirebaseAPI {
    constructor(config) {
        this.config = config;
        this.databaseURL = config.databaseURL;
        this.initialized = false;
    }

    /**
     * Initialize Firebase (called automatically on first use)
     */
    async initialize() {
        if (this.initialized) return;
        
        // Firebase REST API doesn't need initialization
        // Just verify the database URL is accessible
        this.initialized = true;
        console.log('✓ Firebase REST API ready');
    }

    /**
     * Save tab data to Firebase
     * @param {string} tabId - Tab identifier
     * @param {Object} data - Data to save
     */
    async saveTabData(tabId, data) {
        await this.initialize();
        
        try {
            const timestamp = new Date().toISOString();
            const dataToSave = {
                ...data,
                _lastUpdated: timestamp,
                _tabId: tabId
            };
            
            // Firebase REST API PUT request
            const url = `${this.databaseURL}/prodSanityReport/${tabId}.json`;
            
            const response = await fetch(url, {
                method: 'PUT',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(dataToSave)
            });

            if (!response.ok) {
                const error = await response.json();
                throw new Error(`Firebase Error: ${error.error || 'Unknown error'}`);
            }

            const result = await response.json();
            console.log(`✓ Saved ${tabId} to Firebase`);
            return result;
        } catch (error) {
            console.error('Error saving to Firebase:', error);
            throw error;
        }
    }

    /**
     * Load tab data from Firebase
     * @param {string} tabId - Tab identifier
     */
    async loadTabData(tabId) {
        await this.initialize();
        
        try {
            const url = `${this.databaseURL}/prodSanityReport/${tabId}.json`;
            
            const response = await fetch(url);
            
            if (!response.ok) {
                const error = await response.json();
                throw new Error(`Firebase Error: ${error.error || 'Unknown error'}`);
            }

            const data = await response.json();
            
            // Remove Firebase metadata before returning
            if (data && typeof data === 'object') {
                delete data._lastUpdated;
                delete data._tabId;
            }
            
            return data;
        } catch (error) {
            console.error('Error loading from Firebase:', error);
            return null;
        }
    }

    /**
     * Get all data from all tabs
     */
    async getAllData() {
        await this.initialize();
        
        try {
            const url = `${this.databaseURL}/prodSanityReport.json`;
            
            const response = await fetch(url);
            
            if (!response.ok) {
                return {};
            }

            const allData = await response.json();
            return allData || {};
        } catch (error) {
            console.error('Error loading all data from Firebase:', error);
            return {};
        }
    }

    /**
     * Listen for real-time updates on a specific tab
     * @param {string} tabId - Tab identifier
     * @param {Function} callback - Called when data changes
     */
    watchTabData(tabId, callback) {
        // For REST API, we'll use polling
        // Note: For true real-time, would need Firebase SDK
        const pollInterval = 3000; // 3 seconds
        
        let lastData = null;
        
        const poll = async () => {
            try {
                const data = await this.loadTabData(tabId);
                const dataStr = JSON.stringify(data);
                
                if (dataStr !== lastData) {
                    lastData = dataStr;
                    callback(data);
                }
            } catch (error) {
                console.error('Error polling Firebase:', error);
            }
        };
        
        // Initial load
        poll();
        
        // Start polling
        const intervalId = setInterval(poll, pollInterval);
        
        // Return cleanup function
        return () => clearInterval(intervalId);
    }

    /**
     * Delete tab data
     * @param {string} tabId - Tab identifier
     */
    async deleteTabData(tabId) {
        await this.initialize();
        
        try {
            const url = `${this.databaseURL}/prodSanityReport/${tabId}.json`;
            
            const response = await fetch(url, {
                method: 'DELETE'
            });

            if (!response.ok) {
                const error = await response.json();
                throw new Error(`Firebase Error: ${error.error || 'Unknown error'}`);
            }

            return await response.json();
        } catch (error) {
            console.error('Error deleting from Firebase:', error);
            throw error;
        }
    }

    /**
     * Check if Firebase is configured
     */
    isConfigured() {
        return this.config.apiKey !== 'YOUR_FIREBASE_API_KEY' && 
               this.config.databaseURL !== 'https://YOUR_PROJECT-default-rtdb.firebaseio.com';
    }

    /**
     * Test connection to Firebase
     */
    async testConnection() {
        try {
            const url = `${this.databaseURL}/.json`;
            const response = await fetch(url);
            return response.ok;
        } catch (error) {
            console.error('Firebase connection test failed:', error);
            return false;
        }
    }
}

// Create global instance
const firebaseAPI = new FirebaseAPI(FIREBASE_CONFIG);
