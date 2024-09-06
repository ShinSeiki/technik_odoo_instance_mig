select sm.id,
    sm.date_expected,
    sm.product_id,
    sm.name,
    sm.picking_type_id,
    sm.company_id,
    sm.product_qty,
    sm.price_unit,
    product_qty AS u_entrada,
    CASE
        WHEN sm.picking_type_id IS NULL THEN 0
        WHEN sm.picking_type_id = 1 THEN (sm.product_qty * sm.price_unit)
        WHEN sm.picking_type_id = 2 THEN 0
    END as v_entrada,
    CASE
        WHEN sm.picking_type_id IS NULL THEN 0
        WHEN sm.picking_type_id = 1 THEN 0
        WHEN sm.picking_type_id = 2 THEN (sm.product_qty * sm.price_unit)
    END as v_salida,
    sm.state,
    sm.origin,
    sm.reference,
    sl.usage,
    sl.complete_name,
    (sm.location_dest_id) as ubicacion,
    sm.create_uid,
    sm.inventory_id,
    sm.picking_id
from stock_move sm
    inner join stock_location sl on sm.location_dest_id = sl.id
where sm.product_id = 842
    and sm.state = 'done'
    and sl.usage = 'internal'
    and (sm.location_dest_id = 8)
order by date_expected asc