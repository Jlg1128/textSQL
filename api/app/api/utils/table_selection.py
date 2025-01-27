import json
from typing import List
from .messages import get_assistant_message, extract_code_from_markdown


MSG_WITH_DESCRIPTIONS = (
    "Return a JSON object with relevant SQL tables for answering the following natural language query: {natural_language_query}"
    " Respond in JSON format with your answer in a field named \"tables\" which is a list of strings."
    " Respond with an empty list if you cannot identify any relevant tables."
    " Write your answer in markdown format."
    "\n"
    "The following are descriptions of available tables:\n"
    "---------------------\n"
    "Description of table 'crime_by_city':\n"
    "Table 'crime_by_city' has city-level crime data in the United States."
    " It has numbers for violent crime, murder and nonnegligent manslaughter, rape, robbery, aggravated assault, property crime, burglary, larceny theft, motor vehicle theft, and arson."
    "Table 'crime_by_city' has columns: city (TEXT), violent_crime (DOUBLE_PRECISION), murder_and_nonnegligent_manslaughter (DOUBLE_PRECISION), rape (DOUBLE_PRECISION), robbery (DOUBLE_PRECISION), aggravated_assault (DOUBLE_PRECISION), property_crime (DOUBLE_PRECISION), burglary (DOUBLE_PRECISION), larceny_theft (DOUBLE_PRECISION), motor_vehicle_theft (DOUBLE_PRECISION), arson (DOUBLE_PRECISION), state (TEXT)."

    "\n\n"
    "Description of table 'acs_census_data':\n"
    "Table 'acs_census_data' has zip-code level data about average household sizes, income, and population grouped by gender, age, and race."
    "Table 'acs_census_data' has columns: total_population (DOUBLE_PRECISION), elderly_population (DOUBLE_PRECISION), male_population (DOUBLE_PRECISION), female_population (DOUBLE_PRECISION), white_population (DOUBLE_PRECISION), black_population (DOUBLE_PRECISION), native_american_population (DOUBLE_PRECISION), asian_population (DOUBLE_PRECISION), two_or_more_population (DOUBLE_PRECISION), hispanic_population (DOUBLE_PRECISION), adult_population (DOUBLE_PRECISION), citizen_adult_population (DOUBLE_PRECISION), average_household_size (DOUBLE_PRECISION), population_under_5_years (DOUBLE_PRECISION), population_5_to_9_years (DOUBLE_PRECISION), population_10_to_14_years (DOUBLE_PRECISION), population_15_to_19_years (DOUBLE_PRECISION), population_20_to_24_years (DOUBLE_PRECISION), population_25_to_34_years (DOUBLE_PRECISION), population_35_to_44_years (DOUBLE_PRECISION), population_45_to_54_years (DOUBLE_PRECISION), population_55_to_59_years (DOUBLE_PRECISION), population_60_to_64_years (DOUBLE_PRECISION), population_65_to_74_years (DOUBLE_PRECISION), population_75_to_84_years (DOUBLE_PRECISION), population_85_years_and_over (DOUBLE_PRECISION), per_capita_income (DOUBLE_PRECISION), median_income_for_workers (DOUBLE_PRECISION), zip_code (TEXT), city (TEXT), state (TEXT), county (TEXT), lat (DOUBLE_PRECISION), lon (DOUBLE_PRECISION)."
    "\n\n"
    "---------------------\n"
)

DEFAULT_MESSAGES = [
    {
        "role": "system",
        "content": (
                "You are a helpful assistant for identifying relevant SQL tables to use for answering a natural language query."
                " You respond in JSON format with your answer in a field named \"tables\" which is a list of strings."
                " Respond with an empty list if you cannot identify any relevant tables."
                " Write your answer in markdown format."
                "\n"
                "The following are descriptions of available tables:\n"
                "---------------------\n"
                "Description of table 'crime_by_city':\n"
                "Table 'crime_by_city' has city-level crime data in the United States."
                " It has numbers for violent crime, murder and nonnegligent manslaughter, rape, robbery, aggravated assault, property crime, burglary, larceny theft, motor vehicle theft, and arson."
                "Table 'crime_by_city' has columns: city (TEXT), violent_crime (DOUBLE_PRECISION), murder_and_nonnegligent_manslaughter (DOUBLE_PRECISION), rape (DOUBLE_PRECISION), robbery (DOUBLE_PRECISION), aggravated_assault (DOUBLE_PRECISION), property_crime (DOUBLE_PRECISION), burglary (DOUBLE_PRECISION), larceny_theft (DOUBLE_PRECISION), motor_vehicle_theft (DOUBLE_PRECISION), arson (DOUBLE_PRECISION), state (TEXT)."

                "\n\n"
                "Description of table 'acs_census_data':\n"
                "Table 'acs_census_data' has zip-code level data about average household sizes, income, and population grouped by gender, age, and race."
                "Table 'acs_census_data' has columns: total_population (DOUBLE_PRECISION), elderly_population (DOUBLE_PRECISION), male_population (DOUBLE_PRECISION), female_population (DOUBLE_PRECISION), white_population (DOUBLE_PRECISION), black_population (DOUBLE_PRECISION), native_american_population (DOUBLE_PRECISION), asian_population (DOUBLE_PRECISION), two_or_more_population (DOUBLE_PRECISION), hispanic_population (DOUBLE_PRECISION), adult_population (DOUBLE_PRECISION), citizen_adult_population (DOUBLE_PRECISION), average_household_size (DOUBLE_PRECISION), population_under_5_years (DOUBLE_PRECISION), population_5_to_9_years (DOUBLE_PRECISION), population_10_to_14_years (DOUBLE_PRECISION), population_15_to_19_years (DOUBLE_PRECISION), population_20_to_24_years (DOUBLE_PRECISION), population_25_to_34_years (DOUBLE_PRECISION), population_35_to_44_years (DOUBLE_PRECISION), population_45_to_54_years (DOUBLE_PRECISION), population_55_to_59_years (DOUBLE_PRECISION), population_60_to_64_years (DOUBLE_PRECISION), population_65_to_74_years (DOUBLE_PRECISION), population_75_to_84_years (DOUBLE_PRECISION), population_85_years_and_over (DOUBLE_PRECISION), per_capita_income (DOUBLE_PRECISION), median_income_for_workers (DOUBLE_PRECISION), zip_code (TEXT), city (TEXT), state (TEXT), county (TEXT), lat (DOUBLE_PRECISION), lon (DOUBLE_PRECISION)."
                "\n\n"
                "---------------------\n"
            )
    },
    {
        "role": "user",
        "content": "Which top 5 cities have the most total crime?"
    },
    {
        "role": "assistant",
        "content": '```\n{\n    "tables": ["crime_by_city"]\n}\n```'
    },
    {
        "role": "user",
        "content": "What zip code has the highest percentage of people of age 75?"
    },
    {
        "role": "assistant",
        "content": '```\n{\n    "tables": ["acs_census_data"]\n}\n```'
    },
    {
        "role": "user",
        "content": "Which 5 counties have the most arson?"
    },
    {
        "role": "assistant",
        "content": '```\n{\n    "tables": ["crime_by_city", "acs_census_data"]\n}\n```'
    },
]


def get_relevant_tables(natural_language_query) -> List[str]:
    """
    Identify relevant tables for answering a natural language query
    """
    natural_language_query = "Which city has the guys with the biggest dicks?"

    content = MSG_WITH_DESCRIPTIONS.format(natural_language_query=natural_language_query)

    messages = DEFAULT_MESSAGES.copy()
    messages.append({
        "role": "user",
        "content": content
    })

    assistant_message_content = get_assistant_message(messages=messages)['message']['content']
    tables_json_str = extract_code_from_markdown(assistant_message_content)
    tables = json.loads(tables_json_str).get('tables')
    return tables