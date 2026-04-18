# GitHub Actions Schedule & Manual Trigger Guide

## ⚡ Current Schedule: Every 1 Hour

Your workflow now runs **automatically every hour** and can be **triggered manually anytime**.

---

## 🎯 Manual Trigger (Execute Whenever Required)

### **How to Run On-Demand:**

1. **Go to GitHub Actions:**
   ```
   https://github.com/Vishnuramalingam07/Myisp_Tools/actions
   ```

2. **Click on workflow:**
   - Select **"Fetch ADO Test Results and Update Firebase"**

3. **Trigger manually:**
   - Click **"Run workflow"** dropdown (top right)
   - Click green **"Run workflow"** button
   - Wait ~2-3 minutes
   - Check your live report for updates

**Result:** Fresh data fetched from ADO and uploaded to Firebase immediately! ✅

---

## 📅 Schedule Options (Customize as Needed)

Edit `.github/workflows/fetch-ado-data.yml` and change the cron schedule:

### **Common Schedules:**

| Interval | Cron Expression | Description |
|----------|----------------|-------------|
| **Every 30 minutes** | `*/30 * * * *` | Very frequent (48 runs/day) |
| **Every hour** | `0 * * * *` | Current setting (24 runs/day) |
| **Every 2 hours** | `0 */2 * * *` | Balanced (12 runs/day) |
| **Every 4 hours** | `0 */4 * * *` | Original (6 runs/day) |
| **Every 6 hours** | `0 */6 * * *` | Conservative (4 runs/day) |
| **Twice daily** | `0 9,17 * * *` | 9am & 5pm UTC (2 runs/day) |
| **Daily at 8am** | `0 8 * * *` | Morning update only (1 run/day) |
| **Weekdays only** | `0 9 * * 1-5` | Monday-Friday at 9am UTC |

### **How to Change:**

1. Open `.github/workflows/fetch-ado-data.yml`
2. Find the line:
   ```yaml
   - cron: '0 * * * *'
   ```
3. Replace with your preferred schedule from table above
4. Commit and push to GitHub

---

## 🚀 Quick Update Options

### **Option 1: Manual Trigger (Instant)**
- **Speed:** ~2-3 minutes
- **When:** Whenever you click "Run workflow"
- **Best for:** Immediate updates after ADO changes

### **Option 2: Automatic Schedule (Hourly)**
- **Speed:** Updates every hour automatically
- **When:** Background, no action needed
- **Best for:** Keeping data fresh without manual work

### **Option 3: Push-Triggered (Uncomment in workflow)**
- **Speed:** Runs on every git push
- **When:** After you push code changes
- **Best for:** Development/testing

To enable push-triggered, uncomment in workflow file:
```yaml
push:
  branches: [ main ]
```

---

## 💰 Usage Impact

### **Free Tier Limits:**
- Public repos: **Unlimited minutes** ✅
- Private repos: **2,000 minutes/month**

### **Your Estimated Usage:**

| Schedule | Runs/Day | Minutes/Day | Minutes/Month |
|----------|----------|-------------|---------------|
| Every 30 min | 48 | 192 min | **~5,760 min** ⚠️ |
| **Every hour** | 24 | 96 min | **~2,880 min** (current) |
| Every 2 hours | 12 | 48 min | ~1,440 min ✅ |
| Every 4 hours | 6 | 24 min | ~720 min ✅ |

**Recommendation:**
- ✅ **Every hour** is good for most use cases
- ✅ Use **manual trigger** for immediate updates
- ⚠️ **Every 30 min** may exceed free tier for private repos

---

## 📊 Real-World Example

### **Scenario: Need fresh data NOW**

```
9:00 AM - Tests completed in Azure DevOps
9:01 AM - You click "Run workflow" in GitHub
9:03 AM - Firebase updated with latest data
9:04 AM - Team views live report with fresh results
```

**No waiting for the next scheduled run!**

---

## 🛠️ Advanced: Run Only During Work Hours

If you only need updates during business hours:

```yaml
schedule:
  # Every hour from 8am-6pm UTC, weekdays only
  - cron: '0 8-18 * * 1-5'
```

This saves GitHub Actions quota and focuses updates when your team is active.

---

## 🎯 Recommended Setup

**Best configuration for most teams:**

```yaml
on:
  # Automatic: Every 2 hours during work hours
  schedule:
    - cron: '0 8-18/2 * * 1-5'  # Mon-Fri, 8am-6pm UTC, every 2 hours
  
  # Manual: Run anytime via GitHub UI
  workflow_dispatch:
```

This gives you:
- ✅ Auto-updates during business hours (5-6 times/day)
- ✅ Manual trigger for immediate updates
- ✅ Saves quota during nights/weekends
- ✅ ~600 minutes/month usage (well within limits)

---

## 📞 Quick Reference

### **I need fresh data RIGHT NOW:**
→ Go to GitHub Actions → Click "Run workflow"

### **I want hourly auto-updates:**
→ Already configured! ✅

### **I want to change the schedule:**
→ Edit `.github/workflows/fetch-ado-data.yml` → Change cron value → Commit & push

### **How do I check if it's working:**
→ GitHub Actions page shows green ✅ or red ❌ for each run

---

**Updated:** April 18, 2026  
**Current Setting:** Every 1 hour + Manual trigger available
