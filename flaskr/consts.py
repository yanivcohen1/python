class consts:
    def PI(): return 3.14 # pylint: disable=no-method-argument
    def NAME(): return "yan" # pylint: disable=no-method-argument

print("PI:", consts.PI(),
      ", my name:", consts.NAME())
