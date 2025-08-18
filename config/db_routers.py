import random
import socket

def is_host_up(host, port=3306, timeout=2):
    try:
        socket.create_connection((host, port), timeout)
        return True
    except Exception:
        return False

class MasterSlaveRouter:
    MASTER_HOST = '10.10.40.100'    # default DB의 IP
    REPLICA_HOST = '10.10.40.150'   # replica DB의 IP

    def db_for_read(self, model, **hints):
        if is_host_up(self.REPLICA_HOST):
            print(f"[READ] {model.__name__} → replica (정상)")
            return 'replica'
        else:
            print(f"[READ] {model.__name__} → fallback to default (replica 다운)")
            return 'default'

    def db_for_write(self, model, **hints):
        if is_host_up(self.MASTER_HOST):
            print(f"[WRITE] {model.__name__} → default (정상)")
            return 'default'
        else:
            print(f"[WRITE] {model.__name__} → fallback to replica (마스터 다운)")
            return 'replica'  # ⚠️ 레플리카가 read-only면 실패할 수 있음!

    def allow_relation(self, obj1, obj2, **hints):
        return True

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        return db == 'default'
