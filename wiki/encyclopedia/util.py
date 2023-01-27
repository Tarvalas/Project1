import re

from django.core.files.base import ContentFile
from django.core.files.storage import default_storage


def list_entries():
    """
    Returns a list of all names of encyclopedia entries.
    """
    _, filenames = default_storage.listdir("entries")
    return list(sorted(re.sub(r"\.md$", "", filename)
                for filename in filenames if filename.endswith(".md")))


def save_entry(title, content, old_title = ''):
    """
    Saves an encyclopedia entry, given its title and Markdown
    content. If an existing entry with the same title already exists,
    it is replaced. If file title is being edited, the old file title is
    deleted.
    """
    print(f"old_title: {old_title}")
    if old_title:
        default_storage.delete(f"entries/{old_title}.md")
    content = content.encode('ascii')
    filename = f"entries/{title}.md"
    if default_storage.exists(filename):
        default_storage.delete(filename)
    default_storage.save(filename, ContentFile(content))


def get_entry(title):
    """
    Retrieves an encyclopedia entry by its title. If no such
    entry exists, the function returns None.
    """
    try:
        f = default_storage.open(f"entries/{title}.md")
        return f.read().decode("utf-8")
    except FileNotFoundError:
        return None

def get_similar(query):
    similar = []
    query = query.lower()
    for entry in list_entries():
        lower_entry = entry.lower()
        if query in lower_entry or lower_entry in query:
            similar.append(entry)
    
    return similar