const {onRequest} = require('firebase-functions/v2/https');
const {defineSecret} = require('firebase-functions/params');
const fetch = require('node-fetch');

// Define GitHub token as a secret (modern approach)
const githubToken = defineSecret('GITHUB_TOKEN');

/**
 * Firebase Cloud Function to trigger GitHub Actions workflow
 * 
 * This function acts as a secure proxy between the client-side button
 * and GitHub's API. The GitHub token is stored securely in Firebase
 * secrets and never exposed to the browser.
 * 
 * URL: https://us-central1-myisptools.cloudfunctions.net/triggerAdoRefresh
 */
exports.triggerAdoRefresh = onRequest(
    {secrets: [githubToken], cors: true},
    async (req, res) => {
        // Only allow POST requests
        if (req.method !== 'POST') {
            res.status(405).json({error: 'Method not allowed. Use POST.'});
            return;
        }

        try {
            // Get GitHub token from secret
            const token = githubToken.value();
        
        // GitHub API endpoint to trigger workflow
        const owner = 'Vishnuramalingam07';
        const repo = 'Myisp_Tools';
        const workflowId = 'fetch-ado-data.yml';
        const ref = 'main';
        
        const url = `https://api.github.com/repos/${owner}/${repo}/actions/workflows/${workflowId}/dispatches`;
        
        console.log(`Triggering workflow: ${url}`);
        
        // Trigger the GitHub Actions workflow
        const response = await fetch(url, {
            method: 'POST',
            headers: {
                'Accept': 'application/vnd.github.v3+json',
                'Authorization': `token ${token}`,
                'Content-Type': 'application/json',
                'User-Agent': 'MyISP-Tools-Firebase-Function',
            },
            body: JSON.stringify({ref}),
        });
        
        // GitHub API returns 204 No Content on success
        if (response.status === 204) {
            console.log('✓ Workflow triggered successfully');
            res.status(200).json({ 
                success: true,
                message: 'GitHub Actions workflow triggered successfully',
                workflow: workflowId,
                timestamp: new Date().toISOString()
            });
        } else {
            const errorText = await response.text();
            console.error(`GitHub API error (${response.status}):`, errorText);
            res.status(response.status).json({ 
                error: 'GitHub API error',
                status: response.status,
                message: errorText
            });
        }
        
        } catch (error) {
            console.error('Function error:', error);
            res.status(500).json({
                error: 'Internal server error',
                message: error.message,
            });
        }
    },
);

/**
 * Optional: Get workflow status
 * URL: https://us-central1-myisptools.cloudfunctions.net/getWorkflowStatus
 */
exports.getWorkflowStatus = onRequest(
    {secrets: [githubToken], cors: true},
    async (req, res) => {
        try {
            const token = githubToken.value();

            const owner = 'Vishnuramalingam07';
            const repo = 'Myisp_Tools';
            const workflowId = 'fetch-ado-data.yml';

            const url = `https://api.github.com/repos/${owner}/${repo}/actions/workflows/${workflowId}/runs?per_page=5`;

            const response = await fetch(url, {
                headers: {
                    'Accept': 'application/vnd.github.v3+json',
                    'Authorization': `token ${token}`,
                    'User-Agent': 'MyISP-Tools-Firebase-Function',
                },
            });

            if (response.ok) {
                const data = await response.json();
                res.status(200).json({
                    success: true,
                    runs: data.workflow_runs,
                });
            } else {
                res.status(response.status).json({error: 'Failed to fetch workflow status'});
            }
        } catch (error) {
            console.error('Function error:', error);
            res.status(500).json({error: error.message});
        }
    },
);
