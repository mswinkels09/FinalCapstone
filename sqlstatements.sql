-- Profit by category --
Select Sum(TotalPaid - TotalCost) as TotalProfit,
    ItemTitle,
    CategoryName
From (
        SELECT i.item_cost + i.shipping_cost + i.listing_fee + i.final_value_fee as TotalCost,
            i.item_paid + i.shipping_paid as TotalPaid,
            i.title as ItemTitle,
            c.name as CategoryName
        From finalcapstoneapi_item as i
            Join finalcapstoneapi_category c on c.id = i.category_id
        WHERE sold_date is not NULL
    )
Group BY CategoryName;

SELECT "finalcapstoneapi_category"."id",
    "finalcapstoneapi_category"."name",
    SUM(
        (
            (
                (
                    (
                        (
                            "finalcapstoneapi_item"."shipping_paid" + "finalcapstoneapi_item"."item_paid"
                        ) - "finalcapstoneapi_item"."item_cost"
                    ) - "finalcapstoneapi_item"."shipping_cost"
                ) - "finalcapstoneapi_item"."listing_fee"
            ) - "finalcapstoneapi_item"."final_value_fee"
        )
    ) FILTER (
        WHERE "finalcapstoneapi_item"."user_id" = 1
    ) AS "profit"
FROM "finalcapstoneapi_category"
    LEFT OUTER JOIN "finalcapstoneapi_item" ON (
        "finalcapstoneapi_category"."id" = "finalcapstoneapi_item"."category_id"
    )
GROUP BY "finalcapstoneapi_category"."id",
    "finalcapstoneapi_category"."name"



-- Expenses By Month
select strftime('%m', date_purchased) as Month, 
sum(cost)
from finalcapstoneapi_expenses
where strftime('%Y', date_purchased) = strftime('%Y',date('now'))
group by strftime('%m', date_purchased)
order by Month;
