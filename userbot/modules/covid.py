# Copyright (C) 2019 The Raphielscape Company LLC.
#
# Licensed under the Raphielscape Public License, Version 1.d (the "License");
# you may not use this file except in compliance with the License.
#
# Port to UserBot by @MoveAngel
from datetime import datetime
from covid import Covid
from userbot import CMD_HELP
from userbot.events import register
from json import loads
from urllib.request import urlopen


@register(outgoing=True, pattern="^.covid (.*)")
async def corona(event):
    await event.edit("`Processing...`")
    country = event.pattern_match.group(1)
    covid = Covid()
    country_data = covid.get_status_by_country_name(country)
    if country_data:
        output_text = f"`Confirmed   : {country_data['confirmed']}`\n"
        output_text += f"`Active      : {country_data['active']}`\n"
        output_text += f"`Deaths      : {country_data['deaths']}`\n"
        output_text += f"`Recovered   : {country_data['recovered']}`\n"
        output_text += (
            "`Last update : "
            f"{datetime.utcfromtimestamp(country_data['last_update'] // 1000).strftime('%Y-%m-%d %H:%M:%S')}`\n"
        )
        output_text += f"Data provided by [Johns Hopkins University](https://j.mp/2xf6oxF)"
    else:
        output_text = "No information yet about this country!"
    await event.edit(f"Corona Virus Info in {country}:\n\n{output_text}")


@register(outgoing=True, pattern="^.covidindia (.*)")
async def corona_india(event):
    await event.edit("`Processing...`")
    args = event.pattern_match.group(1).split(" ", 2)
    selector = args[0]
    state = args[1].upper()
    district = ""
    with urlopen("https://api.covid19india.org/v3/data.json") as url:
        raw_data = loads(url.read().decode())

    if selector == "-s":
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

    elif selector == "-r":
        district = args[2].title()
        if state in raw_data[state] and district in raw_data[state]['districts']:
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
        event.edit(f"Malformed query [one of the reason for this error could be invalid selector __see help__]")
        return

    await event.edit(f"Corona Virus Info in {state}{', ' + district}:\n\n{output_text}")


CMD_HELP.update({
    "covid":
        ".covid <country>"
        "\nUsage: Get an information about data covid-19 in your country.\n\n"
        ".covidindia <selector> <args>"
        "\nUsage: Get an information about data covid-19 in your State/UT/District.\n"
        "\t<selector>: '-s' for State/UT, '-r' for district\n"
        "\tFor State: specify State/UT code after selector __eg. -s mp__\n"
        "\tFor Disrtict: specify State/UT code and District name after selector __eg. -s dl new delhi__\n"
})
