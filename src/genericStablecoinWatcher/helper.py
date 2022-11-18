import brownie

# Classes
class Erc20Token:
    """
    Controls what comprises a token, noteably:
    - Name
    - Decimal
    - Symbol
    - Address
    """
    def __init__(self, contractAddress=""):
        contract = brownie.Contract.from_explorer(contractAddress)
        self.symbol = contract.symbol()
        self.decimals = contract.decimals()
        self.address = contract.address

        