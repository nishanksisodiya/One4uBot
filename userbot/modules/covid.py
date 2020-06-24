# Copyright (C) 2019 The Raphielscape Company LLC.
#
# Licensed under the Raphielscape Public License, Version 1.d (the "License");
# you may not use this file except in compliance with the License.
#
# Port to UserBot by @MoveAngel
from json import load
from datetime import datetime
from covid import Covid
from userbot import CMD_HELP
from userbot.events import register


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


@register(outgoing=True, pattern="^.covidindia (.*) (.*)")
async def corona(event):
    await event.edit("`Processing...`")
    selector = event.pattern_match.group(1)
    region = event.pattern_match.group(2)
    with open('https://api.covid19india.org/v3/data.json') as f:
        raw_data = load(f)

    if selector == "-s":
        region = region.upper()
        output_text = f"`Confirmed    : {raw_data[region]['total'].get('confirmed', 0)} ({ raw_data[region]['delta'].get('confirmed', 0) })`\n"
        output_text += f"`Active      : {raw_data[region]['total'].get('confirmed', 0) - ( raw_data[region]['total'].get('recovered', 0) + raw_data[region]['total'].get('deceased', 0) )}`\n"
        output_text += f"`Deaths      : {raw_data[region]['total'].get('deceased', 0)} ({raw_data[region]['delta'].get('deceased', 0)})`\n"
        output_text += f"`Recovered   : {raw_data[region]['total'].get('recovered', 0)} ({raw_data[region]['delta'].get('recovered', 0)})`\n"
        output_text += (
            "`Last update : "
            f"{datetime.fromisoformat(raw_data['meta']['last_update']).strftime('%A, %d. %B %Y %I:%M%p %Z')}`\n"
        )
        output_text += f"Data provided by [Covid19India.org](https://api.covid19india.org/)"

    else:
        output_text = "No information yet about this country!"

    await event.edit(f"Corona Virus Info in {region}:\n\n{output_text}")


CMD_HELP.update({
    "covid":
        ".covid <country>"
        "\nUsage: Get an information about data covid-19 in your country.\n"
})
