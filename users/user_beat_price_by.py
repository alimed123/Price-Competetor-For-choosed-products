import logging

from helpers.substring_processor import remove_special_char_except_dot

def beat_price_by(lowest_price, beat_price_by_perc, beat_price_by_dollar):

  beat_price_result = 0

  x = remove_special_char_except_dot(beat_price_by_perc)
  y = remove_special_char_except_dot(beat_price_by_dollar)

  if (beat_price_by_perc):
    beat_price_result = lowest_price * (100 - float(x))/100
  else:
    if (beat_price_by_dollar):
      beat_price_result = lowest_price - float(y)
    else:
      logging.info("Please provide us with either Beat Price by '%' or Beat Price by Dollar.")

  return beat_price_result