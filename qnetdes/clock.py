import inspect

__all__ = ["MasterClock"]

class MasterClock:
    def __init__(self):
        self.transactions = []
        self.time = 0

    def record_transaction(self, time, event_type, source, target, qubits):
        '''
        Update master clock and record transaction

        :param Float time: current time in sends
        :param String event_type: either sent or received. Otherwise, through exception
        :param String source: name of the agent sending qubits
        :param String target: name of the agent receiving qubits
        :param List<Integer> qubits: list of qubits being sent from source to target
        '''
        # Update master clock
        self.time = max(self.time, time)

        # Record Event
        if event_type == 'sent':
            transaction = 'Qubits {} sent from {} to {} at {}'.format(qubits, source, target, time)
        elif event_type == 'received':
            transaction = 'Qubits {} received by {} from {} at {}'.format(qubits, target, source, time)
        else: 
            raise Exception('Event type must be "sent" or "received"') 

        self.transactions.append(transaction)

    def get_time(self):
        '''
        Return master time
        '''
        return self.time
    
    def recent_transaction(self):
        '''
        Print the most recent transaction
        '''
        print(self.transactions[-1])

    def display_transactions(self): 
        '''
        Prints all transactions
        '''
        for transaction in self.transactions: 
            print(transaction)