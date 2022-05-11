import random

import numpy as np
from otree.api import *

# need to code to handle non-consent

c = Currency  # old name for currency; you can delete this.

doc = """
This is a one-period public goods game with 3 players.
"""


class Constants(BaseConstants):
    name_in_url = 'A'
    players_per_group = None
    buyer_role = 'Buyer'
    seller1_role = 'Seller'
    bystander_role = 'Bystander'
    seller2_role = 'Seller'
    num_rounds = 13
    # """Amount allocated to each player"""
    endowment = cu(100)
    multiplier = 12


class Subsession(BaseSubsession):
    ##print("test")
    offersrem = models.IntegerField()
    game_finished = models.BooleanField()
    numbuyers = models.IntegerField()
    bnum = models.IntegerField()
    payround = models.IntegerField()


def creating_session(session):
    random.seed()
    rcoun = 1
    a = np.squeeze(np.asarray(session.get_group_matrix()))  # create NP version
    session.offersrem = 0
    session.numbuyers = int(((a.size - 1) / 3))
    session.bnum = 1
    session.payround = random.randint(2, Constants.num_rounds)

    ##print(session.get_group_matrix())
    ##print(session.round_number)
    ##print("a")
    ##print(a)
    partnum = a.size  # participants number
    if partnum > 4:
        last = np.arange(partnum - 3, partnum + 1)  # creates array for last group
        matrix = np.arange(1, (partnum - 3))  # creates array for groups of 3
        new_structure = np.reshape(matrix, (-1, 3))  # Restructures into matrix for groups of 3
        new_structure = new_structure.tolist()  # converst to list of arrays
        new_structure.append(last)  # adds last array
    else:
        matrix = np.arange(1, partnum + 1)
        new_structure = np.reshape(matrix, (-1, 4))  # Restructures into matrix for groups of 3
        new_structure = new_structure.tolist()  # converst to list of arrays

    session.group_like_round(1)
    ##print("matrix")
    if session.round_number == 1:
        ##print(matrix)
        ##print("ns")
        ##print(new_structure)
        session.set_group_matrix(new_structure)  # Regroups
    # #print(session.get_group_matrix())
    ##print(session.get_group_matrix())

    if session.round_number == 1:
        for group in session.get_groups():
            ##print("inrand")
            player = group.get_players()
            random.shuffle(player)
            group.set_players(player)
    rcoun = rcoun + 1
    ##print("randone")
    ##print(session.get_group_matrix())
    ##print(rcoun)
    treatment(session)


def treatment(session):
    for player in session.get_players():
        if session.session.config['treatment'] == 0:
            player.treatment = 0
            player.pay = 0
        if session.session.config['treatment'] == 1:
            player.treatment = 1
        if session.session.config['treatment'] == 2:
            player.treatment = 2


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    Seatfinal = models.StringField(
        label="Carefully Confirm Seat Number"
    )

    finalpay = models.IntegerField(initial=0)

    payroundpay = models.IntegerField(initial=0)

    QCorrect = models.IntegerField(initial=0)

    treatment = models.IntegerField(
    )
    Q1a = models.IntegerField(
        min=0,
        max =1024,
        label="a. How many points would the Seller earn for the task if round 4 was selected as the payment round?"
    )
    Q1b = models.IntegerField(
        min=0,
        max=1024,
        label="b. How many points would the Buyer earn for the task if round 4 was selected as the payment round?"
    )
    Q1c = models.IntegerField(
        min=0,
        max=1023,
        label="c. How many points would the Bystander earn for the task if round 4 was selected as the payment round?"
    )
    # Q1d = models.IntegerField()
    Q2a = models.IntegerField(
        min=0,
        max=1023,
        label="2. In round 8, assume that a Seller offers a product for sale at a price of 25 points and no Buyer buys the product. How many points would that Seller earn for the task if round 8 was selected as the payment round?"
    )
    Q3 = models.IntegerField(
        min=0,
        max=1023,
        label="3. How many points does each participant earn for completing the study?"
    )
    Q4 = models.BooleanField(  # true
        label="4. There are more Buyers than Sellers in this session (True or False)?",
        choices=[
            [True, 'True'],
            [False, 'False']
        ]
    )
    Q5 = models.BooleanField(  # true
        label="5. There are the same number of Bystanders and Sellers in this session (True or False)?",
        choices=[
            [True, 'True'],
            [False, 'False']
        ]
    )
    Q6 = models.BooleanField(  # true
        label="6. Each Bystander is randomly paired with a Buyer in each round (True or False)?",
        choices=[
            [True, 'True'],
            [False, 'False']
        ]
    )
    Q7 = models.BooleanField(  # true
        label="7. The payment round will be determined randomly by the computer (True or False)?",
        choices=[
            [True, 'True'],
            [False, 'False']
        ]
    )
    Q80 = models.BooleanField(
        label="8. The instructions state that the Bystander does not make any decisions (True or False)?",
        choices=[
            [True, 'True'],
            [False, 'False']
        ],
    )
    Q81 = models.BooleanField(
        label="8. The instructions state that each time a Buyer buys a product, a Bystander’s payment is reduced by 50 points (True or False)?",
        choices=[
            [True, 'True'],
            [False, 'False']
        ],
    )
    Q82 = models.BooleanField(
        label="8. The instructions state that the Buyer and Seller profit at the expense of the Bystander (True or False)?",
        choices=[
            [True, 'True'],
            [False, 'False']
        ]
    )

    offer = models.BooleanField(
        choices=[
            [True, 'Yes'],
            [False, 'No']
        ],
        label="Do you wish to offer a product for sale this round?",
    )

    OfferNum = models.IntegerField()

    OfferTaken = models.IntegerField()

    BuyerNumber = models.IntegerField(initial=0)

    Seatnum2 = models.StringField(
        label="Confirm Seat"
    )

    Seatnum = models.StringField(
        label="Enter Seat"
    )

    pay = models.IntegerField(initial=0)

    isoffertaken = models.BooleanField(
        initial=False,
        choices=[
            [True, 'Yes'],
            [False, 'No']
        ]
    )
    hastakenoffer = models.BooleanField(
        initial=False,
        choices=[
            [True, 'Yes'],
            [False, 'No']
        ]
    )

    consent = models.BooleanField(
        choices=[
            [True, 'Yes'],
            [False, 'No']
        ],
        label="Do you consent?",
    )

    offerPrice = models.CurrencyField(
        min=0,
        max=50,
        doc="""Product pice""",
        label="At what price do you want to offer the product for sale?",
    )

    oprice = models.CurrencyField(
        min=0,
        max=50,
        doc="""Product price""",
        label="At what price do you want to offer the product for sale?",
    )

    guess_num_seller = models.IntegerField(
        min=0,
        max=1000,
        label="If you had instead been assigned the role of Seller, at what price would you offer the product for sale? (If you would not offer a product for sale at any price, please enter 999.)",
    )

    BoughtPrice = models.IntegerField(
        label="Price paid",
    )

    reward = models.TextField(
        label="reward",
        blank=True,
        null=True,
    )

    guess_num_buyer = models.IntegerField(
        min=0,
        max=1000,
        label="If you had instead been assigned the role of Buyer, what is the highest number of points you would pay to purchase the product? (If you would not purchase a product at any price, please enter 999.)",
    )

    def getOffer(self):
        # try:
        #    str_input = self.contribution
        #    numbers = [int(word)
        #               for word in str_input.split() if word.isdigit()]
        #    return numbers[0]
        # except:
        #    pass
        try:
            return self.offerPrice
        except:
            pass


# FUNCTIONS


def vars_for_admin_report(subsession: Subsession):
    pass

def view1(group: Group, request):
    if request.method == "POST":
        values_from_user = request.POST.getlist('my_list')
    reward = values_from_user


# PAGES


class Introduction(Page):
    """Description of the game: How to play and returns expected"""

    @staticmethod
    def vars_for_template(player):
        #print("vars")
        group = player.group
        participant = player.participant
        roundnumber = player.round_number - 1
        # participant.pay = set_payoffs(player.group)
        return dict(
            roundnumber=roundnumber,
        )
    @staticmethod
    def before_next_page(player, timeout_happened):  # sets base payoffs in RoleAssignment, should properly reset for each round
        #print("test")
        player.subsession.offersrem = 0
        if player.role == "Buyer":
            player.pay = 100  # base payoff
            a = np.linspace(1, len(player.subsession.get_groups()), len(player.subsession.get_groups()))
            random.shuffle(a)  ##randomizes order of assignment for buyer number
            #print(a)
            player.BuyerNumber = int(a[player.group.id_in_subsession - 1])
            for p in player.get_others_in_subsession():
                if p.role == "Buyer":
                    p.BuyerNumber = a[p.group.id_in_subsession - 1]
        if player.role == "Seller":
            player.pay = 100  # base payoff
        if player.role == "Bystander":
            player.pay = 50  # needs rework


class ShuffleWaitPage(WaitPage):
    wait_for_all_groups = True

    @staticmethod
    def after_all_players_arrive(subsession):
        # subsession.group_randomly(fixed_id_in_group=True)
        pass


class DisplayRoleAssignment(Page):
    """Description of the game: How to play and returns expected"""

    @staticmethod
    def is_displayed(player):
        return player.round_number == 1
    pass


class OfferM(Page):
    """Player: Choose whether to make an offer"""
    form_model = 'player'
    form_fields = ['offer', 'OfferNum'
                            'guess_num_seller', 'guess_num_buyer']

    @staticmethod
    def get_form_fields(player):
        if player.role == 'Seller':
            return ['offer']
        elif player.role == 'Bystander':
            return ['guess_num_seller', 'guess_num_buyer']

    @staticmethod
    def before_next_page(player, timeout_happened):
        #print(player)
        if player.role == 'Seller':
            if player.offer == 1:
                player.subsession.offersrem = player.subsession.offersrem + 1
                #print(player)
                player.OfferNum = player.subsession.offersrem
            else:
                player.OfferNum = 0

    @staticmethod
    def is_displayed(player):
        return (player.role == 'Seller' or player.role == 'Bystander')


class OfferAM(Page):
    form_model = 'player'
    form_fields = ['offerPrice']

    @staticmethod
    def is_displayed(player):
        if player.role == 'Seller':
            return (player.OfferNum > 0)
        else:
            return False
    @staticmethod
    def before_next_page(player, timeout_happened):
        if player.offerPrice is None:
            player.offer = 0


class OfferWaitPage(WaitPage):
    wait_for_all_groups = True
    body_text = "Please wait until the study continues."


class BuyerAcceptancePage(Page):
    form_model = 'player'
    @staticmethod
    def is_displayed(player):
        if player.subsession.bnum <= player.subsession.numbuyers:
            return True
        else:
            return False
    news = dict()
    @staticmethod
    def live_method(player: Player, number):
        buyer_id = player.group.id_in_subsession
        player.OfferTaken = number
        #print(player.subsession.numbuyers)
        print('!!!!received a bid from', player.id_in_group, ':', number)
        #print('bnum', player.subsession.bnum, "numb", player.subsession.numbuyers)
        player.OfferTaken = number
        #print("onum", player.OfferTaken)
        if player.role == "Buyer":
            if player.OfferTaken >= 0 and player.BuyerNumber == player.subsession.bnum:  # after buyer takes action
                player.subsession.bnum = player.subsession.bnum + 1
                for p in player.get_others_in_subsession():
                    if p.role == "Seller" and p.offer > 0:
                        if p.role == "Seller" and player.OfferTaken == p.OfferNum:
                            print("Offer Taken")
                            player.BoughtPrice = int(p.offerPrice)
                            player.hastakenoffer = True
                            p.isoffertaken = 1
        else:
            news = dict(buyer_id=buyer_id, number=number)
            return {0: dict(
                game_over=player.subsession.game_finished,
                news=news,
            )}
        news = dict(buyer_id=buyer_id, number=number)
        if player.subsession.bnum > player.subsession.numbuyers:
            #print("i")
            player.subsession.game_finished = True
            response = dict(type='game_finished')
            print("n", news)
            print("returnend")
        else:
            player.subsession.game_finished = False
        print("return")
        return {0: dict(
            game_over=player.subsession.game_finished,
            news=news,
        )}
        #print("return2")


    # @ staticmethod
    # def before_next_page(player, timeout_happened): #sets base payoffs in RoleAssignment, should properly reset for each round
    # @staticmethod
    # def vars_for_template(subsession):
    #     offers = []
    #     for p in subsession.get_others_in_subsession():
    #         try:
    #             offers.append(p.contribution)
    #         except:
    #             pass

    #     offerDict = {i: offers[i] for i in range(0, len(offers))}

    #     return offerDict

    # try:
    #    return dict(offer=player.contribution)
    # except:
    #    return dict(offer="Did not offer a product")



class ResultsOne(Page):
    """Players payoff: How much each has earned"""
    form_model = 'player'
    form_fields = ['reward']
    #print("Result")
    """Players payoff: How much each has earned"""
    #print("payoff")

    @staticmethod
    def vars_for_template(player: Player):
        #print("vars")
        group = player.group
        participant = player.participant
        # participant.pay = set_payoffs(player.group)
        try:
            return dict(player.pay)
        except:
            pass


#class ResultsWaitPage(WaitPage):
#    body_text = "Waiting for other participants to contribute."


class Results(Page):
    @staticmethod
    def vars_for_template(player: Player):
        group = player.group


class Launch(Page):
    @staticmethod
    def is_displayed(player):
        return player.round_number == 1


class StartDemo(Page):
    form_model = 'player'

    @staticmethod
    def get_form_fields(player):
        if player.treatment == 0:
            return ['Q1a', 'Q1b', 'Q1c', 'Q2a', 'Q3', 'Q4', 'Q5', 'Q6', 'Q7', 'Q80']
        if player.treatment == 1:
            return ['Q1a', 'Q1b', 'Q1c', 'Q2a', 'Q3', 'Q4', 'Q5', 'Q6', 'Q7', 'Q81']
        if player.treatment == 2:
            return ['Q1a', 'Q1b', 'Q1c', 'Q2a', 'Q3', 'Q4', 'Q5', 'Q6', 'Q7', 'Q82']

    @staticmethod
    def is_displayed(player):
        return player.round_number == 1


class QResults(Page):
    form_model = 'player'

    @staticmethod
    def is_displayed(player):
        return player.round_number == 1

    @staticmethod
    def before_next_page(player, timeout_happened):
        if player.Q1a == 125:
            player.QCorrect = player.QCorrect + 1
        if player.Q1b == 125:
            player.QCorrect = player.QCorrect + 1
        if player.Q1c == 50:
            player.QCorrect = player.QCorrect + 1
        if player.Q2a == 100:
            player.QCorrect = player.QCorrect + 1
        if player.Q3 == 50:
            player.QCorrect = player.QCorrect + 1
        if player.Q4 == False:
            player.QCorrect = player.QCorrect + 1
        if player.Q5 == False:
            player.QCorrect = player.QCorrect + 1
        if player.Q6 == False:
            player.QCorrect = player.QCorrect + 1
        if player.Q7 == True:
            player.QCorrect = player.QCorrect + 1
        if player.treatment == 0:
            if player.Q80 == True:
                player.QCorrect = player.QCorrect + 1
        if player.treatment == 1:
            if player.Q81 == True:
                player.QCorrect = player.QCorrect + 1
        if player.treatment == 2:
            if player.Q82 == True:
                player.QCorrect = player.QCorrect + 1


class Practice(Page):
    form_model = 'player'
    @staticmethod
    def is_displayed(player):
        return player.round_number == 1


class Seat(Page):
    form_model = 'player'
    form_fields = ['Seatnum', 'Seatnum2']

    @staticmethod
    def is_displayed(player):
        return player.round_number == 1

    def before_next_page(player: Player, timeout_happened):
        player.Seatfinal = player.Seatnum


class SeatCon(Page):
    form_model = 'player'
    form_fields = ['Seatfinal']

    @staticmethod
    def is_displayed(player):
        if player.round_number == 1:
            return player.Seatnum != player.Seatnum2
        else:
            return False

class FinalPay(Page):
    form_model = 'player'

    @staticmethod
    def is_displayed(player):
        return player.round_number == Constants.num_rounds
    @staticmethod
    def vars_for_template(player):
        p1 = player.in_round(1)
        #print("p1")
        #print(p1)
        ppay = player.in_round(player.subsession.payround)
        #print(ppay)
        player.payroundpay = ppay.pay
        player.Seatfinal = p1.Seatfinal
        player.QCorrect = p1.QCorrect
        player.finalpay = ppay.pay + (1 * p1.QCorrect) + 50
        Qpay = p1.QCorrect
        a = player.participant.code
        Ppay = ppay.pay
        seat = p1.Seatfinal
        #print("seat")
        #print(seat)
        return dict(
            code=a,
            Qpay=Qpay,
            Ppay=Ppay,
            seat=seat,
        )
        #print(ppay)


def set_round_payoffs(subsession: Player):
    #print("payp")
    #print(subsession.get_players())
    for p in subsession.get_players():
        if p.role == "Seller":
            if p.isoffertaken:
                p.pay = p.pay + int(p.offerPrice)  # base payoff
        if p.role == "Bystander":
            p.pay = 100
            for pl in p.get_others_in_group():
                if (pl.role == "Buyer" and pl.hastakenoffer == True):
                    p.pay = 50
        if p.role == "Buyer":
            if p.hastakenoffer == True:
                p.pay = p.pay + 50 - p.BoughtPrice


class BuyWaitPage(WaitPage):
    wait_for_all_groups = True
    after_all_players_arrive = set_round_payoffs
    body_text = "Please wait until the study continues."
    after_all_players_arrive = 'set_round_payoffs'



page_sequence = [Seat, SeatCon, Launch, Introduction, StartDemo, QResults, ShuffleWaitPage, Practice,
                 DisplayRoleAssignment, OfferWaitPage,
                 OfferM, OfferAM, OfferWaitPage, BuyerAcceptancePage, BuyWaitPage, ResultsOne, FinalPay]
