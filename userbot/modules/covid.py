# Copyright (C) 2019 The Raphielscape Company LLC.
#
# Licensed under the Raphielscape Public License, Version 1.d (the "License");
# you may not use this file except in compliance with the License.
#
# Port to UserBot by @MoveAngel
from covid import Covid
from userbot import CMD_HELP
from userbot.events import register
from json import loads
from urllib.request import urlopen


@register(outgoing=True, pattern="^.covid (.*)")
async def corona(event):
    await event.edit("`Processing...`")
    country = event.pattern_match.group(1)
    covid = Covid(source="worldometers")
    try:
        country_data = covid.get_status_by_country_name(country)
        output_text = (
            f"`Confirmed   : {country_data['confirmed']}`\n" +
            f"`Active      : {country_data['active']}`\n" +
            f"`Deaths      : {country_data['deaths']}`\n" +
            f"`Recovered   : {country_data['recovered']}`\n\n" +
            f"`New Cases   : {country_data['new_cases']}`\n" +
            f"`New Deaths  : {country_data['new_deaths']}`\n" +
            f"`Critical    : {country_data['critical']}`\n" +
            f"`Total Tests : {country_data['total_tests']}`\n\n" +
            f"Data provided by [Worldometer](https://www.worldometers.info/coronavirus/country/{country})")
        await event.edit(f"Corona Virus Info in {country}:\n\n{output_text}")
    except ValueError:
        await event.edit(
            f"No information found for: {country}!\nCheck your spelling and try again."
        )


@register(outgoing=True, pattern="^.covidindia (.*)")
async def corona_india(event):
    await event.edit("`Processing...`")
    args = event.pattern_match.group(1).split(" ", 1)
    state = args[0].upper()
    district = ""
    with urlopen("https://api.covid19india.org/v3/data.json") as url:
        raw_data = loads(url.read().decode())

    if len(args) == 1:
        if state in raw_data:
            data = raw_data[state]
            delta = raw_data[state].get('delta', "N/A")
            if delta == "N/A":
                delta_cnf = "N/A"
                delta_dec = "N/A"
                delta_rec = "N/A"

            else:
                delta_cnf = data['delta'].get('confirmed', 0)
                delta_dec = data['delta'].get('deceased', 0)
                delta_rec = data['delta'].get('recovered', 0)

            output_text = f"`Confirmed    : {data['total'].get('confirmed', 0)} ({delta_cnf})`\n"
            output_text += f"`Active      : {data['total'].get('confirmed', 0) - (data['total'].get('recovered', 0) + data['total'].get('deceased', 0))}`\n"
            output_text += f"`Deaths      : {data['total'].get('deceased', 0)} ({delta_dec})`\n"
            output_text += f"`Recovered   : {data['total'].get('recovered', 0)} ({delta_rec})`\n"
            output_text += (
                "`Last update : "
                f"{datetime.fromisoformat(raw_data[state]['meta']['last_updated']).strftime('%A, %d. %B %Y %I:%M%p %Z')}`\n"
            )
            output_text += f"Data provided by [Covid19India.org](https://api.covid19india.org/)"

        else:
            output_text = f"Invalid State code {state}"

    elif len(args) == 2:
        district = args[1].title()
        if state in raw_data and district in raw_data[state]['districts']:
            data = raw_data[state]['districts'][district]
            delta = data.get('delta', "N/A")
            if delta == "N/A":
                delta_cnf = "N/A"
                delta_dec = "N/A"
                delta_rec = "N/A"

            else:
                delta_cnf = data['delta'].get('confirmed', 0)
                delta_dec = data['delta'].get('deceased', 0)
                delta_rec = data['delta'].get('recovered', 0)

            output_text = f"`Confirmed    : {data['total'].get('confirmed', 0)} ({delta_cnf})`\n"
            output_text += f"`Active      : {data['total'].get('confirmed', 0) - (data['total'].get('recovered', 0) + data['total'].get('deceased', 0))}`\n"
            output_text += f"`Deaths      : {data['total'].get('deceased', 0)} ({delta_dec})`\n"
            output_text += f"`Recovered   : {data['total'].get('recovered', 0)} ({delta_rec})`\n"
            output_text += (
                "`Last update : "
                f"{datetime.fromisoformat(raw_data[state]['meta']['last_updated']).strftime('%A, %d. %B %Y %I:%M%p %Z')}`\n"
            )
            output_text += f"Data provided by [Covid19India.org](https://api.covid19india.org/)"

        else:
            output_text = f"Invalid State code {state} or District {district}"

    else:
        event.edit(
            f"Malformed query [one of the reason for this error could be invalid selector __see help__]")
        return

    await event.edit(f"Corona Virus Info in {state}{', ' + district}:\n\n{output_text}")


CMD_HELP.update({"covid": ".covid <country>"
                 "\nUsage: Get an information about data covid-19 in your country.\n\n"
                 ".covidindia"
                 "\nUsage: Get an information about data covid-19 in your State/UT/District.\n"
                 "\tSpecify State/UT code and District(optional) __eg: .covidindia mp ratlam__\n"})
