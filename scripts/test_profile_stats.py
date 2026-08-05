#!/usr/bin/env python3
"""Focused regression tests for profile statistic updates."""

import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from daily_update import DailyUpdater


class ProfileStatsTests(unittest.TestCase):
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
