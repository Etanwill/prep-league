


class InMemoryDB:
    def __init__(self):
        self.data = {}
        self.backups = []
        
    def set(self, key, field, val):
        if key not in self.data:
            self.data[key] = {}
        self.data[key][field] = val

    def get(self, key, field):
        if key in self.data and field in self.data[key]:
            return self.data[key][field]
        return None

    def delete(self, key, field):
        if key in self.data and field in self.data[key]:
            del self.data[key][field]
            return True
        return False

    def scan(self, key):
        if key not in self.data:
            return []
        res = [[field, val] for field, val in self.data[key].items()] 
        res.sort()
        output = [field + "(" + str(val) + ")"  for field, val in res]
        return output

    def scan_by_prefix(self, key, prefix):
        size = len(prefix)
        res = [field + "(" + str(val) + ")" for  field, val in self.data[key].items() if field[:size] == prefix]
        return res

    def set_at(self, key, field, value, timestamp):
        if key not in self.data:
            self.data[key] = {}
        if field not in self.data[key]:
            self.data[key][field] = []
        self.data[key][field].append(( value, timestamp))
    
    def set_at_with_ttl(self, key, field, value, timestamp, ttl):
        if key not in self.data:
                self.data[key] = {}
        if field not in self.data[key]:
                self.data[key][field] = []
        self.data[key][field].append((value, timestamp, ttl))

    def get_at(self, key, field, ts):
        if key not in self.data or field not in self.data[key]:
            return None
        record = self.data[key][field][-1]
        value = record[0]
        set_ts = record[1]

        if ts < set_ts:
            return None
        if len(record) == 2:
            return value    

        ttl = record[2]
        if ts < set_ts + ttl:
            return value
        return None

    def delete_at(self, key, field, ts):
        if key not in self.data or field not in self.data[key]:
            return False
        value = self.get_at(key, field, ts)
        if value:
            del self.data[key][field]
            return True
        return False

    def scan_at(self, key, ts):
        if key not in self.data:
            return []
        res = []
        for field, record in self.data[key].items():
            value = self.get_at(key, field, ts)
            if value:
                res.append(f"{field}({value})")
        return sorted(res)

    def scan_by_prefix_at(self, key, prefix, ts):
        if key not in self.data:
            return []
        res = []
        for field, record in self.data[key].items():
            if field.startwith(prefix):
                value = self.get_at(key, field, ts)
                if value:
                    res.append(f"{field}({value})")

    def backup(self, ts):
        backup_data = {}
        count = 0
        for key, fields in self.data.items():
            backup_data[key] = {}
            for field, records in fields.items():
                value = self.get_at(key, field, ts)
                if value is not None:
                    record = records[-1]
                    if len(record) == 2:
                        backup_data[key][field] = (value, None)
                    else:
                        set_ts = record[1]
                        ttl = record[2]
                        expiry = set_ts + ttl
                        remaining_ttl = expiry - ts

                        backup_data[key][field] = (value, remaining_ttl)
            if backup_data[key]:
                count += 1
            else:
                del backup_data[key]
        self.backups.append((ts, backup_data))
        return count

    
def restore(self, ts, timestamp_to_restore):
    latest_backup = None
    latest_backup_ts = float("-inf")

    for backup_ts, backup_data in self.backups:
        if backup_ts <= timestamp_to_restore and backup_ts > latest_backup_ts:
            latest_backup = backup_data
            latest_backup_ts = backup_ts

    if latest_backup is None:
        return

    restored_data = {}

    for key, fields in latest_backup.items():
        restored_data[key] = {}

        for field, (value, remaining_ttl) in fields.items():
            if remaining_ttl is None:
                restored_data[key][field] = [(value, ts)]
            else:
                restored_data[key][field] = [(value, ts, remaining_ttl)]


    self.data = restored_data



        
        