# Configuration
| var | default | meaning |
|---|---|---|
| ENABLE_CACHE | **true** | response cache; on by default since v3.1 |
| BACKEND_URL | - | upstream |

Caching has been enabled by default since v3.1, so repeated reads are served
from memory.
