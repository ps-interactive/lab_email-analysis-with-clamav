p="$http_proxy"

scheme=${p%%://*}
rest=${p#*://}

userpass=${rest%@*}
hostport=${rest#*@}

user=${userpass%%:*}    
pass=${userpass#*:}

host=${hostport%%:*}
port=${hostport#*:}

sudo tee -a /etc/clamav/freshclam.conf <<EOF
HTTPProxyServer $host
HTTPProxyPort $port
HTTPProxyUsername $user
HTTPProxyPassword $pass
EOF
