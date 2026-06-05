# Simple WebSockets Server

Primarily intended for usage with the QField `livefield` plugin.

## Testing

Run three terminal instances.

Terminal 1:

```bash
docker run --rm -it -p 8001:8001 --entrypoint=bash ghcr.io/nirvn/ws:main
python app.py
```

Terminal 2:

```bash
npm install -g wscat
wscat -c ws://localhost:8001/
{"type":"create","user":"Alice"}
# Received: {"type": "created", "group": "_1jg4Jt2MWhYmu59", "device": "fj2C0nlpJUuGbA8R"}
{"type":"position","lat":-5.1477,"lon":119.4327,"dir":90,"speed":12}
# Received: {"type": "positions", "devices": {"fj2C0nlpJUuGbA8R": {"user_name": "Alice", "user_color": "#e41a1c", "lat": -5.1477, "lon": 119.4327, "dir": 90, "speed": 12}}}
{"type":"message","content":"hello from Alice"}
# Received: {"type": "message", "device": "fj2C0nlpJUuGbA8R", "content": "hello from Alice"}
```

Terminal 3:

``bash
npm install -g wscat
wscat -c ws://localhost:8001/
{"type":"join","user":"Bob","group":"_1jg4Jt2MWhYmu59"}
# Received: {"type": "joined", "group": "_1jg4Jt2MWhYmu59", "device": "45Nwt5r7nOxgxctH"}
{"type":"position","lat":-5.15,"lon":119.43,"dir":180,"speed":5}
# Position is broadcast in both terminals
# {"type": "positions", "devices": {"fj2C0nlpJUuGbA8R": {"user_name": "Alice", "user_color": "#e41a1c", "lat": -5.1477, "lon": 119.4327, "dir": 90, "speed": 12}, "45Nwt5r7nOxgxctH": {"user_name": "Bob", "user_color": "#4daf4a", "lat": -5.15, "lon": 119.43, "dir": 180, "speed": 5}}}
```
