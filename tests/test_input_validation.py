from datetime import date, timedelta
import pytest
from minewaterwatch.core import analyze

START = date(2024, 1, 1)

def example(values):
    return [(START + timedelta(days=i), v) for i, v in enumerate(values)]

@pytest.mark.parametrize('series', [
    [(START + timedelta(days=1), 12.0), (START, 13.0)],
    [(START, 12.0), (START, 13.0)],
])
def test_analyze_rejects_unsorted_or_duplicate_dates(series):
    with pytest.raises(ValueError, match='strictly increasing'):
        analyze(series, min_segment=2)

@pytest.mark.parametrize('invalid', [-1.0, float('nan'), float('inf'), '12', True])
def test_analyze_rejects_invalid_inflow(invalid):
    with pytest.raises(ValueError, match='finite nonnegative'):
        analyze([(START, invalid), (START + timedelta(days=1), 5.0)], min_segment=2)

def test_analyze_rejects_datetime_strings():
    with pytest.raises(ValueError, match='datetime.date'):
        analyze([('2024-01-01', 12.0), ('2024-01-02', 15.0)], min_segment=2)

def test_analyze_succeeds_for_valid_direct_calls():
    result = analyze(example([5.0, 12.0, 13.0, 5.0]), threshold=10, min_segment=2)
    assert result['observations'] == 4
    assert result['exceedance_events'][0]['days'] == 2

def test_analyze_handles_missing_calendar_dates():
    result = analyze([(START, 12.0), (START + timedelta(days=2), 13.0)],
                     threshold=10, min_segment=2)
    assert result['missing_dates'] == ['2024-01-02']
    assert [event['days'] for event in result['exceedance_events']] == [1, 1]
