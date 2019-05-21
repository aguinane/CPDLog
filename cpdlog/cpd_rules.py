CPD_TYPES = {
    "A": {
        "desc": "Tertiary Education",
        "desc_long": "Any tertiary course taken either as an individual course or for a formal post-graduate award",
        "limit": None,
        "conditions": "",
    },
    "B": {
        "desc": "Industry Education",
        "desc_long": "Short courses, workshops, seminars and discussion groups, conferences, technical inspections and technical meetings",
        "limit": None,
        "conditions": "",
    },
    "C": {
        "desc": "Workplace Learning",
        "desc_long": "Learning activities in the workplace that extend competence in the area of practice",
        "limit": 75,
        "conditions": "A maximum of 75 hours of your total CPD",
    },
    "D": {
        "desc": "Private Study",
        "desc_long": "Private study which extends your knowledge and skills",
        "limit": 35,
        "conditions": "The total claimable hours for Type III and IV combined are 110 hours",
    },
    "E": {
        "desc": "Service",
        "desc_long": "Service to the engineering profession",
        "limit": 50,
        "conditions": "A maximum of 50 hours of your total CPD",
    },
    "F": {
        "desc": "Presentations and papers",
        "desc_long": "The preparation and presentation of material for courses, conferences, seminars and symposia",
        "limit": None,
        "conditions": "Up to 45 hours per paper",
    },
    "G": {
        "desc": "Industry Involvement (for academics)",
        "desc_long": "Practitioners employed in tertiary teaching or academic research",
        "limit": None,
        "conditions": "Chartered members employed in tertiary teaching and/or academic research must be able to demonstrate a minimum of 40 hours of industry involvement",
    },
    "H": {
        "desc": "Other",
        "desc_long": "Any other structured activities not covered by I to VI above that meet the objectives of the CPD policy",
        "limit": None,
        "conditions": "Documentary evidence and a clear justification will be necessary",
    },
}


CPD_MINS = {
    "yrs": 3,
    "total": 150,
    "risk": 10,
    "area": 50,
    "bus": 15,
    "conditions": """
      Your CPD records must document a minimum of 150 hours of structured CPD over a three-year period
      at least 50 hours must relate to your area(s) of practice
      at least 10 hours must cover risk management
      at least 15 hours must address business and management skills
    """,
}
