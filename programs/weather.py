import discord
from discord.ext import commands
import aiohttp
import datetime
import pytz


class weather(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        if hasattr(ctx.command, 'on_error'):
            return

        cog = ctx.cog
        if cog:
            if cog._get_overridden_method(cog.cog_command_error) is not None:
                return

        ignored = (commands.CommandNotFound)
        error = getattr(error, 'original', error)

        if isinstance(error, ignored):
            return

        if isinstance(error, commands.DisabledCommand):
            await ctx.send(f'> {ctx.command} has been disabled.')

        elif isinstance(error, commands.NoPrivateMessage):
            try:
                await ctx.author.send(
                    f'> {ctx.command} can not be used in Private Messages.')
            except discord.HTTPException:
                pass

        else:
            print('Ignoring exception in command {}:'.format(ctx.command),
                  file=sys.stderr)
            traceback.print_exception(type(error),
                                      error,
                                      error.__traceback__,
                                      file=sys.stderr)

    @commands.command()
    async def info(self, ctx, arg1, arg2):
        async with aiohttp.ClientSession() as cs:
            city = arg1
            city = city.capitalize()
            async with cs.get(
                    "https://api.openweathermap.org/data/2.5/weather?q=" +
                    city +
                    "&units=metric&appid=<your api id>"
            ) as r:
                data = await r.json()
                timezone = datetime.datetime.now(
                    tz=pytz.timezone('Asia/Kolkata'))
                date = timezone.strftime('%d %B, %A')
                time = timezone.strftime('%I:%M %p')

                country = data['sys']['country']
                weather = data['weather'][0]['main']
                weather_d = data['weather'][0]['description']
                temp = data['main']['temp']
                temp_min = data['main']['temp_min']
                temp_max = data['main']['temp_max']
                feels_like = data['main']['feels_like']
                humidity = data['main']['humidity']
                longitude = data['coord']['lon']
                latitude = data['coord']['lat']

                #for weather description
                if weather == 'Haze':
                    emoji = '🌫️'

                elif weather == 'Rain':
                    emoji = '🌧️'

                elif weather == 'Clouds':
                    emoji = '☁️'

                elif weather == 'Clear':
                    emoji = '🌤️'

                elif weather == 'Sunny':
                    emoji = '🌞'

                elif weather == 'Mist':
                    emoji = '☂️'

                elif weather == 'Thunderstorm':
                    emoji = '⛈️'

                else:
                    emoji = '🍃'

            #for temperatures
                if temp <= 5:
                    emoji_temp = '🥶'

                elif temp <= 20:
                    emoji_temp = '🤧'

                elif temp <= 25:
                    emoji_temp = '🙂'

                elif temp <= 30:
                    emoji_temp = '😘'

                elif temp <= 35:
                    emoji_temp = '🥵'

                elif temp <= 45:
                    emoji_temp = '🧨🔥'

                else:
                    emoji_temp = ' '

                if arg2 == 'all':
                    e = discord.Embed(
                        title="Weather Today 🌏",
                        description=
                        "You are currently viewing the current weather for **"
                        + city + ", " + country + "**.\n**" + str(date) +
                        "\n" + str(time) + "**",
                        color=0x9b59b6)

                    e.set_thumbnail(
                        url=
                        "https://cdn-icons-png.flaticon.com/512/414/414927.png"
                    )
                    e.add_field(name="📝  Weather description",
                                value=weather + ", " + weather_d + "  " +
                                emoji,
                                inline=False)
                    e.add_field(name="🌡️  Temperature",
                                value=str(temp) + " °C  " + emoji_temp,
                                inline=False)
                    e.add_field(name="❄️  Temperature MIN",
                                value=str(temp_min) + " °C",
                                inline=False)
                    e.add_field(name="🌵  Temperature MAX",
                                value=str(temp_max) + " °C",
                                inline=False)
                    e.add_field(name="😷  Feels like",
                                value=str(feels_like) + " °C",
                                inline=False)
                    e.add_field(name="💦  Humidity",
                                value=str(humidity) + " %",
                                inline=False)
                    e.add_field(name="📌  Coordinates",
                                value="• Longitude:  **" + str(longitude) +
                                "**" + "\n• Latitude:  **" + str(latitude) +
                                "**\n",
                                inline=False)

                    e.set_footer(text="Type info help to see more details.")
                    await ctx.send(embed=e)

                elif arg2 == 'temp':
                    e = discord.Embed(
                        title="🌡️  Temperature  " + emoji_temp,
                        description="The current temperature of **" + city +
                        "** is **" + str(temp) + " °C**.",
                        color=0x9b59b6)
                    e.add_field(name="❄️  Temperature MIN",
                                value=str(temp_min) + " °C",
                                inline=False)
                    e.add_field(name="🌵  Temperature MAX",
                                value=str(temp_max) + " °C",
                                inline=False)
                    await ctx.send(embed=e)

                elif arg2 == 'humidity':
                    e = discord.Embed(
                        title="💦  Humdity",
                        description="The current humidity of **" + city +
                        "** is **" + str(humidity) + " %**.",
                        color=0x9b59b6)
                    await ctx.send(embed=e)

                elif arg2 == 'weather':
                    e = discord.Embed(title="📝  Weather description",
                                      description="The current weather of **" +
                                      city + "** is **" + weather + ", " +
                                      weather_d + "**.",
                                      color=0x9b59b6)
                    await ctx.send(embed=e)

                else:
                    e = discord.Embed(title="😵  Confused!?",
                                      description="What you want me to do! 🤐",
                                      color=0x9b59b6)
                    e.set_footer(text="Type  `info help`  for details.")
                    await ctx.send(embed=e)

    @info.error
    async def info_handler(self, ctx, error):

        if isinstance(error, commands.MissingRequiredArgument):
            if error.param.name == 'arg2':

                e = discord.Embed(
                    title="❌  Error",
                    description=
                    "Missing Argument Error!\nor\nIf you have typed  `info help`  then you need to use a real, valid state name and use these below arguments.",
                    color=0x9b59b6)
                e.add_field(name="✓  Correct Arguments",
                            value="all, weather, temp, humidity",
                            inline=False)
                e.add_field(
                    name="‣ 'all' Argument:",
                    value=
                    "↪ To view each and every weather data for that area.",
                    inline=False)
                e.add_field(
                    name="‣ 'weather' Argument:",
                    value="↪ To view weather description for that area only.",
                    inline=False)
                e.add_field(
                    name="‣ 'temp' Argument:",
                    value=
                    "↪ To view temperature for that area along with minimum and maximum temperatures.",
                    inline=False)
                e.add_field(name="‣ 'humidity' Argument:",
                            value="↪ To view humidity for that area only.",
                            inline=False)
                e.add_field(
                    name="🗒️  __For example:__",
                    value=
                    "Type  `info delhi temp`  to view the temperature of **Delhi**.",
                    inline=False)
                await ctx.send(embed=e)


def setup(bot):
    bot.add_cog(weather(bot))
