#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from __future__ import absolute_import
from wit import Wit

access_token = "JHWJFTAHCTPVARBLGMDRO5AV5OM5BIVV"
curl = "https://api.wit.ai/message?v=20190330&q="

free_text = [
    "spec",
    "dentist",
    "schedule",
    "location",
    "book",
    "cancel",
    "cancelID",
]

def ChatBotQuery(message):
    client = Wit(access_token)
    resp = client.message(message)
    intent = resp["entities"]["Intent"][0]["value"]
    name = None
    start = None
    if intent in free_text:
        name = resp["entities"]["name"][0]["value"]
    if intent == "book" or intent == "cancel":
        start = resp["entities"]["start"][0]["value"]
    context = {
        'intent': intent,
        'value': name,
        'start': start,
    }
    return context
