GREETINGS = (
    'Hi {{ name|title }}!',
    'Howdy {{ name|title }}!',
    'Welcome {{ name|title }}.',
)

WEATHER_REPORTS = (
    '{{ time }} the low is {{ low_temperature }}F and the high is {{ high_temperature }}. {{ description|title }}',
    # 'Well, right now it\'s {{ temperature }}F and {{ description }}',
    # '{{ description|title }} - {{ temperature }}F',
)

PARSE_ERROR = (
    'Sorry, I didn\'t understand that',
    'Huh?',
)

LOCATION_ERROR = (
    'Hmmm, I couldn\'t find {{ data }} on the map',
    'Sorry, I don\'t know where {{ data }} is',
)

WEATHER_ERROR = (
    'Sorry, I couldn\'t find weather for coordinates {{ data.lat }}, {{ data.long }}',
    'No weather available for coordinates {{ data.lat }}, {{ data.long }}',
)
