# IOU Bot

Telegram bot frontend for IOU app

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
