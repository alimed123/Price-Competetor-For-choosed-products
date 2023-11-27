import pandas as pd
import numpy as np
import datetime
import sys
import os
import os.path
import csv
import json
import re

item1 = [
    "RBD-ADJ-PLATFORM-BLK",
    "RBD-ADJ-PLATFORM-BLK",
    "RBD-ADJ-PLATFORM-BLK",
    "RBD-ADJ-PLATFORM-BLK",
    "RBD-ADJ-PLATFORM-BLK",
    "RBD-ADJ-PLATFORM-BLK",
    "RBD-ADJ-PLATFORM-BLK"
]
item2 = [
    "https://www.kayaks2fish.com/railblaza-adjustable-platform-delivered",
    "https://www.kayaks2fish.com/railblaza-adjustable-platform-delivered",
    "https://www.kayaks2fish.com/railblaza-adjustable-platform-delivered",
    "https://www.kayaks2fish.com/railblaza-adjustable-platform-delivered",
    "https://www.kayaks2fish.com/railblaza-adjustable-platform-delivered",
    "https://www.kayaks2fish.com/railblaza-adjustable-platform-delivered",
    "https://www.kayaks2fish.com/railblaza-adjustable-platform-delivered"
]
item3 = [
    "25",
    "25",
    "25",
    "25",
    "25",
    "25",
    "25",
]
item4 = [
    "23.004",
    "23.004",
    "23.004",
    "23.004",
    "23.004",
    "23.004",
    "23.004"
]
item5 = [
    "PAID",
    "PAID",
    "PAID",
    "PAID",
    "PAID",
    "PAID",
    "PAID",
]
item6 = [
    "https://www.arnoldsboatshop.com.au/products/railblaza-adjustable-platform",
    "https://www.outbackequipment.com.au/adjustable-platform-black",
    "https://www.theboatwarehouse.com.au/deck-fittings-hardware/mounting-systems/railblaza-adjustable-platform-only/",
    "https://www.biasboating.com.au/products/railblaza-adjustable-platform",
    "https://www.ebay.com.au/itm/234831384065",
    "https://www.freaksports.com.au/product/railblaza-adjustable-platform-black/",
    "https://www.arnoldsboatshop.com.au/products/railblaza-adjustable-platform-starport-kit"
]

other_item = [
    "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Phasellus ultrices, purus vel dictum varius, ante neque ullamcorper neque, pretium varius dui diam vel sem. Etiam nibh lorem, commodo at porttitor eget, pellentesque vitae leo. Curabitur molestie at turpis et consequat. Sed suscipit, est id dignissim porta, libero sapien sagittis augue, non condimentum urna mauris quis justo. Etiam lectus lacus, semper eu consectetur id, ultricies eget dui. Aliquam ligula nisi, feugiat dapibus lorem a, imperdiet varius sem. Morbi pharetra magna sed massa ultricies tempor. Ut in massa magna. Phasellus a dignissim tortor.",
    "Phasellus hendrerit sem at metus commodo, et sollicitudin mauris vehicula. Ut sodales laoreet dictum. Vestibulum porttitor molestie lectus consequat faucibus. Nullam eros neque, consectetur tristique nisl sit amet, dictum ultrices ante. Aenean consequat nibh vitae leo ullamcorper, non volutpat dolor venenatis. Ut non sapien tellus. Nullam aliquet auctor sem, sed rutrum dolor varius quis. Maecenas in dignissim neque. Integer sed fringilla purus. Curabitur venenatis massa efficitur convallis malesuada. Suspendisse sit amet suscipit urna, in sollicitudin augue. Fusce eu scelerisque ante, cursus sollicitudin turpis. Nulla et purus eget neque tempor malesuada. Praesent quam mauris, convallis nec tempor sed, ullamcorper in augue. Quisque pretium turpis vitae posuere congue. Nam eget ex eget augue bibendum posuere.",
    "Nunc quis nibh erat. Donec interdum, nisl quis cursus porta, urna lectus aliquam arcu, sit amet consequat elit ante quis sapien. Etiam nec nunc sed massa tincidunt viverra eget eu neque. Duis id orci nibh. Pellentesque tellus velit, lobortis ac faucibus sit amet, cursus sed orci. Vestibulum nec blandit lorem. Ut luctus suscipit elit. Ut mollis lorem vel hendrerit mollis. Praesent cursus ex iaculis turpis finibus fringilla. Proin ac luctus magna. Aliquam eu neque neque. Ut et mattis turpis, vitae gravida sem. Aliquam lacinia ac ipsum ac porttitor."
]

def save_to_xsl(item1, item2, item3, item4, item5, item6, other_item):
  print('Silence is Golden.')