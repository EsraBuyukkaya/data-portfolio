from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "data"


def load_data():
    editions = pd.read_csv(DATA_DIR / "world_cup_editions.csv")
    teams = pd.read_csv(DATA_DIR / "team_summary.csv")
    players = pd.read_csv(DATA_DIR / "highest_paid_players_2025.csv")
    return editions, teams, players


def build_visibility_table(teams: pd.DataFrame) -> pd.DataFrame:
    scored = teams.copy()
    scored["visibility_score"] = (
        scored["titles"] * 5 + scored["finals"] * 3 + scored["appearances"]
    )
    return scored.sort_values("visibility_score", ascending=False)


def join_player_country_context(players: pd.DataFrame, teams: pd.DataFrame) -> pd.DataFrame:
    return players.merge(
        teams[["team", "titles", "finals", "appearances"]],
        left_on="country",
        right_on="team",
        how="left",
    ).drop(columns=["team"])


def main():
    editions, teams, players = load_data()
    visibility = build_visibility_table(teams)
    player_context = join_player_country_context(players, teams)

    print("World Cup titles by country")
    print(teams.sort_values("titles", ascending=False)[["team", "titles", "finals"]].head(10))
    print()

    print("World Cup visibility score")
    print(visibility[["team", "region", "titles", "finals", "appearances", "visibility_score"]].head(10))
    print()

    print("Highest-paid footballers with national-team context")
    print(player_context[["player", "country", "total_earnings_musd", "titles", "finals"]])
    print()

    print("Titles by region")
    print(editions.groupby("winner_region").size().sort_values(ascending=False))


if __name__ == "__main__":
    main()
