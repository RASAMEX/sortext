from collections import Counter
import secrets
from .models import Raffle, Participant
import random
import os

from .custom_logger import setup_logger

class LotteryDraw:
    """
    Class to manage the raffle drawing process.

    Attributes:
        raffle (Raffle): The raffle for which the draw is being conducted.
        participant_list (list): List of participants currently in the raffle.
        repeated_ids (list): List of participant IDs based on the number of valid tickets.
        repeated_names (list): List of participant names based on the number of valid tickets.
    """

    def __init__(self, raffle_id):
        """
        Initialize the LotteryDraw with a specific raffle.

        Args:
            raffle_id (int): The ID of the raffle.
        """
        self.raffle = Raffle.objects.get(pk=raffle_id)
        
        self.logger = setup_logger(__name__)
        
        self.logger.info("Raffle ID: " + str(self.raffle.pk))
        
    def load_data(self):
        """
        Load participants who are currently participating in the raffle.
        """
        participating_participants = Participant.objects.filter(raffle=self.raffle.pk, status='Participating')
        self.participant_list = list(participating_participants.values())
        self.logger.info("Participants List: " + str(self.participant_list))
        
    def sorter_list(self):
        """
        Generate lists of participant IDs and names based on the number of valid tickets.

        Returns:
            list: List of participant IDs repeated according to the number of valid tickets.
        """
        self.repeated_ids = [obj['id'] for obj in self.participant_list for _ in range(obj['valid_tickets'])]
        self.repeated_names = [obj['name'] for obj in self.participant_list for _ in range(obj['valid_tickets'])]
        self.logger.info("Repeated ID: " + str(self.repeated_ids))
        return self.repeated_ids
    
    def soft_draw_exec(self, invested=False, two_three=False):
        """
        Execute a soft draw with the option for invested or two-three draw logic.

        Args:
            invested (bool): Flag to use inverted weighted random number generator.
            two_three (bool): Flag to determine if two out of three logic should be used.

        Returns:
            dict: Results of the draw including participating participants, selected indices, and the winner.
        """
        if invested:
            random_index1 = self.generate_inverted_weighted_random_number()
            random_index2 = self.generate_inverted_weighted_random_number()
            random_index3 = self.generate_inverted_weighted_random_number()
        else:
            random_index1 = self.generate_weighted_random_number()
            random_index2 = self.generate_weighted_random_number()
            random_index3 = self.generate_weighted_random_number()
         
        winner = self.apply_result(random_index1, random_index2, random_index3, invested, two_three)
        self.logger.info("soft_draw_exec")
        return {
            "participating": self.participant_list,
            "lane1": random_index1,
            "lane2": random_index2, 
            "lane3": random_index3,
            "winner": winner
        }
        
    def half_draw_exec(self, invested=False, two_three=False):
        """
        Execute a half draw with the option for invested or two-three draw logic.

        Args:
            invested (bool): Flag to use inverted weighted random number generator.
            two_three (bool): Flag to determine if two out of three logic should be used.

        Returns:
            dict: Results of the draw including participating participants, selected indices, and the winner.
        """
        if invested:
            random_index1 = self.generate_inverted_weighted_random_number()
            random_index2 = self.generate_inverted_weighted_random_number()
        else:
            random_index1 = self.generate_weighted_random_number()
            random_index2 = self.generate_weighted_random_number()

        random_index3 = self.generate_random_number(0, len(self.repeated_ids) - 1)
        value3 = self.repeated_ids[random_index3]
        winner = self.apply_result(random_index1, random_index2, value3, invested, two_three)
        self.logger.info("half_draw_exec")
        return {
            "participating": self.participant_list,
            "lane1": random_index1,
            "lane2": random_index2, 
            "lane3": value3,
            "winner": winner
        }
    
    def hard_draw_exec(self, invested=False, two_three=False):
        """
        Execute a hard draw with the option for invested or two-three draw logic.

        Args:
            invested (bool): Flag to use inverted weighted random number generator.
            two_three (bool): Flag to determine if two out of three logic should be used.

        Returns:
            dict: Results of the draw including participating participants, selected indices, and the winner.
        """
        random_index1 = random.randint(0, len(self.repeated_ids) - 1)
        random_index2 = secrets.randbelow(len(self.repeated_ids) - 1)
        random_index3 = self.generate_random_number(0, len(self.repeated_ids) - 1)
        
        value1 = self.repeated_ids[random_index1]
        value2 = self.repeated_ids[random_index2]
        value3 = self.repeated_ids[random_index3]
        winner = self.apply_result(value1, value2, value3, invested, two_three)
        self.logger.info("hard_draw_exec")
        return {
            "participating": self.participant_list,
            "lane1": value1,
            "lane2": value2, 
            "lane3": value3,
            "winner": winner
        }
    
    def generate_random_number(self, minimum, maximum):
        """
        Generate a random number between minimum and maximum.

        Args:
            minimum (int): Minimum value for the random number.
            maximum (int): Maximum value for the random number.

        Returns:
            int: Random number within the specified range.
        """
        random_bytes = os.urandom(8)  # Get 8 bytes (64 bits) for sufficient randomness
        random_number = int.from_bytes(random_bytes, byteorder="big")
        scaled_number = minimum + (random_number % (maximum - minimum + 1))
        return scaled_number   

    def generate_weighted_random_number(self):
        """
        Generate a weighted random number based on ticket frequencies.

        Returns:
            int: Weighted random number.
        """
        frequencies = Counter(self.repeated_ids)
        weighted = []
        for number, frequency in frequencies.items():
            weighted.extend([number] * frequency)
        random_number = random.choice(weighted)
        return random_number
    
    def generate_inverted_weighted_random_number(self):
        """
        Generate an inverted weighted random number.

        Returns:
            int: Inverted weighted random number.
        """
        frequencies = Counter(self.repeated_ids)
        weighted = []
        total_elements = len(self.repeated_ids)
        for number, frequency in frequencies.items():
            probability = 1 - (frequency / total_elements)
            times_to_add = int(probability * total_elements)
            weighted.extend([number] * times_to_add)
        random_number = random.choice(weighted)
        return random_number

    def apply_result(self, r1, r2, r3, invested=False, two_three=False):
        """
        Apply the draw result and determine the winner.

        Args:
            r1 (int): First selected index.
            r2 (int): Second selected index.
            r3 (int): Third selected index.
            invested (bool): Flag to update participant tickets.
            two_three (bool): Flag to determine if two out of three logic should be used.

        Returns:
            int: Winning participant ID.
        """
        if two_three:
            if r1 == r2 or r1 == r3:
                if invested:
                    self.update_table(r1)
                return r1
            elif r2 == r3:
                if invested:
                    self.update_table(r2)
                return r2
        else:
            if r1 == r2 == r3:
                if invested:
                    self.update_table(r1)
                return r1
    
    def update_table(self, r1):
        """
        Update the participant's ticket counts and status.

        Args:
            r1 (int): Participant ID to be updated.
        """
        participants = Participant.objects.filter(pk=r1)
        if participants.exists():
            participant = participants.first()
            participant.valid_tickets -= 1
            participant.invalid_tickets += 1
            if participant.valid_tickets == 0:
                participant.status = 'Disqualified'
            participant.save()