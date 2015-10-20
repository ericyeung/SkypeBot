def tryReading(fileName):
    try:
        f = open(fileName, 'r')
    except:
        f = open(fileName, 'w+')
    return f