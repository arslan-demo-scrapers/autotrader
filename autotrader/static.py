handle_httpstatus_list = [
    400, 401, 402, 403, 404, 405, 406, 407, 409,
    500, 501, 502, 503, 504, 505, 506, 507, 509,
]

headers = {
    'accept': '*/*',
    'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8',
    'content-type': 'application/json',
    'origin': 'https://www.autotrader.co.uk',
    'priority': 'u=1, i',
    'referer': 'https://www.autotrader.co.uk/',
    'sec-ch-ua': '"Not(A:Brand";v="8", "Chromium";v="144", "Google Chrome";v="144"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"macOS"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/144.0.0.0 Safari/537.36',
    'x-sauron-app-name': 'sauron-search-results-app',
    'x-sauron-app-version': '730384378d',
}

fuel_types = [
    # 'Petrol',
    # 'Diesel',
    'Petrol Plug-in Hybrid',
    'Diesel Plug-in Hybrid',
    'Petrol Hybrid',
    'Diesel Hybrid',
]

details_data = [
    {
        'operationName': 'FPADataQuery',
        'variables': {
            # 'advertId': '202601229349779',
            'searchOptions': {
                'advertisingLocations': [
                    'at_cars',
                ],
                'postcode': '',
                'collectionLocationOptions': {
                    'searchPostcode': '',
                },
                'channel': 'cars',
            },
        },
        'query': 'query FPADataQuery($advertId: String!, $searchOptions: SearchOptions) {\n  search {\n    advert(advertId: $advertId, searchOptions: $searchOptions) {\n      id\n      stockItemId\n      excludePreviousOwners\n      advertisedLocations\n      dateOfRegistration\n      capabilities {\n        marketExtensionHomeDelivery {\n          enabled\n          __typename\n        }\n        marketExtensionClickAndCollect {\n          enabled\n          __typename\n        }\n        marketExtensionCentrallyHeld {\n          enabled\n          __typename\n        }\n        marketExtensionOem {\n          enabled\n          __typename\n        }\n        digitalRetailing {\n          enabled\n          __typename\n        }\n        leadsApi {\n          enabled\n          __typename\n        }\n        __typename\n      }\n      registration\n      generation {\n        generationId\n        __typename\n      }\n      isPartExAvailable\n      retailerId\n      privateAdvertiser {\n        tola\n        __typename\n      }\n      dealer {\n        dealerId\n        assignedNumber {\n          number\n          __typename\n        }\n        capabilities {\n          instantMessagingChat {\n            enabled\n            provider\n            __typename\n          }\n          instantMessagingText {\n            enabled\n            provider\n            overrideSmsNumber\n            __typename\n          }\n          __typename\n        }\n        name\n        servicesOffered {\n          sellerPromise {\n            monthlyWarranty\n            daysMoneyBackGuarantee\n            moneyBackRemoteOnly\n            __typename\n          }\n          products\n          nccApproved\n          __typename\n        }\n        __typename\n      }\n      mileageDeviation\n      year\n      sellerType\n      sellerProducts\n      sellerContact {\n        byEmail\n        __typename\n      }\n      colour\n      manufacturerApproved\n      owners\n      specification {\n        isCrossover\n        bodyType\n        fuel\n        make\n        model\n        trim\n        style\n        derivativeId\n        __typename\n      }\n      condition\n      reservation {\n        status\n        eligibility\n        feeCurrency\n        feeInFractionalUnits\n        __typename\n      }\n      __typename\n    }\n    __typename\n  }\n}',
    }
]

listings_filters_data = [
    {
        'operationName': 'SearchResultsListingsGridQuery',
        'variables': {
            'filters': [
                # {
                #     'filter': 'fuel_type',
                #     'selected': [
                #         'Petrol',
                #     ],
                # },
                # {
                #     'filter': 'home_delivery_adverts',
                #     'selected': [
                #         'include',
                #     ],
                # },
                # {
                #     'filter': 'make',
                #     'selected': [
                #         'Mercedes-Benz',
                #     ],
                # },
                {
                    'filter': 'max_year_manufactured',
                    'selected': [
                        '2026',
                    ],
                },
                {
                    'filter': 'min_year_manufactured',
                    'selected': [
                        '2017',
                    ],
                },
                {
                    'filter': 'postcode',
                    'selected': [
                        'bt11al',
                    ],
                },
                {
                    'filter': 'price_search_type',
                    'selected': [
                        'total',
                    ],
                },
            ],
            'channel': 'cars',
            'page': 1,
            'sortBy': 'relevance',
            'listingType': None,
            'searchId': '7f5fa690-72f3-491d-bbbc-905fd2b5ce64',
            'featureFlags': [],
        },
        'query': 'query SearchResultsListingsGridQuery($filters: [FilterInput!]!, $channel: Channel!, $page: Int, $sortBy: SearchResultsSort, $listingType: [ListingType!], $searchId: String!, $featureFlags: [FeatureFlag]) {\n  searchResults(\n    input: {facets: [], filters: $filters, channel: $channel, page: $page, sortBy: $sortBy, listingType: $listingType, searchId: $searchId, featureFlags: $featureFlags}\n  ) {\n    intercept {\n      interceptType\n      title\n      subtitle\n      buttonText\n      sort\n      ctaUrl\n      __typename\n    }\n    listings {\n      ... on SearchListing {\n        type\n        advertId\n        title\n        subTitle\n        attentionGrabber\n        price\n        vehicleLocation\n        locationType\n        discount\n        images\n        numberOfImages\n        rrp\n        sellerType\n        dealerLink\n        dealerReview {\n          overallReviewRating\n          __typename\n        }\n        fpaLink\n        hasDigitalRetailing\n        preReg\n        finance {\n          monthlyPrice {\n            priceFormattedAndRounded\n            __typename\n          }\n          initialPayment\n          termMonths\n          quoteSubType\n          representativeValues {\n            financeKey\n            financeValue\n            __typename\n          }\n          disclaimerText {\n            components {\n              ... on FinanceListingDisclaimerTextComponent {\n                text\n                __typename\n              }\n              ... on FinanceListingDisclaimerLinkComponent {\n                text\n                link\n                __typename\n              }\n              ... on FinanceListingDisclaimerTitleComponent {\n                text\n                __typename\n              }\n              __typename\n            }\n            __typename\n          }\n          financeListingProvider\n          rawFinanceFields {\n            deposit\n            term\n            annualMileage\n            __typename\n          }\n          __typename\n        }\n        badges {\n          type\n          displayText\n          __typename\n        }\n        position\n        trackingContext {\n          retailerContext {\n            id\n            __typename\n          }\n          advertContext {\n            id\n            advertiserId\n            advertiserType\n            make\n            model\n            vehicleCategory\n            year\n            condition\n            price\n            searchVersionId\n            __typename\n          }\n          card {\n            category\n            subCategory\n            pageNumber\n            position\n            __typename\n          }\n          advertCardFeatures {\n            condition\n            numImages\n            hasFinance\n            priceIndicator\n            isManufacturedApproved\n            isFranchiseApproved\n            __typename\n          }\n          distance {\n            distance\n            distance_unit\n            __typename\n          }\n          __typename\n        }\n        __typename\n      }\n      ... on GPTListing {\n        type\n        targetingSegments {\n          name\n          values\n          __typename\n        }\n        areaOfInterest {\n          manufacturerCodes\n          __typename\n        }\n        posId\n        __typename\n      }\n      ... on LeasingListing {\n        type\n        advertId\n        title\n        subTitle\n        price\n        vatStatus\n        images\n        numberOfImages\n        fpaLink\n        finance {\n          monthlyPrice {\n            priceFormattedAndRounded\n            __typename\n          }\n          representativeExample\n          representativeValues {\n            financeKey\n            financeValue\n            __typename\n          }\n          initialPayment\n          termMonths\n          mileage\n          __typename\n        }\n        badges {\n          type\n          displayText\n          __typename\n        }\n        trackingContext {\n          retailerContext {\n            id\n            __typename\n          }\n          advertContext {\n            id\n            advertiserId\n            advertiserType\n            make\n            model\n            vehicleCategory\n            year\n            condition\n            price\n            searchVersionId\n            __typename\n          }\n          card {\n            category\n            subCategory\n            pageNumber\n            position\n            __typename\n          }\n          advertCardFeatures {\n            condition\n            numImages\n            hasFinance\n            priceIndicator\n            isManufacturedApproved\n            isFranchiseApproved\n            __typename\n          }\n          distance {\n            distance\n            distance_unit\n            __typename\n          }\n          __typename\n        }\n        __typename\n      }\n      __typename\n    }\n    page {\n      number\n      count\n      results {\n        count\n        __typename\n      }\n      __typename\n    }\n    searchInfo {\n      isForFinanceSearch\n      leasingSummary\n      __typename\n    }\n    trackingContext {\n      searchId\n      __typename\n    }\n    __typename\n  }\n}',
    },
]

