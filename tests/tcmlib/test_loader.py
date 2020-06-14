from pathlib import Path

import pytest
import tcmlib.loader as victim


def test_select_latest_videos_last_1(fixture_path_abs: Path):
    """Test whether the most recent vids are selected when only requesting 1 minute."""
    vgs = list(victim.generate_latest_video_groups(fixture_path_abs / "2020-06-02_09-10-25", 1))
    assert len(vgs) == 1
    assert vgs[0]["back"].name == "2020-06-02_09-10-05-back.mp4"


def test_select_latest_videos_last_2(fixture_path_abs: Path):
    """Test whether the most recent two minutes are selected in chronological order."""
    vgs = list(victim.generate_latest_video_groups(fixture_path_abs / "2020-06-02_09-10-25", 2))
    assert len(vgs) == 2
    assert vgs[0]["back"].name == "2020-06-02_09-09-04-back.mp4"
    assert vgs[1]["back"].name == "2020-06-02_09-10-05-back.mp4"


def test_select_latest_videos_incomplete(fixture_path_abs: Path):
    """Test whether an incomplete event (less than 4 videos) results in an exception."""
    with pytest.raises(FileNotFoundError):
        list(victim.generate_latest_video_groups(fixture_path_abs / "2020-03-14_18-56-32", 1))
