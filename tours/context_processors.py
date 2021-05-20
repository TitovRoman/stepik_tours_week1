import tours.data as mock_data


def add_title_and_departures(request):
    return {
        'title': mock_data.title,
        'departures': mock_data.departures,
    }
