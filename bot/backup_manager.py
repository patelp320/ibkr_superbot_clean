import tarfile, datetime, os

today = datetime.date.today().isoformat()
backup_file = f"backups/backup_{today}.tar.gz"

with tarfile.open(backup_file, "w:gz") as tar:
    for folder in ["logs", "local_cache"]:
        if os.path.exists(folder):
            tar.add(folder, arcname=os.path.basename(folder))

print(f"✅ Backup created ➜ {backup_file}")
