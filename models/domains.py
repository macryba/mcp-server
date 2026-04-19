#!/usr/bin/env python3
"""
Centralized domain registry for Polish History MCP Server
Single source of truth for all historical source domains with metadata
"""

from dataclasses import dataclass, field
from enum import Enum
from typing import List, Set, Dict
import json


class Category(str, Enum):
    """Domain categories based on content type and educational purpose"""

    # serwisy do systematycznej nauki historii Polski, z artykułami,
    # materiałami dydaktycznymi i treściami dla uczniów oraz nauczycieli
    OGOLNOEDUKACYJNE = "ogolnoedukacyjne"

    # serwisy tłumaczące historię Polski w przystępny sposób,
    # z naciskiem na narrację, kontekst i popularyzację wiedzy
    POPULARNONAUKOWE = "popularnonaukowe"

    # portale z tekami edukacyjnymi, wystawami, infografikami,
    # gotowymi materiałami do pracy szkolnej i samodzielnej nauki
    SZKOLNE_MATERIALY = "szkolne_materialy"

    # serwisy przydatne, gdy chcesz uczyć się historii Polski przez ludzi,
    # elity, działaczy, świadków epok i bohaterów wydarzeń
    BIOGRAFIE_POSTACIE = "biografie_postacie"

    # portale oparte na relacjach, dokumentach, fotografiach, filmach
    # i materiałach źródłowych, pomocne do pracy ze źródłem historycznym
    ZRODLA_SWIADECTWA = "zrodla_swiadectwa"


class Difficulty(str, Enum):
    """Poziomy trudności (Difficulty levels)"""

    EASY = "łatwy"      # łatwy - szkoła podstawowa
    MEDIUM = "średni"   # średni - podstawa programowa / matura
    HARD = "trudny"     # trudny - treści wykraczające poza podręczniki


@dataclass(frozen=True)
class Domain:
    """Complete metadata for a historical source domain"""

    name: str
    base_url: str
    description: str
    categories: Set[Category] = field(default_factory=set)
    difficulties: Set[Difficulty] = field(default_factory=set)
    tags: Set[str] = field(default_factory=set)

    # Search capability flags
    supports_api_search: bool = False      # Has official API for programmatic search
    supports_web_scraping: bool = False    # Can be scraped for content extraction
    supports_url_extraction: bool = False  # Can extract content from specific URLs

    language: str = "pl"
    central_for_ai: bool = False


# Central registry of all Polish history source domains
DOMAINS: List[Domain] = [
    Domain(
        name="Wikipedia",
        base_url="https://pl.wikipedia.org",
        description=(
            "Polskojęzyczna encyklopedia internetowa, dobra jako centralny punkt startowy "
            "dla agenta AI: szybkie wprowadzenie do epok, wydarzeń i postaci historycznych."
        ),
        categories={
            Category.OGOLNOEDUKACYJNE,
            Category.POPULARNONAUKOWE,
            Category.BIOGRAFIE_POSTACIE,
        },
        difficulties={Difficulty.EASY, Difficulty.MEDIUM},
        tags={
            "wikipedia",
            "encyklopedia",
            "biogramy",
            "wydarzenia",
            "przeglad_tematow",
            "api",
        },
        supports_api_search=True,
        supports_web_scraping=True,
        supports_url_extraction=True,
        language="pl",
        central_for_ai=True,
    ),
    Domain(
        name="Edukacja IPN",
        base_url="https://edukacja.ipn.gov.pl",
        description=(
            "Usystematyzowany portal edukacyjny IPN z tekami edukacyjnymi, wystawami, "
            "infografikami, lekcjami i historią mówioną."
        ),
        categories={
            Category.OGOLNOEDUKACYJNE,
            Category.SZKOLNE_MATERIALY,
            Category.ZRODLA_SWIADECTWA,
        },
        difficulties={Difficulty.MEDIUM, Difficulty.HARD},
        tags={
            "ipn",
            "lekcje",
            "teki_edukacyjne",
            "historia_mowiona",
            "xx_wiek",
            "materialy_edukacyjne",
        },
        supports_api_search=False,
        supports_web_scraping=True,
        supports_url_extraction=True,
        language="pl",
    ),
    Domain(
        name="Dzieje.pl",
        base_url="https://dzieje.pl",
        description=(
            "Serwis historyczny o historii Polski z artykułami, fotografiami, dokumentami, "
            "infografikami i materiałami o postaciach historycznych."
        ),
        categories={
            Category.POPULARNONAUKOWE,
            Category.BIOGRAFIE_POSTACIE,
            Category.ZRODLA_SWIADECTWA,
        },
        difficulties={Difficulty.MEDIUM, Difficulty.HARD},
        tags={
            "pap",
            "muzeum_historii_polski",
            "artykuly",
            "postacie",
            "mapy",
            "infografiki",
            "historia_polski",
        },
        supports_api_search=False,
        supports_web_scraping=True,
        supports_url_extraction=True,
        language="pl",
    ),
    Domain(
        name="Przystanek Historia",
        base_url="https://przystanekhistoria.pl",
        description=(
            "Popularnonaukowy portal IPN o historii Polski XX wieku z artykułami, "
            "publikacjami cyfrowymi, nagraniami i materiałami edukacyjnymi."
        ),
        categories={
            Category.POPULARNONAUKOWE,
            Category.SZKOLNE_MATERIALY,
            Category.ZRODLA_SWIADECTWA,
        },
        difficulties={Difficulty.MEDIUM, Difficulty.HARD},
        tags={
            "ipn",
            "publikacje_cyfrowe",
            "artykuly",
            "nagrania",
            "xx_wiek",
            "edukacja",
        },
        supports_api_search=False,
        supports_web_scraping=True,
        supports_url_extraction=True,
        language="pl",
    ),
    Domain(
        name="SuperKid - Historia online",
        base_url="https://www.superkid.pl/historia-online",
        description=(
            "Materiały i ćwiczenia online z historii dla młodszych uczniów, "
            "szczególnie przydatne na poziomie szkoły podstawowej."
        ),
        categories={
            Category.OGOLNOEDUKACYJNE,
            Category.SZKOLNE_MATERIALY,
        },
        difficulties={Difficulty.EASY},
        tags={
            "szkola_podstawowa",
            "cwiczenia",
            "quizy",
            "krzyzowki",
            "dzieci",
        },
        supports_api_search=False,
        supports_web_scraping=True,
        supports_url_extraction=True,
        language="pl",
    ),
    Domain(
        name="GWO - Historia",
        base_url="https://gwo.pl/przedmioty/historia/materialy-dydaktyczne/",
        description=(
            "Materiały dydaktyczne z historii dla szkoły podstawowej oraz liceum i technikum, "
            "powiązane z nauką szkolną i podstawą programową."
        ),
        categories={
            Category.SZKOLNE_MATERIALY,
            Category.OGOLNOEDUKACYJNE,
        },
        difficulties={Difficulty.EASY, Difficulty.MEDIUM},
        tags={
            "gwo",
            "szkola_podstawowa",
            "liceum",
            "technikum",
            "materialy_dydaktyczne",
            "podstawa_programowa",
        },
        supports_api_search=False,
        supports_web_scraping=True,
        supports_url_extraction=True,
        language="pl",
    ),
]


class DomainRegistry:
    """Central registry with query and filtering capabilities"""

    @classmethod
    def get_all_domains(cls) -> List[Domain]:
        """Get all registered domains"""
        return DOMAINS.copy()

    @classmethod
    def get_available_domains(cls) -> List[Domain]:
        """Get only available domains (currently implemented)"""
        return [d for d in DOMAINS if d.api_available]

    @classmethod
    def get_central_domains(cls) -> List[Domain]:
        """Get domains marked as central for AI operations"""
        return [d for d in DOMAINS if d.central_for_ai]

    @classmethod
    def get_domains_by_language(cls, language: str) -> List[Domain]:
        """Get domains filtered by language code"""
        return [d for d in DOMAINS if d.language == language]

    @classmethod
    def get_domains_with_api_search(cls) -> List[Domain]:
        """Get domains that support API search"""
        return [d for d in DOMAINS if d.supports_api_search]

    @classmethod
    def get_domains_with_web_scraping(cls) -> List[Domain]:
        """Get domains that support web scraping"""
        return [d for d in DOMAINS if d.supports_web_scraping]

    @classmethod
    def get_domains_with_url_extraction(cls) -> List[Domain]:
        """Get domains that support URL extraction"""
        return [d for d in DOMAINS if d.supports_url_extraction]

    @classmethod
    def get_trusted_urls(cls) -> Set[str]:
        """Get set of all trusted domain URLs"""
        return {d.base_url for d in DOMAINS}

    @classmethod
    def get_domains_by_category(cls, category: Category) -> List[Domain]:
        """Get domains filtered by category"""
        return [d for d in DOMAINS if category in d.categories]

    @classmethod
    def get_domains_by_difficulty(cls, difficulty: Difficulty) -> List[Domain]:
        """Get domains filtered by difficulty level"""
        return [d for d in DOMAINS if difficulty in d.difficulties]

    @classmethod
    def get_domains_by_tag(cls, tag: str) -> List[Domain]:
        """Get domains that contain a specific tag"""
        return [d for d in DOMAINS if tag in d.tags]

    @classmethod
    def filter_domains(
        cls,
        *,
        categories: Set[Category] | None = None,
        difficulties: Set[Difficulty] | None = None,
        languages: Set[str] | None = None,
        tags: Set[str] | None = None,
        require_all_categories: bool = False,
        require_all_difficulties: bool = False,
        require_api_search: bool = False,
        require_web_scraping: bool = False,
        require_url_extraction: bool = False,
        only_central: bool = False,
    ) -> List[Domain]:
        """
        Advanced filtering with multiple criteria

        Args:
            categories: Filter by categories (OR logic unless require_all_categories=True)
            difficulties: Filter by difficulties (OR logic unless require_all_difficulties=True)
            languages: Filter by language codes
            tags: Filter by tags (must match at least one)
            require_all_categories: Use AND logic for categories
            require_all_difficulties: Use AND logic for difficulties
            require_api_search: Only return domains with API search capability
            require_web_scraping: Only return domains with web scraping capability
            require_url_extraction: Only return domains with URL extraction capability
            only_central: Only return domains marked as central for AI

        Returns:
            Filtered list of domains
        """
        result = []

        for domain in DOMAINS:
            if require_api_search and not domain.supports_api_search:
                continue

            if require_web_scraping and not domain.supports_web_scraping:
                continue

            if require_url_extraction and not domain.supports_url_extraction:
                continue

            if only_central and not domain.central_for_ai:
                continue

            category_ok = True
            difficulty_ok = True
            language_ok = True
            tags_ok = True

            if categories:
                if require_all_categories:
                    category_ok = categories.issubset(domain.categories)
                else:
                    category_ok = bool(domain.categories.intersection(categories))

            if difficulties:
                if require_all_difficulties:
                    difficulty_ok = difficulties.issubset(domain.difficulties)
                else:
                    difficulty_ok = bool(domain.difficulties.intersection(difficulties))

            if languages:
                language_ok = domain.language in languages

            if tags:
                tags_ok = bool(domain.tags.intersection(tags))

            if category_ok and difficulty_ok and language_ok and tags_ok:
                result.append(domain)

        return result

    @classmethod
    def get_domain_by_url(cls, url: str) -> Domain | None:
        """Find domain by base URL"""
        for domain in DOMAINS:
            if domain.base_url == url:
                return domain
        return None

    @classmethod
    def get_suggested_domains_for_tool(
        cls,
        tool_type: str,
        context: str | None = None
    ) -> List[str]:
        """
        Get suggested domains for specific tool types

        Args:
            tool_type: Type of tool (search_historical_figures, search_historical_events, etc.)
            context: Additional context for better suggestions

        Returns:
            List of domain URLs suggested for this tool
        """
        if tool_type == "search_historical_figures":
            # Suggest domains good for biographical content
            domains = cls.filter_domains(
                categories={Category.BIOGRAFIE_POSTACIE, Category.OGOLNOEDUKACYJNE},
                require_api_search=True
            )
        elif tool_type == "search_historical_events":
            # Suggest domains good for events
            domains = cls.filter_domains(
                categories={Category.POPULARNONAUKOWE, Category.OGOLNOEDUKACYJNE},
                require_api_search=True
            )
        elif tool_type == "search_biographies":
            # Suggest domains specifically for biographies
            domains = cls.filter_domains(
                categories={Category.BIOGRAFIE_POSTACIE},
                require_api_search=True
            )
        elif tool_type == "search_primary_sources":
            # Suggest domains for primary sources
            domains = cls.filter_domains(
                categories={Category.ZRODLA_SWIADECTWA},
                require_api_search=True
            )
        else:
            # Default to central domains
            domains = cls.get_central_domains()

        return [d.base_url for d in domains]

    @classmethod
    def to_dict(cls, domain: Domain) -> dict:
        """Convert domain to dictionary"""
        return {
            "name": domain.name,
            "base_url": domain.base_url,
            "description": domain.description,
            "categories": sorted(c.value for c in domain.categories),
            "difficulties": sorted(d.value for d in domain.difficulties),
            "tags": sorted(domain.tags),
            "supports_api_search": domain.supports_api_search,
            "supports_web_scraping": domain.supports_web_scraping,
            "supports_url_extraction": domain.supports_url_extraction,
            "language": domain.language,
            "central_for_ai": domain.central_for_ai,
        }

    @classmethod
    def to_json(cls, domains: List[Domain] | None = None) -> str:
        """Convert domains to JSON string"""
        if domains is None:
            domains = DOMAINS
        return json.dumps([cls.to_dict(d) for d in domains], ensure_ascii=False, indent=2)


# Convenience functions for backward compatibility
def get_trusted_domains() -> Set[str]:
    """Get set of trusted domain URLs (for config.py compatibility)"""
    return DomainRegistry.get_trusted_urls()


def get_available_domains() -> List[Domain]:
    """Get available domains (for tools/search.py compatibility)"""
    return DomainRegistry.get_domains_with_api_search()


if __name__ == "__main__":
    # Test and demonstrate the registry
    print("=== CENTRAL DOMAINS FOR AI ===")
    for d in DomainRegistry.get_central_domains():
        print(f"- {d.name} -> {d.base_url}")

    print("\n=== DOMAINS WITH API SEARCH ===")
    for d in DomainRegistry.get_domains_with_api_search():
        print(f"- {d.name} ({d.language})")

    print("\n=== DOMAINS WITH WEB SCRAPING ===")
    for d in DomainRegistry.get_domains_with_web_scraping():
        print(f"- {d.name} ({d.language})")

    print("\n=== DOMAINS WITH URL EXTRACTION ===")
    for d in DomainRegistry.get_domains_with_url_extraction():
        print(f"- {d.name} ({d.language})")

    print("\n=== EASY DIFFICULTY DOMAINS ===")
    for d in DomainRegistry.get_domains_by_difficulty(Difficulty.EASY):
        print(f"- {d.name}")

    print("\n=== POPULARNONAUKOWE + MEDIUM ===")
    for d in DomainRegistry.filter_domains(
        categories={Category.POPULARNONAUKOWE},
        difficulties={Difficulty.MEDIUM},
    ):
        print(f"- {d.name}")

    print("\n=== SUGGESTED FOR HISTORICAL FIGURES ===")
    for url in DomainRegistry.get_suggested_domains_for_tool("search_historical_figures"):
        print(f"- {url}")

    print("\n=== JSON OUTPUT ===")
    print(DomainRegistry.to_json())