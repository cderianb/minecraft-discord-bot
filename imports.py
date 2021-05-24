# https://crt.sh/?id=2835394 -> SSL Certificate if needed
import os
import random
import sys
import discord
import asyncpg
import multiprocessing
import time
import yagmail

from dotenv import load_dotenv
from discord.ext import commands
