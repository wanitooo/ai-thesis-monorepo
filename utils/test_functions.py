def read_scp(scp_file):
    '''
      read the scp file
    '''
    files = open(scp_file, 'r')
    lines = files.readlines()
    wave = {}
    for line in lines:
        line = line.split()
        if line[0] in wave.keys():
            raise ValueError
        wave[line[0]] = line[1]
    return wave
