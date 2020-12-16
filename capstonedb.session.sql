Select TotalPaid - TotalCost as TotalProfit
    c.name
From (
SELECT item_cost + shipping_cost + listing_fee + final_value_fee as TotalCost,
    item_paid + shipping_paid as TotalPaid,
    title
From finalcapstoneapi_item as i
WHERE sold_date is not NULL
) 
Join finalcapstoneapi_category c on c.id = i.category_id
Group BY i.category_id