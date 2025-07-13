import pickle

# write list to binary file
def write_list(a_list, filename):
    # store list in binary file so 'wb' mode
    with open(filename, 'wb') as fp:
        pickle.dump(a_list, fp)

# Read list to memory
def read_list(fileName):
    # for reading also binary mode is important
    with open(fileName, 'rb') as fp:
        n_list = pickle.load(fp)
        return n_list