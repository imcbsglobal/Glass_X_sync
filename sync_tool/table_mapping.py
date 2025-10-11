TABLE_MAPPING = {
    "products": {
        "table": "acc_product",
        "columns": "code, name, product, brand, unit, taxcode, defect, company"
    },
    "batches": {
        "table": "acc_productbatch",
        "columns": "productcode, cost, salesprice, bmrp, barcode, secondprice, thirdprice"
    },
    "customers": {
        "table": "acc_master",
        "columns": "code, name, super_code, address, phone, phone2",
        "condition": "super_code = 'DEBTO'"
    },
    "users": {
        "table": "acc_users",
        "columns": "id, pass AS pass_field, role"
    }
}
