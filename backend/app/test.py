from pathlib import Path

# تخيل عندي list من ملفات زي دي:
files = [
    Path("003_update_orders.sql"),
    Path("001_init.sql"),
    Path("002_add_users.sql"),
]

# ----------------------------
# 1) نشوف القائمة الأصلية
print("Original list:")
for f in files:
    print(f)  
# هتطبع زي ما هي بدون ترتيب

# ----------------------------
# 2) نرتبهم بدون key
print("\nSorted normally (alphabetical by full path):")
for f in sorted(files):
    print(f)

# ----------------------------
# 3) نرتبهم بالـ key=lambda x: x.name
print("\nSorted by file name only:")
for f in sorted(files, key=lambda x: x.name):
    print(f)

# ----------------------------
# 4) نشرح يعني إيه بيحصل جوه lambda
print("\nValues that lambda returns for sorting:")
for f in files:
    print(f"{f} -> {f.name}")  # ده اللي lambda بيرجعه
