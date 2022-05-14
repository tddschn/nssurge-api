#!/usr/bin/env python3

from typing import Literal


Capability = Literal['mitm', 'capture', 'rewrite', 'scripting', 'system_proxy', 'enhanced_mode']
OutboundMode = Literal['direct', 'proxy', 'rule']
Policy = str
PolicyGroup = str