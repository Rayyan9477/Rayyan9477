# 🤖 Daily README Automation System

A comprehensive automation system that updates your GitHub README daily with fresh quotes, GitHub statistics, and contribution snakes - all in a single commit.

## 🎯 Features

- **📅 Daily Automation**: Runs automatically every day at 8:00 AM UTC
- **💡 Dynamic Quotes**: Fetches inspirational quotes from API with fallback options
- **📊 GitHub Stats**: Updates followers, stars, and repository statistics
- **🐍 Contribution Snake**: Generates latest contribution visualization
- **🔒 Single Commit**: All updates bundled into one clean commit per day
- **📝 Comprehensive Logging**: Detailed logs for monitoring and debugging
- **⚙️ Configurable**: Easy customization via `config.json`
- **🧪 Testing**: Built-in test suite for validation

## 🚀 Quick Start

### 1. Prerequisites

- Python 3.8+
- Git repository with GitHub Actions enabled
- GitHub Personal Access Token (for stats fetching)

### 2. Setup

1. **Clone or add files to your repository:**
   ```bash
   # Add the automation files to your repo
   scripts/daily_update.py
   .github/workflows/daily-update.yml
   config.json
   requirements.txt
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure GitHub Token:**
   - Go to GitHub Settings → Developer Settings → Personal Access Tokens
   - Create a new token with `repo` and `read:user` permissions
   - Add it to your repository secrets as `GITHUB_TOKEN`

4. **Customize configuration:**
   - Edit `config.json` to match your GitHub username and preferences
   - Modify schedule, timezone, and other settings as needed

### 3. Test the System

```bash
# Run the test suite
cd scripts
python test_daily_update.py
```

### 4. Manual Run

```bash
# Test the system manually (without pushing)
cd scripts
PUSH_CHANGES=false python daily_update.py

# Run with automatic push
cd scripts
python daily_update.py
```

## 📁 File Structure

```
├── scripts/
│   ├── daily_update.py          # Main automation script
│   ├── test_daily_update.py     # Test suite
│   ├── update_quote.py          # Legacy quote updater
│   ├── update_readme.py         # Legacy README updater
│   ├── github_stats.py          # Legacy stats fetcher
│   └── generate_snake.py        # Legacy snake generator
├── .github/workflows/
│   └── daily-update.yml         # GitHub Actions workflow
├── assets/
│   └── github-contribution-grid-snake.svg  # Generated snake
├── config.json                  # Configuration file
├── requirements.txt             # Python dependencies
├── daily_update.log            # Runtime logs
└── README.md                   # Your main README
```

## ⚙️ Configuration

### config.json Structure

```json
{
  "github": {
    "username": "YourGitHubUsername",
    "repository": "YourRepositoryName",
    "branch": "main"
  },
  "daily_update": {
    "enabled": true,
    "schedule": "0 8 * * *",
    "timezone": "UTC",
    "auto_push": true,
    "log_level": "INFO",
    "max_retries": 3,
    "timeout": 30
  },
  "quotes": {
    "api_url": "https://api.quotable.io/random",
    "fallback_enabled": true,
    "max_length": 200,
    "categories": ["technology", "programming", "innovation"]
  },
  "github_stats": {
    "enabled": true,
    "include_stars": true,
    "include_forks": true,
    "include_contributions": true,
    "update_badges": true
  },
  "contribution_snake": {
    "enabled": true,
    "theme": "tokyonight",
    "output_format": "svg",
    "include_dark_theme": true
  },
  "readme": {
    "file_path": "README.md",
    "backup_enabled": true,
    "backup_retention_days": 7,
    "update_timestamps": true,
    "preserve_formatting": true
  }
}
```

### Key Configuration Options

| Option | Description | Default |
|--------|-------------|---------|
| `daily_update.schedule` | Cron schedule for automation | `"0 8 * * *"` |
| `daily_update.timezone` | Timezone for scheduling | `"UTC"` |
| `quotes.api_url` | Quote API endpoint | `"https://api.quotable.io/random"` |
| `github_stats.enabled` | Enable GitHub stats fetching | `true` |
| `contribution_snake.enabled` | Enable snake generation | `true` |

## 🔧 GitHub Actions Workflow

The automation runs via GitHub Actions with the following features:

- **Scheduled Execution**: Daily at 8:00 AM UTC
- **Manual Trigger**: Can be run manually via GitHub Actions tab
- **Error Handling**: Comprehensive error logging and artifact upload
- **Security**: Uses repository secrets for tokens
- **Notifications**: Success/failure notifications in logs

### Workflow Triggers

```yaml
on:
  schedule:
    - cron: '0 8 * * *'  # Daily at 8 AM UTC
  workflow_dispatch:     # Manual trigger
  push:
    branches: [ main ]
    paths:
      - 'scripts/daily_update.py'
      - '.github/workflows/daily-update.yml'
```

## 📊 What Gets Updated

### 1. Daily Quote
- Fetches from external API (quotable.io)
- Falls back to curated tech quotes if API fails
- Updates the quote section in README.md
- Updates timestamp comment

### 2. GitHub Statistics
- Fetches latest follower count
- Updates repository statistics
- Refreshes GitHub badges
- Handles rate limiting gracefully

### 3. Contribution Snake
- Generates latest contribution visualization
- Uses Platane/snk API
- Saves as SVG in assets folder
- Updates README reference

### 4. Timestamps
- Updates "Last Updated" timestamp
- Updates "Quote Updated" timestamp
- Maintains audit trail

## 🧪 Testing

### Run Test Suite

```bash
cd scripts
python test_daily_update.py
```

### Test Components Individually

```bash
# Test quote fetching
python -c "from daily_update import DailyUpdater; print(DailyUpdater().get_daily_quote())"

# Test GitHub stats (requires token)
GITHUB_TOKEN=your_token python -c "from daily_update import DailyUpdater; print(DailyUpdater().get_github_stats())"

# Test snake generation
python -c "from daily_update import DailyUpdater; print(DailyUpdater().generate_contribution_snake())"
```

### Test Without Committing

```bash
# Set environment variable to disable pushing
PUSH_CHANGES=false python daily_update.py
```

## 🔍 Monitoring & Logs

### Log Files

- `daily_update.log`: Main runtime logs
- `test_report.json`: Test execution results
- GitHub Actions logs: Available in Actions tab

### Log Levels

- `INFO`: General information and success messages
- `WARNING`: Non-critical issues (API fallbacks, etc.)
- `ERROR`: Critical failures that prevent updates

### Sample Log Output

```
[2025-01-15 08:00:01] INFO: 🚀 Daily Update Script Started
[2025-01-15 08:00:02] INFO: ✅ Fetched quote from API: 'The best way to predict the future...' by Alan Kay
[2025-01-15 08:00:03] INFO: ✅ GitHub stats fetched: 15 repos, 25 followers, 100 stars
[2025-01-15 08:00:04] INFO: ✅ Generated contribution snake SVG
[2025-01-15 08:00:05] INFO: ✅ Updated daily quote in README
[2025-01-15 08:00:06] INFO: ✅ Updated GitHub stats badges
[2025-01-15 08:00:07] INFO: ✅ README content updated successfully
[2025-01-15 08:00:08] INFO: ✅ Added all changes to git
[2025-01-15 08:00:09] INFO: ✅ Changes committed successfully
[2025-01-15 08:00:10] INFO: ✅ Changes pushed to remote repository
[2025-01-15 08:00:11] INFO: 🎉 Daily update completed successfully!
```

## 🛠️ Troubleshooting

### Common Issues

#### 1. GitHub Token Issues
```
❌ Error fetching GitHub stats: 401 Client Error
```
**Solution**: Verify your GitHub token has correct permissions and is properly set in repository secrets.

#### 2. API Rate Limiting
```
⚠️ GitHub API rate limit exceeded
```
**Solution**: The system handles this gracefully by skipping stats updates. Consider using a token with higher rate limits.

#### 3. Quote API Failures
```
⚠️ API quote fetch failed: Connection timeout
```
**Solution**: The system automatically falls back to predefined quotes. No action needed.

#### 4. Git Push Failures
```
❌ Push failed: Permission denied
```
**Solution**: Ensure the GitHub Actions workflow has write permissions to the repository.

### Debug Mode

Enable detailed logging by setting the log level:

```bash
# In config.json
"daily_update": {
  "log_level": "DEBUG"
}
```

### Manual Recovery

If the automation fails, you can manually run:

```bash
# Reset any partial changes
git reset --hard HEAD

# Run update manually
cd scripts
python daily_update.py
```

## 🔒 Security Considerations

- **Token Security**: GitHub tokens are stored as repository secrets
- **API Limits**: System handles rate limiting gracefully
- **Error Sanitization**: Sensitive information is not logged
- **Backup System**: README is backed up before testing

## 📈 Performance

- **Execution Time**: Typically 10-30 seconds
- **API Calls**: Minimal (1-3 calls per run)
- **Storage**: Small log files (< 1MB)
- **Bandwidth**: Minimal (SVG generation + API calls)

## 🤝 Contributing

To contribute to this automation system:

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Submit a pull request

## 📄 License

This automation system is open source and available under the MIT License.

## 🆘 Support

If you encounter issues:

1. Check the logs in `daily_update.log`
2. Run the test suite: `python test_daily_update.py`
3. Review GitHub Actions logs
4. Check the troubleshooting section above
5. Open an issue with detailed error information

---

**Happy Automating! 🚀**

*This system ensures your README stays fresh and engaging with minimal manual intervention.* 