import xml.etree.ElementTree as ET

def scraping(file_path: str):
    data = []
    xml = ET.parse(file_path)
    root = xml.getroot()

    # Namespace usado no XML
    namespace = {'nfe': 'http://www.portalfiscal.inf.br/nfe'}

    # Encontrar todos os elementos da minha nfe
    det_elements = root.findall('.//nfe:det', namespace)
    cnpj = root.find('.//nfe:emit', namespace).find('nfe:CNPJ', namespace).text
    issue_date = root.find('.//nfe:ide', namespace).find('nfe:dhEmi', namespace).text
    name = root.find('.//nfe:emit', namespace).find('nfe:xNome', namespace).text
    fant_name = root.find('.//nfe:emit', namespace).find('nfe:xFant', namespace).text
    invoice_number = root.find('.//nfe:ide', namespace).find('nfe:nNF', namespace).text
    def invoice_value(): return next((vPag.text for vPag in (pag.find('.//vPag') for pag in root.findall('.//pag')) if vPag is not None), None)

    # Iterar sobre cada <det> e extrair informações do <prod>
    for det in det_elements:
        prod = det.find('nfe:prod', namespace)
        if prod is not None:
            description = prod.find('nfe:xProd', namespace).text if prod.find('nfe:xProd', namespace) is not None else ''
            supplier_code = prod.find('nfe:cProd', namespace).text if prod.find('nfe:cProd', namespace) is not None else ''
            barcode = prod.find('nfe:cEAN', namespace).text if prod.find('nfe:cEAN', namespace) is not None else ''

            ncm = prod.find('nfe:NCM', namespace).text if prod.find('nfe:NCM', namespace) is not None else ''
            cest = prod.find('nfe:CEST', namespace).text if prod.find('nfe:CEST', namespace) is not None else ''

            purchase_price = prod.find('nfe:vUnCom', namespace).text if prod.find('nfe:vUnCom', namespace) is not None else '0.00'
            purchase_price = f"{float(purchase_price):.2f}"
        
            data.append({
                'invoice': {
                    'invoice_number': invoice_number,
                    'issue_date': issue_date,
                    'invoice_value': invoice_value()
                },
                'supplier': {
                    'name': name,
                    'fant_name': fant_name,
                    'cnpj': cnpj
                },
                'product': {
                    'supplier_code': supplier_code ,
                    'description': description,
                    'barcode': barcode,
                    'ncm': ncm,
                    'cest': cest,
                    'purchase_price': purchase_price
            }})
    return data
