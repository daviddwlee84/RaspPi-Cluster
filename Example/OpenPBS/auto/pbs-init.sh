#!/usr/bin/env sh
set -euo pipefail

echo "[pbs-init] waiting for pbs server..."

# 等 qmgr 能連上 server
for i in {1..60}; do
    if qmgr -c "list server" >/dev/null 2>&1; then
        break
    fi
    sleep 1
done

echo "[pbs-init] configuring nodes..."

# idempotent：避免重跑失敗
ensure_node () {
    local n="$1"
    if ! qmgr -c "list node ${n}" >/dev/null 2>&1; then
        qmgr -c "create node ${n}"
    fi
    # 掛到 workq（最簡 MVP）
    qmgr -c "set node ${n} queue=workq" || true
}

ensure_node pbs-c1
ensure_node pbs-c2

echo "[pbs-init] done."