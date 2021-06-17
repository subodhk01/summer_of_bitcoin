INPUT_CSV = 'mempool.csv'
OUTPUT_TXT = 'block.txt'
MAX_BLOCK_WEIGHT = 4000000

class Transaction():
    def __init__(self, txid, fee, weight, parents):
        self.txid = txid
        self.fee = int(fee)
        self.weight = int(weight)

        tempParents = []
        for parent in parents:
            if parent:
                tempParents.append(parent)
        self.parents = tempParents

def addTransaction(csv_line):
    return Transaction(csv_line[0], csv_line[1], csv_line[2], csv_line[3].split(";"))

def parseAndLoadCSV(filename):
    """Parse the CSV file and return a list of MempoolTransactions."""
    with open(filename) as f:
        txs = {}
        for line in f.readlines():
            tx = addTransaction(line.strip().split(','))
            txs[tx.txid] = tx
        return txs

def exportOutput(output, filename):
    """To export the code output to a txt file"""
    file = open(filename, "w")
    with file as f:
        for i in output:
            f.write("%s\n" % i)


def isTransactionValid(trx, includedTransactions):
    """To check if all the parents the the current transactions are already completed or not"""
    for parent in trx.parents:
        if not (parent in includedTransactions):
            return False
    return True

def main():
    # init
    txs = parseAndLoadCSV(INPUT_CSV)

    transactionSet = list()
    includedTransactions = set()
    output = []
    blockWeight = 0
    totalFee = 0

    
    for txid in txs:
      
        transactionSet.append([ (txs[txid].fee/txs[txid].weight), txs[txid].txid ,txs[txid] ])
    transactionSet.sort(reverse=True)


    while len(transactionSet) :
        found = False
        for i in range(len(transactionSet)):
            currentTransaction = transactionSet[i][2]
            fee = currentTransaction.fee
            weight = currentTransaction.weight

            if isTransactionValid(currentTransaction, includedTransactions) and blockWeight + weight <= MAX_BLOCK_WEIGHT:
                blockWeight += weight
                includedTransactions.add(currentTransaction.txid)
                output.append(currentTransaction.txid)
                totalFee += fee
                del transactionSet[i]
                found = True
                break
        if not found:
            break
    
    print("Block details:")
    print("{} transactions".format(len(includedTransactions)))
    print("Total Fee: ", totalFee)
    print("Total Weight: ", blockWeight)
    exportOutput(output, OUTPUT_TXT)

main()