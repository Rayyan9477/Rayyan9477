#!/usr/bin/env python3
"""Focused regression tests for profile statistic updates."""

import re
import sys
import unittest
from datetime import datetime, timedelta, timezone
from pathlib import Path
from unittest.mock import Mock, patch

sys.path.insert(0, str(Path(__file__).resolve().parent))
from daily_update import DailyUpdater


class ProfileStatsTests(unittest.TestCase):
    def test_readme_dashboard_has_no_duplicate_or_mismatched_values(self):
        readme = (Path(__file__).resolve().parent.parent / 'README.md').read_text(
            encoding='utf-8'
        )
        self.assertNotIn('<!--PROFILE_VIEWS-->', readme)

        pairs = [
            (r'/badge/Followers-([\d,]+)-', r'<!--FOLLOWERS-->([\d,]+)<!--/FOLLOWERS-->'),
            (r'/badge/Total_Stars-([\d,]+)-', r'<!--TOTAL_STARS-->([\d,]+)<!--/TOTAL_STARS-->'),
            (r'/badge/Current_Streak-(\d+)_Days-', r'<!--CURRENT_STREAK-->(\d+)<!--/CURRENT_STREAK-->'),
        ]
        for badge_pattern, marker_pattern in pairs:
            badge = re.search(badge_pattern, readme)
            marker = re.search(marker_pattern, readme)
            self.assertIsNotNone(badge)
            self.assertIsNotNone(marker)
            self.assertEqual(badge.group(1), marker.group(1))

    def test_skips_unfinished_today_when_calculating_streak(self):
        days = [
            {'date': '2026-08-05', 'contributionCount': 0},
            {'date': '2026-08-04', 'contributionCount': 5},
            {'date': '2026-08-03', 'contributionCount': 2},
            {'date': '2026-08-02', 'contributionCount': 0},
        ]
        self.assertEqual(DailyUpdater._calculate_current_streak(days, '2026-08-05'), 2)

    def test_stops_at_real_streak_break(self):
        days = [
            {'date': '2026-08-05', 'contributionCount': 3},
            {'date': '2026-08-04', 'contributionCount': 0},
            {'date': '2026-08-03', 'contributionCount': 2},
        ]
        self.assertEqual(DailyUpdater._calculate_current_streak(days, '2026-08-05'), 1)

    def test_fetches_prior_window_when_streak_exceeds_one_year(self):
        today = datetime.now(timezone.utc).date()
        current_window = [
            {
                'date': (today - timedelta(days=offset)).isoformat(),
                'contributionCount': 1,
            }
            for offset in range(365)
        ]
        prior_window = [
            {
                'date': (today - timedelta(days=offset)).isoformat(),
                'contributionCount': 1 if offset <= 377 else 0,
            }
            for offset in range(365, 730)
        ]

        def response_for(days):
            response = Mock(status_code=200)
            response.json.return_value = {
                'data': {
                    'user': {
                        'contributionsCollection': {
                            'contributionCalendar': {
                                'weeks': [{'contributionDays': days}],
                            }
                        }
                    }
                }
            }
            return response

        updater = DailyUpdater.__new__(DailyUpdater)
        updater.GH_TOKEN = 'test-token'
        updater.username = 'Rayyan9477'
        updater.log = lambda *args, **kwargs: None

        with patch(
            'daily_update.requests.post',
            side_effect=[response_for(current_window), response_for(prior_window)],
        ) as post:
            self.assertEqual(updater._get_streak_from_github_api(), 378)
            self.assertEqual(post.call_count, 2)

    def test_failed_repository_page_does_not_publish_zero_stars(self):
        updater = DailyUpdater.__new__(DailyUpdater)
        updater.username = 'Rayyan9477'
        updater.log = lambda *args, **kwargs: None
        response = Mock(status_code=503)

        with patch('daily_update.requests.get', return_value=response):
            self.assertIsNone(updater._get_total_stars({}))

    def test_replaces_only_requested_stat_marker(self):
        content = '<!--TOTAL_STARS-->214<!--/TOTAL_STARS--> <!--FOLLOWERS-->93<!--/FOLLOWERS-->'
        updated = DailyUpdater._replace_stat_marker(content, 'TOTAL_STARS', 215)
        self.assertIn('<!--TOTAL_STARS-->215<!--/TOTAL_STARS-->', updated)
        self.assertIn('<!--FOLLOWERS-->93<!--/FOLLOWERS-->', updated)

    def test_language_card_is_valid_svg_with_escaped_labels(self):
        card = DailyUpdater._build_languages_card({'Python': 12, 'C# & .NET': 3})
        self.assertTrue(card.startswith('<svg'))
        self.assertIn('Python', card)
        self.assertIn('C# &amp; .NET', card)
        self.assertIn('</svg>', card)


if __name__ == '__main__':
    unittest.main()
