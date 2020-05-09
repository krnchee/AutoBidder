# AutoBidder

This app allows a user to auction on 3 default items (skates, unicycle, hover board) in an auction.
Once an item has 3 bids, the auction for that item will initiate. Only 3 bids will be taken and once
the third bid is placed, the output will show the winning bidders name and price paid for that item.

##Instructions

Need Python installed!

First create virtual environment by running source venv/bin/activate

Next run pip3 install -r requirements.txt

Start app by running python app.py

##REST APIs:

To retrieve all items for sale:

GET request on localhost:5000/auction_items_for_sale:

ex) http://localhost:5000/auction_items_for_sale

To post a bid on an item:

POST request on localhost:5000/submit_bid with following parameters:

username - must be unique for each bid,
auction_item - must be a one of these three: skates, unicycle, hover board,
max_bid - must be a positive number and greater then the starting bid,
starting_bid - must be a positive number and smaller then the max bid,
auto_increment_amount - must be a positive number

ex) http://localhost:5000/submit_bid?username=olivia&auction_item=unicycle&max_bid=725&starting_bid=599&auto_increment_amount=15

##Unit Test:

To run: python test.py -v
