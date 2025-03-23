def render_price(price_in_pence: float) -> str:
    price_in_pounds = price_in_pence / 100
    return f"£{price_in_pounds:.2f}"
