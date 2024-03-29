# auto upgrade service

## 操作方式

服务启动

```shell
sudo cp /home/nvidia/workspace/aibox-pro2-upgrade/auto_upgrade.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable auto_upgrade
sudo systemctl start auto_upgrade

sudo systemctl status auto_upgrade
# 查看状态，当看到active (running) 代表服务启动成功
```

