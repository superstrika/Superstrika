# Startup console

1. Move `superstrika.service` to `/etc/systemd/system/`:
```bash
cp superstrika.service /etc/systemd/system/superstrika.service
```

2. Reload Services:
```bash
sudo systemctl daemon-reload
```

3. Enable the Service:
```bash
sudo systemctl enable superstrika.service
```

4. Start the Service:
```bash
sudo systemctl start superstrika.service
```

