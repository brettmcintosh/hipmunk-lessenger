GREETINGS = (
    'Hi {{ name|title }}!',
    'Howdy {{ name|title }}!',
    'Welcome {{ name|title }}.',
)

FORECASTS = (
    'Currently it\'s {{ temperature }}F. {{ description|title }}',
    'Well, right now it\'s {{ temperature }}F and {{ description }}',
    '{{ description|title }} - {{ temperature }}F',
)
