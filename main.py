# main.py
import os
import discord
import requests
from discord.ext import commands
from dotenv import load_dotenv

# --- SETUP ---
load_dotenv()
DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')
TMDB_API_KEY = os.getenv('TMDB_API_KEY')

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)

# --- API HELPER FUNCTIONS ---

def get_movie_id(movie_title):
    """Searches for a movie and returns its TMDB ID."""
    url = f"https://api.themoviedb.org/3/search/movie"
    params = {'api_key': TMDB_API_KEY, 'query': movie_title}
    response = requests.get(url, params=params)
    data = response.json()
    if data.get('results'):
        return data['results'][0]['id']
    return None

def get_movie_recommendations(movie_id):
    """Gets a list of recommended movies for a given movie ID."""
    url = f"https://api.themoviedb.org/3/movie/{movie_id}/recommendations"
    params = {'api_key': TMDB_API_KEY}
    response = requests.get(url, params=params)
    data = response.json()
    return data.get('results', [])[:5] # Return top 5 or empty list

def get_book_subjects(book_title):
    """Finds the subjects/genres for a given book title."""
    url = f"http://openlibrary.org/search.json"
    params = {'q': book_title}
    response = requests.get(url, params=params)
    data = response.json()
    if data.get('docs') and 'subject' in data['docs'][0]:
        return data['docs'][0]['subject'][:3] # Return top 3 subjects
    return []

def get_books_by_subject(subject):
    """Gets a list of books for a given subject."""
    url = f"http://openlibrary.org/subjects/{subject.lower().replace(' ', '_')}.json"
    params = {'limit': 5}
    response = requests.get(url, params=params)
    data = response.json()
    return data.get('works', [])

# --- BOT EVENTS ---

@bot.event
async def on_ready():
    """Prints a message to the console when the bot is online."""
    print(f'{bot.user.name} has connected to Discord!')
    print('-----------------------------------------')

# --- BOT COMMANDS ---

@bot.command(name='hello')
async def hello(ctx):
    """A simple test command."""
    await ctx.send(f'Hello, {ctx.author.name}!')

@bot.command(name='movie')
async def movie(ctx, *, search_title: str):
    """Recommends movies based on a given movie title."""
    movie_id = get_movie_id(search_title)
    if not movie_id:
        await ctx.send(f"Sorry, I couldn't find the movie '{search_title}'.")
        return

    recommendations = get_movie_recommendations(movie_id)
    if not recommendations:
        await ctx.send(f"I found '{search_title}', but couldn't find any recommendations.")
        return

    embed = discord.Embed(
        title=f"Recommendations for '{search_title.title()}'",
        description="Here are some movies you might also like:",
        color=discord.Color.blue()
    )
    for rec in recommendations:
        title = rec['title']
        release_date = rec.get('release_date', 'N/A').split('-')[0]
        embed.add_field(name=f"{title} ({release_date})", value="", inline=False)
    
    embed.set_footer(text="Powered by The Movie Database (TMDB)")
    await ctx.send(embed=embed)

@bot.command(name='book')
async def book(ctx, *, search_title: str):
    """Recommends books based on a given book's genres."""
    subjects = get_book_subjects(search_title)
    if not subjects:
        await ctx.send(f"Sorry, I couldn't find '{search_title}' or its genres.")
        return

    primary_subject = subjects[0]
    recommendations = get_books_by_subject(primary_subject)
    if not recommendations:
        await ctx.send(f"Found the book, but couldn't find recommendations in the genre: '{primary_subject}'.")
        return

    embed = discord.Embed(
        title=f"Recommendations for '{search_title.title()}'",
        description=f"Based on the genre: **{primary_subject}**",
        color=discord.Color.orange()
    )
    for rec in recommendations:
        title = rec['title']
        author = rec.get('authors', [{'name': 'Unknown Author'}])[0]['name']
        embed.add_field(name=f"{title}", value=f"by {author}", inline=False)
    
    embed.set_footer(text="Powered by Open Library")
    await ctx.send(embed=embed)     
print(f"Attempting to run with token: {DISCORD_TOKEN}")
# --- RUN THE BOT ---
bot.run(DISCORD_TOKEN)

