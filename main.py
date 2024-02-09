
import argparse
from data_analysis import get_date_range, validate_positive_int, get_info
from plotting import save_plot
from stock_data import download_stock_data
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns


def main():
    parser = argparse.ArgumentParser(description='Stock Analysis Tool')
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('--days', '-d', type=validate_positive_int, help='Specify the number of days for analysis')
    group.add_argument('--months', '-m', type=validate_positive_int, help='Specify the number of months for analysis')
    group.add_argument('--year', '-y', type=validate_positive_int, help='Specify the number of years for analysis')
    
    args = parser.parse_args()
    
    if args.days:
        start, end = get_date_range(str(args.days))
    elif args.months:
        start, end = get_date_range(str(args.months * 30))
    elif args.year:
        start, end = get_date_range(str(args.year * 365))
 
    tickers = ["GOOGL", "META", "AAPL", "AMZN", "F", "CSCO"]

    gogl = download_stock_data(tickers[0], start, end)
    meta = download_stock_data(tickers[1], start, end)
    aapl = download_stock_data(tickers[2], start, end) 
    amzn = download_stock_data(tickers[3], start, end) 
    ford = download_stock_data(tickers[4], start, end)
    csco = download_stock_data(tickers[5], start, end)

    # Display one of the stocks data
    aapl

    # def get_info(dataframe) :
    #     stock_info = pd.DataFrame({
    #                    'Datatype' : dataframe.dtypes,          # Data types of columns
    #                    'Total_Element': dataframe.count(),     # Total elements in columns
    #                    'Null_Count': dataframe.isnull().sum(), # Total null values in columns
    #                    'Null_Percentage': dataframe.isnull().sum()/len(dataframe) * 100 # Percentage of null values 
    #                        })
    #     return stock_info

    # Call the function for each stock  

    # aapl=get_info(aapl)
    # amzn=get_info(amzn)
    # ford=get_info(ford)
    # csco=get_info(csco)

    gogl_vol_avg = round(gogl["Volume"].mean())
    meta_vol_avg = round(meta["Volume"].mean())
    aapl_vol_avg = round(aapl["Volume"].mean())
    amzn_vol_avg = round(amzn["Volume"].mean())
    ford_vol_avg = round(ford["Volume"].mean())
    csco_vol_avg = round(csco["Volume"].mean())


    #to convert the results into an array
    print(gogl_vol_avg)
    vol_avg = np.array([gogl_vol_avg , meta_vol_avg , aapl_vol_avg , amzn_vol_avg , ford_vol_avg , csco_vol_avg ])  
    #vol_avg 

    print(vol_avg) 
    mylabels = ["Google", "Meta","Apple", "Amazon", "Ford", "Cisco"] 
    myexplode = [0.2, 0, 0, 0,0,0]  # To create an exploding wedge 

    plt.pie(vol_avg, labels = mylabels, explode = myexplode, shadow = True, autopct="%.2f") 
    save_plot(plt, 'pie_chart.png')
    plt.show() 

    # Perform the visualization in a single graph
    gogl['Volume'].plot(label = 'Google')  
    meta['Volume'].plot(label = 'Meta')  
    aapl['Volume'].plot(label = 'Apple', figsize = (16,8))  
    amzn['Volume'].plot(label = "Amazon")  
    ford['Volume'].plot(label = 'Ford')  
    csco['Volume'].plot(label = 'Cisco')   

    plt.title('Volume of Stock traded')
    plt.legend()
    save_plot(plt, 'volume_plot.png')
    plt.show()

    gogl['Volume'].plot(label = 'Google')
    meta['Volume'].plot(label = 'Meta') 
    aapl['High'].plot(label = 'Apple', figsize = (16,8)) 
    amzn['High'].plot(label = "Amazon")
    ford['High'].plot(label = 'Ford') 
    csco['High'].plot(label = 'Cisco') 

    plt.title('Highest Price Reached for Each Stock traded') 
    plt.legend() 
    save_plot(plt, 'highest_price.png')
    plt.show()


    gogl['Volume'].plot(label = 'Google')
    meta['Volume'].plot(label = 'Meta')
    aapl['Low'].plot(label = 'Apple', figsize = (16,8)) 
    amzn['Low'].plot(label = "Amazon")
    ford['Low'].plot(label = 'Ford')
    csco['Low'].plot(label = 'Cisco')


    plt.title('Lowest Price Reached for Each Stock traded')
    plt.legend()
    save_plot(plt, 'lowest_price.png')
    plt.show()

    gogl['Volume'].plot(label = 'Google')
    meta['Volume'].plot(label = 'Meta')
    aapl['Open'].plot(label = 'Apple', figsize = (16,8))
    amzn['Open'].plot(label = "Amazon")
    ford['Open'].plot(label = 'Ford')
    csco['Open'].plot(label = 'Cisco') 

    plt.title('Open Price for Each Stock traded')
    plt.legend()
    save_plot(plt, 'open_price.png')
    plt.show()


    #Find the market capitalization values for each of the 6 stocks and visualize the results to determine which stocks would provide a lower risk, with greater returns over time.
    gogl['M_Cap'] = gogl['Open'] * gogl['Volume']
    meta['M_Cap'] = meta['Open'] * meta['Volume']
    aapl['M_Cap'] = aapl['Open'] * aapl['Volume']
    amzn['M_Cap'] = amzn['Open'] * amzn['Volume']
    ford['M_Cap'] = ford['Open'] * ford['Volume']
    csco['M_Cap'] = csco['Open'] * csco['Volume']


    gogl['M_Cap'].plot(label = 'Google') 
    meta['M_Cap'].plot(label = 'Meta') 
    aapl['M_Cap'].plot(label = 'Apple', figsize = (15,7)) 
    amzn['M_Cap'].plot(label = 'Amazon') 
    ford['M_Cap'].plot(label = 'Ford') 
    csco['M_Cap'].plot(label = 'Cisco') 

    plt.title('Market Cap') 
    plt.legend()
    save_plot(plt, 'market_capitalization.png') 
    plt.show()

    # Find the MA for all the stocks

    gogl['MA50'] = gogl['Open'].rolling(50).mean()
    gogl['MA200'] = gogl['Open'].rolling(200).mean()

    meta['MA50'] = meta['Open'].rolling(50).mean()
    meta['MA200'] = meta['Open'].rolling(200).mean() 

    aapl['MA50'] = aapl['Open'].rolling(50).mean()
    aapl['MA200'] = aapl['Open'].rolling(200).mean() 

    amzn['MA50'] = amzn['Open'].rolling(50).mean()
    amzn['MA200'] = amzn['Open'].rolling(200).mean()

    ford['MA50'] = ford['Open'].rolling(50).mean() 
    ford['MA200'] = ford['Open'].rolling(200).mean()

    csco['MA50'] = csco['Open'].rolling(50).mean()
    csco['MA200'] = csco['Open'].rolling(200).mean()

    # Plot them together to compare them

    figure, axes = plt.subplots(2,3, figsize = (15, 10))

    figure.suptitle('Moving Averages for Google,Meta ,Apple, Amazon, Ford, and Cisco')

    axes[0,0].set_title('Google')
    axes[0,1].set_title('Meta')
    axes[0,2].set_title('Apple')
    axes[1,0].set_title('Amazon')   
    axes[1,1].set_title('Ford')
    axes[1,2].set_title('Cisco')  


    gogl['MA50'].plot(ax=axes[0, 0])
    gogl['MA200'].plot(ax=axes[0, 0])
    gogl['Open'].plot(ax=axes[0, 0])

    meta['MA50'].plot(ax=axes[0, 1])
    meta['MA200'].plot(ax=axes[0, 1])
    meta['Open'].plot(ax=axes[0, 1])

    aapl['MA50'].plot(ax=axes[0, 2 ])
    aapl['MA200'].plot(ax=axes[0, 2])
    aapl['Open'].plot(ax=axes[0, 2])
 
    amzn['MA50'].plot(ax=axes[1, 0])
    amzn['MA200'].plot(ax=axes[1, 0])
    amzn['Open'].plot(ax=axes[1, 0])

    ford['MA50'].plot(ax=axes[1, 1])
    ford['MA200'].plot(ax=axes[1, 1])
    ford['Open'].plot(ax=axes[1, 1])

    csco['MA50'].plot(ax=axes[1, 2])
    csco['MA200'].plot(ax=axes[1, 2])
    csco['Open'].plot(ax=axes[1, 2])

    plt.legend()
    save_plot(plt, 'moving_averages.png')
    plt.show()

    # Finding the volatility / stability for each of the stocks.

    gogl['returns'] = (gogl['Close']/gogl['Close'].shift(1)) -1
    meta['returns'] = (meta['Close']/meta['Close'].shift(1)) -1
    aapl['returns'] = (aapl['Close']/aapl['Close'].shift(1)) -1
    amzn['returns'] = (amzn['Close']/amzn['Close'].shift(1)) -1
    ford['returns'] = (ford['Close']/ford['Close'].shift(1)) -1
    csco['returns'] = (csco['Close']/csco['Close'].shift(1)) -1

    # Visualize the results.

    figure, axes = plt.subplots(2, 3, figsize = (15, 10))

    figure.suptitle('Stability and Volatility for Google , Meta, Apple, Amazon, Ford, and Cisco')

    axes[0,0].set_title('Google')
    axes[0,1].set_title('Meta')
    axes[0,2].set_title('Apple')
    axes[1,0].set_title('Amazon')  
    axes[1,1].set_title('Ford')
    axes[1,2].set_title('Cisco') 

    gogl['returns'].hist(bins = 100, label = 'Google', alpha = 0.5, ax=axes[0, 0])

    meta['returns'].hist(bins = 100, label = 'Meta', alpha = 0.5, ax=axes[0, 1])

    aapl['returns'].hist(bins = 100, label = 'Apple', alpha = 0.5, ax=axes[0, 2])

    amzn['returns'].hist(bins = 100, label = 'Amazon', alpha = 0.5, ax=axes[1, 0])

    ford['returns'].hist(bins = 100, label = 'Ford', alpha = 0.5, ax=axes[1, 1])

    csco['returns'].hist(bins = 100, label = 'Cisco', alpha = 0.5, ax=axes[1, 2])


    plt.legend()
    save_plot(plt, 'stability_volatility.png')
    plt.show()

    # Comparing the volatility / stability for all the stocks.

    gogl['returns'] = (gogl['Close']/gogl['Close'].shift(1)) -1
    meta['returns'] = (meta['Close']/meta['Close'].shift(1)) -1
    aapl['returns'] = (aapl['Close']/aapl['Close'].shift(1)) -1
    amzn['returns'] = (amzn['Close']/amzn['Close'].shift(1))-1
    ford['returns'] = (ford['Close']/ford['Close'].shift(1)) - 1
    csco['returns'] = (csco['Close']/csco['Close'].shift(1)) - 1

    gogl['returns'].hist(bins = 100, label = 'Google', alpha = 0.5)
    meta['returns'].hist(bins = 100, label = 'Meta', alpha = 0.5)
    aapl['returns'].hist(bins = 100, label = 'Apple', alpha = 0.5, figsize = (15,7))
    amzn['returns'].hist(bins = 100, label = 'Amazon', alpha = 0.5)
    ford['returns'].hist(bins = 100, label = 'Ford', alpha = 0.5)
    csco['returns'].hist(bins = 100, label = 'Cisco', alpha = 0.5)

    plt.legend()
    save_plot(plt, 'comparing_S_V.png')
    plt.show()


    # Correlation table for Stock 1
    gogl_corr = gogl.corr()
    print(gogl_corr)

    # Correlation table for Stock 2
    meta_corr = meta.corr()
    print(meta_corr)

    # Correlation table for Stock 3
    aapl_corr = aapl.corr()
    print(aapl_corr)

    # Correlation table for Stock 4
    amzn_corr = amzn.corr()
    print(amzn_corr)

    # Correlation table for Stock 5

    ford_corr = ford.corr()
    print(ford_corr)

    # Correlation table for Stock 6

    csco_corr = csco.corr()
    print(csco_corr)


    # Heatmap for Stock 1
    sns.heatmap(gogl_corr, annot=True)
    plt.legend()
    save_plot(plt, 'heatmap1.png')
    plt.show()

    # Heatmap for Stock 2
    sns.heatmap(meta_corr, annot=True)
    plt.legend()
    save_plot(plt, 'heatmap2.png')
    plt.show()

   # Heatmap for Stock 3
    sns.heatmap(aapl_corr, annot=True)
    plt.legend()
    save_plot(plt, 'heatmap3.png')
    plt.show()

    # Heatmap for Stock 4

    sns.heatmap(amzn_corr, annot=True)
    plt.legend()
    save_plot(plt, 'heatmap4.png')
    plt.show()

   # Heatmap for Stock 5

    sns.heatmap(ford_corr, annot=True)
    plt.legend()
    save_plot(plt, 'heatmap5.png')
    plt.show()

   # Heatmap for Stock 6

    sns.heatmap(csco_corr, annot=True)
    plt.legend()
    save_plot(plt, 'heatmap6.png')
    plt.show()

if __name__ == "__main__":
    main()    