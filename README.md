# Python: Nightscout API client

Simple asynchronous Python client for Nightscout API

## About
This library allows to fetch glucose data from the [nightscout api](https://github.com/nightscout/cgm-remote-monitor/wiki/API-v1.0.0-beta-Endpoints)

## How to use

```python
import asyncio

from nightscout import NS


async def main(loop):
    async with NS("cgmtest.herokuapp.com", loop=loop) as cgm:
        info = await cgm.update()
        print(info)


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main(loop))
```