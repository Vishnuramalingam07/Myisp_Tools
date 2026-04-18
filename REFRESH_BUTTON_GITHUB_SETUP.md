# 🔄 Refresh Button Setup Guide

## ✅ What You Get

The **"Refresh from Azure DevOps"** button now triggers your GitHub Actions workflow automatically!

**Features:**
- ✅ Click button → Triggers workflow → Fresh data in 2-3 minutes
- ✅ Real-time progress modal with status updates  
- ✅ Auto-reloads page when complete
- ✅ Polls GitHub Actions for completion status
- ✅ Error handling with helpful messages

---

## 📋 Setup Steps (10 minutes)

### **Step 1: Create GitHub Personal Access Token**

1. **Go to GitHub Settings:**
   ```
   https://github.com/settings/tokens
   ```

2. **Generate New Token:**
   - Click **"Generate new token (classic)"**
   - Name: `MyISP Tools - Workflow Trigger`
   - Expiration: `90 days` (or your preference)
   - Select scopes:
     - ✅ **workflow** (this is the only scope needed)
   - Click **"Generate token"**

3. **COPY THE TOKEN** 🔑
   - You won't be able to see it again!
   - It looks like: `ghp_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx`

---

### **Step 2: Configure the Token**

1. **Open file:** `github-actions-config.js`

2. **Find this line:**
   ```javascript
   token: 'YOUR_GITHUB_TOKEN_HERE',
   ```

3. **Replace with your token:**
   ```javascript
   token: 'ghp_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx',
   ```

4. **Save the file**

---

### **Step 3: Update .gitignore (Important for Security)**

Add this line to `.gitignore` to prevent committing your token:

```
# GitHub Actions config (contains sensitive token)
github-actions-config.js
```

Then create a template file for others:

```powershell
# Create template without token
Copy-Item github-actions-config.js github-actions-config.example.js

# Edit github-actions-config.example.js and replace your token with:
token: 'YOUR_GITHUB_TOKEN_HERE',

# Commit only the template
git add github-actions-config.example.js
git add .gitignore
git commit -m "Add GitHub Actions refresh button (template)"
git push origin main
```

---

### **Step 4: Push Updated live_report.html**

```powershell
git add live_report.html
git commit -m "Add GitHub Actions trigger to refresh button"
git push origin main
```

---

## 🎯 How to Use

1. **Open your live report:**
   ```
   https://vishnuramalingam07.github.io/Myisp_Tools/live_report.html
   ```

2. **Click the button:**
   ```
   🔄 Refresh from Azure DevOps
   ```

3. **Watch the progress:**
   - Step 1/3: Triggering GitHub Actions workflow...
   - Step 2/3: Workflow running... (polls every 5 seconds)
   - Step 3/3: Workflow completed! Reloading page...

4. **Page auto-reloads** with fresh ADO data! ✅

---

## 🔒 Security Considerations

### **⚠️ Important Security Notes:**

1. **Token has workflow permissions**
   - Can trigger any workflow in your repository
   - Keep it secret like a password!

2. **Current setup is client-side**
   - Token is visible in browser dev tools
   - Only suitable for trusted team members

3. **gitignore the config file**
   - Prevents accidentally committing token to GitHub
   - Each team member needs their own token

### **🔐 More Secure Alternative (Advanced):**

For better security, you could:

1. **Store token in Firebase:**
   ```javascript
   // Instead of github-actions-config.js
   const token = await firebase.database()
     .ref('admin/github_token')
     .once('value');
   ```

2. **Use Firebase Security Rules:**
   ```json
   "admin": {
     ".read": "auth != null && auth.token.admin === true"
   }
   ```

3. **Implement server-side proxy:**
   - Token stays on server
   - Button calls your API
   - API triggers GitHub workflow

---

## 🐛 Troubleshooting

### **Error: "GitHub token not configured"**
- ✅ Check `github-actions-config.js` has your actual token
- ✅ Token should start with `ghp_`
- ✅ File is loaded (check browser console for errors)

### **Error: "GitHub API error (401)"**
- ✅ Token has `workflow` scope enabled
- ✅ Token hasn't expired
- ✅ Token is for the correct GitHub account

### **Error: "GitHub API error (404)"**
- ✅ Check `owner`, `repo`, and `workflow_id` in config
- ✅ Repository name is correct (case-sensitive)
- ✅ Workflow file `fetch-ado-data.yml` exists

### **Button shows "Would you like to see setup instructions?"**
- Token is not configured or invalid
- Check the config file

### **Workflow triggered but times out**
- Workflow may take >3 minutes
- Check manually at: https://github.com/Vishnuramalingam07/Myisp_Tools/actions
- Page will show "Check GitHub Actions for status" link

---

## 📊 What Happens Behind the Scenes

```
User clicks button
    ↓
JavaScript calls GitHub API
    ↓
GitHub Actions workflow starts
    ↓
Workflow fetches ADO data (ProdSanity_Report.py)
    ↓
Workflow uploads to Firebase
    ↓
Page polls GitHub API every 5 seconds
    ↓
When workflow completes → Page reloads
    ↓
Fresh data appears! ✅
```

---

## 🎨 User Experience

**Before (Manual GitHub Actions):**
1. User goes to GitHub.com
2. Navigates to Actions tab
3. Finds workflow
4. Clicks "Run workflow"
5. Waits for completion
6. Goes back to report page
7. Refreshes browser

**After (Button Click):**
1. User clicks "Refresh from Azure DevOps" button
2. Waits 2-3 minutes
3. Page auto-reloads with fresh data ✅

**Much better! 🎉**

---

## 🔄 Alternative: Keep Using Manual Trigger

If you don't want to set up the token, you can still:

1. Go to: https://github.com/Vishnuramalingam07/Myisp_Tools/actions
2. Click "Fetch ADO Test Results and Update Firebase"
3. Click "Run workflow" button
4. Wait ~2-3 minutes
5. Reload your report page

The button is optional - your workflow works great without it!

---

## 📝 Configuration Reference

**File:** `github-actions-config.js`

```javascript
const GITHUB_CONFIG = {
    owner: 'Vishnuramalingam07',      // GitHub username
    repo: 'Myisp_Tools',               // Repository name (case-sensitive)
    workflow_id: 'fetch-ado-data.yml', // Workflow filename
    ref: 'main',                        // Branch to trigger
    token: 'ghp_xxxxx...',             // Your Personal Access Token
};
```

---

## 💡 Pro Tips

1. **Token expiration reminder:** Set a calendar reminder before token expires
2. **Multiple team members:** Each person can use their own token
3. **Test locally first:** Open browser dev tools console to see errors
4. **Monitor quota:** GitHub Actions free tier is generous but has limits
5. **Fallback always available:** Manual trigger still works if button fails

---

**Happy Refreshing! 🚀**
