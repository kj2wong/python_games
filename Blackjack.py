# Implementation of Blackjack
# Author: Kevin Jordan Wong
# Written and run through codeskulptor.org, a web Python IDE written for
#	a Coursera.org Python course

# Follow the link below and hit run to see the program run
# http://www.codeskulptor.org/#user25_FlQb0etlD4eG2BS.py

# Note: if the link has expired, copy this code into Codeskulptor.org and run

#Note: simplegui is a graphics module written specifically for Codeskulptor.org
import simplegui
import random

# load card sprite - 949x392 - source: jfitz.com
CARD_SIZE = (73, 98)
CARD_CENTER = (36.5, 49)
card_images = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/cards.jfitz.png")

# load image for back of card (for the dealer)
CARD_BACK_SIZE = (71, 96)
CARD_BACK_CENTER = (35.5, 48)
card_back = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/card_back.png")    

# initialize some useful global variables
in_play = False
outcome = ""
score = 0

# define global tuples and dictionary for the cards
SUITS = ('C', 'S', 'H', 'D')
RANKS = ('A', '2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K')
VALUES = {'A':1, '2':2, '3':3, '4':4, '5':5, '6':6, '7':7, '8':8, '9':9, 'T':10, 'J':10, 'Q':10, 'K':10}


# class: Card
#	Represents each individual card in the deck
class Card:
    def __init__(self, suit, rank):
        if (suit in SUITS) and (rank in RANKS):
            self.suit = suit
            self.rank = rank
        else:
            self.suit = None
            self.rank = None
            print "Invalid card: ", suit, rank

	# method: __str__
	#	the str representation will just be the suit and rank of the card
    def __str__(self):
        return self.suit + self.rank
	
	#method: get_suit()
	#	returns suit of the card
    def get_suit(self):
        return self.suit
	
	#method: get_rank()
	#	returns rank of the card
    def get_rank(self):
        return self.rank

	
	#method: draw
	#	draws the card onto the canvas using the canvas.draw_image function in the simplegui module
    def draw(self, canvas, pos):
        card_loc = (CARD_CENTER[0] + CARD_SIZE[0] * RANKS.index(self.rank), 
                    CARD_CENTER[1] + CARD_SIZE[1] * SUITS.index(self.suit))
        canvas.draw_image(card_images, card_loc, CARD_SIZE, [pos[0] + CARD_CENTER[0], pos[1] + CARD_CENTER[1]], CARD_SIZE)
        
# class: Hand
#	Represent a person's hand in Blackjack (incl player and dealer)
class Hand:
    def __init__(self):
        self.cards = []
		
	#method: __str__
	#	The string rep. of a hand will be "Hand contains __ __ __ __"
    def __str__(self):
        current_hand = "Hand contains "
        for card in self.cards:
            current_hand += str(card) + " "
        return current_hand

	#method: add_card
	#	adds a card to a hand
    def add_card(self, card):
        if (card.get_suit() in SUITS) and (card.get_rank() in RANKS):
            self.cards.append(card)

	#method: get_value
	#	returns the total value of a person's hand
	#	Note: aces count as 1, and if the hand has an ace, add 10 to hand value if it doesn't bust
    def get_value(self):
        total = 0
		#use a counter to keep track of all the aces
        numOfAces = 0
        for card in self.cards:
            total += VALUES[card.get_rank()]
            if card.get_rank() == "A":
                numOfAces += 1
        
        for ace in range(numOfAces):
            if (total <= 11):
                total += 10
        
        return total
	
	#method: draw
	#	draws each card in the hand using the Card.draw method
    def draw(self, canvas, pos):
        new_pos = pos
        for card in self.cards:
            card.draw(canvas, new_pos)
            new_pos[0] += CARD_SIZE[0] + 10
 
        
# class: Deck
#	Represents a full 52 card deck
class Deck:
    def __init__(self):
		# add all the cards to the list
        self.full_deck = []
        for suit in SUITS:
            for rank in RANKS:
                self.full_deck.append(Card(suit, rank))
	
	#method: shuffle
	#	shuffles the deck using the random module
    def shuffle(self):
        random.shuffle(self.full_deck)

	#method: deal_card
	#	deals a card to a player, and removes it from the deck
    def deal_card(self):
        return self.full_deck.pop(0)
		
    #method: __str__
	#	The string rep. of a deck will be "Deck contains __ __ __ __"
    def __str__(self):
        current_deck = "Deck contains "
        for card in self.full_deck:
            current_deck += str(card) + " "
        return current_deck 

# function: deal
#	The button handler for the deal button
def deal():
    global outcome, in_play, next_move, score
    global deck, dealer, player

    outcome = ""
    next_move = "Hit or Stand?"
    
	# if a player hits deal in the middle of a hand, he/she automatically loses
    if in_play == True:
        outcome = "Deal during a game. You lose!"
        score -= 1
    
	#Initialize the deck and hands, and shuffle the deck
    deck = Deck()
    deck.shuffle()
    dealer = Hand()
    player = Hand()
    
	#deal 2 cards to each the player and dealer
    player.add_card(deck.deal_card())
    dealer.add_card(deck.deal_card())
    player.add_card(deck.deal_card())
    dealer.add_card(deck.deal_card())
    
	#set the global var in_play to signal that the game has started
    in_play = True

#function: hit
#	The button handler for the hit button
def hit(): 
    global outcome, next_move, in_play, score
	
    # if the hand is in play and the player is still at or under 21, give the player another card
    if in_play == True:
		#check if the player still has a hand at or under 21
        if player.get_value() <= 21:
            player.add_card(deck.deal_card())
   
        # if busted, assign a message to outcome, update in_play and score
        if player.get_value() > 21:
            outcome = "You have busted. You lose!"
            next_move = "New deal?"
            in_play = False
            score -= 1

# function: stand
#	The button handler for the stand button
def stand():
    global outcome, next_move, in_play, score
    
	# remind the player if they already busted
    if player.get_value() > 21:
        outcome = "You have already busted!"
    
    # if hand is in play, repeatedly hit dealer until his hand has value 17 or more
    if in_play == True:
        while dealer.get_value() < 17:
            dealer.add_card(deck.deal_card())

    # assign a message to outcome, update in_play and score
    if in_play == True:
        if dealer.get_value() > 21:
            outcome = "Dealer has busted. You win!"
            score += 1
        elif dealer.get_value() > player.get_value():
            outcome = "You lose!"
            score -= 1
        elif dealer.get_value() < player.get_value():
            outcome = "You win!"
            score += 1
		else:
			outcome = "Push!"
        next_move = "New deal?"
        in_play = False

# function: draw
#	The draw handler
def draw(canvas):
    canvas.draw_text('Blackjack', (40, 80), 50, 'Aqua')
    canvas.draw_text('Score: ', (320, 80), 30, 'Orange')
    canvas.draw_text(str(score), (420, 80), 30, 'Orange')
    
    canvas.draw_text('Dealer', (60, 150), 40, 'Black')
    dealer.draw(canvas, [60,180])
    
    canvas.draw_text('Player', (60, 370), 40, 'Black')
    player.draw(canvas, [60,400])
    
    canvas.draw_text(outcome, (200, 150), 30, 'Black')
    canvas.draw_text(next_move, (200, 370), 30, 'Black')
    
	# if the game is still going on, hide one of the dealer's cards by drawing the back of the card
    if in_play == True:
        canvas.draw_image(card_back, (35.5, 48), CARD_BACK_SIZE, (60 + 35.5, 180 + 48), CARD_BACK_SIZE)


# initialization frame
frame = simplegui.create_frame("Blackjack", 600, 600)
frame.set_canvas_background("Green")

#create buttons and canvas callback
frame.add_button("Deal", deal, 200)
frame.add_button("Hit",  hit, 200)
frame.add_button("Stand", stand, 200)
frame.set_draw_handler(draw)

# get things rolling
deal()
frame.start()
