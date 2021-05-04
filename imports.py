# https://crt.sh/?id=2835394 -> SSL Certificate if needed
import os
import random
import discord
import asyncpg

from dotenv import load_dotenv
from discord.ext import commands
from flask import Flask

from constant import *