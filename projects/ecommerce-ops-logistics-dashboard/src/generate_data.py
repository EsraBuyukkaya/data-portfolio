from pathlib import Path
import sqlite3

import numpy as np
import pandas as pd


PROJECT_DIR = Path(__file__).resolve().parents[1]
DATA_DIR = PROJECT_DIR / "data"
OUTPUTS_DIR = PROJECT_DIR / "outputs"
DATA_DIR.mkdir(exist_ok=True)
OUTPUTS_DIR.mkdir(exist_ok=True)


RNG = np.random.default_rng(42)


def weighted_choice(values, probs, size):
    return RNG.choice(values, size=size, p=np.array(probs) / np.sum(probs))


def build_orders(n_orders=8500):
    dates = pd.date_range("2025-01-01", "2025-06-30", freq="D")
    product_lines = ["Signature Hoodie", "Cloud Sweatpants", "Zip Hoodie", "Lounge Set", "Weighted Tee"]
    countries = ["United States", "Canada", "United Kingdom", "Australia", "Germany"]
    fulfillment_centers = ["3PL_East", "3PL_West", "3PL_Central", "3PL_International"]
    carriers = ["Carrier_A", "Carrier_B", "Carrier_C", "Carrier_D", "Passport_Global"]
    promo_types = ["none", "email_drop", "influencer_drop", "holiday_sale", "product_launch"]

    order_dates = weighted_choice(
        dates,
        1 + (dates.dayofweek >= 4) * 0.2 + (dates.month.isin([3, 6])) * 0.35,
        n_orders,
    )
    promo = weighted_choice(promo_types, [0.62, 0.13, 0.09, 0.08, 0.08], n_orders)
    units = RNG.choice([1, 1, 1, 2, 2, 3, 4], n_orders)
    product = weighted_choice(product_lines, [0.38, 0.22, 0.17, 0.15, 0.08], n_orders)
    country = weighted_choice(countries, [0.78, 0.08, 0.06, 0.05, 0.03], n_orders)
    fc = np.where(country == "United States", weighted_choice(fulfillment_centers[:3], [0.42, 0.38, 0.2], n_orders), "3PL_International")
    carrier = np.where(country == "United States", weighted_choice(carriers[:4], [0.34, 0.31, 0.22, 0.13], n_orders), "Passport_Global")

    unit_price_map = {
        "Signature Hoodie": 89,
        "Cloud Sweatpants": 78,
        "Zip Hoodie": 96,
        "Lounge Set": 142,
        "Weighted Tee": 54,
    }
    order_value = np.array([unit_price_map[p] for p in product]) * units
    discount = np.where(promo == "none", 0, RNG.choice([0.1, 0.15, 0.2], n_orders))
    order_value = np.round(order_value * (1 - discount), 2)

    base_pick_pack = RNG.normal(1.2, 0.45, n_orders).clip(0.2, 4.5)
    fc_delay = np.select(
        [fc == "3PL_East", fc == "3PL_West", fc == "3PL_Central", fc == "3PL_International"],
        [0.15, 0.35, 0.1, 1.1],
    )
    promo_delay = np.where(np.isin(promo, ["product_launch", "holiday_sale"]), 0.75, 0)
    ship_days = np.round((base_pick_pack + fc_delay + promo_delay + RNG.normal(2.3, 1.0, n_orders)).clip(1, 13), 1)
    promised_days = np.where(country == "United States", 5, 9)
    late = ship_days > promised_days

    shipping_cost = np.round(
        4.25
        + units * 1.15
        + np.where(country == "United States", 0, 7.5)
        + np.select([carrier == "Carrier_D", carrier == "Passport_Global"], [1.8, 4.9], default=0)
        + RNG.normal(0, 0.8, n_orders),
        2,
    ).clip(3, None)

    return_flag = RNG.random(n_orders) < (
        0.055
        + (product == "Lounge Set") * 0.025
        + late * 0.018
        + np.isin(promo, ["holiday_sale", "product_launch"]) * 0.015
    )
    return_reason = np.where(
        return_flag,
        weighted_choice(["fit_issue", "changed_mind", "late_delivery", "quality_issue", "duplicate_order"], [0.32, 0.26, 0.18, 0.16, 0.08], n_orders),
        "none",
    )

    return pd.DataFrame(
        {
            "order_id": [f"ORD{i:06d}" for i in range(1, n_orders + 1)],
            "order_date": pd.to_datetime(order_dates),
            "product_line": product,
            "units": units,
            "order_value": order_value,
            "country": country,
            "fulfillment_center": fc,
            "carrier": carrier,
            "promo_type": promo,
            "shipping_cost": shipping_cost,
            "delivery_days": ship_days,
            "promised_days": promised_days,
            "late_delivery": late,
            "returned": return_flag,
            "return_reason": return_reason,
        }
    )


def build_tickets(orders):
    ticket_rows = []
    categories = ["where_is_my_order", "return_request", "product_question", "damaged_item", "address_change", "cancel_order"]
    channels = ["email", "chat", "social", "sms"]
    agents = ["Aylin", "Maya", "Noor", "Sara", "Zehra", "Layla"]

    for _, order in orders.iterrows():
        ticket_probability = 0.12 + order["late_delivery"] * 0.22 + order["returned"] * 0.18 + (order["promo_type"] == "product_launch") * 0.05
        if RNG.random() >= ticket_probability:
            continue
        created_date = order["order_date"] + pd.Timedelta(days=int(RNG.integers(1, 12)))
        category_weights = [0.39, 0.22, 0.14, 0.11, 0.08, 0.06]
        if order["late_delivery"]:
            category_weights = [0.62, 0.13, 0.07, 0.09, 0.05, 0.04]
        if order["returned"]:
            category_weights = [0.18, 0.52, 0.08, 0.12, 0.05, 0.05]
        category = weighted_choice(categories, category_weights, 1)[0]
        sla_hours = 24 if category in ["damaged_item", "cancel_order"] else 48
        response_hours = max(1, RNG.normal(18, 8) + order["late_delivery"] * 12 + (category == "return_request") * 6)
        resolved_hours = response_hours + max(2, RNG.normal(26, 12))
        breached = response_hours > sla_hours
        sentiment = np.select(
            [breached, category == "damaged_item", category == "product_question"],
            ["negative", "negative", "neutral"],
            default=weighted_choice(["positive", "neutral", "negative"], [0.33, 0.49, 0.18], 1)[0],
        )
        ticket_rows.append(
            {
                "ticket_id": f"TKT{len(ticket_rows) + 1:06d}",
                "order_id": order["order_id"],
                "created_date": created_date,
                "category": category,
                "channel": weighted_choice(channels, [0.43, 0.34, 0.15, 0.08], 1)[0],
                "agent": weighted_choice(agents, [0.18, 0.17, 0.17, 0.16, 0.16, 0.16], 1)[0],
                "first_response_hours": round(response_hours, 1),
                "resolution_hours": round(resolved_hours, 1),
                "sla_hours": sla_hours,
                "sla_breached": bool(breached),
                "sentiment": sentiment,
                "status": weighted_choice(["closed", "closed", "closed", "open", "pending"], [0.58, 0.18, 0.12, 0.07, 0.05], 1)[0],
            }
        )
    return pd.DataFrame(ticket_rows)


def build_daily_forecast(orders, tickets):
    daily_orders = orders.groupby("order_date", as_index=False).agg(
        orders=("order_id", "count"),
        late_rate=("late_delivery", "mean"),
        return_rate=("returned", "mean"),
    )
    daily_tickets = tickets.groupby("created_date", as_index=False).agg(
        tickets=("ticket_id", "count"),
        sla_breaches=("sla_breached", "sum"),
    )
    daily = daily_orders.merge(daily_tickets, left_on="order_date", right_on="created_date", how="left").drop(columns=["created_date"])
    daily[["tickets", "sla_breaches"]] = daily[["tickets", "sla_breaches"]].fillna(0)
    daily["expected_ticket_volume"] = np.round(daily["orders"] * (0.13 + daily["late_rate"] * 0.55 + daily["return_rate"] * 0.4), 0)
    daily["backlog_risk_score"] = np.round((daily["tickets"] * 0.45 + daily["sla_breaches"] * 1.8 + daily["late_rate"] * 100 * 0.35).clip(0, 100), 1)
    daily["risk_level"] = pd.cut(daily["backlog_risk_score"], bins=[-1, 25, 55, 100], labels=["Low", "Medium", "High"])
    return daily


def write_sqlite(orders, tickets, daily):
    db_path = DATA_DIR / "ecommerce_ops.db"
    with sqlite3.connect(db_path) as conn:
        orders.to_sql("orders", conn, if_exists="replace", index=False)
        tickets.to_sql("support_tickets", conn, if_exists="replace", index=False)
        daily.to_sql("daily_operations", conn, if_exists="replace", index=False)
    return db_path


def main():
    orders = build_orders()
    tickets = build_tickets(orders)
    daily = build_daily_forecast(orders, tickets)

    orders.to_csv(DATA_DIR / "orders.csv", index=False)
    tickets.to_csv(DATA_DIR / "support_tickets.csv", index=False)
    daily.to_csv(DATA_DIR / "daily_operations.csv", index=False)
    db_path = write_sqlite(orders, tickets, daily)

    summary = pd.DataFrame(
        [
            {"metric": "orders", "value": len(orders)},
            {"metric": "tickets", "value": len(tickets)},
            {"metric": "late_delivery_rate", "value": round(orders["late_delivery"].mean() * 100, 1)},
            {"metric": "return_rate", "value": round(orders["returned"].mean() * 100, 1)},
            {"metric": "sla_breach_rate", "value": round(tickets["sla_breached"].mean() * 100, 1)},
            {"metric": "avg_shipping_cost", "value": round(orders["shipping_cost"].mean(), 2)},
            {"metric": "high_risk_days", "value": int((daily["risk_level"] == "High").sum())},
        ]
    )
    summary.to_csv(OUTPUTS_DIR / "ops_summary.csv", index=False)
    print(f"Wrote {len(orders):,} orders, {len(tickets):,} tickets, and {len(daily):,} daily rows.")
    print(f"SQLite database: {db_path}")


if __name__ == "__main__":
    main()
