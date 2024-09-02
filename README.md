# IOU Bot

Telegram bot frontend for IOU app

## How to set up

### Create Telegram bot

1. In Telegram, open `@botfather`
2. Create a new bot
3. Get API key


## How to run

```bash
python -m app.main
```


### Development

Pre-commit hooks:

```bash
$ poetry run pre-commit run --all-files
```

## TODO

MVP:

- [ ] Add more tests
- [x] Add CI/CD
- [ ] Add logging, especially for error cases
- [ ] Add lookup of members in chat

More features:

- [ ] Validate that users in a query are indeed in the conversation
