from PyQt5.QtCore import QXmlStreamWriter, QFile, QIODevice
import xml.etree.ElementTree as ET
class Cached():
    def __init__(self, cache_file, cache_size=1000):
        super().__init__()
        self.cache_size = cache_size
        self.cache_file = cache_file
        self.load_cache_from_file()

    def get(self, key):
        key = str(key)
        if key in self.cache:
            print("cache")
            return self.cache[key]
        if len(self.cache) >= self.cache_size:
            self.cache.popitem()

        return ""

    def set(self, key, value):
        key = str(key)
        value = str(value)
        if key in self.cache:
            return
        if len(self.cache) >= self.cache_size:
            self.cache.popitem()
        self.cache[key] = value

    def load_cache_from_file(self):
        try:
            tree = ET.parse(self.cache_file)
            root = tree.getroot()
            self.cache = {}
            for item in root.findall('item'):
                key = item.get('key')
                value = item.text
                self.cache[key] = value
        except:
            self.cache = {}
    def save_cache_to_file(self):
        try:
            file = QFile(self.cache_file)
            if file.open(QIODevice.WriteOnly):
                writer = QXmlStreamWriter(file)
                writer.setAutoFormatting(True)
                writer.writeStartDocument()
                writer.writeStartElement("cache")
                for key, value in self.cache.items():
                    writer.writeStartElement("item")
                    writer.writeAttribute("key", str(key))
                    writer.writeCharacters(str(value))
                    writer.writeEndElement()
                writer.writeEndElement()
                writer.writeEndDocument()
                file.close()
            else:
                print("Error opening file for writing.")
        except:
            pass