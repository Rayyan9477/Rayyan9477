# WakaTime Integration Setup Guide

This guide will help you set up WakaTime integration with your GitHub profile README.

## Prerequisites

1. A WakaTime account (free at [wakatime.com](https://wakatime.com))
2. GitHub repository with admin access
3. GitHub Actions enabled

## Step 1: Get Your WakaTime API Key

1. Go to [WakaTime Settings](https://wakatime.com/settings/api-key)
2. Copy your API key (it looks like: `waka_xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx`)

## Step 2: Add WakaTime API Key to GitHub Secrets

1. Go to your GitHub repository
2. Navigate to **Settings** → **Secrets and variables** → **Actions**
3. Click **New repository secret**
4. Name: `WAKATIME_API_KEY`
5. Value: Paste your WakaTime API key
6. Click **Add secret**

## Step 3: Verify GitHub Token

The workflow uses `GITHUB_TOKEN` which is automatically provided by GitHub Actions. Make sure your repository has the following permissions:

1. Go to **Settings** → **Actions** → **General**
2. Under **Workflow permissions**, select **Read and write permissions**
3. Check **Allow GitHub Actions to create and approve pull requests**

## Step 4: Test the Integration

1. Go to **Actions** tab in your repository
2. Find the **Daily Metrics Update** workflow
3. Click **Run workflow** → **Run workflow**
4. Monitor the execution for any errors

## Troubleshooting

### Common Issues:

1. **"Invalid inputs" error**: Check that all required secrets are set
2. **"Environment variables are misconfigured"**: Verify WAKATIME_API_KEY is correct
3. **No stats appearing**: Make sure you have coding activity in WakaTime
4. **Permission denied**: Check repository permissions and token access

### Debug Steps:

1. Check the workflow logs in the Actions tab
2. Verify your WakaTime API key is valid
3. Ensure you have coding activity in the last 7 days
4. Check that the README.md file has the WakaTime section markers

## Configuration Options

The workflow is configured with these settings:

- **Time Range**: Last 7 days
- **Language Count**: Top 6 languages
- **Show Time**: Yes
- **Show Total**: Yes
- **Schedule**: Daily at 2 AM UTC
- **Section Name**: "📊 WakaTime Stats"

## Customization

You can modify the workflow in `.github/workflows/metrics.yml` to change:

- Time range (last_7_days, last_30_days, etc.)
- Number of languages shown
- Update frequency
- Section name and formatting

## Support

If you continue to have issues:

1. Check the [WakaReadme documentation](https://github.com/athul/waka-readme)
2. Review the workflow logs for specific error messages
3. Ensure your WakaTime account has coding activity 