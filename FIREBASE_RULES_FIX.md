# 🔥 URGENT: Fix Firebase Permission Error

## ❌ Error You're Seeing:
```
Save failed: PERMISSION_DENIED: Permission denied
```

## 🔧 How to Fix (5 minutes):

### Step 1: Go to Firebase Console
1. Open: https://console.firebase.google.com/
2. Select project: **myisptools**

### Step 2: Update Database Rules
1. Click **"Realtime Database"** in left menu
2. Click **"Rules"** tab at the top
3. You'll see current rules (locked mode):
```json
{
  "rules": {
    ".read": false,
    ".write": false
  }
}
```

### Step 3: Replace with These Rules
Copy and paste this:
```json
{
  "rules": {
    "prodSanityReport": {
      ".read": true,
      ".write": false
    },
    "userSelections": {
      ".read": true,
      ".write": true
    }
  }
}
```

### Step 4: Publish
1. Click **"Publish"** button
2. Confirm the change

---

## 📋 What These Rules Do:

| Path | Read | Write | Purpose |
|------|------|-------|---------|
| `prodSanityReport` | ✅ Anyone | ❌ No one | Report data (only GitHub Actions can write via REST API with database secret) |
| `userSelections` | ✅ Anyone | ✅ Anyone | Your saved filter selections (you can save/load) |

---

## 🔒 Security Note:
- This allows anyone with the URL to save selections
- For production, add authentication
- For now, this is safe for internal team use

---

## ✅ After Updating Rules:
1. Refresh your live report page
2. Make a change to a dropdown
3. Click "💾 Save"
4. Should see "✓ Saved to Firebase" (no error!)

---

## 🆘 If Still Not Working:
Run this test in browser console (F12):
```javascript
database.ref('userSelections/test').set({ test: 'hello' })
  .then(() => console.log('✅ Write success!'))
  .catch(err => console.error('❌ Error:', err.message));
```
