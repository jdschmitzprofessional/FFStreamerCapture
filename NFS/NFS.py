import libnfs

class NFS:
    def __init__(self, source=str, name=str, config=dict, ramdisk=str):
        self.source = source
        self.name = name
        self.config=config
        self.ramdisk = ramdisk
    def createExport(self):
        with open("/etc/exports",'r') as infile:
            exportString =
            if self.name not in str(infile.read()):
