#!/usr/bin/env python3

from typing import Literal
import sys

# https://peps.python.org/pep-0655/#usage-in-python-3-11
# if python version >= (3, 11):
if sys.version_info >= (3, 11):
    from typing import TypedDict, NotRequired
else:
    from typing_extensions import TypedDict, NotRequired

Capability = Literal['mitm', 'capture', 'rewrite', 'scripting', 'system_proxy',
                     'enhanced_mode']
OutboundMode = Literal['direct', 'proxy', 'rule']
Policy = str
PolicyGroup = str
RequestsType = Literal['recent', 'active']
Profile = str
Module = str
Enabled = bool
Script = str
LogLevel = Literal['verbose', 'info', 'notify', 'warning']

SetModuleStateRequest = dict[Module, Enabled]


# https://peps.python.org/pep-0589/
class EvalScriptMockRequest(TypedDict):
    """
    {
    "script_text": "The content of JS script",
    "mock_type": "cron",
    "timeout": 5
    }
    """
    script_text: str
    mock_type: str
    timeout: int


class EvalCronScriptRequest(TypedDict):
    script_name: Script


class ChangeDeviceRequest(TypedDict):
    """
    {
    "physicalAddress":"F0:9F:C2:00:00:00", (required)
    "name": "Computer",
    "address": "192.168.1.200",
    "shouldHandledBySurge": true
    }
    """
    physicalAddress: str
    name: NotRequired[str]
    address: NotRequired[str]
    shouldHandledBySurge: NotRequired[bool]
