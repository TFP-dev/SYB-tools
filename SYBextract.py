import sys, getopt, os.path

def extract_syb(inputfile, outputdir):
    print(
    '''
    #######################################
    #                                     #
    #                                     #
    #           SYBextract tool           #
    #                                     #
    #                           by TFPdev #
    #######################################
    '''
    )

    print('Opening input file "' + inputfile + '"...')

    ifile= open(inputfile, "rb")

    ifile_header= ifile.read(4)
    
    if ifile_header != b'\x56\x58\x42\x47':
        print('Input file "' + inputfile + '" is not supported archive type or is damaged!')
        ifile.close()
        sys.exit()

    list_length= int.from_bytes(ifile.read(4), byteorder='little', signed=True)

    cache_filename= b''
    cache_length= b''
    cache_length_iterator= 0
    cache_mode= 1

    files= []

    iterator = 0
    while iterator < list_length:
        iterator += 1
        byte = ifile.read(1)
        if cache_mode == 1:
            if byte != b'\x00':
                cache_filename= cache_filename + byte
            else:
                cache_mode= 2
                files.append([cache_filename, 0])
                cache_filename= b''
        elif cache_mode == 2:
            cache_length_iterator = cache_length_iterator + 1
            cache_length = cache_length + byte
            if cache_length_iterator == 4:
                cache_mode= 1
                files[len(files)-1][1]= int.from_bytes(cache_length, byteorder='little', signed=True)
                cache_length= b''
                cache_length_iterator= 0
    
    for file in files:
        filename= file[0].decode()
        print('Extracting file "' + filename + '"...')
        unpacked_data= ifile.read(file[1])
        unpacked_file= open(os.path.join(outputdir, filename), "wb")
        
        unpacked_file.write(bytearray(unpacked_data))
        unpacked_file.close()

    print('Successfully extracted ' + str(len(files)) + ' files to "' + outputdir + '"')

    ifile.close()
    return

def main(argv):
    inputfile = ''
    outputdir = ''
    try:
        opts, args = getopt.getopt(argv,"hi:o:",["ifile=","odir="])
    except getopt.GetoptError:
        print('SYBextract.py -i <inputfile> -o <outputdir>')
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print('SYBextract.py -i <inputfile> -o <outputdir>')
            sys.exit()
        elif opt in ("-i", "--ifile"):
            inputfile = arg
        elif opt in ("-o", "--odir"):
            outputdir = arg
    if (os.path.exists(inputfile) and os.path.isfile(inputfile)):
        if os.path.exists(outputdir):
            if os.path.isdir(outputdir):
                extract_syb(inputfile, outputdir)
            else:
                print('"' + outputdir + '" is not directory!')
        else:
            print('Creating output directory "' + outputdir + '"...')
            os.mkdir(outputdir)
            extract_syb(inputfile, outputdir)
    else:
        print('Input file "', inputfile, '" does not exists!')
        sys.exit()
    return;

if __name__ == "__main__":
   main(sys.argv[1:])