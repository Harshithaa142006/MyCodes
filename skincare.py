from enum import Enum
from dataclasses import dataclass
from typing import List, Optional
import random


# Enums
class SkinType(Enum):
    OILY = "oily"
    DRY = "dry"
    NORMAL = "normal"
    SENSITIVE = "sensitive"
    COMBINATION = "combination"


class SkinConcern(Enum):
    ACNE = "acne"
    PIMPLES = "pimples"
    PIGMENTATION = "pigmentation"
    TANNING = "tanning"
    DARK_SPOTS = "dark_spots"
    DRYNESS = "dryness"
    DULLNESS = "dullness"
    WRINKLES = "wrinkles"
    MOISTURIZING = "moisturizing"


class BudgetRange(Enum):
    LOW = "low"  # Under $25
    MEDIUM = "medium"  # $25-50
    HIGH = "high"  # $50-100
    PREMIUM = "premium"  # $100+


@dataclass
class UserProfile:
    skin_type: Optional[SkinType] = None
    skin_tone: Optional[str] = None
    concerns: List[SkinConcern] = None
    budget: Optional[BudgetRange] = None


@dataclass
class Product:
    id: str
    name: str
    brand: str
    category: str
    price: float
    rating: float
    description: str
    ingredients: List[str]
    skin_types: List[SkinType]
    concerns: List[SkinConcern]
    image_url: str = ""


# Recommendation Engine
class SkincareRecommendationEngine:
    # Ingredient effectiveness mapping for concerns
    CONCERN_INGREDIENTS = {
        SkinConcern.ACNE: ["salicylic acid", "benzoyl peroxide", "niacinamide", "tea tree", "zinc"],
        SkinConcern.PIMPLES: ["salicylic acid", "benzoyl peroxide", "sulfur", "tea tree"],
        SkinConcern.PIGMENTATION: ["vitamin c", "niacinamide", "arbutin", "kojic acid", "azelaic acid"],
        SkinConcern.TANNING: ["vitamin c", "licorice extract", "kojic acid", "sunscreen"],
        SkinConcern.DARK_SPOTS: ["vitamin c", "retinol", "niacinamide", "hydroquinone", "azelaic acid"],
        SkinConcern.DRYNESS: ["hyaluronic acid", "ceramides", "squalane", "glycerin", "shea butter"],
        SkinConcern.DULLNESS: ["vitamin c", "aha", "glycolic acid", "lactic acid", "niacinamide"],
        SkinConcern.WRINKLES: ["retinol", "peptides", "vitamin c", "hyaluronic acid", "collagen"],
        SkinConcern.MOISTURIZING: ["hyaluronic acid", "ceramides", "glycerin", "aloe vera", "squalane"],
    }

    # Skin type compatibility scores
    SKIN_TYPE_WEIGHTS = {
        SkinType.OILY: {"lightweight": 1.5, "oil-free": 1.5, "mattifying": 1.3},
        SkinType.DRY: {"hydrating": 1.5, "moisturizing": 1.5, "nourishing": 1.3},
        SkinType.SENSITIVE: {"gentle": 1.5, "fragrance-free": 1.5, "soothing": 1.3},
        SkinType.COMBINATION: {"balancing": 1.3, "lightweight": 1.2},
        SkinType.NORMAL: {},  # No special weighting
    }

    def __init__(self, products: List[Product]):
        self.products = products

    def calculate_score(self, product: Product, profile: UserProfile) -> float:
        """Calculate recommendation score for a product based on user profile."""
        score = 0.0

        # 1. Skin type compatibility (0-30 points)
        if profile.skin_type and profile.skin_type in product.skin_types:
            score += 30
        elif profile.skin_type:
            score += 10  # Partial score if skin type not explicitly listed

        # 2. Concern matching (0-40 points)
        if profile.concerns:
            matching_concerns = set(profile.concerns) & set(product.concerns)
            concern_score = (len(matching_concerns) / len(profile.concerns)) * 40
            score += concern_score

            # Bonus for ingredient matching
            product_ingredients_lower = [ing.lower() for ing in product.ingredients]
            for concern in profile.concerns:
                beneficial_ingredients = self.CONCERN_INGREDIENTS.get(concern, [])
                for ingredient in beneficial_ingredients:
                    if any(ingredient in prod_ing for prod_ing in product_ingredients_lower):
                        score += 2  # Bonus per matching ingredient

        # 3. Budget alignment (0-20 points)
        if profile.budget:
            budget_ranges = {
                BudgetRange.LOW: (0, 25),
                BudgetRange.MEDIUM: (25, 50),
                BudgetRange.HIGH: (50, 100),
                BudgetRange.PREMIUM: (100, float('inf')),
            }
            min_price, max_price = budget_ranges[profile.budget]
            if min_price <= product.price <= max_price:
                score += 20
            elif product.price < min_price:
                score += 15  # Under budget is okay
            else:
                score += 5  # Over budget penalty

        # 4. Rating boost (0-10 points)
        score += (product.rating / 5) * 10

        return round(score, 2)

    def get_recommendations(
            self,
            profile: UserProfile,
            limit: int = 10,
            category: Optional[str] = None
    ) -> List[dict]:
        """Get personalized product recommendations."""

        # Filter by category if specified
        products = self.products
        if category:
            products = [p for p in products if p.category.lower() == category.lower()]

        # Calculate scores
        scored_products = []
        for product in products:
            score = self.calculate_score(product, profile)
            scored_products.append({
                "product": product,
                "score": score,
                "match_reasons": self._get_match_reasons(product, profile)
            })

        # Sort by score descending
        scored_products.sort(key=lambda x: x["score"], reverse=True)

        return scored_products[:limit]

    def _get_match_reasons(self, product: Product, profile: UserProfile) -> List[str]:
        """Generate human-readable reasons for the recommendation."""
        reasons = []

        if profile.skin_type and profile.skin_type in product.skin_types:
            reasons.append(f"Suitable for {profile.skin_type.value} skin")

        if profile.concerns:
            matching = set(profile.concerns) & set(product.concerns)
            for concern in matching:
                reasons.append(f"Targets {concern.value.replace('_', ' ')}")

        if product.rating >= 4.5:
            reasons.append("Highly rated by users")

        return reasons

    def get_routine(self, profile: UserProfile) -> dict:
        """Generate a complete skincare routine based on profile."""
        routine = {
            "morning": [],
            "evening": []
        }

        categories_morning = ["cleansers", "toners", "serums", "moisturizers", "sunscreens"]
        categories_evening = ["cleansers", "toners", "serums", "treatments", "moisturizers"]

        for category in categories_morning:
            recs = self.get_recommendations(profile, limit=1, category=category)
            if recs:
                routine["morning"].append(recs[0])

        for category in categories_evening:
            recs = self.get_recommendations(profile, limit=1, category=category)
            if recs:
                routine["evening"].append(recs[0])

        return routine


# Example usage
if __name__ == "__main__":
    # Sample products
    products = [
        Product(
            id="1",
            name="Hydrating Serum",
            brand="GlowLab",
            category="serums",
            price=35.0,
            rating=4.8,
            description="Intense hydration with hyaluronic acid",
            ingredients=["Hyaluronic Acid", "Vitamin B5", "Ceramides"],
            skin_types=[SkinType.DRY, SkinType.NORMAL, SkinType.COMBINATION],
            concerns=[SkinConcern.DRYNESS, SkinConcern.MOISTURIZING]
        ),
        Product(
            id="2",
            name="Vitamin C Brightening Serum",
            brand="RadiantSkin",
            category="serums",
            price=45.0,
            rating=4.6,
            description="Brightens and evens skin tone",
            ingredients=["Vitamin C", "Niacinamide", "Ferulic Acid"],
            skin_types=[SkinType.NORMAL, SkinType.OILY, SkinType.COMBINATION],
            concerns=[SkinConcern.PIGMENTATION, SkinConcern.DULLNESS, SkinConcern.DARK_SPOTS]
        ),
        Product(
            id="3",
            name="Acne Control Cleanser",
            brand="ClearDerm",
            category="cleansers",
            price=22.0,
            rating=4.5,
            description="Deep cleansing for acne-prone skin",
            ingredients=["Salicylic Acid", "Tea Tree Oil", "Zinc"],
            skin_types=[SkinType.OILY, SkinType.COMBINATION],
            concerns=[SkinConcern.ACNE, SkinConcern.PIMPLES]
        ),
    ]

    # Create engine
    engine = SkincareRecommendationEngine(products)

    # Create user profile
    user = UserProfile(
        skin_type=SkinType.OILY,
        skin_tone="medium",
        concerns=[SkinConcern.ACNE, SkinConcern.DARK_SPOTS],
        budget=BudgetRange.MEDIUM
    )

    # Get recommendations
    recommendations = engine.get_recommendations(user, limit=5)

    print("🧴 Personalized Recommendations:\n")
    for i, rec in enumerate(recommendations, 1):
        product = rec["product"]
        print(f"{i}. {product.name} by {product.brand}")
        print(f"   Score: {rec['score']} | Price: ${product.price} | Rating: {product.rating}⭐")
        print(f"   Reasons: {', '.join(rec['match_reasons'])}")
        print()
