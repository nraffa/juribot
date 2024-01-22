import tempfile


def tmpFileCreator(file):
    with tempfile.NamedTemporaryFile(delete=False) as tmp:
        tmp.write(file.getvalue())
        tmpFileName = tmp.name
    return tmpFileName
