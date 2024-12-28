# the seasons starts at jully 1st for the current year and
#  ends at december 31st or 30th for the next year

#   wee need to create at 5 seasons for each year
#   which can be eg: july 1st 2024- july 1st 2025- july 1st 2026- july 1st 2027- july 1st 2028
#   we can create a loop to create each season

#  if we have 5 seasons from the db already created then we list all of them
#  else we create 5 seasons for the current year and 4 seasons for the next year
from datetime import datetime, timedelta

from bm_hunting_settings.serializers import CreateSeasonsSerializer


class SeasonCreationHandler:
    def create_seasons(_self, request):
        current_year = datetime.now().year
        seasons = []

        # Check if we already have 5 seasons in the database
        existing_seasons = SeasonCreationHandler.get_existing_seasons(
            _self
        )  # This function should retrieve existing seasons from the database
        start_date = datetime(current_year, 7, 1)

        if existing_seasons:
            # Find the season with the highest year
            highest_year_season = max(
                existing_seasons, key=lambda season: season.end_at.year
            )
            season_len = len(existing_seasons)
            _is_highest_year_current_year = (
                highest_year_season.end_at.year == current_year
            )
            if season_len >= 5 and _is_highest_year_current_year == False:
                return existing_seasons

            # Start from July 1st of the current year
            elif _is_highest_year_current_year:
                SeasonCreationHandler.update_seasons(seasons, _self, 4, start_date)
        else:
            SeasonCreationHandler.update_seasons(seasons, _self, 5, start_date)

        # Save newly created seasons if any have been added
        if len(seasons) != 0:
            SeasonCreationHandler.save_seasons_to_db(seasons, _self)

        return seasons

    @staticmethod
    def update_seasons(
        seasons, _self, number_of_seasons, start_date=datetime(2024, 7, 1)
    ):
        for i in range(number_of_seasons):  # Creating 4 seasons
            end_date = start_date + timedelta(days=364)  # Seasons end after 364 days
            seasons.append(
                {
                    "start_date": start_date,
                    "end_date": end_date,
                }
            )
            start_date = start_date.replace(year=start_date.year + 1)

    @staticmethod
    def get_existing_seasons(_self):
        return _self.get_queryset()

    @staticmethod
    def save_seasons_to_db(seasons, _self):

        try:

            for season in seasons:
                print(
                    f"Season from {season['start_date'].date()} to {season['end_date'].date()}"
                )
                data = {
                    # get only the tim year from date
                    "name": f"Season {season['start_date'].year}"
                    + "-"
                    + f"{season['end_date'].year}",
                    "start_at": season["start_date"].date(),
                    "end_at": season["end_date"].date(),
                    "description": f"This season starts on {season['start_date'].date()} and ends on {season['end_date'].date()}",
                }
                create_season_sz = CreateSeasonsSerializer(data=data)
                if create_season_sz.is_valid():
                    create_season_sz.save()
                else:
                    raise ValueError(create_season_sz.errors)
        except Exception as e:
            raise ValueError(f"Error while saving seasons to the database: {e}")
