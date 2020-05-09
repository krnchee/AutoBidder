from flask import Flask, request, jsonify
import math

app = Flask(__name__)


global items_for_sale
# Create items list with default values
items_for_sale = {'skates': [], 'unicycle': [], 'hover board': []}

# Post route for posting bids towards an item
@app.route('/submit_bid', methods = ['Post'])
def submit_bid():
    name = request.args.get('username')
    start_bid = request.args.get('starting_bid')
    max_bid = request.args.get('max_bid')
    increment_amount = request.args.get('auto_increment_amount')
    auction_item = request.args.get('auction_item')
    if auction_item:
        auction_item = auction_item.lower()


    if not start_bid or not max_bid or not increment_amount:
        return 'Please enter all bidding values'

    if len(name) == 0:
        return 'Please enter a username!'
        
    # No items left to auction
    if len(items_for_sale) == 0:
        return 'All items have been sold! See you next auction!'

    try:
        float(start_bid)
        float(max_bid)
        float(increment_amount)
    except:
        return 'Please try again and enter positive interger values '\
        'for starting_bid, max_bid, and auto_increment_amount'
    if float(start_bid) < 0 or float(max_bid) < 0 or float(increment_amount) < 0:
        return 'Please try again and enter positive interger values '\
        'for starting_bid, max_bid, and auto_increment_amount'

    start_bid = float(start_bid)
    max_bid = float(max_bid)
    increment_amount = float(increment_amount)

    # Ensure max bid is greater then start bid
    if max_bid < start_bid:
        return 'Max Bid must be greater then Starting Bid'

    # If item is not on auction list, returns list so user can see which items are on list
    if auction_item not in list(items_for_sale.keys()):
        return 'This item is not up for sale. Here the current list of items for sale:\n' \
        + auction_items_for_sale()

    for item in items_for_sale:
        if item == auction_item:
            queue = items_for_sale[item]
            if len(queue) > 0:
                for bid in queue:
                    # Checks if username is already been used by another bidder
                    if bid['name'] == name:
                        return "Some one has already bid with username "\
                        "{}. Please bid again with different username.".format(name)

            # Creates hashmap of bidding information and adds to auction queue for item
            bidding_info = {}
            bidding_info['name'] = name
            bidding_info['start_bid'] = start_bid
            bidding_info['max_bid'] = max_bid
            bidding_info['increment_amount'] = increment_amount

            # Calculates highest potetial bid the bidder can make given their parameters
            highest_potential_bid = start_bid
            while highest_potential_bid <= max_bid:
                highest_potential_bid += increment_amount

            highest_potential_bid -= increment_amount
            bidding_info['highest_potential_bid'] = highest_potential_bid

            queue.append(bidding_info)

            # If there are a total of 3 bidders, auction will initiate, else
            # we will return and wait for more bidders on this item
            if len(queue) == 3:
                return initiate_auction(item)
            return 'Your bid has been submitted! Once a total of three bids '\
            'are placed, the auction will start!'

# Get route that returns a list of all items still availble to bid on
@app.route('/auction_items_for_sale', methods = ['GET'])
def auction_items_for_sale():
    items_string = ''
    for item in items_for_sale:
        queue = items_for_sale[item]
        # if length of queue is less then 3, we are still taking bidders on item
        if len(queue) < 3:
            items_string += '{} currently has {} bidders.\n'.format(item, len(queue))
    items_string += 'Auction items will no longer be available once three bids are placed. So hurry!'
    return items_string

def initiate_auction(item):
    # Select item from items list
    bids_on_item = items_for_sale[item]
    highest_bid, second_highest_bid, highest_inc_amount = 0, 0, 0
    winner_name = ''

    # Find bids with the highest and second highest potential bids.
    for bid in bids_on_item:
        if bid['highest_potential_bid'] > highest_bid:
            second_highest_bid = highest_bid
            highest_bid = bid['highest_potential_bid']
            highest_inc_amount = bid['increment_amount']
            winner_name = bid['name']
        elif bid['highest_potential_bid'] > second_highest_bid and bid['highest_potential_bid'] <= highest_bid:
            second_highest_bid  = bid['highest_potential_bid']

    # Once we have highest and second highest bids, decrement highest
    # by its increment amount until it is below second highest
    # potential bid.
    while highest_bid > second_highest_bid:
        highest_bid -= highest_inc_amount

    # Increment once by increment amount to insure no other bid can out bid it.
    if highest_bid > second_highest_bid:
        highest_bid += highest_inc_amount

    # Remove item from items_for_sale at the end of auction
    del items_for_sale[item]

    return 'The winner of the auction item {} goes to {} for a' \
    ' total of ${}'.format(item, winner_name, highest_bid)


if __name__ == "__main__":
    app.run(debug=True)
