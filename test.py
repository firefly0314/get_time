import tomllib

with open('mein_setting.toml', 'rb') as f:
    settings = tomllib.load(f)
print(settings)