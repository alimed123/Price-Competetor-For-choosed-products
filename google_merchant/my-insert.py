from __future__ import print_function
import sys
import logging

# The common module provides setup functionality used by the samples,
# such as authentication and unique id generation.
from shopping.content import common

# offer_id = 'book#%s' % common.get_unique_id()
offer_id = '2472'
product = {
      'offerId':
        offer_id,
      'channel': 'online',
      'contentLanguage': 'en',
      'targetCountry': 'AU',
      'mpn':
        'RB-ILLUMINATE-i360-V',
      'customLabel0': 'RB-ILLUMINATE-i360-V',
      'brand':
        'Railblaza',
      'condition':
        'new',
      'availability':
        'In Stock',
      'identifierExists':
        'yes',
      'salePrice': {
         'value': '74.95',
         'currency': 'AUD'
      },
      'price': {
         'value': '84',
         'currency': 'AUD'
      },
      'id':
        '2472',
      'link':
        'https://www.kayaks2fish.com/railblaza-illuminate-i360',
      'title':
        'Railblaza Illuminate i360 - Kayaks2Fish - Afterpay Zippay Available',
      'imageLink':
        'https://www.kayaks2fish.com/assets/full/RB-ILLUMINATE-i360-V.jpg',
      'description':
        'Railblaza Illuminate i360 Railblaza Illuminate i360 Introducing the Railblaza Illuminate i360 your ultimate solution for safe and convenient maritime adventures. This navigation light is packed with features that make it stand out from other lights in its class. With powerful Nichia LED Hela Optics and highefficiency digital circuitry this package has been approved by the US Coast Guard to a range of 2nm or more! The product runs on AA battery power without the need for external wiring or switching thanks to its compatibility with any Railblaza StarPort mount. This makes installation quick and easy while maximizing battery life. The IP67 rating ensures dustproofing as well as water ingress protection so you can be sure it will float if accidentally dropped overboard. It meets all required standards for an allaround white navigation light suitable for powerboats and sailboats under 12 meters. Made from UVstabilized fibreglass reinforced plastic this lightweight product is durable enough to withstand harsh marine environments without compromising quality performance standards of such an essential safety device onboard kayaks canoes boats etc. In conclusion the Railblaza Illuminate i360 not only provides a highquality navigational lighting solution but also offers convenience through its compatibility with any RailBlaza StarPort mount allowing it to be mounted just about anywhere on your vessel. Powered by three AA batteries it delivers longlasting illumination hours making every dollar spent worthwhile. So why wait? Get yours today! Features: HighEfficiency Components: Equipped with a powerful Niche power LED Hela Optics and highefficiency digital circuit this nav light offers quality and longevity for every voyage. IP67 Rating: It ensures dust and water ingress protection. In addition it is designed to float if accidentally dropped overboard providing an added level of safety. Easy Powering: Running on AA batteries theres no need for additional wiring or tricky switches making it simple and straightforward to install and use. Three Operating Modes: Choose from high medium and blinking modes to suit your needs at any given time. Long Battery Life: Depending on usage the battery life can last from 25 to over 200 hours with new batteries (batteries sold separately). Durable Material: Made from UVstabilised fibreglass reinforced plastic the i360 is built to withstand the harsh marine environment. Specifications: Brand: Railblaza SKU: RBILLUMINATEi360V MPN: 025004 11 UPC: 9421026833143 Material Composition: UV Stabilised Fiberglass Reinforced Plastic Weight: 9 g Length: 126 mm (5 in) Width: 0.60 mm (2.36 in) Power Source: AA batteries (not included) Mount Compatibility: RAILBLAZA StarPort SidePort RIBPort RailMount Protection Rating: IP67 Regulatory Approval: US Coast Guard approved Lighting Modes: High Medium Blinking Battery Life: 25 to over 200 hours (based on usage) Package Includes: 1 x i360 light (batteries not included) Warning & Disclaimer: Caution: Always follow local laws and regulations regarding navigation lights and safety equipment. Secure Mounting: Ensure proper and secure mounting of the i360 to your kayak or equipment. Visibility: The product is an allround white navigation light but it may not provide sufficient visibility in all conditions. Always exercise caution and maintain a lookout while on the water. Battery Life: The battery life of the i360 varies depending on usage. Make sure to monitor and replace the batteries as needed to maintain optimal performance. Compatibility: Ensure compatibility between the product and your mounting system or base before installation. Disclaimer: The i360 is designed to provide reliable navigation lighting but it has its limitations. It is the users responsibility to ensure proper installation secure attachment and compliance with local regulations. Railblaza is not liable for any damage injury or legal consequences resulting from the misuse improper installation or failure to comply with navigation light regulations.',
      'googleProductCategory':
         'Sporting Goods > Outdoor Recreation > Boating & Water Sports > Boating & Rafting > Kayak Accessories',
      'shippingLabel': 'postagepaid',
      'shippingWeight': {
         'value': '200',
         'unit': 'grams'
      },
      'gtin':
        '9421026833143',
}

def main(argv):
  # Construct the service object to interact with the Content API.
  service, config, _ = common.init(argv, __doc__)

  # Get the merchant ID from merchant-info.json.
  merchant_id = config['merchantId']

  # Create the request with the merchant ID and product object.
  request = service.products().insert(merchantId=merchant_id, body=product)

  # Execute the request and print the result.
  result = request.execute()
  logging.info('Product with offerId "%s" was created.', result['offerId'])

# Allow the function to be called with arguments passed from the command line.
if __name__ == '__main__':
  main(sys.argv)