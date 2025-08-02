"""
Poetry Service - Handles weather poetry generation
"""
import random
from .weather_service import WeatherService


class PoetryService:
    """Service for generating weather-based poetry"""
    
    def __init__(self, weather_service: WeatherService):
        self.weather_service = weather_service

    def generate_poem(self, city, unit="metric"):
        """Generate a poem based on current weather"""
        weather = self.weather_service.get_current_weather(city, unit)
        temp, desc = weather['temperature'], weather['description']
        return f"{city} weather inspires:\n{desc}, {temp}°\nNature sings in every degree."

    def generate_haiku(self, city, unit="metric"):
        """Generate a weather haiku (5-7-5 syllable pattern)"""
        weather = self.weather_service.get_current_weather(city, unit)
        temp = weather['temperature']
        desc = weather['description'].lower()
        
        # Haiku templates based on weather conditions
        haiku_templates = {
            'clear': [
                f"Clear skies above {city}\nSunlight dances on the earth\nWarmth at {temp} degrees",
                f"Blue expanse stretches\nOver {city}'s peaceful streets\n{temp}° pure delight"
            ],
            'clouds': [
                f"Clouds drift over {city}\nGray curtains veil the bright sun\n{temp}° whispers soft",
                f"Cotton clouds gather\nAbove {city}'s rooftops high\nCool {temp} degrees"
            ],
            'rain': [
                f"Raindrops kiss {city}\nNature's tears refresh the earth\n{temp}° cleansing shower",
                f"Gentle rain falls down\nOn {city}'s thirsty gardens\nSweet {temp} degrees"
            ],
            'snow': [
                f"Snowflakes dance in {city}\nWhite crystals paint the landscape\nCold {temp} degrees",
                f"Winter's gift descends\nUpon {city}'s sleeping streets\nFrozen {temp}°"
            ],
            'storm': [
                f"Thunder rolls through {city}\nLightning illuminates sky\nWild {temp} degrees",
                f"Storm clouds rage above\n{city} trembles with power\nFierce {temp}°"
            ]
        }
        
        # Select template based on weather description
        template_key = 'clear'
        for key in haiku_templates:
            if key in desc:
                template_key = key
                break
        
        return random.choice(haiku_templates[template_key])

    def generate_sonnet(self, city, unit="metric"):
        """Generate a weather sonnet (14 lines, ABAB CDCD EFEF GG rhyme scheme)"""
        weather = self.weather_service.get_current_weather(city, unit)
        temp = weather['temperature']
        desc = weather['description']
        humidity = weather.get('humidity', 'unknown')
        wind_speed = weather.get('wind_speed', 'gentle')
        
        sonnets = [
            f"""In {city} where the weather holds its sway,          (A)
The {desc} paints the sky with nature's art,        (B)
At {temp} degrees, the temperature today           (A)
Speaks to every wandering, hopeful heart.          (B)

The humidity at {humidity} percent doth rise,      (C)
While winds at {wind_speed} mph dance through the air,  (D)
Creating scenes that mesmerize the eyes,           (C)
And fill the atmosphere with beauty rare.          (D)

Oh {city}, your weather tells a tale              (E)
Of seasons turning, time's eternal flow,           (F)
Where sunshine, rain, and wind will never fail     (E)
To paint the world in hues we've come to know.     (F)

  So let us praise this day in {city} fair,        (G)
  Where weather weaves its magic in the air.       (G)""",

            f"""Upon the streets of {city} fair and bright,       (A)
The weather casts its spell across the land,       (B)
With {desc} that greets the morning light,         (A)
And {temp} degrees that nature has planned.        (B)

The elements conspire in harmony,                  (C)
As {wind_speed} mph winds begin to play,           (D)
Creating atmospheric symphony,                     (C)
That marks the beauty of this blessed day.         (D)

At {humidity}% humidity's embrace,                 (E)
The air itself becomes a work of art,              (F)
While weather patterns dance with subtle grace,    (E)
And touch the depths of every human heart.         (F)

  In {city}'s realm where sky and earth unite,     (G)
  The weather paints a canvas pure and bright.     (G)"""
        ]
        
        return random.choice(sonnets)

    def generate_limerick(self, city, unit="metric"):
        """Generate a weather limerick (AABBA rhyme scheme)"""
        weather = self.weather_service.get_current_weather(city, unit)
        temp = weather['temperature']
        desc = weather['description'].lower()
        
        limericks = [
            f"""There once was a place called {city},        (A)
Where the weather was quite pretty.       (A)
  With {desc} so fine,                     (B)
  At {temp} divine,                        (B)
The forecast was never too gritty!         (A)""",

            f"""A traveler came to {city} one day,          (A)
When the weather was perfect for play.     (A)
  The {desc} was sweet,                    (B)
  At {temp} degrees neat,                  (B)
Making everyone happy and gay!             (A)""",

            f"""The weather in {city} today,               (A)
Has much of importance to say.             (A)
  With {desc} so bright,                   (B)
  And {temp}° just right,                  (B)
It's a perfect and wonderful day!          (A)""",

            f"""In {city} the sky tells a tale,            (A)
Of weather that will never fail.           (A)
  The {desc} comes through,                (B)
  At {temp}° true,                         (B)
Like a ship with a strong, steady sail!    (A)"""
        ]
        
        return random.choice(limericks)

    def generate_free_verse(self, city, unit="metric"):
        """Generate free verse weather poetry"""
        weather = self.weather_service.get_current_weather(city, unit)
        temp = weather['temperature']
        desc = weather['description']
        humidity = weather.get('humidity', 'unknown')
        wind_speed = weather.get('wind_speed', 0)
        pressure = weather.get('pressure', 'steady')
        
        free_verses = [
            f"""{city}...
            
Where {desc} meets the earth
and {temp} degrees whisper
secrets to the wind.

The air, thick with {humidity}% humidity,
carries stories
of distant storms
and forgotten summers.

At {wind_speed} mph,
the breeze writes poetry
on every leaf,
every windowpane,
every face turned skyward.

This is the language
of atmosphere—
pressure at {pressure},
speaking in millibars
and heartbeats.

{city},
you are a poem
written by the sky.""",

            f"""Atmospheric Symphony in {city}

{temp} degrees—
the temperature of dreams,
where {desc} dances
with the rhythm of the earth.

Listen:
The wind at {wind_speed} mph
is composing verses
in a language only
the trees understand.

Humidity rises to {humidity}%,
moisture painting watercolors
on the canvas of morning.

The barometric pressure at {pressure}
presses against our souls,
reminding us
we are part of something
larger than ourselves.

In {city},
the weather is not just forecast—
it is poetry in motion,
a symphony written
by the invisible hand
of nature herself.""",

            f"""Weather Meditation: {city}

Breathe in:
{desc} at {temp} degrees
filling your lungs
with the essence of this moment.

Feel the {wind_speed} mph wind
as it carries messages
from distant places,
stories of rain and sunshine,
of storms weathered
and calm discovered.

The {humidity}% humidity
reminds us we are water,
mostly water,
connected to every cloud,
every ocean,
every tear.

Here in {city},
the weather teaches us
about impermanence,
about beauty in change,
about finding peace
in the eternal dance
of pressure and temperature,
wind and stillness.

{pressure} millibars
of atmospheric presence
pressing gently
on our existence,
reminding us:
we are here,
we are alive,
we are part of the weather
and the weather
is part of us."""
        ]
        
        return random.choice(free_verses)

    def generate_acrostic(self, city, unit="metric"):
        """Generate an acrostic poem using the city name and weather"""
        weather = self.weather_service.get_current_weather(city, unit)
        desc = weather['description'].capitalize()
        temp = weather['temperature']
        acrostic = []
        for i, letter in enumerate(city.upper()):
            if i == 0:
                line = f"{letter} - {desc} graces the sky."
            elif i == len(city) // 2:
                line = f"{letter} - Temperature: {temp}° brings a mood."
            else:
                line = f"{letter} - Weather's story continues."
            acrostic.append(line)
        return '\n'.join(acrostic)

    def generate_weather_riddle(self, city, unit="metric"):
        """Generate a weather-themed riddle for the city"""
        weather = self.weather_service.get_current_weather(city, unit)
        desc = weather['description'].lower()
        temp = weather['temperature']
        riddles = [
            f"I am felt but never seen, I can be gentle or mean. In {city}, today I am {desc} at {temp}°. What am I?",
            f"I fall from the sky, sometimes I am snow, sometimes I am rain. In {city}, I am {desc}. What am I?",
            f"I can be hot or cold, I change with the seasons. In {city}, I am {temp}°. What am I?"
        ]
        return random.choice(riddles)

    def generate_interactive_prompt(self, city, unit="metric"):
        """Generate an interactive poetry prompt for the user"""
        weather = self.weather_service.get_current_weather(city, unit)
        desc = weather['description']
        temp = weather['temperature']
        prompt = (
            f"Imagine you are standing in {city} where the weather is '{desc}' and the temperature is {temp}°. "
            "Write a short poem or a few lines describing how this weather makes you feel."
        )
        return prompt
