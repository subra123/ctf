import base64

with open('secret_message.txt', 'rb') as f:
    data = f.read().strip()

count = 0
while True:
    try:
        # Check if current data is base64-like
        if not all(c in b"ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/=\n\r " for c in data):
            break
        new_data = base64.b64decode(data)
        data = new_data
        count += 1
    except Exception:
        break

print(f"Decoded {count} times.")
print(f"Length of final data: {len(data)}")
print("Final data (repr):")
print(repr(data[:1000]))
