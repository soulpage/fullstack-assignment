from yourapp.models import UploadedFile

def is_duplicate_file(filename):
    """
    Check if a file with the given filename already exists in the database.

    Args:
        filename (str): Name of the file to check.

    Returns:
        bool: True if a file with the same name exists, False otherwise.
    """
    return UploadedFile.objects.filter(filename=filename).exists()