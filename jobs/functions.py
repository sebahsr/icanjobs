def getFileName(instance, fileName):
        import random
        file_extension = fileName.rsplit(".", 1)[-1]
        return "%s_%d.%s" % (fileName, random.randint(1000, 10000000), file_extension )[0:32]
