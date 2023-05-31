# NSSurge Python API Client

Python implementation of the [Surge HTTP API spec](https://manual.nssurge.com/others/http-api.html) client using `aiohttp`.

## Installation

### [pip](https://pypi.org/project/nssurge-api/)

```
$ pip install nssurge-api
```

## Usage

```python
# source: https://github.com/tddschn/nssurge-cli/blob/master/nssurge_cli/cap_commands.py
from nssurge_api import SurgeAPIClient
from nssurge_api.types import Capability
import asyncio

async def get_set_cap(
    capability: Capability, on_off: OnOffToggleEnum | None = None
) -> bool | tuple[bool, bool]:
    """
    Get or set a capability
    """
    async with SurgeAPIClient(*get_config()) as client:
        state_orig = await get_cap_state(client, capability)
        match on_off:
            case OnOffToggleEnum.on | OnOffToggleEnum.off:
                await client.set_cap(capability, s2b(on_off))
            case OnOffToggleEnum.toggle:
                await client.set_cap(capability, not state_orig)
            case _:
                return state_orig
        state_new = await get_cap_state(client, capability)
        return state_orig, state_new
```

## Develop

```
$ git clone https://github.com/tddschn/nssurge-api.git
$ cd nssurge-api
$ poetry install
```