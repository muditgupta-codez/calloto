def generate_booking_link(customer_id: int, business_name: str) -> str:
    return f"https://calloto.com/book/{customer_id}?name={business_name}"
