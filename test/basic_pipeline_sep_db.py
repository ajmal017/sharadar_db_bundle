import pandas as pd
from zipline.pipeline import Pipeline
from zipline.pipeline.data import USEquityPricing

from sharadar.pipeline.engine import load_sharadar_bundle, symbols, make_pipeline_engine
from zipline.pipeline.filters import StaticAssets
import time
import datetime

bundle = load_sharadar_bundle()

bundle.asset_finder.retrieve_equities([199059, 199623])
print(symbols(['SPY']))

spe = make_pipeline_engine()

pipe_start = pd.to_datetime('2020-02-03', utc=True)
pipe_end = pd.to_datetime('2020-02-07', utc=True)


pipe = Pipeline(columns={
    'Close': USEquityPricing.close.latest,
},
screen = StaticAssets(symbols(['IBM', 'F', 'AAPL']))
)

stocks = spe.run_pipeline(pipe, pipe_start, pipe_end)
print("stocks.shape [close]", stocks)

from sharadar.pipeline.factors import MarketCap, EV, Fundamentals
pipe_mkt_cap = Pipeline(columns={
    'mkt_cap': MarketCap()
},
)

start_time = time.time()
stocks = spe.run_pipeline(pipe_mkt_cap, pipe_start, pipe_end)
print("stocks.shape [mkt cap]", stocks.shape)
print("--- %s ---" % datetime.timedelta(seconds=(time.time() - start_time)))

pipe_mkt_cap_ev = Pipeline(columns={
    'mkt_cap': MarketCap(),
    'ev': EV(),
    'debt': Fundamentals(field='debtusd_arq'),
    'cash': Fundamentals(field='cashnequsd_arq')
},
screen = StaticAssets(symbols(['IBM', 'F', 'AAPL']))
)

stocks = spe.run_pipeline(pipe_mkt_cap_ev, pipe_start, pipe_end)
print(stocks)


