# football_simulator_complete.py
# نظام محاكاة مسيرة كروية احترافي

import json
import random
from dataclasses import asdict, dataclass, field
from enum import Enum
from typing import Dict, List, Optional, Tuple


class Position(Enum):
    STRIKER = "مهاجم رأس حربة"
    WINGER = "جناح"
    MIDFIELDER = "وسط الملعب"
    DEFENDER = "مدافع"
    GOALKEEPER = "حارس مرمى"


CLUBS_DATABASE = {
    "الهلال": {"country": "السعودية", "continent": "آسيا", "tier": 1, "budget": 150},
    "النصر": {"country": "السعودية", "continent": "آسيا", "tier": 1, "budget": 120},
    "الاتحاد": {"country": "السعودية", "continent": "آسيا", "tier": 1, "budget": 110},
    "الشباب": {"country": "السعودية", "continent": "آسيا", "tier": 1, "budget": 100},
    "ريال مدريد": {"country": "إسبانيا", "continent": "أوروبا", "tier": 1, "budget": 500},
    "برشلونة": {"country": "إسبانيا", "continent": "أوروبا", "tier": 1, "budget": 480},
    "أتلتيكو مدريد": {"country": "إسبانيا", "continent": "أوروبا", "tier": 1, "budget": 350},
    "إشبيلية": {"country": "إسبانيا", "continent": "أوروبا", "tier": 1, "budget": 250},
    "يوفنتوس": {"country": "إيطاليا", "continent": "أوروبا", "tier": 1, "budget": 450},
    "إنتر ميلان": {"country": "إيطاليا", "continent": "أوروبا", "tier": 1, "budget": 420},
    "ميلان": {"country": "إيطاليا", "continent": "أوروبا", "tier": 1, "budget": 400},
    "نابولي": {"country": "إيطاليا", "continent": "أوروبا", "tier": 1, "budget": 350},
    "بايرن ميونخ": {"country": "ألمانيا", "continent": "أوروبا", "tier": 1, "budget": 480},
    "بوروسيا دورتموند": {"country": "ألمانيا", "continent": "أوروبا", "tier": 1, "budget": 350},
    "باريس سان جيرمان": {"country": "فرنسا", "continent": "أوروبا", "tier": 1, "budget": 500},
    "مانشستر سيتي": {"country": "إنجلترا", "continent": "أوروبا", "tier": 1, "budget": 520},
    "مانشستر يونايتد": {"country": "إنجلترا", "continent": "أوروبا", "tier": 1, "budget": 500},
    "ليفربول": {"country": "إنجلترا", "continent": "أوروبا", "tier": 1, "budget": 480},
    "تشيلسي": {"country": "إنجلترا", "continent": "أوروبا", "tier": 1, "budget": 450},
    "آرسنال": {"country": "إنجلترا", "continent": "أوروبا", "tier": 1, "budget": 420},
    "توتنهام": {"country": "إنجلترا", "continent": "أوروبا", "tier": 1, "budget": 400},
    "أياكس أمستردام": {"country": "هولندا", "continent": "أوروبا", "tier": 1, "budget": 350},
    "بنفيكا": {"country": "البرتغال", "continent": "أوروبا", "tier": 1, "budget": 380},
    "بورتو": {"country": "البرتغال", "continent": "أوروبا", "tier": 1, "budget": 360},
    "بوكا جونيورز": {"country": "الأرجنتين", "continent": "أمريكا الجنوبية", "tier": 1, "budget": 380},
    "فلامينغو": {"country": "البرازيل", "continent": "أمريكا الجنوبية", "tier": 1, "budget": 400},
    "الأهلي": {"country": "مصر", "continent": "أفريقيا", "tier": 1, "budget": 140},
    "الزمالك": {"country": "مصر", "continent": "أفريقيا", "tier": 1, "budget": 130},
}


@dataclass
class PlayerStats:
    pace: int
    shooting: int
    passing: int
    dribbling: int
    defense: int
    physical: int

    def overall(self) -> int:
        values = (self.pace, self.shooting, self.passing, self.dribbling,
                  self.defense, self.physical)
        return int(sum(values) / len(values))

    def improve(self, attribute: str, amount: int) -> None:
        if not hasattr(self, attribute):
            raise ValueError(f"الإحصائية غير موجودة: {attribute}")
        setattr(self, attribute, max(1, min(99, getattr(self, attribute) + amount)))


@dataclass
class IndividualAwards:
    ballon_dor: List[Tuple[int, int]] = field(default_factory=list)
    golden_boot: List[Tuple[int, int]] = field(default_factory=list)
    golden_boy: List[Tuple[int, bool]] = field(default_factory=list)
    best_young_player: List[Tuple[int, bool]] = field(default_factory=list)
    league_best_player: List[Tuple[int, str]] = field(default_factory=list)
    team_of_year: List[Tuple[int, bool]] = field(default_factory=list)


@dataclass
class TeamAwards:
    league_titles: List[int] = field(default_factory=list)
    cup_titles: List[int] = field(default_factory=list)
    champions_league: List[int] = field(default_factory=list)
    continental_cups: List[int] = field(default_factory=list)


@dataclass
class SeasonRecord:
    season: int
    age: int
    club: str
    appearances: int = 0
    goals: int = 0
    assists: int = 0
    yellow_cards: int = 0
    red_cards: int = 0
    average_rating: float = 0.0
    competitions: Dict[str, Dict] = field(default_factory=dict)

    def minutes_played(self) -> int:
        return self.appearances * 90


@dataclass
class Contract:
    club: str
    start_year: int
    duration_years: int
    weekly_salary: int
    market_value: int

    def is_active(self, current_year: int) -> bool:
        return self.start_year <= current_year < self.start_year + self.duration_years

    def years_remaining(self, current_year: int) -> int:
        return max(0, self.start_year + self.duration_years - current_year)


@dataclass
class Player:
    name: str
    nationality: str
    position: Position
    preferred_foot: str
    birth_year: int
    current_year: int
    stats: PlayerStats
    career_history: List[Contract] = field(default_factory=list)
    season_records: List[SeasonRecord] = field(default_factory=list)
    individual_awards: IndividualAwards = field(default_factory=IndividualAwards)
    team_awards: TeamAwards = field(default_factory=TeamAwards)
    total_goals: int = 0
    total_assists: int = 0
    total_appearances: int = 0
    total_trophies: int = 0

    def age(self) -> int:
        return self.current_year - self.birth_year

    def can_retire(self) -> bool:
        return self.age() >= 35

    def current_contract(self) -> Optional[Contract]:
        active = [c for c in self.career_history if c.is_active(self.current_year)]
        return active[-1] if active else None

    def current_club(self) -> str:
        contract = self.current_contract()
        return contract.club if contract else "بدون نادي"

    def market_value(self) -> int:
        age_factor = 1.0 if 24 <= self.age() <= 28 else (0.8 if self.age() > 30 else 0.9)
        return int((self.stats.overall() * 2 + self.total_trophies * 5) * age_factor)


class FootballSimulator:
    def __init__(self):
        self.player: Optional[Player] = None
        self.current_season = 1

    def generate_player(self, name: Optional[str] = None,
                        position: Optional[Position] = None) -> Player:
        names = ["محمد", "أحمد", "علي", "سارة", "ياسين", "فهد"]
        name = name or f"{random.choice(names)} {random.randint(1, 999)}"
        position = position or random.choice(list(Position))
        base = {
            Position.STRIKER: {"shooting": 75, "pace": 78, "dribbling": 76},
            Position.WINGER: {"pace": 80, "dribbling": 78, "shooting": 72},
            Position.MIDFIELDER: {"passing": 78, "pace": 75, "dribbling": 75},
            Position.DEFENDER: {"defense": 75, "physical": 76, "pace": 73},
            Position.GOALKEEPER: {"defense": 72, "physical": 75, "passing": 60},
        }[position]
        stats = PlayerStats(**{
            key: base.get(key, default) + random.randint(-5, 5)
            for key, default in {
                "pace": 70, "shooting": 65, "passing": 68,
                "dribbling": 70, "defense": 68, "physical": 72,
            }.items()
        })
        player = Player(name, "سعودي", position, random.choice(["يسار", "يمين"]),
                        2007, 2024, stats)
        club = random.choice(list(CLUBS_DATABASE))
        player.career_history.append(Contract(club, 2024, 3, 15, 2))
        self.player = player
        self.current_season = 1
        return player

    def calculate_individual_awards(self, record: SeasonRecord) -> List[str]:
        if not self.player:
            return []
        player = self.player
        awards = player.individual_awards
        result: List[str] = []
        goal_score = record.goals + record.assists

        if record.goals >= 20:
            awards.golden_boot.append((record.season, 1))
            result.append("الحذاء الذهبي")
        elif record.goals >= 15:
            rank = random.randint(2, 5)
            awards.golden_boot.append((record.season, rank))
            result.append(f"المركز {rank} في الحذاء الذهبي")

        if record.age <= 21 and record.average_rating >= 7.2 and player.stats.overall() >= 75:
            awards.best_young_player.append((record.season, True))
            result.append("أفضل لاعب شاب")
        if record.age <= 21 and goal_score >= 20 and player.stats.overall() >= 78:
            awards.golden_boy.append((record.season, True))
            result.append("الفتى الذهبي")
        if record.average_rating >= 7.3 and player.stats.overall() >= 80:
            awards.team_of_year.append((record.season, True))
            result.append("فريق الموسم")

        performance = (record.goals * 2.5 + record.assists * 1.5 +
                       record.average_rating * 10 + player.stats.overall() * 0.7 +
                       player.total_trophies * 3)
        if performance >= 145:
            rank = random.randint(1, 3)
            awards.ballon_dor.append((record.season, rank))
            result.append(f"الكرة الذهبية - المركز {rank}")
        elif performance >= 120:
            rank = random.randint(4, 10)
            awards.ballon_dor.append((record.season, rank))
            result.append(f"الكرة الذهبية - المركز {rank}")

        if record.goals * 2 + record.assists * 1.5 + record.average_rating * 8 >= 100:
            country = CLUBS_DATABASE.get(record.club, {}).get("country", "الدوري المحلي")
            awards.league_best_player.append((record.season, country))
            result.append("أفضل لاعب في الدوري")
        return result

    def calculate_team_awards(self, record: SeasonRecord) -> List[str]:
        if not self.player:
            return []
        data = CLUBS_DATABASE.get(record.club, {})
        strength = data.get("tier", 3) * 10 + data.get("budget", 50) / 20
        score = strength + self.player.stats.overall() / 10 + record.average_rating
        awards = self.player.team_awards
        result: List[str] = []

        probabilities = {
            "league": min(0.75, 0.15 + score / 200),
            "cup": min(0.65, 0.10 + score / 250),
            "champions": min(0.45, 0.03 + score / 350),
            "continental": min(0.35, 0.02 + score / 400),
        }
        if random.random() < probabilities["league"]:
            awards.league_titles.append(record.season)
            result.append("بطولة الدوري")
        if random.random() < probabilities["cup"]:
            awards.cup_titles.append(record.season)
            result.append("بطولة الكأس")

        continent = data.get("continent")
        if continent == "أوروبا" and random.random() < probabilities["champions"]:
            awards.champions_league.append(record.season)
            result.append("دوري أبطال أوروبا")
        elif random.random() < probabilities["continental"]:
            awards.continental_cups.append(record.season)
            result.append("بطولة قارية")

        self.player.total_trophies = sum(len(values) for values in asdict(awards).values())
        return result

    def simulate_season(self) -> Dict:
        if not self.player:
            return {"error": "لم يتم إنشاء لاعب بعد"}
        player = self.player
        club_before = player.current_club()
        appearances = random.randint(30, 38)
        position_factor = 1.25 if player.position in (Position.STRIKER, Position.WINGER) else 0.65
        goals = min(appearances, int(random.randint(0, max(1, appearances // 3)) * position_factor))
        assists = random.randint(0, max(1, appearances // 5))
        rating = round(6.5 + random.uniform(-1, 1.5), 1)
        for attribute in ("pace", "shooting", "passing", "dribbling", "defense", "physical"):
            player.stats.improve(attribute, random.randint(-2, 3))

        record = SeasonRecord(self.current_season, player.age(), club_before, appearances,
                              goals, assists, random.randint(0, 5), random.randint(0, 1), rating)
        player.season_records.append(record)
        player.total_goals += goals
        player.total_assists += assists
        player.total_appearances += appearances
        individual = self.calculate_individual_awards(record)
        team = self.calculate_team_awards(record)
        player.current_year += 1
        self.current_season += 1
        self._renew_or_transfer()
        return {"season": record.season, "club": club_before, "age": record.age,
                "appearances": appearances, "goals": goals, "assists": assists,
                "rating": rating, "overall": player.stats.overall(),
                "market_value": player.market_value(),
                "individual_awards": individual, "team_awards": team}

    def _renew_or_transfer(self) -> None:
        if not self.player or self.player.current_contract():
            return
        old_club = self.player.current_club()
        choices = [club for club in CLUBS_DATABASE if club != old_club]
        new_club = random.choice(choices)
        duration = random.randint(2, 5)
        self.player.career_history.append(
            Contract(new_club, self.player.current_year, duration,
                     max(15, self.player.market_value() // 3), self.player.market_value())
        )

    def retire_player(self) -> Dict:
        if not self.player:
            return {"error": "لم يتم إنشاء لاعب بعد"}
        if not self.player.can_retire():
            return {"error": "لا يمكن الاعتزال قبل عمر 35 سنة", "current_age": self.player.age()}
        return self.career_summary()

    def career_summary(self) -> Dict:
        if not self.player:
            return {}
        p = self.player
        return {"name": p.name, "age": p.age(), "club": p.current_club(),
                "goals": p.total_goals, "assists": p.total_assists,
                "appearances": p.total_appearances, "trophies": p.total_trophies,
                "individual_awards": asdict(p.individual_awards),
                "team_awards": asdict(p.team_awards)}

    def export_to_json(self) -> str:
        if not self.player:
            return "{}"
        p = self.player
        data = {"name": p.name, "nationality": p.nationality,
                "position": p.position.value, "preferred_foot": p.preferred_foot,
                "birth_year": p.birth_year, "current_year": p.current_year,
                "age": p.age(), "current_club": p.current_club(),
                "stats": {**asdict(p.stats), "overall": p.stats.overall()},
                "career_history": [asdict(c) for c in p.career_history],
                "season_records": [asdict(s) for s in p.season_records],
                "individual_awards": asdict(p.individual_awards),
                "team_awards": asdict(p.team_awards),
                "totals": {"goals": p.total_goals, "assists": p.total_assists,
                           "appearances": p.total_appearances, "trophies": p.total_trophies}}
        return json.dumps(data, ensure_ascii=False, indent=4)


if __name__ == "__main__":
    simulator = FootballSimulator()
    player = simulator.generate_player(name="لاعب تجريبي", position=Position.STRIKER)
    print(f"تم إنشاء اللاعب: {player.name} - {player.current_club()}")
    for _ in range(3):
        print(json.dumps(simulator.simulate_season(), ensure_ascii=False, indent=2))
    with open("player_career.json", "w", encoding="utf-8") as file:
        file.write(simulator.export_to_json())
    print("تم حفظ المسيرة في player_career.json")
