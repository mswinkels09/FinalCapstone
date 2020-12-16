
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
Group BY CategoryName