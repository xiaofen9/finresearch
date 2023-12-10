from src.canvas.peerCompare import Ploter
from src.dataProvider.quote import TiingoProvider
import datetime



def whatIfPurchase10k(data, startDate):
    investment = 10000
    results = {}
    startDate = datetime.datetime.strptime(startDate, "%Y-%m-%d")


    # Find the earliest data point that is on or after the startDate
    earliest_data = min(
        (entry for entry in data if datetime.datetime.strptime(entry['date'].split('T')[0], "%Y-%m-%d") >= startDate),
        key=lambda x: x['date'],
        default=None
    )

    # exit if startDate and earliest_data has a gap of more than 1 month
    if earliest_data is not None:
        earliest_date = datetime.datetime.strptime(earliest_data['date'].split('T')[0], "%Y-%m-%d")
        if abs(earliest_date - startDate).days > 30:
            exit("EXIT: cannot find data on or after startDate, the earliest avalible data is " + earliest_data['date'].split('T')[0])
    
    # If there is no data on or after startDate, return an empty list
    if earliest_data is None:
        return results
    purchase_price = earliest_data['close']

    # Calculate the number of shares you can purchase
    shares_purchased = investment / purchase_price

    # Iterate over data points on or after startDate
    for entry in data:
        entryDate = datetime.datetime.strptime(entry['date'].split('T')[0], "%Y-%m-%d")
        if entryDate >= startDate:
            # Calculate asset worth for each date
            assetWorth = shares_purchased * entry['close']
            results[entry['date'].split('T')[0]] = assetWorth
    return results

startDates = ['2008-9-1', '2020-2-1', '2019-7-1', '2007-8-1', '2002-10-1']
offset_dates = [datetime.timedelta(days=30*0), datetime.timedelta(days=30*6), datetime.timedelta(days=30*12), datetime.timedelta(days=30*18), datetime.timedelta(days=30*24)]

sourcer = TiingoProvider(token="PUT_YOUR_TIINGO_TOKEN_HERE")

tltData = sourcer.queryDaily('tlt')
vooData = sourcer.queryDaily('spy')

for startDate in startDates:
    startDateObj = datetime.datetime.strptime(startDate, "%Y-%m-%d")
    
    for offset in offset_dates:
        newstartDateObj = startDateObj -  offset
        newstartDate = newstartDateObj.strftime("%Y-%m-%d")
        voo_asset_values = whatIfPurchase10k(vooData, newstartDate)
        tlt_asset_values = whatIfPurchase10k(tltData, newstartDate)

        ploter = Ploter(filename=startDate + "-" + str(offset.days) + '.png', title=str(offset.days) + ' days before rate cuts')
        ploter.plot([{ 'name':'spy', "data": voo_asset_values}, {'name':'tlt', "data": tlt_asset_values}], duration=datetime.timedelta(days=300)+offset)
