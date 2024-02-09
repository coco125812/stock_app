import os
import argparse
from flask import Flask, render_template, request, redirect, url_for , send_from_directory
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import yfinance as yf
from pandas.plotting import scatter_matrix
from matplotlib.pyplot import savefig
from datetime import datetime, timedelta



app = Flask(__name__)



@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        stock_symbol = request.form['stock_symbol']
        date_range_option = request.form['date_range']

        start_date, end_date = get_date_range(date_range_option)

        if stock_symbol and start_date and end_date:
            # Call your analysis functions with the selected stock symbol and date range
            analyze_stock(stock_symbol, start_date, end_date)
            return redirect(url_for('results', stock_symbol=stock_symbol))

    return render_template('index.html')


@app.route('/results', methods=['GET', 'POST'])
def results():
    print(request.form)
    if request.method == 'POST':
        selected_stocks = request.form.getlist('stock_symbols')  # Get a list of selected stocks
        date_range_option = request.form['date_range']

        start_date, end_date = get_date_range(date_range_option)

        if not selected_stocks:
            return render_template('index.html', error_message="Please select at least one stock.")

        try:
            analyzed_data = analyze_stock(selected_stocks, start_date, end_date)

            if len(selected_stocks) == 1:
                # Single stock selected, display detailed information
                stock_symbol = selected_stocks[0]
                context = {'analyzed_data': analyzed_data[stock_symbol].to_html(classes='table table-striped')}
                return render_template('results.html', **context)
            else:
                # Multiple stocks selected, generate visualizations
                pie_chart = generate_pie_chart(analyzed_data)
                context = {'pie_chart': pie_chart}
                return render_template('results_comparison.html', **context)

        except ValueError as e:
            return render_template('index.html', error_message=str(e))

    elif request.method == 'GET':
        # Handle GET request, for example, redirect to the home page or display an error message
        return redirect(url_for('result'))

# ... (existing code)

def generate_pie_chart(analyzed_data):
    # Example: Create a pie chart of market capitalization for multiple stocks
    plt.figure(figsize=(8, 8))
    labels = analyzed_data.keys()
    sizes = [data['Market Cap'].sum() for data in analyzed_data.values()]
    plt.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90)
    plt.title('Market Capitalization Comparison')
    chart_path = 'static/pie_chart.png'
    savefig(chart_path)
    return chart_path

def analyze_stock(stock_symbols, start_date, end_date):
    analyzed_data = {}

    for stock_symbol in stock_symbols:
        try:
            # Fetch historical data for the specified stock symbol and date range
            stock_data = yf.download(stock_symbol, start=start_date, end=end_date)
            
            # Calculate market capitalization
            market_cap = calculate_market_cap(stock_data)

            # Calculate moving averages
            moving_averages = calculate_moving_averages(stock_data)

            # Store the analyzed data in a DataFrame
            analyzed_data[stock_symbol] = pd.DataFrame({
                'Market Cap': market_cap,
                'Moving Averages': moving_averages
            })

        except Exception as e:
            # Handle invalid stock symbol
            raise ValueError(f"Error analyzing stock {stock_symbol}: {str(e)}")

    return analyzed_data

def calculate_market_cap(stock_data):
    # Calculate market capitalization (example: using closing price)
    market_cap = stock_data['Close'] * stock_data['Volume']
    return market_cap

def calculate_moving_averages(stock_data):
    # Calculate moving averages (example: 20-day and 50-day)
    stock_data['MA_20'] = stock_data['Close'].rolling(window=20).mean()
    stock_data['MA_50'] = stock_data['Close'].rolling(window=50).mean()
    return stock_data[['MA_20', 'MA_50']]



@app.route('/output_images/<filename>')
def uploaded_file(filename):
    return send_from_directory('output_images', filename)


def save_plot(plt, filename):
    output_folder = "output_images"
    os.makedirs(output_folder, exist_ok=True)
    filepath = os.path.join(output_folder, filename)
    plt.savefig(filepath)
    plt.show()
    plt.close()

def get_date_range(option):
    end_date = datetime.now().strftime('%Y-%m-%d')
    
    if option == '7':
        start_date = (datetime.now() - timedelta(days=7)).strftime('%Y-%m-%d')
    elif option == '30':
        start_date = (datetime.now() - timedelta(days=30)).strftime('%Y-%m-%d')
    elif option == '365':
        start_date = (datetime.now() - timedelta(days=365)).strftime('%Y-%m-%d')
    else:
        raise ValueError("Invalid option. Please provide a valid integer for days, months, or years.")
    
    return start_date, end_date


def validate_positive_int(value):
    try:
        int_value = int(value)
        if int_value <= 0:
            raise argparse.ArgumentTypeError("Value must be a positive integer.")
        return int_value
    except ValueError:
        raise argparse.ArgumentTypeError("Invalid input. Please provide a valid integer.")

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

    gogl = yf.download("GOGL",start,end)  
    meta = yf.download("META",start,end)  
    aapl = yf.download("AAPL", start, end)  
    amzn = yf.download("AMZN", start, end)  
    ford = yf.download("F", start, end)   
    csco = yf.download("CSCO", start, end)  

    # Display one of the stocks data
    aapl

    def get_info(dataframe) :
        stock_info = pd.DataFrame({
                       'Datatype' : dataframe.dtypes,          # Data types of columns
                       'Total_Element': dataframe.count(),     # Total elements in columns
                       'Null_Count': dataframe.isnull().sum(), # Total null values in columns
                       'Null_Percentage': dataframe.isnull().sum()/len(dataframe) * 100 # Percentage of null values 
                           })
        return stock_info

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


    # to convert the results into an array
    print(gogl_vol_avg)
    vol_avg = np.array([gogl_vol_avg , meta_vol_avg , aapl_vol_avg , amzn_vol_avg , ford_vol_avg , csco_vol_avg ])  
    # vol_avg 

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
    app.run(debug=True)   