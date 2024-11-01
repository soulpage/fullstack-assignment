import hashlib

def calculate_checksum(file_obj):
    hash = hashlib.sha1()
    file_obj.seek(0)
    if file_obj.multiple_chunks():
        for chunk in file_obj.chunks():
            hash.update(chunk)
    else:
        hash.update(file_obj.read())
    file_obj.seek(0)
    return hash.hexdigest()