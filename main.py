#!/usr/bin/python
__program__ = "ip-api"
__version__ = "1.0"
__author__ = "Simatwa"

import requests
import click
import json
import logging

logging.basicConfig(
    format="%(asctime)s : %(levelname)s - %(message)s [%(funcName)s : %(lineno)d]",
    datefmt="%H:%M:%S",
    level=logging.INFO,
)
trace_me_url = "http://ip-api.com/"
trace_ip_url = "http://ip-api.com/%(format)s/%(query)s"

request_session = requests.Session()
request_session.headers = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
    "Accept-Encoding": "gzip, deflate",
    "Accept-Language": "en-US,en;q=0.5",
    "Connection": "keep-alive",
    "Upgrade-Insecure-Requests": "1",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv",
}


@click.group()
def trace():
    """Get to know IP information"""
    print(
        f"""
              {__program__}  v{__version__}
        Author : {__author__}

    Repo : https://github.com/Simatwa/ip-api
 """
    )


all_fields = [
    "query",
    "status",
    "message",
    "continent",
    "continentCode",
    "country",
    "countryCode",
    "region",
    "regionName",
    "city",
    "district",
    "zip",
    "lat",
    "lon",
    "timezone",
    "offset",
    "currency",
    "isp",
    "as",
    "asname",
    "mobile",
    "proxy",
    "hosting",
    "org",
]

default_fields = [
    "query",
    "status",
    "country",
    "countryCode",
    "region",
    "regionName",
    "city",
    "zip",
    "lat",
    "lon",
    "timezone",
    "isp",
    "org",
    "as",
]

tabulate_formats = [
    "simple",
    "fancy_grid",
    "grid",
    "pretty",
    "html",
    "secure_html",
    "orgtbl",
    "plain",
    "github",
]


@trace.command("me")
@click.option(
    "-f",
    "--fields",
    multiple=True,
    help="Restrict response to only this fields",
    type=click.Choice(all_fields),
    default=default_fields,
)
@click.option(
    "-l",
    "--language",
    type=click.Choice(["ru", "en", "de", "es", "pt-BR", "fr", "ja", "zh-CN"]),
    default="en",
    help="Return response in this language",
)
@click.option(
    "-F",
    "--format",
    help="Response display format",
    type=click.Choice(["csv", "xml", "json"] + tabulate_formats),
    default="json",
)
@click.option(
    "-t",
    "--timeout",
    help="Terminate if request takes more than this time (s)",
    default=30,
    type=click.INT,
)
@click.option(
    "-i",
    "--indent",
    help="Json dumping indentation level",
    type=click.INT,
    default=5,
)
def trace_me(fields, language, format, timeout, indent):
    """Trace your own IP address"""
    resp = request_session.get(
        trace_me_url + (format if format in ("xml", "csv") else "json"),
        timeout=timeout,
        params={"fields": ",".join(fields), "lang": language},
    )
    display_response(resp, format, indent)


@trace.command(
    "ip",
)
@click.option(
    "-q",
    "--query",
    help="IP address to be traced",
    prompt="Enter IP address",
    required=True,
)
@click.option(
    "-f",
    "--fields",
    multiple=True,
    help="Restrict response to only this fields",
    type=click.Choice(all_fields),
    default=default_fields,
)
@click.option(
    "-l",
    "--language",
    type=click.Choice(["ru", "en", "de", "es", "pt-BR", "fr", "ja", "zh-CN"]),
    default="en",
    help="Return response in this language",
)
@click.option(
    "-F",
    "--format",
    help="Response display format",
    type=click.Choice(["csv", "xml", "json"] + tabulate_formats),
    default="json",
)
@click.option(
    "-t",
    "--timeout",
    help="Terminate if request takes more than this time (s)",
    default=30,
    type=click.INT,
)
@click.option(
    "-i",
    "--indent",
    help="Json dumping indentation level",
    type=click.INT,
    default=5,
)
def trace_ip(query, fields, language, format, timeout, indent):
    """Trace other IP address"""
    resp = request_session.get(
        trace_ip_url
        % ({"format": format if format in ("xml", "csv") else "json", "query": query}),
        timeout=timeout,
        params={"fields": ",".join(fields), "lang": language},
    )
    display_response(resp, format, indent)


def display_response(resp, format, indent):
    if resp.ok:
        if (
            format == "json"
            or format not in ("xml", "csv")
            and resp.headers.get("content-type") == "application/json; charset=utf-8"
        ):
            if format in tabulate_formats:
                from tabulate import tabulate

                data = []
                for key, value in resp.json().items():
                    data.append([key, str(value)])

                print(tabulate(data, tablefmt=format))
            else:
                print(json.dumps(resp.json(), indent=indent))
        else:
            print(resp.text)
    else:
        print(resp.text)


if __name__ == "__main__":
    try:
        trace()
    except Exception as e:
        logging.error(e.args[1] if len(e.args) > 1 else e)
        logging.exception(e)
