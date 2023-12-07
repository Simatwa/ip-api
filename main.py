#!/usr/bin/python
__program__ = "ip-api"
__version__ = "1.0"
__author__ = "Simatwa"

import requests
import click
import json
import logging

trace_me_url = "http://ip-api.com/"
trace_ip_url = "http://ip-api.com/batch"

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
    # print(
    #   f"""
    #        {__program__} : v{__version__}
    #  By : {__author__}


# Repo : https://github.com/Simatwa/ip-api
# """
#       )


class Handler:
    @staticmethod
    def exception_handler(exit_on_error=False):
        def decorator(func):
            def main(*args, **kwargs):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    logging.exception(e)
                    logging.error(e.args[1] if len(e.args) > 1 else str(e))
                    if exit_on_error:
                        exit(1)

            return main

        return decorator


@Handler.exception_handler(exit_on_error=True)
@trace.command("me")
@click.option(
    "-f",
    "--fields",
    multiple=True,
    help="Restrict display to only this fields",
    type=click.Choice(
        [
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
        ]
    ),
    default=[
        "status",
        "country",
        "countryCode",
        "regionName",
        "city",
        "lat",
        "lon",
        "timezone",
        "isp",
        "mobile",
    ],
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
    help="Response packing format",
    type=click.Choice(["csv", "xml", "json"]),
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
        trace_me_url + format,
        timeout=timeout,
        params={"fields": ",".join(fields), "lang": language},
    )
    if resp.ok:
        if (
            format == "json"
            and resp.headers.get("content-type") == "application/json; charset=utf-8"
        ):
            print(json.dumps(resp.json(), indent=indent))
        else:
            print(resp.text)
    else:
        print(resp.text)


@Handler.exception_handler(exit_on_error=True)
@trace.command(
    "ip",
)
@click.argument(
    "query",
)  # prompt='Enter IP address to be traced',)help='IP Address to be traced',)
@click.option(
    "-f",
    "--fields",
    multiple=True,
    help="Restrict display to only this fields",
    type=click.Choice(
        [
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
        ]
    ),
    default=[
        "status",
        "country",
        "countryCode",
        "regionName",
        "city",
        "lat",
        "lon",
        "timezone",
        "isp",
        "mobile",
    ],
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
    help="Response packing format",
    type=click.Choice(["csv", "xml", "json"]),
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
    resp = request_session.post(
        trace_ip_url + format,
        timeout=timeout,
        data={"query": query, "fields": ",".join(fields), "lang": language},
    )
    if resp.ok:
        if (
            format == "json"
            and resp.headers.get("content-type") == "application/json; charset=utf-8"
        ):
            print(json.dumps(resp.json(), indent=indent))
        else:
            print(resp.text)
    else:
        print(resp.text)


if __name__ == "__main__":
    trace()
