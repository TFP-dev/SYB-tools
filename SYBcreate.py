import sys, getopt, os.path

def create_syb(inputdir, outputfile, file_list):
    print(
    '''
    #######################################
    #                                     #
    #                                     #
    #            SYBcreate tool           #
    #                                     #
    #                           by TFPdev #
    #######################################
    '''
    )

    print('Creating file "' + outputfile + '" from directory "' + inputdir + '"...')
    
    syb_header= b'\x56\x58\x42\x47'
    syb_file_list= b''
    syb_file_data= b''

    for file in file_list:
        print('Adding file "' + file + '"...')
        syb_file_list += bytes(file, "ascii")
        input_file= open(os.path.join(inputdir, file), "rb")
        file_data= input_file.read()
        syb_file_data += file_data
        syb_file_list += b'\x00'
        syb_file_list += len(file_data).to_bytes(4, "little")
        input_file.close()

    syb_file_list_length= len(syb_file_list).to_bytes(4, "little")

    print('Writing file "' + outputfile + '"...')

    output_file= open(outputfile, "wb")

    output_file.write(syb_header + syb_file_list_length + syb_file_list)
    output_file.write(syb_file_data)

    output_file.close()

    print('Successfully created file "' + outputfile + '"!')
    
    return

def main(argv):
    inputdir = ''
    outputfile = ''
    try:
        opts, args = getopt.getopt(argv,"hi:o:",["idir=","ofile="])
    except getopt.GetoptError:
        print('SYBcreate.py -i <inputdir> -o <outputfile>')
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print('SYBcreate.py -i <inputdir> -o <outputfile>')
            sys.exit()
        elif opt in ("-i", "--idir"):
            inputdir = arg
        elif opt in ("-o", "--ofile"):
            outputfile = arg
    if (os.path.exists(inputdir) and os.path.isdir(inputdir)):
        file_list = [f for f in os.listdir(inputdir) if os.path.isfile(os.path.join(inputdir, f))]
        if len(file_list) > 0:
            create_syb(inputdir, outputfile, file_list)
        else:
            print('Input directory "' + inputdir + '" has no files!')
            sys.exit()
    else:
        print('Input directory "' + inputdir + '" does not exists!')
        sys.exit()
    return;

if __name__ == "__main__":
   main(sys.argv[1:])