# 🚀 GitHub Profile Automation Setup Guide

## 📋 Prerequisites

1. **GitHub Personal Access Token** (Required)
2. **WakaTime API Key** (Optional - for coding time stats)

---

## 🔑 Step 1: Create GitHub Personal Access Token

1. Go to [GitHub Settings > Personal Access Tokens](https://github.com/settings/tokens)
2. Click "Generate new token" → "Generate new token (classic)"
3. Set the following permissions:
   - ✅ `repo` - Full control of private repositories
   - ✅ `workflow` - Update GitHub Action workflows  
   - ✅ `read:user` - Read user profile data
   - ✅ `user:email` - Access user email addresses
4. Set expiration to "No expiration" or your preferred duration
5. Copy the generated token (you won't see it again!)

---

## 🔑 Step 2: Get WakaTime API Key (Optional)

1. Sign up at [WakaTime.com](https://wakatime.com) if you haven't already
2. Install WakaTime extensions for your code editors:
   - [VS Code](https://marketplace.visualstudio.com/items?itemName=WakaTime.vscode-wakatime)
   - [PyCharm](https://plugins.jetbrains.com/plugin/7425-wakatime)
   - [Other editors](https://wakatime.com/plugins)
3. Go to [WakaTime Settings > API Key](https://wakatime.com/settings/api-key)
4. Copy your API key

---

## ⚙️ Step 3: Configure Repository Secrets

### Option A: Using GitHub Web Interface
1. Go to your repository: `https://github.com/Rayyan9477/Rayyan9477`
2. Click **Settings** → **Secrets and variables** → **Actions**
3. Click **"New repository secret"** and add:

| Secret Name | Value | Required |
|-------------|--------|----------|
| `GH_TOKEN` | Your GitHub Personal Access Token | ✅ Yes |
| `WAKATIME_API_KEY` | Your WakaTime API Key | ⚠️ Optional |

### Option B: Using GitHub CLI (if available)
```bash
# Set GitHub token
gh secret set GH_TOKEN --body "your_personal_access_token_here"

# Set WakaTime API key (optional)
gh secret set WAKATIME_API_KEY --body "your_wakatime_api_key_here"
```

---

## 🧪 Step 4: Test the Setup

### Manual Trigger Test
1. Go to **Actions** tab in your repository
2. Click **"🔄 Unified Daily Profile Update"**
3. Click **"Run workflow"** → **"Run workflow"**
4. Monitor the workflow execution

### Check Workflow Status
- ✅ **Green checkmark** = Everything working!
- ❌ **Red X** = Check the logs for errors
- 🟡 **Yellow circle** = Still running

---

## 🔧 Troubleshooting

### Common Issues:

#### ❌ "GITHUB_TOKEN secrets are required"
- **Solution**: Make sure `GH_TOKEN` secret is set with a valid Personal Access Token

#### ❌ "WakaTime API authentication failed"
- **Solution**: Check that `WAKATIME_API_KEY` secret is set correctly
- **Note**: This step will be skipped if no WakaTime key is provided

#### ❌ "Snake generation failed"
- **Solution**: Ensure your `GH_TOKEN` has `repo` and `read:user` permissions

#### ❌ "Push failed"
- **Solution**: Check that your token has `workflow` permissions

### Debug Steps:
1. Check **Actions** → **Latest workflow run** → **View logs**
2. Look for specific error messages
3. Verify all secrets are properly set
4. Ensure token permissions are correct

---

## 📊 What Gets Updated

When working properly, the automation will update:

- 🐍 **Contribution Snake** - Visual representation of your GitHub activity
- ⏰ **WakaTime Stats** - Your weekly coding time and languages  
- 📈 **GitHub Activity** - Recent commits, PRs, and issues
- 💡 **Daily Quote** - Inspirational developer quotes
- 📊 **GitHub Stats** - Followers, stars, and repo counts

---

## ⏰ Automation Schedule

- **Full Update**: Daily at 8:00 AM UTC
- **Activity Only**: Every 6 hours
- **Manual**: Can be triggered anytime via Actions tab

---

## 🔒 Security Notes

- ✅ Tokens are stored as encrypted secrets
- ✅ Workflows use minimal required permissions
- ✅ No secrets are logged or exposed
- ✅ Fallback to `github.token` if personal token unavailable

---

## 🆘 Need Help?

1. Check the [Actions logs](https://github.com/Rayyan9477/Rayyan9477/actions)
2. Verify your [repository secrets](https://github.com/Rayyan9477/Rayyan9477/settings/secrets/actions)
3. Test token permissions at [GitHub Token Checker](https://github.com/settings/tokens)

---

## ✅ Verification Checklist

- [ ] GitHub Personal Access Token created with correct permissions
- [ ] `GH_TOKEN` secret set in repository
- [ ] `WAKATIME_API_KEY` secret set (if using WakaTime)
- [ ] Workflow runs without errors
- [ ] README.md updates automatically
- [ ] Snake animation generates properly
- [ ] All components working as expected

**🎉 Once setup is complete, your profile will update automatically every day!**