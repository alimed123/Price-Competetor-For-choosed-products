import json

global found_target

item = [
  {
    "@context": "https://schema.org",
    "@graph": [
      {
        "@type": "Place",
        "@id": "https://www.freaksports.com.au/#place",
        "address": {
          "@type": "PostalAddress",
          "streetAddress": "2/11 Lensworth Street",
          "addressLocality": "Coopers Plains",
          "addressRegion": "Queensland",
          "postalCode": "4108",
          "addressCountry": "AU"
        }
      },
      {
        "@type": [
          "SportingGoodsStore",
          "Organization"
        ],
        "@id": "https://www.freaksports.com.au/#organization",
        "name": "Freak Sports Australia",
        "url": "https://www.freaksports.com.au",
        "sameAs": [
          "https://www.facebook.com/FreakSports",
          "https://twitter.com/freaksportsaus",
          "http://instagram.com/freaksportsaus",
          "https://au.linkedin.com/company/freak-sports-australia",
          "https://au.pinterest.com/freaksportsaust/",
          "https://www.youtube.com/user/TheFreakSports"
        ],
        "address": {
          "@type": "PostalAddress",
          "streetAddress": "2/11 Lensworth Street",
          "addressLocality": "Coopers Plains",
          "addressRegion": "Queensland",
          "postalCode": "4108",
          "addressCountry": "AU"
        },
        "logo": {
          "@type": "ImageObject",
          "@id": "https://www.freaksports.com.au/#logo",
          "url": "https://www.freaksports.com.au/wp-content/uploads/2020/02/Freak-Sports-Logo-1302-2020-dark-400x90-1.png",
          "contentUrl": "https://www.freaksports.com.au/wp-content/uploads/2020/02/Freak-Sports-Logo-1302-2020-dark-400x90-1.png",
          "caption": "Freak Sports Australia",
          "inLanguage": "en-AU",
          "width": "400",
          "height": "90"
        },
        "priceRange": "$$$",
        "openingHours": [
          "Monday,Tuesday,Wednesday,Thursday,Friday 09:00-16:30",
          "Saturday 09:00-15:00",
          "Sunday Closed"
        ],
        "location": {
          "@id": "https://www.freaksports.com.au/#place"
        },
        "image": {
          "@id": "https://www.freaksports.com.au/#logo"
        },
        "telephone": "1300 437 325"
      },
      {
        "@type": "WebSite",
        "@id": "https://www.freaksports.com.au/#website",
        "url": "https://www.freaksports.com.au",
        "name": "Freak Sports Australia",
        "publisher": {
          "@id": "https://www.freaksports.com.au/#organization"
        },
        "inLanguage": "en-AU"
      },
      {
        "@type": "ImageObject",
        "@id": "https://www.freaksports.com.au/wp-content/uploads/2018/12/Railblaza-Adjustable-Extender-R-Lock-800x800.jpg",
        "url": "https://www.freaksports.com.au/wp-content/uploads/2018/12/Railblaza-Adjustable-Extender-R-Lock-800x800.jpg",
        "width": "800",
        "height": "800",
        "caption": "Railblaza Adjustable Extender R-Lock",
        "inLanguage": "en-AU"
      },
      {
        "@type": "BreadcrumbList",
        "@id": "https://www.freaksports.com.au/product/railblaza-adjustable-extender-r-lock/#breadcrumb",
        "itemListElement": [
          {
            "@type": "ListItem",
            "position": "1",
            "item": {
              "@id": "https://www.freaksports.com.au",
              "name": "FreakSports"
            }
          },
          {
            "@type": "ListItem",
            "position": "2",
            "item": {
              "@id": "https://www.freaksports.com.au/shop/kayak-accessories/",
              "name": "Kayak Accessories"
            }
          },
          {
            "@type": "ListItem",
            "position": "3",
            "item": {
              "@id": "https://www.freaksports.com.au/shop/kayak-accessories/railblaza-accessories/",
              "name": "Railblaza Accessories"
            }
          },
          {
            "@type": "ListItem",
            "position": "4",
            "item": {
              "@id": "https://www.freaksports.com.au/product/railblaza-adjustable-extender-r-lock/",
              "name": "Railblaza Adjustable Extender R-Lock"
            }
          }
        ]
      },
      {
        "@type": "ItemPage",
        "@id": "https://www.freaksports.com.au/product/railblaza-adjustable-extender-r-lock/#webpage",
        "url": "https://www.freaksports.com.au/product/railblaza-adjustable-extender-r-lock/",
        "name": "Railblaza Adjustable Extender R-Lock - Freak Sports Australia",
        "datePublished": "2018-12-20T20:27:02+10:00",
        "dateModified": "2023-08-01T13:24:31+10:00",
        "isPartOf": {
          "@id": "https://www.freaksports.com.au/#website"
        },
        "primaryImageOfPage": {
          "@id": "https://www.freaksports.com.au/wp-content/uploads/2018/12/Railblaza-Adjustable-Extender-R-Lock-800x800.jpg"
        },
        "inLanguage": "en-AU",
        "breadcrumb": {
          "@id": "https://www.freaksports.com.au/product/railblaza-adjustable-extender-r-lock/#breadcrumb"
        }
      },
      {
        "@type": "Product",
        "brand": {
          "@type": "Brand",
          "name": "Railblaza"
        },
        "name": "Railblaza Adjustable Extender R-Lock - Freak Sports Australia",
        "description": "With 2 rotating R-Lock friction joints and a knuckle joint that tilts in 15° increments, the Railblaza Adjustable Extender R-Lock adds great versatility.",
        "sku": "121741399",
        "category": "Kayak Accessories &gt; Railblaza Accessories",
        "mainEntityOfPage": {
          "@id": "https://www.freaksports.com.au/product/railblaza-adjustable-extender-r-lock/#webpage"
        },
        "weight": {
          "@type": "QuantitativeValue",
          "unitCode": "KGM",
          "value": "0.1"
        },
        "height": {
          "@type": "QuantitativeValue",
          "unitCode": "CMT",
          "value": "10"
        },
        "width": {
          "@type": "QuantitativeValue",
          "unitCode": "CMT",
          "value": "10"
        },
        "depth": {
          "@type": "QuantitativeValue",
          "unitCode": "CMT",
          "value": "10"
        },
        "offers": {
          "@type": "Offer",
          "price": "36.95",
          "priceCurrency": "AUD",
          "priceValidUntil": "2024-12-31",
          "availability": "https://schema.org/InStock",
          "itemCondition": "NewCondition",
          "url": "https://www.freaksports.com.au/product/railblaza-adjustable-extender-r-lock/",
          "seller": {
            "@type": "Organization",
            "@id": "https://www.freaksports.com.au/",
            "name": "Freak Sports Australia",
            "url": "https://www.freaksports.com.au",
            "logo": "https://www.freaksports.com.au/wp-content/uploads/2020/02/Freak-Sports-Logo-1302-2020-dark-400x90-1.png"
          },
          "priceSpecification": {
            "price": "36.95",
            "priceCurrency": "AUD",
            "valueAddedTaxIncluded": "True"
          }
        },
        "additionalProperty": [
          {
            "@type": "PropertyValue",
            "name": "pa_brand",
            "value": "Railblaza"
          },
          {
            "@type": "PropertyValue",
            "name": "pa_colour",
            "value": "Black"
          }
        ],
        "aggregateRating": {
          "@type": "AggregateRating",
          "ratingValue": "5",
          "ratingCount": "13"
        },
        "gtin13": "9421026833822",
        "mpn": "03-4144-11",
        "@id": "https://www.freaksports.com.au/product/railblaza-adjustable-extender-r-lock/#richSnippet",
        "image": {
          "@id": "https://www.freaksports.com.au/wp-content/uploads/2018/12/Railblaza-Adjustable-Extender-R-Lock-800x800.jpg"
        }
      }
    ]
  },
  {
    "is_registration_required": "",
    "is_logged_in": ""
  },
  {
    "visitorLoginState": "logged-out",
    "visitorType": "visitor-logged-out",
    "visitorRegistrationDate": "",
    "visitorUsername": "",
    "visitorIP": "164.90.205.52",
    "pageTitle": "Railblaza Adjustable Extender R-Lock - Freak Sports Australia",
    "pagePostType": "product",
    "pagePostType2": "single-product",
    "browserName": "Chrome",
    "browserVersion": "87.0.4280.101",
    "browserEngineName": "Blink",
    "browserEngineVersion": "",
    "osName": "OS X",
    "osVersion": "10.15.7",
    "deviceType": "desktop",
    "deviceManufacturer": "Apple",
    "deviceModel": "Macintosh",
    "postID": 39521,
    "customerTotalOrders": 0,
    "customerTotalOrderValue": "0.00",
    "customerFirstName": "",
    "customerLastName": "",
    "customerBillingFirstName": "",
    "customerBillingLastName": "",
    "customerBillingCompany": "",
    "customerBillingAddress1": "",
    "customerBillingAddress2": "",
    "customerBillingCity": "",
    "customerBillingPostcode": "",
    "customerBillingCountry": "",
    "customerBillingEmail": "",
    "customerBillingEmailHash": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
    "customerBillingPhone": "",
    "customerShippingFirstName": "",
    "customerShippingLastName": "",
    "customerShippingCompany": "",
    "customerShippingAddress1": "",
    "customerShippingAddress2": "",
    "customerShippingCity": "",
    "customerShippingPostcode": "",
    "customerShippingCountry": "",
    "cartContent": {
      "totals": {
        "applied_coupons": [],
        "discount_total": 0,
        "subtotal": 0,
        "total": 0
      },
      "items": []
    },
    "productRatingCounts": [],
    "productAverageRating": 0,
    "productReviewCount": 0,
    "productType": "simple",
    "productIsVariable": 0,
    "event": "gtm4wp.changeDetailViewEEC",
    "ecommerce": {
      "currencyCode": "AUD",
      "detail": {
        "products": [
          {
            "id": 39521,
            "name": "Railblaza Adjustable Extender R-Lock",
            "sku": "121741399",
            "category": "Mounts And Accessories",
            "price": 36.95,
            "stocklevel": 0,
            "brand": "Railblaza"
          }
        ]
      }
    }
  },
  {
    "handle_customer_state": "0"
  },
  {
    "i18n_required_rating_text": "Please select a rating",
    "review_rating_required": "yes",
    "flexslider": {
      "rtl": False,
      "animation": "slide",
      "smoothHeight": True,
      "directionNav": False,
      "controlNav": "thumbnails",
      "slideshow": False,
      "animationSpeed": 500,
      "animationLoop": False,
      "allowOneSlide": False
    },
    "zoom_enabled": "",
    "zoom_options": [],
    "photoswipe_enabled": "1",
    "photoswipe_options": {
      "shareEl": False,
      "closeOnScroll": False,
      "history": False,
      "hideAnimationDuration": 0,
      "showAnimationDuration": 0
    },
    "flexslider_enabled": ""
  },
  {
    "ajax_url": "/wp-admin/admin-ajax.php",
    "wc_ajax_url": "/?wc-ajax=%%endpoint%%"
  },
  {
    "ajax_url": "https://www.freaksports.com.au/wp-admin/admin-ajax.php"
  },
  {
    "tooltip_library": "hint"
  },
  {
    "title": "Credit Card (Stripe)",
    "key": "pk_live_51IacK1CANR3MzxjRy923laTMtKffKJV5w4CTtxYErnvajWUU9TgRxjL4zJZpzrCbRW3GWXNxJL0U4jcY93ecIktJ00Y2awWanK",
    "i18n_terms": "Please accept the terms and conditions first",
    "i18n_required_fields": "Please fill in required checkout fields first",
    "updateFailedOrderNonce": "5d589f5912",
    "updatePaymentIntentNonce": "f4373e2109",
    "orderId": "0",
    "checkout_url": "/?wc-ajax=checkout",
    "stripe_locale": "en",
    "no_prepaid_card_msg": "Sorry, we're not accepting prepaid cards at this time. Your credit card has not been charged. Please try with alternative payment method.",
    "no_sepa_owner_msg": "Please enter your IBAN account name.",
    "no_sepa_iban_msg": "Please enter your IBAN account number.",
    "payment_intent_error": "We couldn't initiate the payment. Please try again.",
    "sepa_mandate_notification": "email",
    "allow_prepaid_card": "yes",
    "inline_cc_form": "yes",
    "is_checkout": "no",
    "return_url": "https://www.freaksports.com.au/checkout/order-received/?utm_nooverride=1",
    "ajaxurl": "/?wc-ajax=%%endpoint%%",
    "stripe_nonce": "0cf096b148",
    "statement_descriptor": "FREAKSPORTS.COM.AU",
    "elements_options": [],
    "sepa_elements_options": {
      "supportedCountries": [
        "SEPA"
      ],
      "placeholderCountry": "NL",
      "style": {
        "base": {
          "fontSize": "15px"
        }
      }
    },
    "invalid_owner_name": "Billing First Name and Last Name are required.",
    "is_change_payment_page": "no",
    "is_add_payment_page": "no",
    "is_pay_for_order_page": "no",
    "elements_styling": "",
    "elements_classes": "",
    "add_card_nonce": "0ae45d6446",
    "create_payment_intent_nonce": "6e76fe13d1",
    "cpf_cnpj_required_msg": "CPF/CNPJ is a required field",
    "invalid_number": "The card number is not a valid credit card number.",
    "invalid_expiry_month": "The card's expiration month is invalid.",
    "invalid_expiry_year": "The card's expiration year is invalid.",
    "invalid_cvc": "The card's security code is invalid.",
    "incorrect_number": "The card number is incorrect.",
    "incomplete_number": "The card number is incomplete.",
    "incomplete_cvc": "The card's security code is incomplete.",
    "incomplete_expiry": "The card's expiration date is incomplete.",
    "expired_card": "The card has expired.",
    "incorrect_cvc": "The card's security code is incorrect.",
    "incorrect_zip": "The card's zip code failed validation.",
    "postal_code_invalid": "Invalid zip code, please correct and try again",
    "invalid_expiry_year_past": "The card's expiration year is in the past",
    "card_declined": "The card was declined.",
    "missing": "There is no card on a customer that is being charged.",
    "processing_error": "An error occurred while processing the card.",
    "invalid_sofort_country": "The billing country is not accepted by Sofort. Please try another country.",
    "email_invalid": "Invalid email address, please correct and try again.",
    "invalid_request_error": "Unable to process this payment, please try again or use alternative method.",
    "amount_too_large": "The order total is too high for this payment method",
    "amount_too_small": "The order total is too low for this payment method",
    "country_code_invalid": "Invalid country code, please try again with a valid country code",
    "tax_id_invalid": "Invalid Tax Id, please try again with a valid tax id"
  },
  {
    "title": "Railblaza Adjustable Extender R-Lock",
    "product_id": "39521",
    "variant_id": "39521",
    "url": "https://www.freaksports.com.au/product/railblaza-adjustable-extender-r-lock/",
    "image_url": "https://www.freaksports.com.au/wp-content/uploads/2018/12/Railblaza-Adjustable-Extender-R-Lock-800x800.jpg",
    "price": "36.95",
    "categories": [
      "Railblaza Accessories",
      "Extenders",
      "Kayak Accessories",
      "Kayak Accessories",
      "Mounts And Accessories"
    ]
  },
  {
    "countries": "{\"AU\":{\"ACT\":\"Australian Capital Territory\",\"NSW\":\"New South Wales\",\"NT\":\"Northern Territory\",\"QLD\":\"Queensland\",\"SA\":\"South Australia\",\"TAS\":\"Tasmania\",\"VIC\":\"Victoria\",\"WA\":\"Western Australia\"},\"AT\":[],\"BE\":[],\"BR\":{\"AC\":\"Acre\",\"AL\":\"Alagoas\",\"AP\":\"Amap\\u00e1\",\"AM\":\"Amazonas\",\"BA\":\"Bahia\",\"CE\":\"Cear\\u00e1\",\"DF\":\"Distrito Federal\",\"ES\":\"Esp\\u00edrito Santo\",\"GO\":\"Goi\\u00e1s\",\"MA\":\"Maranh\\u00e3o\",\"MT\":\"Mato Grosso\",\"MS\":\"Mato Grosso do Sul\",\"MG\":\"Minas Gerais\",\"PA\":\"Par\\u00e1\",\"PB\":\"Para\\u00edba\",\"PR\":\"Paran\\u00e1\",\"PE\":\"Pernambuco\",\"PI\":\"Piau\\u00ed\",\"RJ\":\"Rio de Janeiro\",\"RN\":\"Rio Grande do Norte\",\"RS\":\"Rio Grande do Sul\",\"RO\":\"Rond\\u00f4nia\",\"RR\":\"Roraima\",\"SC\":\"Santa Catarina\",\"SP\":\"S\\u00e3o Paulo\",\"SE\":\"Sergipe\",\"TO\":\"Tocantins\"},\"BG\":{\"BG-01\":\"Blagoevgrad\",\"BG-02\":\"Burgas\",\"BG-08\":\"Dobrich\",\"BG-07\":\"Gabrovo\",\"BG-26\":\"Haskovo\",\"BG-09\":\"Kardzhali\",\"BG-10\":\"Kyustendil\",\"BG-11\":\"Lovech\",\"BG-12\":\"Montana\",\"BG-13\":\"Pazardzhik\",\"BG-14\":\"Pernik\",\"BG-15\":\"Pleven\",\"BG-16\":\"Plovdiv\",\"BG-17\":\"Razgrad\",\"BG-18\":\"Ruse\",\"BG-27\":\"Shumen\",\"BG-19\":\"Silistra\",\"BG-20\":\"Sliven\",\"BG-21\":\"Smolyan\",\"BG-23\":\"Sofia District\",\"BG-22\":\"Sofia\",\"BG-24\":\"Stara Zagora\",\"BG-25\":\"Targovishte\",\"BG-03\":\"Varna\",\"BG-04\":\"Veliko Tarnovo\",\"BG-05\":\"Vidin\",\"BG-06\":\"Vratsa\",\"BG-28\":\"Yambol\"},\"CA\":{\"AB\":\"Alberta\",\"BC\":\"British Columbia\",\"MB\":\"Manitoba\",\"NB\":\"New Brunswick\",\"NL\":\"Newfoundland and Labrador\",\"NT\":\"Northwest Territories\",\"NS\":\"Nova Scotia\",\"NU\":\"Nunavut\",\"ON\":\"Ontario\",\"PE\":\"Prince Edward Island\",\"QC\":\"Quebec\",\"SK\":\"Saskatchewan\",\"YT\":\"Yukon Territory\"},\"CN\":{\"CN1\":\"Yunnan \\/ \\u4e91\\u5357\",\"CN2\":\"Beijing \\/ \\u5317\\u4eac\",\"CN3\":\"Tianjin \\/ \\u5929\\u6d25\",\"CN4\":\"Hebei \\/ \\u6cb3\\u5317\",\"CN5\":\"Shanxi \\/ \\u5c71\\u897f\",\"CN6\":\"Inner Mongolia \\/ \\u5167\\u8499\\u53e4\",\"CN7\":\"Liaoning \\/ \\u8fbd\\u5b81\",\"CN8\":\"Jilin \\/ \\u5409\\u6797\",\"CN9\":\"Heilongjiang \\/ \\u9ed1\\u9f99\\u6c5f\",\"CN10\":\"Shanghai \\/ \\u4e0a\\u6d77\",\"CN11\":\"Jiangsu \\/ \\u6c5f\\u82cf\",\"CN12\":\"Zhejiang \\/ \\u6d59\\u6c5f\",\"CN13\":\"Anhui \\/ \\u5b89\\u5fbd\",\"CN14\":\"Fujian \\/ \\u798f\\u5efa\",\"CN15\":\"Jiangxi \\/ \\u6c5f\\u897f\",\"CN16\":\"Shandong \\/ \\u5c71\\u4e1c\",\"CN17\":\"Henan \\/ \\u6cb3\\u5357\",\"CN18\":\"Hubei \\/ \\u6e56\\u5317\",\"CN19\":\"Hunan \\/ \\u6e56\\u5357\",\"CN20\":\"Guangdong \\/ \\u5e7f\\u4e1c\",\"CN21\":\"Guangxi Zhuang \\/ \\u5e7f\\u897f\\u58ee\\u65cf\",\"CN22\":\"Hainan \\/ \\u6d77\\u5357\",\"CN23\":\"Chongqing \\/ \\u91cd\\u5e86\",\"CN24\":\"Sichuan \\/ \\u56db\\u5ddd\",\"CN25\":\"Guizhou \\/ \\u8d35\\u5dde\",\"CN26\":\"Shaanxi \\/ \\u9655\\u897f\",\"CN27\":\"Gansu \\/ \\u7518\\u8083\",\"CN28\":\"Qinghai \\/ \\u9752\\u6d77\",\"CN29\":\"Ningxia Hui \\/ \\u5b81\\u590f\",\"CN30\":\"Macao \\/ \\u6fb3\\u95e8\",\"CN31\":\"Tibet \\/ \\u897f\\u85cf\",\"CN32\":\"Xinjiang \\/ \\u65b0\\u7586\"},\"CZ\":[],\"DK\":[],\"EE\":[],\"FI\":[],\"FR\":[],\"DE\":{\"DE-BW\":\"Baden-W\\u00fcrttemberg\",\"DE-BY\":\"Bavaria\",\"DE-BE\":\"Berlin\",\"DE-BB\":\"Brandenburg\",\"DE-HB\":\"Bremen\",\"DE-HH\":\"Hamburg\",\"DE-HE\":\"Hesse\",\"DE-MV\":\"Mecklenburg-Vorpommern\",\"DE-NI\":\"Lower Saxony\",\"DE-NW\":\"North Rhine-Westphalia\",\"DE-RP\":\"Rhineland-Palatinate\",\"DE-SL\":\"Saarland\",\"DE-SN\":\"Saxony\",\"DE-ST\":\"Saxony-Anhalt\",\"DE-SH\":\"Schleswig-Holstein\",\"DE-TH\":\"Thuringia\"},\"GR\":{\"I\":\"Attica\",\"A\":\"East Macedonia and Thrace\",\"B\":\"Central Macedonia\",\"C\":\"West Macedonia\",\"D\":\"Epirus\",\"E\":\"Thessaly\",\"F\":\"Ionian Islands\",\"G\":\"West Greece\",\"H\":\"Central Greece\",\"J\":\"Peloponnese\",\"K\":\"North Aegean\",\"L\":\"South Aegean\",\"M\":\"Crete\"},\"HK\":{\"HONG KONG\":\"Hong Kong Island\",\"KOWLOON\":\"Kowloon\",\"NEW TERRITORIES\":\"New Territories\"},\"HU\":{\"BK\":\"B\\u00e1cs-Kiskun\",\"BE\":\"B\\u00e9k\\u00e9s\",\"BA\":\"Baranya\",\"BZ\":\"Borsod-Aba\\u00faj-Zempl\\u00e9n\",\"BU\":\"Budapest\",\"CS\":\"Csongr\\u00e1d-Csan\\u00e1d\",\"FE\":\"Fej\\u00e9r\",\"GS\":\"Gy\\u0151r-Moson-Sopron\",\"HB\":\"Hajd\\u00fa-Bihar\",\"HE\":\"Heves\",\"JN\":\"J\\u00e1sz-Nagykun-Szolnok\",\"KE\":\"Kom\\u00e1rom-Esztergom\",\"NO\":\"N\\u00f3gr\\u00e1d\",\"PE\":\"Pest\",\"SO\":\"Somogy\",\"SZ\":\"Szabolcs-Szatm\\u00e1r-Bereg\",\"TO\":\"Tolna\",\"VA\":\"Vas\",\"VE\":\"Veszpr\\u00e9m\",\"ZA\":\"Zala\"},\"IS\":[],\"IN\":{\"AP\":\"Andhra Pradesh\",\"AR\":\"Arunachal Pradesh\",\"AS\":\"Assam\",\"BR\":\"Bihar\",\"CT\":\"Chhattisgarh\",\"GA\":\"Goa\",\"GJ\":\"Gujarat\",\"HR\":\"Haryana\",\"HP\":\"Himachal Pradesh\",\"JK\":\"Jammu and Kashmir\",\"JH\":\"Jharkhand\",\"KA\":\"Karnataka\",\"KL\":\"Kerala\",\"LA\":\"Ladakh\",\"MP\":\"Madhya Pradesh\",\"MH\":\"Maharashtra\",\"MN\":\"Manipur\",\"ML\":\"Meghalaya\",\"MZ\":\"Mizoram\",\"NL\":\"Nagaland\",\"OR\":\"Odisha\",\"PB\":\"Punjab\",\"RJ\":\"Rajasthan\",\"SK\":\"Sikkim\",\"TN\":\"Tamil Nadu\",\"TS\":\"Telangana\",\"TR\":\"Tripura\",\"UK\":\"Uttarakhand\",\"UP\":\"Uttar Pradesh\",\"WB\":\"West Bengal\",\"AN\":\"Andaman and Nicobar Islands\",\"CH\":\"Chandigarh\",\"DN\":\"Dadra and Nagar Haveli\",\"DD\":\"Daman and Diu\",\"DL\":\"Delhi\",\"LD\":\"Lakshadeep\",\"PY\":\"Pondicherry (Puducherry)\"},\"ID\":{\"AC\":\"Daerah Istimewa Aceh\",\"SU\":\"Sumatera Utara\",\"SB\":\"Sumatera Barat\",\"RI\":\"Riau\",\"KR\":\"Kepulauan Riau\",\"JA\":\"Jambi\",\"SS\":\"Sumatera Selatan\",\"BB\":\"Bangka Belitung\",\"BE\":\"Bengkulu\",\"LA\":\"Lampung\",\"JK\":\"DKI Jakarta\",\"JB\":\"Jawa Barat\",\"BT\":\"Banten\",\"JT\":\"Jawa Tengah\",\"JI\":\"Jawa Timur\",\"YO\":\"Daerah Istimewa Yogyakarta\",\"BA\":\"Bali\",\"NB\":\"Nusa Tenggara Barat\",\"NT\":\"Nusa Tenggara Timur\",\"KB\":\"Kalimantan Barat\",\"KT\":\"Kalimantan Tengah\",\"KI\":\"Kalimantan Timur\",\"KS\":\"Kalimantan Selatan\",\"KU\":\"Kalimantan Utara\",\"SA\":\"Sulawesi Utara\",\"ST\":\"Sulawesi Tengah\",\"SG\":\"Sulawesi Tenggara\",\"SR\":\"Sulawesi Barat\",\"SN\":\"Sulawesi Selatan\",\"GO\":\"Gorontalo\",\"MA\":\"Maluku\",\"MU\":\"Maluku Utara\",\"PA\":\"Papua\",\"PB\":\"Papua Barat\"},\"IE\":{\"CW\":\"Carlow\",\"CN\":\"Cavan\",\"CE\":\"Clare\",\"CO\":\"Cork\",\"DL\":\"Donegal\",\"D\":\"Dublin\",\"G\":\"Galway\",\"KY\":\"Kerry\",\"KE\":\"Kildare\",\"KK\":\"Kilkenny\",\"LS\":\"Laois\",\"LM\":\"Leitrim\",\"LK\":\"Limerick\",\"LD\":\"Longford\",\"LH\":\"Louth\",\"MO\":\"Mayo\",\"MH\":\"Meath\",\"MN\":\"Monaghan\",\"OY\":\"Offaly\",\"RN\":\"Roscommon\",\"SO\":\"Sligo\",\"TA\":\"Tipperary\",\"WD\":\"Waterford\",\"WH\":\"Westmeath\",\"WX\":\"Wexford\",\"WW\":\"Wicklow\"},\"IL\":[],\"IT\":{\"AG\":\"Agrigento\",\"AL\":\"Alessandria\",\"AN\":\"Ancona\",\"AO\":\"Aosta\",\"AR\":\"Arezzo\",\"AP\":\"Ascoli Piceno\",\"AT\":\"Asti\",\"AV\":\"Avellino\",\"BA\":\"Bari\",\"BT\":\"Barletta-Andria-Trani\",\"BL\":\"Belluno\",\"BN\":\"Benevento\",\"BG\":\"Bergamo\",\"BI\":\"Biella\",\"BO\":\"Bologna\",\"BZ\":\"Bolzano\",\"BS\":\"Brescia\",\"BR\":\"Brindisi\",\"CA\":\"Cagliari\",\"CL\":\"Caltanissetta\",\"CB\":\"Campobasso\",\"CE\":\"Caserta\",\"CT\":\"Catania\",\"CZ\":\"Catanzaro\",\"CH\":\"Chieti\",\"CO\":\"Como\",\"CS\":\"Cosenza\",\"CR\":\"Cremona\",\"KR\":\"Crotone\",\"CN\":\"Cuneo\",\"EN\":\"Enna\",\"FM\":\"Fermo\",\"FE\":\"Ferrara\",\"FI\":\"Firenze\",\"FG\":\"Foggia\",\"FC\":\"Forl\\u00ec-Cesena\",\"FR\":\"Frosinone\",\"GE\":\"Genova\",\"GO\":\"Gorizia\",\"GR\":\"Grosseto\",\"IM\":\"Imperia\",\"IS\":\"Isernia\",\"SP\":\"La Spezia\",\"AQ\":\"L'Aquila\",\"LT\":\"Latina\",\"LE\":\"Lecce\",\"LC\":\"Lecco\",\"LI\":\"Livorno\",\"LO\":\"Lodi\",\"LU\":\"Lucca\",\"MC\":\"Macerata\",\"MN\":\"Mantova\",\"MS\":\"Massa-Carrara\",\"MT\":\"Matera\",\"ME\":\"Messina\",\"MI\":\"Milano\",\"MO\":\"Modena\",\"MB\":\"Monza e della Brianza\",\"NA\":\"Napoli\",\"NO\":\"Novara\",\"NU\":\"Nuoro\",\"OR\":\"Oristano\",\"PD\":\"Padova\",\"PA\":\"Palermo\",\"PR\":\"Parma\",\"PV\":\"Pavia\",\"PG\":\"Perugia\",\"PU\":\"Pesaro e Urbino\",\"PE\":\"Pescara\",\"PC\":\"Piacenza\",\"PI\":\"Pisa\",\"PT\":\"Pistoia\",\"PN\":\"Pordenone\",\"PZ\":\"Potenza\",\"PO\":\"Prato\",\"RG\":\"Ragusa\",\"RA\":\"Ravenna\",\"RC\":\"Reggio Calabria\",\"RE\":\"Reggio Emilia\",\"RI\":\"Rieti\",\"RN\":\"Rimini\",\"RM\":\"Roma\",\"RO\":\"Rovigo\",\"SA\":\"Salerno\",\"SS\":\"Sassari\",\"SV\":\"Savona\",\"SI\":\"Siena\",\"SR\":\"Siracusa\",\"SO\":\"Sondrio\",\"SU\":\"Sud Sardegna\",\"TA\":\"Taranto\",\"TE\":\"Teramo\",\"TR\":\"Terni\",\"TO\":\"Torino\",\"TP\":\"Trapani\",\"TN\":\"Trento\",\"TV\":\"Treviso\",\"TS\":\"Trieste\",\"UD\":\"Udine\",\"VA\":\"Varese\",\"VE\":\"Venezia\",\"VB\":\"Verbano-Cusio-Ossola\",\"VC\":\"Vercelli\",\"VR\":\"Verona\",\"VV\":\"Vibo Valentia\",\"VI\":\"Vicenza\",\"VT\":\"Viterbo\"},\"JP\":{\"JP01\":\"Hokkaido\",\"JP02\":\"Aomori\",\"JP03\":\"Iwate\",\"JP04\":\"Miyagi\",\"JP05\":\"Akita\",\"JP06\":\"Yamagata\",\"JP07\":\"Fukushima\",\"JP08\":\"Ibaraki\",\"JP09\":\"Tochigi\",\"JP10\":\"Gunma\",\"JP11\":\"Saitama\",\"JP12\":\"Chiba\",\"JP13\":\"Tokyo\",\"JP14\":\"Kanagawa\",\"JP15\":\"Niigata\",\"JP16\":\"Toyama\",\"JP17\":\"Ishikawa\",\"JP18\":\"Fukui\",\"JP19\":\"Yamanashi\",\"JP20\":\"Nagano\",\"JP21\":\"Gifu\",\"JP22\":\"Shizuoka\",\"JP23\":\"Aichi\",\"JP24\":\"Mie\",\"JP25\":\"Shiga\",\"JP26\":\"Kyoto\",\"JP27\":\"Osaka\",\"JP28\":\"Hyogo\",\"JP29\":\"Nara\",\"JP30\":\"Wakayama\",\"JP31\":\"Tottori\",\"JP32\":\"Shimane\",\"JP33\":\"Okayama\",\"JP34\":\"Hiroshima\",\"JP35\":\"Yamaguchi\",\"JP36\":\"Tokushima\",\"JP37\":\"Kagawa\",\"JP38\":\"Ehime\",\"JP39\":\"Kochi\",\"JP40\":\"Fukuoka\",\"JP41\":\"Saga\",\"JP42\":\"Nagasaki\",\"JP43\":\"Kumamoto\",\"JP44\":\"Oita\",\"JP45\":\"Miyazaki\",\"JP46\":\"Kagoshima\",\"JP47\":\"Okinawa\"},\"MY\":{\"JHR\":\"Johor\",\"KDH\":\"Kedah\",\"KTN\":\"Kelantan\",\"LBN\":\"Labuan\",\"MLK\":\"Malacca (Melaka)\",\"NSN\":\"Negeri Sembilan\",\"PHG\":\"Pahang\",\"PNG\":\"Penang (Pulau Pinang)\",\"PRK\":\"Perak\",\"PLS\":\"Perlis\",\"SBH\":\"Sabah\",\"SWK\":\"Sarawak\",\"SGR\":\"Selangor\",\"TRG\":\"Terengganu\",\"PJY\":\"Putrajaya\",\"KUL\":\"Kuala Lumpur\"},\"MT\":[],\"NL\":[],\"NZ\":{\"NTL\":\"Northland\",\"AUK\":\"Auckland\",\"WKO\":\"Waikato\",\"BOP\":\"Bay of Plenty\",\"TKI\":\"Taranaki\",\"GIS\":\"Gisborne\",\"HKB\":\"Hawke\\u2019s Bay\",\"MWT\":\"Manawatu-Wanganui\",\"WGN\":\"Wellington\",\"NSN\":\"Nelson\",\"MBH\":\"Marlborough\",\"TAS\":\"Tasman\",\"WTC\":\"West Coast\",\"CAN\":\"Canterbury\",\"OTA\":\"Otago\",\"STL\":\"Southland\"},\"NO\":[],\"PH\":{\"ABR\":\"Abra\",\"AGN\":\"Agusan del Norte\",\"AGS\":\"Agusan del Sur\",\"AKL\":\"Aklan\",\"ALB\":\"Albay\",\"ANT\":\"Antique\",\"APA\":\"Apayao\",\"AUR\":\"Aurora\",\"BAS\":\"Basilan\",\"BAN\":\"Bataan\",\"BTN\":\"Batanes\",\"BTG\":\"Batangas\",\"BEN\":\"Benguet\",\"BIL\":\"Biliran\",\"BOH\":\"Bohol\",\"BUK\":\"Bukidnon\",\"BUL\":\"Bulacan\",\"CAG\":\"Cagayan\",\"CAN\":\"Camarines Norte\",\"CAS\":\"Camarines Sur\",\"CAM\":\"Camiguin\",\"CAP\":\"Capiz\",\"CAT\":\"Catanduanes\",\"CAV\":\"Cavite\",\"CEB\":\"Cebu\",\"COM\":\"Compostela Valley\",\"NCO\":\"Cotabato\",\"DAV\":\"Davao del Norte\",\"DAS\":\"Davao del Sur\",\"DAC\":\"Davao Occidental\",\"DAO\":\"Davao Oriental\",\"DIN\":\"Dinagat Islands\",\"EAS\":\"Eastern Samar\",\"GUI\":\"Guimaras\",\"IFU\":\"Ifugao\",\"ILN\":\"Ilocos Norte\",\"ILS\":\"Ilocos Sur\",\"ILI\":\"Iloilo\",\"ISA\":\"Isabela\",\"KAL\":\"Kalinga\",\"LUN\":\"La Union\",\"LAG\":\"Laguna\",\"LAN\":\"Lanao del Norte\",\"LAS\":\"Lanao del Sur\",\"LEY\":\"Leyte\",\"MAG\":\"Maguindanao\",\"MAD\":\"Marinduque\",\"MAS\":\"Masbate\",\"MSC\":\"Misamis Occidental\",\"MSR\":\"Misamis Oriental\",\"MOU\":\"Mountain Province\",\"NEC\":\"Negros Occidental\",\"NER\":\"Negros Oriental\",\"NSA\":\"Northern Samar\",\"NUE\":\"Nueva Ecija\",\"NUV\":\"Nueva Vizcaya\",\"MDC\":\"Occidental Mindoro\",\"MDR\":\"Oriental Mindoro\",\"PLW\":\"Palawan\",\"PAM\":\"Pampanga\",\"PAN\":\"Pangasinan\",\"QUE\":\"Quezon\",\"QUI\":\"Quirino\",\"RIZ\":\"Rizal\",\"ROM\":\"Romblon\",\"WSA\":\"Samar\",\"SAR\":\"Sarangani\",\"SIQ\":\"Siquijor\",\"SOR\":\"Sorsogon\",\"SCO\":\"South Cotabato\",\"SLE\":\"Southern Leyte\",\"SUK\":\"Sultan Kudarat\",\"SLU\":\"Sulu\",\"SUN\":\"Surigao del Norte\",\"SUR\":\"Surigao del Sur\",\"TAR\":\"Tarlac\",\"TAW\":\"Tawi-Tawi\",\"ZMB\":\"Zambales\",\"ZAN\":\"Zamboanga del Norte\",\"ZAS\":\"Zamboanga del Sur\",\"ZSI\":\"Zamboanga Sibugay\",\"00\":\"Metro Manila\"},\"PL\":[],\"PT\":[],\"RS\":{\"RS00\":\"Belgrade\",\"RS14\":\"Bor\",\"RS11\":\"Brani\\u010devo\",\"RS02\":\"Central Banat\",\"RS10\":\"Danube\",\"RS23\":\"Jablanica\",\"RS09\":\"Kolubara\",\"RS08\":\"Ma\\u010dva\",\"RS17\":\"Morava\",\"RS20\":\"Ni\\u0161ava\",\"RS01\":\"North Ba\\u010dka\",\"RS03\":\"North Banat\",\"RS24\":\"P\\u010dinja\",\"RS22\":\"Pirot\",\"RS13\":\"Pomoravlje\",\"RS19\":\"Rasina\",\"RS18\":\"Ra\\u0161ka\",\"RS06\":\"South Ba\\u010dka\",\"RS04\":\"South Banat\",\"RS07\":\"Srem\",\"RS12\":\"\\u0160umadija\",\"RS21\":\"Toplica\",\"RS05\":\"West Ba\\u010dka\",\"RS15\":\"Zaje\\u010dar\",\"RS16\":\"Zlatibor\",\"RS25\":\"Kosovo\",\"RS26\":\"Pe\\u0107\",\"RS27\":\"Prizren\",\"RS28\":\"Kosovska Mitrovica\",\"RS29\":\"Kosovo-Pomoravlje\",\"RSKM\":\"Kosovo-Metohija\",\"RSVO\":\"Vojvodina\"},\"SG\":[],\"SK\":[],\"SI\":[],\"ZA\":{\"EC\":\"Eastern Cape\",\"FS\":\"Free State\",\"GP\":\"Gauteng\",\"KZN\":\"KwaZulu-Natal\",\"LP\":\"Limpopo\",\"MP\":\"Mpumalanga\",\"NC\":\"Northern Cape\",\"NW\":\"North West\",\"WC\":\"Western Cape\"},\"KR\":[],\"ES\":{\"C\":\"A Coru\\u00f1a\",\"VI\":\"Araba\\/\\u00c1lava\",\"AB\":\"Albacete\",\"A\":\"Alicante\",\"AL\":\"Almer\\u00eda\",\"O\":\"Asturias\",\"AV\":\"\\u00c1vila\",\"BA\":\"Badajoz\",\"PM\":\"Baleares\",\"B\":\"Barcelona\",\"BU\":\"Burgos\",\"CC\":\"C\\u00e1ceres\",\"CA\":\"C\\u00e1diz\",\"S\":\"Cantabria\",\"CS\":\"Castell\\u00f3n\",\"CE\":\"Ceuta\",\"CR\":\"Ciudad Real\",\"CO\":\"C\\u00f3rdoba\",\"CU\":\"Cuenca\",\"GI\":\"Girona\",\"GR\":\"Granada\",\"GU\":\"Guadalajara\",\"SS\":\"Gipuzkoa\",\"H\":\"Huelva\",\"HU\":\"Huesca\",\"J\":\"Ja\\u00e9n\",\"LO\":\"La Rioja\",\"GC\":\"Las Palmas\",\"LE\":\"Le\\u00f3n\",\"L\":\"Lleida\",\"LU\":\"Lugo\",\"M\":\"Madrid\",\"MA\":\"M\\u00e1laga\",\"ML\":\"Melilla\",\"MU\":\"Murcia\",\"NA\":\"Navarra\",\"OR\":\"Ourense\",\"P\":\"Palencia\",\"PO\":\"Pontevedra\",\"SA\":\"Salamanca\",\"TF\":\"Santa Cruz de Tenerife\",\"SG\":\"Segovia\",\"SE\":\"Sevilla\",\"SO\":\"Soria\",\"T\":\"Tarragona\",\"TE\":\"Teruel\",\"TO\":\"Toledo\",\"V\":\"Valencia\",\"VA\":\"Valladolid\",\"BI\":\"Biscay\",\"ZA\":\"Zamora\",\"Z\":\"Zaragoza\"},\"SE\":[],\"CH\":{\"AG\":\"Aargau\",\"AR\":\"Appenzell Ausserrhoden\",\"AI\":\"Appenzell Innerrhoden\",\"BL\":\"Basel-Landschaft\",\"BS\":\"Basel-Stadt\",\"BE\":\"Bern\",\"FR\":\"Fribourg\",\"GE\":\"Geneva\",\"GL\":\"Glarus\",\"GR\":\"Graub\\u00fcnden\",\"JU\":\"Jura\",\"LU\":\"Luzern\",\"NE\":\"Neuch\\u00e2tel\",\"NW\":\"Nidwalden\",\"OW\":\"Obwalden\",\"SH\":\"Schaffhausen\",\"SZ\":\"Schwyz\",\"SO\":\"Solothurn\",\"SG\":\"St. Gallen\",\"TG\":\"Thurgau\",\"TI\":\"Ticino\",\"UR\":\"Uri\",\"VS\":\"Valais\",\"VD\":\"Vaud\",\"ZG\":\"Zug\",\"ZH\":\"Z\\u00fcrich\"},\"TR\":{\"TR01\":\"Adana\",\"TR02\":\"Ad\\u0131yaman\",\"TR03\":\"Afyon\",\"TR04\":\"A\\u011fr\\u0131\",\"TR05\":\"Amasya\",\"TR06\":\"Ankara\",\"TR07\":\"Antalya\",\"TR08\":\"Artvin\",\"TR09\":\"Ayd\\u0131n\",\"TR10\":\"Bal\\u0131kesir\",\"TR11\":\"Bilecik\",\"TR12\":\"Bing\\u00f6l\",\"TR13\":\"Bitlis\",\"TR14\":\"Bolu\",\"TR15\":\"Burdur\",\"TR16\":\"Bursa\",\"TR17\":\"\\u00c7anakkale\",\"TR18\":\"\\u00c7ank\\u0131r\\u0131\",\"TR19\":\"\\u00c7orum\",\"TR20\":\"Denizli\",\"TR21\":\"Diyarbak\\u0131r\",\"TR22\":\"Edirne\",\"TR23\":\"Elaz\\u0131\\u011f\",\"TR24\":\"Erzincan\",\"TR25\":\"Erzurum\",\"TR26\":\"Eski\\u015fehir\",\"TR27\":\"Gaziantep\",\"TR28\":\"Giresun\",\"TR29\":\"G\\u00fcm\\u00fc\\u015fhane\",\"TR30\":\"Hakkari\",\"TR31\":\"Hatay\",\"TR32\":\"Isparta\",\"TR33\":\"\\u0130\\u00e7el\",\"TR34\":\"\\u0130stanbul\",\"TR35\":\"\\u0130zmir\",\"TR36\":\"Kars\",\"TR37\":\"Kastamonu\",\"TR38\":\"Kayseri\",\"TR39\":\"K\\u0131rklareli\",\"TR40\":\"K\\u0131r\\u015fehir\",\"TR41\":\"Kocaeli\",\"TR42\":\"Konya\",\"TR43\":\"K\\u00fctahya\",\"TR44\":\"Malatya\",\"TR45\":\"Manisa\",\"TR46\":\"Kahramanmara\\u015f\",\"TR47\":\"Mardin\",\"TR48\":\"Mu\\u011fla\",\"TR49\":\"Mu\\u015f\",\"TR50\":\"Nev\\u015fehir\",\"TR51\":\"Ni\\u011fde\",\"TR52\":\"Ordu\",\"TR53\":\"Rize\",\"TR54\":\"Sakarya\",\"TR55\":\"Samsun\",\"TR56\":\"Siirt\",\"TR57\":\"Sinop\",\"TR58\":\"Sivas\",\"TR59\":\"Tekirda\\u011f\",\"TR60\":\"Tokat\",\"TR61\":\"Trabzon\",\"TR62\":\"Tunceli\",\"TR63\":\"\\u015eanl\\u0131urfa\",\"TR64\":\"U\\u015fak\",\"TR65\":\"Van\",\"TR66\":\"Yozgat\",\"TR67\":\"Zonguldak\",\"TR68\":\"Aksaray\",\"TR69\":\"Bayburt\",\"TR70\":\"Karaman\",\"TR71\":\"K\\u0131r\\u0131kkale\",\"TR72\":\"Batman\",\"TR73\":\"\\u015e\\u0131rnak\",\"TR74\":\"Bart\\u0131n\",\"TR75\":\"Ardahan\",\"TR76\":\"I\\u011fd\\u0131r\",\"TR77\":\"Yalova\",\"TR78\":\"Karab\\u00fck\",\"TR79\":\"Kilis\",\"TR80\":\"Osmaniye\",\"TR81\":\"D\\u00fczce\"},\"US\":{\"AL\":\"Alabama\",\"AK\":\"Alaska\",\"AZ\":\"Arizona\",\"AR\":\"Arkansas\",\"CA\":\"California\",\"CO\":\"Colorado\",\"CT\":\"Connecticut\",\"DE\":\"Delaware\",\"DC\":\"District Of Columbia\",\"FL\":\"Florida\",\"GA\":\"Georgia\",\"HI\":\"Hawaii\",\"ID\":\"Idaho\",\"IL\":\"Illinois\",\"IN\":\"Indiana\",\"IA\":\"Iowa\",\"KS\":\"Kansas\",\"KY\":\"Kentucky\",\"LA\":\"Louisiana\",\"ME\":\"Maine\",\"MD\":\"Maryland\",\"MA\":\"Massachusetts\",\"MI\":\"Michigan\",\"MN\":\"Minnesota\",\"MS\":\"Mississippi\",\"MO\":\"Missouri\",\"MT\":\"Montana\",\"NE\":\"Nebraska\",\"NV\":\"Nevada\",\"NH\":\"New Hampshire\",\"NJ\":\"New Jersey\",\"NM\":\"New Mexico\",\"NY\":\"New York\",\"NC\":\"North Carolina\",\"ND\":\"North Dakota\",\"OH\":\"Ohio\",\"OK\":\"Oklahoma\",\"OR\":\"Oregon\",\"PA\":\"Pennsylvania\",\"RI\":\"Rhode Island\",\"SC\":\"South Carolina\",\"SD\":\"South Dakota\",\"TN\":\"Tennessee\",\"TX\":\"Texas\",\"UT\":\"Utah\",\"VT\":\"Vermont\",\"VA\":\"Virginia\",\"WA\":\"Washington\",\"WV\":\"West Virginia\",\"WI\":\"Wisconsin\",\"WY\":\"Wyoming\",\"AA\":\"Armed Forces (AA)\",\"AE\":\"Armed Forces (AE)\",\"AP\":\"Armed Forces (AP)\"},\"UM\":{\"81\":\"Baker Island\",\"84\":\"Howland Island\",\"86\":\"Jarvis Island\",\"67\":\"Johnston Atoll\",\"89\":\"Kingman Reef\",\"71\":\"Midway Atoll\",\"76\":\"Navassa Island\",\"95\":\"Palmyra Atoll\",\"79\":\"Wake Island\"},\"VN\":[]}",
    "i18n_select_state_text": "Select an option…",
    "i18n_no_matches": "No matches found",
    "i18n_ajax_error": "Loading failed",
    "i18n_input_too_short_1": "Please enter 1 or more characters",
    "i18n_input_too_short_n": "Please enter %qty% or more characters",
    "i18n_input_too_long_1": "Please delete 1 character",
    "i18n_input_too_long_n": "Please delete %qty% characters",
    "i18n_selection_too_long_1": "You can only select 1 item",
    "i18n_selection_too_long_n": "You can only select %qty% items",
    "i18n_load_more": "Loading more results…",
    "i18n_searching": "Searching…"
  },
  {
    "ajaxurl": "/?wc-ajax=%%endpoint%%",
    "refreshForm": "yith_wfbt_refresh_form",
    "loadVariationsDialog": "yith_wfbt_load_variations_dialog_content",
    "loader": "https://www.freaksports.com.au/wp-content/plugins/yith-woocommerce-frequently-bought-together-premium/assets/images/loader.gif",
    "visible_elem": "4",
    "variation_selector": ".variations_form"
  },
  {
    "ajax": {
      "url": "/wp-admin/admin-ajax.php"
    }
  },
  {
    "wc_ajax_url": "/?wc-ajax=%%endpoint%%",
    "i18n_no_matching_variations_text": "Sorry, no products matched your selection. Please choose a different combination.",
    "i18n_make_a_selection_text": "Please select some product options before adding this product to your cart.",
    "i18n_unavailable_text": "Sorry, this product is unavailable. Please choose a different combination."
  },
  {
    "wc_ajax_url": "/?wc-ajax=%%endpoint%%",
    "i18n_no_matching_variations_text": "Sorry, no products matched your selection. Please choose a different combination.",
    "i18n_make_a_selection_text": "Please select some product options before adding this product to your cart.",
    "i18n_unavailable_text": "Sorry, this product is unavailable. Please choose a different combination."
  },
  {
    "ajax_url": "https://www.freaksports.com.au/wp-admin/admin-ajax.php",
    "actions": {
      "add_gift_to_cart": "ywdpd_add_gift_to_cart",
      "add_bogo_to_cart": "ywdpd_add_bogo_to_cart",
      "add_special_to_cart": "ywdpd_add_special_to_cart",
      "show_second_step": "ywdpd_show_second_step",
      "check_variable": "ywdpd_check_variable",
      "update_gift_popup": "ywdpd_update_gift_popup",
      "show_popup_on_shop": "ywdpd_show_popup_on_shop"
    },
    "nonces": {
      "add_gift_to_cart": "e1b6bf6344",
      "add_bogo_to_cart": "1601233ad4",
      "add_special_to_cart": "92ce351f24",
      "show_second_step": "35f2eebd37",
      "check_variable": "d3d9b09007",
      "update_gift_popup": "470faec47d",
      "show_popup_on_shop": "1f1bc5009b"
    },
    "i18n_qty_field_label": "Qty in cart",
    "rtl": "False"
  },
  {
    "show_minimum_price": "no",
    "template": "vertical",
    "is_change_qty_enabled": "yes",
    "is_default_qty_enabled": "no",
    "column_product_info_class": ".single-product .summary",
    "product_price_classes": ".price, .wpb_wrapper .price, .elementor-widget-woocommerce-product-price .price",
    "product_qty_classes": " .qty, .elementor-add-to-cart .qty, .w-post-elm .qty",
    "variation_form_class": "form.variations_form.cart",
    "select_minimum_quantity": "",
    "update_prices_in_ajax": "yes",
    "show_variable_table": "yes",
    "ajax_url": "https://www.freaksports.com.au/wp-admin/admin-ajax.php",
    "actions": {
      "update_product_price": "ywdpd_update_product_price"
    },
    "nonces": {
      "update_product_price": "526bc8c58d"
    }
  },
  {
    "theme": {
      "version": "3.17.4"
    },
    "ajaxurl": "https://www.freaksports.com.au/wp-admin/admin-ajax.php",
    "rtl": "",
    "sticky_height": "70",
    "stickyHeaderHeight": "0",
    "scrollPaddingTop": "0",
    "assets_url": "https://www.freaksports.com.au/wp-content/themes/flatsome/assets/",
    "lightbox": {
      "close_markup": "<button title=\"%title%\" type=\"button\" class=\"mfp-close\"><svg xmlns=\"http://www.w3.org/2000/svg\" width=\"28\" height=\"28\" viewBox=\"0 0 24 24\" fill=\"none\" stroke=\"currentColor\" stroke-width=\"2\" stroke-linecap=\"round\" stroke-linejoin=\"round\" class=\"feather feather-x\"><line x1=\"18\" y1=\"6\" x2=\"6\" y2=\"18\"></line><line x1=\"6\" y1=\"6\" x2=\"18\" y2=\"18\"></line></svg></button>",
      "close_btn_inside": False
    },
    "user": {
      "can_edit_pages": False
    },
    "i18n": {
      "mainMenu": "Main Menu",
      "toggleButton": "Toggle"
    },
    "options": {
      "cookie_notice_version": "1",
      "swatches_layout": False,
      "swatches_disable_deselect": False,
      "swatches_box_select_event": False,
      "swatches_box_behavior_selected": False,
      "swatches_box_update_urls": "1",
      "swatches_box_reset": False,
      "swatches_box_reset_limited": False,
      "swatches_box_reset_extent": False,
      "swatches_box_reset_time": 300,
      "search_result_latency": "500"
    },
    "is_mini_cart_reveal": ""
  }
]

# Function to recursively search for the target value in a dictionary or list
# def search_value(item, target):
#   global found_target
#   found_target = ""

#   if isinstance(item, dict):
#     for key, value in item.items():
#       if value == target:
#         found_target = f'{value}'
#         logging.info("Found target value '%s' at key '%s'", target, key)
#         return
#       elif isinstance(value, (dict, list)):
#         search_value(value, target)
#   elif isinstance(item, list):
#     for i, value in enumerate(item):
#       if value == target:
#         found_target = f'{value}'
#         logging.info("Found target value '%s' at key '%s'", target, i)
#         return
#       elif isinstance(value, (dict, list)):
#         search_value(value, target)

#   logging.info('Found target: %s', found_target)
#   return found_target

# Function to recursively search for the target value in a dictionary or list
def search_value(item, target):
  global found_target
  found_target = ""
  
  def recursive_search(item, target):
    global found_target
    if found_target:
      return

    if isinstance(item, dict):
      for key, value in item.items():
        if value == target:
          found_target = f'{value}'
          print(f"Found target value '{target}' at key '{key}'")
          return
        elif isinstance(value, (dict, list)):
          recursive_search(value, target)
    elif isinstance(item, list):
      for i, value in enumerate(item):
        if value == target:
          found_target = f'{value}'
          print(f"Found target value '{target}' at key '{i}'")
          return
        elif isinstance(value, (dict, list)):
          recursive_search(value, target)

  recursive_search(item, target)
  
  print(f'Found target: {found_target}')
  return found_target

if __name__ == '__main__':

  found_text = search_value(item, '9421026833822')
  print(f'found_text: {found_text}')