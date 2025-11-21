# Dead Horizon - Text Based Zombie Apocalypse Survival Game
import json
import os
import random
from dataclasses import dataclass, field, asdict

# Config & Balancing

Sectors_To_Evac = 20        # reach this many sectors to get to evacuation
Move_Sectors_Range = (1,3)  # number of sectors you move when relocating
Survivor_Size_Range = (2,5)

Initial_Supplies = {'food': 200, 'water': 150, 'medkits': 3, 'antivirals': 3, 'materials': 15, 'ammo': 40}

Consumption_Per_Survivor_Per_Day = {'food': 2, 'water': 2}

Base_Max_Integrity = 10
Rest_Heal = 1
Fortify_Boost = (1,3)
Max_Health = 10

Horde_Base_Chance = 0.18
Infection_Tick_Chance = 0.10
Good_Event_Chance = 0.17
Raider_Chance = 0.12

Save_File = "Dead-Horizon_save.json"

# Data Models

@dataclass
class Survivor:
    name: str