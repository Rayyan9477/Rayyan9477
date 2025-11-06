#!/usr/bin/env python3
"""
GitHub Contributions Fetcher
Fetches real contribution data using GitHub's GraphQL API
"""

import os
import requests
from datetime import datetime
from typing import Dict, Any

class GitHubContributionsFetcher:
    def __init__(self):
        self.token = os.getenv('GH_TOKEN') or os.getenv('GITHUB_TOKEN')
        self.username = 'Rayyan9477'
        self.graphql_url = 'https://api.github.com/graphql'
    
    def fetch_contributions(self) -> Dict[str, Any]:
        """Fetch contribution statistics using GitHub GraphQL API"""
        if not self.token:
            print("⚠️ No GitHub token found, cannot fetch contributions")
            return self._get_fallback_data()
        
        # GraphQL query to get contribution data
        query = """
        query($username: String!) {
          user(login: $username) {
            contributionsCollection {
              contributionCalendar {
                totalContributions
              }
              restrictedContributionsCount
            }
            repositories(first: 100, ownerAffiliations: OWNER) {
              totalCount
              nodes {
                stargazerCount
                forkCount
                languages(first: 10) {
                  edges {
                    size
                    node {
                      name
                    }
                  }
                }
              }
            }
            followers {
              totalCount
            }
            contributionsCollection {
              totalCommitContributions
              totalIssueContributions
              totalPullRequestContributions
              totalPullRequestReviewContributions
            }
          }
        }
        """
        
        headers = {
            'Authorization': f'Bearer {self.token}',
            'Content-Type': 'application/json'
        }
        
        try:
            response = requests.post(
                self.graphql_url,
                json={'query': query, 'variables': {'username': self.username}},
                headers=headers,
                timeout=15
            )
            
            if response.status_code != 200:
                print(f"⚠️ GraphQL API returned status {response.status_code}")
                return self._get_fallback_data()
            
            data = response.json()
            
            if 'errors' in data:
                print(f"⚠️ GraphQL errors: {data['errors']}")
                return self._get_fallback_data()
            
            user_data = data['data']['user']
            contributions = user_data['contributionsCollection']
            
            # Calculate total stars and forks
            total_stars = sum(repo['stargazerCount'] for repo in user_data['repositories']['nodes'])
            total_forks = sum(repo['forkCount'] for repo in user_data['repositories']['nodes'])
            
            # Get this year's contributions
            this_year_contributions = contributions['contributionCalendar']['totalContributions']
            
            # Calculate total contributions (this is an estimate)
            total_commits = contributions['totalCommitContributions']
            total_issues = contributions['totalIssueContributions']
            total_prs = contributions['totalPullRequestContributions']
            total_reviews = contributions['totalPullRequestReviewContributions']
            
            # For lifetime contributions, we need to make multiple queries
            # For now, we'll estimate based on current year data
            lifetime_total = self._estimate_lifetime_contributions(this_year_contributions)
            
            result = {
                'followers': user_data['followers']['totalCount'],
                'public_repos': user_data['repositories']['totalCount'],
                'total_stars': total_stars,
                'total_forks': total_forks,
                'this_year_contributions': this_year_contributions,
                'total_contributions': lifetime_total,
                'total_commits': total_commits,
                'total_issues': total_issues,
                'total_prs': total_prs,
                'total_reviews': total_reviews,
                'updated_at': datetime.now().isoformat()
            }
            
            print(f"✅ Fetched GitHub contributions:")
            print(f"   • This Year: {this_year_contributions:,}")
            print(f"   • Estimated Total: {lifetime_total:,}")
            print(f"   • Commits: {total_commits:,}")
            print(f"   • Followers: {result['followers']:,}")
            print(f"   • Stars: {total_stars:,}")
            
            return result
            
        except requests.exceptions.Timeout:
            print("⚠️ Request timed out")
            return self._get_fallback_data()
        except Exception as e:
            print(f"❌ Error fetching contributions: {e}")
            return self._get_fallback_data()
    
    def _estimate_lifetime_contributions(self, this_year: int) -> int:
        """
        Estimate lifetime contributions based on this year's data
        This is a rough estimate - for accurate data, you'd need to query each year
        """
        # Assuming the account was created in 2020 (adjust as needed)
        account_age_years = datetime.now().year - 2020
        
        # Conservative estimate: assume 70% of current year's pace for previous years
        if account_age_years > 0:
            estimated_total = this_year + (this_year * 0.7 * account_age_years)
            return int(estimated_total)
        return this_year
    
    def _get_fallback_data(self) -> Dict[str, Any]:
        """Return fallback data when API calls fail"""
        return {
            'followers': 0,
            'public_repos': 0,
            'total_stars': 0,
            'total_forks': 0,
            'this_year_contributions': 0,
            'total_contributions': 0,
            'total_commits': 0,
            'total_issues': 0,
            'total_prs': 0,
            'total_reviews': 0,
            'updated_at': datetime.now().isoformat(),
            'fallback': True
        }

def main():
    """Main entry point"""
    fetcher = GitHubContributionsFetcher()
    data = fetcher.fetch_contributions()
    
    # Print data in a format that can be used by other scripts
    if not data.get('fallback', False):
        print("\n=== GitHub Statistics ===")
        print(f"Total Contributions: {data['total_contributions']:,}")
        print(f"This Year: {data['this_year_contributions']:,}")
        print(f"Followers: {data['followers']:,}")
        print(f"Total Stars: {data['total_stars']:,}")
        print(f"Public Repos: {data['public_repos']:,}")
    else:
        print("\n⚠️ Using fallback data - please check your GitHub token")
    
    return data

if __name__ == "__main__":
    main()
