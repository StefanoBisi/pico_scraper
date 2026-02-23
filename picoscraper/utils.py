def fix_filename(filename):
        return filename.lower()\
            .replace(' ', '_')\
            .replace('(', '_')\
            .replace(')', '_')\
            .replace('\'', '_')\
            .replace('!', '_')\
            .replace('.', '_')\
            .replace('!', '_')\
            .replace('-', '_')\
            .replace('<', '_')\
            .replace('>', '_')\
            .replace('&', '_')
