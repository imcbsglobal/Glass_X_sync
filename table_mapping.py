TABLE_MAPPING = {
    "products": {
        "table": "acc_product",
        "columns": "code, name, product, brand, unit, taxcode, defect, company"
    },
    "batches": {
        "table": "acc_productbatch",
        "columns": """
            productcode, 
            cost, 
            salesprice, 
            bmrp, 
            barcode, 
            secondprice, 
            thirdprice, 
            fourthprice,
            (SELECT name FROM acc_pricecode WHERE code = 'CO') AS cost_name,
            (SELECT name FROM acc_pricecode WHERE code = 'S1') AS sales_price_name,
            (SELECT name FROM acc_pricecode WHERE code = 'MR') AS bmrp_name,
            (SELECT name FROM acc_pricecode WHERE code = 'S2') AS secondprice_name,
            (SELECT name FROM acc_pricecode WHERE code = 'S3') AS thirdprice_name,
            (SELECT name FROM acc_pricecode WHERE code = 'S4') AS fourthprice_name
        """
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
