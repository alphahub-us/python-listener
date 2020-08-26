# AlphaHub Signal Listener example

Use this Python project to listen for new AlphaHub signals in real-time.

## Requirements

- Python 3.6+, with the `websockets` and `requests` packages
- At least one AlphaHub subscription

## Instructions

1. Edit `creds.py` to replace the placeholder strings with your AlphaHub email and password.
2. Edit `__main__.py` and enter the IDs for your subscribed algorithms into the `IDs` variable (line 11).
3. Run the following command to start listening:

```
python ../alphahub_listener
```

4. Type `Ctrl+C` to exit the program.
