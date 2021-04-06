import backtrader

# Create a Strategy
class TestStrategy(backtrader.Strategy):

    def log(self, txt, dt=None):
        dt = dt or self.datas[0].datetime.date(0)
        print('%s. %s' % (dt.isoformat(), txt)) 

    def __init__(self):
        # Keep Reference to the "close" line in the data[0] dataseries 
        self.dataclose = self.datas[0].close
        self.order = None
    
    def notify_order(self, order):
        if order.status in [order.Submitted, order. Accepted]:
            return
        
        if order.status in [order.Completed]:
            if order.isbuy():
                self.log('BUY EXECUTED {}'.format(order.executed.price))
            elif order.issell():
                self.log('SELL EXECUTED {}'.format(order.executed.price))

            self.bar_executed = len(self)        
        self.order = None

    def next(self):
        # Simply log the closing price of the series from the reference 
        self.log('Close, %.2f' % self.dataclose[0])

        if self.order:
            return 

        if not self.position:    
            if self.dataclose[0] < self.dataclose[-1]:
                # Current Close less than previous close 

                if self.dataclose[-1] < self.dataclose[-2]:
                    #Previous Close less than the previous close 

                    #BUY 
                    self.log('BUY Create, %.2f' % self.dataclose[0])
                    self.buy(size=0.01)
        else:
            if len(self) >= (self.bar_executed + 5):
                self.log('SELL CREATED {}'.format(self.dataclose[0]))
                self.order = self.sell(size=0.01)