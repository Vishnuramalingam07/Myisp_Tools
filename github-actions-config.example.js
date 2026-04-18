// ============================================
// GITHUB ACTIONS CONFIGURATION
// ============================================
// This configuration enables the "Refresh from Azure DevOps" button
// to trigger GitHub Actions workflow automatically.
//
// Setup Instructions:
// 1. Create GitHub Personal Access Token:
//    - Go to: https://github.com/settings/tokens
//    - Click "Generate new token (classic)"
//    - Select scopes: ✅ workflow
//    - Generate and COPY the token
//
// 2. Add the token below (replace YOUR_GITHUB_TOKEN_HERE)
//
// 3. Security Warning:
//    ⚠️  This token allows triggering workflows in your repo
//    ⚠️  Only share this page with trusted team members
//    ⚠️  Consider using Firebase to store the token server-side for better security
//
// ============================================

const GITHUB_CONFIG = {
    owner: 'Vishnuramalingam07',           // Your GitHub username
    repo: 'Myisp_Tools',                    // Your repository name
    workflow_id: 'fetch-ado-data.yml',      // Workflow filename
    ref: 'main',                             // Branch name
    token: 'YOUR_GITHUB_TOKEN_HERE',        // ⚠️ REPLACE with your GitHub PAT
};

// ============================================
// GITHUB ACTIONS API CLIENT
// ============================================

class GitHubActionsClient {
    constructor(config) {
        this.config = config;
        this.apiBase = 'https://api.github.com';
    }

    /**
     * Check if GitHub token is configured
     */
    isConfigured() {
        return this.config.token && 
               this.config.token !== 'YOUR_GITHUB_TOKEN_HERE' &&
               this.config.token.length > 20;
    }

    /**
     * Trigger the GitHub Actions workflow
     */
    async triggerWorkflow() {
        if (!this.isConfigured()) {
            throw new Error('GitHub token not configured. Please update github-actions-config.js');
        }

        const url = `${this.apiBase}/repos/${this.config.owner}/${this.config.repo}/actions/workflows/${this.config.workflow_id}/dispatches`;
        
        const response = await fetch(url, {
            method: 'POST',
            headers: {
                'Accept': 'application/vnd.github.v3+json',
                'Authorization': `token ${this.config.token}`,
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                ref: this.config.ref
            })
        });

        if (!response.ok) {
            const errorText = await response.text();
            throw new Error(`GitHub API error (${response.status}): ${errorText}`);
        }

        return true;
    }

    /**
     * Get recent workflow runs
     */
    async getWorkflowRuns() {
        if (!this.isConfigured()) {
            return [];
        }

        const url = `${this.apiBase}/repos/${this.config.owner}/${this.config.repo}/actions/workflows/${this.config.workflow_id}/runs?per_page=5`;
        
        const response = await fetch(url, {
            method: 'GET',
            headers: {
                'Accept': 'application/vnd.github.v3+json',
                'Authorization': `token ${this.config.token}`
            }
        });

        if (!response.ok) {
            return [];
        }

        const data = await response.json();
        return data.workflow_runs || [];
    }

    /**
     * Get status of a specific workflow run
     */
    async getRunStatus(run_id) {
        if (!this.isConfigured()) {
            return null;
        }

        const url = `${this.apiBase}/repos/${this.config.owner}/${this.config.repo}/actions/runs/${run_id}`;
        
        const response = await fetch(url, {
            method: 'GET',
            headers: {
                'Accept': 'application/vnd.github.v3+json',
                'Authorization': `token ${this.config.token}`
            }
        });

        if (!response.ok) {
            return null;
        }

        return await response.json();
    }
}

// Create global instance
const githubActions = new GitHubActionsClient(GITHUB_CONFIG);

// ============================================
// HELPER FUNCTIONS
// ============================================

/**
 * Show GitHub setup instructions
 */
function showGitHubSetupInstructions() {
    const message = `
📋 GitHub Token Setup Required

To enable the "Refresh from Azure DevOps" button, you need to:

1. Create a GitHub Personal Access Token:
   • Go to: https://github.com/settings/tokens
   • Click "Generate new token (classic)"
   • Name: "MyISP Tools - Workflow Trigger"
   • Select scope: ✅ workflow
   • Click "Generate token"
   • COPY the token (you won't see it again!)

2. Update the configuration:
   • Open: github-actions-config.js
   • Find: token: 'YOUR_GITHUB_TOKEN_HERE'
   • Replace with your actual token
   • Save the file

3. Commit and push to GitHub:
   • git add github-actions-config.js
   • git commit -m "Add GitHub token"
   • git push origin main

⚠️  Security Note:
The token allows triggering workflows in your repo.
Only share this page with trusted team members.

Alternative: Use the GitHub Actions UI
• Go to: https://github.com/${GITHUB_CONFIG.owner}/${GITHUB_CONFIG.repo}/actions
• Click "Fetch ADO Test Results and Update Firebase"
• Click "Run workflow" button
    `.trim();

    alert(message);
}

console.log('✓ GitHub Actions client loaded');
console.log(`  Configured: ${githubActions.isConfigured() ? 'Yes ✓' : 'No - token needed'}`);
