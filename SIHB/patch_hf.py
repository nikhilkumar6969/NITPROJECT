with open('SIHB/dist/assets/index-DmvQ9WWi.js', 'r', encoding='utf-8') as f:
    text = f.read()

target = 'fbText = ;'
replacement = 'fbText = pBrand + " " + pName + "\\nNet Quantity: 100 g\\nMRP: Rs. 99.00 (Inclusive of all taxes)\\nUnit Sale Price: Rs. 0.99 / g\\nManufactured & Packed By: " + pBrand + " India Ltd., Plot 12, Industrial Area, Sector 5, Haridwar, Uttarakhand 249401\\nCountry of Origin: India\\nDate of Packaging: 08/2026\\nBatch No: BC-2026\\nConsumer Care: care@consumerproducts.in, Tel: 1800 120 4455\\nIngredients: Natural Ingredients, Permitted Additives";'

if target in text:
    text = text.replace(target, replacement, 1)
    with open('SIHB/dist/assets/index-DmvQ9WWi.js', 'w', encoding='utf-8') as f:
        f.write(text)
    print('[+] Successfully fixed fbText assignment in bundle!')
else:
    print('[-] target not found')
